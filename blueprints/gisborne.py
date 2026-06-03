"""Gisborne — Tairāwhiti research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name gisborne_bp.
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
    "climate": "Cyclone Gabrielle, slash and erosion, drought risk, and adaptation in Tairāwhiti.",
    "crime": "Family violence, youth offending, and the policing of an isolated East Cape region.",
    "economy": "Wine (Chardonnay, ~2,200 ha), Eastland Port, sheep and beef, forestry, and Ngāti Porou economic development.",
    "education": "Tertiary access from rural Tairāwhiti, school engagement, and te reo Māori in schools.",
    "environment": "Slash on East Cape beaches, Tairāwhiti waterways, and native ecosystem recovery.",
    "governance": "Gisborne District (unitary authority), Ngāti Porou Treaty settlement, and central–local relations.",
    "health": "Gisborne Hospital, primary care, mental health, and rural reach in Tairāwhiti.",
    "housing": "Affordability, rural overcrowding, and emergency accommodation post-Gabrielle.",
    "inequality": "Highest deprivation nationally, rural isolation, and structural drivers.",
    "infrastructure": "SH35 (~330 km East Cape road), three waters, and resilience after Cyclone Gabrielle.",
    "transport": "SH2 / SH35 reliability, Eastland Port freight, and the cyclone-damaged road network.",
}

gisborne_bp = make_region_blueprint(
    "gisborne",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
