# Architecture

<!-- auto:meta:begin -->
**Updated:** 2026-05-30
**Blog posts:** 17 · **Auckland entities:** 69 · **Auckland generated pages:** 61 · **URL rules:** 129
<!-- auto:meta:end -->

How this site is put together and why. Read [`../README.md`](../README.md) first if you want to run the code; this document is for a reviewer who wants to understand the design without running it.

---

## 1. Design principles

The design is conservative in scope but specific in taste. The four principles below are visible in the code; anywhere an implementation choice looks unusual, one of these is usually why.

### 1.1 Portable to self-hosting

The **architecture** is designed to run without a cloud backend: one Flask process, one hand-written stylesheet, filesystem-backed content, a single SQLite-free data layer (flat Python modules + YAML). `SITE_URL` defaults to `http://127.0.0.1:5000` in [`app.py`](../app.py) and is only replaced if explicitly set in the environment. The contact form writes to a local JSONL file at the origin rather than sending mail. The blog's daily and weekly agents both run on local Ollama, not a hosted API.

The **current deployment** is Cloudflare, chosen as a transitional measure until the owner has dedicated hardware for self-hosting. Practical implications:

- Cloudflare terminates TLS at its edge, so every request is visible to them as plaintext HTTP.
- Cloudflare's proxy sets a `__cf_bm` bot-management cookie on responses by default, and retains request logs per their retention policy.
- The Flask origin (whether Luke's current machine via Cloudflare Tunnel, or dedicated hardware later) still owns all state: `data/messages.jsonl`, `server.log`, `content/**`, the Auckland entity graph. Nothing the application writes is delegated to Cloudflare Pages/Workers/KV.

The architecture is the part that is local-by-design; the current hosting is the part that isn't, and the migration path to self-hosting is a hardware swap, not a rewrite.

### 1.2 No JavaScript framework

There is one `<script>` block on the whole site: a 20-line anchor-link helper in [`templates/base.html`](../templates/base.html). No bundler, no npm, no build step. Styling is one hand-written CSS file at [`static/css/main.css`](../static/css/main.css) using CSS custom properties for design tokens. The whole presentation layer is text you can read.

### 1.3 Content-as-data where — and only where — it earns its keep

The blog is plain Markdown. The projects list is a Python list. The biography is a Python data module. The Auckland research project, by contrast, is a typed entity graph with schema validation, a lint pass, and a renderer. The difference is the shape of the content: blog posts do not cite each other, projects do not need invariants across entries, but an Auckland problem page pulls together drivers, camps, evidence, and sources that are also referenced by other problems. When the structure has cross-references and invariants, data wins; otherwise Markdown wins. This trade-off is revisited in §7.

### 1.4 Reproducibility and honest provenance

Every Auckland page declares `generated_from` in its frontmatter so a reader or a reviewer can trace a rendered page back to the entity YAML. The Auckland lint gate ([`content/auckland/tools/lint.py`](../content/auckland/tools/lint.py)) refuses to render if an Evidence entity has no Source, or if a Camp lacks flagship moves / tensions / interventions / addressed problems. The goal is that facts are checkable, not persuasive. The blog agents run against version-controllable prompt files at [`agent/prompts/daily_post.md`](../agent/prompts/daily_post.md) and [`agent/prompts/weekly_post.md`](../agent/prompts/weekly_post.md).

Content drafting is two-channel and disclosed as such: the blog's two-stage pipeline (daily drafts → weekly public post) uses **local Ollama** (`qwen2.5:14b`); longer-form prose drafts — including the research pages under `/research/` and documentation like this file — are produced with **Claude AI via Anthropic's hosted API** and then edited before publication. Both channels feed into the same content tree; the lint gate (for Auckland) and ordinary editorial review (for everything else) are the checks.

---

## 2. Layered architecture

The site separates into four layers. Each is small; none has much coupling to the others.

### 2.1 Runtime layer — Flask app factory

[`app.py`](../app.py) is the entire runtime spec.

- `create_app()` builds a Flask instance, reads `SITE_URL` / `SITE_NAME` / `SITE_TAGLINE` into `app.config`, and registers five blueprints.
- A single `@app.context_processor` injects `site_url`, `site_name`, `site_tagline` into every template, so `render_template` calls stay small.
- Two error handlers (`404`, `500`) render bespoke templates at [`templates/404.html`](../templates/404.html) and [`templates/500.html`](../templates/500.html).
- No extensions. No middleware. No request hooks. No logger configuration beyond what Flask defaults to.

Blueprint URL prefixes are the only place in the code where URL structure is declared:

| Blueprint | Prefix | Source |
|---|---|---|
| `main` | `/` | [`blueprints/main.py`](../blueprints/main.py) |
| `blog` | `/blog` | [`blueprints/blog.py`](../blueprints/blog.py) |
| `research` | `/research` | [`blueprints/research.py`](../blueprints/research.py) |
| `auckland` | `/research/auckland` | [`blueprints/auckland.py`](../blueprints/auckland.py) |
| `davidsimmons` | `/davidsimmons` | [`blueprints/davidsimmons.py`](../blueprints/davidsimmons.py) |

The Auckland blueprint deliberately nests under `/research/auckland` so the URL structure expresses that Auckland *is* a research branch — not a peer section. The corresponding URL structure is enumerated in [`SITEMAP.md`](SITEMAP.md).

### 2.2 Presentation layer — Jinja inheritance

One `base.html` at [`templates/base.html`](../templates/base.html) provides the shell: `<head>` with OG + Twitter metadata blocks, fonts, canonical link, the Atom feed link, the `_partials/nav.html` include, the `{% block subnav %}{% endblock %}` extension point, and the `_partials/footer.html` include.

Two shared partials do most of the navigation work:

- **[`templates/_partials/nav.html`](../templates/_partials/nav.html)** — six-item top nav. Active state is derived from `request.endpoint` and `request.blueprint` (note the Research item matches when either `research` or `auckland` is the current blueprint).
- **[`templates/_partials/breadcrumbs.html`](../templates/_partials/breadcrumbs.html)** — a `breadcrumbs(items)` macro used by every content page. Each page passes a list of `(label, url_or_None)` tuples.

The research collection shares a single secondary layout:

- **[`templates/research/_layout.html`](../templates/research/_layout.html)** provides the primary research subnav (Overview / CS / Climate / Medical / Auckland) and a conditional secondary subnav for whichever branch is active, including Auckland. Prev/next links at the foot of each research page use the shared [`templates/_partials/pagination.html`](../templates/_partials/pagination.html) macro `pagination_pair(prev, next)`, which every branch imports.

Styling uses CSS custom properties in [`static/css/main.css`](../static/css/main.css):

- Design tokens: `.page`, `.page-header`, `.prose`, `.breadcrumbs`, `.subnav`, `.subnav-secondary`.
- Chip / card / work components: `.chips`, `.chip`, `.card-grid`, `.card`, `.work`, `.work-body`.
- Feed and list components: `.post-list`, `.pagination-pair`, `.anchor-link`.

There is no theme toggle. The palette and typography are set once.

### 2.3 Content layer — four distinct patterns

The content layer is the most interesting part of the design because it deliberately hosts **four** different patterns in the same Flask app. Each is the right shape for the content it holds.

#### a) Python data modules

[`data/projects.py`](../data/projects.py) and [`data/david_simmons.py`](../data/david_simmons.py) are plain Python modules exporting list and dict constants. The corresponding blueprint imports them and passes them straight to `render_template`. Convenient for small, heterogeneous data (mixed HTML, rich types, dates, nested lists) that a human edits rarely. Cheaper than YAML for a list of five things.

#### b) Markdown + YAML frontmatter (blog)

[`blueprints/blog.py`](../blueprints/blog.py) reads every `*.md` file from [`content/blog/`](../content/blog/), parses the frontmatter with `python-frontmatter`, renders the body with `Markdown` (`extra`, `codehilite`, `sane_lists`, `smarty` extensions), and serves it. Posts within `RECENT_WINDOW_DAYS` (7) are shown full-width on the index; older posts move to a year-grouped sidebar archive. The post URL is `/blog/<filename-stem>/`. The blueprint is a pure reader; new posts appear on the next request.

#### c) Hand-written research pages (per-page Jinja)

The three older research branches — Computer Science, Climate Science & AI, Medical Science — are each a set of per-page Jinja templates with one route per page in [`blueprints/research.py`](../blueprints/research.py). There is no generation step and no content store behind them; the template *is* the content, and the branch's navigation is curated by hand in [`templates/research/_layout.html`](../templates/research/_layout.html). Why this pattern? Because each page is long-form prose with a particular shape, and the cost of templating extraction for fixed content is negative: you lose version-controllable text and gain a content model you do not need.

#### d) Content-as-data (Auckland)

The Auckland subsystem is the one place where a content model pays for itself. It is described in detail in §3.

---

## 3. Auckland subsystem

### 3.1 Why content-as-data here and nowhere else

An Auckland problem page is not a standalone essay. It is a view over a graph: the Housing / Land page references drivers that also drive Housing / Supply Economics, evidence that is cited by multiple camps, sources that underpin multiple pieces of evidence, camps whose positions are defined in tension with one another. Hand-authoring this as Markdown would force the same cross-references to be duplicated across pages, and the first time a source citation changed, four pages would silently drift. A typed graph with schema validation and a render step makes the cross-references first-class and the outputs diffable.

There is also a correctness argument. The owner has committed to an even-handed framing for the Auckland research (see the briefing). Schema invariants — "every Evidence cites a Source", "every Camp has flagship moves / tensions / interventions / addressed problems" — are baked in as lint failures rather than style rules. The graph makes the discipline enforceable, not performative.

### 3.2 Entity types

Eight types live under [`content/auckland/data/`](../content/auckland/data/):

| Type | Purpose | Count |
|---|---|---:|
| **Problem** | A subpage of a research section. Owns narrative prose. | 3 |
| **Driver** | A causal factor that affects one or more Problems. | 15 |
| **Camp** | A cluster of proposed responses, with flagship moves, tensions, interventions, and the Problems it addresses. | 15 |
| **Evidence** | An atomic factual claim. Must cite at least one Source. | 17 |
| **Source** | A bibliographic entry. | 19 |
| **Response** | An existing policy or programme response (not yet populated). | 0 |
| **Metric** | A time-series indicator (not yet populated). | 0 |
| **Actor** | An institution or individual referenced across pages (not yet populated). | 0 |

The empty types are intentional placeholders; their schemas are real and their directories exist, so they can be populated without code changes.

### 3.3 IDs and namespacing

Every entity ID is prefixed with its type. `problem.housing.land`, `driver.regulatory_regime`, `camp.compact_city`, `source.linz`. The loader at [`content/auckland/tools/graph.py`](../content/auckland/tools/graph.py) cross-checks that the type prefix matches the directory the file lives in. Filenames under each type directory are the bare slug (`compact_city.yaml` → `camp.compact_city`). This makes references readable and resolves any ambiguity about what a bare slug means.

### 3.4 Schemas

JSON Schema Draft 2020-12 under [`content/auckland/schema/`](../content/auckland/schema/), one schema per entity type. All schemas use `additionalProperties: false` — unknown keys fail lint — and every ID pattern is the same shape: `^<type>\.[a-z0-9_.]+$`.

Validation is performed by [`graph.py`](../content/auckland/tools/graph.py) via `Draft202012Validator`. Errors are collected on `Graph.validation_errors` rather than raised, so the caller can batch-report all failures in one run.

### 3.5 Graph invariants (enforced by `lint.py`)

[`content/auckland/tools/lint.py`](../content/auckland/tools/lint.py) runs on top of the schema pass and enforces invariants that JSON Schema cannot express:

- **Reference integrity** — every ID mentioned in `driver_ids` / `camp_ids` / `evidence_ids` / `response_ids` / `source_ids` / `tensions_with` / `addresses` / `affects` / `measures` resolves to a known entity.
- **Problem minimums** — a Problem must have at least one Driver, Camp, Evidence, and Source.
- **Evidence provenance** — every Evidence must cite at least one Source.
- **Camp completeness** — every Camp must have at least one flagship move, tension, intervention, and addressed Problem.
- **Figure references** — a figure declared in a Problem's `figures` block must be referenced by image path or id in the narrative body.

Lint exits 0 on a clean graph and 1 on any failure. The render pipeline refuses to run on a failing graph unless `--skip-lint` is passed — deliberate friction for skipping the gate.

### 3.6 Render pipeline

[`content/auckland/tools/render.py`](../content/auckland/tools/render.py) loads the graph, runs lint (unless skipped), and for each target Problem writes Markdown under [`content/auckland/pages/<section>/<subpage>.md`](../content/auckland/pages/). The sole template is [`content/auckland/templates/subpage.md.j2`](../content/auckland/templates/subpage.md.j2).

Each generated file carries frontmatter with `section`, `subpage`, `title`, `summary`, `order`, `updated`, `status`, and `generated_from` keys. The `generated_from` field points at the source Problem's ID so the rendered output carries its own provenance. Both the source YAML and the rendered Markdown should be committed together so diffs of rendered output are visible in review.

### 3.7 Service-side (Auckland blueprint)

[`blueprints/auckland.py`](../blueprints/auckland.py) is a pure reader: it walks [`content/auckland/pages/`](../content/auckland/pages/) with `rglob("*.md")`, parses frontmatter the same way the blog blueprint does, and groups pages by section. Three routes:

- `GET /research/auckland/` — index of all sections (populated + in-progress).
- `GET /research/auckland/<section>/` — section hub.
- `GET /research/auckland/<section>/<subpage>/` — one page, with prev/next calculated from sibling order.

Display titles for section slugs live in a `SECTION_TITLES` dict at [`blueprints/auckland.py:27`](../blueprints/auckland.py). It acts as a forward declaration — eleven sections are named, but only `housing` has pages today. The Auckland index page renders both — populated sections link to their subpage list; the remaining sections appear under a dedicated "In progress" heading so visitors can see the scope without hitting 404s. A section's subpage URL resolves only after its Problems have been authored and rendered.

### 3.8 Adding a new Problem

1. Create `content/auckland/data/problems/<section>.<subpage>.yaml` with narrative, drivers, camps, evidence, sources, and figures.
2. Add or reuse any new Drivers / Camps / Evidence / Sources under their respective directories.
3. `cd content/auckland && python tools/lint.py` and fix until it returns 0.
4. `python tools/render.py <problem.id>` to write the Markdown.
5. If the section is new, add it to `SECTION_TITLES` in `blueprints/auckland.py` and restart the server.
6. `python -m agent.regen_docs` from the project root to refresh counts in `SITEMAP.md` / `README.md` / this file.

Everything above is verifiable against the code. If the Auckland pipeline ever drifts from this description, trust the code.

---

## 4. Routing and navigation

### 4.1 URL structure

Enumerated in [`SITEMAP.md`](SITEMAP.md). The design rules:

- **Trailing slashes on every content URL.** Flask redirects non-slashed versions.
- **Lowercase, kebab-case paths.** `climate-science-and-ai`, not `ClimateScienceAI`.
- **Sections nest their children.** A research branch is `/research/<branch>/<page>/`, never `/<branch>/<page>/`.
- **Auckland's URL reflects that it is a research branch.** Its prefix is `/research/auckland/`, so the breadcrumbs and the nav's "Research active" check both work without special-casing.

### 4.2 Breadcrumbs

Every content page renders breadcrumbs using the `breadcrumbs()` macro from [`templates/_partials/breadcrumbs.html`](../templates/_partials/breadcrumbs.html). A page passes a list of `(label, url_or_None)` tuples; the final tuple renders as the current page (no link). The macro is trivial, but centralising it means a global change to breadcrumb style is a one-file edit.

### 4.3 Subnavs

Research branches share one `_layout.html` and render a primary subnav (Overview / CS / Climate / Medical / Auckland) plus a conditional secondary subnav per branch. The secondary subnav is a static list inside the layout, not derived from the branch's route list — it is curated because page order carries editorial meaning.

---

## 5. Operational concerns

### 5.1 Start / stop

[`start.bat`](../start.bat) refuses to start a second copy, auto-creates `.venv` on first run, launches `flask run --no-reload` hidden via PowerShell, and records the PID in `.server.pid`. Stdout and stderr are redirected to `server.log` and `server.err`.

[`stop.bat`](../stop.bat) prefers `.server.pid` and falls back to killing whatever is listening on port 5000. It prints whether anything was actually stopped. **Known gotcha:** `.server.pid` stores the `flask.exe` launcher PID, which can be a different process from the Python interpreter that actually binds port 5000. Killing the launcher does not always kill the listener, and the netstat fallback is what does the real work in those cases. Always `curl` the site after a restart to confirm.

### 5.2 `--no-reload` posture

Deliberate. A single PID is clean to stop, and the Flask reloader's fork-on-change interacts badly with the hidden-window launcher on Windows. The cost is that Python changes require a restart; template and content changes are picked up on the next request, which is the usual development loop for this site.

### 5.3 Logs

- `server.log` / `server.err` — hidden Flask process stdout/stderr, overwritten per run.
- `agent/logs/daily.log` — append-only, truncated to the last 1000 lines at the start of each run.

### 5.4 First-run setup

`start.bat` creates `.venv/` and installs dependencies automatically if there is no venv. No separate bootstrap step.

### 5.5 Daily agent

Two cooperating agents, both running on local Ollama:

- [`agent/daily_post.py`](../agent/daily_post.py) runs every day. It fetches the current Hacker News top stories + the last 3 days of arXiv cs.AI, calls local Ollama, and writes a private draft to `agent/daily_drafts/YYYY-MM-DD-<slug>.md`. The drafts are **not served by Flask** and are gitignored; they are working notes for the weekly agent.
- [`agent/weekly_post.py`](../agent/weekly_post.py) runs on Sundays. It reads up to 7 daily drafts from the past week, fetches the week's top HN stories (via the Algolia HN search API) and the week's cs.AI arXiv papers, and writes one public blog post to `content/blog/YYYY-MM-DD-weekly-digest.md`. The weekly prompt is explicit that daily-draft citations must be cross-checked against the authoritative weekly HN/arXiv lists before being repeated — hallucinated attributions in daily drafts must not propagate into public posts.

Both scripts are idempotent, timezone-aware (Pacific/Auckland, with a loud UTC fallback if `tzdata` is missing), and retry on Ollama timeouts with exponential backoff. Both are scheduled via Windows Task Scheduler — see [`agent/README.md`](../agent/README.md) for the two `schtasks` commands.

The two-stage split is deliberate. A 14B local model does well on a tight input (2 sources, 300 words); it struggles on a wide, multi-topic comprehensive post across a full week of raw feeds. Splitting daily extraction from weekly synthesis keeps each stage inside the model's strengths.

### 5.6 Docs regeneration

[`agent/regen_docs.py`](../agent/regen_docs.py) walks `app.url_map` and the content directories, regenerates [`SITEMAP.md`](SITEMAP.md), and rewrites the `<!-- auto:* -->` blocks in [`../README.md`](../README.md) and this document. It is called at the end of `agent\run_daily.bat`, so counts update whenever the agent writes a new post. It is deterministic — no AI is involved in docs regeneration; the numbers are counted, not summarised.

### 5.7 Ingress (Cloudflare)

The current public-facing ingress is Cloudflare. The origin Flask process does not need to know about this — it still binds `127.0.0.1:5000`, and Cloudflare (via Tunnel or an equivalent reverse-proxy setup) forwards requests. TLS, edge caching of static assets, and bot-management cookies are handled at the edge; everything dynamic (blog, Auckland, contact form) hits the origin. The `SITE_URL` env var should be set to the public URL in the deployment environment so canonical links, OG tags, and the XML sitemap emit real URLs. The planned end-state is to move the origin from the current machine to dedicated self-hosted hardware; the ingress layer stays the same shape whether or not Cloudflare is in front.

---

## 6. Testing posture

There is no automated test suite. The closest approximation is the Auckland lint, which gates rendering. In practice:

- **Auckland data changes** are gated by [`content/auckland/tools/lint.py`](../content/auckland/tools/lint.py). No clean lint → no render.
- **Route correctness** is checked by ad-hoc `app.url_map` inspection and by [`SITEMAP.md`](SITEMAP.md) regeneration, which surfaces drift between declared routes and their templates/content.
- **Agent correctness** is checked by `python -m agent.daily_post --dry-run` and `python -m agent.weekly_post --dry-run`, which print the assembled prompt (and, for the weekly, the enumerated daily drafts and weekly HN/arXiv inputs) without calling Ollama or writing.

For a personal site of this scope, this is deliberate. A full test harness would be larger than the app it covers. If the app grows a feature where a test would pay for itself (for example, the contact form ever sends email), add a test then — not before.

---

## 7. Design decisions and trade-offs

Decisions the site has made that are not obvious from the code alone.

### Flask over a static site generator

Flask is slightly more flexible than Jekyll / Hugo / Eleventy, and the blog + Auckland blueprints benefit from the Python ecosystem (`jsonschema`, `python-frontmatter`, `PyYAML`, `markdown`). The cost is a running process rather than a pile of static files — a tradeoff that buys form-handling (the contact page), true dynamic routes (the Auckland page generator), and the ability to grow a real backend without changing hosts.

### Hand-written CSS, no framework

Tailwind / Bootstrap / shadcn would make the site cheaper to iterate but more expensive to read. One stylesheet with named tokens is legible and is as close as the site gets to a design system. Build tooling is more costly than it looks — the dependency graph of a modern frontend toolchain is larger than the site itself.

### Cloudflare ingress, self-hosted origin (not GitHub Pages)

The site is currently fronted by Cloudflare with a self-hosted origin, not deployed to GitHub Pages / Netlify / Vercel. Two reasons: **control** over the full stack (the contact form writes to local disk; static-host PaaS cannot run a Python origin at all), and **portability** to dedicated hardware later (the same Flask process moves; only the ingress changes). Cloudflare handles TLS, edge caching of static assets, and bot filtering; the origin handles everything dynamic. The stated end-state is a fully self-hosted origin on the owner's own hardware — Cloudflare is a transitional dependency, not a design commitment.

### Content-as-data for Auckland but Markdown for the blog

Cross-references and invariants earn the cost of a content model. Blog posts do not cite each other and do not need invariants across entries. The blog is Markdown. Auckland has a typed graph. If either side's constraints change, the line moves.

### Per-page Jinja templates for the older research branches

CS / Climate / Medical Science predate the Auckland subsystem. They are hand-written because their content is long-form prose, not entity-structured, and migrating them to a content model would be churn without payoff. If those branches ever grow cross-references (for example, a citation network), they will become candidates for a content model — but until then, the templates *are* the content.

### The agents are a separate concern from the web app

[`agent/`](../agent/) contains writers, not readers. They produce files that the blog blueprint reads. The agents could be removed entirely without touching the web app. The split is deliberate; writing and serving have different failure modes. The daily/weekly two-stage split inside the agent folder is a second application of the same principle — extraction and synthesis have different model-capacity requirements and different failure modes, so they are separate processes.

### `docs/SITEMAP.md` is auto-generated; `docs/README.md` and this file are hand-written with auto blocks

The sitemap is mechanical — the source of truth is `app.url_map` + the filesystem — so it is wholly regenerated. The README and architecture are narrative documents; regenerating them with an LLM daily would be churn at best and drift at worst. Instead, the regenerator rewrites only the small `<!-- auto:* -->` blocks that carry dated facts (counts, the "Updated" stamp). This keeps narrative text under human control while keeping volatile numbers honest.

---

## 8. Where the design is inconsistent, and why

It is worth stating inconsistencies plainly rather than hiding them.

1. **Three content patterns coexist.** Python data modules for small lists, Markdown for blog, content-as-data for Auckland, per-page Jinja for hand-written research. Each is the right pattern for its content. The cost is that a newcomer has four places to learn; the benefit is that no pattern is overextended.
2. **Auckland has a lint gate; nothing else does.** Because only Auckland has invariants that cross entries. The blog has no invariants to check; the projects list has no invariants to check; per-page research templates have no invariants to check. Adding lint for its own sake would be performative.
3. **`SECTION_TITLES` in `auckland.py` declares eleven sections; only `housing` has pages.** The extras will 404 until Problems exist for them. This is deliberate — the list is a forward declaration so the UI can preview the scope of the project without the data being there yet. It is a roadmap gap, not a bug.
4. **Auckland's forward-declared sections are in progress, not hidden.** The index page lists sections that do not yet have Problems under an "In progress" heading, so a reader can see the scope of the project without navigating to a 404.

---

## 9. What this document does not cover

- Specific page content. Read the pages.
- The contents of `content/auckland/briefings/` — those are private decision-support documents, not part of the public architecture.
- Cloudflare configuration specifics (which product, DNS, tunnel config, WAF rules). Those live outside the repo.
- Future plans beyond the agent roadmap in [`agent/README.md`](../agent/README.md).

If a reviewer reads this and still has questions about why the site is shaped the way it is, that is a documentation gap — flag it.
