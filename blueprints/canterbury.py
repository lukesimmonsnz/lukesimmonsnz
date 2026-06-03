"""Canterbury — Waitaha research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name canterbury_bp.
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
    "climate": "Glacier retreat (Southern Alps), drought risk, and adaptation in Waitaha.",
    "crime": "Family violence, methamphetamine harm, and policing across post-quake Christchurch.",
    "economy": "The Christchurch rebuild, agriculture (~650K dairy herd, irrigation), and Lyttelton Port (~2.1M TEU).",
    "education": "University of Canterbury, Lincoln University, post-quake school recovery, and tertiary reach.",
    "environment": "Canterbury aquifers (45 community bores at exceedance), nitrate loads, and biodiversity.",
    "governance": "Environment Canterbury (ECan), the Christchurch / Selwyn / Waimakariri councils, and Treaty (Ngāi Tahu).",
    "health": "Christchurch Hospital pressure, primary care, mental health, and the Hagley project.",
    "housing": "Earthquake-prone stock (~3,200 EPB), affordability, and supply pressures.",
    "inequality": "East Christchurch deprivation, post-quake recovery disparity, and structural drivers.",
    "infrastructure": "Earthquake debt (~$15B Crown), three waters (~$6B capex to 2054), and Lyttelton Port.",
    "transport": "Christchurch motorways, Lyttelton freight, and the SH1 South Island spine.",
}

canterbury_bp = make_region_blueprint(
    "canterbury",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
