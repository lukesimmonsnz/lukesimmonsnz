---
title: "A personal finance dashboard built around Akahu"
date: 2026-05-25
author: luke
summary: "I built a personal finance dashboard around the Akahu open banking API to stop manually reconciling bank exports. Node and React — which I'd choose differently today. The Akahu integration is the leverage that actually matters."
tags: [project-writeup, akahu, personal-finance, build-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## The problem

I was doing my own financial reconciliation in spreadsheets, which is what most people do, and like most people I was doing it badly. Every month I'd download the bank exports, ctrl-F for each expected payment, tick them off, chase the missing ones, then categorise the rest of the spend by hand. The first time I did it, it took an evening. The second time, two hours. Around the third month I stopped, and the spreadsheets quietly went out of date.

The actual pain wasn't any single one of those tasks. It was the reconciliation step — the part where you sit down with a CSV and your own memory and try to match them against each other. That's the work the dashboard exists to remove.

## What it does

The app is a local-only web app. It runs on my laptop, on my home network, and never leaves the machine — the database holds real bank data, so it has to stay off the internet. The browser tab has a small number of sections: an overview with cashflow charts and balances, a transaction view with filter and re-categorise affordances, and a recurring-payments view that highlights anything expected-but-missing.

The whole thing is wired to [Akahu](https://akahu.nz), New Zealand's open banking API, which is the single biggest reason this tool exists at all. More on that below.

## The stack — and what I'd do differently now

Backend is Node + Express. Frontend is React via Vite. Database is SQLite through `better-sqlite3`. Charts are Recharts. Styling is Tailwind. There are ~31 API endpoints in `server.js` (~1,000 lines) and a handful of backend modules covering the schema, the Akahu client, the categoriser, and the import/sync pipeline.

If I were starting today I'd build this in Python with Flask. Not because Node is bad at this — it's fine at it, and the app works — but because every other project I currently maintain is Python or Rust, and the cognitive switching cost of jumping between Node-flavoured async and Python-flavoured everything-else is real overhead when you're maintaining six projects at once. Consistency matters more than language merit at my scale.

I'm not going to rewrite it. That would be a couple of weeks of work for zero new functionality, and the existing code runs. But I won't start another project in this stack, and that's the honest version of "what would you choose differently." The constraint I set later — Python or Rust only — was set partly because of this project. Maintaining a one-off Node app inside an otherwise Python portfolio taught me that picking a stack per project is a tax I keep paying forever.

Why Node was the right call at the time: I'd just come off a React project, the frontend was going to be the thing I actually saw every week, and going same-language across the stack felt like the right move when I was building this in spare evenings and couldn't afford a Python-to-React context switch every time I wanted to add a column. It was a defensible choice for that moment. It's just not the choice I'd make from where I am now.

## Akahu is the leverage point

The thing that makes this dashboard worth maintaining isn't the React UI. It's that I never have to enter a transaction by hand.

Akahu is an NZ open banking aggregator — it brokers OAuth-style access to the major NZ banks. The user goes through Akahu's portal once, approves enduring consent, and from then on the app can pull transactions from connected accounts on demand. The OAuth flow is the standard authorization-code-for-access-token dance. The token gets stored in SQLite's `config` table and reused on every sync.

The integration is in `backend/akahu.js`. The shape of it:

1. Hit `/accounts` to get the list of connected accounts.
2. For each account, call `/accounts/{id}/refresh` to force Akahu to poll the bank for fresh data (otherwise you get cached results — important during reconciliation).
3. Wait ~8 seconds for the refresh to land. Yes, an 8-second `setTimeout`. Akahu doesn't give you a webhook for refresh-complete on the tier I'm on, and polling for it added more code than the sleep was worth.
4. Fetch transactions with cursor-based pagination, 100 per page, until the cursor runs out.
5. Run each transaction through the categoriser and `INSERT OR IGNORE` into SQLite, keyed on Akahu's unique transaction ID.

The three things that were hard:

**Auth.** OAuth is fine when there's documentation. The fiddly part was the difference between the app token (identifies my app to Akahu) and the user token (identifies me to Akahu as a person who's granted access). Both go on every request, in different headers. I burned an evening on that.

**Dedup between two sources.** There are two sources of truth: CSVs imported from before Akahu was connected, and the live Akahu feed afterwards. They overlap, and they don't share IDs. Imported rows get a composite unique index on `(date, amount_cents, description, reference)`. Akahu rows get a unique index on the Akahu ID. The two never collide because the imported rows have `akahu_id IS NULL` and the partial unique index is scoped to that condition. SQLite's partial unique indexes carried that design — I'm not sure I'd have landed on as clean a solution in Postgres.

**Categorisation rule ordering.** The categoriser is a list of ordered rules matching payee name and reference. The interesting wrinkle is that the same payee can appear under several different formattings — banks change how they emit payee names between financial years, merchants rebrand, payment networks restructure. The categoriser has to be a list of patterns rather than a lookup table because the source data isn't stable. There's a load-bearing comment in the file explaining why one rule has to come *before* another that looks similar — different reference field, different category. Stuff like that is the actual work of an internal tool.

## What's modelled and what isn't

In the schema: accounts, transactions, recurring payment expectations, transaction categorisation rules, plus a small `config` table for the Akahu tokens and a few user preferences.

Not in the schema: anything resembling double-entry bookkeeping. This is a dashboard, not an accounting system. The dashboard exists to make my own reconciliation fast, not to replace anyone else's accounting workflow.

## Lessons from a tool with one user

You can ship ugly when you're the only user. The UI has rough edges. Tab spacing is inconsistent. Some modules borrow half their components from others and the seams show. None of that matters because the only person who sees it is me, and I built it, and I know which buttons do what.

You can also let an ugly internal tool rot, and that's the trap. The dashboard is in active use because I designed it around one painful task — reconciliation — and made that task take 90 seconds instead of an hour. As long as that core loop stays fast, I'll keep opening the app, and the rest of it stays current by osmosis. The week I stop reconciling is the week the whole app starts decaying. The discipline isn't "keep it pretty." It's "keep one loop sharp."

The other lesson: an internal tool's value is the *integration* it owns, not the code it runs. The Akahu connection is the value. The React shell could be Flask, could be a Streamlit prototype, could be a CLI with a Rich table — and the dashboard would be equally useful. What it couldn't be is "manually downloaded CSV files every month." That's the line.

If I built v2, the Akahu integration is the only piece I'd keep verbatim. Everything else I'd port to Python so it stops being the odd-one-out in my portfolio. But there's no v2 on the roadmap, because v1 still does the job. That's the bar for a small internal tool: does it still do the job. Not: is it the stack I'd pick today.

*— Luke Simmons, Auckland*
