## Hi, I'm Luke 👋

Early-career **software & AI engineer** in Auckland, New Zealand — an
"AI-leveraged operator": I ship working software fast by pairing first-principles
thinking with modern AI tooling. SAE-trained **audio engineer** too — audio × AI
is my niche. Heading toward **AI / Forward-Deployed / Solutions Engineering**.

🌐 [lukesimmonsnz.kiwi](https://lukesimmonsnz.kiwi)  ·  💼 [LinkedIn](https://www.linkedin.com/in/lukesimmonsnz)

### Things I've built
- 🧭 **[job-scout](https://github.com/lukesimmonsnz/job-scout)** — local-first job aggregator with on-device LLM scoring (Flask · Ollama · SQLite): 10 source adapters, AI ranking with tunable weights, outreach CRM.
- ⚡ **[server-dashboard](https://github.com/lukesimmonsnz/server-dashboard)** — auto-discovering launcher for local projects: live status + one-click start/stop.
- 🎬 **[streamfinder-nz](https://github.com/lukesimmonsnz/streamfinder-nz)** — where-to-watch aggregator for NZ streaming (FastAPI · TMDB).
- 🦀 **[rust-wasm-playground](https://github.com/lukesimmonsnz/rust-wasm-playground)** — interactive Rust → WebAssembly learning playground.
- 🎙️ **[voice-cloning-pipeline](https://github.com/lukesimmonsnz/voice-cloning-pipeline)** — on-device voice-cloning narration (Chatterbox-Turbo · FFmpeg).

### Toolkit
`Python` · `Rust` · `JavaScript / TypeScript` · `SQL` · Flask · FastAPI · SQLite · local LLMs (Ollama) · Linux · Git

<sub>Open to early-career engineering roles — Auckland or remote (NZ / APAC / worldwide).</sub>

---

<sub>↓ The rest of this README documents the personal-site app this repository serves.</sub>

# Luke Simmons — personal site

<!-- auto:meta:begin -->
**Updated:** 2026-06-03
**Blog posts:** 17 · **Auckland entities:** 69 · **Auckland generated pages:** 61
<!-- auto:meta:end -->

An engineering README for the Flask app that serves [lukesimmonsnz.kiwi](https://lukesimmonsnz.kiwi/) from the owner's own machine.

Companion documents in [`docs/`](docs/):

- [`docs/SITEMAP.md`](docs/SITEMAP.md) — every URL, every content source, every count. Auto-regenerated.
- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — the design, the trade-offs, and the Auckland content-as-data subsystem.

If you just want to read this repo and understand it, start with `docs/ARCHITECTURE.md`. If you want to clone, run, and edit, keep reading here.

---

## What this is

A self-contained personal site, **architecturally portable to self-hosting**: one Flask process, one hand-written stylesheet, no JavaScript framework, no site-owned analytics, no third-party scripts outside Google Fonts. Content is authored locally in Markdown or Python data modules. One subsystem (the Auckland research project) is generated from a typed entity graph.

**Hosting, as of 2026-04-23:** fronted by Cloudflare as a transitional measure until dedicated self-hosting hardware is in place. Cloudflare terminates TLS at the edge, sets its own bot-management cookie, and retains its own request logs under its privacy policy. The Flask origin (currently the owner's machine via Cloudflare Tunnel) still owns all application state — `data/messages.jsonl`, `server.log`, `content/**`, the Auckland entity graph. When the hardware move happens, only the ingress changes; the app does not.

**AI drafting disclosure.** Two channels, both disclosed on the `/sitemap/` page:

- The daily blog agent ([`agent/daily_post.py`](agent/daily_post.py)) uses **local Ollama** (`qwen2.5:14b`).
- Longer-form prose — research pages, documentation such as this file, ARCHITECTURE.md — is drafted with **Claude AI via Anthropic's hosted API** and then edited before publication.

---

## Stack

- **Runtime:** Python 3.11+, [Flask 3](https://flask.palletsprojects.com/) with a small app factory.
- **Templating:** Jinja2, one `base.html` everything inherits from.
- **Content formats:** Markdown (`Markdown` + `python-frontmatter`) for blog & Auckland pages; Python data modules for the projects list and David Simmons biography; YAML + JSON Schema for the Auckland entity graph.
- **Validation:** `jsonschema` (Draft 2020-12) for the Auckland knowledge base.
- **Styling:** one hand-written CSS file, no framework. Two fonts from Google Fonts (Fraunces, Inter) loaded via `<link>`.
- **JavaScript:** a 20-line snippet in `base.html` that adds `§` anchors to prose headings. No other JS.
- **Local agents:** two cooperating agents at [`agent/`](agent/), both running on local [Ollama](https://ollama.com/) (default `qwen2.5:14b`). A **daily** agent writes private working notes to `agent/daily_drafts/` (not served). A **weekly** agent runs on Sundays, synthesises the week's notes plus weekly-trending HN + arXiv, and writes one public blog post.

See [`requirements.txt`](requirements.txt) for exact versions.

---

## Directory layout

```
Current website/
├── README.md                 # You are here
├── app.py                    # Flask factory, blueprint registration, error handlers
├── requirements.txt          # Python deps
├── start.bat / stop.bat      # Run/stop the hidden Flask process on Windows
├── .flaskenv                 # FLASK_APP=app.py, FLASK_DEBUG=1 (auto-loaded by python-dotenv)
├── .server.pid               # Written by start.bat; read by stop.bat
├── server.log / server.err   # Captured stdout/stderr from the hidden Flask
│
├── blueprints/               # One file per URL section
│   ├── main.py               # home, projects, now, contact, sitemap.xml, robots.txt
│   ├── blog.py               # Markdown + YAML frontmatter reader
│   ├── research.py           # One route per hand-written research page
│   ├── davidsimmons.py       # Biography, driven by data/david_simmons.py
│   └── auckland.py           # Reads generated Markdown from content/auckland/pages/
│
├── templates/
│   ├── base.html             # Site shell, OG tags, anchor-link JS, nav + footer
│   ├── 404.html / 500.html
│   ├── _partials/            # nav, footer, breadcrumbs macro, pagination macro
│   ├── main/                 # home / projects / now / contact / sitemap.xml
│   ├── blog/                 # index, post, feed.xml
│   ├── research/             # _layout.html + per-branch subtrees
│   ├── davidsimmons/         # biography section
│   └── auckland/             # index / section / page
│
├── static/
│   ├── css/main.css          # the single stylesheet
│   └── img/                  # cover + biography + placeholder imagery
│
├── data/                     # Python data consumed by blueprints
│   ├── projects.py           # PROJECTS list shown on /projects/
│   ├── david_simmons.py      # Structured biographical data
│   └── messages.jsonl        # Contact-form submissions (gitignored, auto-created)
│
├── content/
│   ├── blog/                 # YYYY-MM-DD-<slug>.md — Markdown + YAML frontmatter
│   └── auckland/             # Content-as-data subsystem (see docs/ARCHITECTURE.md §3)
│       ├── schema/           # JSON Schemas for each entity type
│       ├── data/             # One YAML file per entity, grouped by type
│       ├── templates/        # subpage.md.j2
│       ├── tools/            # graph.py / lint.py / render.py
│       ├── pages/            # Generated Markdown (do not hand-edit)
│       └── README.md         # Knowledge base conventions and workflow
│
├── agent/                    # Daily + weekly digest agents, plus docs regenerator
│   ├── daily_post.py         # Fetches HN + arXiv → Ollama → agent/daily_drafts/ (private)
│   ├── weekly_post.py        # Sundays: reads drafts + weekly HN/arXiv → content/blog/
│   ├── regen_docs.py         # Regenerates SITEMAP.md and refreshes auto blocks
│   ├── run_daily.bat         # Task-Scheduler entry point for the daily agent
│   ├── run_weekly.bat        # Task-Scheduler entry point for the weekly agent
│   ├── prompts/              # daily_post.md + weekly_post.md (voice, constraints, JSON schema)
│   ├── daily_drafts/         # Gitignored; accumulated daily notes for the weekly agent
│   └── logs/                 # daily.log, weekly.log — rotated on each run
│
└── docs/
    ├── SITEMAP.md            # Auto-generated
    ├── ARCHITECTURE.md
    └── BRIEFING-site-documentation.md   # Brief used to produce the docs
```

---

## Run it locally

### Windows

From the project root (`D:\ai-website-manager\Current website\`):

```
start.bat
```

What this does:

1. If `.server.pid` exists and that PID is still running, a dialog says so and exits.
2. If `.venv/` does not exist, creates it and `pip install -r requirements.txt`.
3. Starts `flask run --no-reload` hidden via PowerShell, redirecting stdout to `server.log` and stderr to `server.err`.
4. Writes the new process PID to `.server.pid`.

To stop:

```
stop.bat
```

which `taskkill`s the PID from `.server.pid`, then falls back to killing whatever is bound to port 5000.

Open <http://127.0.0.1:5000/>.

### Any other platform

The `.bat` files are Windows-specific. The equivalent shell workflow is:

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
flask run --no-reload
```

`.flaskenv` sets `FLASK_APP=app.py` and `FLASK_DEBUG=1`; `python-dotenv` picks it up automatically.

### The `--no-reload` posture

The site runs without Flask's auto-reloader. That means:

- **Python changes** (any `.py` in `blueprints/`, `data/`, `app.py`) require `stop.bat` then `start.bat`.
- **Template and content changes** (`templates/`, `content/blog/*.md`, `content/auckland/pages/*.md`) are picked up on the next request. No restart needed.
- **CSS changes** are picked up on the next request.

Why `--no-reload`? A single PID is clean to stop, and the reloader's fork-on-change interacts badly with the hidden-window launcher on Windows.

---

## How to develop

### Add a blog post by hand

Create a file in [`content/blog/`](content/blog/) named `YYYY-MM-DD-<slug>.md`. Frontmatter keys (see [`blueprints/blog.py`](blueprints/blog.py) docstring):

```yaml
---
title: "Post title"
date: 2026-04-23
author: luke          # or "agent" — styles differently in templates
summary: "One-line lede shown in the list view."
tags: [flask, local-first]
---

Markdown body goes here. Supports the `extra`, `codehilite`, `sane_lists`, and
`smarty` extensions.
```

It will appear at `/blog/<filename-stem>/` on the next request. No restart.

### Add a project to `/projects/`

Append a dict to `PROJECTS` in [`data/projects.py`](data/projects.py). Fields are documented in that file's docstring. Restart required.

### Add a research page to Computer Science / Climate / Medical Science

These three branches are **hand-written**, not generated. One route per page, one template per route.

1. Add the route in [`blueprints/research.py`](blueprints/research.py).
2. Add the template under `templates/research/<branch>/`.
3. Add the page to the secondary subnav in [`templates/research/_layout.html`](templates/research/_layout.html).
4. Import the shared pagination macro: `{% from "_partials/pagination.html" import pagination_pair %}` and use `{{ pagination_pair(prev=..., next=...) }}` at the bottom of the page body.
5. Restart.

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for why this is hand-written rather than generated.

### Add content to the Auckland research project

The Auckland subsystem is content-as-data. Do not hand-edit the generated Markdown under `content/auckland/pages/`. Workflow:

1. Author entities as YAML under `content/auckland/data/<type>/<slug>.yaml`.
2. `cd content/auckland && python tools/lint.py` — must exit 0 before anything renders.
3. `python tools/render.py <problem.id>` or `python tools/render.py --all` to write Markdown into `content/auckland/pages/`.
4. The Flask app picks up the new page on the next request.

Full details of entity types, schemas, and invariants live in [`content/auckland/README.md`](content/auckland/README.md) and [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md).

### Re-run the docs

```
.venv\Scripts\python -m agent.regen_docs
```

Regenerates [`docs/SITEMAP.md`](docs/SITEMAP.md) in full and refreshes the `<!-- auto:* -->` blocks in this file and in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md). The daily agent runs it automatically after writing a post.

### Run the daily blog-post agent

```
agent\run_daily.bat
```

Or interactively from an activated venv:

```
python -m agent.daily_post --dry-run     # show the prompt; do not call Ollama
python -m agent.daily_post                # real run; writes one post
python -m agent.daily_post --force        # overwrite today's post
```

Requires Ollama running locally at `http://localhost:11434` with the configured model pulled. See [`agent/README.md`](agent/README.md) for Task Scheduler setup.

---

## Conventions

These are project rules — not stylistic preferences, not negotiable for automated changes:

1. **No email addresses in any public HTML.** The contact page uses a form that writes to `data/messages.jsonl` at the origin. No `mailto:` links anywhere. No plaintext email in templates, biographies, references, or the sitemap.
2. **No JavaScript frameworks.** The only JS on the site is the 20-line anchor-link snippet in [`templates/base.html`](templates/base.html). Do not add build tooling (Webpack, Vite, Rollup, bundlers of any kind).
3. **No site-owned analytics or third-party scripts.** The site does not add its own tracking. (Cloudflare's own logging operates on the ingress and is disclosed on `/sitemap/`.)
4. **Cloudflare now, self-hosting later.** The app is not deployed to PaaS (GitHub Pages / Netlify / Vercel). It runs on a Flask origin fronted by Cloudflare, with the origin eventually moving to the owner's dedicated hardware.
5. **Restart after Python changes.** `--no-reload` is deliberate; get into the habit of `stop.bat && start.bat` after editing a blueprint. **Verify the listener actually died** — `stop.bat` sometimes kills only the `flask.exe` launcher, not the Python process holding port 5000.
6. **Do not hand-edit generated files.** `content/auckland/pages/**/*.md` is produced by [`content/auckland/tools/render.py`](content/auckland/tools/render.py). `docs/SITEMAP.md` is produced by [`agent/regen_docs.py`](agent/regen_docs.py). Blocks marked `<!-- auto:* -->` in the other docs are rewritten by the regenerator — edit the surrounding prose, not the blocks.
7. **Private material stays out of public content.** The [`content/auckland/briefings/`](content/auckland/briefings/) directory and anything marked private in memory are decision-support artefacts. They are not served and must not leak into public pages.

---

## Deployment

Currently: **Flask origin fronted by Cloudflare** (Tunnel or equivalent), as a transitional setup until dedicated self-hosting hardware is in place. `SITE_URL` should be set in the environment to the production URL so OG tags, canonical URLs, and the XML sitemap emit real URLs instead of `http://127.0.0.1:5000` (see [`app.py`](app.py)). The `.flaskenv` file is only for the local dev defaults; production `SITE_URL` belongs in the process environment, not in the repo.

Known gaps that exist once the site is internet-facing:

- `flask run` is used as the runner and works behind Cloudflare Tunnel, but a proper WSGI server (gunicorn / waitress) is the right move on dedicated hardware.
- The contact form writes plaintext to `data/messages.jsonl` with no rate limit, no captcha, and no spam defence. Cloudflare's default bot protections catch some of this, but an application-level guard is the correct fix.
- **Email forwarding for the contact form.** When the site goes live, submissions should also be emailed to `luke@lukesimmonsnz.kiwi` (which forwards to Gmail). This means adding outbound SMTP to [`blueprints/main.py`](blueprints/main.py), picking a transactional-mail provider or self-sent via the domain's MX, and handling the credential via environment variables — not in the repo. The email address itself must **never** be rendered anywhere in the site's public HTML (see the first convention above); use it only as a backend destination.
- No secret rotation story yet. Once there is one secret (SMTP credential), add a documented rotation path.

---

## Testing

There is **no automated test suite at present.** The closest thing to CI is [`content/auckland/tools/lint.py`](content/auckland/tools/lint.py), which validates the Auckland entity graph against its JSON Schemas and checks graph invariants. It exits non-zero on any failure and is the gate for rendering.

Ad-hoc verification:

- `.venv\Scripts\python -c "from app import app; print(app.url_map)"` — enumerate routes.
- `python content/auckland/tools/graph.py` — dump graph summary + validation errors.
- `python -m agent.daily_post --dry-run` — exercise the agent without calling Ollama.

---

## Copyright and license

© Luke Simmons. **All rights reserved.**

There is no open-source license file in this repository. The site's source code, prose, biographical material, and the Auckland research content are all under default copyright — no permission to copy, redistribute, modify, or republish is granted. The footer on every page of the rendered site carries the same notice.

If you would like to reuse any part of this work (code or content), ask first. Quotation for the purposes of commentary, criticism, or research is usually fine under the ordinary fair-dealing rules of New Zealand copyright law, but that is a reader judgement, not a license.
