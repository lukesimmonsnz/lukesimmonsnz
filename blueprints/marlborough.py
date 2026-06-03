"""Marlborough — Te Tauihu-o-te-Waka research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name marlborough_bp.
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
    "climate": "Drought risk, coastal hazard, and adaptation in Marlborough wine country.",
    "crime": "Family violence, seasonal RSE-related issues, and the policing of a rural region.",
    "economy": "Wine (~77% of NZ production, ~$1.8B exports, ~28,000 ha), aquaculture (~100,000 t mussels, ~95% NZ), Cook Strait ferries.",
    "education": "NMIT / EIT tertiary, school engagement, and the seasonal-work education context.",
    "environment": "Marlborough Sounds ecology, freshwater allocation, and the wine-country impact.",
    "governance": "Marlborough District (unitary authority), Treaty settlements (Ngāti Toa, Rangitāne).",
    "health": "Wairau Hospital (Blenheim), primary care, mental health, and rural reach.",
    "housing": "Affordability for seasonal workers (RSE), rural housing, and lifestyle-block supply.",
    "inequality": "Seasonal work, RSE worker conditions, and structural drivers in Marlborough.",
    "infrastructure": "Kaikōura SH1 repair (~$1.4B post-quake), Cook Strait ferries, and three waters.",
    "transport": "SH1 reliability post-Kaikōura, Cook Strait ferries (Picton), and the wine-region road network.",
}

marlborough_bp = make_region_blueprint(
    "marlborough",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
