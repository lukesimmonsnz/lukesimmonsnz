# CMS-IMPL-WAVE-4 — Settings surfaces, search & replace, diff/history

**Status:** design artefact — items 9 and 10 of `CMS-SPEC.md` §13, plus
the diff/history surface deferred from wave 3 (W3-3).
**Predecessors:**
- `docs/CMS-IMPL-WAVE-1.md` (items 1–3 ratified 2026-05-02)
- `docs/CMS-IMPL-WAVE-2.md` (items 5, 7, 8 ratified 2026-05-02)
- `docs/CMS-IMPL-WAVE-3.md` (items 4, 6 ratified 2026-05-02 — item 4 with
  preserved mastery gap)

**Held-back gate:** §3.3 strategy-B round-trip parser remains v2.

**Why this is the closing wave.** All 10 items in `CMS-SPEC.md` §13 are
covered after this document. The remaining surface is implementation,
which sits with the PI per the conceptual-gap regime.

---

## 9. Item 9 — Settings surfaces

### 9.1 Role

`/admin/settings/` exposes the five setting groups enumerated in
`CMS-SPEC.md` §7: site identity, navigation, theme tokens, contact
form, footer. Each group is a small typed form. On publish, settings
are written to `cms.db.settings` (k/v) and exported to a JSON snapshot
that `before_request` consumes to populate `g.site_settings`.

### 9.2 Storage layout — **decision needed (W4-1)**

Two regimes:

| Regime | Row layout | Trade-off |
|---|---|---|
| **(a) Flat dotted keys** | `site.name = "Luke Simmons"`, `nav.0.label = "Home"`, `theme.color.primary = "#1a73e8"` | Per-field SQL queries, easy update granularity, painful for nested arrays (navigation list) — requires synthetic `nav.<i>` indexing |
| **(b) JSON-blob per group** | `site = '{"name": "...", "tagline": "..."}'`, `nav = '[{"label": "Home", "url": "/"}, ...]'` | Five rows total; each settings form serialises its group to one blob; arrays trivially nestable; per-field updates require read-modify-write of the blob |

Recommendation: **(b) JSON-blob per group**. Five rows is a fixed cost;
the navigation list (variable-length) and theme tokens (variable-key)
are awkward under flat keys; read-modify-write at single-PI scale costs
nothing.

### 9.3 JSON exporter contract

On settings publish:

$$\text{publish\_settings}(g) \;\Rightarrow\; \text{instance/site\_settings.json} \leftarrow \bigcup_{g \in \text{groups}} \{g : \text{db\_blob}(g)\}$$

The exporter writes atomically (`os.replace`). The output schema is
flat-by-group:

```json
{
  "site":    { "name": "...", "tagline": "...", "url": "...", ... },
  "nav":     [ { "label": "Home", "url": "/" }, ... ],
  "theme":   { "color": {"primary": "#1a73e8", ...}, "font_stack": "...", "max_width": "70ch" },
  "contact": { "turnstile_site_key": "...", "submit_url": "..." },
  "footer":  { "copyright": "...", "social": [...] }
}
```

### 9.4 `before_request` hook

```python
# app.py  (delta — before_request registration)

@app.before_request
def _load_site_settings():
    g.site_settings = _site_settings_cache.get_or_load()
```

The `_site_settings_cache` is a module-level cache keyed by mtime of
`instance/site_settings.json`. Reload when mtime changes; hold reference
otherwise. PI fills the cache class body — small (~20 lines).

`g.site_settings` is then available to every template via a context
processor:

```python
@app.context_processor
def _inject_site_settings():
    return {"site_settings": g.site_settings}
```

Existing templates referencing `site_settings.site.name` etc. work
without further plumbing. PI to audit existing templates and migrate
hard-coded strings to `{{ site_settings.* }}` references on a
per-template basis (mechanical, not strategic).

### 9.5 Theme-token delivery — **decision needed (W4-2)**

Theme tokens are CSS custom properties. Two delivery mechanisms:

| Mechanism | Pipeline | Trade-off |
|---|---|---|
| **(a) Static CSS file** regenerated on settings publish | `publish_settings` writes `static/theme.css` containing `:root { --color-primary: #1a73e8; ... }` | Cached by browser (HTTP `Cache-Control`); separate file is grep-able; one extra atomic write per settings publish |
| **(b) Inline `<style>` block** in `templates/_base.html` | Populated from `g.site_settings.theme` at render | No cache (inlined per HTML); zero file regeneration; theme changes reflect immediately without cache invalidation |

Recommendation: **(a) static CSS file**. Browser cache wins; settings
publish frequency is low (PI authors theme rarely); the cache-bust
on regeneration is handled by appending the file's mtime as a
querystring (`/static/theme.css?v=<mtime>`). PI fills the bust logic.

### 9.6 Form UI

Each group is a Jinja partial under `templates/admin/cms/settings/`:

```
templates/admin/cms/settings/
  index.html         ← group selector + active form
  _site.html         ← site identity form
  _nav.html          ← drag-reorderable list
  _theme.html        ← colour pickers + token table; live preview via item 4
  _contact.html      ← Turnstile site key, submit URL
  _footer.html       ← copyright text, social links
```

Drag-reorder for navigation: a tiny vanilla-JS shim with `drag` events
plus a hidden ordered input. PI elects whether to add a library
(SortableJS, ~10 KB) or hand-roll.

### 9.7 Live theme preview

Theme-token edits drive item 4's preview overlay. The preview iframe
receives the **draft theme** (not yet published) via the same
`postMessage` channel as content drafts:

```javascript
// _theme.html shim
function pushThemeToPreview(theme) {
  document.getElementById("preview-iframe").contentWindow
    .postMessage({type: "cms-theme-preview", theme}, "*");
}
```

The iframe listens, applies the theme as inline `<style>` overrides for
the duration of the preview. On publish, the static CSS file
regenerates and the override becomes redundant.

This makes item 4's overlay reusable for theme edits, which is why
Q4 ratification (single source of truth) pays off here.

### 9.8 Contact form `.env` shadow rule

Per `CMS-SPEC.md` §0 row 12 (ratified): contact-form keys are
read-only-displayed from `.env`; Settings overrides write to
`instance/site_settings.json` and shadow `.env` at request time.

Implementation: in `before_request`, after loading `g.site_settings`,
overlay `.env` values that are not present in `site_settings.contact`:

$$\text{effective}(k) = \begin{cases}
  \text{site\_settings.contact}[k] & k \in \text{site\_settings.contact} \\
  \text{os.environ}[k] & \text{otherwise}
\end{cases}$$

The Settings UI shows the `.env` value as ghosted/read-only when no
override exists.

### 9.9 Invariants

1. **JSON exporter atomicity.** `instance/site_settings.json` is never
   torn — readers see either pre- or post-publish bytes
   (`os.replace`).
2. **`g.site_settings` consistency within a request.** The
   `before_request` hook reads the JSON once; subsequent re-renders in
   the same request observe the same snapshot. Concurrent settings
   publishes during a long request are not visible until the next
   request.
3. **Theme CSS bust.** The CSS file's `mtime`-querystring guarantees
   browsers fetch fresh after publish.

### 9.10 Implementation gap

- Five form partial bodies (mechanical).
- `_site_settings_cache` class body (~20 lines).
- `publish_settings` exporter body.
- The static-CSS regeneration logic (W4-2 (a)).
- Drag-reorder library/hand-roll choice for `_nav.html`.

---

## 10. Item 10 — Search & replace

### 10.1 Role

Site-wide text search across the CMS-editable surface. Replace
operation produces drafts (NOT direct writes), preserving the draft /
publish lifecycle.

Existing capability: `blueprints/search.py` indexes 709 rendered region
pages, ranked by title (×4) / summary (×2) / body (×1) hit count.

CMS extension: index the **source** content, not the rendered HTML, and
add YAML field values for `PROJECTED` pages.

### 10.2 Index scope

| Source | Indexed fields |
|---|---|
| `DIRECT_MD` (`/blog/`, methodology) | frontmatter `title`, `summary`; body Markdown |
| `HYBRID` (about, research index) | each slot's frontmatter + body |
| `PROJECTED` (corpus leaves) | YAML fields: `statement`, `category`, `theme`, child entity statements (drivers, camps, claims) |
| `SETTINGS` | not indexed (small surface; navigated via UI tree) |

The index is keyed by `page_id` (URL) — same identifier as the resolver
and draft store.

### 10.3 Index storage — **decision needed (W4-3)**

| Regime | Implementation | Trade-off |
|---|---|---|
| **(a) Extend in-memory rebuild** | Existing `blueprints/search.py` extended to walk `content/<region>/data/**/*.yaml`; rebuilt at startup | Simplest; matches current pattern; rebuild is ~1 s for ~2000 entities |
| **(b) Migrate to SQLite FTS5** | New `cms.db.search_index` virtual table; incremental update on draft autosave / publish | Persistent; supports incremental update; faster cold start; adds schema complexity |

Recommendation: **(a) in-memory rebuild** for v1. The cold-start cost
is paid once per Flask process; admin surface restarts are
infrequent. (b) becomes attractive only if index size grows beyond
~10k entries.

### 10.4 Search UI

```
GET /admin/search/?q=<query>&kind=<filter>&scope=<draft|published>
```

`scope`:
- `published` — search files on disk (default).
- `draft` — search the union of drafts + files (drafts shadow files
  for pages that have one).

Result row:

```
┌──────────────────────────────────────────────────────────────────┐
│ /research/auckland/transport/congestion/         [PROJECTED]    │
│ ...the Auckland congestion ranks in the top decile of OECD...   │
│   3 matches in this page                                         │
└──────────────────────────────────────────────────────────────────┘
```

Click → opens the editor, jumps cursor to first match.

### 10.5 Replace UI — confirm-per-match

Replace is **never blind-bulk**. The flow:

```
[1] PI enters find / replace strings, clicks "Find matches"
[2] Server returns a list of (page_id, line_number, context_before,
    context_after) tuples — match candidates
[3] UI renders one row per match with a checkbox
[4] PI selects matches, clicks "Apply to selected drafts"
[5] Server creates/updates a draft per affected page with the replace
    applied
[6] PI navigates to each affected page and Publishes via the normal
    pipeline
```

No replace operation writes directly to disk; all replaces go through
drafts. This is non-negotiable — preserves the publish lint gate (item
7) for projected pages.

### 10.6 Replace scope — **decision needed (W4-4)**

Within the confirm-per-match flow, two scoping options:

| Scope | Behaviour |
|---|---|
| **(a) Whole-string match** | `find = "Aotearoa"` matches every occurrence verbatim |
| **(b) Whole-word match (toggle)** | UI toggle for word-boundary regex `\bAotearoa\b` to avoid matching substrings (e.g. inside other words) |

Recommendation: ship with both — a UI toggle (`☑ whole word only`)
defaulting to **on**. Whole-word default avoids the surprise where
`find = "the"` matches inside words like "their".

### 10.7 Match-set safety

Before showing the match list, the search backend computes a checksum
over the match set. If between display and apply the underlying file
content changes (autosave from another tab, git pull), the apply step
detects the mismatch and re-prompts. Implementation: same `base_sha`
mechanism from wave 1 §3.2, applied per match-set.

### 10.8 Invariants

1. **Replace via drafts only.** No code path bypasses the draft store
   for replace operations.
2. **Idempotence on no-replace.** `find = X, replace = X` produces no
   drafts.
3. **Reversibility.** Each draft created by replace can be discarded
   normally; nothing about replace bypasses `drop_draft`.

### 10.9 Implementation gap

- `blueprints/search.py` extension to scan YAML field values.
- The find/replace UI partials.
- The match-set `base_sha` checksum logic (10.7).
- Cursor-jump behaviour on result click (10.4) — small JS.

---

## 11. Diff / history (deferred from wave 3 W3-3)

### 11.1 Role

Per-page surface for inspecting prior commits and restoring older
content. Backed by `git log -- <file>` and `git diff`.

The toolbar (item 6 §6.5) already has a "History" button placeholder.

### 11.2 History view

```
GET /admin/history/<page_id>
```

Returns a list of commits touching the page's source file(s). For
`HYBRID` and `PROJECTED` (multi-file) pages, the union of commits over
all `source_paths` is shown, deduplicated by SHA.

```
┌────────────────────────────────────────────────────────────────┐
│ <sha>  2026-04-27  cms: Wellington transport claim revision   │
│ <sha>  2026-04-26  cms: Wellington corpus initial commit      │
│ ...                                                            │
└────────────────────────────────────────────────────────────────┘
```

Each row is clickable: opens diff view between `<sha>~..<sha>`.

### 11.3 Diff view

```
GET /admin/diff/<page_id>?from=<sha>&to=<sha>
```

Renders unified diff. Library options (PI elects, **W4-5**):

| Library | Output | Trade-off |
|---|---|---|
| **(a) `subprocess git diff` + `<pre>`** | plain text diff | zero deps; no syntax highlighting |
| **(b) `subprocess git diff` + a JS diff renderer** (e.g. `diff2html`) | side-by-side HTML diff | adds ~50 KB JS; substantially more readable |

Recommendation: **(a)** for v1. Plain `<pre>` diff is sufficient for
single-PI reading; (b) is a polish item.

### 11.4 Restore-to-commit action

A "Restore to this version" button on each history row:

```
[1] User clicks "Restore <sha>" on /admin/history/<page_id>
[2] Server reads file content at <sha> via `git show <sha>:<path>`
[3] Server creates/replaces the draft for <page_id> with that content
    (base_sha = current file sha256, NOT the historical sha)
[4] Editor reloads showing the restored content as a draft
[5] PI publishes via the normal pipeline to apply
```

Restore goes through the draft, not direct file write — same regime as
search/replace (10.5). PI may inspect, edit, then publish.

### 11.5 Invariants

1. **Read-only over git.** History and diff views never mutate the
   git repo (no `git checkout`, `git reset`).
2. **Restore via draft.** The restore button creates a draft; it does
   not overwrite the working tree.

### 11.6 Implementation gap

- The two route handlers (`/admin/history/<page_id>`,
  `/admin/diff/<page_id>`).
- `git show <sha>:<path>` subprocess wrapper.
- Templates for history list and diff view (mechanical).

---

## 12. Open decisions for PI (wave 4)

| # | Decision | Recommendation |
|---|---|---|
| W4-1 | **Settings storage** (§9.2) — flat keys vs JSON-blob-per-group | **(b) JSON-blob per group**. Five rows; arrays/nested keys trivial. |
| W4-2 | **Theme-token delivery** (§9.5) — static CSS file vs inline `<style>` | **(a) static CSS file** with mtime cache-bust. |
| W4-3 | **Search index storage** (§10.3) — extend in-memory vs migrate to FTS5 | **(a) extend in-memory**. ~1 s rebuild; matches current pattern. |
| W4-4 | **Replace scope toggle** (§10.6) — whole-word default | Ship the toggle; **default on** to avoid `the`-inside-word surprises. |
| W4-5 | **Diff renderer** (§11.3) — `<pre>` plain text vs JS side-by-side | **(a) `<pre>`** for v1. JS renderer is polish. |

---

## 13. v1 closure

After wave 4 is implemented, all 10 items in `CMS-SPEC.md` §13 are
delivered:

| Wave | Items | Status |
|---|---|---|
| 1 | 1, 2, 3 — page resolver, `cms.db` DAO, draft store API | designed, ratified |
| 2 | 5, 7, 8 — page tree builder, publish pipeline, media library | designed, ratified |
| 3 | 4, 6 — preview overlay (mastery gate), two-pane editor partials | designed, ratified |
| 4 | 9, 10, diff/history — settings surfaces, search & replace, git surfaces | designed (this doc) |

The PI's mastery surface across all four waves:

1. **§3.3 strategy-B parser** — v2 stretch. Round-trip $R(R^{-1}(m'))=m'$
   for corpus leaves. Not blocking v1.
2. **§5.2 preview overlay** — wave 3 §4. Contract published; choice of
   candidate (A+B layered) ratified; implementation is PI's.
3. **All function bodies** across the four waves — type signatures,
   contracts, and invariants are stated; the bodies are mechanical and
   PI-completable.

The CMS, when shipped, replaces the YAML-form admin
(`blueprints/admin/...` from DASHBOARD-SPEC) as the primary authoring
surface. The DASHBOARD-SPEC routes survive at `/admin/yaml/...` as a
fallback for raw entity edits when projected MD's strategy-A form
isn't sufficient (CMS-SPEC §10).

## 14. Beyond v1 (informational)

Out-of-scope items from `CMS-SPEC.md` §12 that may surface as v2 work:

- §3.3 strategy-B Markdown round-trip parser.
- Per-slot `base_sha` for HYBRID conflict granularity (wave 1 §3.2 v2
  schema migration).
- Multi-user editing, role-based permissions.
- AI-assisted writing in-editor — orthogonal axis.
- DOI / Zenodo handshake — Phase-6 stretch from `CLAUDE.md`.
- Mobile admin UI.

None of these gate v1.
