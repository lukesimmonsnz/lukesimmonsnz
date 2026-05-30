---
title: "Organising the files on my machine, safely"
date: 2026-05-24
author: luke
summary: "A Windows file-organisation system built around the rule that no automation gets to touch my filesystem without a dry-run first. Everything + Python organize + digiKam, with JSONL logs of every move."
tags: [project-writeup, file-organizer, automation, build-log]
status: published
---

*Author's note: this post was drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing. The voice and judgments are mine; the typing isn't.*

## The mess

The trigger was a specific moment: I was building my website, wanted photos of my grandfather (David Roy Simmons, ethnologist, 1930-2015), and after twenty minutes of clicking around realised the photos I needed had been sitting inside Windows Mail's attachment cache the whole time. The full path, for the record:

```
C:\Users\Luke Simmons\AppData\Local\Packages\
  microsoft.windowscommunicationsapps_8wekyb3d8bbwe\
  LocalState\Files\S0\4\Attachments\
```

774 files, 227 MB, completely invisible to normal browsing. That was the prompt to audit the rest. A few highlights:

- `C:\Users\Luke Simmons\Downloads`: **5,680 files, 3.47 GB** — mostly `.jar` and `.class` debris from a university Minecraft modding project.
- `D:\Downloads`: **929 files, 19.40 GB**, most under 30 days old — the *actual* active Downloads folder.
- `D:\Documents` and `D:\Hard Drive - SONY`: near-identical extension profiles. One was almost certainly a forgotten backup of the other.

In total, roughly **7,500 files in active staging locations** plus ~2,700 photo candidates to consolidate. None of it would fit in my head, which is why I'd been ignoring it.

## The two-pronged tool choice

I installed [Everything](https://www.voidtools.com/) (Voidtools) for instant filename search. That solved half the problem — the Mail-cache discovery would have taken thirty seconds with Everything installed, instead of a year of low-grade frustration.

For the actual sorting I picked [`organize`](https://organize.readthedocs.io/) — Python, MIT-licensed, YAML-configured. The rules live in `config\config.yaml` and `organize sim` runs the whole pipeline in dry-run mode without touching disk. The rules themselves are boring (e.g. `D:\Downloads` images → `D:\Photos\Inbox\{created.year}-{created.month}\`). Boring is the point. The cleverness lives in everything *around* the rules engine.

## The safety design — this is the writeup

This isn't really "a file organiser." It's a set of safety gates wrapped around a file organiser. Every design decision was about not eating my data.

**Rule 1: never delete. Move, don't `rm`.** When the destination is unclear, the rule moves the file to `D:\Quarantine\YYYY-MM-DD\` and leaves it there for a week. I have not yet found a "delete this file" rule worth writing.

**Rule 2: dry-run first, every time, no exceptions.** `organize sim` walks every rule against the real filesystem and prints what *would* move. The hard rule: no rule runs for real until it's had a full successful dry-run pass with output I've actually read. This caught at least one bug per rule on average.

**Rule 3: every operation writes a JSONL log line.** I wrote a custom `organize` action (`actions/log_move.py`, ~80 lines) that wraps `shutil.move` and `shutil.copy2` with structured logging. Every move writes one line to `logs\moves.jsonl`:

```json
{"ts": "...", "rule_id": "downloads-images", "reason": "...",
 "mode": "move", "src": "...", "dest": "...", "size": 123456}
```

The log is the audit trail and the rollback trail — if a rule goes wrong I can scan the JSONL, find every file the bad rule touched, and reverse those specific moves.

**Rule 4: copy-only mode for irreversible sources.** The Mail attachment cache is the canonical case. Windows Mail may still need the originals, so the rule that pulls from `microsoft.windowscommunicationsapps_8wekyb3d8bbwe\LocalState\Files\` runs in `mode="copy"`, never `mode="move"`. The `log_move` helper also short-circuits if a same-name same-size file already exists at the destination.

**Rule 5: off-limits directories are explicit.** The config has a fixed exclusion list — `D:\SteamLibrary`, the Hyper-V VM, `D:\ai-website-manager` (this website), plus the usual `.venv\`, `.git\`, `node_modules\`. The rules engine is not allowed to make decisions about my active project folders.

## digiKam, for the photo half

I didn't build my own photo deduplicator. [digiKam](https://www.digikam.org/) already does it better than I would have, so I used digiKam. The split worked out clean: `organize` handles the ongoing flow (new images land in dated inbox folders), digiKam handles the one-time consolidation pass and perceptual-hash dedup.

## What broke

A compressed-files rule matched too broadly on its first dry-run — it would have swept up `.tar` and `.gz` files inside a Linux dotfile backup I'd forgotten about. The dry-run output was the only reason I caught it; one-line fix with `max_depth: 0`.

The Mail-attachments copy rule, on its first real run, created a duplicate loop — the JSONL log showed the same file being copied as `(1)`, `(2)`, `(3)` on consecutive scheduled runs. Fixed with the same-name-same-size check in `log_move`. The dry-run hadn't caught it because the duplicates only appeared *after* a real run created the first copy. Honest lesson: dry-runs catch the rules-that-should-not-fire problem; the JSONL log is what made the state-after-the-rule-fires problem visible.

## Where it sits now

The pipeline runs hourly via a Windows Task Scheduler job that invokes `scripts\run_organize.ps1`. Every run appends to `logs\organize-runs.log` and, for any actual moves, `logs\moves.jsonl`. Restic backs the lot up nightly.

## The principle

Most file-automation tools fail one basic test: they assume the user trusts them. They shouldn't. Filesystem automation has the same risk profile as a database migration — silent corruption is more dangerous than a loud failure, the consequences are durable, and "undo" is rarely free. The right default is the opposite of what most tools ship with: every action reversible, every action audited, every rule dry-runnable.

The reason this project works for me isn't the YAML rules. It's that there is no path through the system that touches my filesystem without leaving a JSONL receipt and without having first been shown to me in simulation. That's the test I'd want any future automation I build to pass.

*— Luke Simmons, Auckland*
