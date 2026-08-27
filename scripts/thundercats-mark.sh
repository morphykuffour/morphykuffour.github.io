#!/usr/bin/env bash
#
# Cut the ThunderCats emblem down to the mark that closes the top bar.
#
# Usage: scripts/thundercats-mark.sh [source.png [out.png]]
#
# Defaults are the copy kept in the repository and the file the layout reads,
# so with no arguments this regenerates what is checked in.
#
# The file as downloaded is a 3840x2160 sheet with the emblem sitting in the
# middle of it and everything around it transparent -- a 16:9 frame around a
# round mark, which in the bar is a circle with two wide columns of nothing
# either side of it, and nothing is exactly as wide as something when a flex
# row is measuring. So it is trimmed to what is actually drawn.
#
# The trim is taken from the alpha channel rather than written down: the box
# below is where the opaque pixels are, and it comes out 2046 square to the
# pixel, which is the emblem being a disc drawn on the diagonal of its own
# frame. Reading it each run is what keeps that true of whatever file is put
# here, rather than true of the one that was here when the numbers were typed.

set -euo pipefail
cd "$(dirname "$0")/.."

src=${1:-images/thundercats/emblem-source.png}
out=${2:-images/thundercats/emblem.png}

# Three times the 2.25rem the bar draws it at, which is the retina copy and
# nothing more. Square, because the trim is.
size=144

read -r x0 y0 side < <(
  ffmpeg -v error -i "$src" -vf format=rgba -f rawvideo - \
  | python3 -c "
import sys, subprocess
w, h = (int(v) for v in subprocess.run(
    ['ffprobe','-v','error','-select_streams','v:0',
     '-show_entries','stream=width,height','-of','csv=p=0:nk=1','$src'],
    capture_output=True, text=True).stdout.strip().split(','))
d = sys.stdin.buffer.read()
minx, miny, maxx, maxy = w, h, -1, -1
for y in range(h):
    alpha = d[y * w * 4 + 3 : (y + 1) * w * 4 : 4]
    xs = [i for i, v in enumerate(alpha) if v > 8]
    if not xs:
        continue
    miny = min(miny, y); maxy = y
    minx = min(minx, xs[0]); maxx = max(maxx, xs[-1])
# Squared off around the longer side, so a mark that trims a pixel out of true
# is centred in its box rather than stretched to fill it.
side = max(maxx - minx + 1, maxy - miny + 1)
print(minx - (side - (maxx - minx + 1)) // 2,
      miny - (side - (maxy - miny + 1)) // 2,
      side)
")

# PNG out, not JPEG: the ground has to stay transparent -- the bar is white on
# one theme, near black on another and aubergine on the third, and a disc
# delivered on a square of any one of them is a sticker on the other two. Flat
# colour and hard edges besides, which is what PNG is for and what JPEG makes a
# halo of.
# format=rgba first, and the pixel format named on the way out. The file as
# downloaded is palettised, and its transparent entry carries a colour of its
# own -- a grey green, as it happens. Left to pick its own formats ffmpeg drops
# the alpha somewhere in the chain and that colour is what is underneath: the
# disc arrives on a green square, which on the purple page is unmistakable and
# on the black one is nearly not. So the alpha is asked for at both ends.
ffmpeg -y -v error -i "$src" \
  -vf "format=rgba,crop=${side}:${side}:${x0}:${y0},scale=${size}:${size}:flags=lanczos" \
  -pix_fmt rgba "$out"

printf '%s: %sx%s at %s,%s -> %s at %spx\n' "$(basename "$out")" \
       "$side" "$side" "$x0" "$y0" "$(du -h "$out" | cut -f1)" "$size"
