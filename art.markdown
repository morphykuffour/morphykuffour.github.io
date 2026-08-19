---
layout: page
title: art
permalink: /art/
description: >-
  Pins saved from Pinterest, mirrored here at full resolution and shown one at
  a time, each one linked back to where it came from.
---

{%- comment -%}
The carousel is driven by _data/art.yml rather than by whatever happens to be
sitting in images/art/, because the file alone cannot say where a picture came
from. Each entry carries the pin it was saved from, so every image keeps a link
home; scripts/pinterest-art.py writes both the folder and the file in one pass.

Nothing here is authored by me. The images are other people's work, saved to a
Pinterest board and mirrored so the page keeps working when a pin is deleted --
which is the usual fate of a pin. The link on each one is the credit.

The strip itself lives in _includes/carousel.html, shared with /unc/.
{%- endcomment -%}
{%- assign art = site.data.art -%}
{%- capture art_base -%}{{ site.baseurl }}/images/art/{%- endcapture -%}
{%- if art and art.size > 0 -%}
{% include carousel.html items=art base=art_base label="Saved pins" unit="pin" %}

<p class="art-note">
  {{ art.size }} pins, saved from
  <a href="https://www.pinterest.com/morphykuffour/">pinterest.com/morphykuffour</a>
  and mirrored here so they outlive the originals. Each image links back to its
  pin; the work is its author's, not mine.
</p>
{%- else -%}
<p class="art-note">
  Nothing mirrored yet — the carousel is filled by running
  <code>scripts/pinterest-art.py</code>, which writes both
  <code>images/art/</code> and <code>_data/art.yml</code>. Meanwhile the pins
  live at
  <a href="https://www.pinterest.com/morphykuffour/">pinterest.com/morphykuffour</a>.
</p>
{%- endif -%}
