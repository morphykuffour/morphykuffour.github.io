---
layout: page
title: xkcd
permalink: /xkcd/
description: >-
  xkcd, framed inside morphykuffour.github.io — today's comic by default, and
  a random one on request.
---

<p class="paper-actions">
  <a id="xkcd-random" href="https://xkcd.com/" target="xkcd-frame" data-latest="3285">Random comic</a>
  <a href="https://xkcd.com/" target="xkcd-frame">Today's comic</a>
  <a href="https://xkcd.com/">Open xkcd.com itself</a>
</p>

{%- comment -%}
The frame is named and the first two links target that name, so a click swaps
what is inside the frame and leaves this page -- its header, menu and theme --
standing. No script needed for that: `target=` on a plain <a> has done exactly
this since frames existed.

xkcd sends neither X-Frame-Options nor a frame-ancestors policy, so it is one
of the few sites that can be embedded like this at all. If that ever changes
the frame goes blank, which is what the line underneath it is for.
{%- endcomment -%}
<iframe class="xkcd-embed"
        name="xkcd-frame"
        src="https://xkcd.com/"
        title="xkcd"
        referrerpolicy="no-referrer"></iframe>

<p class="xkcd-note">
  Comics are Randall Munroe's, served live from xkcd.com and licensed
  <a href="https://creativecommons.org/licenses/by-nc/2.5/">CC BY-NC 2.5</a>.
  Nothing here is mirrored. If the frame is blank, your browser is blocking it —
  <a href="https://xkcd.com/">read it on xkcd.com</a>.
</p>

<script>
// xkcd's own random button points at c.xkcd.com/random/comic/, which answers
// with a redirect to an *http* comic URL. This site is served over https, so
// that redirect is mixed content and the browser blocks the frame rather than
// following it. Rolling the number here instead keeps every URL on https.
//
// The roll happens ahead of the click, not during it: the href is armed on
// load and re-armed after each use, so the plain target= navigation above does
// the work and this script only chooses where it points. Rewriting the href
// inside the click handler does not work -- Chrome follows the href it read
// when the click began, so every jump would land on the previous roll.
// With JS off the link keeps its authored href and loads today's comic.
//
// data-latest is a floor, not the true latest: nothing on a static site can
// learn today's number (xkcd's JSON API sends no CORS header), so it is the
// count as of this page being written and comics past it are reached with
// xkcd's own Next button. Bump it whenever, or never -- an out-of-date floor
// only narrows the draw, it cannot land on a comic that does not exist.
//
// 404 is skipped because there is no comic 404: xkcd left the number empty as
// the joke, and the URL duly 404s.
(function () {
  var a = document.getElementById('xkcd-random');
  if (!a) return;
  var latest = parseInt(a.getAttribute('data-latest'), 10);
  function arm() {
    var n;
    do { n = 1 + Math.floor(Math.random() * latest); } while (n === 404);
    a.href = 'https://xkcd.com/' + n + '/';
  }
  arm();
  a.addEventListener('click', arm);
})();
</script>
