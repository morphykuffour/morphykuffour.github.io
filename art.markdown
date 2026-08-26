---
layout: page
title: art
# Sits beside the heading, decoration only -- see .title-marker.
marker: '~2'
permalink: /art/
description: >-
  Pins saved from Pinterest and a few picked up elsewhere, mirrored here at
  full resolution and shown one at a time.
---

{%- comment -%}
The carousel is driven by _data/art.yml rather than by whatever happens to be
sitting in images/art/, because the file alone cannot say where a picture came
from. Each entry carries the pin it was saved from, so every image keeps a link
home; scripts/pinterest-art.py writes both the folder and the file in one pass.

_data/art_local.yml is the hand-kept half, for images saved from somewhere
other than Pinterest. It is a second file rather than more entries in art.yml
because that script rewrites art.yml wholesale on every run. Those come first
in the strip, since they were put there deliberately rather than scraped.

Nothing here is authored by me. The images are other people's work, saved to a
Pinterest board and mirrored so the page keeps working when a pin is deleted --
which is the usual fate of a pin. The link on each one, or its title where
there is no pin to point at, is the credit.

The strip itself lives in _includes/carousel.html, shared with /unc/.
{%- endcomment -%}
{%- assign pins = site.data.art -%}
{%- assign local = site.data.art_local -%}
{%- comment -%}
Built up rather than written as one concat so that either file being absent or
empty is simply fewer slides, not a page that fails to render.
{%- endcomment -%}
{%- assign art = "" | split: "" -%}
{%- if local -%}{%- assign art = art | concat: local -%}{%- endif -%}
{%- if pins -%}{%- assign art = art | concat: pins -%}{%- endif -%}
{%- capture art_base -%}{{ site.baseurl }}/images/art/{%- endcapture -%}
{%- if art.size > 0 -%}
{% include carousel.html items=art base=art_base label="Saved pins" unit="pin" %}
{%- else -%}
<p class="art-note">
  Nothing mirrored yet — the carousel is filled by running
  <code>scripts/pinterest-art.py</code>, which writes both
  <code>images/art/</code> and <code>_data/art.yml</code>. Meanwhile the pins
  live at
  <a href="https://www.pinterest.com/morphykuffour/">pinterest.com/morphykuffour</a>.
</p>
{%- endif -%}
