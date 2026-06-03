"""Wellington research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name wellington_bp.

URL scheme (served from app.py via register_blueprint):
    /research/wellington/
    /research/wellington/<section>/
    /research/wellington/<section>/<subpage>/
"""

from blueprints.region import make_region_blueprint

SECTION_TITLES: dict[str, str] = {
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
    "climate": "Sea level rise, the Wellington Fault, coastal hazard, and adaptation for the harbour-bowl capital.",
    "crime": "Family violence, methamphetamine harm, and the policing of central Wellington's hospitality precinct.",
    "economy": "Public-sector concentration, central-government employment, and Wellington's productivity profile.",
    "education": "Tertiary access via Victoria University, school zoning, and lifelong learning across the Wellington region.",
    "environment": "Wellington Harbour, Cook Strait fisheries, biodiversity, and freshwater in the capital region.",
    "governance": "Wellington City Council, the GWRC, central–local relations, and Three Waters reform.",
    "health": "Wellington Regional Hospital capacity, the nurse workforce, mental health, and primary care access.",
    "housing": "Affordability, supply, social and emergency housing, and the rental market in Te Whanganui-a-Tara.",
    "inequality": "Income, wealth, suburban disparity (Hutt vs central), and the structural drivers of Wellington inequality.",
    "infrastructure": "Three waters, rail and road tunnel resilience, energy, and digital connectivity in the harbour bowl.",
    "transport": "Rail patronage, the Mt Victoria and Terrace tunnels, motorway capacity, and active modes across Wellington.",
}

wellington_bp = make_region_blueprint(
    "wellington",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
