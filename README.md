# morphykuffour.github.io

Jekyll blog, built by GitHub Pages from `main`. Theme is
[riggraz/no-style-please](https://github.com/riggraz/no-style-please), pulled at
build time via `remote_theme`.

## Local development

```sh
nix develop        # ruby + bundler + the native-extension toolchain
bundle install     # once; installs into vendor/bundle
./preview.sh       # http://127.0.0.1:4000
```

`flake.nix` is the source of truth for the toolchain, and its `shellHook` sets
`BUNDLE_PATH` so gems land in `vendor/bundle` rather than your user profile.

### If `bundle install` dies compiling a gem

Almost always the wrong `bundle` is winning the PATH. macOS ships a system Ruby
(2.6) with its own bundler at `/usr/local/bin/bundle`, and if that one runs, it
tries to build native extensions — `colorator`, `nokogiri`, `ffi` — against
Ruby 2.6 headers and fails partway through with a C compiler error.

Check which one you have before debugging the gem itself:

```sh
bundle -v && which bundle    # want the nix one, not /usr/local/bin
```

Inside `nix develop` this is already correct. Outside it, be explicit:

```sh
/etc/profiles/per-user/$USER/bin/bundle install
```

The failure names whichever gem happened to compile first, so it reads like a
broken dependency rather than a PATH problem. It isn't.

## Tests

```sh
nix develop
./tests/run.sh
```

`tests/` drives the built pages in headless Chrome — computed styles, laid-out
geometry, and the appearance toggle's `localStorage` round-trip. See
[tests/README.md](tests/README.md) for what belongs there and what a browser
cannot check about the embedded resume PDF.

## Resume

`/resume/` does not build the resume. The LaTeX and the compiled PDF both live in
[morph-k/resume](https://github.com/morph-k/resume), which publishes the PDF to
its own GitHub Pages site; this page embeds that file, so a push there shows up
here on the next load with nothing to rebuild on this side. Edit the resume in
that repository. The two URLs are `resume_pdf` and `resume_source` in
`_config.yml`.

## Appearance modes

Three modes, toggled top-right and stored in `localStorage` under `appearance`:
`light`, `purple`, `dark`.

Light and dark are a single palette flipped — the theme implements dark as
`filter: invert(1)` on `<body>`, and `assets/css/main.scss` re-inverts code
blocks and the toggle so the Matrix green survives the flip.

Purple can't be reached by inverting anything, so it is authored outright under
`body[a="purple"]`: its own page colours, its own syntax palette, and no
`filter` at all. The practical consequence is that **every colour the theme
paints has to be restated there** — body, links, headings, `hr`, blockquote,
tables, inline `code`, the Rouge token classes, and the toggle. Anything missed
falls through to the theme's light-mode value and shows up as a light-on-purple
element. When adding markup that carries new colour, check it in purple mode
specifically; light and dark will look fine either way because they share a
palette.
