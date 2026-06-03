"""
One-off bulk rollout — apply Auckland/Wellington's theme-list pattern to the
other 14 regions.

For each region:
  1. Rewrite blueprints/<region>.py with a SECTION_BLURBS dict and pass it
     into make_region_blueprint().
  2. Replace the heading-style theme list in templates/<region>/index.html
     with the theme-list / theme-title / theme-blurb structure (drop the
     "In progress" block — all regions have all 11 themes).

Idempotent: re-running on an already-updated region is a no-op for the
template (the new structure has no <h2> heading inside the article) and
overwrites the blueprint with the same content.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Region slug → (display title, BLUEPRINT_NAME, lede_paragraph, blurbs by theme)
REGIONS: dict[str, dict] = {
    "northland": {
        "title": "Northland — Te Tai Tokerau",
        "blurbs": {
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
        },
    },
    "waikato": {
        "title": "Waikato",
        "blurbs": {
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
        },
    },
    "bay-of-plenty": {
        "title": "Bay of Plenty — Te Moana-a-Toi",
        "blurbs": {
            "climate": "Coastal hazard for Tauranga, kiwifruit and orchard climate exposure, and adaptation in Te Moana-a-Toi.",
            "crime": "Family violence, gang harm, methamphetamine, and the policing of growing Tauranga.",
            "economy": "Kiwifruit (Zespri exports), the Port of Tauranga, Rotorua tourism, and Māori land economy.",
            "education": "Tertiary access via Toi Ohomai and University of Waikato, school engagement, and rural reach.",
            "environment": "Lake Rotorua water quality, Tauranga Harbour, native ecosystem, and forestry impacts.",
            "governance": "Bay of Plenty Regional, the Tauranga / Western Bay of Plenty / Rotorua councils, and iwi co-governance.",
            "health": "Tauranga Hospital capacity, primary care, mental health, and rural reach across the BoP.",
            "housing": "Tauranga affordability (severely unaffordable), supply pressures, and rural-urban housing.",
            "inequality": "Eastern Bay of Plenty deprivation, Māori land development, and structural drivers.",
            "infrastructure": "Tauranga Northern Link, three waters, and Eastern Bay road resilience.",
            "transport": "The Tauranga–Auckland corridor, the port freight network, and SH2 / SH29 reliability.",
        },
    },
    "gisborne": {
        "title": "Gisborne — Tairāwhiti",
        "blurbs": {
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
        },
    },
    "hawkes-bay": {
        "title": "Hawke's Bay — Te Matau-a-Māui",
        "blurbs": {
            "climate": "Cyclone Gabrielle recovery (~$3–5B regional), heat, drought, and adaptation in Te Matau-a-Māui.",
            "crime": "Family violence, youth offending, gang harm, and policing post-Gabrielle.",
            "economy": "Horticulture (apples, pip-fruit), wine, RSE seasonal labour, and Heretaunga Plains agriculture.",
            "education": "EIT tertiary, school engagement, and the post-Gabrielle education recovery.",
            "environment": "Heretaunga aquifers, Tukituki River, freshwater quality, and biodiversity.",
            "governance": "Hawke's Bay Regional, the Hastings / Napier councils, and central–local relations post-Gabrielle.",
            "health": "Hawke's Bay Hospital, primary care, mental health, and Māori health equity.",
            "housing": "Flaxmere / Wairoa affordability, post-Gabrielle housing recovery, and rural overcrowding.",
            "inequality": "Wairoa deprivation, Flaxmere disparity, and structural drivers in Hawke's Bay.",
            "infrastructure": "Three waters resilience, post-Gabrielle road repair, and Napier Port freight.",
            "transport": "SH2 / SH5 reliability, Napier Port, and the Hawke's Bay rail link.",
        },
    },
    "taranaki": {
        "title": "Taranaki",
        "blurbs": {
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
        },
    },
    "manawatu-whanganui": {
        "title": "Manawatū-Whanganui — Te Manawa o te Ika",
        "blurbs": {
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
        },
    },
    "nelson": {
        "title": "Nelson — Whakatū",
        "blurbs": {
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
        },
    },
    "tasman": {
        "title": "Tasman — Te Tai-o-Aorere",
        "blurbs": {
            "climate": "Coastal hazard, the 2022 Pigeon Valley fire, drought, and adaptation in Te Tai-o-Aorere.",
            "crime": "Family violence, rural policing, and the policing of a low-density region.",
            "economy": "Horticulture, forestry, aquaculture, and tourism (Abel Tasman / Golden Bay).",
            "education": "Tertiary access from a rural region, school engagement, and home-school networks.",
            "environment": "Abel Tasman, Te Waikoropupū Springs, freshwater quality, and native ecosystem.",
            "governance": "Tasman District (unitary authority), Treaty settlements, and central–local relations.",
            "health": "Nelson-Tasman shared hospital, the GP shortage, and 90-min Takaka–Nelson hospital travel.",
            "housing": "Lifestyle-migration affordability pressures, rural housing, and the rental market.",
            "inequality": "Geographic isolation (Golden Bay), seasonal work, and structural drivers.",
            "infrastructure": "Three waters, SH60 (Takaka Hill), and digital connectivity in Te Tai-o-Aorere.",
            "transport": "SH60 / SH6 reliability, the Takaka Hill route, and connectivity to Nelson / West Coast.",
        },
    },
    "marlborough": {
        "title": "Marlborough — Te Tauihu-o-te-Waka",
        "blurbs": {
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
        },
    },
    "west-coast": {
        "title": "West Coast — Te Tai Poutini",
        "blurbs": {
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
        },
    },
    "canterbury": {
        "title": "Canterbury — Waitaha",
        "blurbs": {
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
        },
    },
    "otago": {
        "title": "Otago",
        "blurbs": {
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
        },
    },
    "southland": {
        "title": "Southland — Murihiku",
        "blurbs": {
            "climate": "Coastal hazard, Fiordland's wet climate, and adaptation in Murihiku.",
            "crime": "Family violence, methamphetamine harm, and rural policing in Southland.",
            "economy": "Tiwai Point smelter (~1,000 jobs, ~13% of NZ electricity, contract to 2026), Fonterra Edendale, Bluff oysters, Fiordland tourism (~700K visitors).",
            "education": "Southern Institute of Technology, school engagement, and tertiary reach.",
            "environment": "Fiordland (UNESCO), freshwater, biodiversity, and the agricultural impact.",
            "governance": "Southland Regional, the Invercargill / Southland District councils, and Treaty (Ngāi Tahu).",
            "health": "Southland Hospital (Invercargill), the GP shortage, mental health, and rural reach.",
            "housing": "Invercargill affordability, rural housing, and the post-Tiwai contingency.",
            "inequality": "Population retention, post-Tiwai uncertainty, and structural drivers.",
            "infrastructure": "Manapouri 850 MW (Tiwai dependency), three waters, and Bluff Port.",
            "transport": "The SH1 spine, Bluff Port, and Stewart Island ferry connectivity.",
        },
    },
}

SECTION_TITLES_TEMPLATE = '''SECTION_TITLES: dict[str, str] = {
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
}'''


BLUEPRINT_TEMPLATE = '''"""{title} research blueprint.

Produced by the RegionBlueprintFactory. All routing and page-loading logic
lives in blueprints/region.py; this module supplies only the region-specific
SECTION_TITLES + SECTION_BLURBS and registers the blueprint under the
canonical name {var_name}.
"""

from blueprints.region import make_region_blueprint

{section_titles}

# One-sentence summaries shown under each theme link on the region index.
# First-pass drafts; edit freely.
SECTION_BLURBS: dict[str, str] = {{
{blurbs}
}}

{var_name} = make_region_blueprint(
    "{slug}",
    SECTION_TITLES,
    section_blurbs=SECTION_BLURBS,
)
'''


def render_blurbs_dict(blurbs: dict[str, str]) -> str:
    keys = ["climate", "crime", "economy", "education", "environment",
            "governance", "health", "housing", "inequality",
            "infrastructure", "transport"]
    lines = []
    for k in keys:
        v = blurbs[k].replace('"', '\\"')
        lines.append(f'    "{k}": "{v}",')
    return "\n".join(lines)


def write_blueprint(slug: str, info: dict) -> None:
    var_name = slug.replace("-", "_") + "_bp"
    bp_path = ROOT / "blueprints" / f"{slug.replace('-', '_')}.py"
    if not bp_path.exists():
        # Some blueprint files use hyphens-to-underscore convention only sometimes.
        # Try the slug as-is too.
        alt = ROOT / "blueprints" / f"{slug}.py"
        if alt.exists():
            bp_path = alt
    content = BLUEPRINT_TEMPLATE.format(
        title=info["title"],
        var_name=var_name,
        section_titles=SECTION_TITLES_TEMPLATE,
        slug=slug,
        blurbs=render_blurbs_dict(info["blurbs"]),
    )
    bp_path.write_text(content, encoding="utf-8")
    print(f"  blueprint: {bp_path.relative_to(ROOT)}")


# Match the heading-based theme list block (everything between <article class="prose">
# and the closing </article>).
ARTICLE_BLOCK_RE = re.compile(
    r'(<article class="prose">)\s*(.*?)\s*(</article>)',
    re.DOTALL,
)


def new_article_body(slug: str) -> str:
    var_name = slug.replace("-", "_")
    return f'''
    {{% if by_section %}}
      <ul class="theme-list">
      {{% for section_slug, pages in by_section.items() %}}
      {{% if section_slug != 'framing' %}}
        <li class="theme-list-item">
          <a class="theme-title" href="{{{{ url_for('{var_name}.section', section=section_slug) }}}}">
            {{{{ section_titles.get(section_slug, section_slug.replace('_', ' ').title()) }}}}
          </a>
          {{% if section_blurbs.get(section_slug) %}}
          <p class="theme-blurb">{{{{ section_blurbs[section_slug] }}}}</p>
          {{% endif %}}
        </li>
      {{% endif %}}
      {{% endfor %}}
      </ul>
    {{% else %}}
      <aside class="notice">
        <strong>No pages yet.</strong> Pages are generated from entity data under
        <code>content/{slug}/data/</code>.
      </aside>
    {{% endif %}}
  '''


def update_template(slug: str) -> None:
    tpl_path = ROOT / "templates" / slug / "index.html"
    text = tpl_path.read_text(encoding="utf-8")
    new_body = new_article_body(slug)
    new_text, n = ARTICLE_BLOCK_RE.subn(
        rf'\1{new_body}\3', text, count=1
    )
    if n != 1:
        raise RuntimeError(f"could not match <article class='prose'> in {tpl_path}")
    tpl_path.write_text(new_text, encoding="utf-8")
    print(f"  template:  {tpl_path.relative_to(ROOT)}")


def main():
    for slug, info in REGIONS.items():
        print(f"=== {slug} ===")
        write_blueprint(slug, info)
        update_template(slug)
    print(f"\nDone. {len(REGIONS)} regions updated.")


if __name__ == "__main__":
    main()
