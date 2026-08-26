#!/usr/bin/env python3
"""Pull the playlists behind /cybersecurity/ into images and data.

Writes images/cybersecurity/ and _data/cybersecurity.yml, the way
scripts/youtube-music.py writes the music page. Everything comes out of
yt-dlp; nothing here talks to YouTube itself.

Public playlists, so unlike the music script this needs no cookies and no
signed-in anything -- a playlist id is enough. One flat listing per playlist
is one request for the lot, and a flat listing already carries the id, the
title and the duration, which is everything a cover needs. There is no second
per-video pass because there is no question to ask: a playlist put together by
hand is already the filter that the music script has to reconstruct from
YouTube's category field.

PLAYLISTS below is the page. What is on it is the list here, in this order, and
the note beside each one is the reason it is here -- written by a person, kept
in the script rather than the data file because the data file is rewritten
wholesale on every run and a note in it would last exactly until the next one.

The other half of the page is a talk that belongs to no playlist. Those go in
_data/cybersecurity_local.yml, hand-kept for the reason _data/music_local.yml
is: a run rewrites cybersecurity.yml wholesale, so an entry added to it by
hand would last exactly until the next one. --add writes to that file and
touches nothing else, which is why it takes a URL and needs no playlist.

    ./scripts/youtube-cyber.py
    ./scripts/youtube-cyber.py --quiet
    ./scripts/youtube-cyber.py --add https://www.youtube.com/watch?v=...

Re-running is cheap: a cover already on disk is not fetched again, and a
playlist that has grown since the last run simply comes back longer.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT, "images", "cybersecurity")
DATA_FILE = os.path.join(ROOT, "_data", "cybersecurity.yml")
LOCAL_FILE = os.path.join(ROOT, "_data", "cybersecurity_local.yml")

PLAYLIST = "https://www.youtube.com/playlist?list={}"
WATCH = "https://www.youtube.com/watch?v={}"
# hqdefault is the one thumbnail every video has. maxres is nicer and often
# missing, so it is tried first and this is the fallback rather than the plan.
THUMBS = ("https://i.ytimg.com/vi/{}/maxresdefault.jpg",
          "https://i.ytimg.com/vi/{}/hqdefault.jpg")

# One line per playlist on the page, in the order they appear on it.
#
#   id    the list= of the playlist URL.
#   note  why it is here. Mine, not YouTube's description of it.
PLAYLISTS = [
    {
        "id": "PLyAXNQGte3qPMk5XvACx4lQslwXcqUJrh",
        "note": "Power analysis and fault injection done on a bench rather "
                "than on a slide: a scope, a target board and a key coming "
                "out of a chip that never leaked it in software. The two-hour "
                "CHES tutorial is the one to sit down with; the two-minute "
                "demos are what make you believe it first.",
    },
    {
        "id": "PLnzpmyOBy8Cgmg1puLtovvS5adTwUuEm4",
        "note": "The other half of the subject: not breaking a chip on a "
                "bench but living with the machines you already carry. A "
                "compartmentalised desktop, a phone with Google taken out of "
                "it, and a cheap hotspot turned into a detector for the "
                "fake cell towers that log which phones walked past. Setup "
                "walkthroughs rather than arguments -- each one is somebody "
                "doing the install with the awkward parts left in.",
    },
]

# Entries a flat listing hands back for a video that is no longer there. They
# have an id and a placeholder title and nothing else, so they would mirror as
# a missing cover and read on the page as a track with no picture.
GONE = ("[Private video]", "[Deleted video]", "[Unavailable video]")


def yt_dlp(args):
    cmd = ["yt-dlp", "--no-warnings", "--ignore-errors"] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 and not (proc.stdout or "").strip():
        last = (proc.stderr or "").strip().splitlines()
        sys.exit("yt-dlp failed: " + (last[-1] if last else "no output"))
    return (proc.stdout or "").splitlines()


def listing(playlist_id, verbose):
    """A playlist as (title, channel, channel_url, videos), in playlist order.

    Printed as tab-separated fields rather than JSON: every field here is one
    of YouTube's own strings and a tab is the one character none of them can
    contain, whereas a title with a brace in it is ordinary.
    """
    fields = "\t".join(("%(playlist_title)s", "%(playlist_channel)s",
                        "%(playlist_channel_id)s", "%(id)s", "%(title)s",
                        "%(duration)s"))
    lines = yt_dlp(["--flat-playlist", "--print", fields,
                    PLAYLIST.format(playlist_id)])
    title, channel, channel_id, videos = "", "", "", []
    for line in lines:
        parts = line.rstrip("\n").split("\t")
        if len(parts) != 6:
            continue
        title, channel, channel_id, vid, name, secs = parts
        if not vid or name in GONE:
            continue
        videos.append({"id": vid, "title": name, "duration": secs})
    if verbose:
        print(f"{title or playlist_id}: {len(videos)} video(s)")
    channel_url = (f"https://www.youtube.com/channel/{channel_id}"
                   if channel_id and channel_id != "NA" else "")
    return title, ("" if channel == "NA" else channel), channel_url, videos


def cover(video_id, verbose):
    """Mirror the thumbnail into images/cybersecurity/, and name the file.

    Mirrored rather than hotlinked for the reason the covers on /music/ are:
    i.ytimg.com serves a thumbnail only as long as its video exists, so a page
    of live thumbnail URLs turns into grey boxes the day one is taken down.
    """
    # Jekyll skips any file whose name starts with an underscore, so an id like
    # _ABk7TmjnVk would be mirrored here and then never copied into _site.
    # Ids are always 11 characters, so the "v" prefix cannot collide with one.
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
    try:
        seconds = int(float(seconds))
    except (TypeError, ValueError):
        return ""
    h, rest = divmod(seconds, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


def yaml_quote(value):
    return "'" + str(value).replace("'", "''") + "'"


def write_data(playlists):
    lines = [
        "# Written by scripts/youtube-cyber.py -- edit that, not this.",
        "# One entry per playlist behind /cybersecurity/, in the order the",
        "# page shows them: what the playlist is, whose it is, the note",
        "# saying why it is here, and every video in it with the cover",
        "# mirrored under images/cybersecurity/.",
        "",
    ]
    for playlist in playlists:
        lines.append(f"- title: {yaml_quote(playlist['title'])}")
        lines.append(f"  url: {yaml_quote(playlist['url'])}")
        lines.append(f"  channel: {yaml_quote(playlist['channel'])}")
        lines.append(f"  channel_url: {yaml_quote(playlist['channel_url'])}")
        lines.append(f"  note: {yaml_quote(playlist['note'])}")
        lines.append("  videos:")
        for video in playlist["videos"]:
            lines.append(f"    - file: {yaml_quote(video['file'])}")
            lines.append(f"      title: {yaml_quote(video['title'])}")
            lines.append(f"      duration: {yaml_quote(video['duration'])}")
            lines.append(f"      link: {yaml_quote(video['link'])}")
    with open(DATA_FILE, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


LOCAL_HEADER = """\
# Hand-kept, unlike _data/cybersecurity.yml: talks put on the page one at a
# time rather than pulled from a playlist. They live in a second file because
# scripts/youtube-cyber.py rewrites cybersecurity.yml wholesale on every run,
# so an entry added to it by hand would survive until the next update and no
# longer.
#
# Written by `youtube-cyber.py --add <url>`, newest first, and plain enough to
# edit or delete an entry by hand afterwards.
"""


def add_one(url, verbose):
    """Put one video at the top of the hand-kept file, cover and all.

    The one place this script asks yt-dlp about a video rather than a
    playlist. Printed as JSON rather than the tab-separated fields a listing
    uses: a single line is being read, and a title with a brace in it is no
    trouble to the parser that a title with a tab would be.
    """
    fields = "%(.{id,title,channel,channel_url,duration})j"
    lines = yt_dlp(["--skip-download", "--print", fields, url])
    row = next((json.loads(l) for l in lines if l.strip().startswith("{")), None)
    if not row or not row.get("id"):
        sys.exit(f"nothing playable at {url}")

    text = LOCAL_HEADER
    if os.path.exists(LOCAL_FILE):
        text = open(LOCAL_FILE, encoding="utf-8").read()
    link = WATCH.format(row["id"])
    if link in text:
        print(f"already there: {row['title']}")
        return

    os.makedirs(IMAGE_DIR, exist_ok=True)
    name = cover(row["id"], verbose)
    if not name:
        sys.exit(f"no cover for {row['id']}, so nothing added")
    entry = (f"- file: {yaml_quote(name)}\n"
             f"  title: {yaml_quote(row.get('title') or row['id'])}\n"
             f"  channel: {yaml_quote(row.get('channel') or '')}\n"
             f"  channel_url: {yaml_quote(row.get('channel_url') or '')}\n"
             f"  duration: {yaml_quote(clock(row.get('duration')))}\n"
             f"  link: {yaml_quote(link)}\n")
    # Newest first, so the insertion point is above the first entry rather
    # than the end of the file -- and the header, which is the whole file
    # until there is a first entry, stays on top either way.
    cut = text.find("- file:")
    head, rest = (text, "") if cut == -1 else (text[:cut], text[cut:])
    if not head.endswith("\n\n"):
        head = head.rstrip("\n") + "\n\n"
    with open(LOCAL_FILE, "w", encoding="utf-8") as fh:
        fh.write(head + entry + rest)
    print(f"added: {row['title']}  [{clock(row.get('duration'))}]"
          " -> _data/cybersecurity_local.yml")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--add", metavar="URL",
                        help="put one video at the top of the hand-kept file "
                             "and stop, leaving the playlists alone")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    verbose = not args.quiet

    # An early return rather than a mode flag threaded through the rest: the
    # two jobs share the cover mirror and nothing else, and a run that pulled
    # every playlist as a side effect of adding one talk would be a surprise.
    if args.add:
        add_one(args.add, verbose)
        return

    os.makedirs(IMAGE_DIR, exist_ok=True)
    out, total = [], 0
    for entry in PLAYLISTS:
        title, channel, channel_url, videos = listing(entry["id"], verbose)
        kept = []
        for video in videos:
            name = cover(video["id"], verbose)
            if not name:
                continue
            kept.append({
                "file": name,
                "title": video["title"],
                "duration": clock(video["duration"]),
                "link": WATCH.format(video["id"]),
            })
        total += len(kept)
        out.append({
            "title": title or entry["id"],
            "url": PLAYLIST.format(entry["id"]),
            "channel": channel,
            "channel_url": channel_url,
            "note": entry["note"],
            "videos": kept,
        })

    write_data(out)
    print(f"{len(out)} playlist(s), {total} video(s) -> "
          "images/cybersecurity/ and _data/cybersecurity.yml")


if __name__ == "__main__":
    main()
