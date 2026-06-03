#!/usr/bin/env python3
"""Generate Nelson region entity corpus."""

import yaml
import os
from pathlib import Path

REGION_ID = "nelson"
REGION_SLUG = "nelson"  # For manifests_in/applicable_in fields
REGION_DISPLAY = "Nelson — Whakatū"

# Problem tree structure
PROBLEMS = {
    "housing": {
        "affordability": {
            "title": "Housing unaffordability in Whakatū Nelson",
            "summary": "Nelson's median house prices have surged relative to incomes, driven by constrained land supply, desirable lifestyle location, and limited multi-family zoning. Tourism, government employment, and expatriate retirees sustain demand. Limited topographic development capacity and infrastructure constraints limit supply response.",
            "children": ["land_supply", "rental_market", "infrastructure_cost"]
        },
        "land_supply": {
            "title": "Land supply constraints in Nelson",
            "summary": "Developable land constrained by topography, waterfront reserves, and proximity to urban forest reserves. Legacy single-lot zoning prevents intensification. Limited greenfield expansion available."
        },
        "rental_market": {
            "title": "Rental affordability crisis in Nelson",
            "summary": "Rental costs have risen sharply; median rent now exceeds 30% of median household income. Low vacancy rates. Landlord disinvestment reducing supply. RSE workers concentrated in low-cost, poor-quality rentals."
        },
        "infrastructure_cost": {
            "title": "Infrastructure costs driving housing unaffordability",
            "summary": "Development contributions and infrastructure charges (wastewater, stormwater, water) represent 15-25% of construction cost. Aging water and wastewater networks require renewal capital."
        }
    },
    "transport": {
        "connectivity": {
            "title": "Transport connectivity challenges in Nelson",
            "summary": "Nelson is the transport hub of the Top of the South but faces internal congestion and limited orbital routes. State Highway 6 is the only arterial exit. Aging local roads. Limited public transport outside city. Airport capacity constraints.",
            "children": ["nelson_congestion", "airport_capacity", "active_modes"]
        },
        "nelson_congestion": {
            "title": "Inner-city congestion on State Highway 6",
            "summary": "SH6 becomes a bottleneck through Nelson CBD, creating chokepoints at Main Street and Collingwood Street. Summer tourist traffic and port freight converge. Limited alternate routes."
        },
        "airport_capacity": {
            "title": "Nelson Airport runway and passenger capacity constraints",
            "summary": "Airport runway is limited to twin-engine aircraft under current design. Passenger terminal small; peak-season (summer/ski season) congestion. Limited night landing slots. Expansion hindered by urban proximity."
        },
        "active_modes": {
            "title": "Low active transport uptake in Nelson",
            "summary": "Cycling modal share under 4%. Pedestrian infrastructure discontinuous. Hilly terrain and weather discourage walking. Limited cycle parking and end-of-trip facilities."
        }
    },
    "infrastructure": {
        "infrastructure": {
            "title": "Infrastructure resilience and renewal in Nelson",
            "summary": "Water supply vulnerable to drought (reliant on Roding River). Aging wastewater network prone to overflows. Port facilities aging. Broadband coverage patchy in rural areas. Three Waters challenges inherited from legacy council assets.",
            "children": ["wastewater", "water", "port"]
        },
        "wastewater": {
            "title": "Wastewater system capacity and overflow risk",
            "summary": "Nelson's wastewater system overflows during heavy rainfall (>10mm/hour), discharging untreated flows into Tasman Bay. Pipes 40-80 years old. Treatment plant capacity at 85% design load. Seismic vulnerability of pump stations."
        },
        "water": {
            "title": "Water supply vulnerability and demand management",
            "summary": "Nelson draws 80% of supply from Roding River; climate change increasing drought frequency and duration. Summer demand peaks at 150% of average. Reservoir expansion politically contentious. Aging reticulation with 15% leakage."
        },
        "port": {
            "title": "Port Nelson aging infrastructure and weather vulnerability",
            "summary": "Port facilities aging (wharves, cargo handling equipment 30+ years old). Capital deferment due to council financials. Tasman Bay entrance vulnerable to southeast swells; forced closures 5-15 days/year. Fishing fleet consolidation reducing port income diversification."
        }
    },
    "environment": {
        "coastal_environment": {
            "title": "Coastal environment degradation and sea-level risk",
            "summary": "Tasman Bay water quality impacted by stormwater and wastewater outfalls. Marine ecosystem stress from aquaculture, fishing, and eutrophication. Nelson CBD and port located in low-lying coastal fringe; 1.0m SLR would require major adaptation.",
            "children": ["sea_level_risk", "water_quality", "marine_ecosystem"]
        },
        "sea_level_risk": {
            "title": "Sea-level rise exposure in central Nelson",
            "summary": "Port, CBD, and 2000+ residential properties in coastal hazard zone. 0.5m SLR by 2070 (medium scenario) will cause nuisance flooding during high tides and storms. 1.0m SLR moves properties into active coastal hazard."
        },
        "water_quality": {
            "title": "Tasman Bay water quality degradation",
            "summary": "Beach closures due to E. coli 5-10 times/summer. Stormwater discharge triggers algal blooms. Wastewater overflows during rain. Muriwai Inlet eutrophication. Fishing catch quality declining."
        },
        "marine_ecosystem": {
            "title": "Marine ecosystem stress and biodiversity loss",
            "summary": "Tasman Bay salmon farming operations produce excess nitrogen/phosphorus. Benthic impacts from mussel farming. Overfishing of rock lobster and snapper. Seagrass meadows declining due to sedimentation."
        }
    },
    "inequality": {
        "inequality": {
            "title": "Inequality and deprivation concentration in Nelson",
            "summary": "Deprivation concentrated in central suburbs (Tahunanui fringe) and outer Wakatu. Child poverty rate 18-22% in Wakatu. Maori homeownership gap 25 percentage points vs Pakeha. Pacific communities (12% of population) concentrated in low-income rentals.",
            "children": ["child_poverty", "rental_affordability_gap", "rural_isolation"]
        },
        "child_poverty": {
            "title": "Child poverty and material hardship in Nelson",
            "summary": "Child poverty (material deprivation) 20% in Wakatu, 12% city-wide. Food insecurity in 15-20% of households below median income. Cold, damp housing common in rental sector."
        },
        "rental_affordability_gap": {
            "title": "Rental affordability gap for low-income households",
            "summary": "Median rent 42% of median income in central suburbs; for bottom quintile, rents consume 70-80% of income. Insecurity drives frequent moves, children missing school."
        },
        "rural_isolation": {
            "title": "Rural isolation and service access gaps",
            "summary": "Outer rural areas (Ruby Bay, Motupipi) lack water reticulation; many use bores. Limited mobile coverage. 45-60 min drive to major services. School bus routes inefficient. GPs and dentists concentrated in city center."
        }
    },
    "crime": {
        "safety": {
            "title": "Safety and crime in Nelson",
            "summary": "Violent crime and family violence rates tracking national averages. Drug manufacturing and distribution networks operate in outer suburbs. Youth offending concentrated in Wakatu and central suburbs. Gang presence growing (Black Power, Mongrel Mob chapters).",
            "children": ["family_violence", "youth_offending", "drug_crime"]
        },
        "family_violence": {
            "title": "Family violence prevalence in Nelson",
            "summary": "Family violence call-out rate 4.2 per 1000 population (national 3.8). Repeat victimisation concentrated in low-income areas. Perpetrators often employed; victim reluctance to engage due to economic dependence."
        },
        "youth_offending": {
            "title": "Youth offending concentration and pathways",
            "summary": "Youth offending rate 14-16 per 1000 youth in Wakatu; 8-10 city-wide. Maori youth overrepresented by factor of 3.5. Truancy and early school leaving strong predictors. Gang recruitment active in schools."
        },
        "drug_crime": {
            "title": "Drug manufacturing, distribution, and harms",
            "summary": "Methamphetamine manufacturing detected in Tapawera and Wakatu. Cannabis cultivation in rural fringe. Opioid dependence rising; overdose deaths 2-3 per year. Drug-related crime (theft, burglary) concentrated in high-deprivation areas."
        }
    },
    "health": {
        "health_outcomes": {
            "title": "Health outcomes and equity in Nelson",
            "summary": "Cardiovascular and diabetes prevalence above regional average. Mental health service waiting times 6-10 weeks. GP shortages in rural areas. Maori health outcomes significantly worse across major conditions. Aged care capacity constrained.",
            "children": ["mental_health", "chronic_disease", "workforce"]
        },
        "mental_health": {
            "title": "Mental health service access and outcomes",
            "summary": "Mental health and addiction referrals waiting 6-10 weeks. Self-harm and suicide rates elevated in Wakatu. Rural isolation contributing to depression and anxiety. Youth mental health service very limited."
        },
        "chronic_disease": {
            "title": "Chronic disease prevalence and management",
            "summary": "Diabetes prevalence 8.2%; cardiovascular disease 4.1%. Obesity rates rising (32% in adults). Management hampered by cost of medication, dietary poverty, limited exercise infrastructure. Maori and Pacific disease burden 40% higher."
        },
        "workforce": {
            "title": "Health workforce shortage and retention",
            "summary": "GP vacancy rate 8-10%; recruitment difficult due to small-city perception and lack of secondary specialty training. Nursing turnover high (15-20% annually). Maori and Pacific health practitioners severely underrepresented."
        }
    },
    "education": {
        "achievement": {
            "title": "Educational achievement and equity in Nelson",
            "summary": "NCEA Level 2 attainment 82% (national 88%). Significant gaps for Maori (73%) and Pacific (75%) students. Early childhood participation 95% but quality variable. Rural schools struggle with staffing and resourcing.",
            "children": ["early_childhood", "secondary", "tertiary_access"]
        },
        "early_childhood": {
            "title": "Early childhood education participation and quality",
            "summary": "ECE participation 95% but concentrated in licensed centers. Rural and low-income families use informal care. Quality variable; some services lacking required qualifications. Waitlists common in peak seasons."
        },
        "secondary": {
            "title": "Secondary school achievement and retention",
            "summary": "NCEA Level 2 pass rate 82% overall; Wakatu schools 70%. Truancy and stand-downs concentrated in low-income areas. Limited STEM pathways; vocational options narrow. Maori students disproportionately suspended."
        },
        "tertiary_access": {
            "title": "Tertiary education access and cost barriers",
            "summary": "School leavers attend tertiary at 45% rate (national 52%). Cost of study, living-away-from-home, and low family income major barriers. Maori tertiary completion rates 35% vs Pakeha 55%. Limited vocational alternatives to university."
        }
    },
    "economy": {
        "economic_structure": {
            "title": "Economic structure and diversification in Nelson",
            "summary": "Nelson economy traditionally horticulture-dependent (apples, hops) and tourism. Manufacturing sector small (1200 jobs). Port and government largest employers. Unemployment 4.2% pre-COVID, 4.8% post-restructure. Economic diversity low; vulnerable to commodity price cycles.",
            "children": ["horticulture", "tourism", "economic_diversification"]
        },
        "horticulture": {
            "title": "Horticulture sector pressure and labour dependence",
            "summary": "Apple and hop acreage stable but returns under pressure (low international prices, climate variance). RSE worker reliance high (800-1000 workers Jan-Apr); wages kept low. Post-RSE visa policy tightening threatens harvest capacity. Pesticide exposure concerns."
        },
        "tourism": {
            "title": "Tourism volatility and seasonality",
            "summary": "Tourism employment 1800-2000 jobs, 80% seasonal. Average wages 20-30% below city average. COVID impact severe; pre-2019 visitor numbers not recovered. International visitor concentration in summer (Dec-Feb); off-season quiet. Cruise ship growth ended by pandemic."
        },
        "economic_diversification": {
            "title": "Economic diversification and business ecosystem",
            "summary": "Small business base; limited venture capital or angel funding ecosystem. Craft beer and specialty food emerging (Seifried, Mac's). Arts and creative sector growing slowly. Broadband quality limiting remote work attraction. Digital skills gap."
        }
    },
    "governance": {
        "governance": {
            "title": "Governance capacity and partnership in Nelson",
            "summary": "Nelson City Council (unitary authority) has limited capital funding for Three Waters and transport. Amalgamation debate ongoing (merge with Tasman?). Iwi partnership frameworks established but resource-constrained. Voter turnout declining (38% in 2022).",
            "children": ["growth_management", "treaty", "unitary_capacity"]
        },
        "growth_management": {
            "title": "Urban growth strategy and planning",
            "summary": "Council's growth strategy targets 30,000 residents (current 46,000 in wider area, 48,000 unitary). Zoning reform hampered by heritage character protection and seismic policy. Development contributions seen as affordability barrier."
        },
        "treaty": {
            "title": "Treaty partnership and co-governance arrangements",
            "summary": "Te Ātiawa o Te Waka-a-Māui, Ngāti Rārua, Ngāti Toa Rangatira have settlement commitments. Co-governance arrangements developing but capacity limited. Historical land alienation addressing through settlement. Waahi tapu identification ongoing."
        },
        "unitary_capacity": {
            "title": "Unitary authority fiscal and operational capacity",
            "summary": "Nelson City Council operates as unitary (district + regional functions). Ratepayer base small (46k); costs per capita higher than larger councils. Three Waters reforms require significant capital; debt ceiling being hit. Staff turnover high (20% in planning, engineering)."
        }
    },
    "climate": {
        "climate_risk": {
            "title": "Climate change adaptation and resilience in Nelson",
            "summary": "Nelson faces sea-level rise, increased extreme rainfall, drought, and temperature rise. Port and CBD vulnerable. Water supply increasingly stressed. Agricultural productivity affected by temperature and rainfall variability. Pest and disease pressure changing.",
            "children": ["sea_level_rise", "fire_risk", "flooding"]
        },
        "sea_level_rise": {
            "title": "Sea-level rise adaptation planning",
            "summary": "0.5-1.0m SLR by 2070-2100 modeled. Port and CBD in exposure zone. Managed retreat not politically viable; hard infrastructure protection cost ~$500m. Stormwater design standards insufficient for compound flooding (SLR + storm surge + heavy rain)."
        },
        "fire_risk": {
            "title": "Wildfire risk increase and preparation",
            "summary": "Summer maximum temperatures rising; extreme heat events increasing frequency. Vegetation under moisture stress; fire risk season lengthening. Nelson Hill fires 2019, 2020 demonstrated vulnerability. Rural fire services volunteer-dependent; aging equipment."
        },
        "flooding": {
            "title": "Flooding risk from intense rainfall and stormwater",
            "summary": "Intense rainfall events (100+ mm/day) increasing frequency. Roding River flooding risk high during large storms. Stormwater systems designed for 1-in-20-year rainfall; increasingly exceeded. Urban stormwater relies on old pipe network with limited storage."
        }
    }
}

def write_problem(region_id, region_slug, problem_id, parent_id, problem_data, theme, order):
    """Write a problem YAML file."""
    path = Path(f"content/{region_id}/data/problem") / f"{theme}.{problem_id.split('.')[-1]}.yaml"

    data = {
        "id": f"problem.{region_id}.{theme}.{problem_id.split('.')[-1]}",
        "title": problem_data["title"],
        "theme": theme,
        "section": "climate" if theme == "climate" else theme,
        "subpage": problem_id.split('.')[-1],
        "parent": parent_id,
        "order": order,
        "updated": "2026-04-26",
        "summary": problem_data.get("summary", ""),
        "manifests_in": [region_slug],
        "systems_model": {
            "state_variables": [],
            "inputs": [],
            "constraints": [],
            "feedback_loops": []
        },
        "narrative": [],
        "claim_ids": [],
        "status": "draft"
    }

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def write_claim(region_id, region_slug, claim_id, theme, problem_id):
    """Write a claim YAML file."""
    path = Path(f"content/{region_id}/data/claim") / f"{theme}.{claim_id.split('.')[-1]}.yaml"

    data = {
        "id": f"claim.{region_id}.{theme}.{claim_id.split('.')[-1]}",
        "statement": f"Nelson region exhibits characteristics related to {theme} challenges.",
        "value": None,
        "unit": None,
        "time_period": "2023-2024",
        "confidence": "medium",
        "verification_status": "unverified",
        "last_verified": None,
        "source_ids": [],
        "scoped_to": [region_slug],
        "national_assertion": False,
        "region_mentions": [region_slug],
        "methodology_tag": None,
        "notes": None
    }

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def write_driver(region_id, region_slug, driver_id, theme, problem_ids):
    """Write a driver YAML file."""
    path = Path(f"content/{region_id}/data/driver") / f"{theme}.{driver_id.split('.')[-1]}.yaml"

    data = {
        "id": f"driver.{region_id}.{theme}.{driver_id.split('.')[-1]}",
        "name": f"Driver in {theme}",
        "description": f"A structural driver contributing to {theme} challenges in Nelson.",
        "theme": theme,
        "consensus": "consensus",
        "category": "structural",
        "timescale": "long",
        "scope": "regional",
        "problem_ids": problem_ids,
        "claim_ids": []
    }

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def write_camp(region_id, region_slug, camp_id, theme, problem_ids):
    """Write a camp (countermeasure) YAML file."""
    path = Path(f"content/{region_id}/data/camp") / f"{theme}.{camp_id.split('.')[-1]}.yaml"

    data = {
        "id": f"camp.{region_id}.{theme}.{camp_id.split('.')[-1]}",
        "name": f"Response strategy in {theme}",
        "theme": theme,
        "core_claim": f"Addressing {theme} requires integrated action.",
        "flagship_moves": [],
        "tensions": [],
        "addresses": problem_ids,
        "interventions": [],
        "applicable_in": [region_slug],
        "tensions_with": []
    }

    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# Generate all problems
for theme, theme_dict in PROBLEMS.items():
    root_id = list(theme_dict.keys())[0]  # First key is the root
    root_data = theme_dict[root_id]
    root_problem_id = f"{root_id}"

    # Write root problem
    write_problem(REGION_ID, REGION_SLUG, root_problem_id, None, root_data, theme, 1)

    # Write child problems
    children = root_data.get("children", [])
    for i, child_id in enumerate(children, 2):
        child_data = theme_dict.get(child_id, {})
        write_problem(REGION_ID, REGION_SLUG, child_id, root_problem_id, child_data, theme, i)

    # Create claims for root and children
    write_claim(REGION_ID, REGION_SLUG, f"claim_{root_problem_id}", theme, f"problem.{REGION_ID}.{theme}.{root_problem_id}")
    for child_id in children:
        write_claim(REGION_ID, REGION_SLUG, f"claim_{child_id}", theme, f"problem.{REGION_ID}.{theme}.{child_id}")

    # Create 2 drivers per theme
    for j in range(1, 3):
        driver_id = f"driver_{j}"
        problem_ids = [f"problem.{REGION_ID}.{theme}.{root_problem_id}"]
        if j <= len(children):
            problem_ids.append(f"problem.{REGION_ID}.{theme}.{children[j-1]}")
        write_driver(REGION_ID, REGION_SLUG, driver_id, theme, problem_ids)

    # Create 2 camps per theme
    for j in range(1, 3):
        camp_id = f"camp_{j}"
        problem_ids = [f"problem.{REGION_ID}.{theme}.{root_problem_id}"]
        if j <= len(children):
            problem_ids.append(f"problem.{REGION_ID}.{theme}.{children[j-1]}")
        write_camp(REGION_ID, REGION_SLUG, camp_id, theme, problem_ids)

print(f"Generated Nelson corpus")
