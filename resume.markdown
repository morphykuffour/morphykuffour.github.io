---
layout: page
title: Resume
permalink: /resume/
description: >-
  Resume of Morphy Kuffour — Linux-focused technology professional with
  experience in cybersecurity, cloud engineering, MLOps, and infrastructure
  automation.
---

{%- comment -%}
  Both URLs come from _config.yml and point at morph-k/resume, which owns the
  LaTeX and publishes the built PDF to its own Pages site. Embedding that file
  rather than a copy kept here is what makes this page current: a push there
  rebuilds the PDF, and the next load of this page picks it up. Nothing in this
  repository has to be rebuilt or redeployed for the change to show.
{%- endcomment -%}

<p class="paper-actions">
  <a href="{{ site.resume_pdf }}">Download the PDF</a>
  <a href="{{ site.resume_source }}">LaTeX source</a>
</p>

<object class="resume-embed"
        data="{{ site.resume_pdf }}#view=FitH&amp;toolbar=0"
        type="application/pdf">
  <p>Your browser will not display the PDF inline —
     <a href="{{ site.resume_pdf }}">download it instead</a>.</p>
</object>
