"""West Coast — Te Tai Poutini research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name west_coast_bp.
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
    "climate": "Glacier retreat, flooding, drought risk, and adaptation in Te Tai Poutini.",
    "crime": "Family violence, methamphetamine harm, and the policing of a remote, low-density region.",
    "economy": "Mining transition (post-coal), the conservation economy, dairy, and the visitor economy.",
    "education": "Tertiary access from a remote region, school engagement, and the kura kaupapa network.",
    "environment": "Conservation estate (~85% of land), West Coast forests, freshwater, and biodiversity.",
    "governance": "West Coast Regional, the Buller / Grey / Westland councils, and Treaty (Ngāi Tahu).",
    "health": "Te Nikau Hospital (Greymouth), the GP shortage, mental health, and rural reach.",
    "housing": "Population decline, rural housing, and lifestyle-buyer market dynamics.",
    "inequality": "Population decline, deprivation pockets, and structural drivers.",
    "infrastructure": "SH6 / SH73 resilience, three waters, and digital connectivity.",
    "transport": "SH6 (the only South Island West Coast road), SH73 (Arthur's Pass), and freight reliability.",
}

west_coast_bp = make_region_blueprint(
    "west-coast",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
