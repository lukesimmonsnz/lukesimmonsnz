# Changelog

An administrative log of notable changes to the site, the agents, and the surrounding
tooling. Entries are appended in reverse-chronological order (newest first). One
bullet per change, grouped under the date the change landed.

This is a human-edited file. It is **not** auto-generated — the docs regenerator
([`agent/regen_docs.py`](../agent/regen_docs.py)) deliberately leaves it alone.
Agents (and Claude-Code sessions) that make non-trivial changes should add an
entry here before ending the session.

Conventions:

- **Date** format `YYYY-MM-DD`. Use the actual calendar date the change landed,
  not a release version. There are no releases.
- **Scope tag** in square brackets at the start of each bullet: `[site]`,
  `[agent]`, `[docs]`, `[ops]`, `[content]`, `[infra]`, `[memory]`.
- **Link** to the touched file(s) when it helps a future reader jump to the change.
- Keep each bullet to one sentence. If it needs more, it probably wants a short
  follow-up paragraph underneath.

---

## 2026-05-30

- `[content]` **Nine project-writeup posts shipped to `/blog/`.** Portfolio launch series under `2026-05-21` through `2026-05-28`: the minikv-retirement Rust-learning-style realisation, streamfinder, political research, file organiser, personal finance dashboard, smart-home design, voice clone, Job Scout post-mortem, and the 7B-LLM internals companion. Each post carries an explicit AI-authorship disclosure paragraph at the top — "drafted by Claude (Anthropic) from my project notes and source code, then reviewed and edited by me before publishing" — mirroring the voice-clone consequentialist-disclosure principle (disclose when the listener/reader would otherwise reasonably assume human authorship). ~9,800 words across the set after a 25%-trim pass on first-draft lengths. Files: [`content/blog/2026-05-21-the-rust-project-i-retired-and-why.md`](../content/blog/2026-05-21-the-rust-project-i-retired-and-why.md) through [`content/blog/2026-05-28-how-the-7b-llm-processes-information.md`](../content/blog/2026-05-28-how-the-7b-llm-processes-information.md). Committed as `f9f920a`.
- `[content]` **Smart-home post reframed from "shipped" to "design log".** Drafted as if the home automation were deployed — "tested by unplugging the WAN cable", "Two sensors refused to join until I factory-reset them" — but the install isn't actually live yet (no rooms covered, no dongle chosen, no hardware paired). Rewrote as honest design doc: Y-then-X principle framing preserved, fabricated What-Broke anecdotes removed, new "Where this sits today: design locked, staging VM only, no production hardware on the network yet" section added. YouTube narration script updated in lockstep — "six projects **from** this year" (not "shipped this year"), "smart-home **design**" (not "smart-home controller").
- `[content]` **Personal finance dashboard post rewritten for privacy.** First-draft contained named third-party financial details inappropriate for publication. Rewrote as generic "A personal finance dashboard built around Akahu" with all private references stripped; technical substance (Akahu OAuth dance, the 8-second `setTimeout` confession, partial-unique-index dedup between Excel imports and live Akahu feeds, Node-vs-Python stack honesty, one-user-tool discipline) intact. Word count 1,500 → 970.
- `[infra]` **Recovered 671 Northland datacamp files from Unicode-path-encoded filename corruption.** 1,184 files in the repo root had filenames like `D⟨U+F03A⟩⟨U+F05C⟩ai-website-manager⟨U+F05C⟩Current website⟨U+F05C⟩content⟨U+F05C⟩northland⟨U+F05C⟩data⟨U+F05C⟩camp/climate.camp_1.yaml` — some tool wrote the full path string as the filename, substituting U+F03A and U+F05C (Unicode Private Use codepoints) for `:` and `\\` because Windows can't have those in filenames. Wrote a one-shot Python rename script that decodes the codepoints, strips the `D:/ai-website-manager/Current website/` prefix, and moves each file to its intended project-relative path *only* when the target doesn't already exist (so content-conflict cases are left for manual triage). 671 of 1,184 moved cleanly into `content/northland/`; **513 remain in root** with target collisions to triage individually. The corrupt files held unique content, not duplicates — bulk-deleting would have lost the Northland corpus.
- `[ops]` **Cloudflare Pages deploy** via [`scripts/deploy.py`](../scripts/deploy.py). Carried the nine-post blog launch, the smart-home rewrite, the finance-dashboard privacy rewrite, the requirements pin, and the 671 relocated Northland files. **985 URLs frozen, 0 failed; 1,054 files uploaded (1,037 cached, 17 new) in 2.75 sec of wrangler push.** Preview at `https://435bba93.lukesimmonsnz.pages.dev`; production verified live (all four sampled `/blog/2026-05-2[1-8]-...` URLs returned HTTP 200, AI-authorship disclosure rendered, smart-home post's old "tested by unplugging the WAN cable" claim absent, new "design is locked" framing present).
- `[ops]` **`requirements.txt` pinned from venv.** Was 10 packages with mostly `>=` minimums (1 pinned, 9 unpinned); rewrote as exact versions read from the current `.venv` (e.g. `Flask==3.1.3`, `python-dotenv==1.2.2`, `Pillow==12.2.0`, `Markdown==3.10.2`). Stops silent breakage when re-installing from scratch. Same pass applied to the sibling streamfinder-nz project's requirements file (6 packages, 0 pinned → all pinned).
- `[ops]` **Repo-root debris removed.** Deleted `_perm_test.tmp`, `_probe_v3.py`, `pytest-cache-files-whd74yte/`, and 14 unreferenced HTMLs in `_gui_preview/` (kept `settings.html` + `theme.html` — those have live `grep`-detected references).
- `[ops]` **Stale `.git/index.lock` removed.** Dated 2026-05-02 — four weeks old, blocking `git add`/`commit`. Plausibly explains other git-tooling weirdness over the past month.
- `[memory]` **Local Claude-session memory indexes updated** across several project workspaces — recording the AI-authorship disclosure pattern, the privacy posture for finance-related content, and the streamfinder Phase 3+6 completion.
- `[ops]` **Deploy dashboard.** Two new files under [`scripts/`](../scripts/): (1) [`deploy.py`](../scripts/deploy.py) extended to tee subprocess output, parse `freeze.py` URL counts + `wrangler` upload counts + preview URL via regex, capture git SHA / branch / dirty-flag, and append one JSONL row to [`logs/deploys.jsonl`](../logs/deploys.jsonl) per run (success or failure). (2) [`scripts/deploys.py`](../scripts/deploys.py) is a stdlib-only CLI viewer that reads the JSONL and prints a plain-text table newest-first, marking the most recent successful deploy with `<- live` and dirty-tree deploys with `*` next to the git SHA. Flags: `--limit N`, `--full` (adds preview-URL column), `--json` (raw passthrough for piping). Stdlib only — no Rich, no Flask, no Werkzeug — runs in any terminal including unmodified Windows `cp1252` (ASCII output only). Tonight's deploy seeded as the first row. Future-extension hooks noted in module docstrings: merge `wrangler pages deployment list` cloud-side history; add an HTML view at `/admin/deploys/` reusing the same JSONL.
- `[infra]` **`/admin/yaml/` typed-entity editor shelved.** [`docs/DASHBOARD-SPEC.md`](DASHBOARD-SPEC.md) was ratified 2026-05-02 and partially implemented at `blueprints/admin/{blueprint,save_pipeline,schema_walker,edges}.py` (registered as `admin_bp` at `/admin/yaml`), but the build never reached a usable state — a previous Claude session couldn't repair it, and the work was abandoned. PI call 2026-05-30: shelve rather than keep dragging it. Four implementation files moved to [`archive/admin-yaml/`](../archive/admin-yaml/); `blueprints/admin/__init__.py` rewritten to be a docstring-only namespace marker (so the `blueprints.admin.cms.*` import paths still resolve); [`app.py`](../app.py) loses the `from blueprints.admin import admin_bp` import and the `register_blueprint(admin_bp, url_prefix="/admin/yaml")` call. CMS at `blueprints/admin/cms/*` is a different surface and stays live — `/admin/diff/`, `/admin/edit/`, `/admin/history/`, `/admin/media/`, `/admin/preview/`, `/admin/search/`, `/admin/settings/`, `/admin/theme/` and the `/admin/api/*` routes all verified intact post-shelve via `app.url_map`. DASHBOARD-SPEC.md gets a top-of-file SHELVED header so the spec can't be re-implemented against without an explicit PI reopen.

---

## 2026-05-06

- `[content]` **AI / automation / migration / ageing added to the typed graph.** Four new NZ patterns: `economy.ai_automation_labour_exposure` (10 regions), `economy.ai_productivity_capture_asymmetry` (7 regions), `economy.ageing_workforce_shortage` (10 regions), `inequality.rural_population_decline` (8 regions). Backed by 4 new sources (Stats NZ population projections 2024, Productivity Commission frontier-firms 2021, Te Whatu Ora workforce plan 2024, OECD Nedelkoska-Quintini 2018) and 10 new claims under `content/auckland/data/claim/` (covering automation exposure share, AI diffusion lag, frontier-firm productivity gap, median age trajectory, dependency ratio, regional aged-share divergence, rural population decline, youth outflow, AI capture distributional risk, health workforce retirement). Wired into 5 existing Auckland problems (`labour_market`, `fiscal_sustainability`, `productivity`, `income_polarisation`, `economic_disadvantage`). Auckland: 452 entities, 0 errors. NZ corpus now 37 patterns across 11 themes (was 33).
- `[site]` **New analytical Solutions essay at `/research/nz/solutions/`.** [`blueprints/nz.py`](../blueprints/nz.py) gains a `solutions` route that loads the pattern index for cross-linking. New template [`templates/nz/solutions.html`](../templates/nz/solutions.html) is a hand-authored cross-pattern essay organised by intervention mechanism rather than by theme: infrastructure-led unlock, land-use reform, risk-based pricing, polycentric urban form, Treaty-based co-governance, economic diversification, the AI/migration/ageing synthesis lever, and what the corpus does not solve. Linked from `/research/nz/` intro paragraph. 23 KB rendered. Smoke: 10/10 affected routes HTTP 200.
- `[content]` **Citations converted to APA 7th edition author-date style.** [`content/auckland/templates/section.md.j2`](../content/auckland/templates/section.md.j2) now renders in-text clusters as `(Stats NZ, 2024; OECD, 2018)` instead of bracketed numbers `[1] [2]`. References list switches from numbered ordered list to APA-formatted unordered list: `Author. (Year). *Title*. Publisher. URL`. APA helpers (`_apa_short`, `_apa_full`, `_resolve_author`, `_derive_org_from_source_id`) added to both [`content/auckland/tools/render.py`](../content/auckland/tools/render.py) and [`scripts/generate_section_essays.py`](../scripts/generate_section_essays.py); kept in sync by hand. Acronym table (NZIER, MBIE, OECD, NZTA, LSF, etc.) preserves uppercase in derived org names from source IDs. Multi-author handling: 1 author → "Surname"; 2 authors → "A & B"; 3+ → "A et al.". Re-rendered Auckland's 11 sections + 15 other regions' 11 sections (165 essays). Live smoke: `/research/auckland/economy/` shows `(Nedelkoska & Quintini, 2018; NZIER Productivity, 2023; Stats NZ Labour Market, 2023; Te Whatu Ora, 2024)` in text; references list APA-formatted with hyperlinked URLs.
- `[ops]` **Server restart for nz.solutions endpoint.** Live `bin/start.bat`-launched Flask was running pre-edit code; `url_for('nz.solutions')` referenced from updated [`templates/nz/index.html`](../templates/nz/index.html) raised `BuildError` and 500'd `/research/nz/`. Stopped via PID file, restarted with `bin/start.bat`. Curl confirms 200 on both `/research/nz/` and `/research/nz/solutions/`.
- `[site]` **Solutions essay relocated and rewritten for pragmatism.** Cards for "Aotearoa national patterns" and "Solution space" moved out of the regional card-grid on [`templates/research/index.html`](../templates/research/index.html) into a new "National synthesis" subsection at the bottom of the Aotearoa tab (h3 + own card-grid + intro prose + visible top border). New `.cross-regional-synthesis` CSS rule in [`static/css/main.css`](../static/css/main.css). Solution space CTA on [`templates/nz/index.html`](../templates/nz/index.html) promoted from muted footnote to a `.page-cta` callout with copper-accent left border. Solutions essay [`templates/nz/solutions.html`](../templates/nz/solutions.html) substantially rewritten: Treaty-based co-governance section removed entirely (8 → 7 sections; meta description, card description, and AI/migration paragraph also scrubbed of Treaty references). Remaining six sections rewritten for pragmatism — each now names specific NZ statutes (IFF Act 2020, Climate Adaptation Bill, RMA), agencies (Toka Tū Ake EQC, Callaghan Innovation, Te Whatu Ora, NZTE), programmes (R&D Tax Incentive, Skilled Migrant Category regional bonus, Income Insurance Scheme, Just Transitions Partnership), and dollar/scale figures ($30k–80k trunk infrastructure per dwelling; ~$200–400M/km for light rail; ~1.4% combined Income Insurance levy). Added explicit "Trade-off" paragraph to each lever calling out who bears the cost. AI/migration/ageing synthesis converted from prose to a 4-item bulleted action list (SME AI diffusion, regional immigration loading, active labour-market policy, health workforce). Smoke: `/research/`, `/research/nz/`, `/research/nz/solutions/` all 200; zero remaining Treaty/co-governance mentions on the page.

---

## 2026-05-17

- `[content]` **Weekly digest 2026-05-17 published — section dropped for a citation defect.** Agent-drafted digest at [`content/blog/2026-05-17-weekly-digest.md`](../content/blog/2026-05-17-weekly-digest.md). The agent's draft section 1 ("Local-First Systems and Hardware Security") cited two distinct sources but pointed both at the *same* Twitter URL, and described an HN thread while linking to Twitter — an unrecoverable citation error. Per PI decision, section 1 was dropped entirely. Post retitled "Multimodal Generation and Robust Agent Engineering" (was "The Week in Local AI and Multimodal Generation"); rewritten to two themes — multimodal generation (AlphaGRPO, continual learning) and robust agent engineering (AI Workflow Store) — all three remaining citations are verified `arxiv.org/abs/2605.*` links. Stock "local-first / self-sovereignty" framing removed throughout (recurring agent-template artefact; site is Cloudflare-hosted). `status: draft` → `published`.
- `[ops]` **Cloudflare deploy.** 974 URLs frozen 0 failures; 183 files uploaded (861 cached) in 4.3 sec; preview `e3eb1fbb.lukesimmonsnz.pages.dev`. `deploy.py`'s `_resolve_wrangler()` fix (2026-05-10) worked unattended — resolved `wrangler.CMD` via `shutil.which`. Production smoke: blog index + new post both 200; post shows correct title, 0 Twitter links, 3 arXiv links.
- `[agent]` **Weekly/daily digest prompts corrected at the root cause.** The agent had produced the unwanted "local-first" framing for two weeks running, plus a duplicated citation URL — both traceable to the prompt templates. [`agent/prompts/weekly_post.md`](../agent/prompts/weekly_post.md) and [`agent/prompts/daily_post.md`](../agent/prompts/daily_post.md): (1) the Luke-bio line that read "interested in local-first systems … building things on his own hardware rather than in the cloud" rewritten to accurate framing (ML + software-engineering practice + Māori history; runs some models locally but the site is Cloudflare-hosted and he is pragmatic about cloud), plus an explicit instruction not to frame him as a "local-first / anti-cloud advocate" or make local-first a recurring lens; (2) citation rules hardened with a new bullet — *each distinct reference gets its own distinct URL, taken from the entry it belongs to; a repeated URL is always a bug; never borrow a URL from one list entry for another* — directly targeting the 2026-05-17 duplicate-Twitter-link defect. No embedded prompt strings in `weekly_post.py`/`daily_post.py`/`weekly_research.py`; the `.md` files are the single source of truth. Effect lands on the next weekly run; no deploy needed (agent-pipeline files, not site content).

---

## 2026-05-10

- `[ops]` **Cloudflare Pages deploy.** First deploy with the full multi-region corpus + new NZ pages. **974 URLs frozen, 0 failures, 976 files uploaded** (67 cached) in ~10 sec; preview at `e9231584.lukesimmonsnz.pages.dev`. Production smoke: 7/7 routes 200 (`/`, `/research/nz/`, `/research/nz/solutions/`, `/research/wellington/`, `/blog/2026-05-10-weekly-digest/`, `/sitemap/`, `/sitemap.xml`).
- `[ops]` **Freeze pipeline fix — was only deploying Auckland.** [`scripts/freeze.py`](../scripts/freeze.py) `_enumerate_dynamic_urls()` had a hard-coded `pages_dir = "auckland"` and only enumerated Auckland's section/leaf URLs. The other 15 regions (Wellington, Northland, Waikato, Bay of Plenty, Gisborne, Hawke's Bay, Taranaki, Manawatu-Whanganui, Nelson, Tasman, Marlborough, West Coast, Canterbury, Otago, Southland) plus all 11 NZ theme rollups were missing from every Cloudflare deploy since their corpora landed (2026-04-26 onward). Replaced with a tuple of all 16 region slugs and an enumeration that handles both consolidated (`pages/_sections/<theme>.md`) and legacy (`pages/<section>/*.md`) layouts. Underscore-prefixed dirs/stems skipped (so `_sections/` is not double-rendered as a URL). Added NZ pattern theme enumeration with `climate → climate-adaptation` URL alias for the route's enum check. **URL count went 138 → 974** (+836).
- `[ops]` **deploy.py wrangler invocation hardened for Windows.** Step 3 of [`scripts/deploy.py`](../scripts/deploy.py) called `subprocess.run(["wrangler", ...])`, which `FileNotFoundError`s on Windows because npm-installed CLIs are `.cmd` shims, not `.exe`s. New `_resolve_wrangler()` uses `shutil.which` (PATHEXT-aware) to find the shim, falling back to `wrangler.cmd` and finally the bare name.
- `[content]` **Weekly digest 2026-05-10 published.** Agent-drafted weekly digest at [`content/blog/2026-05-10-weekly-digest.md`](../content/blog/2026-05-10-weekly-digest.md): three threads — safety scaling laws in clinical LLMs (SaFE-Scale, BAMI/GUI grounding bias), explicit control flow for long-horizon agents (LongSeeker, "Agents need control flow not more prompts"), and AI's effect on vulnerability-disclosure norms (Jeff Kaufman). Promoted from `status: draft` → `status: published`. Rewrote the agent's stock "local-first / minimizing reliance on centralized cloud" framing — site is Cloudflare-hosted; per `feedback`/`project_hosting_and_ai_posture` memory the local-first claim is not accurate. Closer reframed around the unifying theme (rare-event behaviour vs average-case behaviour).

---

## 2026-05-05

- `[site]` **Nav simplification: dropped Projects, reordered personal-first.** Top nav is now Home · Blog · David Simmons · Research · Contact (+ search icon). Projects route, template ([`templates/main/projects.html`](../templates/main/projects.html)), data file ([`data/projects.py`](../data/projects.py)), and CMS slot ([`content/_pages/projects.md`](../content/_pages/projects.md)) all deleted. Replaced by a "What I'm building" prose section in [`content/_pages/home.md`](../content/_pages/home.md) covering the three active projects (this site, Aotearoa research, local AI agent). Updated downstream references: [`templates/_partials/nav.html`](../templates/_partials/nav.html), [`templates/_partials/footer.html`](../templates/_partials/footer.html), [`content/_theme/header.md`](../content/_theme/header.md), [`content/_theme/footer.md`](../content/_theme/footer.md), [`templates/rendered/_theme/header.html`](../templates/rendered/_theme/header.html), [`templates/rendered/_theme/footer.html`](../templates/rendered/_theme/footer.html), [`blueprints/main.py`](../blueprints/main.py) (route + import gone), [`blueprints/admin/cms/resolver.py`](../blueprints/admin/cms/resolver.py) (`_build_projects` + pattern gone), [`agent/regen_docs.py`](../agent/regen_docs.py) (`_projects_count` + MAIN_ROUTES entry gone). Smoke: 7/7 nav routes 200, `/projects/` correctly 404, no Projects mentions remain in rendered home page.
- `[site]` **Research index split into a two-tab layout.** [`templates/research/index.html`](../templates/research/index.html) now uses CSS-only radio-button tabs ("Aotearoa New Zealand" default-active; "Science notes" for CS/Climate/MedSci). New tab CSS appended to [`static/css/main.css`](../static/css/main.css) (~50 lines, uses existing `--accent`/`--rule` tokens, no JS). The "Two authorship regimes" footer section sits below both tabs, visible regardless.

---

## 2026-04-24

- `[infra]` **Pivoted deployment target from Cloudflare Tunnel to Cloudflare Pages.** Tunnel requires the origin machine to be on 24/7; Pages is static-file hosting on Cloudflare's edge, so the machine can be off and the site stays up. Built the full pipeline:
  - [`scripts/freeze.py`](../scripts/freeze.py) — walks `app.url_map`, hits every GET route via Flask's test client, writes `_site/<path>/index.html` for pretty URLs. Draft-status blog posts skipped. Idempotent; wipes `_site/` each run (with a Windows-permission retry handler).
  - [`functions/api/contact.js`](../functions/api/contact.js) — Cloudflare Pages Function replacing the Flask contact POST handler. Validates Cloudflare Turnstile, sanity-checks fields, sends email via [Resend](https://resend.com), redirects to `/contact/thanks/`.
  - [`scripts/deploy.bat`](../scripts/deploy.bat) — two-step freeze + `wrangler pages deploy`.
  - [`docs/CLOUDFLARE-DEPLOY.md`](CLOUDFLARE-DEPLOY.md) — full one-time setup walk-through (domain in Cloudflare DNS, Pages project, Turnstile widget, Resend sender verification, env vars, wrangler install) plus the day-to-day loop and rollback instructions.
  - The Live-website folder that I briefly built for a two-Flask-process staging model is deleted — Pages makes it obsolete.
- `[site]` Added Turnstile bot protection to the contact form and fixed the
  stale "runs locally, saves to messages.jsonl" paragraph underneath it. The
  form now:
  1. Shows a Cloudflare Turnstile challenge (when `TURNSTILE_SITE_KEY` env var is set at freeze time).
  2. POSTs to whichever URL `CONTACT_SUBMIT_URL` env var names — `/api/contact` for Pages, Flask's own endpoint for local dev.
  3. Inline JS on the contact page reads a `?error=<code>` query and shows a human-readable banner when the Pages Function rejects a submission.
  Plus a new `/contact/thanks/` route + template as the redirect target.
- `[infra]` **Site went live at `https://lukesimmonsnz.kiwi`** via Cloudflare Pages.
  First deploy via dashboard upload; subsequent deploys via `wrangler pages deploy`.
  All four Pages env vars set (Turnstile secret, Resend API key, `CONTACT_TO`,
  `CONTACT_FROM`). Contact form tested end-to-end: Turnstile challenge
  validated, Resend sent the email, delivery to Gmail confirmed.
- `[infra]` **Bug caught and fixed during first deploy**: running
  `freeze.py` from git-bash mangled `CONTACT_SUBMIT_URL=/api/contact` into
  `C:/Program Files/Git/api/contact` via MSYS path translation. Added a
  sanity check in [`freeze.py`](../scripts/freeze.py) that refuses to build
  when the submit URL doesn't look like a path or URL. Fix in the build
  command is `MSYS_NO_PATHCONV=1` or run from cmd.exe.
- `[infra]` `CONTACT_TO` set to `lukesimmonsnz+form@gmail.com` (Gmail plus-
  addressing) rather than `luke@lukesimmonsnz.kiwi` because the latter's
  mailbox isn't set up yet — Resend would bounce with "recipient not found"
  and then suppress the address. Fix later: enable Cloudflare Email Routing
  on the domain, forward `luke@lukesimmonsnz.kiwi` to Gmail, flip the env
  var back.
- `[docs]` Wrote [`docs/MONETIZATION.md`](MONETIZATION.md) — a structured
  assessment of monetisation options given Luke's specific situation. Three
  buckets: career capital (highest EV — site as engineering portfolio),
  direct monetisation (paid newsletter ≫ consulting ≫ open-source ≫ Ko-fi;
  ads discouraged), and the scope question (is 40 hrs/week the right
  allocation?). Concludes with a concrete list of site features to add in
  support of each path, none of them urgent.

- `[content]` Removed six placeholder chart figures from
  [`supply-economics.md`](../content/auckland/pages/housing/supply-economics.md)
  and [`affordability.md`](../content/auckland/pages/housing/affordability.md)
  — the data either requires manual curation or a fetcher that isn't yet
  built. Replaced each with a short prose paragraph pointing readers to the
  upstream source. Four specs / CSVs / SVGs deleted from
  [`content/auckland/data/`](../content/auckland/data/) and
  [`static/img/auckland/`](../static/img/auckland/). Only two figures now
  live across the three housing pages: the real OECD productivity chart and
  the real NIWA sea-level-rise map.
- `[content]` Added two new Auckland framing pages: [`last-100-years.md`](../content/auckland/pages/framing/last-100-years.md) and [`next-100-years.md`](../content/auckland/pages/framing/next-100-years.md). New `framing` section in [`blueprints/auckland.py`](../blueprints/auckland.py) + a new "Framing" link in the Auckland subnav at [`_layout.html`](../templates/research/_layout.html). Both pages are outlines (status: outline) with structural headings awaiting Luke's narrative expansion.
- `[agent]` Built the first upstream **fetcher**: [`content/auckland/tools/fetchers/oecd.py`](../content/auckland/tools/fetchers/oecd.py) — productivity-by-industry pull from OECD SDMX REST API (`DSD_PDB@DF_PDB_ISIC4_I4`), no auth, rebased to any chosen base year. Added fetcher-dispatch plumbing to [`render_charts.py`](../content/auckland/tools/render_charts.py): specs gain an optional `fetcher: {name, params}` block; when present, the renderer imports `tools/fetchers/<module>.py`, calls `<function>(params) -> bytes`, and writes to the spec's `data:` path before rendering.
- `[content]` Flipped `supply-construction-productivity` to real data via the OECD fetcher. Series rebased to 2010 = 100 (OECD NZ coverage starts 2010, not 2000 as the placeholder suggested). Shows construction productivity is actually **up ~11%** since 2010, not flat — a different story from the illustrative CSV.
- `[agent]` Abandoned the Stats NZ building-consents fetcher for now. Stats NZ's information-release pages are heavily JavaScript-rendered; the download URLs aren't in the raw HTML and no stable public CSV URL exists for the bulk release. The Aotearoa Data Explorer has an API but its free public tier isn't documented. Options for later: (a) use a headless browser to follow the download link, or (b) sign up for ADE API access. In the meantime `supply-annual-consents` and `supply-consents-by-typology` remain as illustrative placeholders with the "placeholder data" stamp visible.

- `[content]` Scaffolded the Auckland **chart pipeline**: raw-SVG renderer at
  [`content/auckland/tools/render_charts.py`](../content/auckland/tools/render_charts.py)
  (pure Python, PyYAML only, supports `line` + `bar`); spec directory
  [`content/auckland/data/charts/`](../content/auckland/data/charts/) with
  [`supply-annual-consents.yaml`](../content/auckland/data/charts/supply-annual-consents.yaml)
  as the first example; CSV directory
  [`content/auckland/data/series/`](../content/auckland/data/series/) with an
  illustrative placeholder CSV and a README mapping each of the nine
  referenced figures to its upstream data source. The existing `<img>` tags
  in the Auckland pages now resolve (previously all 404s).
- `[content]` Extended the renderer with `area-stacked`, `dual-axis`, and
  `placeholder` chart types; wrote specs and illustrative CSVs for the
  remaining 12 figures (9 charts + 3 map placeholders) across
  [land.md](../content/auckland/pages/housing/land.md),
  [supply-economics.md](../content/auckland/pages/housing/supply-economics.md),
  and [affordability.md](../content/auckland/pages/housing/affordability.md).
  All 13 figures now render with a "placeholder data" stamp; real data lands
  by swapping the CSV and flipping the spec's `status:` to `verified`.
- `[content]` Added escape hatch to
  [`render_charts.py`](../content/auckland/tools/render_charts.py): every
  rendered SVG now embeds a `data-pipeline=render_charts` signature, and the
  renderer skips any output that lacks the signature and is newer than its
  inputs. Plus an explicit `manual: true` spec flag for specs that are
  intentionally hand-produced. Workflow documented in
  [`data/series/README.md`](../content/auckland/data/series/README.md).
- `[content]` Added **map renderer** at
  [`content/auckland/tools/render_maps.py`](../content/auckland/tools/render_maps.py)
  — pure-Python GeoJSON → SVG projector, no GDAL. Fetches from public ArcGIS
  FeatureServer endpoints (Auckland Council Hub is unauthenticated), caches
  to [`data/maps/cache/`](../content/auckland/data/maps/cache/), supports
  pagination, category colouring, and the same escape-hatch as the chart
  renderer. First real map live:
  [`volcanic-cones-viewshafts.svg`](../static/img/auckland/volcanic-cones-viewshafts.svg)
  from Auckland Council's D14 locally-significant viewshafts overlay (5
  polygons, 3 cones — Mount Wellington, Rangitoto, One Tree Hill).
- `[ops]` Hooked `render_maps.py` into
  [`agent/run_regen_docs.bat`](../agent/run_regen_docs.bat) so the 15-minute
  scheduled task runs charts + maps together.
- `[docs]` Wrote [`docs/AUCKLAND-DATA-PIPELINE.md`](AUCKLAND-DATA-PIPELINE.md)
  — the Phase 2 roadmap: fetcher registry (one module per upstream), figure
  lint, and a daily refresh task. Not executed yet; the plan is the
  deliverable so Luke knows where this is going as he writes more subpages.
- `[content]` Fixed a cache-invalidation bug in
  [`render_maps.py`](../content/auckland/tools/render_maps.py): a stale
  background fetch of the wrong FeatureServer layer finished late and
  clobbered the cache with ~300 MB of irrelevant contour features (→ 115 MB
  SVG). Every cached GeoJSON now carries a `_pipeline.fetch_signature`
  (hash of URL + layer + where + outFields); the cache is discarded and
  re-fetched if the spec's current signature doesn't match.
- `[docs]` Wrote [`content/auckland/data/PLACEHOLDER-STATUS.md`](../content/auckland/data/PLACEHOLDER-STATUS.md)
  — a per-figure audit of all 13 Auckland figures, classifying each by data-access
  tier (open API no key, API with free key, direct CSV URL, manual, composite,
  needs reconnaissance) and recommending a fetcher build order for Phase 2.
- `[content]` Removed the volcanic viewshafts map from
  [`land.md`](../content/auckland/pages/housing/land.md) — the 5-polygon map
  without a basemap was visually confusing. Deleted the spec, cached GeoJSON,
  and rendered SVG.
- `[content]` Replaced the sea-level-rise placeholder on
  [`land.md`](../content/auckland/pages/housing/land.md) with a real map —
  NIWA-modelled coastal inundation under a 1% AEP storm tide + 1 m sea-level
  rise (639 polygon features from Auckland Council's FeatureServer). Now the
  sole figure on the page, renumbered to Figure 1. Briefly tried the Rural
  Urban Boundary and Unitary Plan Base Zone as candidates for a "land use"
  map; Base Zone blew up to 28 MB (139k polygons) and RUB looked too sparse
  on the page, so both were dropped.
- `[content]` Added `max_allowable_offset` option to
  [`render_maps.py`](../content/auckland/tools/render_maps.py) so coastline
  and parcel layers can be simplified server-side (via the ArcGIS query
  parameter of the same name) before the renderer sees them. Also added
  `category_labels:` to map numeric zone codes to human-readable legend
  labels. Both changes baked into the fetch signature so a simplification
  change invalidates the cache.
- `[content]` **Bug fix:** the `PIPELINE_SIGNATURE` I added as an escape-hatch
  marker was embedded as a bare attribute (`data-pipeline=render_charts` —
  unquoted), which is invalid XML. Strict SVG parsers in modern browsers
  rejected the whole file, so no figures rendered visually even though every
  SVG served HTTP 200. Fixed both renderers to emit a properly-quoted
  attribute (`data-pipeline="render_charts"`) and re-rendered all 10 figures;
  XML now parses cleanly.
- `[content]` Removed the three manual-curation-only figures from the housing
  pages (REINZ price-vs-consents lag, Saiz/Glaeser supply elasticity, Demographia
  long-run PTI). Replaced each `<figure>` block with a short paragraph that
  links readers to the authoritative upstream source. Orphaned chart specs,
  CSVs, and rendered SVGs deleted. Ten figures remain across the three pages;
  status doc updated accordingly. Viewshafts figcaption corrected to drop
  the stale "Placeholder" wording.
- `[ops]` Hooked `render_charts.py` into
  [`agent/run_regen_docs.bat`](../agent/run_regen_docs.bat) so the 15-minute
  scheduled task renders charts alongside the sitemap regeneration.
- `[agent]` Fixed a counting bug in
  [`agent/regen_docs.py`](../agent/regen_docs.py) — the new chart-spec YAMLs
  under `content/auckland/data/charts/` were being counted as Auckland
  entities. Added an `ENTITY_TYPE_DIRS` allowlist so only the eight real
  entity subdirectories are counted.
- `[ops]` Registered Windows scheduled task `lukesimmonsnz-regen-docs` to run
  [`agent/run_regen_docs.bat`](../agent/run_regen_docs.bat) every 15 minutes, so
  [SITEMAP.md](SITEMAP.md) and the auto-blocks in [`../README.md`](../README.md)
  and [ARCHITECTURE.md](ARCHITECTURE.md) stay current between agent runs.
- `[docs]` Rewrote the "A note on AI assistance" section in the sitemap template
  ([`agent/regen_docs.py`](../agent/regen_docs.py)) to reflect the new two-stage
  blog pipeline (private daily drafts → public weekly post) and to stop
  overclaiming editorial review on the three unedited research branches.
- `[site]` Renamed the blog Atom-feed author label from "Daily agent" to
  "Weekly agent" in [`templates/blog/feed.xml`](../templates/blog/feed.xml).
- `[docs]` Updated [ARCHITECTURE.md](ARCHITECTURE.md) §1.1 and §1.4 to talk about
  both daily and weekly agents instead of a single daily blog agent.
- `[docs]` Created this changelog.

## 2026-04-23 — 2026-04-24 (prior Claude-Code session)

Consolidated from the compaction summary of session
`bd93466c-88a9-4c76-a4e9-19bf5ccd1264`. Dates are approximate — the session
spanned both days.

- `[site]` Added a conditional **branch-authorship banner** to
  [`templates/research/_layout.html`](../templates/research/_layout.html):
  Auckland pages carry an `agent + luke` chip ("AI-drafted in iterative dialogue
  with Luke…"); CS / Climate / MedSci pages carry an `agent` chip ("AI-drafted
  reference notes that Luke has not edited…").
- `[site]` Replaced the "Conventions" section on
  [`templates/research/index.html`](../templates/research/index.html) with a
  two-column **"Two authorship regimes"** split explaining the same distinction
  in fuller prose.
- `[site]` Rewrote the blog index lede at
  [`templates/blog/index.html`](../templates/blog/index.html) to disclose the
  weekly-digest pipeline (local Ollama, `qwen2.5:14b`, HN + arXiv cs.AI).
- `[site]` Added `@app.after_request` hook in [`../app.py`](../app.py) that
  rewrites external `<a>` tags site-wide to open in a new tab
  (`target="_blank" rel="noopener"`).
- `[site]` Added `/sitemap/` route in
  [`../blueprints/main.py`](../blueprints/main.py) rendering
  [SITEMAP.md](SITEMAP.md) through the site's Markdown pipeline; linked from the
  footer.
- `[agent]` Split the blog agent into two stages:
  [`agent/daily_post.py`](../agent/daily_post.py) now writes **private drafts** to
  `agent/daily_drafts/` (gitignored, unserved), and
  [`agent/weekly_post.py`](../agent/weekly_post.py) (new) runs on Sundays to
  synthesise the week of drafts + weekly HN + arXiv into a single public post.
- `[agent]` Rewrote [`agent/prompts/daily_post.md`](../agent/prompts/daily_post.md)
  and added [`agent/prompts/weekly_post.md`](../agent/prompts/weekly_post.md)
  with voice rules that stop claiming Luke has read the content and require
  inline citations to provided source URLs only.
- `[agent]` Added [`agent/run_weekly.bat`](../agent/run_weekly.bat) and updated
  [`agent/run_daily.bat`](../agent/run_daily.bat) to call `regen_docs` after the
  agent run.
- `[agent]` Rewrote [`agent/regen_docs.py`](../agent/regen_docs.py) templates:
  trimmed the sitemap (removed route table, dynamic instances, special
  endpoints, issues, regeneration sections); added How-to-cite, Copyright,
  Privacy (with Cloudflare disclosure), Accessibility, About sections; render
  tree as a nested Markdown list rather than code-fenced ASCII.
- `[content]` Consolidated four daily agent-authored blog posts
  (2026-04-21 … 2026-04-24) into a single weekly digest at
  [`content/blog/2026-04-26-weekly-digest.md`](../content/blog/2026-04-26-weekly-digest.md);
  the four originals were deleted.
- `[content]` Corrected the weekly digest's Anthropic-postmortem paragraph
  after WebFetch revealed the postmortem describes March–April **2025** events,
  not 2026.
- `[site]` Consolidated three identical research pagination partials into a
  single `pagination_pair` macro at
  [`templates/_partials/pagination.html`](../templates/_partials/pagination.html);
  19 research templates updated accordingly.
- `[site]` Added footer copyright line and sitemap link in
  [`templates/_partials/footer.html`](../templates/_partials/footer.html).
- `[docs]` Moved `README.md` to the project root; rewrote for the two-stage
  agent pipeline and the Cloudflare ingress disclosure.
- `[docs]` Rewrote [`agent/README.md`](../agent/README.md) for the two-agent
  pipeline with an ASCII diagram and scheduling notes.
- `[content]` Updated site self-description in
  [`../data/projects.py`](../data/projects.py) — "self-contained" and
  "currently fronted by Cloudflare" rather than "local-first".
- `[memory]` Saved four cross-session memory files:
  `feedback_restart_after_python_changes`, `project_hosting_and_ai_posture`,
  `project_contact_form_email_flow`, `project_research_authorship_regimes`.
- `[ops]` Diagnosed the `stop.bat` gotcha: the launcher `flask.exe` PID is not
  the listener Python PID; killing the launcher can leave the socket held.
  Documented in [ARCHITECTURE.md](ARCHITECTURE.md) §5.1.
