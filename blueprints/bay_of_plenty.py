"""Bay of Plenty — Te Moana-a-Toi research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name bay_of_plenty_bp.
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
    "climate": "Coastal hazard for Tauranga, kiwifruit and orchard climate exposure, and adaptation in Te Moana-a-Toi.",
    "crime": "Family violence, gang harm, methamphetamine, and the policing of growing Tauranga.",
    "economy": "Kiwifruit (Zespri exports), the Port of Tauranga, Rotorua tourism, and Māori land economy.",
    "education": "Tertiary access via Toi Ohomai and University of Waikato, school engagement, and rural reach.",
    "environment": "Lake Rotorua water quality, Tauranga Harbour, native ecosystem, and forestry impacts.",
    "governance": "Bay of Plenty Regional, the Tauranga / Western Bay of Plenty / Rotorua councils, and iwi co-governance.",
    "health": "Tauranga Hospital capacity, primary care, mental health, and rural reach across the BoP.",
    "housing": "Tauranga affordability (severely unaffordable), supply pressures, and rural-urban housing.",
    "inequality": "Eastern Bay of Plenty deprivation, Māori land development, and structural drivers.",
    "infrastructure": "Tauranga Northern Link, three waters, and Eastern Bay road resilience.",
    "transport": "The Tauranga–Auckland corridor, the port freight network, and SH2 / SH29 reliability.",
}

bay_of_plenty_bp = make_region_blueprint(
    "bay-of-plenty",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
