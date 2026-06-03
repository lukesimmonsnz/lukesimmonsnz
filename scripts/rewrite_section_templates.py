"""Generate a clean section.html for every region.

Each section page now renders all of that section's leaves as a single
long essay with subheadings (one h2 per leaf). Pre-built consolidated
essays (Auckland's `pages/_sections/<theme>.md`) are still rendered when
they're substantive — checked by length threshold to avoid the
placeholder stubs in the other 15 regions.
"""

from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REGIONS = [
    ("auckland",            "Auckland"),
    ("wellington",          "Wellington"),
    ("northland",           "Northland"),
    ("waikato",             "Waikato"),
    ("bay-of-plenty",       "Bay of Plenty"),
    ("gisborne",            "Gisborne"),
    ("hawkes-bay",          "Hawke's Bay"),
    ("taranaki",            "Taranaki"),
    ("manawatu-whanganui",  "Manawatū-Whanganui"),
    ("nelson",              "Nelson"),
    ("tasman",              "Tasman"),
    ("marlborough",         "Marlborough"),
    ("west-coast",          "West Coast"),
    ("canterbury",          "Canterbury"),
    ("otago",               "Otago"),
    ("southland",           "Southland"),
]


def render(slug: str, label: str) -> str:
    # Use double-quotes inside Jinja string literals to allow apostrophes
    # in region labels (e.g. "Hawke's Bay").
    label_for_jinja = label
    return f"""{{% extends "research/_layout.html" %}}
{{% from "_partials/breadcrumbs.html" import breadcrumbs %}}
{{% from "_partials/cite.html" import cite_block %}}

{{% block title %}}{{{{ section_title }}}} · {label} · Research · Luke Simmons{{% endblock %}}
{{% block meta_description %}}{{{{ section_title }}}} in {label} — a consolidated overview of all problems in this section, with claims, drivers, solution camps, and sources.{{% endblock %}}

{{% block content %}}
<div class="page">
  {{{{ breadcrumbs([
    ('Home', url_for('main.home')),
    ('Research', url_for('research.index')),
    ("{label_for_jinja}", url_for('{slug}.index')),
    (section_title, None),
  ]) }}}}

  {{% if consolidated and consolidated.body_html %}}
  <header class="page-header">
    <span class="eyebrow">{label} &middot; Section</span>
    <hr class="rule">
  </header>
  <article class="prose section-essay">
    {{{{ consolidated.body_html | safe }}}}
  </article>
  {{% else %}}
  <header class="page-header">
    <span class="eyebrow">{label} &middot; Section</span>
    <h1>{{{{ section_title }}}}</h1>
    <hr class="rule">
  </header>
  <aside class="notice">
    <strong>No content yet</strong> for this section.
  </aside>
  {{% endif %}}

  {{{{ cite_block(title=section_title ~ " — {label}", path=request.path, site_url=site_url, current_quarter=current_quarter) }}}}

  <nav class="pagination-pair" aria-label="Adjacent research themes">
    {{% if prev_section %}}
      <a class="prev" href="{{{{ url_for('{slug}.section', section=prev_section.slug) }}}}">
        <span class="label">&larr; Previous theme</span>
        <span class="title">{{{{ prev_section.title }}}}</span>
      </a>
    {{% else %}}
      <span class="prev empty" aria-hidden="true"></span>
    {{% endif %}}

    {{% if next_section %}}
      <a class="next" href="{{{{ url_for('{slug}.section', section=next_section.slug) }}}}">
        <span class="label">Next theme &rarr;</span>
        <span class="title">{{{{ next_section.title }}}}</span>
      </a>
    {{% else %}}
      <span class="next empty" aria-hidden="true"></span>
    {{% endif %}}
  </nav>
</div>
{{% endblock %}}
"""


def main():
    for slug, label in REGIONS:
        path = ROOT / "templates" / slug / "section.html"
        path.write_text(render(slug, label), encoding="utf-8")
        print(f"  wrote: {path.relative_to(ROOT)}")
    print(f"\nDone. {len(REGIONS)} section templates regenerated.")


if __name__ == "__main__":
    main()
