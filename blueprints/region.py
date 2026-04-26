"""RegionBlueprintFactory — produces a Flask Blueprint for any research region.

Each region has its own typed entity graph under content/<region>/ and its own
set of theme sections. This factory encapsulates all routing and page-loading
logic so that adding a new region requires only:

    1. A content/<region>/pages/ directory populated by the render pipeline.
    2. A SECTION_TITLES dict for that region.
    3. A one-line call to make_region_blueprint() in blueprints/<region>.py.
    4. A register_blueprint() call in app.py.

URL scheme produced (per CLAUDE.md §5 row 1):
    /research/<region>/                          — index
    /research/<region>/<theme>/                  — theme hub
    /research/<region>/<theme>/<subpage>/        — individual page

Templates are resolved under templates/<template_prefix>/ (defaults to the
region slug). Auckland retains its existing templates/auckland/ tree unchanged.

Gate guarantee: make_region_blueprint("auckland", AUCKLAND_SECTION_TITLES)
produces routes that are byte-identical to the pre-refactor auckland_bp.
"""

from datetime import date as _date, datetime
from pathlib import Path

import frontmatter
import markdown
from flask import Blueprint, abort, render_template

# Resolved once at import; all per-region PAGES_DIR values derive from this.
_ROOT = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------------
# Module-level utilities — no region-specific state
# ---------------------------------------------------------------------------

def _markdown():
    """Fresh Markdown converter per call (not thread-safe to reuse)."""
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


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def make_region_blueprint(
    region: str,
    section_titles: dict[str, str],
    *,
    template_prefix: str | None = None,
) -> Blueprint:
    """Return a Flask Blueprint serving the research pages for *region*.

    Parameters
    ----------
    region:
        Lowercase slug, e.g. ``"auckland"``.  Drives the Blueprint name,
        ``url_prefix`` (``/research/<region>``), and the ``PAGES_DIR``
        path (``content/<region>/pages/``).
    section_titles:
        Mapping of section slug → display title, e.g.
        ``{"housing": "Housing", "climate": "Climate adaptation"}``.
        Region-specific; supplied by the caller so the factory itself
        remains filesystem-agnostic and unit-testable.
    template_prefix:
        Directory under ``templates/`` that holds this region's
        ``index.html``, ``section.html``, and ``page.html``.  Defaults
        to *region* when ``None``, so Auckland resolves to
        ``"auckland"`` and its existing templates are used unchanged.
    """

    tmpl = template_prefix if template_prefix is not None else region
    pages_dir = _ROOT / "content" / region / "pages"

    bp = Blueprint(region, __name__, url_prefix=f"/research/{region}")

    # ------------------------------------------------------------------
    # Private helpers — closures over pages_dir and section_titles
    # ------------------------------------------------------------------

    def _load_page(path: Path) -> dict:
        fm = frontmatter.load(path)
        meta = fm.metadata or {}
        body_html = _markdown().convert(fm.content)
        section = str(meta.get("section") or path.parent.name)
        subpage = str(meta.get("subpage") or path.stem)
        return {
            "section": section,
            "section_title": section_titles.get(
                section, section.replace("_", " ").title()
            ),
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
        if not pages_dir.exists():
            return []
        pages = [_load_page(p) for p in pages_dir.rglob("*.md")]
        pages.sort(key=lambda p: (p["section"], p["order"], p["subpage"]))
        return pages

    def _pages_by_section() -> dict[str, list[dict]]:
        by_section: dict[str, list[dict]] = {}
        for page in _all_pages():
            by_section.setdefault(page["section"], []).append(page)
        return by_section

    # ------------------------------------------------------------------
    # Routes
    # ------------------------------------------------------------------

    @bp.route("/")
    def index():
        by_section = _pages_by_section()
        return render_template(
            f"{tmpl}/index.html",
            by_section=by_section,
            section_titles=section_titles,
        )

    @bp.route("/<section>/")
    def section(section: str):
        by_section = _pages_by_section()
        if section not in by_section:
            abort(404)
        return render_template(
            f"{tmpl}/section.html",
            section=section,
            section_title=section_titles.get(section, section.replace("_", " ").title()),
            pages=by_section[section],
        )

    @bp.route("/<section>/<subpage>/")
    def page(section: str, subpage: str):
        path = pages_dir / section / f"{subpage}.md"
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
            f"{tmpl}/page.html",
            page=current,
            section=section,
            section_title=section_titles.get(
                section, section.replace("_", " ").title()
            ),
            prev_page=prev_page,
            next_page=next_page,
        )

    return bp
