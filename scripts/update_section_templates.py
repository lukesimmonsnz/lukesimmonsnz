"""
Replace the if-consolidated/else-pages branch in each region's section.html
with a uniform "optional intro + leaf cards" structure.

Each region's section.html keeps its region-specific breadcrumbs (we only
patch the inner content branch). Leaf URLs are constructed via
url_for(request.blueprint ~ '.page', ...) so no per-region hardcoding.
"""

from __future__ import annotations
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REGIONS = [
    "auckland", "wellington", "northland", "waikato", "bay-of-plenty",
    "gisborne", "hawkes-bay", "taranaki", "manawatu-whanganui", "nelson",
    "tasman", "marlborough", "west-coast", "canterbury", "otago", "southland",
]

# New body block — replaces the if/else block.
NEW_BODY = """  <header class="page-header">
    <span class="eyebrow">Section</span>
    <h1>{{ section_title }}</h1>
    <hr class="rule">
  </header>

  {% if consolidated and consolidated.body_html and consolidated.body_html|striptags|trim %}
  <article class="prose section-intro">
    {{ consolidated.body_html | safe }}
  </article>
  {% endif %}

  {% if pages %}
  <section>
    <ul class="leaf-list">
      {% for p in pages %}
      <li class="leaf-list-item">
        <a class="leaf-title" href="{{ url_for(request.blueprint ~ '.page', section=p.section, subpage=p.subpage) }}">
          {{ p.title }}
        </a>
        {% if p.summary %}
        <p class="leaf-summary">{{ p.summary }}</p>
        {% endif %}
      </li>
      {% endfor %}
    </ul>
  </section>
  {% endif %}"""

# Match everything from the first `<header class="page-header">` to the
# closing `</article>` that ends the legacy branch (whichever comes last
# before the closing </div> of the .page wrapper).
# Strategy: match from `<header class="page-header">` to `</article>` and
# then any whitespace, where the matched content contains either
# {% if consolidated %} or {% else %} or both.
PATTERN = re.compile(
    r'<header class="page-header">.*?</article>\s*(?:\{%\s*endif\s*%\})?',
    re.DOTALL,
)


def update(region: str) -> None:
    path = ROOT / "templates" / region / "section.html"
    text = path.read_text(encoding="utf-8")

    new_text, n = PATTERN.subn(NEW_BODY, text, count=1)
    if n != 1:
        # The template might have more than one </article> — try a more
        # specific match that handles both branches.
        # Fall back: match the entire {% if consolidated %}...{% endif %}
        # along with the surrounding page-header.
        alt = re.compile(
            r'(?:<header class="page-header">.*?</header>\s*)?'
            r'\{%\s*if\s+consolidated\s*%\}.*?\{%\s*endif\s*%\}',
            re.DOTALL,
        )
        new_text, n = alt.subn(NEW_BODY, text, count=1)
        if n != 1:
            raise RuntimeError(f"Could not update {path}: no match")

    path.write_text(new_text, encoding="utf-8")
    print(f"  updated: {path.relative_to(ROOT)}")


def main():
    for r in REGIONS:
        update(r)
    print(f"\nDone. {len(REGIONS)} section templates updated.")


if __name__ == "__main__":
    main()
