"""Pattern rollup query functions for the national (nz) view.

Patterns are the only entity type defined as cross-regional by schema invariant
P8 (manifests_in ≥ 2 regions). They live in content/nz/data/pattern/ — the
national namespace — rather than in any single region's data/ directory.

This module is the single query interface between the Flask nz blueprint and
the Pattern YAML corpus. It deliberately does not import Pydantic or Flask;
the blueprint owns the HTTP layer, invariants.py owns validation, this module
owns data loading and query logic.

Usage (from the nz blueprint)::

    from content.nz.tools.query import load_patterns, query_patterns, patterns_by_theme

    _patterns = load_patterns(_NZ_DATA_DIR)
    grouped   = patterns_by_theme(query_patterns(_patterns, min_regions=2))
"""

from __future__ import annotations

from pathlib import Path

import yaml


# ---------------------------------------------------------------------------
# Canonical theme display titles.
# Themes are a shared enum across all regions (SCHEMA-DESIGN §1; ~11 entries).
# When Auckland is rebuilt against content/_schema/, its SECTION_TITLES should
# reference this dict rather than redeclare it. For now, declared here.
# ---------------------------------------------------------------------------

THEME_TITLES: dict[str, str] = {
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


# ---------------------------------------------------------------------------
# Loader
# ---------------------------------------------------------------------------

def load_patterns(data_dir: Path) -> list[dict]:
    """Load all Pattern YAML files from ``data_dir/pattern/``.

    Returns an empty list if the directory does not exist or contains no
    ``*.yaml`` files — the blueprint renders an empty-corpus state gracefully.

    Does NOT validate against JSON Schema; that is lint's responsibility.
    Malformed YAML that fails ``yaml.safe_load`` is silently skipped (parse
    error logged to stderr) so a single bad file does not break the live site.
    """
    pattern_dir = data_dir / "pattern"
    if not pattern_dir.is_dir():
        return []

    results: list[dict] = []
    for path in sorted(pattern_dir.glob("*.yaml")):
        try:
            with path.open("r", encoding="utf-8") as fh:
                data = yaml.safe_load(fh)
            if isinstance(data, dict) and "id" in data:
                results.append(data)
            else:
                import sys
                print(f"query.py: skipping {path} — not a mapping or missing 'id'", file=sys.stderr)
        except yaml.YAMLError as exc:
            import sys
            print(f"query.py: YAML error in {path}: {exc}", file=sys.stderr)

    return results


# ---------------------------------------------------------------------------
# Query
# ---------------------------------------------------------------------------

def query_patterns(
    patterns: list[dict],
    *,
    theme: str | None = None,
    min_regions: int = 2,
) -> list[dict]:
    """Filter and sort a pattern list.

    Parameters
    ----------
    patterns:
        Raw list as returned by ``load_patterns``.
    theme:
        If given, restrict to patterns whose ``theme`` field matches this slug
        exactly. Pass ``None`` to include all themes.
    min_regions:
        Minimum ``len(manifests_in)`` for a pattern to appear. P8 schema
        minimum is 2. The rendering layer may raise this threshold once ≥ 3
        regions are populated; the default here is the schema floor.

    Returns
    -------
    Filtered list, sorted by ``(theme, -evidence_count, id)`` for stable
    rendering across builds.
    """
    results = []
    for p in patterns:
        manifests_in = p.get("manifests_in") or []
        if not isinstance(manifests_in, list):
            continue
        if len(manifests_in) < min_regions:
            continue
        if theme is not None and p.get("theme") != theme:
            continue
        results.append(p)

    results.sort(
        key=lambda p: (
            p.get("theme") or "",
            -(len(p.get("evidenced_by") or [])),
            p.get("id") or "",
        )
    )
    return results


# ---------------------------------------------------------------------------
# Grouping
# ---------------------------------------------------------------------------

def patterns_by_theme(patterns: list[dict]) -> dict[str, list[dict]]:
    """Group a (pre-filtered) pattern list by theme slug.

    Returns an ordered dict with themes in THEME_TITLES canonical order;
    themes present in data but absent from THEME_TITLES appear at the end,
    sorted alphabetically.

    Each pattern dict is augmented with a ``theme_title`` key for direct
    template use (avoids a template-level dict lookup).
    """
    by_theme: dict[str, list[dict]] = {}
    for p in patterns:
        slug = p.get("theme") or "unknown"
        p_annotated = dict(p)
        p_annotated["theme_title"] = THEME_TITLES.get(slug, slug.replace("_", " ").title())
        by_theme.setdefault(slug, []).append(p_annotated)

    # Canonical theme order first, then any extras alphabetically.
    ordered: dict[str, list[dict]] = {}
    for slug in THEME_TITLES:
        if slug in by_theme:
            ordered[slug] = by_theme[slug]
    for slug in sorted(by_theme):
        if slug not in ordered:
            ordered[slug] = by_theme[slug]

    return ordered
