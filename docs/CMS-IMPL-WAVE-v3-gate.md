# CMS-IMPL-WAVE-v3 — gate-closed (2026-05-03)

Status: gate-closed; all v3 deliverables shipped; section-block end-to-end
exercised on /; about slots promoted; documentation caught up.

## 1. What shipped

| Item | Status |
|---|---|
| v3-1 — 7 top-level pages promoted (home, davidsimmons-root, research-root, projects, contact, now, sitemap) | DONE |
| v3-2 — 16 region intros (`content/<region>/_intro.md`) | DONE |
| v3-3 — 11 NZ pattern theme intros (`content/nz/_intro/<theme>.md`) | DONE |
| v3-4 — section block partials (`templates/blocks/section_*.html`) | shipped earlier; verified end-to-end this session |
| v3-5 — bulk-seed 165 region section stubs | DONE |
| v3-5b — 15 non-Auckland region section.html templates updated for consolidated mode | DONE |
| About slots — 4 davidsimmons sub-pages (biography→about, timeline, works, references) | DONE |
| Section blocks rendered on / via v2-1 → v2-3 → v2-9 chain | EXERCISED |

## 2. Edit-surface inventory after v3 close

| Category | Count |
|---|---|
| Top-level pages (home, davidsimmons-root, research-root, projects, contact, now, sitemap, blog-index, methodology) | 9 |
| Region intros (16 regions) | 16 |
| NZ pattern theme intros (11 themes) | 11 |
| Region section pages (16 × 11) | 176 |
| About slots (about, timeline, works, references) | 4 |
| Theme slots (header, footer) | 2 |
| Blog posts | 5 |
| Settings groups | 5 |
| Corpus leaves | 704 |
| **Total editable surfaces** | **932** |

## 3. Architectural delta

- `blueprints/admin/cms/page_slots.py` — 4 render functions
  (`page_slot_render`, `region_intro_render`, `nz_intro_render`,
  `davidsimmons_slot_render`) routed through
  `blocks/renderer.py::render_md_with_blocks` when `jinja_env` is
  available, falling back to plain `markdown.markdown` otherwise.
  This is what enables v2-9 directive blocks (`::section-hero`,
  `::section-cta`, etc.) to render in v3-promoted slots.
- `app.py` — startup invokes `regenerate_all_v3(jinja_env=app.jinja_env)`
  to pre-bake block-aware HTML caches at
  `templates/rendered/{_pages,region_intro,nz_intro,davidsimmons}/*.html`.
- 4 Jinja globals registered: `page_slot_render`, `region_intro_render`,
  `nz_intro_render`, `davidsimmons_slot_render`.
- 15 non-Auckland region section templates gained the
  `{% if consolidated %}...{% else %}{% for p in pages or [] %}...{% endif %}`
  guard. Auckland already had this; the 15 others now match.

## 4. Verification gate (this session)

```
v2-1 round-trip pytest:        12/12 green (carried forward from prev session)
v2 wave-bodies pytest:         32/32 green
public render of `/`:          200, contains block-section-hero +
                                block-section-feature-grid + block-section-cta
admin/edit smoke:              16/16 green across all promoted surfaces
public smoke:                  17/17 green across all promoted surfaces
edit-surface count:            932 (up from 928 in handoff)
```

## 5. Out of scope for v3 (deferred)

| Item | Why |
|---|---|
| PROJECTED preview rendering refactor | CMS-SPEC-v2 §14 row 2 — v1 carry-over PI mastery surface; preserved per ratification |
| `templates/base.html` data-driven `<head>` | layout-level edit; reserved for v4 |
| 4xx / 5xx error pages, search-results template | low-traffic; layout-level edits |
| v2-2 visual-block editor cells in /admin/edit | Sonnet-pinned focused session; v2-1 parser body is the dependency and has been satisfied, but the cell-rendering UI is its own ~4-6 hr surface |
| Per-page Jinja `template:` override (frontmatter-driven layout switching) | v3-6 stretch goal |

## 6. Tooling caveats encountered

- Write tool truncation pattern recurred on `app.py:174` mid-comment. Detected
  via `wc -l` discrepancy with Read; repaired via Python heredoc through
  `mcp__workspace__bash`. Same recovery pattern as the prior handoff §4/§5.1.
- FUSE mount blocks `unlink()` on bulk-revert paths. Pivoted from
  delete-and-revert to template-update strategy (15 region section.html
  guards) — better outcome than the original revert plan.
