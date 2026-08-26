---
layout: page
title: investment
permalink: /investment/
description: >-
  Talks from the firms that trade for a living, each cover linking back to the
  video it plays from.
---

{%- comment -%}
The talks a trading firm gives in public. Not advice and not a portfolio: what
is here is the engineering that the money side of this industry pays for, put
on a stage by the people doing it -- what a CPU actually does with a hot loop,
why a test suite that passes proves less than it looks like it does, where the
line between software and hardware stopped being real.

Loose videos rather than playlists, which is what makes this the /music/ shape
and not the /cybersecurity/ one. A playlist is a course and is walked in
order; these are hours long, unrelated, and posted years apart, so the page is
a flat list and the order is the one chosen in the script.

The grid and the covers are /music/'s, sharing its component rather than a
second copy of it: a grid of 16:9 covers that link out is the same problem
every time, and the rules for it live once in main.scss.

Covers are mirrored into images/investment/ rather than hotlinked from
i.ytimg.com, for the reason the music covers are: a thumbnail is served only
while its video is, so a page of live thumbnail URLs turns into grey boxes the
day a video is taken down. The link under each one still points at YouTube,
which is where the talk actually is.

Filled by scripts/youtube-invest.py, which rewrites _data/investment.yml
wholesale on every run. A talk is added by putting its id in that script's
VIDEOS list, in the place on the page it should have.
{%- endcomment -%}
{%- assign talks = site.data.investment -%}
{%- if talks and talks.size > 0 -%}
{%- comment -%}
The same markup a track on /music/ gets, and the same classes: one cover, its
duration stamped on it -- which here is the whole reason the stamp exists,
since a fifty-minute talk and a three-hour one look identical as pictures --
and the title under it linking where the cover does, so the whole cell is a
way to the video rather than a picture with a link beside it.
{%- endcomment -%}
<ul class="video-grid">
  {%- for talk in talks -%}
  <li class="video-item">
    <a class="video-cover" href="{{ talk.link }}" rel="noopener">
      <img src="{{ site.baseurl }}/images/investment/{{ talk.file }}"
           alt="Cover for {{ talk.title | escape }}"
           width="1280" height="720" loading="lazy" decoding="async">
      {%- if talk.duration != '' -%}<span class="video-time">{{ talk.duration }}</span>{%- endif -%}
    </a>
    <a class="video-title" href="{{ talk.link }}" rel="noopener">{{ talk.title }}</a>
    {%- if talk.channel != '' -%}
    <a class="video-channel" href="{{ talk.channel_url }}" rel="noopener">{{ talk.channel }}</a>
    {%- endif -%}
  </li>
  {%- endfor -%}
</ul>
{%- else -%}
<p class="video-note">
  Nothing here yet — the page is filled by running
  <code>scripts/youtube-invest.py</code>, which writes both
  <code>images/investment/</code> and <code>_data/investment.yml</code>.
</p>
{%- endif -%}
