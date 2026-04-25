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
