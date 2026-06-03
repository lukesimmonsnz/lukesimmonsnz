"""National (nz) blueprint — serves the Pattern rollup at /research/nz/.

Patterns are cross-regional generalisations (schema invariant P8:
manifests_in >= 2 regions). Their YAML corpus lives at
content/nz/data/pattern/; this blueprint loads and projects that corpus
for the national view.

This is NOT a RegionBlueprintFactory call. The factory (blueprints/region.py)
serves rendered Markdown pages from content/<region>/pages/. The national
view serves Pattern graph projections; different data source, different
blueprint.

URL scheme (url_prefix="/research/nz" embedded):
    /research/nz/                   — all themes, Patterns grouped by theme
    /research/nz/<theme>/           — single-theme Pattern list; 404 if none
"""

from pathlib import Path

from flask import Blueprint, abort, render_template

from content.nz.tools.query import (
    THEME_TITLES,
    load_patterns,
    patterns_by_theme,
    query_patterns,
)

nz_bp = Blueprint("nz", __name__, url_prefix="/research/nz")

_NZ_DATA_DIR = Path(__file__).resolve().parent.parent / "content" / "nz" / "data"

# Rendering threshold: minimum number of regions a Pattern must manifest in
# to appear on the national view. P8 schema floor is 2; raise once >= 3
# regions are populated. Final value is PI's decision.
_MIN_REGIONS = 2


REGION_TITLES: dict[str, str] = {
    "auckland":            "Auckland",
    "wellington":          "Wellington",
    "northland":           "Northland",
    "waikato":             "Waikato",
    "bay-of-plenty":       "Bay of Plenty",
    "gisborne":            "Gisborne",
    "hawkes-bay":          "Hawke's Bay",
    "taranaki":            "Taranaki",
    "manawatu-whanganui":  "Manawatū-Whanganui",
    "nelson":              "Nelson",
    "tasman":              "Tasman",
    "marlborough":         "Marlborough",
    "west-coast":          "West Coast",
    "canterbury":          "Canterbury",
    "otago":               "Otago",
    "southland":           "Southland",
}


@nz_bp.route("/")
def index():
    patterns = load_patterns(_NZ_DATA_DIR)
    filtered = query_patterns(patterns, min_regions=_MIN_REGIONS)
    grouped = patterns_by_theme(filtered)
    return render_template(
        "nz/index.html",
        by_theme=grouped,
        theme_titles=THEME_TITLES,
        region_titles=REGION_TITLES,
        total_pattern_count=len(filtered),
    )


@nz_bp.route("/solutions/")
def solutions():
    """Cross-pattern analytical essay on solution space for the
    structural issues observed in the regional corpus.

    Distinct from the per-theme rollup at /research/nz/<theme>/: this
    page reasons across patterns rather than within a theme. The body
    is hand-authored prose in templates/nz/solutions.html; the route
    only injects the pattern index for cross-linking.
    """
    patterns = load_patterns(_NZ_DATA_DIR)
    filtered = query_patterns(patterns, min_regions=_MIN_REGIONS)
    pattern_index: dict[str, dict] = {p["id"]: p for p in filtered}
    return render_template(
        "nz/solutions.html",
        pattern_index=pattern_index,
        theme_titles=THEME_TITLES,
        region_titles=REGION_TITLES,
    )


@nz_bp.route("/<theme>/")
def theme(theme: str):
    # D1: 404 if no patterns exist for this theme (avoids dead-end pages).
    # To switch to empty-state: remove the abort(404) and always render.
    if theme not in THEME_TITLES:
        abort(404)
    patterns = load_patterns(_NZ_DATA_DIR)
    filtered = query_patterns(patterns, theme=theme, min_regions=_MIN_REGIONS)
    if not filtered:
        abort(404)
    return render_template(
        "nz/theme.html",
        theme=theme,
        theme_title=THEME_TITLES.get(theme, theme.replace("_", " ").title()),
        patterns=filtered,
        theme_titles=THEME_TITLES,
    )
