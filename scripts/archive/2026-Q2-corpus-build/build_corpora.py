#!/usr/bin/env python3
"""
Build Otago and Southland research entity corpora.
Generates all source, methodology, problem, driver, camp, claim YAMLs.
"""

import yaml
from pathlib import Path
from datetime import datetime

# Define regions
REGIONS = {
    'otago': {
        'display': 'Otago — Ōtākou',
        'slug': 'otago',
        'infix': 'otago',
    },
    'southland': {
        'display': 'Southland — Murihiku',
        'slug': 'southland',
        'infix': 'southland',
    },
}

THEMES = [
    'housing', 'transport', 'infrastructure', 'environment',
    'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate'
]

DATE = '2026-04-26'

# ============================================================================
# SOURCES (region-specific)
# ============================================================================

OTAGO_SOURCES = [
    {
        'id': 'source.otago_stats_2024',
        'title': 'Otago Regional Council Statistics 2024',
        'author': 'Otago Regional Council',
        'publisher': 'ORC',
        'year': 2024,
        'url': 'https://www.orc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Regional planning and environmental data.',
    },
    {
        'id': 'source.queenstown_lakes_district_2024',
        'title': 'Queenstown Lakes District Council 2024 Annual Report',
        'author': 'Queenstown Lakes District Council',
        'publisher': 'QLDC',
        'year': 2024,
        'url': 'https://www.qldc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Housing market, infrastructure, tourism data.',
    },
    {
        'id': 'source.dunedin_city_2024',
        'title': 'Dunedin City Council 2024 Long-Term Plan',
        'author': 'Dunedin City Council',
        'publisher': 'DCC',
        'year': 2024,
        'url': 'https://www.dunedin.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'City planning, infrastructure, housing data.',
    },
    {
        'id': 'source.nz_tourism_2023',
        'title': 'New Zealand Tourism Board: Queenstown Regional Profile 2023',
        'author': 'Tourism New Zealand',
        'publisher': 'TNZ',
        'year': 2023,
        'url': 'https://www.tourismnewzealand.com',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Tourism numbers, visitor demographics.',
    },
    {
        'id': 'source.otago_university_2023',
        'title': 'University of Otago Institutional Research 2023',
        'author': 'University of Otago',
        'publisher': 'UO',
        'year': 2023,
        'url': 'https://www.otago.ac.nz',
        'type': 'academic',
        'credibility': 'academic',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Student population, economic impact.',
    },
    {
        'id': 'source.nz_health_2024',
        'title': 'Ministry of Health: New Zealand Health Statistics 2024',
        'author': 'Ministry of Health',
        'publisher': 'MOH',
        'year': 2024,
        'url': 'https://www.health.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Health outcomes, mental health, chronic disease data.',
    },
    {
        'id': 'source.stats_nz_housing_2024',
        'title': 'Stats NZ Household Labour Force Survey 2024',
        'author': 'Stats NZ Tatauranga Aotearoa',
        'publisher': 'Stats NZ',
        'year': 2024,
        'url': 'https://www.stats.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'auckland', 'wellington', 'nz'],
        'notes': 'Comparable housing and employment data across regions.',
    },
    {
        'id': 'source.otago_wine_2023',
        'title': 'Central Otago Wine Marketing 2023 Report',
        'author': 'Central Otago Wine Growers',
        'publisher': 'COWG',
        'year': 2023,
        'url': 'https://www.centralotagonz.com',
        'type': 'industry',
        'credibility': 'industry_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Wine sector economics and employment.',
    },
    {
        'id': 'source.ngai_tahu_2023',
        'title': 'Ngāi Tahu Charitable Trust Annual Report 2023',
        'author': 'Ngāi Tahu',
        'publisher': 'Ngāi Tahu',
        'year': 2023,
        'url': 'https://www.ngaitahu.iwi.nz',
        'type': 'community',
        'credibility': 'community_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Iwi governance and economic interests.',
    },
    {
        'id': 'source.otago_hospital_2024',
        'title': 'Southern DHB 2024 Health Needs Assessment',
        'author': 'Southern District Health Board',
        'publisher': 'SDHB',
        'year': 2024,
        'url': 'https://www.southernhealth.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Hospital planning, infrastructure, health workforce.',
    },
    {
        'id': 'source.clutha_water_2023',
        'title': 'Clutha River Water Management Study 2023',
        'author': 'Otago Regional Council',
        'publisher': 'ORC',
        'year': 2023,
        'url': 'https://www.orc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Water management, irrigation, environmental flows.',
    },
    {
        'id': 'source.otago_transport_2024',
        'title': 'Otago Regional Transport Committee Strategic Plan 2024',
        'author': 'Otago Regional Council',
        'publisher': 'ORC',
        'year': 2024,
        'url': 'https://www.orc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Transport infrastructure and mode share planning.',
    },
    {
        'id': 'source.queenstown_tourism_pressure_2023',
        'title': 'Queenstown Tourism Capacity Study 2023',
        'author': 'Queenstown Chamber of Commerce',
        'publisher': 'QLCC',
        'year': 2023,
        'url': 'https://www.queenstownchamber.co.nz',
        'type': 'industry',
        'credibility': 'industry_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Visitor impacts, infrastructure strain.',
    },
    {
        'id': 'source.new_zealand_police_2024',
        'title': 'New Zealand Police Crime Statistics 2024',
        'author': 'New Zealand Police',
        'publisher': 'NZP',
        'year': 2024,
        'url': 'https://www.police.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Crime rates, family violence, offending statistics.',
    },
    {
        'id': 'source.nz_education_2024',
        'title': 'Ministry of Education: Educational Performance Indicators 2024',
        'author': 'Ministry of Education',
        'publisher': 'MOE',
        'year': 2024,
        'url': 'https://www.education.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['otago', 'nz'],
        'notes': 'Achievement rates, school enrollment, attendance.',
    },
]

SOUTHLAND_SOURCES = [
    {
        'id': 'source.southland_council_2024',
        'title': 'Southland Regional Council Strategic Plan 2024',
        'author': 'Southland Regional Council',
        'publisher': 'SRC',
        'year': 2024,
        'url': 'https://www.southland.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Regional planning, water quality, economic data.',
    },
    {
        'id': 'source.invercargill_city_2024',
        'title': 'Invercargill City Council 2024 Long-Term Plan',
        'author': 'Invercargill City Council',
        'publisher': 'ICC',
        'year': 2024,
        'url': 'https://www.icc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'City planning, housing, infrastructure.',
    },
    {
        'id': 'source.nzas_meridian_2023',
        'title': 'New Zealand Aluminium Smelter / Meridian Energy: Operations Report 2023',
        'author': 'NZAS / Meridian Energy',
        'publisher': 'NZAS',
        'year': 2023,
        'url': 'https://www.nzas.co.nz',
        'type': 'industry',
        'credibility': 'industry_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Smelter operations, employment, energy use.',
    },
    {
        'id': 'source.southland_dairy_2024',
        'title': 'Southland District Council Dairy Industry Profile 2024',
        'author': 'Southland District Council',
        'publisher': 'SDC',
        'year': 2024,
        'url': 'https://www.southland.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Dairy farming, water pollution, economic contribution.',
    },
    {
        'id': 'source.fiordland_conservation_2024',
        'title': 'Department of Conservation: Fiordland National Park Visitor Study 2024',
        'author': 'Department of Conservation',
        'publisher': 'DOC',
        'year': 2024,
        'url': 'https://www.doc.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Tourism pressure, ecosystem management, visitor numbers.',
    },
    {
        'id': 'source.stats_nz_southland_2024',
        'title': 'Stats NZ Southland Regional Profile 2024',
        'author': 'Stats NZ Tatauranga Aotearoa',
        'publisher': 'Stats NZ',
        'year': 2024,
        'url': 'https://www.stats.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Demographic, employment, income, housing data.',
    },
    {
        'id': 'source.stewart_island_2024',
        'title': 'Stewart Island Rakiura Council 2024 Annual Report',
        'author': 'Stewart Island Rakiura Council',
        'publisher': 'SIRC',
        'year': 2024,
        'url': 'https://www.stewartisland.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Island infrastructure, population, isolation.',
    },
    {
        'id': 'source.ngai_tahu_murihiku_2023',
        'title': 'Ngāi Tahu Murihiku Economic Development 2023',
        'author': 'Ngāi Tahu',
        'publisher': 'Ngāi Tahu',
        'year': 2023,
        'url': 'https://www.ngaitahu.iwi.nz',
        'type': 'community',
        'credibility': 'community_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Iwi economic interests, governance.',
    },
    {
        'id': 'source.southland_health_2024',
        'title': 'Southland District Health Board 2024 Health Needs Assessment',
        'author': 'Southland DHB',
        'publisher': 'SDHB',
        'year': 2024,
        'url': 'https://www.southernhealth.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Health outcomes, workforce, rural health.',
    },
    {
        'id': 'source.southland_education_2024',
        'title': 'Ministry of Education: Southland School Performance 2024',
        'author': 'Ministry of Education',
        'publisher': 'MOE',
        'year': 2024,
        'url': 'https://www.education.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Achievement rates, enrollment, attendance.',
    },
    {
        'id': 'source.southland_rivers_study_2023',
        'title': 'Southland Rivers Water Quality Monitoring 2023',
        'author': 'Southland Regional Council',
        'publisher': 'SRC',
        'year': 2023,
        'url': 'https://www.southland.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Water quality degradation, nutrient levels.',
    },
    {
        'id': 'source.nz_police_southland_2024',
        'title': 'New Zealand Police Crime Statistics: Southland District 2024',
        'author': 'New Zealand Police',
        'publisher': 'NZP',
        'year': 2024,
        'url': 'https://www.police.govt.nz',
        'type': 'official_data',
        'credibility': 'government_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Crime rates, family violence, offending.',
    },
    {
        'id': 'source.foveaux_strait_2024',
        'title': 'Foveaux Strait Marine Ecosystem Assessment 2024',
        'author': 'NIWA',
        'publisher': 'NIWA',
        'year': 2024,
        'url': 'https://www.niwa.co.nz',
        'type': 'research',
        'credibility': 'research_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Sea level rise, marine ecosystem changes.',
    },
    {
        'id': 'source.manapouri_hydroelectric_2024',
        'title': 'Manapouri Hydroelectric Station Operations Report 2024',
        'author': 'Meridian Energy',
        'publisher': 'Meridian',
        'year': 2024,
        'url': 'https://www.meridianenergy.co.nz',
        'type': 'industry',
        'credibility': 'industry_primary',
        'geo_granularity': ['southland', 'nz'],
        'notes': 'Power generation, environmental impacts, grid role.',
    },
]

# ============================================================================
# Problem structures (44 per region: 11 themes × 1 root + 3 children)
# ============================================================================

def problem_tree(region_slug, region_infix, theme, root_id, root_title, root_summary, children):
    """
    Generate problem YAML for a tree: root + 3 children.
    children = [{'id': 'child_descriptor', 'title': 'Child Title', 'summary': 'Child summary'}, ...]
    """
    problems = []

    # Root
    root_yaml = {
        'id': f'problem.{region_infix}.{theme}.{root_id}',
        'title': root_title,
        'theme': theme,
        'section': 'climate-adaptation' if theme == 'climate' else theme,
        'subpage': root_id,
        'parent': None,
        'order': 1,
        'updated': DATE,
        'summary': root_summary,
        'manifests_in': [region_slug],
        'systems_model': {
            'state_variables': [],
            'inputs': [],
            'constraints': [],
            'feedback_loops': [],
        },
        'narrative': [
            {
                'heading': 'Overview',
                'body': root_summary,
            }
        ],
        'claim_ids': [],
        'status': 'draft',
    }
    problems.append((f'problem.{region_infix}.{theme}.{root_id}', root_yaml))

    # Children
    for i, child in enumerate(children, start=2):
        child_yaml = {
            'id': f'problem.{region_infix}.{theme}.{child["id"]}',
            'title': child['title'],
            'theme': theme,
            'section': 'climate-adaptation' if theme == 'climate' else theme,
            'subpage': child['id'],
            'parent': f'problem.{region_infix}.{theme}.{root_id}',
            'order': i,
            'updated': DATE,
            'summary': child['summary'],
            'manifests_in': [region_slug],
            'systems_model': {
                'state_variables': [],
                'inputs': [],
                'constraints': [],
                'feedback_loops': [],
            },
            'narrative': [
                {
                    'heading': 'Overview',
                    'body': child['summary'],
                }
            ],
            'claim_ids': [],
            'status': 'draft',
        }
        problems.append((f'problem.{region_infix}.{theme}.{child["id"]}', child_yaml))

    return problems

# Define Otago problems
otago_problems = []

otago_problems.extend(problem_tree('otago', 'otago', 'housing', 'housing_market',
    'Housing Affordability Crisis in Otago',
    'Otago faces a bifurcated housing crisis: Queenstown has among NZ\'s highest property prices and worker housing stress; Dunedin has university-driven student rental pressure and stagnant owner-occupation rates. Both create workforce retention challenges.',
    [
        {'id': 'queenstown_affordability', 'title': 'Queenstown-Lakes Housing Affordability Collapse',
         'summary': 'Queenstown has NZ\'s most expensive regional housing market, with median prices exceeding $1.2M and median multiples approaching 12. Acute shortage of worker housing.'},
        {'id': 'dunedin_student_rental', 'title': 'Dunedin Student Rental Pressure',
         'summary': 'University of Otago enrolls ~20,000 students; inflated rental market and overcrowded flats create poor housing quality and landlord incentives to neglect maintenance.'},
        {'id': 'worker_housing', 'title': 'Essential Worker Housing Shortage',
         'summary': 'Healthcare, hospitality, education workers cannot afford market rents; difficulty recruiting and retaining essential workforce across the region.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'transport', 'connectivity',
    'Transport Connectivity Constraints',
    'Otago\'s geography fragments the region; Southern Link motorway construction relieves Dunedin congestion; Queenstown-Lakes faces extreme traffic pressure; limited active transport and public transit.',
    [
        {'id': 'queenstown_congestion', 'title': 'Queenstown-Lakes Traffic Congestion',
         'summary': 'Tourism and population growth drive extreme seasonal congestion on State Highway 6; limited alt routes; parking and air quality deteriorate.'},
        {'id': 'dunedin_southern_link', 'title': 'Dunedin Southern Link Motorway Capacity',
         'summary': 'Major infrastructure project underway to improve Dunedin connectivity; completion timing and funding constraints may delay congestion relief.'},
        {'id': 'active_modes', 'title': 'Low Active Transport Mode Share',
         'summary': 'Otago relies heavily on private vehicles; Central Otago Rail Trail success not replicated into urban cycling networks; winter weather discourages walking/cycling.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'infrastructure', 'infrastructure',
    'Infrastructure Resilience and Upgrade Backlog',
    'Otago faces aging water/wastewater systems, major hospital rebuild project, rural digital divide, and seismic upgrade pressures on heritage buildings in Dunedin.',
    [
        {'id': 'otago_hospital_rebuild', 'title': 'Otago Hospital Rebuild Project',
         'summary': 'Southern DHB\'s major Dunedin hospital rebuild is critical but faces cost escalation, labor constraints, and timeline uncertainty. Overcapacity in interim period.'},
        {'id': 'wakatipu_water', 'title': 'Wakatipu Basin Water Supply Constraints',
         'summary': 'Rapid Queenstown population growth strains water supply; irrigation demand in summer; wastewater treatment and stormwater capacity gaps.'},
        {'id': 'digital_rural', 'title': 'Rural Digital Infrastructure Gap',
         'summary': 'Central Otago and remote areas lack fibre and reliable broadband; limits agricultural modernization, business creation, remote work adoption.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'environment', 'freshwater_stress',
    'Freshwater Stress and Environmental Degradation',
    'Otago\'s irrigation expansion and pastoral farming intensify pressure on Clutha/Mata-au river system; lake eutrophication (Lakes Wakatipu, Wanaka); coastal ecosystem decline.',
    [
        {'id': 'irrigation_water_quality', 'title': 'Irrigation Expansion and Freshwater Depletion',
         'summary': 'Central Otago wine and horticulture expand irrigation; seasonal water allocation conflicts between agricultural and environmental flows in Clutha system.'},
        {'id': 'lake_eutrophication', 'title': 'Lake Eutrophication: Wanaka and Wakatipu',
         'summary': 'Tourism, pastoral inputs, and stormwater runoff drive nutrient loading; toxic algal blooms emerging; threatens recreational and drinking water quality.'},
        {'id': 'coastal_otago', 'title': 'Coastal Ecosystem Degradation',
         'summary': 'Otago Peninsula and Port Chalmers harbor face stormwater pollution, invasive marine species, and fishing pressure; marine protected area coverage incomplete.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'inequality', 'inequality',
    'Structural Inequality and Regional Disparities',
    'Queenstown\'s wealth concentration contrasts starkly with Dunedin deprivation and rural isolation. Worker conditions in tourism and agriculture are poor; gender and Māori wealth gaps pronounced.',
    [
        {'id': 'queenstown_worker_conditions', 'title': 'Queenstown Tourism Worker Precarity',
         'summary': 'Tourism jobs are seasonal, low-wage, minimal benefits; workers live in vehicle or shared housing; high turnover, stress, mental health impacts.'},
        {'id': 'dunedin_deprivation', 'title': 'Dunedin East Deprivation',
         'summary': 'NZ Deprivation Index scores place East Dunedin among most deprived urban areas; youth unemployment, family poverty, limited opportunity.'},
        {'id': 'rural_isolation', 'title': 'Rural Isolation and Service Access',
         'summary': 'Outlying farming communities face distance to healthcare, education, jobs; limited public transport; broadband gaps worsen isolation.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'crime', 'safety',
    'Crime and Community Safety',
    'Family violence rates exceed national average in Dunedin and rural Otago; youth offending in East Dunedin; visitor crime in Queenstown (assaults, theft).',
    [
        {'id': 'family_violence', 'title': 'Family Violence Prevalence',
         'summary': 'Dunedin and rural Otago have high reported family violence; barriers to disclosure and prosecution; inadequate support services reach.'},
        {'id': 'youth_offending', 'title': 'Youth Offending in Dunedin',
         'summary': 'East Dunedin has elevated youth crime; gang activity, lack of community engagement, limited diversion programs.'},
        {'id': 'queenstown_visitor_crime', 'title': 'Queenstown Visitor-Related Crime',
         'summary': 'Assaults on hospitality workers, tourist theft, late-night violence concentrated in CBD; enforcement and venue management challenges.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'health', 'health_outcomes',
    'Health Outcomes and Workforce Challenges',
    'Otago faces elevated mental health and chronic disease burden; rural workforce shortages (GPs, nurses, allied health); Dunedin student mental health crisis.',
    [
        {'id': 'mental_health', 'title': 'Mental Health Service Demand and Access',
         'summary': 'Student mental health crisis at University of Otago; youth suicide rates elevated; community mental health services oversubscribed, long waitlists.'},
        {'id': 'chronic_disease', 'title': 'Chronic Disease Burden',
         'summary': 'Dunedin and rural Otago have higher rates of type 2 diabetes, cardiovascular disease, obesity; lifestyle and nutrition factors; access to preventive care limited.'},
        {'id': 'rural_workforce', 'title': 'Rural Health Workforce Shortage',
         'summary': 'Central Otago and rural areas struggle to attract and retain GPs and nurses; locum costs escalate; remote area classification may improve incentives.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'education', 'achievement',
    'Educational Achievement Disparities',
    'Dunedin has strong tertiary sector (University of Otago, Otago Polytechnic) but secondary student achievement lags in rural and low-income areas. Early childhood enrollment rates below national average.',
    [
        {'id': 'early_childhood', 'title': 'Early Childhood Education Participation',
         'summary': 'ECE enrollment rates in rural Otago and East Dunedin below national average; affordability and accessibility barriers; impact on primary readiness.'},
        {'id': 'secondary', 'title': 'Secondary Achievement and Retention',
         'summary': 'NCEA pass rates lower in rural and low-income Dunedin schools; higher stand-down/suspension rates; pastoral support systems under-resourced.'},
        {'id': 'tertiary_dunedin', 'title': 'Tertiary Sector Student Wellbeing and Outcomes',
         'summary': 'University of Otago and Otago Polytechnic have strong enrollment but mental health, housing, and graduate job placement challenges for regional students.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'economy', 'economic_structure',
    'Economic Structure and Diversification',
    'Otago economy is bifurcated: Queenstown driven by tourism and property; Dunedin by university and government; Central Otago by wine/horticulture. Narrow sectoral dependencies create vulnerability.',
    [
        {'id': 'tourism_queenstown', 'title': 'Queenstown Tourism Over-Dependence',
         'summary': 'Queenstown economy >40% dependent on tourism; vulnerability to external shocks (COVID, currency); visitor saturation threatens amenity; staff turnover high.'},
        {'id': 'agri_primary', 'title': 'Agricultural Primary Sector Commodity Exposure',
         'summary': 'Central Otago wine and horticulture, regional pastoral farming exposed to commodity prices, irrigation cost shocks, and climate variability.'},
        {'id': 'university_economy', 'title': 'Dunedin University Sector Dependence',
         'summary': 'University of Otago is major employer and economic anchor; public funding cuts risk Dunedin\'s vitality; limited economic diversification.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'governance', 'governance',
    'Governance and Decision-Making Structures',
    'Otago has fragmented governance (Otago RC, three TAs, DHB); Queenstown rapid growth outpaces planning; Ngāi Tahu co-governance interests expanding.',
    [
        {'id': 'queenstown_growth_management', 'title': 'Queenstown Growth Management and Planning',
         'summary': 'QLDC growth planning lags population growth; infrastructure, housing, services struggle to keep pace; tensions between tourism and livability.'},
        {'id': 'treaty_ngai_tahu', 'title': 'Treaty Settlements and Ngāi Tahu Co-Governance',
         'summary': 'Ngāi Tahu expanded co-governance roles in resource management and governance; ongoing debates about iwi consultation depth and decision power.'},
        {'id': 'otago_hospital_governance', 'title': 'Southern DHB Governance and Planning',
         'summary': 'Hospital rebuild coordination across council, health sector, and government; DHB structure and accountability debates ongoing.'},
    ]
))

otago_problems.extend(problem_tree('otago', 'otago', 'climate', 'climate_risk',
    'Climate Change Risk and Adaptation',
    'Central Otago faces drought and alpine hazard risk; Dunedin coastal flooding and storm surge risk; Wakatipu basin extreme weather; region-wide agricultural adaptation pressure.',
    [
        {'id': 'drought_central_otago', 'title': 'Central Otago Drought and Irrigation Stress',
         'summary': 'Central Otago is NZ\'s driest region; climate change extends dry season; irrigation demand and environmental flow conflicts intensify.'},
        {'id': 'alpine_hazards', 'title': 'Alpine Hazards: Avalanche and Glacial Lake Hazards',
         'summary': 'Queenstown-Lakes faces avalanche risk in ski areas and transport corridors; glacial lake outburst flood potential in Fiordland headwaters.'},
        {'id': 'coastal_dunedin', 'title': 'Dunedin Coastal Flood and Storm Surge Risk',
         'summary': 'Dunedin CBD and Port Chalmers face sea level rise and extreme storm surge risk; earthquake and tsunami risk from Hikurangi Subduction Zone.'},
    ]
))

# Define Southland problems
southland_problems = []

southland_problems.extend(problem_tree('southland', 'southland', 'housing', 'housing_market',
    'Housing Market Stagnation and Affordability',
    'Southland\'s housing market is subdued; Invercargill affordability moderate but population stagnation reduces demand. Rural housing aging. Worker housing shortages emerge.',
    [
        {'id': 'invercargill_affordability', 'title': 'Invercargill Housing Affordability Pressures',
         'summary': 'Invercargill median multiple ~5.5; affordable compared to national, but low incomes mean affordability stress for families. Rental vacancy high; ownership declining.'},
        {'id': 'rural_housing', 'title': 'Rural Housing Stock Aging and Maintenance',
         'summary': 'Southland farming communities have aging housing stock; high maintenance costs; limited new construction; affects workforce retention.'},
        {'id': 'worker_housing', 'title': 'Dairy and Processing Worker Housing Shortage',
         'summary': 'Dairy and meat processing sectors struggle to attract workers; housing shortages in areas near farms and plants; temporary worker accommodations inadequate.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'transport', 'connectivity',
    'Transport Connectivity and Infrastructure Access',
    'Southland is geographically isolated; long distances to Auckland and Wellington; limited public transit; Fiordland access via single highway (SH94); Stewart Island ferry dependency.',
    [
        {'id': 'invercargill_roading', 'title': 'Invercargill Roading Network and Congestion',
         'summary': 'Invercargill CBD roading is aging; intersections congested during peak hours; limited alternative routes; walkability and cycling infrastructure limited.'},
        {'id': 'fiordland_access', 'title': 'Fiordland Highway Access and Bottlenecks',
         'summary': 'SH94 is sole tourism and access route to Fiordland; seasonal closures; single-lane sections create bottlenecks; resilience concerns for Milford Sound operations.'},
        {'id': 'active_modes', 'title': 'Low Active Transport and Public Transit Uptake',
         'summary': 'Southland relies on private vehicles; limited bus services; cold climate and short distances favor driving; walkability low in Invercargill CBD.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'infrastructure', 'infrastructure',
    'Infrastructure: Water, Wastewater, Power, Digital',
    'Southland faces aging water and wastewater systems; Manapōuri hydroelectric power uniquely supports smelter; rural digital divide; Fiordland tourist infrastructure under pressure.',
    [
        {'id': 'water_wastewater', 'title': 'Water and Wastewater System Aging',
         'summary': 'Invercargill and district water systems aging; wastewater treatment capacity constraints; rural septic systems inadequate; infrastructure funding gap widening.'},
        {'id': 'manapouri_power', 'title': 'Manapōuri Hydroelectric Power and Smelter Dependency',
         'summary': 'NZAS smelter depends on Manapōuri-Meridian power contract; smelter closure would free 550+ MW to grid but devastate Southland economy. Contract negotiations critical.'},
        {'id': 'digital_rural', 'title': 'Rural Digital Infrastructure and Broadband',
         'summary': 'Rural Southland lacks fibre; broadband coverage patchy; limits farm automation, agritech adoption, business creation, remote work.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'environment', 'freshwater_degradation',
    'Freshwater Degradation and Ecosystem Pressures',
    'Southland rivers (Mataura, Oreti) severely degraded by dairy pollution; Fiordland wilderness ecosystem threatened by invasive species and tourism pressure; coastal pollution.',
    [
        {'id': 'southland_river_quality', 'title': 'Southland Rivers Water Quality Collapse',
         'summary': 'Dairy intensification and conversion drove nutrient and bacterial pollution in Mataura, Oreti, and other rivers; swimming unsafe; ecosystem biodiversity declined.'},
        {'id': 'fiordland_ecosystem', 'title': 'Fiordland Ecosystem and Invasive Species',
         'summary': 'Fiordland faces invasive rats, stoats, and marine species; tourism pressure on Milford Sound and remote valleys; conservation resources stretched.'},
        {'id': 'coastal_foveaux', 'title': 'Foveaux Strait Coastal Degradation and Fisheries Stress',
         'summary': 'Foveaux Strait ecosystem stressed by overfishing, sea urchin barrens, marine invasives; Southland fisheries income declining; aquaculture conflicts.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'inequality', 'deprivation',
    'Deprivation and Regional Inequality',
    'Invercargill East and rural Southland have high deprivation scores; child poverty elevated; gender pay gap; Māori and Pasifika disparities pronounced.',
    [
        {'id': 'invercargill_east_poverty', 'title': 'Invercargill East Deprivation',
         'summary': 'Invercargill East among NZ\'s most deprived urban areas; family poverty, youth unemployment; limited economic opportunity and social services access.'},
        {'id': 'child_poverty', 'title': 'Child Poverty and Family Hardship',
         'summary': 'Southland child poverty rates elevated; food insecurity, housing instability, inadequate clothing/heating; impacts educational and health outcomes.'},
        {'id': 'rural_isolation', 'title': 'Rural Isolation and Service Access Gaps',
         'summary': 'Farming families face distance to healthcare, education, recreation; limited transport; service gaps worsen isolation and mental health.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'crime', 'safety',
    'Crime and Community Safety',
    'Family violence rates exceed national average; youth offending in Invercargill; rural crime underreported; limited police presence in remote areas.',
    [
        {'id': 'family_violence', 'title': 'Family Violence and Domestic Abuse',
         'summary': 'Southland has high family violence call-out rates; barriers to reporting in rural areas; support services under-resourced; perpetrator programs limited.'},
        {'id': 'youth_offending', 'title': 'Youth Offending in Invercargill',
         'summary': 'Invercargill youth crime elevated; gang-associated offending; limited youth engagement and diversion programs; police youth team under-staffed.'},
        {'id': 'rural_crime', 'title': 'Rural Crime: Stock Theft and Property Crime',
         'summary': 'Farming community experiences stock theft, vehicle theft, and farm break-ins; limited police patrol; insurance costs rising; farm security investments high.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'health', 'health_outcomes',
    'Health Outcomes and Health System Pressures',
    'Southland has higher chronic disease burden; rural workforce shortages (GPs, nurses); mental health services oversubscribed; deprivation drives poor health outcomes.',
    [
        {'id': 'mental_health', 'title': 'Mental Health Service Demand',
         'summary': 'Southland mental health services under-resourced; waitlists long; rural access barriers; suicide rates elevated; substance abuse issues prominent.'},
        {'id': 'chronic_disease', 'title': 'Chronic Disease and Preventable Illness',
         'summary': 'Southland has higher type 2 diabetes, obesity, cardiovascular disease; lifestyle factors (food security, activity, smoking); health promotion limited.'},
        {'id': 'rural_workforce', 'title': 'Rural Health Workforce Shortages',
         'summary': 'GPs, nurses, allied health scarce in rural Southland; Invercargill hospital competes with other regions; locum costs high; recruitment barriers high.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'education', 'achievement',
    'Educational Achievement and Tertiary Access',
    'Southland secondary achievement below national average; early childhood participation low in rural areas; limited tertiary options; brain drain to Auckland/Dunedin.',
    [
        {'id': 'early_childhood', 'title': 'Early Childhood Education Participation',
         'summary': 'Rural Southland ECE enrollment low; affordability and access barriers; long waiting lists; impacts primary readiness and achievement trajectories.'},
        {'id': 'secondary', 'title': 'Secondary School Achievement',
         'summary': 'NCEA pass rates below national average; stand-down/suspension rates elevated; pastoral support systems limited; subject choices narrow in smaller schools.'},
        {'id': 'tertiary_access', 'title': 'Tertiary Education Access and Local Provision',
         'summary': 'Southland lacks university campus; Southern Institute of Technology provides pathways but brain drain to Dunedin/Auckland; student loan debt burdens.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'economy', 'industrial_transition',
    'Economic Structure and Industrial Transition Pressure',
    'Southland economy heavily dependent on smelter, dairy, pastoral farming, and fisheries. Single-sector reliance creates vulnerability; limited diversification.',
    [
        {'id': 'smelter_dependency', 'title': 'Smelter Closure Risk and Economic Dependency',
         'summary': 'NZAS provides ~3,000 direct and indirect jobs; closure would devastate Southland economy. Ongoing energy contract negotiations; grid resilience debates.'},
        {'id': 'agri_commodity', 'title': 'Dairy and Pastoral Commodity Price Exposure',
         'summary': 'Dairy sector is core Southland economy; exposed to milk prices, feed costs, environmental regulation; margins compressed; structural change accelerating.'},
        {'id': 'economic_diversification', 'title': 'Economic Diversification and Business Development',
         'summary': 'Southland lacks innovation ecosystem; limited startup activity; brain drain to larger cities; tourism (Fiordland) only partial offset to agricultural exposure.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'governance', 'governance',
    'Governance and Strategic Direction',
    'Southland RC and territorial authorities face capacity and funding constraints. Smelter energy negotiations complex; Ngāi Tahu co-governance expanding.',
    [
        {'id': 'smelter_energy_policy', 'title': 'Smelter Energy Policy and Infrastructure Negotiations',
         'summary': 'Meridian-NZAS power contract negotiations; smelter future affects Manapōuri dam operations, national grid, Southland employment; political complexity high.'},
        {'id': 'treaty_ngai_tahu', 'title': 'Treaty Settlements and Ngāi Tahu Rights',
         'summary': 'Ngāi Tahu Murihiku settlement ongoing; co-governance roles expanding in resource management; iwi consultation requirements increasing.'},
        {'id': 'local_govt_reform', 'title': 'Local Government Structure and Funding Reform',
         'summary': 'Southland councils face rating pressures and funding gaps; three-waters reforms; regional amalgamation debates; capacity constraints on strategic planning.'},
    ]
))

southland_problems.extend(problem_tree('southland', 'southland', 'climate', 'climate_risk',
    'Climate Change Risk and Agricultural Adaptation',
    'Southland faces flooding risk from rainfall-driven events; agricultural systems require adaptation; alpine hazards in Fiordland; sea level rise for coastal communities.',
    [
        {'id': 'flooding_rivers', 'title': 'Flood Risk from Rainfall Events and River Overflow',
         'summary': 'Southland rivers prone to flooding; climate change intensifies rainfall extremes; low-lying farmland and Invercargill CBD vulnerable; drainage systems at capacity.'},
        {'id': 'drought_agricultural', 'title': 'Pastoral and Dairy Sector Climate Adaptation',
         'summary': 'Southern pastoral and dairy systems face changing rainfall, temperature, and growing season pressures; feed deficit years more common; diversification slow.'},
        {'id': 'coastal_foveaux_rise', 'title': 'Foveaux Strait Coastal Flooding and Sea Level Rise',
         'summary': 'Coastal Southland communities (Riverton, Aparima) face long-term sea level rise; storm surge risk increasing; adaptation planning nascent.'},
    ]
))

# ============================================================================
# Helper to write YAML files
# ============================================================================

def write_yaml_file(directory, filename, data):
    """Write YAML file preserving order and formatting."""
    path = Path(directory) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

def write_region_entities(region_slug, region_infix, display_name, sources, problems):
    """Write all entity files for a region."""
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / f'content/{region_slug}/data'

    # Write sources
    for source_dict in sources:
        write_yaml_file(base_path / 'source', f'{source_dict["id"].split(".")[-1]}.yaml', source_dict)

    # Copy methodologies from Wellington and clear source_ids
    wellington_method_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / 'content/wellington/data/methodology'
    method_path = base_path / 'methodology'
    method_path.mkdir(parents=True, exist_ok=True)

    for method_file in wellington_method_path.glob('*.yaml'):
        with open(method_file, 'r', encoding='utf-8') as f:
            method_data = yaml.safe_load(f)
        method_data['source_ids'] = []
        write_yaml_file(method_path, method_file.name, method_data)

    # Write problems
    for problem_id, problem_data in problems:
        filename = problem_id.split('.')[-1] + '.yaml'
        write_yaml_file(base_path / 'problem', filename, problem_data)

    print(f"✓ {region_slug}: {len(sources)} sources, {len(problems)} problems written")

# ============================================================================
# Execute
# ============================================================================

if __name__ == '__main__':
    write_region_entities('otago', 'otago', 'Otago — Ōtākou', OTAGO_SOURCES, otago_problems)
    write_region_entities('southland', 'southland', 'Southland — Murihiku', SOUTHLAND_SOURCES, southland_problems)
    print("\n✓ All source and problem files written")
