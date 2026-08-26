---
layout: page
title: cybersecurity
permalink: /cybersecurity/
description: >-
  Playlists of security work worth watching end to end, each cover linking
  back to the video it plays from.
---

{%- comment -%}
Playlists rather than loose videos, because the unit of this subject is a
course and not a clip. A ten-minute video on breaking AES with a scope tells
you it can be done; the twenty around it are the ones that tell you how, and a
page that keeps only the striking one keeps the wrong half.

So the page is a list of playlists, each with the note saying why it is here,
and under it every video in it in playlist order -- which is teaching order,
put there by whoever built the playlist, and is the only ordering here anyone
has thought about.

The grid and the covers are /music/'s, sharing its component rather than a
second copy of it: a grid of 16:9 covers that link out is the same problem
both times, and the rules for it live once in main.scss. What is different is
what sits above them -- a listening history is one flat list, and this is
several named ones.

Covers are mirrored into images/cybersecurity/ rather than hotlinked from
i.ytimg.com, for the reason the music covers are: a thumbnail is served only
while its video is, so a page of live thumbnail URLs turns into grey boxes the
day a video is taken down. The link under each one still points at YouTube,
which is where the video actually is.

Filled by scripts/youtube-cyber.py, which rewrites _data/cybersecurity.yml
wholesale on every run. A playlist is added by putting its id in that script's
PLAYLISTS list -- with the note, which lives there rather than in the data
file so that it survives the rewrite.

Not everything worth keeping was taught as a course, though, so under the
playlists is a shelf for talks that belong to no playlist at all. Those are
hand-kept in _data/cybersecurity_local.yml, written by `--add <url>`, for the
reason /music/ keeps a second file: the pulled one is rewritten wholesale and
would carry a hand-added entry only until the next run. They sit last because
the playlists are the substance of the page and a single talk is an addition
to it -- and unlike a playlist's videos, each carries its channel, since there
is no owner named above it to inherit.
{%- endcomment -%}
{%- assign playlists = site.data.cybersecurity -%}
{%- assign loose = site.data.cybersecurity_local -%}
{%- if playlists and playlists.size > 0 -%}
{%- for playlist in playlists -%}
<section class="playlist">
  <h2 class="playlist-name">
    <a href="{{ playlist.url }}" rel="noopener">{{ playlist.title }}</a>
  </h2>
  {%- comment -%}
  Whitespace control matters in this line: the em dash and the count are one
  sentence, and a `-%}` between them eats the space that keeps it one.
  {%- endcomment -%}
  <p class="playlist-credit">
    {%- if playlist.channel != '' %}<a href="{{ playlist.channel_url }}" rel="noopener">{{ playlist.channel }}</a> — {% endif -%}
    {{ playlist.videos.size }} video{% if playlist.videos.size != 1 %}s{% endif %}.
  </p>
  {%- if playlist.note -%}<p class="playlist-note">{{ playlist.note }}</p>{%- endif -%}
  {%- comment -%}
  The same markup a track on /music/ gets, and the same classes: one cover,
  its duration stamped on it, and the title under it linking to the same
  place the cover does -- so the whole cell is a way to the video rather than
  a picture with a link beside it.
  {%- endcomment -%}
  <ul class="video-grid">
    {%- for video in playlist.videos -%}
    <li class="video-item">
      <a class="video-cover" href="{{ video.link }}" rel="noopener">
        <img src="{{ site.baseurl }}/images/cybersecurity/{{ video.file }}"
             alt="Cover for {{ video.title | escape }}"
             width="1280" height="720" loading="lazy" decoding="async">
        {%- if video.duration != '' -%}<span class="video-time">{{ video.duration }}</span>{%- endif -%}
      </a>
      <a class="video-title" href="{{ video.link }}" rel="noopener">{{ video.title }}</a>
    </li>
    {%- endfor -%}
  </ul>
</section>
{%- endfor -%}
{%- endif -%}
{%- if loose and loose.size > 0 -%}
<section class="loose">
  {%- comment -%}
  A plain heading rather than a link, because there is nothing on YouTube for
  it to point at: this shelf exists here and nowhere else.
  {%- endcomment -%}
  <h2 class="playlist-name">On their own</h2>
  <p class="playlist-credit">
    {{ loose.size }} talk{% if loose.size != 1 %}s{% endif %}, newest first.
  </p>
  <p class="playlist-note">
    Kept one at a time rather than pulled from a playlist — a talk that was
    never part of a course, and is not made one by being filed next to them.
  </p>
  <ul class="video-grid">
    {%- for video in loose -%}
    <li class="video-item">
      <a class="video-cover" href="{{ video.link }}" rel="noopener">
        <img src="{{ site.baseurl }}/images/cybersecurity/{{ video.file }}"
             alt="Cover for {{ video.title | escape }}"
             width="1280" height="720" loading="lazy" decoding="async">
        {%- if video.duration != '' -%}<span class="video-time">{{ video.duration }}</span>{%- endif -%}
      </a>
      <a class="video-title" href="{{ video.link }}" rel="noopener">{{ video.title }}</a>
      {%- if video.channel != '' -%}
      <a class="video-channel" href="{{ video.channel_url }}" rel="noopener">{{ video.channel }}</a>
      {%- endif -%}
    </li>
    {%- endfor -%}
  </ul>
</section>
{%- endif -%}
{%- unless playlists.size > 0 or loose.size > 0 -%}
<p class="video-note">
  Nothing here yet — the page is filled by running
  <code>scripts/youtube-cyber.py</code>, which writes both
  <code>images/cybersecurity/</code> and <code>_data/cybersecurity.yml</code>.
</p>
{%- endunless -%}
