# CMS-IMPL-WAVE-v2-8 — Per-page SEO panel + extended frontmatter schema

**Status:** design artefact — wave v2-8 of `CMS-SPEC-v2.md` §8.
**PI directive (2026-05-02):** authored in parallel; mechanical.
**Scope:** typed `seo:` frontmatter sub-tree; head.html consumption;
editor SEO tab; schema.org JSON-LD.

---

## 1. The frontmatter extension

A new typed sub-tree under the existing frontmatter `seo:` key. The
v1 base template already consumes flat `og_*` Jinja blocks (see
`templates/base.html` lines 12-21); v2 reads the typed sub-tree
instead, falling through to the v1 defaults when the sub-tree is
absent (full backward compat).

```yaml
---
title: "Auckland congestion is a tractable problem"
date: 2024-09-12
seo:
  meta_description: "Why Auckland's transport bottleneck is a planning failure, not a fundamental constraint."
  og:
    title:        ""                          # falls back to title
    description:  ""                          # falls back to meta_description
    image:        "/static/media/aa/cover.jpg"
    type:         article                     # article | website | book
  twitter:
    card:         summary_large_image         # summary | summary_large_image
  schema_type:    BlogPosting                 # BlogPosting | Article | Person | …
  canonical:      ""                          # cross-post canonical URL
  robots:         index,follow                # default; "noindex,nofollow" to hide
---
```

**Defaults render to absent keys.** PI's existing pages that don't
have a `seo:` block emit identical HTML to v1 — the v2-8 head.html
extension only emits `<meta>` tags for keys present in `seo:`. The
v1 byte-preservation invariant (CMS-SPEC §0 row 3) is honoured.

---

## 2. JSON Schema (canonical)

`content/_schema/seo.schema.json` defines the typed sub-tree. The v1
schema infrastructure validates this at lint time; the editor's SEO
tab uses it to drive form generation.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://lukesimmonsnz.kiwi/schema/seo",
  "title": "Per-page SEO frontmatter sub-tree",
  "type": "object",
  "additionalProperties": false,
  "properties": {
    "meta_description": {
      "type": "string",
      "maxLength": 320,
      "description": "Meta description; warned in UI if >155 chars."
    },
    "og": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "title":       {"type": "string", "maxLength": 70},
        "description": {"type": "string", "maxLength": 200},
        "image":       {"type": "string", "format": "uri-reference"},
        "type":        {"enum": ["article", "website", "book", "profile"]}
      }
    },
    "twitter": {
      "type": "object",
      "additionalProperties": false,
      "properties": {
        "card": {"enum": ["summary", "summary_large_image"]}
      }
    },
    "schema_type": {
      "enum": ["BlogPosting", "Article", "WebPage", "Person", "ResearchProject", "TechArticle"]
    },
    "canonical": {"type": "string", "format": "uri-reference"},
    "robots":    {"type": "string", "pattern": "^(index|noindex)(,\\s*(follow|nofollow))?$"}
  }
}
```

`maxLength` warnings (155 for meta_description, 70 for og.title, 200
for og.description) are SEO-best-practice character counts; the
schema's `maxLength` is intentionally looser (320, 70, 200) — exact
limits are warned at the editor / lint layer, not rejected by the
schema. PI may tighten if desired.

---

## 3. head.html partial extension

Currently `templates/base.html` lines 9-21 hardcode og:* and twitter:*.
Refactor to read from the typed sub-tree, with fall-through to existing
Jinja blocks for backward compat:

```jinja
{# templates/_partials/head.html — NEW; replaces inline head in base.html #}
<meta name="description" content="{{ seo.meta_description or self.meta_description() }}">
<title>{% block title %}{{ site_name }}{% endblock %}</title>

<meta property="og:site_name"   content="{{ site_name }}">
<meta property="og:type"        content="{{ seo.og.type or self.og_type() }}">
<meta property="og:title"       content="{{ seo.og.title or self.og_title() }}">
<meta property="og:description" content="{{ seo.og.description or self.og_description() }}">
<meta property="og:url"         content="{{ site_url }}{{ request.path }}">
<meta property="og:image"       content="{{ seo.og.image or self.og_image() }}">

<meta name="twitter:card"        content="{{ seo.twitter.card or 'summary_large_image' }}">
<meta name="twitter:title"       content="{{ seo.og.title or self.og_title() }}">
<meta name="twitter:description" content="{{ seo.og.description or self.og_description() }}">
<meta name="twitter:image"       content="{{ seo.og.image or self.og_image() }}">

<link rel="canonical" href="{{ seo.canonical or (site_url ~ request.path) }}">

{% if seo.robots %}<meta name="robots" content="{{ seo.robots }}">{% endif %}

{% if seo.schema_type %}
<script type="application/ld+json">
{{ jsonld(seo, request.path, site_url, site_name) | safe }}
</script>
{% endif %}
```

The `seo` Jinja variable is injected by a context processor that
extracts the parsed frontmatter's `seo:` sub-tree (or an empty
`SeoView` namespace for pages without one — so `seo.og.title` is
always safe to access without `is defined` guards).

---

## 4. The `SeoView` namespace + context processor

```python
# blueprints/admin/cms/seo.py — NEW

from dataclasses import dataclass
from typing import Any
import json

@dataclass(frozen=True)
class _OgView:
    title:       str = ""
    description: str = ""
    image:       str = ""
    type:        str = ""


@dataclass(frozen=True)
class _TwitterView:
    card: str = ""


@dataclass(frozen=True)
class SeoView:
    meta_description: str         = ""
    og:               _OgView     = _OgView()
    twitter:          _TwitterView = _TwitterView()
    schema_type:      str         = ""
    canonical:        str         = ""
    robots:           str         = ""

    @classmethod
    def from_frontmatter(cls, fm: dict | None) -> "SeoView":
        if not fm or "seo" not in fm:
            return cls()
        s = fm["seo"]
        return cls(
            meta_description = s.get("meta_description", ""),
            og               = _OgView(**(s.get("og") or {})),
            twitter          = _TwitterView(**(s.get("twitter") or {})),
            schema_type      = s.get("schema_type", ""),
            canonical        = s.get("canonical", ""),
            robots           = s.get("robots", ""),
        )


def jsonld(seo: SeoView, path: str, site_url: str, site_name: str) -> str:
    """Emit a schema.org JSON-LD blob for the given seo + page metadata.

    Returned as a JSON string (the head.html partial wraps it in a
    <script type="application/ld+json"> tag).
    """
    ...   # PI fills body — straightforward dict-build → json.dumps
```

The Jinja context processor injects `seo` and the `jsonld` filter on
every request. Pages that don't pass frontmatter through the request
context (most of v1's blueprint routes) get the empty `SeoView`.

---

## 5. Editor SEO tab

The editor (templates/admin/cms/editor.html) currently has two panes:
body and frontmatter. v2-8 adds a third tab — **SEO** — that drives a
form from the seo.schema.json structure:

```
[ Body ] [ Frontmatter ] [ SEO ]

  Meta description ··················· (155 char counter)
  ────────────────
  Open Graph
  ├── Title ········· (70 char counter; falls back to page title if blank)
  ├── Description ··· (200 char counter)
  ├── Image ········· [pick from media library]
  └── Type ·········· [article | website | book | profile] (radio)

  Twitter
  └── Card ·········· [summary | summary_large_image] (radio)

  schema.org type ····· [BlogPosting | Article | WebPage | …] (dropdown)
  Canonical URL ······· (text)
  Robots ·············· [index,follow | noindex,nofollow] (radio)
```

On save, the form values are spliced into the frontmatter under the
`seo:` key. The byte-preservation invariant: editing only SEO fields
never perturbs the body, and only modifies the `seo:` sub-tree of
frontmatter — keys outside `seo:` retain their byte order, quoting,
and list style.

This is achieved by a focused merge: parse the existing frontmatter
to a dict, write the new `seo:` value, and re-serialise via PyYAML
**only the seo sub-tree**, then splice that fragment into the original
raw frontmatter text at the position of an existing `seo:` block (or
append at the end if absent). The rest of the frontmatter remains
verbatim.

```python
# blueprints/admin/cms/seo.py — continued

def splice_seo_into_frontmatter(raw_fm: str, new_seo: dict) -> str:
    """Splice a new `seo:` sub-tree into raw frontmatter text without
    perturbing other keys' byte order / quoting / list style.

    Locality property:

        For every key k != 'seo' in raw_fm, the bytes contributed by k
        to the output equal the bytes contributed by k in raw_fm.

    PI mastery is NOT introduced here — the splice is mechanical, but
    the test for locality is non-trivial. See test_seo_splice.py.
    """
    ...   # PI fills body — locate `^seo:` block, replace its byte range
```

---

## 6. Module + template layout

```
blueprints/admin/cms/seo.py            — NEW: SeoView, jsonld, splice
content/_schema/seo.schema.json        — NEW: canonical schema
templates/_partials/head.html          — NEW: extracted from base.html
templates/base.html                    — DELTA: include head.html partial
templates/admin/cms/editor.html        — DELTA: SEO tab
app.py                                 — DELTA: context processor for `seo`
```

---

## 7. Verification gate

1. `python -m json.tool < content/_schema/seo.schema.json` parses (no
   tail corruption).
2. A v1 blog post (no `seo:` in frontmatter) renders identical
   `<head>` HTML before and after the wave — verify by diffing the
   rendered HTML byte-by-byte.
3. Adding a `seo:` block with `meta_description` and `og.image` to a
   blog post and re-rendering: only those two `<meta>` tags change in
   the output; canonical / og:url / twitter:card stay default.
4. Editor's SEO tab generates a form matching the schema; saving
   splices into frontmatter byte-preservingly (unrelated keys' bytes
   unchanged on round-trip).
5. JSON-LD: a post with `schema_type: BlogPosting` emits a valid
   schema.org blob — verify with `json.loads(...)` plus a property
   spot-check (`@type == "BlogPosting"`, `headline == title`,
   `datePublished` present).

---

## 8. Out of scope

- Sitemap.xml extension to consume `seo.canonical` for rel-canonical
  per-URL (already largely correct; v3 if needed).
- Per-page social-card image generation (Open Graph image rendered
  on-demand from page title + tagline). v3 candidate.
- Programmatic SEO audits / lighthouse integration.
- AMP / structured-data validators in CI.
