# tests

```sh
nix develop
./tests/run.sh          # build, serve, drive the pages in headless Chrome
./tests/run.sh --no-build   # reuse the last build in _site
```

`run.sh` is the harness runner; `e2e.html` is every case. It is served from the
built site so it shares an origin with the pages it frames, which is what lets
it read their computed styles, their laid-out geometry, and the `appearance`
key the theme toggle writes to `localStorage`.

Only assert things a browser can answer. Anything checkable by reading the
source — a URL in an `href`, a filename — belongs in a grep, not here. What
earns a case is behaviour that emerges from the cascade or the layout: which
rule wins in purple mode, whether a floated element still shortens the lines
beside it, whether a small-screen rule fires at the width it claims.

Two habits worth keeping:

- **Frame width is viewport width.** A page framed at 420px evaluates its media
  queries at 420px, so small-screen rules can be tested without resizing the
  browser. Resizing the browser window does not work as well — Chrome enforces
  a minimum window width, so a `--window-size=420` screenshot is still laid out
  wider than it looks.
- **Floats move line boxes, not block boxes.** A floated portrait shortens the
  lines of the paragraph beside it while that paragraph's block box still spans
  the full column, so assert on `Range.getClientRects()[0]`, not on the
  element's own rect.

## The cross-origin frame on /xkcd/

`run.sh` launches Chrome with site isolation off. `/xkcd/` frames xkcd.com, and
virtual time is per-renderer: with isolation on, that frame gets a renderer of
its own that never receives the budget, so it sits pending, the page's `load`
never fires, and the harness waits out the clock on a page that is already laid
out. In one process it loads like any other frame. The cases themselves stay on
this side of the frame — its `src`, its `name`, the armed random link, and the
CSS each mode puts on it — because nothing can read into another origin.

## What a browser cannot check here

The resume page embeds a PDF, which the browser paints through its own viewer.
Headless Chrome does not render that viewer, so the cases under `resume/` assert
the CSS that reaches it — the filter chain, the blend mode, the mode-specific
values — and stop there. To eyeball the result, rasterise a page and apply the
same declarations to the image:

```sh
curl -fsSL -o /tmp/resume.pdf https://morph-k.github.io/resume/resume.pdf
qlmanage -t -s 1400 -o /tmp /tmp/resume.pdf   # /tmp/resume.pdf.png
```

That PDF is served by `morph-k/resume`, not by this repository — the page embeds
it cross-origin so it tracks that repository's latest build. The cases assert the
`data` and `href` the page ships, which is all this side of the origin can see;
whether the file itself is current is that repository's business.
