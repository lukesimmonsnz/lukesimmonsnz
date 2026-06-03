# CMS-SPEC-v2 — full-customization GUI

**Status:** design spec, awaiting PI ratification.
**Predecessor:** `docs/CMS-SPEC.md` (v1) and the four
`docs/CMS-IMPL-WAVE-{1,2,3,4}.md` docs. v1 ships an MD-source CMS with
typed-form fallback for the corpus; this document specifies the
extensions that close the gap to a **modern visual-website-builder
authoring surface** without abandoning the file-backed +
per-page-git invariants that make the corpus citable
(CMS-SPEC.md §0 row 10, ratified arch decision #1).

**Goal in one sentence.** Bring lukesimmonsnz.kiwi within a single
keystroke of every customisation a non-technical author would expect
from a visual website builder, while keeping every change a clean
line-level git diff.

**The relevant prior art** — pattern inventory drawn from across the
landscape, not a single product:

| Tool family | What we borrow conceptually |
|---|---|
| Gutenberg / Editor.js / TipTap / ProseMirror | Block-based authoring as the editor primitive |
| Webflow / Framer / Squarespace | Section-based page composition; design-system-as-tokens |
| Ghost / Notion / Tina CMS | Markdown-native source with visual overlay |
| Sanity / Strapi / Contentful / Builder.io | Schema-typed content (we already have this for the corpus) |
| Wix / Squarespace | Typography presets; theme switching with live preview |
| Hugo / Eleventy / Jekyll | Static-site purity; file-backed source-of-truth |
| WordPress / Drupal | Menu-builder UX; per-page SEO panels; tag/category taxonomies |
| Yoast / Rank Math | SEO panel ergonomics (character counts, schema.org typing) |
| Obsidian / Logseq | Reference-graph navigation between pages (latent v3) |

The v2 design picks the operationally-best pattern from each — not a
clone of any single tool — and renders it on top of the file-backed
substrate v1 already established.

---

## 0. Ratified architectural invariants (carried forward from v1)

These are non-negotiable; v2 design must honour them.

| # | Invariant | Source |
|---|---|---|
| I-1 | Content is file-backed (Markdown / YAML); SQLite is for ephemera (drafts, media, settings). | CMS-SPEC §0 row 3 |
| I-2 | Each publish is a per-page git commit; no batch-publish silently merges PI work into a single SHA. | CMS-SPEC §0 row 10 |
| I-3 | Round-trip is byte-identical (Markdown frontmatter + body, or YAML for corpus); editor surfaces never reformat what they don't touch. | α(md) round-trip property |
| I-4 | Live preview uses production templates; no parallel preview pipeline. | CMS-SPEC §11-Q4 |
| I-5 | Conflict detection via SHA-256 `base_sha`; no locks, single-PI scale. | CMS-SPEC §0 row 9 |
| I-6 | Localhost-gated admin; no auth surface in v1 or v2. | DASHBOARD-SPEC §0 |

The Wix/WordPress UX leans on a database-backed store and an in-product
editor that reformats content freely. v2 keeps the file-backed
substrate and adds a layered visual editor over it.

---

## 1. The modern-website-builder feature inventory, mapped to our regime

The capabilities a non-technical author expects from any modern
visual-website-builder, with v1 status and v2 plan:

| Capability | Why it matters | v1 status | v2 plan |
|---|---|---|---|
| **Block-based body editing** with insertable / reorderable / typed cells | Lets the author compose a page from semantic units (heading, paragraph, image, callout, columns, gallery, code, embed) without learning Markdown syntax | textarea + raw MD | **Block-as-directive** layer (§3) — MD stays source-of-truth, blocks are MD directives, editor renders each as a discrete UI cell |
| **Inline rich-text** within text blocks (bold / italic / link / code) | Most-frequent edit; demanding raw `**…**` is the biggest UX gap | none | Block-scoped toolbar that splices the right MD markers at the cursor (§3.4 / V2-10) |
| **Image upload with crop, focal point, alt text, caption** | Photo-heavy pages need fine control over how an image clips into a fixed container | upload + thumbnail only | **Media transforms** (§4) — crop, focal-point, responsive `srcset` |
| **Theme customisation with live preview** | Visual identity changes without touching CSS | 5 settings groups + `theme.css` regen | Theme **presets** + token-override layer + live preview via δ overlay (§5) |
| **Editable header / footer / sidebar** through the same UI as page bodies | Site-wide content (logo, nav, contact, social) is what makes the visual identity coherent | layout-locked Jinja | Promote to **MD slots** under `content/_theme/` (§6) |
| **Drag-and-drop menu builder** with nesting and reordering | Almost every site needs this; flat JSON config is a power-user fallback | flat JSON array | **Nested menu tree** + drag-reorder UI (§7) |
| **Per-page SEO panel** (meta description, OG image, schema typing, canonical, robots) | Search visibility is most authors' #1 motivation | frontmatter free-form | **Typed `seo:` frontmatter sub-tree** + dedicated SEO tab (§8) |
| **Page-builder layout sections** (hero, feature grid, CTA, columns) | Marketing / landing-page composition without a designer | none | **Section-block library** — full-bleed directive blocks (§9) |
| **Featured image + excerpt** for index / archive cards | Blog / portfolio / news templates universally use these | frontmatter free-form | Typed fields with media picker integration (§10) |
| **Taxonomy management** (tags, optionally categories) with auto-generated archive pages | Discovery; cross-linking; topic clustering | `tags:` in frontmatter, no archive | Auto-generated `/blog/tag/<slug>/` pages + management UI (§11) |
| **Responsive preview** (desktop / tablet / mobile) | Authors need to see what the reader sees on each form factor | desktop only | Viewport switcher in the preview iframe (§12) |
| **Analytics toggle** (provider-agnostic) | Site visibility into traffic without code changes | hardcoded none | Opt-in setting; script injection at base-template level (§13) |
| **Forms** (contact, signup, custom) | Reader engagement | hardcoded contact form only | Out of scope for v2 — keep code-level (§16) |
| **Reference graph navigation** (backlinks, "What links here") | Long-form research / wiki sites benefit substantially | none | Out of scope for v2; v3 candidate from the Obsidian/Logseq pattern |

The v2 implementation work is items §3–§13 (eleven of fourteen
patterns).

---

## 2. Architectural delta over v1

```
                  ┌── v1 ────────────────────────────────┐
                  │  resolver → projection → drafts →    │
                  │     publish (atomic write + git)     │
                  │                                      │
                  │  body = raw Markdown (textarea)      │
                  │  frontmatter = raw YAML (textarea)   │
                  └──────────────────────────────────────┘
                                    │
                                    ▼
       ┌──────────── v2 LAYER (additive; no v1 changes) ───────────┐
       │                                                           │
       │  ┌─ block parser (MD ↔ block tree) ─────────────────────┐ │
       │  │  Tokens: ::block-name{...attrs}\nbody\n::            │ │
       │  │  Block tree consumed by visual editor + renderer     │ │
       │  └──────────────────────────────────────────────────────┘ │
       │                                                           │
       │  ┌─ block library (Jinja partials per block kind) ──────┐ │
       │  │  paragraph, heading, image, gallery, callout,        │ │
       │  │  code, columns, embed, divider, button, hero, …      │ │
       │  └──────────────────────────────────────────────────────┘ │
       │                                                           │
       │  ┌─ visual editor (htmx + small JS shim) ────────────────┐ │
       │  │  Renders block tree as a column of UI cells;          │ │
       │  │  per-cell forms; "+" inserts new blocks; drag-reorder │ │
       │  └──────────────────────────────────────────────────────┘ │
       │                                                           │
       │  ┌─ theme preset system (presets + override deltas) ────┐ │
       │  │  Final CSS = compose(preset_base_tokens,             │ │
       │  │                       user_override_tokens)          │ │
       │  └──────────────────────────────────────────────────────┘ │
       │                                                           │
       │  ┌─ extended frontmatter schema (typed seo, excerpt, …) ┐ │
       │  └──────────────────────────────────────────────────────┘ │
       │                                                           │
       └───────────────────────────────────────────────────────────┘
```

Crucially, **v1 still works after v2 lands**. A page authored without
any block directives is still valid Markdown that v2 renders unchanged.
The block layer is opt-in per page.

---

## 3. Block-based authoring via MD directives

### 3.1 Why directive-MD instead of a JSON block tree

WordPress's Gutenberg stores blocks as HTML comments wrapping the
rendered output. This makes the source diff-friendly but the format is
HTML, not Markdown.

We extend Markdown with **directive blocks**, a syntax already
proposed by [CommonMark generic directives][cm-directives] and
implemented in `markdown-it-directive`, `mdx`, and `myst`. The on-disk
representation:

```markdown
# Auckland congestion

A short paragraph that's plain Markdown — no block syntax needed.

::callout{type=warning title="Construction-era CRL"}
Single-track operation through 2026; expect 30–40% capacity reduction.
::

::columns{count=2}
::: column
Left content. Plain MD.
:::
::: column
![Median multiple](/static/media/.../auckland_mm.png)
:::
::

More plain Markdown after the block.
```

### 3.2 The block grammar

A directive block:

$$\text{block} \;=\; \texttt{::}\,\text{name}\,\{\text{attrs}\}\,\texttt{\textbackslash n}\,\text{body}\,\texttt{\textbackslash n::}$$

Nested blocks use one extra colon per nesting level: `:::`, `::::`.
This matches the existing MDX/MyST convention so PI can paste content
between systems if useful.

`attrs` is a space-separated list of `key=value` pairs. Quoted values
support spaces. The grammar is deliberately small — anything more
elaborate goes in the body as YAML frontmatter (block-scoped).

### 3.3 Round-trip property — **PI mastery surface**

The block parser must satisfy:

$$P_\text{md→tree}(P_\text{tree→md}(t)) = t$$
$$P_\text{tree→md}(P_\text{md→tree}(s)) \equiv s$$

up to canonical attribute ordering and whitespace normalisation
internal to a block. The proof obligation:

- Blocks not authored as directives (plain MD paragraphs / headings /
  images) are kept as-is, never reformatted (extends I-3 to v2).
- Authoring a block via the visual editor and saving produces the
  same on-disk text as if the PI had hand-written the directive.
- Editing one block does not perturb sibling blocks' bytes.

This is the v2 analogue of v1's `_split_frontmatter` round-trip
identity — and a more involved proof. **PI's mastery work**: the
parser body. The contract above is the spec it must satisfy.

### 3.4 Block library

Twelve seed blocks, mirroring Gutenberg's "core" blocks:

| Block | Attrs | Body |
|---|---|---|
| `paragraph` | `align?` | inline MD (text + bold/italic/link) |
| `heading` | `level` (1–6), `id?` | inline MD |
| `image` | `src`, `alt`, `caption?`, `align?`, `focal?` | none |
| `gallery` | `cols`, `crop?` | list of `image` blocks |
| `code` | `language?` | code text |
| `callout` | `type` (info/warning/tip/danger), `title?` | nested blocks |
| `columns` | `count` (2/3/4), `gap?` | `column` children |
| `column` | none | nested blocks |
| `embed` | `url`, `provider?` (youtube/vimeo/twitter) | none |
| `divider` | `style?` (line/space/star) | none |
| `button` | `href`, `style?` (primary/secondary), `target?` | text |
| `hero` | `image?`, `align?`, `height?` | nested blocks |

Three "section" blocks (full-bleed page-builder layouts):

| Block | Attrs | Body |
|---|---|---|
| `section-hero` | `bg_image?`, `height?` | heading + paragraph + button |
| `section-feature-grid` | `cols` (2/3) | list of feature cells |
| `section-cta` | `bg_color?` | heading + paragraph + button |

PI can extend the library by adding a Jinja partial at
`templates/blocks/<name>.html` and registering an entry in
`content/_blocks/registry.yaml`. Custom blocks are first-class.

### 3.5 Visual editor surface

The editor's body pane (currently a single `<textarea>`) becomes a
column of **block cells**, each rendered server-side from the parsed
block tree:

```
┌─ block toolbar (insert │ duplicate │ move │ delete) ──┐
├──────────────────────────────────────────────────────┤
│ [paragraph]   "A short paragraph that's plain MD."   │  ← editable
├──────────────────────────────────────────────────────┤
│ [callout warning] "Construction-era CRL"             │
│   "Single-track operation through 2026..."           │
├──────────────────────────────────────────────────────┤
│ [columns: 2]                                         │
│   ┌─ column ──────────┬─ column ─────────────────┐  │
│   │ "Left content..." │ "[image: auckland_mm.png]"│  │
│   └───────────────────┴───────────────────────────┘  │
└──────────────────────────────────────────────────────┘
        ↑ "+" insertion gutters between blocks
```

Each cell is a server-rendered htmx fragment. Inline editing of a
paragraph block uses `contenteditable="true"` with a small toolbar
for bold/italic/link. Other blocks expose a per-attribute form on
click.

### 3.6 Source-of-truth toggle

A header switch lets PI flip between **visual** mode and **source**
mode (the v1 textarea). Source mode shows the same MD that visual mode
parses. This is how Gutenberg's "Code editor" works.

---

## 4. Media transforms — crop, focal point, srcset

v1: original + thumbnail.
v2 adds **per-asset transforms**:

```sql
CREATE TABLE media_transforms (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    media_id      INTEGER NOT NULL REFERENCES media(id),
    kind          TEXT NOT NULL,    -- 'crop' | 'focal' | 'rotate'
    params        TEXT NOT NULL,    -- JSON
    output_sha    TEXT NOT NULL,    -- sha256 of derived asset
    created_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

Crop / focal-point UI: media browser opens an asset → crop overlay
(draggable rectangle) → save → persists derived asset at
`static/media/<sha[:2]>/<sha>__<transform-id>.<ext>`.

Responsive `srcset`: the renderer emits multiple sizes (320, 640,
1024, 1920) on demand, generated lazily by Pillow on first request,
cached on disk. `<img srcset="..." sizes="...">` in the rendered HTML.

This is mechanical; no PI mastery.

---

## 5. Theme system v2 — presets + override layers

### 5.1 The mathematical model

A theme is a flat dict of design tokens:

$$\Theta : K \to V$$

where $K$ is a finite token-name set and $V$ is the value type
(strings — colors, dimensions, shadows, etc.).

A **preset** is a curated $\Theta_p$ shipped with the CMS. v2 ships
three:

| Preset | Aesthetic | Token count |
|---|---|---|
| `editorial` | David Roy Simmons biography aesthetic — serif headings, narrow column, generous spacing | ~40 |
| `documentary` | Research-corpus aesthetic — sans-serif, grid layout, dense | ~40 |
| `classic` | Personal-blog aesthetic — sans-serif, single column, default | ~40 (current site's tokens) |

A user override is a sparse dict $\Delta : K \to V$ stored in the
existing `theme` settings group. The effective theme is

$$\Theta_\text{effective} = \Theta_p \oplus \Delta$$

where $\oplus$ is pointwise overwrite (right argument wins).

`regenerate_theme_css` (v1) is extended to first load the active
preset, then layer the override.

### 5.2 Token taxonomy

Beyond v1's `color.primary`, v2 standardises:

```
typography:
  scale         (modular ratio; e.g. 1.25)
  font-family-body
  font-family-heading
  font-family-mono
  line-height-body
  line-height-heading
  weight-body
  weight-bold
  weight-heading

spacing:
  unit          (4px or 8px)
  scale-0..-9   (computed from unit × Fibonacci)

color:
  primary, primary-fg
  bg, fg, muted, accent, danger, success
  surface-1, surface-2 (cards, modals)
  border

radius:
  sm, md, lg, full

shadow:
  sm, md, lg

motion:
  duration-fast, duration-base
  easing-standard, easing-emphasised

layout:
  max-width, gutter
  breakpoint-sm, breakpoint-md, breakpoint-lg
```

This is ~40 tokens — a small, documentable design system, not the
unbounded CSS surface a real WordPress theme ships.

### 5.3 Theme customizer UI

Replaces the v1 JSON-textarea editor for the `theme` group:

- **Preset selector** — three radio buttons + "custom" (no preset, all
  values come from override)
- **Live preview** — δ overlay activates a sandbox theme; preview
  iframe re-renders with override theme as inline `<style>`
- **Per-token form** — each token in the taxonomy gets an appropriate
  input (color picker for colors, slider for scales, text for
  font-family, etc.)
- **"Reset to preset"** per-token button

Saving writes the override-only delta to the `theme` group. Preset
choice goes to a new `theme_preset` settings key.

---

## 6. Template slots — header, footer, sidebar as MD

Currently `templates/_partials/header.html`, `footer.html` etc. are
Jinja-only and edit only at code level. v2 promotes them to **MD
slots**:

```
content/_theme/
  header.md         ← logo + nav (rendered in <header>)
  footer.md         ← copyright + social (rendered in <footer>)
  sidebar.md        ← right-rail content (research index pages)
```

Each is a DIRECT_MD page in the resolver:

```
GET /admin/edit/?id=/_theme/header/    → opens header.md in the editor
GET /admin/edit/?id=/_theme/footer/    → footer.md
```

The base template includes `{% include "rendered/_theme/header.html" %}`
which is rendered from `header.md` through the standard pipeline
(or rendered live during preview via δ).

Why this is a win: PI can drop a callout block into the header, swap
the footer's social links, or move the menu without touching Jinja.

---

## 7. Menu builder — nested tree + drag-reorder

v1 nav: `[{label, url}]` flat array.
v2 nav: nested tree.

```yaml
nav:
  - label: Home
    url: /
  - label: Research
    url: /research/
    children:
      - label: Auckland
        url: /research/auckland/
      - label: Wellington
        url: /research/wellington/
      - label: …
  - label: Blog
    url: /blog/
  - label: About
    url: /davidsimmons/
```

UI: a recursive `<ul>` with drag handles. Indent / outdent buttons (or
nesting via drag-into-sibling). Inserts a new item below the dragged
position; SortableJS or a hand-rolled handler.

Validation: tree depth ≤ 3 (most nav menus collapse beyond that
visually). PI can ratify a different cap.

---

## 8. Per-page SEO panel

Frontmatter extension (typed sub-tree under a `seo:` key):

```yaml
---
title: "…"
date: 2026-04-21
seo:
  meta_description: "…"           # ≤ 155 chars; warned in UI if longer
  og:
    title: ""                      # falls back to page title
    description: ""                # falls back to summary
    image: "/static/media/.../og.jpg"
    type: article                  # article | website | book
  twitter:
    card: summary_large_image      # summary | summary_large_image
  schema_type: BlogPosting         # BlogPosting | Article | …
  canonical: ""                    # for cross-posted content
  robots: index,follow             # default; noindex,nofollow toggle
---
```

The editor exposes an **SEO** tab next to the body / frontmatter
toggle. Each field gets a typed input + character counter +
guidance. Defaults render to empty in the YAML when unset (v1
byte-preservation invariant — PI's existing frontmatter doesn't
acquire spurious empty `seo:` keys).

The renderer extends `templates/_partials/head.html` to consume
`seo.*` keys and emit the right `<meta>` / `<link>` tags. The
existing site's `head.html` is mostly there already; v2 just adds
the schema.org JSON-LD block.

---

## 9. Page-builder layouts (sections)

A **section** is a top-level directive block that consumes
full-bleed width. Three section blocks (§3.4):

- `section-hero` — large image background + headline + subhead + CTA
- `section-feature-grid` — 2 / 3 columns of feature cards
- `section-cta` — accent-colored band with headline + button

Section blocks render via dedicated Jinja partials at
`templates/blocks/section_*.html` that explicitly break out of the
page's `max-width` constraint with `width: 100vw; margin-left:
calc(50% - 50vw);` (the standard "full bleed" CSS trick).

Where this matters: the homepage (`templates/main/index.html`) and
the About page (`/davidsimmons/`) — both currently have hardcoded
hero areas. v2 lets the PI assemble these from sections without
touching the Jinja layer.

---

## 10. Featured image + excerpt for blog

Frontmatter extension:

```yaml
featured_image:
  src: /static/media/.../hero.jpg
  alt: "…"
  focal: "0.5,0.4"        # focal point for cropping (x,y in [0,1])
excerpt: "…"               # 1–2 sentence summary; falls back to first paragraph
```

The blog index page renders featured images in a card grid (instead
of the current text-only list). The featured image picker reuses the
v1 media browser modal; focal-point is a draggable target overlay on
the selected asset.

---

## 11. Tags / categories with archive pages

Current state: `tags: [travel, ...]` in blog frontmatter; no index.

v2 adds:

- `/blog/tag/<slug>/` — auto-generated archive page listing all posts
  with that tag
- `/blog/tag/` — index of all tags with post counts
- (Optional) Categories as a separate, hierarchical taxonomy:
  `/blog/category/<path>/`

A tag-management UI under `/admin/tags/` lets PI rename / merge /
delete tags. Operations rewrite frontmatter across affected posts via
the existing `apply_replaces` machinery (η).

For research corpus, theme already plays the role of category. No
change.

---

## 12. Mobile / tablet preview switcher

The editor's preview iframe gains three viewport buttons:

| Button | Width × height |
|---|---|
| Mobile | 375 × 812 |
| Tablet | 768 × 1024 |
| Desktop | 100% × 100% (current) |

CSS-only — the iframe's container `width` toggles among the three
values, with a `transform: scale(...)` if needed for fit. No content
changes; the responsive CSS in `theme.css` does the rest.

---

## 13. Analytics integration

Settings group `analytics` (new, sixth):

```yaml
analytics:
  provider: none      # none | plausible | umami | ga4
  site_id: ""         # provider-specific; e.g. domain for Plausible
  script_url: ""      # auto-derived from provider; override available
  honour_dnt: true    # respect Do-Not-Track
```

A new `templates/_partials/analytics.html` partial conditionally
emits the right `<script>` tag based on `g.site_settings.analytics`.
GA4 / Plausible / Umami all have a single-line script tag; the
partial is ~10 lines.

DNT respect is opt-in per CMS-SPEC's privacy posture (CMS-SPEC §10).

---

## 14. PI mastery surfaces in v2

Two genuine mastery surfaces are preserved (per the project's
`PI/Tool` dynamic):

1. **§3.3 — block parser** (round-trip MD ↔ block tree). The proof
   obligation $P(P^{-1}(t)) = t \land P^{-1}(P(s)) \equiv s$ has the
   same flavour as v1's `_split_frontmatter` identity but at greater
   scope. Implementing it requires:

   - A tokenizer that respects nested `:::` levels.
   - A serializer that emits canonical attribute order **only for
     attrs the editor touched**, preserving original formatting for
     untouched blocks.
   - A test corpus of hand-written directive MD files used as
     round-trip ground truth (parallel to v1's blog-post round-trip
     test).

2. **PROJECTED preview rendering** (carried over from v1). The
   `content/<region>/tools/render.py::render_leaf` refactor to take
   in-memory YAML rather than re-reading from disk. v2 makes this
   higher-leverage because corpus blocks (callouts in Problem
   statements, columns in claims) become live-previewable once
   render_leaf accepts in-memory input.

Mechanical pieces (the other 11 v2 features) are PI-completable from
the contracts in this doc.

---

## 15. Open design questions for PI

| # | Question | Recommendation |
|---|---|---|
| V2-1 | **Block parser strategy**: parse on every render (cost: ~ms per page) vs. parse-once-cache-in-cms.db (cost: cache invalidation complexity)? | Parse-on-render. v1 is already per-request. The cache savings are negligible vs. the invalidation footgun. |
| V2-2 | **Visual editor on by default for new pages**, or opt-in per page? | Opt-in via a frontmatter flag `editor: visual`. Default to source mode preserves the v1 author flow. |
| V2-3 | **Custom block registration**: PI hand-edits `_blocks/registry.yaml`, or a `/admin/blocks/` UI for adding blocks via JSON? | Hand-edit for v2; UI is v3. Adding a block is rare and structural. |
| V2-4 | **Theme presets bundled** with the codebase, or downloadable? | Bundled. Three is a small enough number to maintain in-tree. |
| V2-5 | **Template slot promotion** — promote header/footer/sidebar all in one wave, or staged? | Staged. Header + footer first (they have current content); sidebar second (currently empty). |
| V2-6 | **Tags vs categories**: ship tags only (current), or both as separate taxonomies? | Tags only for v2. Categories is a v3 wave if blog volume justifies hierarchy. |
| V2-7 | **Mobile preview**: iframe `width` only, or include a `transform: scale()` to fit a phone-sized iframe inside a desktop viewport? | `width` only. Scaling adds blur and is misleading about real-device rendering. |
| V2-8 | **Analytics defaults**: ship with `provider: none` (current behaviour), or warn the PI on first /admin/ visit if no analytics is set? | Default `none`, no warning. Privacy-positive. |
| V2-9 | **Backwards compatibility**: existing v1 pages (no blocks) work unchanged. But what about pages partially migrated to blocks — are they visual-mode by default? | Visual mode is opt-in per V2-2; partial migration shows source mode by default, PI explicitly switches to visual to author with the new editor. |
| V2-10 | **Rich-text inline (bold/italic/link) within paragraph blocks**: contenteditable with custom toolbar (re-implement Markdown bold/italic), or pass through to the existing Markdown renderer? | Pass-through. The paragraph block's body is plain Markdown; the toolbar inserts `**…**` or `[…](…)` at the cursor. No DOM rich-text engine. Preserves git diff readability. |

---

## 16. Out of scope for v2

- **Form builder** (drag-drop forms with validation rules, multi-step
  flows). The contact form stays code-level.
- **Plugin marketplace / extension system**. Custom blocks via Jinja
  partial + registry.yaml is the only extensibility seam.
- **Multi-user roles, comments, approval flows**. Single-PI assumption
  persists.
- **WYSIWYG export to non-MD formats** (ODT, DOCX, PDF). Existing
  toolchain already produces good output.
- **Shopping cart / e-commerce**. No current need.
- **AI-assisted writing in-editor** (Claude integration in the editor
  pane). A separate axis of work, intentionally orthogonal to v2.
- **i18n / translation surfaces**.
- **Custom domains / DNS management**. Cloudflare side, not Flask
  side.

---

## 17. Wave plan (proposed)

Ten v2 waves, dependency-ordered:

| Wave | What | Depends on | Duration estimate |
|---|---|---|---|
| **v2-1** | Block parser + grammar + 12 seed blocks (PI mastery: parser body) | nothing | substantive |
| **v2-2** | Visual editor partials — block cells, "+ insert" gutter, drag-reorder | v2-1 | mechanical |
| **v2-3** | Block library Jinja partials + registry | v2-1 | mechanical |
| **v2-4** | Theme presets (3) + override layer + customizer UI | nothing (parallel to v2-1) | mechanical |
| **v2-5** | Media transforms — crop, focal point, srcset | nothing (parallel) | mechanical |
| **v2-6** | Template slot promotion — header.md + footer.md + sidebar.md | nothing | mechanical |
| **v2-7** | Menu builder UI (drag-reorder, nesting) | v2-6 (header consumes nav) | mechanical |
| **v2-8** | Per-page SEO panel + extended frontmatter schema | nothing | mechanical |
| **v2-9** | Page-builder section blocks (3) | v2-1 + v2-3 | mechanical |
| **v2-10** | Featured image + excerpt + tag archive pages + analytics + mobile preview | v2-3 + v2-5 | mechanical |

After v2-10: the CMS surface is functionally peer to mid-tier
WordPress + most of Wix's editorial UX. The design integrity remaining
is the PROJECTED preview rendering (v1 carry-over) and the optional
v3 strategy-B parser for the corpus typed graph (the original v1
mastery gate).

---

## 18. Reading order for the PI

1. §0 — confirm the architectural invariants are still acceptable.
2. §1 — sanity-check the Wix/WP feature mapping; flag missing items.
3. §3 — the load-bearing design choice (directive-MD vs JSON tree).
4. §15 — ratify the ten open questions.
5. §17 — sequence the waves; pick which to schedule first.

The other sections are detail that becomes relevant per-wave.

[cm-directives]: https://talk.commonmark.org/t/generic-directives-plugins-syntax/444
