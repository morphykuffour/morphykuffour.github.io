---
layout: page
title: speech
permalink: /speech/
description: >-
  Speeches worth sitting through, played whole rather than quoted, each one
  with who is speaking and why it is here.
---

{%- comment -%}
Whole speeches, not clips. A quote from one of these is the part that survives
being repeated, which is exactly the part that does not need the page -- the
reason to keep a speech is the twenty minutes around the line, so the frame
here is the whole thing and there is no transcript, no pull quote, and no
timestamp pointing at the good bit.

"Speech" is meant loosely: a commencement address, a last lecture, a talk to a
room of students. What they have in common is a lectern, one person, and an
argument long enough to need the time it takes.

Driven from _data/speeches.yml for the reason /math-tricks/ and /music/ are:
the id in the URL carries the video and nothing else, and the speaker, the
occasion, and the reason it is here have to be written down somewhere. Writing
them beside the id also means the markup below is written once, so a second
speech is four lines in the data file rather than another copy of an iframe.

Played from youtube-nocookie.com rather than youtube.com: same player, same
video, but the embed holds off on the cookie until someone presses play. The
title under each frame links to the ordinary watch URL, which is where the
comments, the description and the channel are -- none of which belong in a
frame on this page.

The referrer policy is YouTube's own rather than the no-referrer /xkcd/ uses.
That is not carelessness: an uploader can restrict where a video may be
embedded, and YouTube decides that from the referrer, so a frame that sends
none is a frame that can answer "video unavailable" on a video that plays
everywhere else. Origin-only is what YouTube's embed code sends -- the page
this is on is not sent, only the site.

Dark mode needs no rule for the frames. The theme re-inverts <iframe> under
its whole-page invert exactly as it does <img>, so the player keeps its own
tone here the way the pictures do everywhere else.
{%- endcomment -%}
{%- assign speeches = site.data.speeches -%}
{%- if speeches and speeches.size > 0 -%}
{%- for speech in speeches -%}
<figure class="speech">
  {%- comment -%}
  loading="lazy" is not premature here even with one speech on the page: the
  frame is a whole YouTube player, it is the heaviest thing this site loads,
  and every speech added below the fold is another one fetched before the
  first word of the page is read.
  {%- endcomment -%}
  <iframe class="speech-embed"
          src="https://www.youtube-nocookie.com/embed/{{ speech.id }}"
          title="{{ speech.title | escape }} — {{ speech.speaker | escape }}"
          loading="lazy"
          referrerpolicy="strict-origin-when-cross-origin"
          allow="accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
          allowfullscreen></iframe>
  <figcaption>
    <a href="https://www.youtube.com/watch?v={{ speech.id }}">{{ speech.title }}</a>
    — {{ speech.speaker }}, {{ speech.where }}.
    {%- if speech.note %}<span class="speech-why">{{ speech.note }}</span>{% endif -%}
  </figcaption>
</figure>
{%- endfor -%}

{%- else -%}
<p class="speech-note">
  Nothing here yet: the page is filled from <code>_data/speeches.yml</code>.
</p>
{%- endif -%}
