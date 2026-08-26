---
layout: page
title: unc
permalink: /unc/
description: >-
  Photographs of me, one at a time, which is the whole page and the whole joke.
---

{%- comment -%}
The same carousel as /art/, from the same include, pointed at _data/unc.yml.
The two pages differ in what they hold rather than in how it is shown: pins
there, my own camera roll here. Neither prints a line under the picture -- a
pin gets a link back to its author instead, which is the credit it needs, and
these are mine and need none.
{%- endcomment -%}
{%- assign unc = site.data.unc -%}
{%- capture unc_base -%}{{ site.baseurl }}/images/unc/{%- endcapture -%}
{%- if unc and unc.size > 0 -%}
{% include carousel.html items=unc base=unc_base label="Photographs of me" unit="photo" %}

<p class="unc-note">
  {{ unc.size }} photos, mine — unlike <a href="{{ site.baseurl }}/art/">/art/</a>,
  where none of it is.
</p>
{%- else -%}
<p class="unc-note">
  Nothing here yet: the carousel is filled from <code>_data/unc.yml</code> and
  <code>images/unc/</code>.
</p>
{%- endif -%}
