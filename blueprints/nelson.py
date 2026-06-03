"""Nelson — Whakatū research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name nelson_bp.
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
    "climate": "Pigeon Valley / Moutere Hills bushfire (2022, ~2,200 ha combined), coastal hazard, and adaptation in Whakatū.",
    "crime": "Family violence, methamphetamine, and the policing of a small, desirable city.",
    "economy": "Aquaculture, tourism, the fishing port, hops, and the Nelson seafood economy.",
    "education": "Nelson-Marlborough Institute of Technology (NMIT), school engagement, and tertiary reach.",
    "environment": "Tasman Bay, marine ecology, freshwater quality, and native ecosystem.",
    "governance": "Nelson City Council (unitary authority), Treaty settlements, and central–local relations.",
    "health": "Nelson Hospital, primary care, mental health, and the regional health workforce.",
    "housing": "Severely-unaffordable housing in a desirable city, supply pressure, and rental market.",
    "inequality": "Suburban disparity, low-wage seasonal work, and structural drivers.",
    "infrastructure": "Three waters, Port Nelson, and the SH6 connection to Tasman / Marlborough.",
    "transport": "SH6 reliability, Port Nelson, and connectivity to West Coast / Marlborough.",
}

nelson_bp = make_region_blueprint(
    "nelson",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
