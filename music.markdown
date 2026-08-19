---
layout: page
title: music
permalink: /music/
description: >-
  What I have been listening to on YouTube, most recent first, each cover
  linking back to the video it was played from.
---

{%- comment -%}
Not a taste statement and not a chart: this is the music YouTube's own history
says I played, in the order it says I played it, pulled by
scripts/youtube-music.py and filtered to the videos YouTube itself files under
the Music category. So a three-hour jazz mix counts the same as a single, and
nothing here is ranked by anything.

A grid rather than the /art/ carousel. A carousel is right when the picture is
the whole point and there is nothing to compare across; a listening history is
a list, and a list you can only see one row of at a time is a worse list. The
covers stay the size they are worth at a glance and the titles sit under them.

The covers are mirrored into images/music/ rather than hotlinked from
i.ytimg.com: a thumbnail is served only while its video is, so a page of live
thumbnail URLs turns into grey boxes the day a track is taken down. The link
under each one still points at YouTube, which is where the music actually is.

_data/music_local.yml is the hand-kept half: tracks put here directly rather
than picked up from the history. It is a second file because the script
rewrites music.yml wholesale on every run. They lead the grid, and a pulled
entry pointing at the same video is skipped below -- otherwise a hand-added
track would double up the day the history catches up with it. A track removed
from the page needs the other half of that: its id in the script's DROPPED
set, or the next run pulls it straight back.
{%- endcomment -%}
{%- assign pulled = site.data.music -%}
{%- assign local = site.data.music_local -%}
{%- comment -%}
Built up rather than written as one concat so that either file being absent or
empty is simply fewer covers, not a page that fails to render. Hand-kept first,
which is also what makes the de-duplication below keep the hand-kept copy.
{%- endcomment -%}
{%- assign tracks = "" | split: "" -%}
{%- if local -%}{%- assign tracks = tracks | concat: local -%}{%- endif -%}
{%- if pulled -%}{%- assign tracks = tracks | concat: pulled -%}{%- endif -%}
{%- if tracks.size > 0 -%}
{%- comment -%}
One loop over both lists rather than one loop each: the markup for a cover is
the thing most likely to be changed later, and a second copy of it is a second
copy to forget. A video seen already is skipped, so a hand-added track does not
double up the day the history catches up with it, and `shown` is counted here
rather than from the list sizes so the note below cannot claim a number the
grid does not hold.
{%- endcomment -%}
{%- assign seen = "" -%}
{%- assign shown = 0 -%}
<ul class="music-grid">
  {%- for track in tracks -%}
  {%- unless seen contains track.link -%}
  {%- assign seen = seen | append: track.link | append: " " -%}
  {%- assign shown = shown | plus: 1 -%}
  <li class="music-track">
    <a class="music-cover" href="{{ track.link }}" rel="noopener">
      <img src="{{ site.baseurl }}/images/music/{{ track.file }}"
           alt="Cover for {{ track.title | escape }}"
           width="1280" height="720" loading="lazy" decoding="async">
      {%- if track.duration -%}<span class="music-time">{{ track.duration }}</span>{%- endif -%}
    </a>
    <a class="music-title" href="{{ track.link }}" rel="noopener">{{ track.title }}</a>
    {%- if track.channel != '' -%}
    <a class="music-channel" href="{{ track.channel_url }}" rel="noopener">{{ track.channel }}</a>
    {%- endif -%}
  </li>
  {%- endunless -%}
  {%- endfor -%}
</ul>

<p class="music-note">
  {{ shown }} tracks, newest first — my
  <a href="https://www.youtube.com/feed/history">YouTube watch history</a>
  filtered to what YouTube files under Music, plus anything put here by hand.
  Pulled with
  <a href="https://github.com/yt-dlp/yt-dlp">yt-dlp</a> by
  <code>scripts/youtube-music.py</code>; the history feed only goes back a few
  hundred videos, so this is recent listening rather than all of it. The music
  is its artists', not mine.
</p>
{%- else -%}
<p class="music-note">
  Nothing pulled yet — the page is filled by running
  <code>scripts/youtube-music.py</code>, which needs a signed-in cookie to read
  the history feed at all and writes both <code>images/music/</code> and
  <code>_data/music.yml</code>.
</p>
{%- endif -%}
