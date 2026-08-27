#!/usr/bin/env bash
#
# Cut the thunder GIF down to the frames it actually holds, for the storm that
# crosses the Virgin Islands flag in the top bar.
#
# Usage: scripts/thunder-frames.sh [thunder.gif [outdir]]
#
# Defaults are the copy kept in the repository and the folder the stop motion
# include reads, so with no arguments this regenerates what is checked in.
#
# --- why a stop motion of two stills, and not the GIF -------------------------
#
# The GIF is twenty frames of two pictures: one set of bolts held for ten, a
# second set held for ten, forever. That is not footage, it is a flicker
# between two photographs -- which is exactly what the stop motion include
# already does, and doing it that way buys three things the GIF cannot.
#
# The first is the dark-mode handling every other picture on the site gets for
# free: the theme flips the page and re-inverts <img>, and the include emits
# <img>. The second is that the timing comes out of CSS, so the flag can stand
# in a quiet sky for four and a half seconds and be crossed for a quarter of
# one -- a GIF holds each of its two frames for the same beat and can only
# strobe. The third is a reduced-motion setting the stylesheet can honour by
# taking the storm off the flag altogether, which a GIF gives no handle on.
#
# So the two pictures are pulled out here and the rhythm is left to main.scss.

set -euo pipefail
cd "$(dirname "$0")/.."

src=${1:-images/thunder/thunder.gif}
outdir=${2:-images/thunder}

# The flag's own shape, from images/flags/vi.svg: 1275x850, which is 3:2. The
# storm is laid over the flag edge to edge, so a crop of any other ratio is a
# picture stretched across it rather than a sky behind it. Three times the
# 60x40 the flag is drawn at, which is the retina copy and nothing more -- at
# 2.5rem tall there is no third use for more pixels than that.
width=180
height=120

mkdir -p "$outdir"

work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

# --- the two pictures ---------------------------------------------------------
#
# mpdecimate rather than a count written down here: the GIF's twenty frames are
# ten of each, and which of the twenty are which is a fact about the file, not
# about this script. Dropping every frame that is a duplicate of the one before
# leaves exactly the pictures the file holds, however many that turns out to be
# -- and the reel below is built from whatever comes out, so a longer GIF
# dropped in its place needs only `count` changed where the include is called.
#
# The thresholds are loose because the two frames are wholly different pictures:
# there is no near-duplicate here to be careful about, only exact repeats.
ffmpeg -y -v error -i "$src" \
  -vf "mpdecimate=hi=1000:lo=500:frac=0.05" -fps_mode passthrough \
  "$work/unique-%02d.png"

# --- the sky, before the bolts ------------------------------------------------
#
# The photograph is not bolts on black. It is bolts in a lit cloud: a milky
# violet haze filling most of the frame, which is what a real sky does when a
# strike lights it from inside. Over a flag it does something else -- the storm
# is composited at about seven tenths, so the haze goes on as a grey wash and
# the eagle underneath comes up flat and fogged for the length of the flash.
#
# The curve pulls the low half to black and leaves the top alone. The haze sits
# under it and goes out; the bolts sit over it and stay exactly as bright as
# they were photographed. What lands on the flag afterwards is a nearly black
# sky the flag reads through, crossed by strokes that are still the brightest
# thing on the page. The one place it costs anything is the faint branching at
# the edges of the frame, which is halfway up the curve and dims with the haze
# -- at sixty pixels wide those filaments are under a pixel each anyway.
crush="curves=all='0/0 0.45/0.02 0.7/0.5 1/1'"

# The crop is bottom-anchored: 663 of the sheet's 800 rows, taken from the
# bottom. Lightning is read downwards, and the rows given up at the top are the
# ones where the bolts are still a single trunk in the glare. What is kept is
# where they fork.
n=0
for frame in "$work"/unique-*.png; do
  n=$((n + 1))
  out=$(printf '%s/thunder-%02d.jpg' "$outdir" "$n")

  ffmpeg -y -v error -i "$frame" \
    -vf "crop=in_w:in_w*${height}/${width}:0:in_h-in_w*${height}/${width},${crush},scale=${width}:${height}:flags=lanczos" \
    -q:v 3 "$out"

  printf '%s -> %s\n' "$(basename "$out")" "$(du -h "$out" | cut -f1)"
done

printf '%s frames; the include wants count=%s\n' "$n" "$n"
