---
layout: home
---

{%- comment -%}
The board that closes the page. It is one flattened image rather than a grid of
separate files because the overlaps are the point -- the tiles are arranged, not
laid out -- and no CSS grid would hold that arrangement across widths. Saved as
a JPEG at the collage's own resolution, which is roughly twice the column, so it
stays sharp on a retina screen without carrying a 2MB PNG onto the front page.

Nothing here is mine; the images are other people's work, saved the same way the
ones on /art/ were. This one has no per-image credit to give, so it stands as a
board rather than a gallery.

Two more clips are hung over the board, in the same three-copy stack the two
further up the page use. They are not floated like those: a float would push
the image out of the way rather than sit on it, so each one is wrapped in an
absolutely positioned box and the board is its containing block.

Where each box goes is authored here rather than in the stylesheet, the way the
stacks upstairs hand over their clip's aspect ratio -- these are percentages of
this particular picture, measured against the arrangement they sit in, and a
rule per clip in main.scss would only be those same numbers a file away from
the thing they describe. Being percentages, the composition holds at every
width: the clips ride the board down as it scales instead of drifting across it.

They are placed to land in the board's own white space -- the empty top right,
the strip down the top left, the gap under the left column -- so they read as
three more tiles on it rather than as something dropped over the pictures.
{%- endcomment -%}
<figure class="home-collage">
  <img src="{{ site.baseurl }}/images/collage.jpg"
       alt="A tall collage of saved images overlapping down the page: paintings, film stills, a manga panel, a terminator skull, big cats, a raven on a skull, and a polar bear on a snowboard.">
  <div class="collage-clip" style="--clip-left: 57%; --clip-top: 2%; --clip-width: 40%">
    {%- include cascade.html
          file="riders" width=640 height=360
          label="Black and white cuts from a fantasy film: a mud-caked armoured figure, a dragon passing over horsemen on a hillside, a white-haired man under a tree." -%}
  </div>
  <div class="collage-clip" style="--clip-left: 0%; --clip-top: 4%; --clip-width: 21%">
    {%- include cascade.html
          file="yinyang" width=480 height=854
          label="An overhead night shot of a round pool, where a black cat and a pale one circle each other and settle into a turning yin-yang." -%}
  </div>
  <div class="collage-clip" style="--clip-left: 0%; --clip-top: 72%; --clip-width: 28%">
    {%- include cascade.html
          file="frogs" width=480 height=480
          label="A cartoon of four frogs riding in a cream-coloured car along a road." -%}
  </div>
</figure>

{%- comment -%}
The rain that closes the page, under the board. Pure CSS: there is no script
behind it and no <canvas> -- an integer is animated in the stylesheet, read back
through counters, and printed as glyphs, after the technique in
https://dev.to/tetragius/pure-css-matrix-code-effect-5b6k. What falls is older
than the film's katakana; the alphabets are in main.scss, where a counter style
is just a list of symbols.

The columns are written out rather than drawn, because each one has to carry
three numbers of its own: how long its fall takes, how far into that fall it
starts, and where it parks when the reader has asked for less motion. Without
the middle one they fall in step, which is a curtain rather than rain; without
the last one they park above the band, which is a black box with nothing in it.
The numbers come off the loop counter rather than being written out one by one
-- three multipliers, each coprime to its modulus, so no two columns get the
same pair and the pattern does not repeat across the band.

Twenty-six of them. They divide whatever width the band has between them, so
this is the count at every screen size; it is a number picked for how it looks
rather than for anything the layout needs.
{%- endcomment -%}
<div class="matrix-rain" aria-hidden="true">
  {%- for column in (1..26) -%}
  {%- assign pace = forloop.index0 | times: 7 | modulo: 9 | times: 5 | plus: 40 -%}
  {%- assign lag = forloop.index0 | times: 13 | modulo: 19 | times: 4 -%}
  {%- assign rest = forloop.index0 | times: 11 | modulo: 7 | times: 12 | minus: 30 -%}
  <span style="--pace: {{ pace | divided_by: 10.0 }}s; --lag: -{{ lag | divided_by: 10.0 }}s; --rest: {{ rest }}%"></span>
  {%- endfor -%}
</div>

{%- comment -%}
The skulls under the rain: sixteen studies of one skull from sixteen angles,
rolling past in a single endless strip. They are Jeff Searle's, sliced out of
one sheet of his and listed in _data/skulls.yml, which carries each one's own
width -- the drawings are not all the same shape, and a lazy image without its
size reserves the wrong box and shifts the strip when it lands. The credit is
in the caption
because the sheet's own signature sat in the margin under the bottom-left
drawing, and a margin is the one part of a sheet that does not survive being
cut into sixteen; said in words under the strip it is legible, which at this
size it never was.

The strip is written out twice. The loop walks it exactly one pass to the left
and starts over, which puts the copy where the original stood -- so there is no
jump to hide, and no script is needed to hide one.

The images carry no alt text of their own, deliberately: sixteen of them saying
"a skull, from a slightly different angle" is sixteen interruptions for one
idea, and the caption below says the whole of it once. The class on them is the
theme's, and it is what keeps the page's dark mode from inverting them back to
ink-on-white -- pencil lines on a dark page want to be the light half, not a
white box with a drawing in it.
{%- endcomment -%}
<section class="skull-roll">
  <h2>Heads will roll</h2>
  <figure>
    <div class="skull-roll-window">
      <div class="skull-roll-track">
        {%- for pass in (1..2) -%}
        {%- for skull in site.data.skulls -%}
        <img class="ioda" src="{{ site.baseurl }}/images/skulls/{{ skull.file }}"
             alt="" width="{{ skull.width }}" height="{{ skull.height }}"
             loading="lazy" decoding="async">
        {%- endfor -%}
        {%- endfor -%}
      </div>
    </div>
    <figcaption>
      Sixteen studies of one skull by
      <a href="https://jeffsearle.blogspot.co.uk/" rel="noopener">Jeff Searle</a>,
      off a single sheet of his. The drawings are his, not mine.
    </figcaption>
  </figure>
</section>
