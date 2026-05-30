---
title: "streamfinder: a streaming aggregator that knows about NZ free TV"
date: 2026-05-22
author: luke
summary: "An NZ-specific streaming aggregator that combines TMDB provider data with sitemaps from TVNZ+ and ThreeNow — so 'free to watch right now in New Zealand' actually means something. FTS5 search, sitemap parsing, and what's still ahead."
tags: [project-writeup, streamfinder, nz-streaming, sqlite, build-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## The gap I'm filling

If you live in New Zealand and you want to know who's streaming a given title, your options are JustWatch or the others — and JustWatch is also the data source behind TMDB's `/watch/providers` endpoint, so it's implicitly behind most aggregators too. For paid services in NZ it's mostly fine — Netflix, Disney+, Neon, Prime, Apple TV+ all get indexed reasonably well.

The free side is where it falls apart.

TVNZ+ has a catalogue of [CHECK: ~1,200] shows including a large BBC slice that I'm currently paying for via Sky/Neon. ThreeNow has [CHECK: ~580]. Between them you can put together a meaningful "what can I watch tonight without paying for another subscription" answer for a NZ household. JustWatch under-indexes TVNZ+ badly and the matching is patchy enough that I stopped trusting it.

The international aggregators aren't going to bother — NZ is a small market with two free services no global product is going to bend its schema around. So if I want this solved properly, I have to solve it myself.

That's streamfinder.

## What it actually does

- **Search any title** → metadata, ratings, runtime, and every NZ-region streaming provider, with free options surfaced prominently.
- **Free-service search** runs against a locally indexed catalogue of TVNZ+ and ThreeNow, not against a third party's interpretation of those services.
- **Deep links** open the title in the user's existing browser session on the service that has it. No credential storage, no playback, no proxying.
- **Local-first.** SQLite file in `data/streamfinder.db`. The TMDB calls are the only external traffic, logged to `logs/api-calls.jsonl` with the API key stripped.

Stack: Python 3.13, FastAPI on port 8765, HTMX + Tailwind via CDN (no build step — I want to read every line of every template), SQLite with FTS5, TMDB for international provider data, custom sitemap fetchers for the NZ free side. CLI first, web UI second, same data underneath.

## TMDB for the paid side

For the paid services I lean on TMDB's `/watch/providers` endpoint. One call gives you every region in one response, and you slice it client-side. The Python wrapper is about 130 lines including search, details, recommendations, and the provider lookup. The provider data comes from JustWatch under the hood — good for Netflix / Disney+ / Neon / Prime, mediocre for TVNZ+, missing for ThreeNow.

TMDB also gives me canonical metadata plus a useful merged "similar titles" view from combining `/recommendations` (editorial) and `/similar` (algorithmic) — nice for discovery that isn't just "type the name of the thing you already know."

TMDB is the licensed access path. Free, documented, rate-limit-friendly. Scraping JustWatch is fragile and rude. Use the API that exists.

## Sitemap parsing for the free side

This is the part I'm proud of, because it sidesteps a category of problems most people would reach for the wrong tool to solve.

Both TVNZ+ and ThreeNow publish XML sitemaps for SEO purposes:

- `https://www.tvnz.co.nz/sitemap/sitemap-video.xml` — full `<video:video>` blocks with title, description, thumbnail, category, and a `requires_subscription` flag (TVNZ wraps some shows behind a free account).
- `https://www.threenow.co.nz/sitemap_shows.xml` — URL-only entries. Title gets reconstructed from the slug.

Both robots.txt files are permissive, so this is the sanctioned access path. The combined payload is around [CHECK: 1.5 MB], trivial to re-pull nightly. No JavaScript rendering, no API key, no rate limiter to dance around. The data is structured, stable, and — crucially — the format the services *want* search engines to consume. If they break the sitemap, their Google ranking dies, so the format has strong incentives against breaking.

Much better than scraping the front-end, reverse-engineering the mobile APIs, or asking the services for a feed.

The sitemap is *the answer the service already wrote down*. Use it.

The parser is one file (`free_index.py`, ~180 lines), uses `xml.etree.ElementTree`, and produces one row per show with a normalised slug for cross-matching against TMDB titles. Upserts by `(service, service_id)` so re-running is idempotent. Will be scheduled nightly via Task Scheduler once Phase 6 is fully wired up.

## Why FTS5 SQLite over Elasticsearch or Postgres

For a personal-scale project — single user, low thousands of records, on-device — FTS5 is the right answer and it isn't even close.

**Elasticsearch:** absurd. It's a clustered search engine. I have one user. The JVM heap alone would dwarf the rest of the app.

**Postgres + tsvector:** also overkill. Now I'm running a database server, managing a connection pool, writing migrations, and getting search quality that's *worse* than FTS5 for the prefix-typeahead behaviour I want. Postgres is right when you have multiple writers, real concurrency, or you're already running it. For a Windows desktop app with one user, it's a service to babysit.

**FTS5:** virtual table, lives in the same `.db` file as everything else, prefix matching with `term*` syntax for nice typeahead, unicode tokenizer with `remove_diacritics 2` so "pokemon" finds "Pokémon," triggers keep it in sync with the base table automatically. Zero ops. About 20 lines of SQL in the schema plus a 15-line query function.

Tradeoffs I'm accepting: no multi-process writers (only one ingest job writes, WAL mode lets the web app read concurrently), no ranking beyond bm25 (I'm not running Google), no distributed scaling (there is exactly one node and it is my laptop).

Most search-engine choices in side projects are people picking the tool they read about, not the tool that fits the problem. FTS5 fits this problem. If "what if I scale" ever becomes real I can swap the backend behind the same interface — the schema is portable.

## The schema, briefly

The free-catalogue side is `free_titles` (one row per show, unique on `(service, service_id)` for idempotent re-ingest) and `free_titles_fts` (FTS5 virtual table over title + description, kept in sync via three triggers so I never have to remember to reindex). There are also caches for two probes that didn't pan out; schema kept around in case I find a better signal later.

What I haven't built yet: a unified `media` / `watchlist` / `history` set of tables for the full Phase 3 flow. That's coming.

## Where the project is right now

Status as of late May 2026:

- **Phase 1 — CLI + TMDB validation.** Done. `search` and `lookup` subcommands; confirmed TMDB is good enough for the paid side, partial for the free side.
- **Phase 2 — web UI.** Done. FastAPI on 8765, HTMX search, results with provider badges colour-coded by monetisation type, detail page with overseas-region fallback when NZ has nothing.
- **Phase 3 — watchlist + history.** Not built. Highest-value next thing.
- **Phase 4 — Trakt sync.** Not built. Optional, low priority.
- **Phase 5 — LLM recommendations.** Not built. Lower priority than I originally thought (see my recent post about pulling the LLM out of job-scout — same lesson applies here).
- **Phase 6 — NZ free-service indexing.** In flight. Sitemap parsers work end-to-end, FTS5 search runs locally, cross-matching against TMDB by `(slug, year)` is next, then surfacing "Free on TVNZ+" as a prominent badge alongside the paid providers — the actual headline feature for an NZ user.

## What I'm learning about niche regional products

The whole project is a bet on one claim: **the value of a regional product is precisely in the local knowledge that global products won't bother to encode.** JustWatch could index TVNZ+ properly — they choose not to, because the engineering cost isn't worth it at their scale for a market my size. That's the gap, and that's the moat for anyone who lives here and is willing to do the maintenance work.

The cost is exactly what it sounds like: when TVNZ rebrands or ThreeNow restructures their URLs, my parser breaks and theirs doesn't. For a personal project that tax is cheap — the sitemap format is stable for years, and maintenance is roughly one evening every six months. If I were shipping this as SaaS, the calculus would be different.

## What's next

1. **Finish Phase 6** — wire the free-catalogue rows into the main search results so a single query returns paid providers (TMDB), free providers (TMDB, where it knows), and free-catalogue hits (my own index) in one merged view.

After that: Phase 3 (watchlist + history), nightly Task Scheduler refresh with a visible "last successful" timestamp, and better cross-source matching (year + slug + fuzzy fallback so TMDB's "Pokémon" finds TVNZ+'s "Pokemon: Indigo League").

Phase 5 LLM recommendations dropped significantly after the job-scout post-mortem. A deterministic "what's new on the services I subscribe to" view is more valuable to me than a model's vibes-based suggestions. If recommendations come back, they'll be a thin layer on top of structured data, not a black box.

The project is doing what I wanted it to do. It tells me whether something is on TVNZ+ before I open Neon to pay for it. That's the feature.

*— Luke Simmons, Auckland*
