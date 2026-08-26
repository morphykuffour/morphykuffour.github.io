#!/usr/bin/env python3
"""Pull the talks behind /investment/ into images and data.

Writes images/investment/ and _data/investment.yml, the way
scripts/youtube-cyber.py writes the cybersecurity page. Everything comes out
of yt-dlp; nothing here talks to YouTube itself.

Public videos, so like the cybersecurity script and unlike the music one this
needs no cookies and no signed-in anything -- a video id is enough.

Loose videos rather than playlists, which is the difference from
scripts/youtube-cyber.py and the reason this is a second script rather than a
flag on that one. A trading firm's engineering channel is not a course: the
talks are hours long, unrelated to each other, and posted years apart, so what
is worth keeping is a handful of them and not the feed they came from. There
is nothing to walk in order, so VIDEOS below is the order, chosen here.

VIDEOS is the page. What is on it is the list here, in this order, and each
id is fetched once for its title, channel and duration -- one yt-dlp run for
the lot, the way the music script's second pass works.

    ./scripts/youtube-invest.py
    ./scripts/youtube-invest.py --quiet

Re-running is cheap: a cover already on disk is not fetched again, and a video
that has been taken down since the last run simply drops off the page.
"""

import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGE_DIR = os.path.join(ROOT, "images", "investment")
DATA_FILE = os.path.join(ROOT, "_data", "investment.yml")

WATCH = "https://www.youtube.com/watch?v={}"
# hqdefault is the one thumbnail every video has. maxres is nicer and often
# missing, so it is tried first and this is the fallback rather than the plan.
THUMBS = ("https://i.ytimg.com/vi/{}/maxresdefault.jpg",
          "https://i.ytimg.com/vi/{}/hqdefault.jpg")

# The fields the page shows, asked for as one JSON object per video.
FIELDS = "%(.{id,title,channel,channel_url,duration})j"

# One id per talk on the page, in the order they appear on it. The v= of the
# watch URL, and nothing else: everything a cover needs is fetched.
VIDEOS = [
    "BVVNtG5dgks",
    "zPLc3jjHbnU",
    "F_LvzcdNH3Q",
    "v0JjG0Qfwi8",
    "OwQjTedWSUM",
]


def yt_dlp(args):
    cmd = ["yt-dlp", "--no-warnings", "--ignore-errors"] + args
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0 and not (proc.stdout or "").strip():
        last = (proc.stderr or "").strip().splitlines()
        sys.exit("yt-dlp failed: " + (last[-1] if last else "no output"))
    return (proc.stdout or "").splitlines()


def describe(ids, verbose):
    """Metadata for each id, in one yt-dlp run rather than one per video.

    yt-dlp takes many URLs at once and prints a line per video, so the whole
    pass is a single process; --ignore-errors keeps a video that has been made
    private from ending the run, and its line simply never arrives.
    """
    lines = yt_dlp(["--skip-download", "--print", FIELDS]
                   + [WATCH.format(v) for v in ids])
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


def cover(video_id, verbose):
    """Mirror the thumbnail into images/investment/, and name the file.

    Mirrored rather than hotlinked for the reason the covers on /music/ and
    /cybersecurity/ are: i.ytimg.com serves a thumbnail only as long as its
    video exists, so a page of live thumbnail URLs turns into grey boxes the
    day one is taken down.
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


def write_data(entries):
    lines = [
        "# Written by scripts/youtube-invest.py -- edit that, not this.",
        "# One entry per talk behind /investment/, in the order the page",
        "# shows them: the cover under images/investment/, what the talk is,",
        "# whose channel it is on, and the video it plays from.",
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
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    verbose = not args.quiet

    os.makedirs(IMAGE_DIR, exist_ok=True)
    rows = describe(VIDEOS, verbose)

    entries = []
    for video_id in VIDEOS:
        row = rows.get(video_id)
        if not row:
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
    print(f"{len(entries)} talk(s) -> images/investment/ and "
          "_data/investment.yml")


if __name__ == "__main__":
    main()
