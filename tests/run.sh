#!/usr/bin/env bash
# End-to-end tests: build the site, serve it, and drive the real pages in a
# real browser. Everything asserted here is something only a browser can
# answer -- computed styles after the cascade, laid-out geometry, and the
# localStorage round-trip behind the appearance toggle -- so there is no
# static-HTML shortcut for any of it.
#
#   ./tests/run.sh          # build, then test
#   ./tests/run.sh --no-build   # reuse the last build in _site
#
# Exit status is 0 only if every case passes.
set -euo pipefail
cd "$(dirname "$0")/.."

PORT=${PORT:-8765}
BUILD=_site

# Same guard as preview.sh: the macOS system Ruby cannot build these gems, and
# the failure it produces names a random gem rather than the PATH problem.
ruby_major_minor=$(ruby -e 'print RUBY_VERSION[/\d+\.\d+/]')
if [[ $ruby_major_minor == 2.* ]]; then
  echo "tests/run.sh: found Ruby $ruby_major_minor ($(command -v ruby))." >&2
  echo "That's the macOS system Ruby; gems won't build. Run 'nix develop' first." >&2
  exit 1
fi

# The pages are driven through an iframe from a same-origin harness, so the
# browser has to be one that ships headless. Override with CHROME=... for
# Chromium, Brave, or an Edge build.
CHROME=${CHROME:-}
if [[ -z $CHROME ]]; then
  for candidate in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/Applications/Chromium.app/Contents/MacOS/Chromium" \
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser" \
    "$(command -v google-chrome-stable || true)" \
    "$(command -v chromium || true)"; do
    [[ -n $candidate && -x $candidate ]] && CHROME=$candidate && break
  done
fi
if [[ -z $CHROME ]]; then
  echo "tests/run.sh: no Chrome-family browser found. Set CHROME=/path/to/chrome." >&2
  exit 1
fi

if [[ ${1:-} != "--no-build" ]]; then
  bundle exec jekyll build --destination "$BUILD" --quiet
fi

# The harness has to come from the same origin as the pages it inspects, so it
# is copied into the build rather than opened off disk. The build directory is
# gitignored and rebuilt each run, so the copy leaves nothing behind.
cp tests/e2e.html "$BUILD/e2e.html"

python3 -m http.server "$PORT" --directory "$BUILD" >/dev/null 2>&1 &
server=$!
trap 'kill $server 2>/dev/null || true; rm -f "$BUILD/e2e.html"' EXIT

# Wait for the server rather than sleeping a guessed interval.
for _ in $(seq 1 50); do
  curl -sf -o /dev/null "http://localhost:$PORT/e2e.html" && break
  sleep 0.1
done

# --virtual-time-budget lets the harness's awaited page loads finish before the
# DOM is dumped; the <pre> it fills is the whole report.
#
# Site isolation is turned off for the run because /xkcd/ frames another
# origin. Virtual time is per-renderer, and a cross-origin frame gets its own
# renderer that never receives the budget: the subframe then sits pending, the
# page's load event never fires, and the harness waits out the clock on a page
# that is in fact laid out. In one process the frame loads like any other.
# Reduced motion is forced for the run so that anything which scrolls itself
# lands where it is going within the same task instead of animating there.
# Under --virtual-time-budget Chrome never runs the rendering lifecycle, so a
# `behavior: smooth` scroll is simply inert and the box never moves at all --
# the /art/ carousel could not be driven otherwise. Nothing here asserts an
# animation, so no case loses anything by it.
output=$("$CHROME" --headless=new --disable-gpu --virtual-time-budget=20000 \
  --force-prefers-reduced-motion \
  --disable-site-isolation-trials --disable-features=IsolateOrigins,site-per-process \
  --dump-dom "http://localhost:$PORT/e2e.html" 2>/dev/null |
  sed -n '/<pre id="out">/,/<\/pre>/p' | sed 's/<[^>]*>//g')

echo "$output"

summary=$(echo "$output" | tail -1)
if [[ $summary != *" 0 failed" ]]; then
  echo
  echo "tests/run.sh: FAILED -- $summary" >&2
  exit 1
fi
