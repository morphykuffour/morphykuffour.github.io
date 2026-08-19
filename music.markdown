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
{%- endcomment -%}
{%- assign music = site.data.music -%}
{%- if music and music.size > 0 -%}
<ul class="music-grid">
  {%- for track in music -%}
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
  {%- endfor -%}
</ul>

<p class="music-note">
  {{ music.size }} tracks, newest first — everything in my
  <a href="https://www.youtube.com/feed/history">YouTube watch history</a> that
  YouTube files under Music. Pulled with
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
