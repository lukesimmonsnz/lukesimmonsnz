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
    section_blurbs: dict[str, str] | None = None,
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
    sections_dir = pages_dir / "_sections"

    # Auto-detect "consolidated" mode: if pages/_sections/ exists, the region
    # serves one consolidated essay per theme and individual leaf URLs 404.
    # Otherwise the legacy per-leaf routing applies.
    consolidated_mode = sections_dir.is_dir()

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
        # Skip any path containing an underscore-prefixed directory or filename
        # (convention: _sections/, _all.md, etc. are internal aggregations,
        # not user-facing leaves).
        pages = [
            _load_page(p) for p in pages_dir.rglob("*.md")
            if not any(
                part.startswith("_") for part in p.relative_to(pages_dir).parts
            )
        ]
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
            section_blurbs=section_blurbs or {},
        )


    def _section_neighbours(current: str) -> tuple[dict | None, dict | None]:
        """Compute prev/next navigable sections, in alphabetical slug order.

        Matches the alphabetical order that the region index renders (which
        comes from _pages_by_section()). The 'framing' section is excluded.
        Returns dicts with keys 'slug' and 'title', or None at the ends.
        """
        ordered = sorted(
            (
                (slug, title)
                for slug, title in section_titles.items()
                if slug != "framing"
            ),
            key=lambda pair: pair[0],
        )
        try:
            idx = next(i for i, (slug, _) in enumerate(ordered) if slug == current)
        except StopIteration:
            return (None, None)
        prev_pair = ordered[idx - 1] if idx > 0 else None
        next_pair = ordered[idx + 1] if idx + 1 < len(ordered) else None
        prev_section = (
            {"slug": prev_pair[0], "title": prev_pair[1]} if prev_pair else None
        )
        next_section = (
            {"slug": next_pair[0], "title": next_pair[1]} if next_pair else None
        )
        return (prev_section, next_section)

    @bp.route("/<section>/")
    def section(section: str):
        prev_section, next_section = _section_neighbours(section)
        by_section = _pages_by_section()
        section_pages = by_section.get(section, [])

        # Optional consolidated intro essay (pages/_sections/<section>.md).
        # Now used as a *header* over the leaf list, not a replacement for it,
        # so that leaves are always reachable. If neither the consolidated
        # essay nor any leaves exist for this section, 404.
        consolidated = None
        if consolidated_mode:
            consolidated_path = sections_dir / f"{section}.md"
            if consolidated_path.is_file():
                consolidated = _load_page(consolidated_path)
        if not consolidated and not section_pages:
            abort(404)

        return render_template(
            f"{tmpl}/section.html",
            section=section,
            section_title=section_titles.get(
                section, section.replace("_", " ").title()
            ),
            consolidated=consolidated,
            pages=section_pages,
            prev_section=prev_section,
            next_section=next_section,
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
