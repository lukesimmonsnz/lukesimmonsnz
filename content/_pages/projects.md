---
title: "Projects"
tagline: "Build logs and post-mortems for the things I am working on, have worked on, or have retired."
---

# Projects

A working portfolio. Each entry links to a longer build log or
post-mortem on the [blog](/blog/) — what I built, what worked, what
broke, and what I would do differently. Most of these are
open-source on [GitHub](https://github.com/lukesimmonsnz).

## Local AI on my own hardware

::section-feature-grid{cols=2}
::: column
### [Job Scout — post-mortem](/blog/2026-05-28-why-i-dropped-a-7b-local-llm-from-my-job-aggregator/)

A job-aggregator that asked a local 7B model to score listings. The
scoring layer is the part I retired — what I built, why I thought
local-AI judgment would work, what actually broke, and what replaced
it. A companion post traces a single listing
[through the transformer forward pass, layer by layer](/blog/2026-05-28-how-the-7b-llm-processes-information/),
for the curious about why "let the LLM decide" was the wrong abstraction.
:::
::: column
### [Voice clone](/blog/2026-05-27-cloning-my-own-voice/)

A voice-cloning pipeline trained on my own audio — what it took to make
it convincing, how the listener test went, and where I will actually use
it.
:::
::: column
### [File organiser](/blog/2026-05-24-organising-the-files-on-my-machine/)

A Windows file-organisation system built around the rule that no
automation touches my filesystem without a dry-run first. Everything +
Python `organize` + digiKam, with JSONL logs of every move.
:::
::: column
### [Smart-home design log](/blog/2026-05-26-a-smart-home-on-my-terms/)

A home-automation design built around what I want my house to do — and,
just as importantly, what I do not want it to do. Principles are locked;
hardware is not on the network yet.
:::
::

## New Zealand–specific tools

::section-feature-grid{cols=2}
::: column
### [streamfinder](/blog/2026-05-22-streamfinder-a-streaming-aggregator-that-knows-about-nz-free-tv/)

An NZ-specific streaming aggregator that combines TMDB provider data
with sitemaps from TVNZ+ and ThreeNow — so "free to watch right now in
New Zealand" actually means something. FTS5 search, sitemap parsing, and
what is still ahead.
:::
::: column
### [Political research tool](/blog/2026-05-23-a-political-research-tool-for-new-zealand/)

A local Flask app combining NZ politician profiles with a Vote Compass
/ Political Compass questionnaire mapped against the actual platforms of
NZ parties. What I built, what I left out, and why.
:::
::

## Personal infrastructure

::section-feature-grid{cols=2}
::: column
### [Personal finance dashboard](/blog/2026-05-25-a-personal-finance-dashboard-with-akahu/)

A dashboard built around the [Akahu](https://www.akahu.nz/) open banking
API to stop manually reconciling bank exports. Node and React —
which I would choose differently today. The Akahu integration is the
leverage that actually matters.
:::
::: column
### [This site](https://github.com/lukesimmonsnz)

Flask, Jinja, a single hand-written stylesheet, no JavaScript framework,
no third-party scripts beyond Google Fonts. Frozen to static HTML and
deployed to Cloudflare Pages. The contact form is a Pages Function.
The weekly digest you may have noticed is written by a local agent on
my own hardware.
:::
::

## Retired, with lessons

::section-feature-grid{cols=2}
::: column
### [MiniKV — a Bitcask-style KV store in Rust](/blog/2026-05-21-the-rust-project-i-retired-and-why/)

Designed to teach me Rust the hard way: a Bitcask-style key-value store
with a Rust core and PyO3 Python bindings. I retired it. The post explains
why, and what I am doing instead to learn the same material.
:::
::

## What is not here

The [Aotearoa research project](/research/aotearoa/) is the largest
thing on this site, but it lives under
[Research](/research/) because it is closer in shape to a
long-form research artefact than to a discrete build. The
[Wāhi Pounamu / David Simmons biography](/davidsimmons/) is its own
thing too.
