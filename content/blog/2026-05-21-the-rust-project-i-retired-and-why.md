---
title: "The Rust project I retired, and what it taught me about how I learn"
date: 2026-05-21
author: luke
summary: "A Bitcask-style key-value store with a Rust core and PyO3 Python bindings — designed to teach me Rust the hard way. I retired it. Here's why, and what I'm doing instead."
tags: [project-writeup, minikv, rust, learning, retired, post-mortem]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## What minikv was

`minikv` was supposed to be the project that taught me Rust properly. The design is a Bitcask-style key-value store — the same pattern Riak's storage engine uses — written as a Rust library (`src/lib.rs`) and exposed to Python through PyO3 bindings, built with `maturin`. The end state would have been a `pip install`-able Python package whose hot path is native Rust.

The Bitcask model is small and tidy, which is part of why I picked it. Writes go to the end of a single append-only log file. A separate in-memory keydir holds a `HashMap<Key, FileOffset>` mapping every live key to the byte offset of its most recent value on disk. Reads consult the keydir, seek to the offset, and pull the value out in one I/O operation. Deletes write a tombstone record. The log grows forever, so a periodic compaction pass rewrites a fresh log containing only the live keys and atomically swaps it in. That's the whole design. Six milestones from scaffold to concurrent reads with CRCs and `fsync`.

I picked it for two reasons. It would force me to confront Rust on its own terms — ownership puzzles you can't paper over, lifetimes you have to actually think through, an FFI boundary where you feel every byte you copy. And the Rust-core / Python-bindings pattern itself is a real deployable technique: plenty of production Python codebases bolt a Rust hot path on via PyO3. Knowing how that boundary works is genuinely useful.

The design was sound. The scaffolding got built. Then I sat at `src/lib.rs` with a blank file and a spec, and I didn't write any code.

## What actually happened

It's not that Rust was too hard. Rust *is* hard, but "hard" isn't a blocker — every project I've shipped this year had a hard part. The actual problem was more specific.

minikv was built around an implicit premise: that I learn by writing implementation myself from a blank file, with an AI assistant nearby to nudge me when I get stuck. The project's `claude.md` even had a rule on it — *don't write Rust function bodies for Luke* — to keep the exercise honest.

After a few weeks of not opening the file, I noticed this wasn't a motivation problem. I'd shipped six other things in 2026 — Job Scout, a personal finance dashboard, voice cloning, the smart-home rebuild, a file organizer, a political research tool. I wasn't bouncing off building software. I was bouncing off this specific format: blank file, spec, you go.

What does work for me — what I've been doing all year without naming it — is the inverse loop. I sit with Claude, describe what I want, watch it write the implementation, read the result, ask why it made the choices it made, and push back when something looks wrong. By the third or fourth pass on a given pattern, I can see the design space clearly. I can tell when Claude has reached for the wrong abstraction. I'm not typing the function bodies, but I'm making the architectural calls, and the pattern is in my head afterwards.

That's not a worse mode of learning. It's just not the mode minikv was built for.

## The realisation

The moment I named this was almost embarrassingly casual. I told Claude, more or less, that it's more fun watching it build things and then having it explain them afterwards than it is grinding the implementation myself. Once that sentence was out, the project's whole premise came apart. Every constraint I'd put on Claude was built for a learning style I don't actually have.

So I retired the old rule and inverted it. As of 2026-05-28: Claude builds the implementation, then explains the design choices afterwards — ownership, lifetimes, FFI boundary types, the gotchas. I read, review, and ask why. I don't retype. That sounds like a small policy change but it isn't, because it follows from a bigger thing I'd been avoiding saying out loud.

## What this actually means

I'm an AI-leveraged operator, not a hand-coder.

That's the frame. The portfolio I've built in 2026 is real software that real users (mostly me) actually use, but the implementation work was done largely with AI assistance. My value-add was judgment, direction, integration, and shipping decisions — what to build, why, what shape it should take, when to cut scope. The Job Scout post-mortem is the cleanest example: the valuable insight wasn't writing the Python, it was correctly identifying that a 7B local LLM can't do calibrated judgment under category-edge ambiguity, and ripping the model out. Nobody needs me to hand-type a Flask route. They might need me to call when to delete one.

Once I name that honestly, things follow. The career path that fits is FDE, solutions engineer, founder, or AI-direction roles — not IC engineering at Halter or an embedded shop. Both gate on writing code in live whiteboard interviews. My learning style doesn't develop that skill, and pretending it does by grinding minikv was implicitly preparing me for a career I'm not actually pursuing.

The textbook-style learning resources — Rustlings, the Brown interactive Rust Book, Exercism — aren't going to land for me, and I should stop feeling guilty about that. I read the chapters; I bounce off the exercises. It's not a discipline failure — it's the wrong shape for how my brain encodes patterns.

And admitting this is more useful than completing minikv would have been. A finished minikv would have been a 600-line Rust crate that does what `dbm` already does. Naming my actual learning mode unlocks every project after this.

## What replaces minikv

Not nothing.

The Rust-core / Python-bindings pattern is still one I want available. I just won't get to it by hand-coding a key-value store. I'll get to it the same way I get to every other pattern: wait until a real project needs it, direct Claude to build it, and read the result.

The next concrete instance is already lined up. TenderPilot — my upcoming NZ government tender aggregator, scoped into the gap Job Scout's restructure left behind — has a Rust GETS fetcher in its design. Not because the project needs Rust everywhere, but because the GETS XML feed is the kind of high-throughput parallel-fetch problem where Rust earns its keep over Python. The fetcher will be a Rust binary called from a Python orchestrator. Claude will write it. I'll review the ownership choices, the error handling, the parallelism model, the FFI surface if we go that way. That's the build-and-explain loop applied to a real project where Rust does work Python can't easily do.

I'll learn the pattern there. I won't learn it by completing minikv. There's a queue of follow-on projects where Rust fits the hot path, and the knowledge will accumulate through them — via the loop that works for me, not the one I thought I was supposed to use.

## The honest closing

There's a version of this post that reads as confession — "I tried to learn Rust and failed." That version would be wrong. I haven't failed to learn Rust. I've redefined what learning Rust means for someone in my position.

I don't need to type function bodies to understand patterns. The pattern is what makes architectural calls. The syntax is what AI fills in. As long as I can read a Rust crate, recognise when the ownership model is wrong for the problem, see when a lifetime annotation is doing real work versus just placating the borrow checker, and direct the build at the architecture level — that's the skill that actually pays. minikv was built around the assumption that the syntax reps were the load-bearing part. They aren't, for me.

I get a week of my life back, I stop forcing myself through a learning mode that doesn't fit, and the Rust knowledge I actually want — pattern-level, deployable, real-project-grounded — comes in through TenderPilot and the projects after it instead.

minikv is retired. The Rust isn't.

*— Luke Simmons, Auckland*
