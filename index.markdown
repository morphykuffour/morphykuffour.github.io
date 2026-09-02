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

