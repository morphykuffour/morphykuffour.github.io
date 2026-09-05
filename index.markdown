---
layout: home
---

{%- comment -%}
The clip that opens the page, ahead of everything else in it. Four lightsabers
in black and white, cut down to twenty seconds; nothing here is mine.

The same three-copy stack the crown beside the menu takes, and for once the
arrangement is doing more than decorating: the clip is a figure with four arms
moving at once, and three copies of it a third of a pass apart is that idea
run again at the level of the whole frame -- the same body in three places,
which is what the shot is about.

Unfloated, unlike the two stacks that stand beside lists a page apart. Those
push the lines next to them aside; this one has nothing beside it to push, so
it takes the middle of its own line and the width the column allows. That is a
class on the section rather than a parameter to the include, because it is a
fact about where this stack sits, not about how a stack is built -- and it is
its own class rather than the one the pair above the rain uses, because that
pair is a row of two and this is a clip alone on a line.

{%- endcomment -%}

<section class="opening">
  {%- include cascade.html
        file="grievous" width=640 height=360
        label="Black and white footage of General Grievous, four lightsabers lit, turning in the middle of a battle." -%}
</section>


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
The pair between the board and the rain: two more clips in the same three-copy
stack, and the last footage on the page.

Side by side rather than one under the other, which is the whole of what makes
them a pair instead of two more things in the column. The two are cut opposite
ways -- a tall frame with a line of skydivers strung head to foot down it, a
squat one with a herd running across -- so in a column they would read as two
unrelated boxes with a gap between them. On one line they are a portrait and a
landscape of the same idea: bodies going somewhere fast, once down the frame
and once across it.

Here rather than anywhere else because of what is under them. The band below is
the page's one unphotographed thing, twenty-six columns of dead alphabets
falling; above it the last two clips are men falling through air and horses
walking into fog until the fog has them. The rain takes the falling over when
these have finished with it.

The widths are authored here rather than in main.scss, the way the clips over
the board are placed on it. They are also not a matter of taste: a 9:16 frame
at 27% of the column and a 5:4 one at 60% come out the same height to within a
rounding error -- 0.27 x 854/480 and 0.60 x 512/640 are both 0.48 -- so the two
sit on one line rather than one of them hanging below the other. Being
percentages, that holds at every width the row survives, and a third clip of
some third shape is another number here rather than another rule down there.
{%- endcomment -%}
<section class="interlude">
  <div class="interlude-clip" style="--clip-width: 27%">
    {%- include cascade.html
          file="divers" width=480 height=854
          label="A line of ten skydivers in freefall over farmland, strung head to foot down the frame; the shot cycles through a burnt orange, black and white, and a negative in which the divers come up gold against an orange ground." -%}
  </div>
  <div class="interlude-clip" style="--clip-width: 60%">
    {%- include cascade.html
          file="horses" width=640 height=512
          label="Grainy black and white footage of a herd of dark horses coming across a field and walking on into fog, until the fog has all but the nearest of them." -%}
  </div>
</section>



{%- comment -%}
The rain that closes the page, under the board and the pair below it. Pure CSS:
there is no script behind it and no <canvas> -- an integer is animated in the
stylesheet, read back through counters, and printed as glyphs, after the
technique in
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

The strip itself is _includes/roll.html: the doubled track, the loop that walks
it one pass and starts over, and the reasons for both. The skulls under this
one run through the same include, which is why neither this section nor that
one says anything about how a roll is made.

These take the theme's own dark-mode handling rather than the include's `ioda`
opt-out, which is the opposite of the call the skulls below make. Those are
pencil on white and want to be the light half of an inverted page; these are
photographs and paintings, and the only right thing to do to a photograph on a
dark page is leave its colours alone.
{%- endcomment -%}
<section class="roll frieze">
  <figure>
    {%- include roll.html data=site.data.frieze dir="frieze" -%}
  </figure>
</section>

{%- comment -%}
The skulls under the frieze: sixteen studies of one skull from sixteen angles,
rolling past in a strip of their own under the strip of photographs. They are
Jeff Searle's, sliced out of one sheet of his and listed in _data/skulls.yml,
which carries each one's own width -- the drawings are not all the same shape.

Two rolls rather than one mixed strip, and this is the whole of why: these are
sixteen views of a single object and those are ten unrelated pictures. Run
together they would read as one grab bag in which the skulls happen to recur;
kept apart, each strip is the kind of thing it is, and only the second one can
carry a credit and a line about looking at one thing sixteen times.

The credit is in the caption because the sheet's own signature sat in the
margin under the bottom-left drawing, and a margin is the one part of a sheet
that does not survive being cut into sixteen; said in words under the strip it
is legible, which at this size it never was.

The `ioda` on the images is the include's opt-out from the theme's dark mode,
and it is what keeps that mode from inverting these back to ink-on-white --
pencil lines on a dark page want to be the light half, not a white box with a
drawing in it.
{%- endcomment -%}
<section class="roll skull-roll">
  <figure>
    {%- include roll.html data=site.data.skulls dir="skulls" ioda=true -%}
  </figure>

  {%- comment -%}
  The line under the roll, which is there because it describes the sheet's
  situation rather than the drawings on it. Sixteen studies of one skull are an
  attempt at the same object over and over, none of them final, and the passage
  is about exactly that: no absolute knowledge, only a method for working out
  which of the available accounts holds.

  Searle's own words, from his post on Plato's dialectic -- he is the man whose
  sheet was cut, which is why the credit and the line come from the same person,
  and why this sits inside the roll's section rather than off on its own between
  two things.

  Inside .skull-roll rather than between it and the shoal, for the same reason:
  it belongs to the drawings above it. The gap below is the shoal's own top
  margin, so nothing here needs to make one.
  {%- endcomment -%}
  <blockquote class="roll-epigraph">
    <p>&ldquo;It is a fact of &lsquo;the human condition&rsquo; that we <i>Homo
      sapiens</i>, not being gods, do not enjoy absolute knowledge &ndash; what
      individuals or even entire societies can know with certainty about the
      universe is profoundly limited. The human world therefore is full of
      opinions, many of them in conflict, and it can be hard to tell the
      difference between truth and mere belief. Rather than despairing at the
      possibility of ever arriving at truth, we need a philosophical method that
      can help us to navigate the wealth of available opinion and work out what
      is true and what is not.&rdquo;</p>
    <cite>&mdash; Jeff Searle,
      <a href="https://jeffsearle.blogspot.com/2021/06/dialectics-part-3-plato.html"
         rel="noopener">Dialectics, part 3</a></cite>
  </blockquote>
</section>

{%- comment -%}
all hail hydra
{%- endcomment -%}

<figure class="hydra">
<img src="{{ site.baseurl }}/images/hydra.jpg"
       alt="all hail hydra">
</figure>

<section class="dance of death">
  <figure>
    {%- include roll.html data=site.data.skulls dir="skulls" ioda=true -%}
  </figure>

  {%- comment -%}
  Dance of Death
  {%- endcomment -%}
  <blockquote class="roll-epigraph">
    <figure class="hydra">
    <img src="{{ site.baseurl }}/images/dance_of_death.jpg"
           alt="all hail hydra">
    </figure>
    <p>&ldquo;Dance of Death (replica of 15th-century fresco; National Gallery of Slovenia); Representing the universality of death regardless of class or job
  </blockquote>
</section>

