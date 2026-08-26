#!/usr/bin/env bash
#
# Cut the three numbered steps out of the water-crown sheet into a stop motion.
#
# The sheet is one page of pencil studies -- a rendered splash across the top,
# a row of construction steps numbered 1, 2, 3 under it, a row of variants
# under that, and a large drawing at the foot. Only the numbered three are
# taken. They are the sequence the sheet itself states: an ellipse, the column
# that rises out of it, the crown it opens into. The variants below them are
# the same crown seen from other eye levels, and the two finished drawings are
# a different weight of line altogether; either put in the reel reads as the
# sequence cutting away to another picture rather than as one shape building.
#
# Usage: scripts/watercrown-frames.sh [sheet.jpg [outdir]]
#
# Defaults are the copy kept in the repository and the folder the stop motion
# include reads, so with no arguments this regenerates what is checked in.
#
# --- what makes it read as one drawing rather than three ---------------------
#
# The three studies sit at different sizes and different places on the page, so
# a crop of each at some fixed box would give three drawings jumping around
# their frames. They are registered on the one feature all three share instead:
# the ellipse where the water meets the crown. Each crop is centred on that
# ellipse, and scaled so the ellipse spans the same fraction of every frame --
# which puts the waterline in the same place, at the same width, in all three.
# What is then left to move between frames is only what the artist drew
# differently, which is the whole point of the sequence.
#
# The measurements below are that ellipse in each study, read off the sheet in
# its own pixels: centre and half-width. They are the only numbers here that
# are about this particular photograph of this particular page, which is why
# they are a table rather than three copies of an ffmpeg line.

set -euo pipefail
cd "$(dirname "$0")/.."

sheet=${1:-images/watercrown/sheet.jpg}
outdir=${2:-images/watercrown}

# How much of a frame's width the waterline ellipse takes, and how far down the
# frame its centre sits. The first is what fixes the scale; below about .7 the
# crown loses the droplets thrown off the rim, above it the sheet's own pencil
# grid crowds in from the sides. The second leaves the upper three quarters for
# what grows out of the water, which is where every difference between the
# three frames is.
ellipse=0.64
waterline=0.74

# 16:9, and small: this plays at about a hundred pixels above the portrait, so
# what is being reserved here is the retina copy of that and nothing more.
width=384
height=216

# step  centre-x  centre-y  half-width, in the sheet's own pixels
steps=(
  "01 220  876 127"   # the ellipse: the surface, before anything happens to it
  "02 577  890 150"   # the column standing up out of it, arrows for the rise
  "03 968  887 152"   # the crown, rim broken into points and throwing droplets
)

mkdir -p "$outdir"

# --- the paper, before anything is cut out of it -----------------------------
#
# The sheet is a photograph of a page under a room light, so the paper is not
# one tone: it is a soft gradient across the picture, a little over 200 where
# the light falls and darker at the corners. Left in, every frame arrives as a
# grey card -- on the light page a box ruled round the drawing, on the dark one
# a card that does not quite reach the black behind it, and the three of them
# at slightly different greys flickering as the reel steps.
#
# Divided by a heavily blurred copy of itself, the gradient divides out: the
# blur is the lighting with the drawing averaged away, and every pixel over its
# own local paper level is white by construction. What is left is the graphite.
# That is one pass over the whole page rather than one per crop, because the
# gradient is a fact about the photograph and not about any one study on it.
#
# The curve after it is what puts the pencil back. The division leaves the ink
# lighter than it was drawn, and a plain contrast lift would take the faint
# construction lines with it -- they are the lightest thing on the page and the
# first to go, and in step 1 they are most of what there is to see. So the two
# ends are pinned and only the middle is pulled down: paper stays white, the
# darkest strokes stay where they are, and everything between them darkens.
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT
flat=$work/flat.png
ffmpeg -y -v error -i "$sheet" -filter_complex \
  "[0:v]format=gray,split=2[page][cast];
   [cast]gblur=sigma=30[lighting];
   [page][lighting]blend=all_mode=divide[flat]" \
  -map "[flat]" "$flat"

for step in "${steps[@]}"; do
  set -- $step; n=$1; cx=$2; cy=$3; hw=$4

  # The crop box falls out of the two fractions and the measured ellipse: as
  # wide as the ellipse needs to be that fraction of it, 16:9 tall, centred on
  # the ellipse across and hung above it down the frame. Clamped at the sheet's
  # edges, since step 3 sits close to the right margin of the page.
  read -r cw ch x0 y0 < <(python3 -c "
sheet_w, sheet_h = 1206, 1689
cw = round(2 * $hw / $ellipse)
ch = round(cw * $height / $width)
print(cw, ch,
      max(0, min(sheet_w - cw, round($cx - cw / 2))),
      max(0, min(sheet_h - ch, round($cy - $waterline * ch))))")

  # Lanczos because the reduction is better than half, and a box filter loses
  # the thin lines first -- which here are the crown's points.
  ffmpeg -y -v error -i "$flat" \
    -vf "crop=${cw}:${ch}:${x0}:${y0},curves=all='0/0 0.3/0.14 0.6/0.42 0.88/0.94 1/1',scale=${width}:${height}:flags=lanczos" \
    -q:v 3 "$outdir/watercrown-$n.jpg"

  printf '%s: %sx%s at %s,%s -> %s\n' "watercrown-$n.jpg" "$cw" "$ch" "$x0" "$y0" \
         "$(du -h "$outdir/watercrown-$n.jpg" | cut -f1)"
done
