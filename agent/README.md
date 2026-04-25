# agent/

Two cooperating agents, both running on local Ollama:

| Agent | Runs | Output goes to | Public? |
|---|---|---|---|
| **`daily_post.py`** | Every day | `agent/daily_drafts/YYYY-MM-DD-<slug>.md` | No — private working notes |
| **`weekly_post.py`** | Sundays | `content/blog/YYYY-MM-DD-weekly-digest.md` | **Yes** — one post a week |

`regen_docs.py` is a third, deterministic (non-LLM) script that regenerates `docs/SITEMAP.md` and refreshes the `<!-- auto:* -->` blocks in `README.md` and `docs/ARCHITECTURE.md` after each run of either agent.

## Pipeline

```
        Hacker News RSS          arXiv cs.AI (last 3 days)
               \                         /
                \                       /
                 v                     v
               daily_post.py  ─>  agent/daily_drafts/YYYY-MM-DD-<slug>.md
                                        |
                                        |  (accumulates 7 drafts over the week)
                                        v
               weekly HN (Algolia, last 7 days)
               weekly arXiv cs.AI (last 7 days)
                                        |
                                        v
                                 weekly_post.py
                                        |
                                        v
                              content/blog/YYYY-MM-DD-weekly-digest.md
                                        |
                                        v
                                 regen_docs.py (counts, sitemap)
```

Two stages so that the smaller local model (qwen2.5:14b) is only ever asked to do tasks within its strengths: the daily agent does short, tight digests over a narrow input (2 sources); the weekly agent synthesises across a pre-distilled week plus a weekly-trending feed.

## `daily_post.py`

### What it does

1. Fetches the current top ~20 Hacker News stories (RSS) and the 6 most recent arXiv `cs.AI` papers (Atom feed).
2. Hands them plus a voice prompt to local Ollama (default `qwen2.5:14b`, override via `OLLAMA_MODEL` env or `--model`).
3. Parses the JSON response and writes to `agent/daily_drafts/YYYY-MM-DD-<slug>.md`.
4. **Does not publish.** The draft is gitignored and not served by Flask. It is working material for the weekly agent (and for you to skim if you want).

### Running

```powershell
# from the site root
.\.venv\Scripts\python -m agent.daily_post --dry-run     # fetch + show prompt, no Ollama call
.\.venv\Scripts\python -m agent.daily_post              # real run
.\.venv\Scripts\python -m agent.daily_post --force      # overwrite today's draft
.\.venv\Scripts\python -m agent.daily_post --model qwen2.5:7b
```

Or double-click / invoke `agent\run_daily.bat` — same thing, wraps venv activation and also runs `regen_docs.py` afterwards.

Idempotent: if a draft already exists for today, it exits 0 without touching anything (unless `--force`).

## `weekly_post.py`

### What it does

1. Reads up to 7 daily drafts from `agent/daily_drafts/` dated within the past week.
2. Fetches this week's top Hacker News stories via the [Algolia HN search API](https://hn.algolia.com/api) (front-page, last 7 days, ranked by points, up to 25 items).
3. Fetches this week's cs.AI arXiv papers (last 7 days, up to 25 items).
4. Hands all three streams to local Ollama with a prompt that demands themed synthesis (2–3 threads across the week) and inline citations on every concrete reference.
5. Writes `content/blog/YYYY-MM-DD-weekly-digest.md` — **this file is public** and served by the blog blueprint.

The target length is 700–900 words, which sits comfortably inside qwen2.5:14b's reliable range and keeps output-drift and hallucination-by-length within acceptable bounds.

### Running

```powershell
.\.venv\Scripts\python -m agent.weekly_post --dry-run    # show inputs + prompt, no Ollama call
.\.venv\Scripts\python -m agent.weekly_post             # real run
.\.venv\Scripts\python -m agent.weekly_post --force     # overwrite this week's post
.\.venv\Scripts\python -m agent.weekly_post --date 2026-04-26   # override post date
```

Or invoke `agent\run_weekly.bat` for the Task-Scheduler-ready wrapper.

Idempotent: if a weekly post for this Sunday already exists in `content/blog/`, it exits 0 without overwriting (unless `--force`).

### Why it doesn't trust the daily drafts' citations

The daily agent runs a 14B model on short inputs and occasionally hallucinates an author or a URL. The weekly prompt is explicit about this: daily digests are a guide to *what was interesting each day*, but all URLs and paper metadata must be cross-checked against the authoritative weekly HN and arXiv lists before citing. If a daily mentions something that isn't in the weekly authoritative lists, the weekly agent is instructed to drop the citation rather than propagate it.

## Ollama setup (one-time)

Both agents assume Ollama is running on `localhost:11434`. Native install is the simple path:

1. Download from <https://ollama.com/download>, install.
2. `ollama pull qwen2.5:14b` — pulls ~9 GB of weights; happens once.
3. Ollama runs as a background service. Confirm with `curl http://localhost:11434/api/tags`.

If Ollama isn't reachable, the agents exit with code 2 and log the failure. The site keeps working.

## Scheduling (Windows Task Scheduler)

Two tasks. From an **elevated** PowerShell or cmd:

```powershell
# Daily: every day at 07:00 NZT. Writes today's private draft.
schtasks /Create ^
    /TN "Luke blog agent — daily" ^
    /SC DAILY ^
    /ST 07:00 ^
    /TR "\"D:\ai-website-manager\Current website\agent\run_daily.bat\"" ^
    /F

# Weekly: Sundays at 08:00 NZT — one hour after the daily run, so the
# weekly agent has this Sunday's draft available.
schtasks /Create ^
    /TN "Luke blog agent — weekly" ^
    /SC WEEKLY ^
    /D SUN ^
    /ST 08:00 ^
    /TR "\"D:\ai-website-manager\Current website\agent\run_weekly.bat\"" ^
    /F
```

Check with `schtasks /Query /TN "Luke blog agent — daily"`; delete with `/Delete /F`.

If you prefer "run as soon as possible after scheduled start is missed," that's a checkbox in the GUI task settings.

## Prompt templates

Both live as version-controlled Markdown:

- `agent/prompts/daily_post.md`
- `agent/prompts/weekly_post.md`

Each splits into a `## System` and `## User` section. The loader substitutes `{{today}}`, `{{hn_list}}`, `{{arxiv_list}}`, and (weekly only) `{{daily_digests}}` at runtime.

Edit them freely. If a post reads off, tune the prompt rather than the code.

## Logs

- `agent/logs/daily.log` — appended per run, rotated to the last 1000 lines at startup.
- `agent/logs/weekly.log` — same shape, separate file.

Both are gitignored.

## AI-assistance disclosure

Both agents run **local Ollama only** for generation. No prompt or output transits a hosted LLM from these scripts. The broader site also uses hosted Claude AI for longer-form prose drafts (research pages, documentation) — that is a separate workflow, disclosed on the live [/sitemap/](/sitemap/) page, and does not involve the agents in this directory.
