"""Manawatū-Whanganui — Te Manawa o te Ika research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name manawatu_whanganui_bp.
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
    "climate": "Whanganui River legal personhood (Te Awa Tupua Act 2017), Ruapehu volcanic hazard, and adaptation.",
    "crime": "Family violence, youth offending, and the policing of a region with multiple urban centres.",
    "economy": "Massey University (~12K students), agriculture, NZDF (Ohakea / Linton), and energy (Manawatū wind).",
    "education": "Massey University, UCOL, school engagement, and rural tertiary access.",
    "environment": "The Whanganui River, the Manawatū River, native bush, and freshwater quality.",
    "governance": "Horizons Regional, the Palmerston North / Whanganui / Ruapehu councils, and Treaty (Whanganui, Rangitīkei iwi).",
    "health": "Palmerston North Hospital, primary care, mental health, and rural reach.",
    "housing": "Palmerston North affordability, Whanganui rural housing, and rental supply.",
    "inequality": "Whanganui deprivation, rural isolation, and structural drivers.",
    "infrastructure": "Three waters, Ruapehu volcanic risk, and the SH1 / SH3 reliability.",
    "transport": "Manawatū Gorge replacement (Te Ahu a Turanga), SH1 reliability, and rail freight to Wellington.",
}

manawatu_whanganui_bp = make_region_blueprint(
    "manawatu-whanganui",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
