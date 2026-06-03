"""Auckland research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name auckland_bp.

URL scheme (served from app.py via register_blueprint):
    /research/auckland/
    /research/auckland/all/                — single-page "view all" essay
    /research/auckland/<section>/
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

# One-sentence summaries shown under each theme link on the region index.
# First-pass drafts; edit freely.
SECTION_BLURBS: dict[str, str] = {
    "climate": "Sea level rise, urban heat, flooding, and the decarbonisation transition for New Zealand's largest city.",
    "crime": "Family violence, youth offending, retail crime, and the policing of inequality in Auckland.",
    "economy": "Productivity, jobs, the labour market, and the structural makeup of the Auckland economy.",
    "education": "School funding, attainment gaps, the tertiary pipeline, and lifelong learning in Auckland.",
    "environment": "Freshwater, marine, biodiversity, and waste in the Auckland region.",
    "governance": "Council structure, central-local relations, Treaty governance, and democratic participation.",
    "health": "Hospital capacity, primary care access, mental health, and the health workforce in Auckland.",
    "housing": "Affordability, supply, social and emergency housing, and the rental market in Tāmaki Makaurau.",
    "inequality": "Income, wealth, regional disparity, and the structural drivers of Auckland inequality.",
    "infrastructure": "Water, energy, digital connectivity, and the resilience of Auckland's lifeline systems.",
    "transport": "Car dependency, congestion, public transport investment, and active modes across the Auckland region.",
}

auckland_bp = make_region_blueprint(
    "auckland",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
