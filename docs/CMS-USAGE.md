# CMS-USAGE — operating the lukesimmonsnz.kiwi content management system

**Audience:** PI (sole author) and any future Claude session that needs
to know what the CMS can do without reading the four wave docs.

**Status:** v1 feature-complete (2026-05-02). Two known surfaces are
deferred — see §10.

---

## 1. Launch

```powershell
cd "D:\ai-website-manager\Current website"
.\.venv\Scripts\Activate.ps1
flask --app app run
```

The dev server prints `Running on http://127.0.0.1:5000`. Leave it
running; Flask hot-reloads on most file changes.

Two admin surfaces hang off `/admin/`:

| URL | What |
|---|---|
| http://127.0.0.1:5000/admin/ | new CMS — page tree, editor, media, settings, search, history |
| http://127.0.0.1:5000/admin/yaml/ | DASHBOARD-SPEC YAML form — typed corpus entity editor (drivers, camps, claims, sources) |

The two surfaces share `cms.db` for drafts/media/settings; they touch
different aspects of the same content tree.

---

## 2. Page tree at `/admin/`

The landing page renders the full editable surface as a recursive
tree, plus a list of dirty drafts.

```
root
├─ Home          /                  layout-locked
├─ About         /davidsimmons/     layout-locked
│   ├─ Biography                    editable (slot)
│   └─ Citations                    editable (slot)
├─ Blog          /blog/             editable (index)
│   └─ <date> <title>               editable (each post)
├─ Research      /research/         layout-locked
│   ├─ Methodology                  editable (docs/METHODOLOGY.md)
│   ├─ Auckland                     layout-locked (16 regions)
│   │   └─ <theme>/<slug>/          editable (Problem YAML)
│   └─ NZ                           layout-locked
│       └─ Pattern: <theme>         editable (Pattern YAML — first match)
└─ Settings      /admin/settings/   editable (5 groups)
```

`edit ✎` links appear on every leaf with `lock=editable`. Layout-locked
nodes are shown for navigation but cannot be opened in the editor.

---

## 3. Editing a page

`/admin/edit/?id=<page_id>` — two-pane layout:

```
┌── header ───────────────────────────────────────────────────┐
│ CMS › <Title>  [direct_md]  /blog/<slug>/                   │
├── toolbar ──────────────────────────────────────────────────┤
│ Save  Publish  Discard  Media…  History  ↗ live   [status] │
├── frontmatter (collapsible YAML) ───────────────────────────┤
├── body ─────────────────────────┬── preview iframe ────────┤
│  <textarea>                     │  <iframe>                │
└─────────────────────────────────┴───────────────────────────┘
```

### 3.1 Status bar

- `fresh — no draft yet` → no draft on disk for this page
- `draft loaded` → an existing draft was reopened
- `saving…` → autosave PUT in flight
- `saved · 14:23:07` → draft persisted
- `publishing…` → publish POST in flight
- `published · abc12345` → git commit succeeded
- `conflict — reload to merge` → on-disk source SHA-256 has shifted
  since `base_sha` capture (someone else edited the file or you pulled)
- `save failed` / `publish failed` / `save error` → see browser DevTools
  Network tab; usually a 4xx/5xx from the API

### 3.2 Autosave / publish lifecycle

```
type → 2 s debounce → PUT /admin/api/draft/?id=<page_id>
                          (clamps base_sha; updates body+frontmatter)
        ↓ 400 ms debounce → postMessage to preview iframe (refresh)

click Publish:
  1. force-flush autosave
  2. confirmation dialog
  3. POST /admin/api/publish/?id=<page_id>
     - read draft
     - materialise via projection.save → file bytes
     - atomic write (os.replace)
     - lint (PROJECTED only; W2-2 split: schema hard, invariants soft)
     - render derived pages (PROJECTED only)
     - git add + commit  → "cms: publish <page_url> [<page_url>]"
     - drop draft row
  4. status shows commit short-sha; editor reloads with new base_sha
```

### 3.3 Frontmatter

The `Frontmatter` collapsible expands to a `<textarea>` containing the
raw YAML between the `---` markers (no markers themselves). Editing
this is **byte-preserving** — your key order, quote styles, and flow
vs block list styles are kept verbatim through the round-trip. (We
deliberately do NOT route this through PyYAML's emitter, which would
reformat aggressively.)

### 3.4 Live preview (DIRECT_MD / HYBRID-single)

The right pane embeds `/admin/preview/?id=<page_id>`. While a draft is
active, the preview shows your **draft** content rendered by the
production templates (single source of truth). The mechanism is a
request-scoped `Path.read_text` intercept (`overlay.py`), activated
during an internal `test_client.get(page_id)` call.

If the draft body is empty or no draft exists, preview falls through
to the published page (with a banner explaining).

### 3.5 Live preview is gated for corpus pages

PROJECTED corpus / pattern pages render the stub (published content +
banner). Live draft preview for those requires the corpus rendering
pipeline (`content/<region>/tools/render.py`) to accept in-memory YAML
instead of re-reading from disk — a deferred refactor. Until then,
preview shows the last-published version even when you have unsaved
corpus YAML edits.

---

## 4. Media library

Click `Media…` in the editor toolbar → `<dialog>` opens with:

- Drop zone (drag-drop) + file picker
- Search box (filename / alt-text / caption)
- Thumbnail grid (sorted newest-first)

Click a thumbnail → splices `![<alt>](url)` at the cursor in the body.
The URL is the **original-resolution** asset (W2-5 ratified). The
theme caps `max-width: 100%` so the original is the right default.

### 4.1 Upload pipeline

1. POST `/admin/api/media/` (multipart, field `file`)
2. SHA-256 over content
3. Dedupe — re-uploading the same bytes returns the existing row
4. MIME whitelist — accepts `image/{jpeg,png,webp,gif}` and
   `application/pdf`. **SVG is rejected** (stored-XSS surface)
5. Write to `static/media/<sha[:2]>/<sha>.<ext>`
6. If image → Pillow thumbnail at `<sha>_thumb.jpg` (max 240px, q=80)
7. Insert row in `cms.db.media`

### 4.2 Editing media metadata

`PATCH /admin/api/media/<id>/` with JSON `{alt_text, caption}`. Direct
write — no draft semantics for media metadata. The browse modal
exposes this via inline edit (when wired in v2).

---

## 5. Settings

`/admin/settings/` — five groups, each a JSON blob in `cms.db.settings`:

| Group | What it controls |
|---|---|
| **site** | name, tagline, url, favicon, og_image |
| **nav** | navigation list (array of `{label, url}`) |
| **theme** | CSS custom properties (color, font_stack, max_width) |
| **contact** | turnstile_site_key, submit_url (shadows .env) |
| **footer** | copyright, social links |

### 5.1 Workflow

1. Visit `/admin/settings/` → list of groups
2. Click a group → JSON textarea editor with per-group help
3. Edit JSON → click **Save** (validates JSON; persists to `cms.db`)
4. Repeat for other groups if needed
5. Return to `/admin/settings/` → click **Publish All**
   - Writes `instance/site_settings.json` (atomic)
   - Regenerates `static/theme.css` from theme group
   - Invalidates the in-process settings cache

### 5.2 Shadow rule

For contact-form keys (`turnstile_site_key`, `submit_url`):

$$\text{effective}(k) = \begin{cases}
  \text{site\_settings.contact}[k] & k \text{ present and non-empty} \\
  \text{os.environ}[k_\text{env}] & \text{otherwise}
\end{cases}$$

Settings override `.env` at request time. If you clear the setting,
`.env` takes over again on the next publish.

### 5.3 Theme tokens

The theme group's nested dict converts to CSS custom properties:

```yaml
color:
  primary: "#1a73e8"
  text: "#222"
font_stack: "ui-sans-serif, system-ui, sans-serif"
max_width: "70ch"
```

becomes

```css
:root {
  --color-primary: #1a73e8;
  --color-text: #222;
  --font_stack: ui-sans-serif, system-ui, sans-serif;
  --max_width: 70ch;
}
```

Note: dotted keys join with hyphens (`color.primary` → `--color-primary`).
Keys with underscores stay as-is. If you want `--font-stack` instead
of `--font_stack`, rename the JSON key to `font-stack`.

`<link rel="stylesheet" href="/static/theme.css?v={{ theme_css_bust }}">`
in your base template gets cache-busted by the file's mtime.

---

## 6. Search & replace

`/admin/search/?q=<query>&whole_word=1`

Walks all editable sources per request (no startup index — W4-3
ratified). Covers: blog, methodology, davidsimmons slots, all 16
region problem YAMLs, NZ pattern YAMLs.

### 6.1 Find

- Plain text search, case-insensitive
- `whole_word` toggle (default on, W4-4 ratified) — wraps query in `\b`
  boundaries
- Results group by page; up to 5 matches shown per page with ±2 lines
  of context; matched line gets `<mark>` highlighting
- Each result has an `edit ✎` link to the editor at that page

### 6.2 Replace

Reveal: type a replacement string in the toolbar, tick page checkboxes
(default: all selected), click **Apply to selected**.

**Replace operates only via drafts** (§10.5 invariant). For each
selected page:
- Load via projection
- `pat.subn(replace, body)` and `pat.subn(replace, frontmatter)`
- `drafts.put_draft(...)` with current `hash_concat` as `base_sha`

After apply: `created N draft(s); review at /admin/ then publish per
page`. The dirty-drafts list on `/admin/` shows the affected pages —
visit each, eyeball the changes, Publish individually.

PROJECTED pages are skipped silently because the corpus projection
load body is `simple A` and `pat.subn` on raw YAML risks breaking
quoting/structure. (Corpus replace would lift after a stricter
projection is wired.)

---

## 7. Diff / history / restore

`/admin/history/?id=<page_id>` — list of commits touching the page's
source files (max 50, newest first).

Each row links the short SHA to `/admin/diff/?id=<page_id>&from=<sha>`
which shows the unified diff for that single commit (vs. its parent;
root commits diff against the empty tree).

### 7.1 Restore to draft

Click `restore` next to any commit:
- Confirmation dialog
- `git show <sha>:<path>` extracts the historical file
- `_split_frontmatter` parses fm + body
- `drafts.put_draft(...)` with current on-disk `hash_concat` as base_sha
- Editor opens with the restored content as a fresh draft
- PI reviews and publishes (or discards)

**Read-only over git** (§11.5 invariant) — no `checkout`, `reset`, or
`revert`. The working tree is never touched.

### 7.2 Restore is gated for multi-source pages

Multi-slot HYBRID and PROJECTED pages raise `RestoreError` because
restoring transitive YAML entities atomically requires the projection
bodies to be filled in. Single-source pages (DIRECT_MD, slot_md,
section_md, simple-A corpus_leaf) work fine.

---

## 8. Working with the corpus through the new CMS

A corpus leaf at `/research/<region>/<theme>/<slug>/` opens the
**Problem entity YAML** in the editor textarea. You can edit the
Problem byte-preservingly and publish via git commit.

Transitive entities (drivers, camps, claims, sources, methodologies)
are **not** loaded into the same editor. To edit those:

- Navigate to `/admin/yaml/<region>/claim/<claim_id>/` (or driver, camp,
  source, methodology) — this is the DASHBOARD-SPEC typed-form editor
- It has its own save pipeline (`save_pipeline.py`) with full lint
  gating and atomic write

The two surfaces compose: the new CMS owns the Problem entity; the
DASHBOARD-SPEC owns the typed-graph leaves.

A v2 strategy-B parser would unify both into one editor (round-trip
the rendered MD ↔ YAML graph), with the proof obligation
$R(R^{-1}(m')) = m'$ on the renderer/parser pair. That's the explicit
v2 stretch.

---

## 9. Conflict resolution

Each draft carries `base_sha` = SHA-256 over the source files at the
time the draft was opened. On publish:

$$\text{conflict}(p) \iff \text{sha256\_concat}(\text{file}(p)) \neq \text{draft}(p).\text{base\_sha}$$

If conflict: 409 from `/admin/api/publish/`, status bar shows
`conflict — reload to merge`. The user's options:

- **Reload** the editor — re-reads the on-disk source as the new base.
  Loses the typed body unless saved separately.
- **Force-publish** — not currently exposed in the UI. To do it, drop
  the draft via `DELETE /admin/api/draft/`, then re-edit + publish.

True 3-way merge UI is in the design (`conflict_triple` returns
base/file_now/draft) but not yet wired. Single-PI scale rarely hits
this — typical trigger is `git pull` mid-edit.

---

## 10. What's deferred (known gaps)

| Feature | Status | What's missing |
|---|---|---|
| **PROJECTED preview** | stub | `render.py` refactor to take in-memory YAML |
| **Multi-slot HYBRID editor** | NotImplementedError | `home_slots`, `davidsimmons_slots` projection bodies |
| **Computed index pages** | layout-locked | Acceptable — these are template-driven, not file-backed |
| **Multi-entity corpus editor** | simple A only | Strategy A "graph form" or v2 strategy B (round-trip MD) |
| **Corpus replace** | skipped | Stricter projection that operates on parsed YAML safely |
| **Drag-reorder for nav** | JSON edit | SortableJS or hand-rolled drag handlers |
| **Color pickers / typed forms** | JSON textareas | per-group typed Jinja partials |
| **CodeMirror 6** | textarea | W3-2 ratified; vendor `static/vendor/codemirror.bundle.js` |
| **3-way merge UI** | 409 on conflict | conflict_triple → side-by-side merge editor |
| **Media browser as standalone page** | modal-only | `/admin/media/` page with infinite scroll |
| **`media_rebuild_thumbnails` admin command** | absent | walk media table, regenerate missing thumbs |

None of these block v1 use; each is a discrete win when scheduled.

---

## 11. Files / paths reference

```
D:\ai-website-manager\Current website\
├── app.py                                      ← Flask factory; wires CMS
├── instance/
│   ├── cms.db                                  ← SQLite: drafts, media, settings
│   └── site_settings.json                      ← exported on Publish All
├── static/
│   ├── theme.css                               ← regenerated on Publish All
│   └── media/<sha[:2]>/<sha>.<ext>             ← uploaded assets
├── content/
│   ├── blog/<slug>.md                          ← DIRECT_MD
│   ├── davidsimmons/<slot>.md                  ← HYBRID slot
│   └── <region>/data/problem/<theme>.<slug>.yaml  ← PROJECTED Problem
├── docs/
│   ├── METHODOLOGY.md                          ← DIRECT_MD
│   ├── CMS-SPEC.md                             ← top-level spec
│   ├── CMS-IMPL-WAVE-{1,2,3,4}.md              ← per-wave design
│   └── CMS-USAGE.md                            ← this document
└── blueprints/admin/cms/
    ├── __init__.py
    ├── blueprint.py                            ← Flask routes
    ├── resolver.py                             ← URL → PageRef + projections
    ├── db.py                                   ← cms.db connection / migrate
    ├── dao.py                                  ← row dataclasses
    ├── drafts.py                               ← draft CRUD + base_sha clamp
    ├── tree.py                                 ← page tree builder
    ├── media.py                                ← upload + browse + thumbnails
    ├── publish.py                              ← compositional publish pipeline
    ├── settings.py                             ← 5-group library + theme.css regen
    ├── search.py                               ← find_matches / apply_replaces
    ├── history.py                              ← git log/diff/show/restore
    └── overlay.py                              ← Path.read_text intercept (δ)
```

---

## 12. Troubleshooting

### CMS landing returns 500

Check Flask console for the traceback. Usual culprits:
- `cms.db` corrupted — delete `instance/cms.db`; first request
  recreates schema via `migrate()`. Loses drafts (intentional).
- `python-frontmatter` not installed — `pip install -r requirements.txt`

### Preview iframe shows "preview overlay not yet wired" banner

You're on a PROJECTED corpus / pattern page. Live preview is gated
there. The editor itself works; published view is what the iframe
shows.

### Settings publish writes JSON but theme.css doesn't update in browser

Browser cache. The `?v=<mtime>` querystring should bust it; if not,
hard-refresh (Ctrl+F5).

### Replace created drafts but I want to undo

Visit `/admin/` → for each affected page in the dirty-drafts list,
click `edit ✎` → click **Discard** → confirms.

### Corpus YAML edits broke lint

Lint runs on Publish for PROJECTED pages (W2-2 split: schema=hard,
invariants=soft). Schema errors abort publish; the file is on disk
but no commit. Edit again to fix; re-publish.

### Conflict on publish

`base_sha` mismatch. Either reload the editor (loses local edits but
reconciles base_sha) or use git CLI to inspect what changed
(`git log -p -- <path>`).

### git commit fails ("nothing to commit")

The draft body is byte-identical to the current file. Edit something
first, or verify the autosave actually wrote.

---

## 13. Extending the CMS

The four PI-mastery surfaces left in the codebase:

1. **`corpus_leaf_form_A` strategy A — multi-entity** (currently simple A,
   only Problem entity loaded). To extend: `_ProblemYamlProjection.load`
   resolves transitive driver/camp/claim/source/methodology files,
   concatenates with `# === <kind>:<id> ===` section markers, returns
   a multi-entity YAML buffer. `save` parses sections and dispatches
   to per-file writes.

2. **`pattern_form_A`** — symmetric to (1), but the source set is
   multiple Pattern files per theme.

3. **PROJECTED preview rendering** — refactor
   `content/<region>/tools/render.py::render_leaf` to accept an
   in-memory YAML graph dict instead of re-reading from disk. Inside
   `cms.preview` for PROJECTED, parse the draft YAML, build the graph
   slice, call render_leaf to produce MD, render the leaf template,
   return as iframe content.

4. **v2 strategy-B parser** — the round-trip MD ↔ YAML graph proof
   obligation:
   $$R(R^{-1}(m')) = m' \quad\text{and}\quad R^{-1}(R(g)) \cong g$$
   up to canonical child ordering. Requires anchored MD comments
   (`<!-- claim:claim.<region>.<theme>.<id> -->`) at every section
   boundary in the renderer's output, plus a parser that reverses the
   render. A genuine research-software artefact.

Each is a discrete project; the CMS-IMPL-WAVE-{1..4}.md docs spell out
the contracts and invariants.
