# Handoff — consolidated section mode (Auckland pilot, ready for propagation)

This document is the bridge between the Aotearoa migration ledger in
`CLAUDE.md` and the next session that picks up this project (Cowork, the
CLI, doesn't matter — both load `docs/` files the same way). **Read
CLAUDE.md first**; this doc describes only the delta since its last update.

Authored 2026-05-02. PI: Luke Simmons. Auckland pilot complete; PI sign-off
granted in-conversation (page reads correctly in browser). Ready for
propagation to the other 15 regions.

---

## 1. What changed (delta from CLAUDE.md ledger)

The per-leaf rendering model in §6 row 4a–4q is superseded for the *routing
surface*. Entity data is unchanged. Per-leaf URLs (`/research/<region>/<theme>/<leaf>/`)
now 404; per-theme URLs (`/research/<region>/<theme>/`) now serve a single
consolidated essay covering every issue in the theme.

The per-leaf Markdown files at `content/<region>/pages/<section>/*.md` are
still on disk but unrouted — kept for diff/cite-check workflows. Do not
delete during propagation.

### New artifacts (Auckland only)

| File | Role |
|---|---|
| `content/auckland/templates/section.md.j2` | Renders one theme's full essay (issues as h2, narrative h3s, drivers + camps as prose, references deduped). |
| `content/auckland/tools/render.py` | Extended with `render_section()` and CLI flags `--section <slug>` / `--all-sections`. Legacy `render_problem()` retained. |
| `content/auckland/pages/_sections/<theme>.md` | 11 generated section essays. Frontmatter `kind: section`. |
| `templates/auckland/index.html` | Theme list shows plain bold title + one-sentence blurb (no link, no count, no view-all). Pulls blurbs from `section_blurbs` template var. |
| `templates/auckland/section.html` | Renders `consolidated.body_html` + cite block + bottom-of-page prev/next theme nav. Legacy fallback branch retained but unused. |
| `blueprints/auckland.py` | Adds `SECTION_BLURBS` dict (11 hand-authored sentences). Passed to factory via `section_blurbs=` kwarg. |
| `blueprints/region.py` | (a) Auto-detects consolidated mode via `(pages_dir / "_sections").is_dir()`; (b) `_section_neighbours()` helper for prev/next nav (alphabetical); (c) `_all_pages()` skips any path containing an underscore-prefixed dir or filename (excludes `_sections/*` and any future internal aggregations); (d) leaf route returns 404 in consolidated mode. |

### Orphan files left on disk (filesystem ACL blocked deletion)

These do not affect routing — they exist on disk but are not referenced:
- `content/auckland/pages/_sections/_all.md` (empty, from the cancelled `/all/` view)
- `templates/auckland/all.html`
- `content/auckland/templates/all.md.j2`
- `templates/auckland/index.html.fixed`, `templates/auckland/section.html.fixed`
- `content/auckland/templates/subpage.md.j2.new`

Clean up via Windows Explorer / git rm next time the workspace is read-write.
None of these are imported or rendered.

### Pre-existing bug fixed in passing

`content/auckland/templates/subpage.md.j2` referenced `d.core_claim` for
drivers, but the driver schema's text field is `description`. Drivers were
silently rendering with empty bodies on the legacy leaf pages. Fixed in
`section.md.j2`. The legacy `subpage.md.j2` still has the old wrong field
name; irrelevant unless leaves get re-routed, but worth fixing if anyone
regenerates leaf pages.

---

## 2. Architectural model after the pilot

Two independent axes:

```
                     │  consolidated_mode = True   │  consolidated_mode = False
                     │  (Auckland after pilot)     │  (other 15 regions, current)
─────────────────────┼─────────────────────────────┼─────────────────────────────
/research/<r>/       │  index of theme summaries   │  index of theme links
/research/<r>/<t>/   │  loads pages/_sections/<t>.md│  iterates pages/<t>/*.md
/research/<r>/<t>/<l>/  404                       │  loads pages/<t>/<l>.md
```

The mode switch is purely the existence of `pages/_sections/`. No
configuration flag, no kwarg. Generate the directory and the region flips.

Pagination between themes is alphabetical, computed in
`_section_neighbours()`, framing excluded. The order intentionally matches
the alphabetical order of `_pages_by_section()` (which the index uses), not
the dict insertion order of `SECTION_TITLES`.

---

## 3. Propagation plan (15 regions + NZ)

The Auckland pilot demonstrated the full pattern. Propagation is mechanical:

For each of the 15 remaining regions (`wellington`, `northland`, `waikato`,
`bay-of-plenty`, `gisborne`, `hawkes-bay`, `taranaki`, `manawatu-whanganui`,
`marlborough`, `nelson`, `tasman`, `west-coast`, `canterbury`, `otago`,
`southland`):

1. **Copy templates.** `cp content/auckland/templates/section.md.j2
   content/<region>/templates/section.md.j2`. The template is region-agnostic
   (uses `region` and `section_title` template vars).
2. **Copy renderer extension.** Replicate the `render_section()` function and
   `--section` / `--all-sections` CLI flags into `content/<region>/tools/render.py`.
   Note the `_SECTION_TITLES` dict at the top of render.py is per-region —
   copy from the region's existing blueprint.
3. **Generate section files.** `python content/<region>/tools/render.py --all-sections`.
   Produces 11 files in `content/<region>/pages/_sections/`.
4. **Author SECTION_BLURBS.** Add a `SECTION_BLURBS: dict[str, str]` to
   `blueprints/<region>.py`, one sentence per theme. Region-specific. Pass
   to `make_region_blueprint` via `section_blurbs=` kwarg.
5. **Copy templates.** `cp templates/auckland/{index,section}.html
   templates/<region>/`. Update breadcrumb labels and `url_for('<region>.…')`
   endpoint names in the new copies.
6. **Smoke test.** `flask test_client` hits should show: 11 section URLs 200,
   all leaf URLs 404, index has 11 blurbs no link, pagination at section bottom.

For NZ Pattern pages (`content/nz/`, `blueprints/nz.py`): different data
model (Pattern entities, not Problem). Defer until PI ratifies whether NZ
should also flip to consolidated mode or keep its current per-pattern view.

### Effort estimate

~30–60 min per region if no surprises; the bottleneck is authoring 11
SECTION_BLURBS per region (165 sentences total). Auto-deriving from the
section .md's first sentence is a faster fallback if the PI is happy with
generic blurbs.

---

## 4. Files to read before touching this surface

| Path | Why |
|---|---|
| `CLAUDE.md` | Ratified decisions, layer ledger, PI dynamic. Non-negotiable. |
| `docs/HANDOFF-consolidated-section-mode.md` | This file. |
| `docs/SCHEMA-DESIGN-aotearoa.md` | Typed entity graph definition. |
| `content/_schema/invariants.py` | 18 cross-entity predicates that gate render. |
| `blueprints/region.py` | The factory. Generic across regions. Auto-detects consolidated mode. |
| `blueprints/auckland.py` | Reference example for the new section_blurbs pattern. |
| `content/auckland/templates/section.md.j2` | Reference template for consolidated section rendering. |
| `content/auckland/tools/render.py` | Reference renderer with `render_section()`. |

---

## 5. Gotchas observed during the Auckland pilot

These bit me more than once. Worth bookmarking.

1. **`Edit` and `Write` tools occasionally truncate files mid-write.** When
   patching `region.py`, `render.py`, or any HTML/Jinja template, follow up
   immediately with `python3 -c "import ast; ast.parse(open(...).read())"`
   for `.py`, or load via Flask's test_client for `.html`. If truncated,
   re-write the tail via `bash` heredoc — that has been reliable.
2. **Stale `.pyc` cache masks broken Python.** When `blueprints/region.py`
   is mid-edit, Python silently loads `blueprints/__pycache__/region.cpython-310.pyc`
   from the previous successful compile. The route appears to "work" but
   serves stale logic. Always `rm -rf blueprints/__pycache__` after editing
   the factory, and force a recompile via `python3 -c "import py_compile; …"`.
3. **`start.bat` had a stale-PID bug.** Fixed in this session — added
   `setlocal EnableDelayedExpansion` and `!EXISTING_PID!` syntax. If
   `.server.pid` exists from a prior crash, `del .server.pid` then re-run.
4. **`content/<region>/tools/graph.py` defines `WellingtonGraph`** as the
   class name across *every* region (copy-paste artifact). Functionally
   correct because `load_graph()` resolves `root` from `__file__`, but
   visually misleading. Out of scope for the consolidated-mode work.
5. **Driver schema field is `description`, not `core_claim`.** Confirmed via
   `content/_schema/driver.schema.json`. Don't write templates that reference
   `d.core_claim`.
6. **Underscore-prefixed paths are conventionally internal.** The
   `_all_pages()` filter in `region.py` excludes any path with a `_`-prefixed
   part. Future internal aggregations should follow the same convention.

---

## 6. Verification harness

Run from the repo root with the venv activated.

```bash
# Lint (zero errors required before render)
python content/<region>/tools/lint.py

# Re-render section files
python content/<region>/tools/render.py --all-sections

# Boot smoke
python -c "from app import create_app; app = create_app(); print(len(app.url_map._rules), 'routes')"

# Per-region route check (test_client)
python -c "
from app import create_app
c = create_app().test_client()
for s in ['climate', 'transport', 'housing']:  # sample three
    r = c.get(f'/research/<region>/{s}/')
    print(r.status_code, len(r.get_data()), f'/research/<region>/{s}/')
"
```

Expected: section URLs 200, sizes 30–70 KB; leaf URLs 404 (in consolidated
mode); zero lint errors; route count steady (no new routes introduced by
propagation, only behaviour change of existing routes).

---

## 7. Open decisions for the PI

These have not been ratified and should not be assumed:

1. **NZ Pattern pages.** Same consolidated pattern, or keep current?
2. **Sitemap.xml.** Currently still enumerates per-leaf URLs (now 404 for
   Auckland). `blueprints/main.py:_region_urls()` should be updated to skip
   leaves when `_sections/` exists. Not yet done; will silently pollute
   search engines until fixed.
3. **CLAUDE.md ledger update.** The §6 layer ledger should grow a row
   describing consolidated mode + Auckland pilot completion. Defer to PI
   on wording.
4. **Cleanup of orphan files.** `_all.md`, `all.html`, `all.md.j2`, the
   `.fixed`/`.new` patch artifacts. Filesystem ACL blocked deletion in
   the session that produced them.
