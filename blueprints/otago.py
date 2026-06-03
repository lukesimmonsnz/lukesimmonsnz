"""Otago research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name otago_bp.
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
    "climate": "Alpine Fault hazard (~27% Mw8+ in 50 years), Queenstown climate, and adaptation.",
    "crime": "Family violence, methamphetamine harm, and policing across Dunedin / Queenstown.",
    "economy": "Queenstown tourism (~2M+ visitors / ~$2.5–3B spend), Pinot Noir (~2,200 ha), Dunedin Hospital rebuild (~$2.3B+).",
    "education": "University of Otago (Dunedin's economic anchor), school engagement, and tertiary reach.",
    "environment": "Central Otago freshwater, the Lake District ecology, and the Alpine Fault risk.",
    "governance": "Otago Regional, the Dunedin / Queenstown-Lakes / Central Otago councils, and Treaty (Ngāi Tahu).",
    "health": "Dunedin Hospital rebuild, the GP shortage, mental health, and Otago primary care.",
    "housing": "Queenstown housing (>15× median multiple), Dunedin student housing, and rural supply.",
    "inequality": "Queenstown wealth disparity, rural isolation, and structural drivers.",
    "infrastructure": "Port Chalmers, three waters, SH1 (Pigroot), and the Alpine Fault hazard.",
    "transport": "The SH1 spine, Port Chalmers freight, and Queenstown airport pressure.",
}

otago_bp = make_region_blueprint(
    "otago",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
