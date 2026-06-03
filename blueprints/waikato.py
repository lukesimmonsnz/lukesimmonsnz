"""Waikato research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name waikato_bp.
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
    "climate": "Climate adaptation in dairy country, peatland emissions, and Hauraki Gulf heating.",
    "crime": "Methamphetamine harm, Huntly deprivation, family violence, and rural policing across the Waikato.",
    "economy": "Dairy (1.2–1.4M cattle, three Fonterra plants), Ruakura Superhub, and the agricultural-industrial base.",
    "education": "University of Waikato (~12K students), kura kaupapa, and rural school engagement.",
    "environment": "The Waikato River, peatland, freshwater nitrate loads, and Te Awa Tupua-style governance.",
    "governance": "Waikato-Tainui co-governance (WRA 50/50), and the Hamilton / Waikato District councils.",
    "health": "Waikato Hospital capacity, primary care, mental health, and Māori health equity.",
    "housing": "Hamilton growth pressures, affordability, and rural / lifestyle-block supply.",
    "inequality": "Huntly / Tokoroa deprivation pockets, rural-urban gaps, and structural drivers.",
    "infrastructure": "Hamilton ring road, three waters, energy, and digital across the Waikato.",
    "transport": "The Auckland–Hamilton corridor, the SH1 freight route, and rail connectivity to the BoP.",
}

waikato_bp = make_region_blueprint(
    "waikato",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
