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

The track is a scroll container with scroll-snap, not a JS slider: with the
script off it is still a swipeable, keyboard-scrollable strip of pictures, and
with it on the arrows only call scrollTo on that same box. So the carousel has
no state of its own to get out of step -- where it is *is* its scroll offset,
which is also what a swipe, a trackpad and a focus ring all already move.
{%- endcomment -%}
{%- assign art = site.data.art -%}
{%- if art and art.size > 0 -%}
<div class="art-carousel" data-art-carousel>
  <ul class="art-track" tabindex="0" aria-label="Saved pins">
    {%- for piece in art -%}
    <li class="art-slide">
      <a href="{{ piece.link }}" rel="noopener nofollow"
         title="{{ piece.title | default: 'Saved pin' | escape }}">
        <img src="{{ site.baseurl }}/images/art/{{ piece.file }}"
             alt="{{ piece.title | default: 'Saved pin' | escape }}"
             loading="lazy" decoding="async">
      </a>
    </li>
    {%- endfor -%}
  </ul>

  {%- comment -%}
  Authored hidden and revealed by the script below. A button that does nothing
  is worse than no button, and without JS these do nothing -- the strip is
  swipeable on its own, so nothing is lost by leaving them out of that case.
  {%- endcomment -%}
  <div class="art-controls" hidden>
    <button type="button" class="art-prev" aria-label="Previous pin">&larr;</button>
    <span class="art-count" aria-live="polite">1 / {{ art.size }}</span>
    <button type="button" class="art-next" aria-label="Next pin">&rarr;</button>
  </div>
</div>

<p class="art-note">
  {{ art.size }} pins, saved from
  <a href="https://www.pinterest.com/morphykuffour/">pinterest.com/morphykuffour</a>
  and mirrored here so they outlive the originals. Each image links back to its
  pin; the work is its author's, not mine.
</p>

<script>
// Everything the arrows do, a swipe already did. They move the same scroll box
// by exactly one slide, and the counter is read back out of the scroll offset
// rather than kept alongside it -- so a swipe, a trackpad flick, a keyboard
// scroll and an arrow click all end up reporting the same number, and there is
// no "current index" to fall out of sync with where the strip actually is.
(function () {
  var root = document.querySelector('[data-art-carousel]');
  if (!root) return;
  var track = root.querySelector('.art-track');
  var slides = track.querySelectorAll('.art-slide');
  var controls = root.querySelector('.art-controls');
  var count = root.querySelector('.art-count');
  if (!slides.length) return;

  controls.hidden = false;

  function step() {
    // The slide's own width, not the track's: they are the same today, but
    // reading the slide keeps this honest if the CSS ever shows a peek of the
    // next one at a wide viewport.
    return slides[0].getBoundingClientRect().width;
  }

  function index() {
    return Math.min(slides.length - 1,
                    Math.max(0, Math.round(track.scrollLeft / step())));
  }

  function report() {
    count.textContent = (index() + 1) + ' / ' + slides.length;
  }

  // Someone who has asked their system for less motion gets the jump rather
  // than the glide. Read per call, not once: the setting can change under a
  // running page, and there is nothing to invalidate if it is never cached.
  function motion() {
    return window.matchMedia('(prefers-reduced-motion: reduce)').matches
      ? 'auto' : 'smooth';
  }

  function go(delta) {
    // Snapping to a computed offset rather than scrollBy: at the ends a
    // partial scroll would otherwise leave the track between two snap points.
    track.scrollTo({
      left: Math.min(slides.length - 1, Math.max(0, index() + delta)) * step(),
      behavior: motion(),
    });
  }

  root.querySelector('.art-prev').addEventListener('click', function () { go(-1); });
  root.querySelector('.art-next').addEventListener('click', function () { go(1); });

  // The track is focusable so it can be scrolled from the keyboard at all; the
  // browser's own left/right on a scroll container moves by a scroll step
  // rather than a slide, so those two keys are taken over here.
  track.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowLeft')  { e.preventDefault(); go(-1); }
    if (e.key === 'ArrowRight') { e.preventDefault(); go(1); }
  });

  // The browser already coalesces scroll to once per frame, so this needs no
  // throttle of its own -- and reading the offset back here, rather than
  // setting a number when an arrow is clicked, is what keeps a swipe, a
  // trackpad flick and a keyboard scroll all reporting correctly too.
  track.addEventListener('scroll', report, { passive: true });

  report();
})();
</script>
{%- else -%}
<p class="art-note">
  Nothing mirrored yet — the carousel is filled by running
  <code>scripts/pinterest-art.py</code>, which writes both
  <code>images/art/</code> and <code>_data/art.yml</code>. Meanwhile the pins
  live at
  <a href="https://www.pinterest.com/morphykuffour/">pinterest.com/morphykuffour</a>.
</p>
{%- endif -%}
