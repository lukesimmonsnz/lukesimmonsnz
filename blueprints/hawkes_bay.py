"""Hawke's Bay — Te Matau-a-Māui research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name hawkes_bay_bp.
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
    "climate": "Cyclone Gabrielle recovery (~$3–5B regional), heat, drought, and adaptation in Te Matau-a-Māui.",
    "crime": "Family violence, youth offending, gang harm, and policing post-Gabrielle.",
    "economy": "Horticulture (apples, pip-fruit), wine, RSE seasonal labour, and Heretaunga Plains agriculture.",
    "education": "EIT tertiary, school engagement, and the post-Gabrielle education recovery.",
    "environment": "Heretaunga aquifers, Tukituki River, freshwater quality, and biodiversity.",
    "governance": "Hawke's Bay Regional, the Hastings / Napier councils, and central–local relations post-Gabrielle.",
    "health": "Hawke's Bay Hospital, primary care, mental health, and Māori health equity.",
    "housing": "Flaxmere / Wairoa affordability, post-Gabrielle housing recovery, and rural overcrowding.",
    "inequality": "Wairoa deprivation, Flaxmere disparity, and structural drivers in Hawke's Bay.",
    "infrastructure": "Three waters resilience, post-Gabrielle road repair, and Napier Port freight.",
    "transport": "SH2 / SH5 reliability, Napier Port, and the Hawke's Bay rail link.",
}

hawkes_bay_bp = make_region_blueprint(
    "hawkes-bay",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
