#!/usr/bin/env python3
"""Pull the music out of a YouTube watch history into /music/.

Writes images/music/ and _data/music.yml, the way scripts/pinterest-art.py
writes the art page. Everything comes out of yt-dlp; nothing here talks to
YouTube itself.

Watch history is a signed-in page, so this needs cookies and cannot be run
without them. By default it reads them straight from a browser profile
(--browser, default brave), which is yt-dlp's --cookies-from-browser; on macOS
that reads the browser's own cookie store and may want the keychain. A
cookies.txt exported by hand works too, via --cookies. Neither is written into
the repo, and .gitignore keeps the usual names out of it.

Two passes, because the cheap one cannot answer the question:

  * the history feed lists ids and titles and nothing else -- `--flat-playlist`
    is one request for the lot, and none of what comes back says whether a
    video is music.
  * so every unique id is then extracted properly, one request each, and kept
    only if YouTube's own category for it is Music. That is the uploader's
    label rather than a guess from the title, which is why a "Topic" auto-upload
    and a 3-hour jazz mix both land correctly and a podcast about music does
    not.

The history feed caps out around 350 entries no matter what --limit says; that
is YouTube's, not ours. Roughly one in twenty is music, so expect a page of
tens rather than hundreds.

    ./scripts/youtube-music.py
    ./scripts/youtube-music.py --browser chrome
    ./scripts/youtube-music.py --cookies ~/cookies.txt --limit 100

Re-running is cheap: a cover already on disk is not fetched again, and the
order in the file is history order, most recently played first.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT, "images", "music")
DATA_FILE = os.path.join(ROOT, "_data", "music.yml")

HISTORY = "https://www.youtube.com/feed/history"
WATCH = "https://www.youtube.com/watch?v={}"
# hqdefault is the one thumbnail every video has. maxres is nicer and often
# missing, so it is tried first and this is the fallback rather than the plan.
THUMBS = ("https://i.ytimg.com/vi/{}/maxresdefault.jpg",
          "https://i.ytimg.com/vi/{}/hqdefault.jpg")

# The fields the page actually shows, asked for as one JSON object per video.
FIELDS = "%(.{id,title,channel,channel_url,categories,duration})j"

# Videos YouTube files under Music that are not music: a vlog whose uploader
# picked the category once and never revisited it. Dropped by id here rather
# than by some heuristic on the title, because there is no rule that separates
# these from a real track -- only a person looking at them.
DROPPED = {
    "-oW3k3RxUr4",  # a Vancouver breakup vlog, categorised Music
    "Sbcq7TZLQA4",  # a DAC calibration walkthrough, categorised Music
}


def yt_dlp(args, cookie_args, capture=True):
    cmd = ["yt-dlp", "--no-warnings", "--ignore-errors"] + cookie_args + args
    proc = subprocess.run(cmd, capture_output=capture, text=True)
    if proc.returncode != 0 and not (proc.stdout or "").strip():
        sys.exit("yt-dlp failed: " + (proc.stderr or "").strip().splitlines()[-1]
                 if (proc.stderr or "").strip() else "yt-dlp failed")
    return (proc.stdout or "").splitlines()


def history_ids(cookie_args, limit, verbose):
    """Every video in the history feed, most recent first, de-duplicated.

    Order is kept rather than sorted: it is the only thing the flat listing
    knows that the per-video pass does not, and it is what the page is ordered
    by. A video watched twice keeps its earlier -- more recent -- place.
    """
    lines = yt_dlp(["--flat-playlist", "--playlist-end", str(limit),
                    "--print", "%(id)s", HISTORY], cookie_args)
    seen, ids = set(), []
    for vid in (l.strip() for l in lines):
        if vid and vid not in seen:
            seen.add(vid)
            ids.append(vid)
    if verbose:
        print(f"{len(ids)} videos in history ({len(lines)} plays)")
    return ids


def describe(ids, cookie_args, verbose):
    """Full metadata for each id, in one yt-dlp run rather than one per video.

    yt-dlp takes many URLs at once and prints a line per video, so the whole
    pass is a single process; --ignore-errors keeps a deleted or private video
    from ending the run, and its line simply never arrives.
    """
    urls = [WATCH.format(v) for v in ids]
    lines = yt_dlp(["--skip-download", "--print", FIELDS] + urls, cookie_args)
    by_id = {}
    for line in lines:
        line = line.strip()
        if not line.startswith("{"):
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        if row.get("id"):
            by_id[row["id"]] = row
    if verbose:
        print(f"{len(by_id)} of {len(ids)} still playable")
    return by_id


def is_music(row):
    return "Music" in (row.get("categories") or [])


def cover(video_id, verbose):
    """Mirror the thumbnail into images/music/, and say what it is called.

    Mirrored rather than hotlinked for the same reason the pins are: i.ytimg.com
    keeps serving a thumbnail only as long as the video exists, and a page of
    live thumbnail URLs goes to grey boxes the day one is taken down.
    """
    # Jekyll skips any file whose name starts with an underscore, so an id
    # like _ABk7TmjnVk would be mirrored here and then never copied into
    # _site -- a broken cover with the file sitting right there. Ids are
    # always 11 characters, so the "v" prefix cannot collide with a real one.
    name = f"{video_id}.jpg"
    if name.startswith("_"):
        name = "v" + name
    path = os.path.join(IMAGE_DIR, name)
    if os.path.exists(path):
        return name
    for url in THUMBS:
        try:
            with urllib.request.urlopen(url.format(video_id), timeout=30) as res:
                blob = res.read()
        except (urllib.error.URLError, TimeoutError):
            continue
        # A missing maxres answers 404, but a few of YouTube's placeholder
        # responses come back 200 and tiny, so size is the real test.
        if len(blob) < 2000:
            continue
        with open(path, "wb") as fh:
            fh.write(blob)
        if verbose:
            print(f"  saved {name}  ({len(blob) // 1024} KB)")
        return name
    print(f"  ! no cover reachable for {video_id}", file=sys.stderr)
    return None


def clock(seconds):
    """Duration as a person writes it: 3:41, or 1:23:45 past the hour."""
    seconds = int(seconds or 0)
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def yaml_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def write_data(entries):
    lines = [
        "# Written by scripts/youtube-music.py -- edit that, not this.",
        "# One entry per track behind /music/, in the order it was played:",
        "# the cover under images/music/, what it is, and the video it was",
        "# played from so each cover keeps a way back to the source.",
        "",
    ]
    for entry in entries:
        lines.append(f"- file: {yaml_quote(entry['file'])}")
        lines.append(f"  title: {yaml_quote(entry['title'])}")
        lines.append(f"  channel: {yaml_quote(entry['channel'])}")
        lines.append(f"  channel_url: {yaml_quote(entry['channel_url'])}")
        lines.append(f"  duration: {yaml_quote(entry['duration'])}")
        lines.append(f"  link: {yaml_quote(entry['link'])}")
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--browser", default="brave",
                        help="browser profile to read cookies from "
                             "(yt-dlp's --cookies-from-browser). Default: brave")
    parser.add_argument("--cookies",
                        help="cookies.txt to use instead of a browser profile")
    parser.add_argument("--limit", type=int, default=400,
                        help="how deep into the history to look. YouTube stops "
                             "answering around 350 whatever this says")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    verbose = not args.quiet

    cookie_args = (["--cookies", args.cookies] if args.cookies
                   else ["--cookies-from-browser", args.browser])

    os.makedirs(IMAGE_DIR, exist_ok=True)
    ids = history_ids(cookie_args, args.limit, verbose)
    rows = describe(ids, cookie_args, verbose)

    entries = []
    for video_id in ids:
        row = rows.get(video_id)
        if not row or not is_music(row) or video_id in DROPPED:
            continue
        name = cover(video_id, verbose)
        if not name:
            continue
        entries.append({
            "file": name,
            "title": row.get("title") or video_id,
            "channel": row.get("channel") or "",
            "channel_url": row.get("channel_url") or "",
            "duration": clock(row.get("duration")),
            "link": WATCH.format(video_id),
        })

    write_data(entries)
    print(f"{len(entries)} track(s) -> images/music/ and _data/music.yml")


if __name__ == "__main__":
    main()
