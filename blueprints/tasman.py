"""Tasman — Te Tai-o-Aorere research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name tasman_bp.
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
    "climate": "Coastal hazard, the 2022 Pigeon Valley fire, drought, and adaptation in Te Tai-o-Aorere.",
    "crime": "Family violence, rural policing, and the policing of a low-density region.",
    "economy": "Horticulture, forestry, aquaculture, and tourism (Abel Tasman / Golden Bay).",
    "education": "Tertiary access from a rural region, school engagement, and home-school networks.",
    "environment": "Abel Tasman, Te Waikoropupū Springs, freshwater quality, and native ecosystem.",
    "governance": "Tasman District (unitary authority), Treaty settlements, and central–local relations.",
    "health": "Nelson-Tasman shared hospital, the GP shortage, and 90-min Takaka–Nelson hospital travel.",
    "housing": "Lifestyle-migration affordability pressures, rural housing, and the rental market.",
    "inequality": "Geographic isolation (Golden Bay), seasonal work, and structural drivers.",
    "infrastructure": "Three waters, SH60 (Takaka Hill), and digital connectivity in Te Tai-o-Aorere.",
    "transport": "SH60 / SH6 reliability, the Takaka Hill route, and connectivity to Nelson / West Coast.",
}

tasman_bp = make_region_blueprint(
    "tasman",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
