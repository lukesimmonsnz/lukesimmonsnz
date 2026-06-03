---
name: Consolidated-mode template guard pattern
description: When seeding `_sections/<theme>.md` for a region, the public `templates/<region>/section.html` MUST handle both consolidated and legacy modes.
type: feedback
---

When v3-5 bulk-seeded 165 region section MDs to make them editable, all 15
non-Auckland regions started returning HTTP 500 because `region.py` flips
`consolidated_mode = sections_dir.is_dir()` to True as soon as the
directory exists, but their section.html templates still iterate `{% for p
in pages %}` (which is None in consolidated mode). Auckland's template
already had the right `{% if consolidated %}...{% else %}...{% endif %}`
guard.

**Why:** the consolidated-mode flag in `blueprints/region.py` is computed
from filesystem state (`sections_dir.is_dir()`), not from per-region
configuration. Adding any file under `content/<region>/pages/_sections/`
flips the region into consolidated mode for ALL its theme URLs.

**How to apply:** if a future wave adds region-level section MDs, FIRST
verify each region's section.html template has the consolidated guard.
The pattern (from Auckland) is:

```
{% if consolidated %}
  <article class="prose section-essay">{{ consolidated.body_html | safe }}</article>
{% else %}
  <article class="prose">{% for p in pages or [] %}...{% endfor %}</article>
{% endif %}
```

The `or []` matters — the legacy path passes `pages` undefined when there
are no leaves under that theme.
