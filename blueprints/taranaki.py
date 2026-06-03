"""Taranaki research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name taranaki_bp.
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
    "climate": "Energy transition from oil and gas, volcanic risk (Taranaki Maunga), and adaptation.",
    "crime": "Family violence, youth offending, methamphetamine harm, and policing across Taranaki.",
    "economy": "Oil and gas wind-down, dairy, the energy transition, and Māori land / Treaty (Parihaka).",
    "education": "WITT tertiary, school engagement, and post-oil education pathways.",
    "environment": "Taranaki Maunga, freshwater, native ecosystem, and the dairy intensity legacy.",
    "governance": "Taranaki Regional, the New Plymouth / Stratford / South Taranaki councils, and Treaty (Te Atiawa, Ngāruahine, Taranaki iwi).",
    "health": "Taranaki Base Hospital, primary care, mental health, and rural reach.",
    "housing": "New Plymouth affordability, rural housing, and post-oil town stability.",
    "inequality": "South Taranaki deprivation, post-oil employment shifts, and structural drivers.",
    "infrastructure": "Three waters, Port Taranaki, energy (post-Maui field), and digital connectivity.",
    "transport": "SH3 reliability, Port Taranaki freight, and the New Plymouth airport.",
}

taranaki_bp = make_region_blueprint(
    "taranaki",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
