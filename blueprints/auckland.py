"""Auckland blueprint — serves the generated pages under content/auckland/pages/.

Pages are generated from typed entity YAML under content/auckland/data/ by the
render pipeline at content/auckland/tools/render.py. This blueprint is a pure
reader: it does not generate or edit pages. To refresh a page, run the
renderer and commit both the entity data and the regenerated Markdown.

URL scheme:
    /auckland/                        — index of all sections and subpages
    /auckland/<section>/              — section hub (subpages listed by order)
    /auckland/<section>/<subpage>/    — individual rendered page
"""

from datetime import date as _date, datetime
from pathlib import Path

import frontmatter
import markdown
from flask import Blueprint, abort, render_template

auckland_bp = Blueprint("auckland", __name__)

PAGES_DIR = Path(__file__).resolve().parent.parent / "content" / "auckland" / "pages"

# Display titles for the section slugs used in the entity model.
# Extend this map as new sections are added.
SECTION_TITLES: dict[str, str] = {
    "framing": "Framing",
    "housing": "Housing",
    "transport": "Transport",
    "infrastructure": "Infrastructure",
    "environment": "Environment",
    "inequality": "Inequality",
    "crime": "Crime & safety",
    "health": "Health",
    "education": "Education",
    "economy": "Economy",
    "governance": "Governance",
    "climate": "Climate adaptation",
}


def _markdown():
    # Fresh converter per call — Markdown's reset is not threadsafe.
    return markdown.Markdown(
        extensions=["extra", "codehilite", "sane_lists", "smarty"],
        output_format="html5",
    )


def _format_date(value):
    if isinstance(value, datetime):
        value = value.date()
    if isinstance(value, _date):
        return value.strftime("%d %B %Y").lstrip("0")
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value).date().strftime("%d %B %Y").lstrip("0")
        except ValueError:
            return value
    return ""


def _load_page(path: Path) -> dict:
    fm = frontmatter.load(path)
    meta = fm.metadata or {}
    body_html = _markdown().convert(fm.content)
    section = str(meta.get("section") or path.parent.name)
    subpage = str(meta.get("subpage") or path.stem)
    return {
        "section": section,
        "section_title": SECTION_TITLES.get(section, section.replace("_", " ").title()),
        "subpage": subpage,
        "title": meta.get("title") or subpage.replace("-", " ").title(),
        "summary": (meta.get("summary") or "").strip(),
        "order": meta.get("order") if isinstance(meta.get("order"), int) else 99,
        "updated_raw": meta.get("updated"),
        "updated_display": _format_date(meta.get("updated")),
        "status": meta.get("status"),
        "generated_from": meta.get("generated_from"),
        "body_html": body_html,
    }


def _all_pages() -> list[dict]:
    if not PAGES_DIR.exists():
        return []
    pages = [_load_page(p) for p in PAGES_DIR.rglob("*.md")]
    pages.sort(key=lambda p: (p["section"], p["order"], p["subpage"]))
    return pages


def _pages_by_section() -> dict[str, list[dict]]:
    by_section: dict[str, list[dict]] = {}
    for page in _all_pages():
        by_section.setdefault(page["section"], []).append(page)
    return by_section


@auckland_bp.route("/")
def index():
    by_section = _pages_by_section()
    return render_template(
        "auckland/index.html",
        by_section=by_section,
        section_titles=SECTION_TITLES,
    )


@auckland_bp.route("/<section>/")
def section(section: str):
    by_section = _pages_by_section()
    if section not in by_section:
        abort(404)
    return render_template(
        "auckland/section.html",
        section=section,
        section_title=SECTION_TITLES.get(section, section.replace("_", " ").title()),
        pages=by_section[section],
    )


@auckland_bp.route("/<section>/<subpage>/")
def page(section: str, subpage: str):
    path = PAGES_DIR / section / f"{subpage}.md"
    if not path.is_file():
        abort(404)
    current = _load_page(path)

    siblings = sorted(
        (p for p in _all_pages() if p["section"] == section),
        key=lambda p: (p["order"], p["subpage"]),
    )
    idx = next(
        (i for i, p in enumerate(siblings) if p["subpage"] == subpage),
        None,
    )
    prev_page = siblings[idx - 1] if idx is not None and idx > 0 else None
    next_page = (
        siblings[idx + 1] if idx is not None and idx + 1 < len(siblings) else None
    )

    return render_template(
        "auckland/page.html",
        page=current,
        section=section,
        section_title=SECTION_TITLES.get(section, section.replace("_", " ").title()),
        prev_page=prev_page,
        next_page=next_page,
    )
