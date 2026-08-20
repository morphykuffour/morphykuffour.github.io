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
The frieze under the rain: ten pictures run past in a single endless strip.
They are set to one height and left at their own widths, which is what keeps
the line of the strip steady while nothing in it is cropped to a common shape.

They are other people's and I do not know whose. Most look like one hand's
work and two arrived as reposts with the app's chrome still on them, which is
all that can honestly be said, so the caption says that and stops. The two
screenshots had their bars cut off before the pictures were cut to height --
chrome is not picture -- and two more had a mute badge trimmed off the corner
for the same reason. Nothing else in any of the ten was touched.

The strip is written out twice. The loop walks it exactly one pass to the left
and starts over, which puts the copy where the original stood -- so there is no
jump to hide, and no script is needed to hide one.

The images carry no alt text of their own, deliberately: ten of them each
describing a different picture is ten interruptions in the middle of a page,
and none of them is load-bearing -- the strip is a mood, not an argument. The
caption below names what the strip is, once.

They take the theme's own dark-mode handling rather than opting out of it with
`ioda`, which is the opposite of the call the skulls here made before them.
Those were pencil on white and wanted to be the light half of an inverted page;
these are photographs and paintings, and the only right thing to do to a
photograph on a dark page is leave its colours alone.
{%- endcomment -%}
<section class="frieze">
  <h2>Frieze</h2>
  <figure>
    <div class="frieze-window">
      <div class="frieze-track">
        {%- for pass in (1..2) -%}
        {%- for picture in site.data.frieze -%}
        <img src="{{ site.baseurl }}/images/frieze/{{ picture.file }}"
             alt="" width="{{ picture.width }}" height="{{ picture.height }}"
             loading="lazy" decoding="async">
        {%- endfor -%}
        {%- endfor -%}
      </div>
    </div>
  </figure>
</section>

{%- comment -%}
The shoal that closes the page: three stop motions -- a manta rising, a humpback
turning, a whale shark feeding -- crossed over the Windows XP hill. Ten stills
off a clip each, held about a quarter second and replaced. Stills rather than
the footage they were cut from, which is the opposite of the call the five
cascades upstairs make; the reasoning is in _includes/stopmotion.html, next to
the mechanism it explains.

Six reels for three clips, laid along two diagonals that cross in the middle.
One runs manta, whale, whale shark from the top left down to the bottom right;
the other runs whale shark, whale, manta from the top right down to the bottom
left. So each clip sits at two opposite corners of the board and each diagonal
carries all three -- the crossing is between the animals rather than merely
between two lines, which is the whole reason for six rather than three.

The two middles are pulled apart rather than left on top of each other. Dead
centre both diagonals want the same square, and one reel exactly behind another
is a reel you cannot see; a few points either side and the X pinches in the
middle instead, which is the shape it is copied from.

Six reels at a quarter of the board leave the arms clear of each other, which
matters here more than it would on a plain ground: the hill is meant to be seen
between them. Wider and they tile the board and it is a mosaic with a strip of
sky at the top; at this size the X reads as an X and the sweep of the hill runs
under it.

Each clip's two copies are half a pass out of phase. At one phase they are
identical twins holding the same frame at the same moment, which reads as a
mistake; half a pass apart they are one sequence seen at two points in it --
the trick the cascade upstairs plays with three copies of a video, played here
with two copies of a reel.

Where each reel sits is authored here rather than in the stylesheet, three
percentages to a slot, the way the clips over the collage are placed on the
picture. Being percentages, the crossing holds at every width: the reels ride
the board down as it narrows instead of drifting across it, and a seventh is
three more numbers rather than another rule in main.scss.

The hill behind them is an <img> rather than a background, which is what gets it
the theme's dark-mode handling for free -- the page inverts whole and re-inverts
<img> back to true tone, and a CSS background would be the one thing on the
board coming out in negative. It is absolutely positioned and covers the square,
so it sets no height of its own; the board's ratio does that.

The clips are other people's, and so is the hill. Two of the clips carry their
maker's line burnt into the picture, which is a caption I did not write and will
not crop off; the caption under the board says all of it.
{%- endcomment -%}
<section class="shoal">
  <h2>Three, crossing</h2>
  <figure>
    <div class="shoal-board">
      <img class="shoal-ground" src="{{ site.baseurl }}/images/bliss.jpg" alt=""
           width="2048" height="1152" loading="lazy" decoding="async">

      {%- comment -%}
      The first diagonal, top left down to bottom right.
      {%- endcomment -%}
      <div class="shoal-slot" style="--slot-left: 0%; --slot-top: 0%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="manta" count=10 width=480 height=854 pace="2.5s"
              label="Ten frames of a manta ray rising through blue water towards the surface, from a distant speck to a white underside filling the frame." -%}
      </div>
      <div class="shoal-slot" style="--slot-left: 31%; --slot-top: 21.55%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="whale" count=10 width=480 height=854 pace="3.1s"
              label="Ten frames of a humpback whale turning through deep blue water below a broken surface, trailing a long cloud of bubbles behind it." -%}
      </div>
      <div class="shoal-slot" style="--slot-left: 76%; --slot-top: 43.1%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="whaleshark" count=10 width=480 height=854 pace="3.7s"
              label="Ten frames of a whale shark: a pale open mouth filling the frame head-on, then the spotted back and tail passing overhead through a cloud of small fish." -%}
      </div>

      {%- comment -%}
      The second, top right down to bottom left, carrying the same three the
      other way round and each of them half a pass behind its own first copy.
      {%- endcomment -%}
      <div class="shoal-slot" style="--slot-left: 76%; --slot-top: 0%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="whaleshark" count=10 width=480 height=854 pace="3.7s" phase="-1.85s"
              label="The same whale shark sequence, half a pass further on." -%}
      </div>
      <div class="shoal-slot" style="--slot-left: 45%; --slot-top: 21.55%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="whale" count=10 width=480 height=854 pace="3.1s" phase="-1.55s"
              label="The same humpback sequence, half a pass further on." -%}
      </div>
      <div class="shoal-slot" style="--slot-left: 0%; --slot-top: 43.1%; --slot-width: 24%">
        {%- include stopmotion.html
              dir="manta" count=10 width=480 height=854 pace="2.5s" phase="-1.25s"
              label="The same manta sequence, half a pass further on." -%}
      </div>
    </div>
    <figcaption>
      Thirty stills off three clips, ten each &mdash; a manta rising, a humpback
      turning, a whale shark feeding &mdash; crossed twice over Bliss, the hill
      Charles O&rsquo;Rear photographed for Windows XP. None of it is mine: not
      the footage, not the lines written across two of the clips, not the hill.
    </figcaption>
  </figure>
</section>
