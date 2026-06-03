# CMS-SPEC — entire-site WYSIWYG Markdown CMS

**Status:** design spec, awaiting PI ratification.
**Goal:** WordPress/Wix-class browser editor for **every public page** of
`lukesimmonsnz.kiwi`. Two-pane Markdown + live preview, file-backed content
with hybrid SQLite for media / drafts / autosave.
**Supersedes scope of:** `DASHBOARD-SPEC.md` — that earlier document
described a YAML-form editor for the typed corpus only. Its implementation
(`blueprints/admin/*`) is preserved as the CMS's **YAML-fallback layer**
for raw entity edits when Markdown projection (§3.3) is insufficient.

---

## 0. Ratified decisions (2026-05-02)

| # | Decision | Source |
|---|---|---|
| 1 | **Scope**: Entire public site as CMS — personal site + corpus surface unified. Corpus YAML/lint regime is *wrapped*, not replaced (see §3.3). | PI 2026-05-02 |
| 2 | **Editing mechanic**: two-pane — Markdown source on the left, live HTML preview on the right (iframe served by the same Flask process). | PI 2026-05-02 |
| 3 | **Persistence**: hybrid — content stays file-backed (Markdown / YAML), media library + drafts + autosave use SQLite. | PI 2026-05-02 |
| 4 | **§11-Q1 — projected-MD strategy**: **A (field-level form) for v1**; B (Markdown round-trip with anchor parsing) explicitly deferred to v2. Trade-off acknowledged: corpus leaves edit as typed form, not as MD, until B's correctness obligation $R(R^{-1}(m'))=m'$ is discharged. | PI 2026-05-02 |
| 5 | **§11-Q2 — editor library**: **CodeMirror 6**, single-file ESM, vim mode optional. | PI 2026-05-02 |
| 6 | **§11-Q3 — image processing**: **Pillow thumbnails only** for v1. Responsive `srcset` deferred. | PI 2026-05-02 |
| 7 | **§11-Q4 — preview fidelity**: **production templates**, request-scoped overlay (§5.2). Single source of truth. | PI 2026-05-02 |
| 8 | **§11-Q5 — frontmatter UX**: **collapsible YAML editor**. Typed-per-field deferred until a frontmatter schema registry exists. | PI 2026-05-02 |
| 9 | **§11-Q6 — concurrency**: **single-PI**, no locks, content-SHA-256 `base_sha` conflict gate. 3-way merge UI on detect. | PI 2026-05-02 |
| 10 | **§11-Q7 — publish granularity**: **per-page git commit**. Preserves SEP citation block per-edition provenance. | PI 2026-05-02 |
| 11 | **§11-Q8 — theme tokens**: **live CSS custom-property editor** with side-by-side preview, reusing §5.2's overlay. | PI 2026-05-02 |
| 12 | **§11-Q9 — `.env` integration**: read-only display; Settings overrides write to `instance/site_settings.json` and shadow `.env` at request time (precedence: `site_settings.json ≻ .env`). | PI 2026-05-02 |

Wave 1 design (items 1–3 of §13): see `docs/CMS-IMPL-WAVE-1.md`.

---

## 1. What is to be edited

The site's renderable surface, by source:

| Section | URL prefix | Source on disk | Source format | Authoring model |
|---|---|---|---|---|
| Home | `/` | `templates/main/index.html` | Jinja | template-bound, see §3.4 |
| About / biography | `/davidsimmons/` | `templates/davidsimmons/*.html` + `content/davidsimmons/*.md` (mixed) | Jinja + MD | hybrid |
| Blog | `/blog/`, `/blog/<slug>/` | `content/blog/*.md` | Markdown + frontmatter | **direct MD** |
| Research index | `/research/` | template + `content/research/methodology.md` | Jinja + MD | hybrid |
| Region pages | `/research/<region>/[<theme>/[<slug>/]]` | `content/<region>/pages/**/*.md` (rendered) ← `content/<region>/data/**/*.yaml` (source) | rendered MD ← typed YAML graph | **projected MD** (§3.3) |
| NZ Pattern | `/research/nz/<theme>/` | `content/nz/data/pattern/*.yaml` (rendered to template) | typed YAML | **YAML or projected** |
| Methodology | `/research/methodology/` | `docs/METHODOLOGY.md` + `content/_schema/` | MD + JSON Schema | direct MD + schema browser |
| Sitemap / RSS / atom | `/sitemap.xml`, `/blog/feed.atom` | auto-generated | n/a | not editable |

The CMS treats Jinja templates as **layout-locked** (§3.4) — they are not
free-text-edited; their content slots come from Markdown / YAML.

Approximate page count (per CLAUDE.md):
$$|\text{leaves}| \approx 706_\text{corpus} + 33_\text{nz-pattern} + 13_\text{personal} + N_\text{blog} \approx 760+.$$

---

## 2. Architecture

```
┌────────────────────────────────────────────────────────────────┐
│  /admin/  (Flask blueprint, localhost-gated)                   │
│                                                                │
│  ┌─ Page tree ─┐  ┌─ Two-pane editor ────────────────────────┐ │
│  │ Home        │  │ ┌──────────────┐ ┌─────────────────────┐ │ │
│  │ About       │  │ │              │ │   <iframe src=      │ │ │
│  │ Blog        │  │ │  Markdown    │ │     /preview/...>   │ │ │
│  │  ├ post 1   │  │ │  (CodeMirror │ │                     │ │ │
│  │  └ post 2   │  │ │   or         │ │   live preview      │ │ │
│  │ Research    │  │ │   Monaco)    │ │                     │ │ │
│  │  ├ Auckland │  │ │              │ │                     │ │ │
│  │  │  └ ...   │  │ └──────────────┘ └─────────────────────┘ │ │
│  │  ├ ...      │  │                                          │ │
│  │  └ NZ       │  │ Toolbar: Save · Publish · Discard ·     │ │
│  │ Pages       │  │   Media · Diff · History                 │ │
│  │ Settings    │  │                                          │ │
│  └─────────────┘  └──────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────┘
                              │
            ┌─────────────────┼──────────────────┐
            │                 │                  │
       file system      SQLite (cms.db)     git
       (authoritative   (drafts, media,     (per-publish
        content)         autosave, locks)    commit)
```

### 2.1 Layers

| Layer | Responsibility |
|---|---|
| **Page resolver** | URL → (source, projection, lock) tuple. The single function the editor consults to load any page. |
| **Projection** | `MD ↔ YAML graph` for corpus pages (§3.3); identity for direct-MD pages; template-slot extraction for hybrid pages (§3.4). |
| **Draft store** (SQLite) | Per-(user, page) draft buffer; autosave every 2 s; survives reload. Promoted to file on Publish. |
| **Media store** (SQLite + `static/media/`) | Uploaded files on disk; metadata (alt text, caption, dimensions, mime, sha256) in DB. |
| **Preview** | Flask renders the same templates with the *draft* content layered over the published content via a request-scoped override. |
| **Publish** | Atomic write file → run lint pipeline (corpus only) → re-render derived pages → git commit. |
| **History** | `git log -- <file>` per page, with a "restore to commit" action. |

### 2.2 SQLite schema (sketch)

```sql
-- cms.db lives at instance/cms.db (Flask convention; out of git via .gitignore).
CREATE TABLE drafts (
    page_id     TEXT PRIMARY KEY,    -- canonical page URL, e.g. /blog/foo/
    body        TEXT NOT NULL,       -- current draft Markdown
    frontmatter TEXT,                -- YAML frontmatter as text
    base_sha    TEXT,                -- sha256 of file contents at draft start
    updated     TIMESTAMP NOT NULL,
    by_user     TEXT
);
CREATE TABLE media (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    sha256      TEXT UNIQUE NOT NULL,
    filename    TEXT NOT NULL,
    mime        TEXT NOT NULL,
    width       INTEGER, height INTEGER,
    bytes       INTEGER NOT NULL,
    alt_text    TEXT, caption TEXT,
    uploaded_at TIMESTAMP NOT NULL
);
CREATE TABLE settings (
    key TEXT PRIMARY KEY, value TEXT NOT NULL
);
-- Future: revisions, locks, comments — deferred to v2.
```

---

## 3. Source projection rules

The editor surface is uniform Markdown + frontmatter. The mapping back
to disk depends on page type. Three projection regimes:

### 3.1 Direct MD (`/blog/`, `docs/METHODOLOGY.md`, `content/<region>/pages/_sections/<theme>.md` *iff PI declares it source-of-truth*)

Identity projection: the editor's Markdown text is the file. Save writes
the buffer to disk verbatim. Frontmatter is parsed/serialised by
`python-frontmatter` (already a dep).

### 3.2 Hybrid template + content slots (`/davidsimmons/`, `/research/`)

The page consists of a Jinja template carrying layout, with one or more
**named slots** filled from sibling Markdown files. Example:

```
templates/davidsimmons/index.html        ← layout-locked
content/davidsimmons/biography.md        ← editable slot "biography"
content/davidsimmons/citations.md        ← editable slot "citations"
```

The CMS exposes each slot as an independent Markdown editor under a
"page" parent. The template stays read-only.

### 3.3 Projected MD ↔ typed YAML graph (corpus leaves)

This is the load-bearing piece and the genuine implementation gap. The
rendered Markdown for `/research/auckland/transport/congestion/` is
produced by `content/auckland/tools/render.py` from a Problem entity
plus its drivers, camps, claims, and sources. Two strategies:

| Strategy | Editor sees | On save |
|---|---|---|
| **A. Field-level form** | Every typed YAML field (statement, drivers[], camps[], claims[], systems_model{}). Same as current `/admin/` (DASHBOARD-SPEC). | Direct YAML write; lint runs; render runs. |
| **B. Markdown round-trip** | The rendered Markdown for the page, with each section anchored to its YAML source by HTML comments (`<!-- claim:claim.auckland.transport.x -->`). | Parse the edited Markdown back into YAML field updates by anchor matching. |

PI to ratify (§11 Q1). Recommendation: **A for v1, B as v2 stretch.**
Strategy B is the "Wix feel" but requires a bidirectional parser whose
correctness is a non-trivial proof obligation; strategy A reuses what
DASHBOARD-SPEC already shipped.

### 3.4 Layout-locked templates

The CMS does NOT permit free-form HTML edits to Jinja templates. A
"Theme" surface (§7) lets the PI adjust a small set of design tokens
(colours, spacing, typography). Template structural edits remain a
code-level change made outside the CMS.

---

## 4. Page tree

The sidebar tree is computed at request time from one function:

$$\text{tree}(t) = \{(\text{label}, \text{url}, \text{children}, \text{kind}, \text{lock})\}$$

where $\text{kind} \in \{\text{direct\_md}, \text{hybrid}, \text{projected}, \text{settings}\}$.

Top-level structure:

```
Home
About
  ├ Biography
  └ Citations
Blog
  ├ <date> <title>
  └ ...
Research
  ├ Methodology
  ├ Auckland
  │   ├ transport
  │   │   ├ congestion        ← projected MD ↔ YAML
  │   │   └ ...
  │   ├ housing
  │   └ ...
  ├ Wellington
  ├ ...  (16 regions)
  └ NZ
      ├ Pattern: housing
      └ ...
Settings
  ├ Site identity
  ├ Navigation
  ├ Theme tokens
  └ Contact form
```

The tree is filterable by free-text and by kind ("show only direct-MD").

---

## 5. Two-pane editor

### 5.1 Layout

```
┌─────────────────────────────────────────────────────────────────┐
│ Toolbar:  [Save draft]  [Publish]  [Discard]  [Media]  [⋯]      │
├─────────────────────────────────────────────────────────────────┤
│ Frontmatter (collapsible YAML editor)                           │
├──────────────────────────────────┬──────────────────────────────┤
│                                  │                              │
│    Markdown editor               │    Live preview iframe       │
│    (CodeMirror 6, vim mode opt.) │    src=/admin/preview/<id>   │
│                                  │                              │
│                                  │                              │
└──────────────────────────────────┴──────────────────────────────┘
   Status: autosaved 2 s ago · base sha matches · lint OK
```

### 5.2 Live preview

Implementation: the iframe loads `/admin/preview/<page_id>`. The Flask
view reads the *draft* row from `cms.db` for that page, applies it as
an override in a request-scoped overlay (Werkzeug context-local), and
calls the normal rendering pipeline. The result is byte-identical to
the published page modulo the override.

This avoids a parallel rendering stack — the public `render_template`
calls are reused intact.

Preview refresh: the editor pane debounces typing (≈ 400 ms) and emits
a custom event; the iframe listens via `postMessage` and reloads.

### 5.3 Editor library choice

PI to ratify (§11 Q2). Candidates:

| Library | Bundle size | Vim mode | Markdown affordances | Notes |
|---|---|---|---|---|
| CodeMirror 6 | ~200 KB | ✓ | extensions for headings, links, table | recommended |
| Monaco | ~2 MB | via plugin | fewer MD-native features | overkill |
| Textarea + custom JS | ~5 KB | ✗ | minimal | regression vs current expectation |

---

## 6. Media library

### 6.1 Upload flow

1. Drag/drop into editor pane → `POST /admin/api/media` with the file
   as multipart.
2. Server: compute sha256, dedupe against `media.sha256` unique index;
   if new, write to `static/media/<first-2-of-sha>/<sha>.<ext>`; insert
   row.
3. Response: `{id, url, width, height}` for the editor to splice into
   the Markdown as `![alt](/static/media/.../<sha>.png)`.

### 6.2 Media browser

A `/admin/media/` modal — grid of thumbnails, search by alt-text,
click to insert into the active editor.

### 6.3 Image processing

PI to ratify (§11 Q3). Options: do nothing (store as uploaded); generate
thumbnails synchronously via Pillow; generate responsive sizes
(srcset) via Pillow. Recommendation: thumbnails only for v1.

---

## 7. Settings surfaces

`/admin/settings/` exposes site-wide knobs. Each maps to a `settings`
row in `cms.db`, with a snapshot exported to `instance/site_settings.json`
on save (consumed by the Flask app's `before_request` to populate
`g.site_settings`).

| Surface | Keys |
|---|---|
| Site identity | `site_name`, `site_tagline`, `site_url`, favicon, OG image |
| Navigation | top-nav items (label, url) — drag-reorderable list |
| Theme tokens | colour palette (CSS custom properties), font stack, max width |
| Contact form | Turnstile site key, contact submit URL — currently in `.env`; CMS reads from there if present, writes to `instance/site_settings.json` if PI overrides |
| Footer | copyright, social links |

---

## 8. Draft / publish lifecycle

```
            type → autosave to drafts (2 s debounce)
                          │
                          ▼
                   PI clicks Publish
                          │
                          ▼
   [1] Read draft buffer from cms.db
   [2] If page kind == projected: parse MD → YAML deltas (strategy A or B)
   [3] Atomic write to file
   [4] Run lint pipeline (corpus only) — soft-block per CMS-SPEC §0
   [5] Re-render derived pages
   [6] git add + commit (per-page commit, message editable in toolbar)
   [7] Delete draft row
   [8] Reload editor with the new file as base
```

Draft conflict detection: each draft row carries `base_sha`. If the
underlying file has changed since the draft started (concurrent git pull,
or another tab edited the same page), the editor surfaces a 3-way merge
UI before allowing publish.

---

## 9. Search and replace

`/admin/search/?q=...` — full-text over all editable content (Markdown
bodies + YAML field values). Reuses the existing
`blueprints/search.py` index, extended to scan YAML in addition to the
already-indexed rendered pages.

Replace is a separate route that requires explicit confirmation per
match — no blind bulk apply.

---

## 10. Migration from the YAML-form `/admin/` (DASHBOARD-SPEC)

The corpus-form admin built last week becomes the **YAML-fallback layer**:

- Routes mounted at `/admin/yaml/...` (renamed from `/admin/...`).
- Reachable from any projected MD editor via a "Edit raw YAML" link in
  the toolbar.
- The schema-walker, edge registry, and save pipeline are unchanged.
- The new CMS root `/admin/` becomes the page-tree home.

Reusable from DASHBOARD-SPEC implementation:

| Component | Reuse |
|---|---|
| `blueprints/admin/save_pipeline.py` | atomic write, jsonschema validate, invariants, git commit — used by Publish (§8 step 3,4,6). |
| `content/_render/` | render dispatcher — used by Publish step 5. |
| `content/_schema/edges.yaml` | registry — used when YAML fallback is open. |
| `blueprints/admin/schema_walker.py` | used only inside the YAML fallback route. |
| Localhost gate | reused at the new `/admin/` root. |

---

## 11. Open design questions for PI — **all ratified 2026-05-02 (see §0 rows 4–12)**

| # | Question | Recommendation |
|---|---|---|
| 1 | **Projected-MD strategy** for corpus pages: A field-level form (current YAML editor) or B Markdown round-trip with anchor parsing? | **A for v1** (proven); B is v2 stretch. |
| 2 | **Editor library**: CodeMirror 6 / Monaco / textarea? | CodeMirror 6 — Markdown-native, vim mode optional, ~200 KB. |
| 3 | **Image processing on upload**: none / thumbnails / responsive srcset? | Thumbnails only for v1 (Pillow). |
| 4 | **Live preview fidelity**: same templates as production (recommended) or simplified preview-only template? | Same templates — single source of truth. |
| 5 | **Frontmatter editing UX**: collapsible YAML editor / typed form per known field / hidden? | Collapsible YAML — surfaces complexity only when needed. |
| 6 | **Concurrency model**: single-PI assumption (no locks) / pessimistic per-page locks / optimistic with merge? | Single-PI for v1; `base_sha` conflict detection without locks. |
| 7 | **Publish granularity**: per-page commit (current spec) / batch "publish all dirty drafts" / both? | Per-page default; batch is a stretch surface. |
| 8 | **Theme-token editor**: live CSS custom-property editor / hand-edit a JSON file? | Live editor with side-by-side preview. |
| 9 | **`.env` integration**: read-only display / overridable in Settings / hidden? | Read-only display; Settings overrides go to `instance/site_settings.json` and shadow the `.env` value at request time. |

---

## 12. Out of scope for v1

- Multi-user editing, role-based permissions, comments, approval flows.
- Plugin / extension system.
- WYSIWYG rich-text mode (only Markdown).
- AI-assisted writing (Claude integration in-editor) — a separate axis.
- Mobile-friendly admin UI — desktop-only at this scale.
- i18n / translation surfaces.
- DOI / Zenodo handshake (stays a Phase-6 stretch in CLAUDE.md).
- Auth (single-PI, localhost-only assumption persists).

---

## 13. Implementation deltas (left to PI)

Dependency-ordered. Each gates the next.

| # | Item | Notes |
|---|---|---|
| 1 | **Page resolver** (§2.1, §4) | Pure function. Unit-testable. The truth table for kind ∈ {direct_md, hybrid, projected, settings} per URL. |
| 2 | **`cms.db` schema + DAO** (§2.2) | SQLite + tiny dataclass layer. No ORM. |
| 3 | **Draft store API** (§8) | get_draft, put_draft, drop_draft, list_dirty. Autosave hook. |
| 4 | **Preview overlay** (§5.2) | Werkzeug context-local that intercepts file reads inside `render_template`. The novel piece. |
| 5 | **Page tree builder** (§4) | Walks filesystem; uses CLAUDE.md region list; produces JSON for the htmx sidebar. |
| 6 | **Two-pane editor partials** (§5.1) | Jinja + htmx + CodeMirror 6 (single-file ESM build pulled at page load). |
| 7 | **Publish pipeline** (§8) | Wraps DASHBOARD-SPEC's `save_entity` (corpus) and adds direct-MD/hybrid paths. |
| 8 | **Media library** (§6) | Upload, dedupe, browse, insert. Pillow for thumbnails. |
| 9 | **Settings surfaces** (§7) | Form per group; `instance/site_settings.json` exporter. |
| 10 | **Search & replace** (§9) | Index extension + UI. |

The conceptual gaps that should remain the PI's mastery:

- **§3.3 strategy B parser**, if/when v2 arrives — a Markdown-AST-walking
  function that emits typed YAML deltas. The contract is non-trivial:
  show that for any rendered page $r = R(g)$ where $g$ is the YAML
  graph, $R(R^{-1}(\text{edit}(r))) = \text{edit}(r)$ up to ordering of
  children. This is a real proof obligation.
- **§5.2 preview overlay**: the request-scoped intercept that diverts
  `Path.read_text` for files with active drafts. Subtle because Jinja
  caches, and because async render paths must not see the override.

The mechanical pieces (CRUD, file IO, search) are PI-completable from
the surface design above without me writing turn-key code.
