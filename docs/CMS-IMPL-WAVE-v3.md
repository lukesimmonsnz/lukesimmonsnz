# CMS-IMPL-WAVE-v3 — Edit-everything dashboard

Status: design + implementation, this session.
Predecessor: CMS v2 tier 2 + parser/transforms shipped (handoff 2026-05-02).

## 0. Goal

After v2: 729 surfaces editable, 203 still LAYOUT_LOCKED.
After v3: 0 LAYOUT_LOCKED text surfaces. Every prose-bearing page on
the site addressable and editable through /admin/.

## 1. Strategy

The promotion pattern from v2-6 (header.md / footer.md), generalised:
each currently-locked Jinja page gains a content slot MD. The Jinja
template stays code-level for layout; the prose / headings / imagery
come from the slot, rendered into the template at request time.

Two slot variants per Q1 ratification:

  (a) Full-body slot   — slot replaces the template body entirely.
                         Used for /, /projects/, /contact/, /now/, /sitemap/.
  (b) Intro slot       — slot prepends; the rest of the Jinja stays.
                         Used for /davidsimmons/, /research/,
                         /research/<region>/, /research/nz/<theme>/.

## 2. Module surface

`blueprints/admin/cms/page_slots.py` (new) — extends theme_slots.py:

    page_slot_render(name) → str   # reads content/_pages/<name>.md,
                                   # md→html via existing pipeline,
                                   # cached at templates/rendered/_pages/<name>.html
    region_intro_render(region)    # content/<region>/_intro.md
    nz_intro_render(theme)         # content/nz/_intro/<theme>.md
    regenerate_page_cache(name)
    regenerate_region_intro(region)
    regenerate_nz_intro(theme)
    regenerate_all_v3()            # called at app startup

Mirror of v2-6 design — same mtime cache fall-through, same atomic write.

## 3. Resolver delta

Each page's builder, when its slot MD exists, returns DIRECT_MD
+ EDITABLE pointing at the slot. Live URL still served by the
existing public blueprint route; admin /admin/edit/?id=<url> opens
the slot.

    _build_home              → DIRECT_MD on content/_pages/home.md
    _build_davidsimmons_root → DIRECT_MD on content/_pages/davidsimmons.md
    _build_research_index    → DIRECT_MD on content/_pages/research-index.md
    _build_projects          → NEW; DIRECT_MD on content/_pages/projects.md
    _build_contact           → NEW; DIRECT_MD on content/_pages/contact.md
    _build_now               → NEW; DIRECT_MD on content/_pages/now.md
    _build_sitemap_html      → NEW; DIRECT_MD on content/_pages/sitemap.md
    _build_region_index      → DIRECT_MD on content/<region>/_intro.md (when present)
                               else falls through to LAYOUT_LOCKED behaviour
    _build_nz_pattern_theme  → adds `content/nz/_intro/<theme>.md` to
                               source_paths when present

## 4. Wave items

  v3-1   7 top-level pages           ratified strategy-a-or-b
  v3-2   16 region intros            content/<region>/_intro.md
  v3-3   11 NZ pattern theme intros  content/nz/_intro/<theme>.md
  v3-4   section block partials      ALREADY SHIPPED (templates/blocks/section_*.html)
  v3-5   bulk-seed 165 region        16 × 11 minus already-authored 12
         section stubs

## 5. Verification gate

  1. /admin/ tree shows all promoted surfaces under "Pages" section.
  2. /admin/edit/?id=/ opens content/_pages/home.md in the editor.
  3. Live `/` renders the slot's HTML at the configured insertion point.
  4. Round-trip: edit → save → publish → live page reflects change.
  5. `wc -l` audit on resolver.py + page_slots.py + 7 templates: no
     truncation; smoke test 8/8 admin routes still HTTP 200.

## 6. Out of scope for v3

  - templates/base.html itself stays code-level (deferred to v4).
  - 4xx / 5xx error pages stay code-level.
  - Search results template stays code-level.
  - Per-page Jinja override (frontmatter `template:` field) — v3-6 stretch.
  - Region intro-MD rendering for the 165 newly-seeded section stubs is
    out of scope; the stubs are byte-stable text PI overrides per page.
