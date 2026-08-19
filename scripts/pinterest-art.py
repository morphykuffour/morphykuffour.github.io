#!/usr/bin/env python3
"""Pull the pins off a Pinterest account into images/art/ and _data/art.yml.

Nothing here is scraped off the rendered page: logged out, pinterest.com serves
an empty SPA shell with not one pin in it. The pins come from the same web API
the site calls for itself -- which is also where the Pinterest Power Menu
userscript gets its URLs from. Three of that script's findings are reused:

  * pins are served at i.pinimg.com/<size>x/ab/cd/ef/<hash>.jpg and the
    full-resolution file is the same path under /originals/, sometimes with a
    different extension than the thumbnail advertises. Hence the candidate
    walk in `download`.
  * the API wants the csrftoken cookie echoed back in an X-CSRFToken header.
    Without it every endpoint answers a bare 403 `Invalid Resource Request`,
    with no hint that a cookie is what is missing. An X-Pinterest-PWS-Handler
    naming the page the call is supposed to come from is the second half of
    that gate -- the same 403, and the same silence about why.
  * i.pinimg.com refuses a request with no Referer from the site itself.

A public profile needs no credentials: `bootstrap` fetches the profile page
once purely to be handed a cookie jar, and that anonymous session is enough.
A private one is not readable this way at all -- the API answers `4808 This
account is private` for every board on it -- so for that case only, a
signed-in Cookie header can be supplied via --cookies (a file holding the
string devtools copies out of a request's Cookie header) or the
PINTEREST_COOKIE variable. The file is read, never written, and .gitignore
keeps the usual name out of the repo.

    ./scripts/pinterest-art.py
    ./scripts/pinterest-art.py --board wallpapers --limit 60
    ./scripts/pinterest-art.py --cookies .pinterest-cookie   # private account

Re-running is cheap: an image already on disk is not fetched again, so the
normal update is a second run that only pulls what is new.
"""

import argparse
import http.cookiejar
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT, "images", "art")
DATA_FILE = os.path.join(ROOT, "_data", "art.yml")

API = "https://www.pinterest.com/resource/{}/get/"
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36")

# Extensions Pinterest actually stores originals under. The thumbnail URL's
# own extension is only a hint -- a .jpg thumbnail regularly has a .png or
# .webp original -- so each is tried in turn before giving up on /originals/.
ORIGINAL_EXTS = ("jpg", "png", "webp", "gif")


def parse_cookies(raw):
    """`a=1; b=2` -> {'a': '1', 'b': '2'}, ignoring blank and comment lines."""
    jar = {}
    for line in raw.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for part in line.split(";"):
            if "=" not in part:
                continue
            name, value = part.split("=", 1)
            jar[name.strip()] = value.strip()
    return jar


def supplied_cookies(path):
    """A Cookie header the user pasted, or {} if they passed none."""
    raw = ""
    if path:
        with open(path, encoding="utf-8") as fh:
            raw = fh.read()
    elif os.environ.get("PINTEREST_COOKIE"):
        raw = os.environ["PINTEREST_COOKIE"]
    if not raw.strip():
        return {}
    jar = parse_cookies(raw)
    if "csrftoken" not in jar:
        sys.exit("pinterest-art: the supplied cookies carry no csrftoken. "
                 "Copy the whole Cookie header, not just the session.")
    return jar


class Client:
    """Everything goes through one opener holding one cookie jar.

    The jar has to be a real one rather than a dict of Set-Cookie headers off
    a single response: the profile URL redirects, and the cookies that matter
    are handed out across the hops of that chain, not all on the last one.
    """

    def __init__(self, seed=None):
        self.cookies = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(self.cookies))
        for name, value in (seed or {}).items():
            self.cookies.set_cookie(http.cookiejar.Cookie(
                0, name, value, None, False, ".pinterest.com", True, True,
                "/", True, True, None, False, None, None, {}))

    def warm_up(self, username):
        """One GET of the profile page, purely to be handed a cookie jar."""
        req = urllib.request.Request("https://www.pinterest.com/%s/" % username,
                                     headers={"User-Agent": UA})
        try:
            self.opener.open(req, timeout=30).read()
        except urllib.error.URLError as err:
            sys.exit(f"pinterest-art: could not reach the profile page: {err}")
        if not self.csrf():
            sys.exit("pinterest-art: pinterest handed back no csrftoken; the "
                     "API will refuse every call. Try again, or pass --cookies.")

    def csrf(self):
        for cookie in self.cookies:
            if cookie.name == "csrftoken":
                return cookie.value
        return ""

    def _open(self, url, headers, binary=False):
        req = urllib.request.Request(url, headers=headers)
        with self.opener.open(req, timeout=30) as resp:
            return resp.read() if binary else resp.read().decode("utf-8")

    def call(self, endpoint, options, source_url, handler):
        """One Pinterest resource call. Returns (data, bookmark).

        `handler` names the site page this call is pretending to come from.
        Pinterest checks it: with the right cookies, the right CSRF header and
        no handler, every endpoint here answers 403 `Invalid Resource Request`.
        X-APP-VERSION, which the browser also sends, turns out not to matter.
        """
        query = urllib.parse.urlencode({
            "source_url": source_url,
            "data": json.dumps({"options": options, "context": {}}),
        })
        headers = {
            "User-Agent": UA,
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            # Echoing the cookie back as a header is what separates a 200 from
            # a bare 403 here; the session cookie alone is not enough.
            "X-CSRFToken": self.csrf(),
            "X-Pinterest-PWS-Handler": handler,
            "X-Pinterest-AppState": "active",
            "Referer": "https://www.pinterest.com" + source_url,
        }
        try:
            body = self._open(API.format(endpoint) + "?" + query, headers)
        except urllib.error.HTTPError as err:
            detail = err.read().decode("utf-8", "replace")[:300]
            sys.exit(f"pinterest-art: {endpoint} answered {err.code}. {detail}")
        payload = json.loads(body)
        response = payload.get("resource_response", {})
        if response.get("status") != "success":
            message = (response.get("error") or {}).get("message", "unknown error")
            sys.exit(f"pinterest-art: {endpoint} refused the request: {message}")
        return response.get("data"), response.get("bookmark")

    def paged(self, endpoint, options, source_url, handler, limit):
        """Walk an endpoint's bookmarks until it runs dry or `limit` is met."""
        seen = []
        bookmark = None
        while True:
            page_options = dict(options)
            if bookmark:
                page_options["bookmarks"] = [bookmark]
            data, bookmark = self.call(endpoint, page_options, source_url, handler)
            items = [d for d in (data or []) if isinstance(d, dict)]
            seen.extend(items)
            # Pinterest signals the end of a feed with this sentinel rather
            # than by dropping the bookmark, and repeats the last page forever
            # if it is followed.
            if not items or not bookmark or bookmark == "-end-":
                break
            if limit and len(seen) >= limit:
                break
            time.sleep(0.4)
        return seen[:limit] if limit else seen

    def fetch(self, url):
        headers = {
            "User-Agent": UA,
            # pinimg answers 403 without a Referer from the site itself.
            "Referer": "https://www.pinterest.com/",
            "Accept": "image/webp,image/apng,image/*,*/*;q=0.8",
        }
        return self._open(url, headers, binary=True)


def originals(url):
    """Descending-quality candidates for a pin image URL, best first."""
    match = re.match(
        r"^(https?://i\.pinimg\.com)/(?:originals|\d+x)"
        r"(/[0-9a-f]{2}/[0-9a-f]{2}/[0-9a-f]{2}/[^/?#]+)$", url or "")
    if not match:
        return [url] if url else []
    base, path = match.groups()
    stem = re.sub(r"\.[^.]+$", "", path)
    out = [f"{base}/originals{stem}.{ext}" for ext in ORIGINAL_EXTS]
    out.append(f"{base}/736x{path}")
    return list(dict.fromkeys(out))


def best_image_url(pin):
    """The largest image URL Pinterest offers for a pin, before upgrading."""
    images = pin.get("images") or {}
    if isinstance(images.get("orig"), dict) and images["orig"].get("url"):
        return images["orig"]["url"]
    sized = [(int(re.match(r"(\d+)", key).group(1)), value.get("url"))
             for key, value in images.items()
             if isinstance(value, dict) and re.match(r"\d+", key) and value.get("url")]
    if sized:
        return max(sized)[1]
    story = pin.get("story_pin_data") or {}
    for page in story.get("pages") or []:
        for block in page.get("blocks") or []:
            block_images = (block.get("image") or {}).get("images") or {}
            orig = block_images.get("originals") or block_images.get("orig")
            if isinstance(orig, dict) and orig.get("url"):
                return orig["url"]
    return None


def pin_title(pin):
    for key in ("grid_title", "title", "seo_title", "description",
                "auto_alt_text", "closeup_unified_description"):
        value = (pin.get(key) or "").strip()
        if value:
            return re.sub(r"\s+", " ", value)[:120]
    return ""


def sniff_ext(blob):
    """Extension from the file's own magic bytes, not from the URL's claim."""
    if blob[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png"
    if blob[:3] == b"\xff\xd8\xff":
        return ".jpg"
    if blob[:6] in (b"GIF87a", b"GIF89a"):
        return ".gif"
    if blob[:4] == b"RIFF" and blob[8:12] == b"WEBP":
        return ".webp"
    return ".jpg"


def download(client, pin, verbose):
    """Save a pin's best available image. Returns its repo-relative name."""
    url = best_image_url(pin)
    if not url:
        return None
    pin_id = str(pin.get("id") or "")
    existing = [n for n in os.listdir(IMAGE_DIR) if os.path.splitext(n)[0] == pin_id]
    if existing:
        return existing[0]
    for candidate in originals(url):
        try:
            blob = client.fetch(candidate)
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError):
            continue
        if len(blob) < 1024:          # an error page dressed as an image
            continue
        name = pin_id + sniff_ext(blob)
        with open(os.path.join(IMAGE_DIR, name), "wb") as fh:
            fh.write(blob)
        if verbose:
            print(f"  saved {name}  ({len(blob) // 1024} KB)")
        return name
    print(f"  ! no image reachable for pin {pin_id}", file=sys.stderr)
    return None


def yaml_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def write_data(entries):
    lines = [
        "# Written by scripts/pinterest-art.py -- edit that, not this.",
        "# One entry per pin behind /art/: the file under images/art/, the",
        "# caption, and the pin it was saved from so each image keeps a way",
        "# back to its source.",
        "",
    ]
    for entry in entries:
        lines.append(f"- file: {yaml_quote(entry['file'])}")
        lines.append(f"  title: {yaml_quote(entry['title'])}")
        lines.append(f"  link: {yaml_quote(entry['link'])}")
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--username", default="morphykuffour")
    parser.add_argument("--cookies",
                        help="file holding a signed-in Cookie header; only "
                             "needed for a private account")
    parser.add_argument("--board", action="append", default=[],
                        help="board name or slug; repeatable. Default: every board")
    parser.add_argument("--limit", type=int, default=0,
                        help="stop after this many pins (0 = all)")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    verbose = not args.quiet

    os.makedirs(IMAGE_DIR, exist_ok=True)
    client = Client(supplied_cookies(args.cookies))
    client.warm_up(args.username)
    profile = "/" + args.username + "/"

    boards = client.paged("BoardsResource", {
        "username": args.username,
        "field_set_key": "profile_grid_item",
        "privacy_filter": "all",
        "sort": "last_pinned_to",
        "page_size": 25,
    }, profile, "www/[username].js", 0)
    if args.board:
        wanted = {b.lower() for b in args.board}
        boards = [b for b in boards
                  if (b.get("name") or "").lower() in wanted
                  or (b.get("url") or "").strip("/").split("/")[-1].lower() in wanted]
        if not boards:
            sys.exit("pinterest-art: no board matched " + ", ".join(args.board))
    if verbose:
        print(f"{len(boards)} board(s): " + ", ".join(b.get("name", "?") for b in boards))

    entries, seen_pins = [], set()
    for board in boards:
        remaining = args.limit - len(entries) if args.limit else 0
        if args.limit and remaining <= 0:
            break
        if verbose:
            print(f"- {board.get('name')} ({board.get('pin_count', '?')} pins)")
        pins = client.paged("BoardFeedResource", {
            "board_id": board.get("id"),
            "field_set_key": "react_grid_pin",
            "page_size": 25,
            "prepend": False,
            "add_vase": True,
        }, board.get("url") or profile, "www/[username]/[slug].js", remaining)
        for pin in pins:
            # Pinterest injects one `type: "story"` card per board feed -- a
            # "more ideas" promo, not a saved pin. Dropping it by type rather
            # than by "it had no image we could fetch" keeps that path free to
            # report a pin that genuinely failed to download.
            if pin.get("type") not in (None, "pin"):
                continue
            pin_id = str(pin.get("id") or "")
            if not pin_id or pin_id in seen_pins:
                continue
            seen_pins.add(pin_id)
            name = download(client, pin, verbose)
            if not name:
                continue
            entries.append({
                "file": name,
                "title": pin_title(pin),
                "link": f"https://www.pinterest.com/pin/{pin_id}/",
            })

    write_data(entries)
    print(f"{len(entries)} pin(s) -> images/art/ and _data/art.yml")


if __name__ == "__main__":
    main()
