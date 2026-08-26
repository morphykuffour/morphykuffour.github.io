---
layout: page
title: interesting white papers
permalink: /papers/
description: >-
  Papers I keep going back to, mirrored here as PDFs, each shown by its own
  front page with a line on why it is worth the afternoon.
---

{%- comment -%}
A shelf, read front-cover-out. The strip at the top is the first page of each
paper as it was typeset, and the list under it is the record: title, authors,
where it appeared, and why it is here.

The front page is the cover on purpose. A paper has no jacket art, and any
thumbnail I invented for one would be a picture of my opinion of it rather than
of the paper -- whereas page one already carries the title, the authors, their
institutions and the abstract, set the way the authors set them. It is also
exactly what opening the file shows, so the strip and the download agree.

The covers are rendered from the mirrored PDFs rather than checked in from
somewhere else, so a paper cannot end up on the shelf under another paper's
face. They are ink on white at 1200px tall, which is legible enough to read the
title and the abstract's first lines without opening anything.

Every paper is mirrored into assets/papers/ instead of linked to its publisher.
See the head of _data/papers.yml for why; the short version is that half of
these have already moved once.

The strip itself is _includes/carousel.html, shared with /art/ and /unc/. It
takes each slide's link ready-made, which is why the data file spells the PDF
path out rather than leaving it to be built here.

The wrapper around it is the one thing this page needs that those two do not.
Their slides are photographs and are left alone in every mode; these are black
type on a white sheet, which on the purple page arrives as a slab. The class
gives that rule something to hang off without the shared include growing a
parameter for one caller.
{%- endcomment -%}
{%- assign papers = site.data.papers -%}
{%- if papers and papers.size > 0 -%}
{%- capture papers_base -%}{{ site.baseurl }}/images/papers/{%- endcapture -%}
<div class="whitepaper-shelf">
{% include carousel.html items=papers base=papers_base label="Paper front pages" unit="paper" %}
</div>

{%- comment -%}
The list repeats no more of the cover than the title. Everything here is what a
picture of page one cannot be asked to carry: who wrote it, where it landed,
the reason it is on this page, and a link that downloads rather than zooms.
{%- endcomment -%}
{%- for paper in papers -%}
<article class="whitepaper">
  <h2 class="whitepaper-title">
    <a href="{{ site.baseurl }}/assets/papers/{{ paper.pdf }}">{{ paper.title }}</a>
  </h2>
  <p class="whitepaper-credit">{{ paper.authors }} &middot; {{ paper.where }}</p>
  {%- if paper.note %}
  <p class="whitepaper-note">{{ paper.note }}</p>
  {%- endif %}
</article>
{%- endfor -%}

{%- else -%}
<p class="whitepaper-none">
  Nothing on the shelf yet: the page is filled from
  <code>_data/papers.yml</code>.
</p>
{%- endif -%}
