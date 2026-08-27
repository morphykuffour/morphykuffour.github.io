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
The shoal that closes the page: three stop motions -- a manta rising, a humpback
turning, a whale shark feeding -- crossed over the Windows XP hill. Ten stills
off a clip each, held about a quarter second and replaced. Stills rather than
the footage they were cut from, which is the opposite of the call the seven
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
  </figure>
</section>

{%- comment -%}
The picture under the shoal: three skulls in a row, drawn in
braille dots. Fifty-one glyphs to a line and sixteen lines, each glyph a 2x4
grid of dots, which is 102 by 64 pixels' worth of picture carried as text.

Text rather than a picture file, and that is the whole point of it being here.
Everything around it is images and video -- a collage, two rolls, seven
cascades, six reels, and the pair below -- and this is the one thing in the
list that is none of those: an image made of characters, in the same monospace
the theme sets for the body, that survives being copied out of the page and
pasted somewhere else. It also costs no request and no bytes beyond the markup,
which after a megabyte of whale is a joke worth making quietly.

The third skull on the page, after Searle's sixteen studies of one and the one
on the collage. That is not a plan, but it is why this sits here rather than
anywhere else: the page has been circling the subject and this is the last word
on it.

`role="img"` with a label, because a screen reader handed the markup reads
eight hundred braille cells one at a time. The label is what a sighted reader
gets in a second; the dots are not text and should not be read as text.
{%- endcomment -%}
<section class="cairn">
  <pre role="img" aria-label="Three skulls in a row, drawn in braille dots: a large one at the left in three-quarter view with its eye sockets and teeth, a second overlapping behind it, and a smaller third turned away at the top right.">⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣶⣶⣶⣶⣶⣦⣄⡀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣾⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⣀⣀⡀⠀⠀⠀⠀⠀⢀⣈⣿⣶⣿⣿⣿⡿⢿⣿⡿⠛⠙⠻⣿⣿⡇⠀⠀
⠀⠀⠀⠀⠀⣀⣤⣤⣶⣶⣆⣀⣤⣄⡀⠀⠀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⢀⣿⣿⣿⣿⡿⠿⠚⠀⢀⣾⣧⡀⠀⠀⠀⠀⠑⠄⠀
⠀⠀⠀⣤⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣤⣰⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣜⠇⣇⠹⠋⠀⠀⠀⠀⢨⣿⠿⢦⡀⠀⠀⠀⠀⡀⠀
⠀⠀⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡆⣿⣏⠀⠀⠀⠀⣀⣿⠇⠀⠀⢷⣆⣸⣀⣰⣿⣇
⠀⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣸⣿⣿⣷⣶⡾⢟⠁⠀⠀⢀⠀⣹⣟⡉⠀⠈⠻
⢀⣿⡏⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧⣾⣤⣤⣴⣾⣿⣿⣾⡆⠀⠀⠀
⠀⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⣿⣿⣿⠿⣿⣿⠁⠀⠀⠀⠀⢸⣿⣿⣿⠇⠀⠀⠙⣿⠛⢙⣛⠿⢿⣿⣿⣿⡯⠿⠿⠏⠏⢃⠀⠀⠀
⠀⢠⡏⠁⠀⠀⠀⠙⣻⣿⣿⣿⡿⠿⠻⠿⡛⡀⣾⣿⣦⣤⡄⣀⣀⣰⣿⠟⣿⣂⠀⠀⠀⣷⠀⣺⣿⣧⢈⣥⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢀⡆⢄⡄⠀⢀⣠⣴⣿⣿⣿⠿⠀⠀⠀⠀⠈⢣⣿⣿⣿⣿⣷⣿⣿⣿⣿⠀⢘⣿⣷⣶⣾⣿⡆⠸⠿⢿⣿⠟⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢿⢿⣿⣷⣴⣿⣿⣿⠟⠁⢸⣧⡄⠀⠀⣀⣴⡷⠻⢿⣿⣿⣿⣿⣿⣿⣧⣠⣤⣿⣿⣿⣿⣿⣿⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⢨⢻⣿⣿⣿⣿⣿⡃⢀⣀⢀⣯⣿⣿⣶⣿⣿⡇⠀⠀⠉⠉⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠻⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⢸⣿⣿⣿⣿⣿⣾⣯⣴⣿⣿⢿⣿⣿⡿⠃⠀⠀⠀⠘⢾⣿⡟⡿⠛⠛⠛⢿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠐⠿⠿⣿⢿⡿⢿⣿⣿⣿⣿⣽⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠛⠛⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀</pre>
</section>

{%- comment -%}
The three pictures that close the page, under the cairn: a portrait of a geisha
drawn in the manner of a woodblock print, a katana laid across its stand with
the scabbard behind it, and a starter pack of new year's resolutions. None is
mine. All three were saved off the web with no name attached -- the last one
carries two handles in its own bottom corner and nothing else, and the other
two came with filenames that say only what they are. So what stands under them
is the alt text and nothing more: there is no credit to give and inventing one
would be worse than the silence.

Plain <img> stacked down the column, rather than a board or a roll. The two
things this page already does with more than one picture are both here -- the
collage arranges its tiles and the two strips run theirs past -- and three is
still too few for either: a strip of three is a strip you have seen the whole
of at a glance, and an arrangement of three is a picture with two pictures next
to it. At the column's width, one under the other, they are simply the last
three things on the page.

Tall, then wide, then tall again, which is the order they arrived in and also
the better one: the portrait is a column, the sword is a line across it, and
the starter pack is a column again -- so no shape follows itself, and the sword
is the rule between the two pages of type either side of it.

The last is the odd one, and it is the reason it is last rather than tucked
into the collage upstairs. The tiles up there are things I like; this is a list
of instructions, and read after the skulls it is either the answer to them or
the joke about the answer -- twenty-odd things to do about mortality, laid out
with the confidence of a supplement label. The page has spent itself on what I
am interested in. This is what one is supposed to *do*.

None of the three needs a dark rule, for the reason the collage gives: the
theme inverts the page whole and inverts <img> back again, so all keep true
tone -- the portrait's paper ground, the sword's black field, and the starter
pack's white sheet of type included, which is the half of this that a CSS
background would have got wrong.
{%- endcomment -%}
<section class="coda">
  <img src="{{ site.baseurl }}/images/geisha.jpg"
       width="1182" height="1920" loading="lazy" decoding="async"
       alt="A woodblock-style portrait of a geisha in three-quarter view: white face, black hair pinned up with lacquered picks and a white chrysanthemum, wearing a rust kimono patterned with pale blossoms over a blue collar, against a pale ground hung with two columns of calligraphy.">
  <img src="{{ site.baseurl }}/images/katana.jpg"
       width="1280" height="853" loading="lazy" decoding="async"
       alt="A katana drawn from its black scabbard and laid blade-up across a lacquered stand, the scabbard crossed behind it, against a black field. The stand's rail is painted with a gold-faced dragon in green and orange among clouds.">
  <img src="{{ site.baseurl }}/images/unrecognizable.jpg"
       width="595" height="742" loading="lazy" decoding="async"
       alt="A poster headed 'Become Unrecognizable in 2026 — Your New Year's Resolution Starter Pack': two dozen cut-out pictures crowded on a white sheet, each labelled in serif type. Lift 3x weekly, face your fears, meditate 10 min daily, no more weed, no screens 1 hr before bed, 10K steps daily, let God lead the way, control your breath, limit alcohol, liver and oysters 1x weekly, 3 nutrient-dense meals daily, ground 15 min daily, 100g protein daily, forgive others and yourself, 30 min AM sunlight, practice gratitude, dry brush before showers, no more porn, seek the truth, no more doomscrolling, sex 3x weekly, stay hydrated, coffee enema 1x weekly, sauna 3x weekly. The pictures are a kettlebell, a spider, a woman's face with a third eye, a footprint, a lit figure seen from behind, a slab of liver and an oyster, a whisky glass, a tree with a figure inside it, a steak, an anatomical heart, a bowl of fruit and eggs, a sun's face, a dry brush, an eye in an open palm, a phone, and a bag of dark liquid. Signed in the corner @alexorton.nd and @kolbyourada.">
</section>
