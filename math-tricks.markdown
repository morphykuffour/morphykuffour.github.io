---
layout: page
title: math tricks
# Sits beside the heading, decoration only -- see .title-marker.
marker: '×'
permalink: /math-tricks/
description: >-
  Shortcuts and notes worth keeping: an animation of the one I rebuilt myself,
  and hand-drawn sheets under it, each with its rule written out.
---

{%- comment -%}
The animation leads the page and the sheets follow it, which is the order the
two kinds of thing earn rather than the order they arrived in: the sheets are
saved from other people, and the animation is the one thing here that was
built rather than mirrored.

Everything below is driven by _data/math_tricks.yml rather than by whatever is
sitting in images/math-tricks/, for the reason /art/ is: the file alone cannot
carry the caption, the rule, or the alt text, and a picture of handwriting
without alt text is a blank square to anyone not looking at it.

A column of figures rather than the carousel /art/ uses. A carousel is right
when the picture is the whole point and there is nothing to compare across --
these are the opposite: each one is a thing to read, and a sheet you can only
see one of at a time is worse than a page of them.

Each sheet's rule is written out under it as text as well as being in the
picture, which is the whole difference between this page and a folder of
screenshots. The picture is how the trick is remembered; the sentence is how
it is found by a search, read out loud, or got at when the image does not
load.

The sheets are not mine. They are other people's notes, saved and mirrored so
the page keeps working when the post they came from goes; the caption is the
credit where there is a name to give.
{%- endcomment -%}

{%- comment -%}
The mesh-analysis animation. It is rendered by scripts/mesh_analysis.py with
Manim -- see that file for the circuit and the reasoning -- and then run
forward and backward by scripts/boomerang.sh, which is why it loops without a
seam: a matrix that builds up over forty seconds and then cuts back to an
empty screen is the whole point being undone in one frame. Backward it is the
same fact read the other way, a matrix being taken apart into the circuit it
came from.

Authored paused with a poster on it, not `autoplay` in the markup, and given
controls. The script at the foot of this file is what starts it, and only when
the reader has not asked for less motion -- the same call _includes/cascade.html
makes, for the same reason: a <video autoplay> has already started before any
script can ask.

The poster is a real frame from the end of the build rather than a title card,
so a reader who never plays it still gets the finished system out of the page.

Not the include: cascade.html plays three copies of a clip over each other and
stopmotion.html flips through ten stills. Both are decoration by design, and
this is the opposite -- one copy, played once through, meant to be read.
{%- endcomment -%}
<figure class="math-animation">
  <video id="mesh-analysis"
         src="{{ site.baseurl }}/videos/mesh-analysis.mp4"
         poster="{{ site.baseurl }}/videos/mesh-analysis-poster.jpg"
         width="720" height="1280"
         muted loop playsinline controls preload="metadata"
         aria-label="A circuit of three mesh loops, and its resistance matrix filled in a term at a time: each diagonal the sum of the resistors round one loop, each off-diagonal the negative of the resistor two loops share, ending in the solved currents."></video>
  <figcaption>
    <span class="math-trick-title">Mesh analysis, or why that matrix is a picture of the circuit</span>
    <span class="math-trick-rule">
      Every entry is a branch you can point at. A diagonal is the sum of the
      resistors around one loop; an off-diagonal is minus the resistor two
      loops share, negative because the two currents run through it in
      opposite directions. Only the loop holding the source gets a voltage,
      so <span class="math-nowrap">V = [16, 0, 0]</span> and the whole circuit
      comes down to three numbers.
      Written with <a href="https://www.manim.community/">Manim</a> in
      <a href="{{ site.baseurl }}/scripts/mesh_analysis.py">scripts/mesh_analysis.py</a>,
      after a reel by <a href="https://www.instagram.com/mae.academy/">MAE Academy</a>;
      the circuit and the numbers are theirs, the drawing is not.
    </span>
  </figcaption>
</figure>

{%- comment -%}
Built up rather than read straight off site.data, so the file being absent or
empty is simply no sheets rather than a page that fails to render on
`nil.size` -- the same guard /art/ and /music/ put in front of their lists.
{%- endcomment -%}
{%- assign tricks = "" | split: "" -%}
{%- if site.data.math_tricks -%}
{%- assign tricks = tricks | concat: site.data.math_tricks -%}
{%- endif -%}
{%- if tricks.size > 0 -%}
{%- for trick in tricks -%}
<figure class="math-trick">
  <img src="{{ site.baseurl }}/images/math-tricks/{{ trick.file }}"
       alt="{{ trick.alt | strip_newlines | escape }}"
       {%- if trick.width %} width="{{ trick.width }}"{% endif %}
       {%- if trick.height %} height="{{ trick.height }}"{% endif %}
       loading="lazy" decoding="async">
  <figcaption>
    <span class="math-trick-title">{{ trick.title }}</span>
    {%- if trick.rule %}
    <span class="math-trick-rule">{{ trick.rule }}</span>
    {%- endif %}
  </figcaption>
</figure>
{%- endfor -%}
{%- endif -%}

<script>
// The animation is authored paused so that this can decide whether it plays.
// Reduced motion means it stays on its poster, which is a frame of the solved
// system and so loses the reader nothing but the building of it; the controls
// are in the markup either way, so playing it is always one click away.
//
// It also stops when it is scrolled off. A video decoder running against a
// part of the page nobody is looking at is a laptop fan for nothing, and this
// one is three quarters of a minute long -- the same call the cascades on the
// homepage make, and pausing does not move currentTime, so it picks up where
// it was left.
(function () {
  var video = document.getElementById('mesh-analysis');
  if (!video) return;
  if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

  // A rejected play() is a normal outcome -- a browser that declines to
  // autoplay, a tab opened in the background -- and the poster is a fine thing
  // to be left looking at, so it is caught and dropped.
  function play() {
    var p = video.play();
    if (p && p.catch) p.catch(function () {});
  }

  if (!window.IntersectionObserver) { play(); return; }
  new IntersectionObserver(function (entries) {
    // Paused by hand stays paused: the observer only resumes what it stopped,
    // or a reader who hit pause would have it start again on the way back.
    if (entries[0].isIntersecting) {
      if (video.dataset.autoPaused) { delete video.dataset.autoPaused; play(); }
      else if (video.paused && !video.dataset.userPaused) play();
    } else if (!video.paused) {
      video.dataset.autoPaused = '1';
      video.pause();
    }
  }, { threshold: 0.15 }).observe(video);

  video.addEventListener('pause', function () {
    if (!video.dataset.autoPaused) video.dataset.userPaused = '1';
  });
  video.addEventListener('play', function () { delete video.dataset.userPaused; });
})();
</script>
