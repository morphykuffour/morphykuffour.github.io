#!/usr/bin/env bash
#
# Play a clip forward and then backward, so it loops without a cut.
#
# A <video loop> jumps from the last frame to the first, and for anything that
# builds up over its length -- a matrix filling in, a drawing being drawn --
# that jump is the whole thing being wiped in one frame. Run backward after it
# runs forward and the end meets the beginning where it left it: the loop has
# no seam because there is nothing to cut back to.
#
# It also gets the reverse for free as a second reading. The mesh animation
# forward is a matrix being assembled from a circuit; backward it is a matrix
# being taken apart into the circuit it came from, which is the same fact read
# the other way round.
#
# Usage: scripts/boomerang.sh in.mp4 out.mp4 [poster.jpg]
#
# The poster is optional and is taken from the frame the loop begins on, which
# for a build-up animation is a nearly empty screen. Pass a frame number as a
# fourth argument to take it from somewhere with more on it.

set -euo pipefail

src=${1:?input video}
out=${2:?output video}
poster=${3:-}
poster_frame=${4:-0}

frames=$(ffprobe -v error -select_streams v:0 -count_frames \
                 -show_entries stream=nb_read_frames \
                 -of default=nw=1:nk=1 "$src")

# Two frames come off the reversed half, and each one is a frame that would
# otherwise be shown twice in a row. The first is the clip's own last frame,
# which the forward half has just finished on; the last is its first frame,
# which the forward half is about to start on again when the loop comes round.
# Left in, both read as a stutter at the turn rather than as a turn.
last=$((frames - 1))

ffmpeg -y -v error -i "$src" -filter_complex "
  [0:v]split=2[fwd][rev];
  [rev]reverse,trim=start_frame=1:end_frame=$last,setpts=PTS-STARTPTS[back];
  [fwd][back]concat=n=2:v=1[out]
" -map "[out]" \
  -an \
  -c:v libx264 -profile:v high -pix_fmt yuv420p -crf 24 -preset slow \
  -movflags +faststart \
  "$out"

# -an rather than a silent track: the clips already on the site carry no audio
# stream at all, and a <video muted autoplay> needs no such thing to start.

if [ -n "$poster" ]; then
  ffmpeg -y -v error -i "$out" -vf "select=eq(n\,$poster_frame)" -vframes 1 \
         -q:v 3 "$poster"
fi

printf '%s: %s frames -> %s\n' "$out" "$((frames * 2 - 2))" \
       "$(du -h "$out" | cut -f1)"
