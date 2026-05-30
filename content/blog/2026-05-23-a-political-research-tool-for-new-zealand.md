---
title: "A political research tool for New Zealand"
date: 2026-05-23
author: luke
summary: "A local Flask app combining NZ politician profiles with a combined Vote Compass / Political Compass questionnaire mapped against the actual platforms of NZ parties. What I built, what I left out, and why."
tags: [project-writeup, political-research, nz-politics, civic-tech, build-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## The itch

Every three years a major outlet stands up an election-cycle quiz, you take it once, you screenshot the result, and then the URL rots. The methodology was never documented in a way you could interrogate, and after the election the whole thing disappears.

The other half of the friction is the lookup problem. When I want to remind myself who an MP is, what they actually stand for, and how their party is positioned, I end up in five tabs that don't compose.

I wanted one local tool that did both jobs, that I could pull apart and edit, and that didn't go away after election night. So I built it: a Flask app on `127.0.0.1:5000`, ~175 lines in `app.py`, three editable JSON files in `data/`, and three thin service modules in `services/`. In debug mode it reloads the data files on every request, so I can tweak a party's stance on the wealth tax, hit refresh, and watch the match percentages move.

## What's in it

Three things, deliberately small.

**A party browser.** All seven parties currently in the conversation — Labour, National, Greens, ACT, NZ First, Te Pāti Māori, TOP. Each has a curated profile in `data/nz_parties.json`: leader, founding year, summary, five key policies, a colour, and a Political Compass position. Party pages also pull a live Wikipedia summary as a neutral third-party blurb next to my characterisation.

**An international browser.** Curated entries for a handful of countries in `data/countries.json`, enriched live with Wikipedia. The `/world` page fans the fetches across a thread pool so it loads in the time of the slowest single request.

**A quiz.** Twenty questions in `data/questions.json`, each tagged by category (Economic, Environment, Social, Treaty, Foreign), each with an `econ_weight`, a `social_weight`, and a per-party expected answer on a five-point scale (-2 to +2). Submitting projects your answers onto the Political Compass and computes a Vote-Compass-style percentage match against each party.

## Why a REST endpoint, not a scraper

The Wikipedia integration hits `https://en.wikipedia.org/api/rest_v1/page/summary/<title>`. No API key, no scraping, no HTML parsing — just a small JSON blob with an extract and a link out. Responses are cached in-process for an hour with a six-second timeout. For the use case I'm actually solving — "remind me who this person is in 30 seconds" — a scraper would be overkill.

## The hard part: where do you put each party on the compass?

This is the part that has to be defensible or the whole tool is theatre.

Each party gets a compass coordinate stored in `nz_parties.json`. Labour sits at `(-3, -1)`. National at `(5, 2)`. The Greens at `(-6, -5)`. ACT at `(8, -4)`. NZ First at `(1, 6)` — economically near the centre but socially the most authoritarian of the seven. Te Pāti Māori at `(-5, -2)`. TOP at `(-1, -4)`.

These are not endorsements and the data file says so in a leading `_note` field. They're characterisations based on published platforms, calibrated against each party's official policy pages, their voting record in the House, and the per-question positions I encoded in `questions.json`. The per-question positions are the audit trail. If you think I've put the Greens too far left on the economic axis, you can open the questions file and see exactly which positions on wealth tax, capital gains, welfare, rent controls, and SOE ownership produced that placement. Change the number, refresh, and the compass position shifts.

This matters most for the parties whose platforms don't fit a clean left-right line. NZ First is the standout: economically interventionist in places (protecting SOEs, regional development) but socially conservative and nationalist in a way that doesn't map onto either Labour or National. The Greens are the inverse — a left economic platform paired with a libertarian-leaning social one, which is why they sit in the lower-left quadrant rather than the top-left. TOP doesn't really sit anywhere conventional; their land-value tax and UBI agenda is economically heterodox in a way that a single left-right number genuinely struggles with.

I'd rather show that ambiguity than smooth it away. The compass coordinate is one summary. The per-question breakdown is the real thing.

## How the matching works

The maths is deliberately boring. Per-question similarity is a linear mapping from absolute distance in [-2, +2] into [0, 1]; the overall match is the unweighted mean, expressed as a percent. The compass projection is a separate weighted sum of answers against each question's `econ_weight` and `social_weight`, normalised and clamped to [-10, +10].

Equal weighting per question is a choice. A more sophisticated version would let you mark questions as "important to me" and weight those higher — Vote Compass does this. I haven't built it yet because I want to use v1 through an election cycle first and see whether the unweighted version is actually wrong in practice or just feels wrong in theory.

## What I deliberately didn't build

No predictions. No polling. No vote-share modelling. No "you should vote for X." No tactical-voting calculator that says "in your electorate, your party vote is most efficiently spent on Y." The tool is research, not strategy. The output is "here is how your answers line up with each party's positions, and here is where you sit on the compass" — not "here is what you should do with that information."

I also didn't build a headlines integration. The country page calls a `get_recent_headlines(country_id)` stub in `services/news.py` that returns an empty list. The hook is there if I want to drop in NewsAPI or the Guardian Open Platform later. Anything behind that stub becomes something to maintain across an election cycle, and I'd rather ship the questionnaire first.

## The civic-tech principle

There's a class of small, local-first civic tools that respect the user's intelligence. They show you the data, document their assumptions, let you disagree, and don't tell you what to do with what you've found. The election-cycle quizzes mostly don't — they're built to be consumed once, screenshotted, and forgotten. A tool you can edit, that runs on your own machine, that you can use between elections, is a different kind of object.

That's the version I wanted. So that's the version I built.

## What's next

- Council-level data, starting with Auckland Council and the local boards — the layer of government that affects me most and that I see least.
- A platform refresh before the next general election, since every party will republish policy and the per-question encodings will need a pass.
- An "importance weight" affordance on the quiz, once I've used the unweighted version through a cycle.

None of these are blocking. The tool already does the two things I built it for: it lets me look up an MP or party without leaving the tab, and it gives me a calibrated, editable version of the quiz I take every three years.

*— Luke Simmons, Auckland*
