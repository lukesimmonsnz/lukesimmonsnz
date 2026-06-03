"""Northland — Te Tai Tokerau research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name northland_bp.
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
    "climate": "Coastal erosion, kauri dieback resilience, drought risk, and climate adaptation in Te Tai Tokerau.",
    "crime": "Family violence, youth offending, gang harm, and the policing of remote rural Northland.",
    "economy": "Tourism, kauri / dairy / forestry, primary-industry diversification, and seasonal employment.",
    "education": "School engagement, tertiary access from a rural region, and the kura kaupapa Māori network.",
    "environment": "Kauri dieback, Kaipara Harbour, native bush retention, and freshwater quality.",
    "governance": "Far North / Kaipara / Whangārei councils, central–local relations, and the unsettled Ngāpuhi claim.",
    "health": "Hospital access, the GP shortage, mental health, and Māori health equity in Te Tai Tokerau.",
    "housing": "Affordability, rural overcrowding, papakāinga, and emergency accommodation in Northland.",
    "inequality": "High deprivation, geographic isolation, and the structural drivers of Northland inequality.",
    "infrastructure": "SH1, three waters (boil-water notices), and digital connectivity in a long, narrow region.",
    "transport": "SH1 reliability, Pūhoi–Warkworth, and the lack of north-of-Whangārei rail.",
}

northland_bp = make_region_blueprint(
    "northland",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
