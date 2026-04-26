"""Auckland research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES and registers the blueprint under the canonical name auckland_bp.

URL scheme (served from app.py via register_blueprint):
    /research/auckland/
    /research/auckland/<section>/
    /research/auckland/<section>/<subpage>/
"""

from blueprints.region import make_region_blueprint

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

auckland_bp = make_region_blueprint("auckland", SECTION_TITLES)
