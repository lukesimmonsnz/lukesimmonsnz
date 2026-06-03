"""Southland — Murihiku research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name southland_bp.
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
    "climate": "Coastal hazard, Fiordland's wet climate, and adaptation in Murihiku.",
    "crime": "Family violence, methamphetamine harm, and rural policing in Southland.",
    "economy": "Tiwai Point smelter (~1,000 jobs, ~13% of NZ electricity, contract to 2026), Fonterra Edendale, Bluff oysters, Fiordland tourism (~700K visitors).",
    "education": "Southern Institute of Technology, school engagement, and tertiary reach.",
    "environment": "Fiordland (UNESCO), freshwater, biodiversity, and the agricultural impact.",
    "governance": "Southland Regional, the Invercargill / Southland District councils, and Treaty (Ngāi Tahu).",
    "health": "Southland Hospital (Invercargill), the GP shortage, mental health, and rural reach.",
    "housing": "Invercargill affordability, rural housing, and the post-Tiwai contingency.",
    "inequality": "Population retention, post-Tiwai uncertainty, and structural drivers.",
    "infrastructure": "Manapouri 850 MW (Tiwai dependency), three waters, and Bluff Port.",
    "transport": "The SH1 spine, Bluff Port, and Stewart Island ferry connectivity.",
}

southland_bp = make_region_blueprint(
    "southland",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
