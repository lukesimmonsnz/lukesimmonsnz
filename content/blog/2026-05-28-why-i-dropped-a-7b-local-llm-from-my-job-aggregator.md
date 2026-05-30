---
title: "Why I dropped a 7B local LLM from my job aggregator"
date: 2026-05-28
author: luke
summary: "A post-mortem of scout_mvp.py — what I built, why I thought local-AI judgment would work, what actually broke, and what replaced it."
tags: [project-writeup, post-mortem, job-scout, local-llm, ollama]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## TL;DR

I built a job aggregator that used a local 7B model (Qwen2.5-7B via Ollama, on an RTX 3070) to score each listing for relevance, growth, and attainability against my profile. It worked end-to-end in one sitting. It also returned verdicts that were systematically wrong in two specific, consistent ways. I dropped the LLM scoring layer and replaced it with a dashboard that surfaces the data and lets me — the human — do the judgment. The model still has a place in the system, just not the place I originally gave it.

This isn't a "local LLMs are bad" post. It's a "local 7B models can't do calibrated judgment under category-edge ambiguity, even when the prompt is good" post — and the spec I wrote *before* building this literally hedged on exactly that. The lesson is about which sub-tasks of the system the model is suitable for, not whether to use one at all.

---

## What I built

A vertical slice: pull a feed, normalise it, score each listing with a local LLM, print the top 10 to stdout. ~230 lines of Python, no database, no dedup.

**Stack:** RemoteOK's public JSON API for fetching (~50–100 listings per call), normalisation into a canonical record with HTML stripped, then per-listing scoring via a local Ollama instance running `qwen2.5:7b`. Composite score = `0.45 * growth + 0.35 * relevance + 0.20 * attainability`, each axis a 0–100 integer the model returned.

The system prompt was the load-bearing artifact: ~40 lines encoding my candidate profile (early-career technical generalist in Auckland, AI-engineering aspiration), in-scope domains, hard exclusions (manual labour, non-NZ-eligible remote), and the three scoring axes.

The hypothesis: a well-prompted local 7B model can do this include/exclude + rough-scoring work reliably enough to be useful. Not perfect accuracy — just "directionally right often enough that I trust the top 10."

It wasn't.

---

## What broke

Two failure modes, both consistent, both fundamental enough that no prompt tweak fixed them.

### 1. Over-aggressive exclusion on category-edge cases

The prompt's hard-constraint clause: *"EXCLUDE any role requiring manual labour, physical lifting, driving, trades, warehouse, hospitality, or on-feet-all-day work."* Reasonable rule, meant for delivery drivers and hospitality managers.

What it actually did: it excluded **"Junior Front End Developer"** with `exclude_reason: "requires manual labour"`.

This wasn't a one-off. The model latched onto incidental words in long descriptions ("ship features," "build pipelines," "hands-on work") and pattern-matched them into the manual-labour bucket. Mentions of a physical office, on-call rotation, or "fast-paced environment" did the same. The model wasn't reasoning about the role — it was running fuzzy keyword similarity against my exclusion list, then writing a plausible-sounding justification.

For a 7B model in JSON mode, this is the dominant failure pattern. Plenty of capacity to produce structured output and pattern-match on surface features. Not enough capacity to hold "what does this role *actually* require" in mind while also holding the rubric.

### 2. Hallucinated location constraints

The location clause required reading the listing carefully and deciding whether the listed location was NZ-eligible (Auckland, NZ-wide, or remote explicitly open to NZ/APAC/worldwide).

What it did instead: it invented constraints that weren't in the listing. A "Remote (Worldwide)" tag would come back as `nz_remote_eligible: false` with `exclude_reason: "appears to require US work authorization"` — even when the listing said nothing about US authorization. Conversely, some US-only roles came back as `nz_remote_eligible: true` because the description mentioned "we hire globally" in a recruiting blurb that didn't reflect actual policy.

Roughly **30–40% of location verdicts were wrong**, in both directions. The model was generating *plausible* location reasoning rather than *grounded* location reasoning. JSON-mode output made the hallucinations more confident-looking, because they came wrapped in structure.

### Why these matter

Either failure mode alone would have been a tuning problem. Together they composed into something worse: the surviving top-10 was systematically biased *away* from exactly the roles I most wanted to see. Front-end and full-stack junior roles got excluded by the manual-labour misfire. NZ-eligible remote roles got excluded by the hallucinated US-only constraint. I read the digests for about a week. The signal-to-noise was worse than browsing RemoteOK directly, which is the failure condition that matters.

---

## What I should have caught before building

The spec I wrote before coding the MVP literally said this:

> **8B model ceiling:** good enough for include/exclude and rough scoring. If you want it to reason about subtle career-fit nuance, that's where the home-lab box and a larger model would earn their keep — but prove you need it first.

I read that, agreed with it, and then built as if I disagreed with it. The fix isn't "trust the model more." The fix is: **judgment-under-edge-cases is exactly the kind of subtlety the spec was hedging against.** The MVP wasn't testing whether the model handled the easy cases (it did). It was testing whether it handled the hard cases — the category boundaries between knowledge work and manual labour, between truly-global remote and let's-say-we-hire-globally remote. It didn't.

The test that matters isn't whether the model handles the typical case. It's whether it handles the cases where the rubric and the data are both fuzzy at the same time.

---

## What replaced it

I dropped the LLM scoring layer entirely. The current system is a Flask dashboard (SQLite-backed) that renders the full job list with filter affordances and lets me do the judgment myself. Triage is fast — 40 listings in 10 minutes.

The honest framing: **the AI was supposed to do the part of the work that's actually mine to do.** The aggregator's value is "Luke's eyes on the right data, fast" — not "AI tells Luke what to apply for." Removing the LLM made the system simpler, faster, and more honest about where the value comes from.

---

## What I'd do if I were doing it again

I'd put the LLM back in — but on different sub-tasks, and with a different model class.

A 7B model is good at **summarisation** (compress a 4,000-character description into a 40-word brief), **tag extraction** (stack, seniority, remote policy, salary range — structured extraction is its home turf), and **cross-source deduplication** (embedding similarity beats keyword matching). It's bad at judgment-against-rubric where the rubric edges are fuzzy. For that, either Luke does it, or you use a Claude/GPT-4-class model and accept the per-call cost — 80 listings/day at ~$0.01 each is $24/month, trivial.

**The architectural decision I'd make differently from day one:** separate "extraction" tasks from "judgment" tasks in the design, not just in retrospect. A v2 of Job Scout would explicitly route those to different model classes — local for extraction, cloud for judgment, human for ranking.

The MVP taught me where the boundary lives. That's worth more than the MVP itself.

---

## The wider lesson, briefly

A lot of 2026 product discussion treats "local LLM" and "cloud LLM" as a deployment-cost trade-off — same capability, different cost curve. That framing misses the point. The local-vs-cloud line is also a **capability line for judgment-shaped tasks**, and it's sharper than people who haven't tried it think. A 7B model on consumer hardware can do extraction, summarisation, classification on clean categories, and structured rephrasing well enough to be useful. It cannot do calibrated judgment when the rubric and the data are both ambiguous — and most real-world filtering problems are exactly that.

If you're designing a system that uses local LLMs for anything, the test that matters is not "does it work on the easy cases." It's "what does it do on the cases where a human would have to think carefully." If the model can't, route those to a larger model or to a human. Don't try to prompt your way out of a capability gap.

---

*Part of an ongoing series of project writeups. Companion piece: [How a 7B local LLM actually processes a job listing](/blog/2026-05-28-how-the-7b-llm-processes-information/) — same project, one layer deeper.*

*— Luke Simmons, Auckland*
