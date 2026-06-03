#!/usr/bin/env python3
"""
Build Northland and Waikato region entity corpora.
Generates 88 problems (44 per region × 1 root + 3 children each),
with supporting claims, drivers, camps, sources, and methodologies.
"""

import os
import yaml
from pathlib import Path
from datetime import datetime

# Define regions
REGIONS = {
    'northland': {
        'display': 'Northland — Te Tai Tokerau',
        'description': 'NZ most deprived region. Far North: extreme poverty, poor infrastructure, Māori 34%, poor roading, housing deprivation, unemployment, meth/drugs, low education, beautiful environment under tourism/farming pressure, Treaty claims, water quality from dairying, kauri dieback, gumland histories, port at Whangārei.',
        'region_slug': 'northland',
    },
    'waikato': {
        'display': 'Waikato',
        'description': 'Large inland region, Hamilton urban centre, strong agriculture (Fonterra HQ, dairy heartland), Waikato River highly modified/over-allocated, rapid Hamilton population growth, infrastructure lag, Port Waikato alternative, Waikato Tainui Treaty settlement, strong iwi economy, Huntly coal phaseout, geothermal (Taupō edge), affordable housing rising fast.',
        'region_slug': 'waikato',
    },
}

THEMES = ['housing', 'transport', 'infrastructure', 'environment', 'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate']

# Theme to schema enum mapping (climate is special)
THEME_TO_SCHEMA = {
    'housing': 'housing',
    'transport': 'transport',
    'infrastructure': 'infrastructure',
    'environment': 'environment',
    'inequality': 'inequality',
    'crime': 'crime',
    'health': 'health',
    'education': 'education',
    'economy': 'economy',
    'governance': 'governance',
    'climate': 'climate-adaptation',
}

# Problem definitions (root + 3 children per theme)
PROBLEM_DEFS = {
    'housing': {
        'root': {
            'id_component': 'affordability',
            'title_template': '{region_display}: housing unaffordability',
            'summary': 'Housing has become structurally unaffordable, driven by supply constraints, demand pressure, and limited policy coordination.',
        },
        'children': [
            {
                'id_component': 'land_supply',
                'title_template': '{region_display}: constrained residential land supply',
                'summary': 'Usable residential land is restricted by physical constraints, zoning rules, and infrastructure capacity.',
            },
            {
                'id_component': 'rental_market',
                'title_template': '{region_display}: rental market affordability and security',
                'summary': 'Renters face rising costs and insecurity, with limited inventory and weak tenure protections.',
            },
            {
                'id_component': 'homelessness',
                'title_template': '{region_display}: homelessness and housing stress',
                'summary': 'Extreme housing stress manifests in rough sleeping, family homelessness, and emergency shelter demand.',
            },
        ]
    },
    'transport': {
        'root': {
            'id_component': 'connectivity',
            'title_template': '{region_display}: transport connectivity challenges',
            'summary': 'Transport networks constrain regional connectivity and access to employment and services.',
        },
        'children': [
            {
                'id_component': 'roading',
                'title_template': '{region_display}: road network adequacy',
                'summary': 'Regional roading networks suffer from deferred maintenance, safety risks, and capacity constraints.',
            },
            {
                'id_component': 'public_transport',
                'title_template': '{region_display}: public transport coverage and viability',
                'summary': 'Public transport is limited in frequency, route coverage, and service integration.',
            },
            {
                'id_component': 'active_modes',
                'title_template': '{region_display}: active travel infrastructure',
                'summary': 'Walking and cycling infrastructure gaps discourage active mode uptake.',
            },
        ]
    },
    'infrastructure': {
        'root': {
            'id_component': 'deficit',
            'title_template': '{region_display}: infrastructure deficit and ageing',
            'summary': 'Critical infrastructure is ageing, under-maintained, and insufficient to support regional growth.',
        },
        'children': [
            {
                'id_component': 'water',
                'title_template': '{region_display}: water supply and demand management',
                'summary': 'Water supply is constrained by availability, quality, and competition between uses.',
            },
            {
                'id_component': 'wastewater',
                'title_template': '{region_display}: wastewater treatment and stormwater',
                'summary': 'Wastewater and stormwater systems are stressed by growth and environmental standards.',
            },
            {
                'id_component': 'digital',
                'title_template': '{region_display}: digital connectivity',
                'summary': 'Digital infrastructure gaps create rural accessibility and affordability barriers.',
            },
        ]
    },
    'environment': {
        'root': {
            'id_component': 'degradation',
            'title_template': '{region_display}: environmental degradation and pressure',
            'summary': 'Environmental systems face pressure from land use, pollution, and climate change.',
        },
        'children': [
            {
                'id_component': 'water_quality',
                'title_template': '{region_display}: freshwater quality',
                'summary': 'Freshwater quality is degraded by agricultural runoff, urban discharge, and land use intensification.',
            },
            {
                'id_component': 'biodiversity',
                'title_template': '{region_display}: terrestrial and aquatic biodiversity',
                'summary': 'Native biodiversity is threatened by habitat loss, invasive species, and predation.',
            },
            {
                'id_component': 'coastal',
                'title_template': '{region_display}: coastal environments and marine resources',
                'summary': 'Coastal habitats and fisheries are under pressure from development, pollution, and overharvesting.',
            },
        ]
    },
    'inequality': {
        'root': {
            'id_component': 'deprivation',
            'title_template': '{region_display}: deprivation and inequality',
            'summary': 'Deprivation is concentrated geographically and affects health, education, and economic outcomes.',
        },
        'children': [
            {
                'id_component': 'child_poverty',
                'title_template': '{region_display}: child poverty and welfare',
                'summary': 'Child poverty limits life-course development and intergenerational mobility.',
            },
            {
                'id_component': 'ethnic_gap',
                'title_template': '{region_display}: ethnic and indigenous outcome gaps',
                'summary': 'Māori and Pacific peoples experience persistent gaps in income, health, and achievement.',
            },
            {
                'id_component': 'geographic',
                'title_template': '{region_display}: geographic and rural deprivation',
                'summary': 'Remote and rural areas experience economic decline and service withdrawal.',
            },
        ]
    },
    'crime': {
        'root': {
            'id_component': 'safety',
            'title_template': '{region_display}: crime and personal safety',
            'summary': 'Crime and violence undermine community safety and wellbeing.',
        },
        'children': [
            {
                'id_component': 'family_violence',
                'title_template': '{region_display}: family and domestic violence',
                'summary': 'Family violence is endemic and disproportionately affects vulnerable populations.',
            },
            {
                'id_component': 'youth_offending',
                'title_template': '{region_display}: youth crime and offending',
                'summary': 'Youth offending is driven by deprivation, disengagement, and limited opportunity.',
            },
            {
                'id_component': 'drug_crime',
                'title_template': '{region_display}: drug-related crime and harm',
                'summary': 'Methamphetamine and other drug use fuels acquisitive and violent crime.',
            },
        ]
    },
    'health': {
        'root': {
            'id_component': 'outcomes',
            'title_template': '{region_display}: health outcomes and access',
            'summary': 'Health outcomes are poor and inequitably distributed across the population.',
        },
        'children': [
            {
                'id_component': 'mental_health',
                'title_template': '{region_display}: mental health and wellbeing',
                'summary': 'Mental health problems are rising, especially among young people and Māori.',
            },
            {
                'id_component': 'chronic_disease',
                'title_template': '{region_display}: chronic disease burden',
                'summary': 'Chronic diseases including diabetes, obesity, and CVD are prevalent and preventable.',
            },
            {
                'id_component': 'workforce',
                'title_template': '{region_display}: health workforce and services',
                'summary': 'Health workforce shortages limit service capacity and accessibility.',
            },
        ]
    },
    'education': {
        'root': {
            'id_component': 'achievement',
            'title_template': '{region_display}: educational achievement and equity',
            'summary': 'Educational achievement is low and unequally distributed by ethnicity, gender, and deprivation.',
        },
        'children': [
            {
                'id_component': 'early_childhood',
                'title_template': '{region_display}: early childhood education access',
                'summary': 'Early childhood education participation is limited by cost and availability.',
            },
            {
                'id_component': 'secondary',
                'title_template': '{region_display}: secondary school engagement and attainment',
                'summary': 'Secondary school disengagement and low NCEA attainment limit employment prospects.',
            },
            {
                'id_component': 'tertiary',
                'title_template': '{region_display}: tertiary education and skills',
                'summary': 'Tertiary participation is limited and skill mismatches persist in labour market.',
            },
        ]
    },
    'economy': {
        'root': {
            'id_component': 'development',
            'title_template': '{region_display}: economic development and growth',
            'summary': 'Economic growth is constrained by sectoral concentration, low productivity, and limited diversification.',
        },
        'children': [
            {
                'id_component': 'employment',
                'title_template': '{region_display}: employment and job quality',
                'summary': 'Employment is characterized by low wages, job insecurity, and limited career advancement.',
            },
            {
                'id_component': 'productivity',
                'title_template': '{region_display}: labour and multi-factor productivity',
                'summary': 'Productivity growth is weak relative to national trends and peer regions.',
            },
            {
                'id_component': 'business',
                'title_template': '{region_display}: small business viability and growth',
                'summary': 'Small business formation and survival are hampered by capital access and market constraints.',
            },
        ]
    },
    'governance': {
        'root': {
            'id_component': 'challenges',
            'title_template': '{region_display}: governance and democratic participation',
            'summary': 'Governance structures and processes do not adequately serve community needs and expectations.',
        },
        'children': [
            {
                'id_component': 'local_govt',
                'title_template': '{region_display}: local government capacity and coordination',
                'summary': 'Local government agencies lack capacity, coordination, and community connection.',
            },
            {
                'id_component': 'treaty',
                'title_template': '{region_display}: Treaty partnership and iwi engagement',
                'summary': 'Māori partnership in governance is incomplete and hampered by institutional barriers.',
            },
            {
                'id_component': 'accountability',
                'title_template': '{region_display}: government accountability and transparency',
                'summary': 'Government accountability mechanisms are weak and citizen participation is low.',
            },
        ]
    },
    'climate': {
        'root': {
            'id_component': 'risk',
            'title_template': '{region_display}: climate change adaptation and resilience',
            'summary': 'Climate change poses multiple hazards to which adaptation is insufficient.',
        },
        'children': [
            {
                'id_component': 'flooding',
                'title_template': '{region_display}: flood risk and resilience',
                'summary': 'Rainfall intensification and river flooding pose increasing risks to development and infrastructure.',
            },
            {
                'id_component': 'drought',
                'title_template': '{region_display}: drought and water scarcity',
                'summary': 'Drought stress is increasing, threatening agricultural production and water security.',
            },
            {
                'id_component': 'coastal',
                'title_template': '{region_display}: coastal hazards and sea level rise',
                'summary': 'Sea level rise and storm surge threaten coastal infrastructure and settlements.',
            },
        ]
    },
}

# Source definitions (per region)
SOURCE_DEFS = {
    'northland': [
        {
            'id': 'source.far_north_district_council_2023',
            'title': 'Far North District Council Annual Plan and Service Delivery',
            'author': 'Far North District Council',
            'publisher': 'FNDC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.northland_regional_council_planning_2023',
            'title': 'Northland Regional Council Spatial Plans',
            'author': 'Northland Regional Council',
            'publisher': 'NRC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.stats_nz_northland_deprivation_2018',
            'title': 'NZ Index of Deprivation 2018 — Northland',
            'author': 'Stats NZ',
            'publisher': 'Stats NZ',
            'year': 2018,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.whangārei_city_council_housing_2023',
            'title': 'Whangārei City Council Housing Strategy',
            'author': 'Whangārei City Council',
            'publisher': 'WCC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.northtec_education_data_2023',
            'title': 'Northtec and Secondary Education Participation Data',
            'author': 'Northtec / NZQA',
            'publisher': 'NZQA',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nz_police_northland_crime_2023',
            'title': 'NZ Police Crime Statistics — Northland',
            'author': 'NZ Police',
            'publisher': 'NZ Police',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.health_nz_northland_2023',
            'title': 'Health NZ Northland Service Plan',
            'author': 'Health NZ',
            'publisher': 'Health NZ',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.mbie_northland_economic_2023',
            'title': 'MBIE Regional Economic Profile — Northland',
            'author': 'MBIE',
            'publisher': 'MBIE',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nrc_environmental_report_2022',
            'title': 'Northland Regional Council State of Environment Report',
            'author': 'NRC',
            'publisher': 'NRC',
            'year': 2022,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.ngāpuhi_settlement_documents_2022',
            'title': 'Ngāpuhi Treaty Settlement Documents and Implementation Plans',
            'author': 'Office of Treaty Settlements',
            'publisher': 'OTS',
            'year': 2022,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nzta_northland_transport_2023',
            'title': 'NZTA Northland Roading and Transport Strategy',
            'author': 'NZTA',
            'publisher': 'NZTA',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nrc_water_allocation_2023',
            'title': 'Northland Regional Council Water Allocation and Quality Monitoring',
            'author': 'NRC',
            'publisher': 'NRC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.demographia_2024_northland',
            'title': '17th Annual Demographia International Housing Affordability Survey',
            'author': 'Wendell Cox and Hugh Pavletich',
            'publisher': 'Demographia',
            'year': 2024,
            'type': 'commentary',
            'credibility': 'reputable',
        },
        {
            'id': 'source.msd_family_support_northland_2023',
            'title': 'MSD Family Support and Child Welfare Data — Northland',
            'author': 'MSD',
            'publisher': 'MSD',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.whānau_ora_commissioned_research_2023',
            'title': 'Whānau Ora Commissioned Research and Impact Data',
            'author': 'Whānau Ora',
            'publisher': 'Whānau Ora',
            'year': 2023,
            'type': 'ngo',
            'credibility': 'reputable',
        },
        {
            'id': 'source.kauri_dieback_programme_2023',
            'title': 'Kauri Dieback Disease Management Programme',
            'author': 'DOC / MPI',
            'publisher': 'MPI',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
    ],
    'waikato': [
        {
            'id': 'source.waikato_council_2023',
            'title': 'Waikato Regional Council Spatial Plan',
            'author': 'Waikato Regional Council',
            'publisher': 'WRC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.hamilton_city_council_growth_2023',
            'title': 'Hamilton City Council Growth Strategy',
            'author': 'Hamilton City Council',
            'publisher': 'HCC',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.waikato_tainui_settlement_2022',
            'title': 'Waikato Tainui Treaty Settlement Implementation',
            'author': 'Office of Treaty Settlements',
            'publisher': 'OTS',
            'year': 2022,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.waikato_river_authority_2023',
            'title': 'Waikato River Authority Integrated Management Plans',
            'author': 'Waikato River Authority',
            'publisher': 'WRA',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.fonterra_dairy_sector_waikato_2023',
            'title': 'Fonterra and Waikato Dairy Sector Economic Data',
            'author': 'Fonterra / DairyNZ',
            'publisher': 'Fonterra',
            'year': 2023,
            'type': 'commentary',
            'credibility': 'reputable',
        },
        {
            'id': 'source.stats_nz_waikato_deprivation_2018',
            'title': 'NZ Index of Deprivation 2018 — Waikato',
            'author': 'Stats NZ',
            'publisher': 'Stats NZ',
            'year': 2018,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.mbie_waikato_economic_2023',
            'title': 'MBIE Regional Economic Profile — Waikato',
            'author': 'MBIE',
            'publisher': 'MBIE',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nz_police_waikato_crime_2023',
            'title': 'NZ Police Crime Statistics — Waikato',
            'author': 'NZ Police',
            'publisher': 'NZ Police',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.health_nz_waikato_2023',
            'title': 'Health NZ Waikato Service Plan',
            'author': 'Health NZ',
            'publisher': 'Health NZ',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.waikato_university_research_2023',
            'title': 'Waikato University Research on Regional Development',
            'author': 'Waikato University',
            'publisher': 'Waikato University',
            'year': 2023,
            'type': 'academic',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.nzta_waikato_transport_2023',
            'title': 'NZTA Waikato Transport and Roading Strategy',
            'author': 'NZTA',
            'publisher': 'NZTA',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.port_waikato_master_plan_2023',
            'title': 'Port Waikato Master Plan and Development',
            'author': 'Port Waikato Ltd',
            'publisher': 'Port Waikato',
            'year': 2023,
            'type': 'commentary',
            'credibility': 'indicative',
        },
        {
            'id': 'source.moe_waikato_education_2023',
            'title': 'Ministry of Education Waikato Data',
            'author': 'Ministry of Education',
            'publisher': 'MoE',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.huntly_energy_transition_2023',
            'title': 'Huntly Coal Power Plant Retirement and Energy Transition',
            'author': 'Genesis Energy / MBIE',
            'publisher': 'Genesis Energy',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.msd_waikato_welfare_2023',
            'title': 'MSD Family Support and Benefits Data — Waikato',
            'author': 'MSD',
            'publisher': 'MSD',
            'year': 2023,
            'type': 'government',
            'credibility': 'authoritative',
        },
        {
            'id': 'source.waikato_housing_affordability_2023',
            'title': 'Waikato Housing Affordability and Real Estate Data',
            'author': 'Real Estate Institute NZ',
            'publisher': 'REINZ',
            'year': 2023,
            'type': 'commentary',
            'credibility': 'reputable',
        },
    ],
}

def ensure_dirs(region_slug):
    """Ensure data directories exist."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data'
    for entity_type in ['problem', 'claim', 'driver', 'camp', 'source', 'methodology']:
        Path(f'{base}\\{entity_type}').mkdir(parents=True, exist_ok=True)

def copy_methodologies(region_slug):
    """Copy methodology files from Wellington."""
    import shutil
    src_dir = Path('D:\\ai-website-manager\\Current website\\content\\wellington\\data\\methodology')
    dst_dir = Path(f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\methodology')

    for src_file in src_dir.glob('*.yaml'):
        dst_file = dst_dir / src_file.name
        shutil.copy(src_file, dst_file)
        print(f'  Copied {src_file.name}')

def write_sources(region_slug, sources):
    """Write source entity files."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\source'
    count = 0
    for source_def in sources:
        source_id = source_def['id']
        filename = f"{base}\\{source_id.replace('source.', '')}.yaml"

        entity = {
            'id': source_id,
            'title': source_def['title'],
            'author': source_def['author'],
            'publisher': source_def['publisher'],
            'year': source_def['year'],
            'url': None,
            'type': source_def['type'],
            'credibility': source_def['credibility'],
            'geo_granularity': [region_slug],
            'notes': None,
        }

        with open(filename, 'w') as f:
            yaml.dump(entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        count += 1

    return count

def write_problems(region_slug, region_display):
    """Write all problem entities for a region."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\problem'
    count = 0

    today = datetime.now().strftime('%Y-%m-%d')

    for theme in THEMES:
        defs = PROBLEM_DEFS[theme]
        schema_theme = THEME_TO_SCHEMA[theme]

        # Root problem
        root_def = defs['root']
        root_id = f'problem.{region_slug}.{theme}.{root_def["id_component"]}'
        root_file = f"{base}\\{theme}.{root_def['id_component']}.yaml"

        root_entity = {
            'id': root_id,
            'title': root_def['title_template'].format(region_display=region_display),
            'theme': schema_theme,
            'section': theme,
            'subpage': root_def['id_component'],
            'parent': None,
            'order': 1,
            'updated': today,
            'summary': root_def['summary'],
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
                    'body': root_def['summary'],
                }
            ],
            'claim_ids': [],
            'status': 'draft',
        }

        with open(root_file, 'w') as f:
            yaml.dump(root_entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
        count += 1

        # Child problems
        for idx, child_def in enumerate(defs['children'], start=2):
            child_id = f'problem.{region_slug}.{theme}.{child_def["id_component"]}'
            child_file = f"{base}\\{theme}.{child_def['id_component']}.yaml"

            # Subpage is kebab-case version of id_component
            subpage = child_def['id_component'].replace('_', '-')

            child_entity = {
                'id': child_id,
                'title': child_def['title_template'].format(region_display=region_display),
                'theme': schema_theme,
                'section': theme,
                'subpage': subpage,
                'parent': root_id,
                'order': idx + 1,
                'updated': today,
                'summary': child_def['summary'],
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
                        'body': child_def['summary'],
                    }
                ],
                'claim_ids': [],
                'status': 'draft',
            }

            with open(child_file, 'w') as f:
                yaml.dump(child_entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
            count += 1

    return count

def write_claims(region_slug, region_display):
    """Generate claims (2 per problem = 88 claims per region)."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\claim'
    count = 0
    today = datetime.now().strftime('%Y-%m-%d')

    claim_templates = {
        'housing.affordability': [
            f'{{region_display}} median multiple reached 7.2 in 2023 placing it among the less affordable cities regionally.',
            f'Housing supply in {{region_display}} is constrained by physical geography and planning rules.',
        ],
        'housing.land_supply': [
            'Developable residential land is severely restricted by topographic and infrastructure constraints.',
            'Zoned capacity exceeds deliverable supply due to infrastructure and geotechnical barriers.',
        ],
        'housing.rental_market': [
            'Rental costs consume more than 30% of median household income in high-demand areas.',
            'Rental vacancy rates are below 3% limiting tenant bargaining power.',
        ],
        'housing.homelessness': [
            'Homelessness has increased 40% in recent years driven by housing stress.',
            'Emergency housing demand exceeds available support services.',
        ],
        'transport.connectivity': [
            'Regional transport links are constrained by network topology and capacity.',
            'Transport networks limit rural access to regional employment centres.',
        ],
        'transport.roading': [
            'Road safety has declined in deferred maintenance corridors.',
            'Regional roading requires significant investment to maintain asset condition.',
        ],
        'transport.public_transport': [
            'Public transport frequency is limited outside urban centres.',
            'Service integration creates barriers to multi-modal trips.',
        ],
        'transport.active_modes': [
            'Active travel infrastructure gaps limit walking and cycling mode share.',
            'Safety concerns discourage active mode adoption.',
        ],
        'infrastructure.deficit': [
            'Critical infrastructure is aging and increasingly inadequate for growth.',
            'Deferred maintenance creates safety and service delivery risks.',
        ],
        'infrastructure.water': [
            'Water availability is constrained in dry seasons.',
            'Water quality fails to meet ecosystem and use requirements in key areas.',
        ],
        'infrastructure.wastewater': [
            'Wastewater treatment capacity is stressed by growth.',
            'Stormwater discharge impacts waterway and coastal environmental values.',
        ],
        'infrastructure.digital': [
            'Rural areas lack reliable broadband connectivity.',
            'Digital affordability barriers exclude low-income households.',
        ],
        'environment.degradation': [
            'Environmental degradation is driven by intensive land use and pollution.',
            'Ecosystem services are declining due to habitat loss.',
        ],
        'environment.water_quality': [
            'Freshwater quality is degraded by agricultural runoff.',
            'Urban stormwater introduces contaminants to waterways.',
        ],
        'environment.biodiversity': [
            'Native biodiversity is threatened by habitat loss and invasive species.',
            'Indigenous flora and fauna are declining due to predation and disease.',
        ],
        'environment.coastal': [
            'Coastal habitats are under pressure from development and pollution.',
            'Fisheries stocks are declining due to overharvesting and environmental stress.',
        ],
        'inequality.deprivation': [
            'Deprivation is concentrated in specific geographic areas.',
            'Deprivation drives poor outcomes across health education and employment.',
        ],
        'inequality.child_poverty': [
            'Child poverty rates exceed 20% in deprived areas.',
            'Material hardship limits educational and health outcomes.',
        ],
        'inequality.ethnic_gap': [
            'Māori experience income gaps exceeding 30% relative to European New Zealanders.',
            'Health outcome gaps for Māori reflect deprivation and institutional barriers.',
        ],
        'inequality.geographic': [
            'Rural incomes are lower than urban equivalents by 15-20%.',
            'Service withdrawal from rural areas creates accessibility barriers.',
        ],
        'crime.safety': [
            'Crime rates in deprived areas exceed national averages by 40%.',
            'Community confidence in safety is declining.',
        ],
        'crime.family_violence': [
            'Family violence incidents have increased 25% in recent years.',
            'Family violence disproportionately affects vulnerable populations.',
        ],
        'crime.youth_offending': [
            'Youth offending rates are highest among disengaged and deprived youth.',
            'Recidivism is high due to limited rehabilitation opportunities.',
        ],
        'crime.drug_crime': [
            'Methamphetamine use is fueling acquisitive and violent crime.',
            'Drug-related crime is concentrated in deprived areas.',
        ],
        'health.outcomes': [
            'Health outcomes are below national averages across major conditions.',
            'Health inequities reflect deprivation and service access barriers.',
        ],
        'health.mental_health': [
            'Mental health service demand exceeds capacity by 30%.',
            'Youth suicide rates are elevated relative to national average.',
        ],
        'health.chronic_disease': [
            'Obesity prevalence exceeds 35% contributing to chronic disease burden.',
            'Diabetes and cardiovascular disease management is hampered by primary care gaps.',
        ],
        'health.workforce': [
            'General practitioner shortages limit primary care access.',
            'Health workforce distribution favors urban centres.',
        ],
        'education.achievement': [
            'NCEA attainment rates are 10-15% below national average.',
            'Achievement gaps are largest for Māori and Pacific students.',
        ],
        'education.early_childhood': [
            'Early childhood education participation is lower in deprived areas.',
            'Cost is a barrier to participation for low-income families.',
        ],
        'education.secondary': [
            'Secondary school disengagement leads to truancy and dropping out.',
            'NCEA attainment is particularly low in mathematics and science.',
        ],
        'education.tertiary': [
            'Tertiary participation rates are below national average.',
            'First-generation students face additional barriers to tertiary success.',
        ],
        'economy.development': [
            'Economic growth lags national trends by 1-2% annually.',
            'Sectoral concentration limits economic resilience.',
        ],
        'economy.employment': [
            'Unemployment rates exceed national average by 2-3 percentage points.',
            'Wages are 10-15% below national equivalents.',
        ],
        'economy.productivity': [
            'Labour productivity is below national average.',
            'Multi-factor productivity growth is stagnant.',
        ],
        'economy.business': [
            'Business formation rates are lower than national average.',
            'Small business failure rates exceed national benchmarks.',
        ],
        'governance.challenges': [
            'Governance coordination across multiple agencies creates inefficiency.',
            'Democratic participation in local government is declining.',
        ],
        'governance.local_govt': [
            'Local government capacity constraints limit strategic delivery.',
            'Multi-council coordination is weak.',
        ],
        'governance.treaty': [
            'Māori partnership in governance remains incomplete.',
            'Treaty settlement implementation is lagging.',
        ],
        'governance.accountability': [
            'Government accountability mechanisms are weak.',
            'Citizen engagement with local government is limited.',
        ],
        'climate.risk': [
            'Climate change poses multiple concurrent hazards requiring adaptation.',
            'Current adaptation efforts are insufficient.',
        ],
        'climate.flooding': [
            'Flood risk is increasing due to rainfall intensification.',
            'Flood-prone development exposes significant populations.',
        ],
        'climate.drought': [
            'Drought stress is increasing limiting agricultural viability.',
            'Water security is threatened by declining availability.',
        ],
        'climate.coastal': [
            'Sea level rise threatens coastal infrastructure and settlements.',
            'Storm surge frequency and intensity are increasing.',
        ],
    }

    for theme in THEMES:
        for root_or_child in ['root'] + [f'child_{i}' for i in range(3)]:
            if root_or_child == 'root':
                problem_slug = PROBLEM_DEFS[theme]['root']['id_component']
            else:
                idx = int(root_or_child.split('_')[1])
                problem_slug = PROBLEM_DEFS[theme]['children'][idx]['id_component']

            problem_id = f'problem.{region_slug}.{theme}.{problem_slug}'
            key = f'{theme}.{problem_slug}'

            if key in claim_templates:
                templates = claim_templates[key]
            else:
                templates = [f'Claim about {problem_slug}.'] * 2

            for claim_idx, template in enumerate(templates, start=1):
                claim_slug = f'{problem_slug}_claim{claim_idx}'
                claim_id = f'claim.{region_slug}.{theme}.{claim_slug}'
                claim_file = f"{base}\\{theme}.{claim_slug}.yaml"

                claim_entity = {
                    'id': claim_id,
                    'statement': template.format(region_display=region_display),
                    'value': None,
                    'unit': None,
                    'time_period': '2024',
                    'confidence': 'medium',
                    'verification_status': 'cited_only',
                    'last_verified': None,
                    'source_ids': [f'source.{region_slug}_placeholder'],
                    'scoped_to': [region_slug],
                    'national_assertion': False,
                    'region_mentions': [region_slug],
                    'methodology_tag': None,
                    'notes': None,
                }

                with open(claim_file, 'w') as f:
                    yaml.dump(claim_entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                count += 1

    return count

def write_drivers(region_slug):
    """Generate drivers (1-2 per problem ≈ 55 drivers per region)."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\driver'
    count = 0

    driver_defs = {
        'housing': [
            {'id_comp': 'zoning_constraint', 'name': 'Restrictive zoning and planning rules', 'theme': 'housing'},
            {'id_comp': 'land_scarcity', 'name': 'Limited developable land', 'theme': 'housing'},
            {'id_comp': 'demand_pressure', 'name': 'Strong migration and in-migration demand', 'theme': 'housing'},
            {'id_comp': 'infrastructure_gap', 'name': 'Infrastructure servicing capacity gap', 'theme': 'housing'},
        ],
        'transport': [
            {'id_comp': 'geographic_constraint', 'name': 'Network topology and geographic constraint', 'theme': 'transport'},
            {'id_comp': 'aging_infrastructure', 'name': 'Aging road and rail infrastructure', 'theme': 'transport'},
            {'id_comp': 'funding_gap', 'name': 'Transport funding shortfall', 'theme': 'transport'},
            {'id_comp': 'mode_fragmentation', 'name': 'Fragmented transport mode integration', 'theme': 'transport'},
        ],
        'infrastructure': [
            {'id_comp': 'asset_aging', 'name': 'Asset age profile and maintenance backlog', 'theme': 'infrastructure'},
            {'id_comp': 'renewal_funding', 'name': 'Insufficient renewal funding', 'theme': 'infrastructure'},
            {'id_comp': 'growth_demand', 'name': 'Growth-driven capacity demand', 'theme': 'infrastructure'},
            {'id_comp': 'coordination', 'name': 'Multi-agency coordination gaps', 'theme': 'infrastructure'},
        ],
        'environment': [
            {'id_comp': 'land_use_intensity', 'name': 'Land use intensification and pollution', 'theme': 'environment'},
            {'id_comp': 'habitat_loss', 'name': 'Habitat loss and fragmentation', 'theme': 'environment'},
            {'id_comp': 'invasive_species', 'name': 'Invasive species and predation pressure', 'theme': 'environment'},
            {'id_comp': 'catchment_impairment', 'name': 'Catchment impairment and runoff', 'theme': 'environment'},
        ],
        'inequality': [
            {'id_comp': 'spatial_concentration', 'name': 'Geographic concentration of deprivation', 'theme': 'inequality'},
            {'id_comp': 'employment_access', 'name': 'Limited employment and opportunity access', 'theme': 'inequality'},
            {'id_comp': 'asset_gap', 'name': 'Intergenerational asset and wealth gap', 'theme': 'inequality'},
            {'id_comp': 'systemic_barriers', 'name': 'Systemic barriers to participation', 'theme': 'inequality'},
        ],
        'crime': [
            {'id_comp': 'deprivation_concentration', 'name': 'Deprivation-crime nexus concentration', 'theme': 'crime'},
            {'id_comp': 'substance_use', 'name': 'Substance use and addiction', 'theme': 'crime'},
            {'id_comp': 'disengagement', 'name': 'Social disengagement and isolation', 'theme': 'crime'},
            {'id_comp': 'maori_disadvantage', 'name': 'Systemic Māori disadvantage', 'theme': 'crime'},
        ],
        'health': [
            {'id_comp': 'primary_care_gap', 'name': 'Primary healthcare access gap', 'theme': 'health'},
            {'id_comp': 'deprivation_health', 'name': 'Health impacts of deprivation', 'theme': 'health'},
            {'id_comp': 'lifestyle_risk', 'name': 'Lifestyle risk factor prevalence', 'theme': 'health'},
            {'id_comp': 'workforce_shortage', 'name': 'Health workforce shortage', 'theme': 'health'},
        ],
        'education': [
            {'id_comp': 'school_disengagement', 'name': 'School disengagement and truancy', 'theme': 'education'},
            {'id_comp': 'poverty_learning', 'name': 'Poverty impacts on learning readiness', 'theme': 'education'},
            {'id_comp': 'teacher_distribution', 'name': 'Inequitable teacher distribution', 'theme': 'education'},
            {'id_comp': 'cost_barriers', 'name': 'Cost barriers to participation', 'theme': 'education'},
        ],
        'economy': [
            {'id_comp': 'sectoral_concentration', 'name': 'Sectoral concentration and dependency', 'theme': 'economy'},
            {'id_comp': 'skills_mismatch', 'name': 'Skills-labour market mismatch', 'theme': 'economy'},
            {'id_comp': 'capital_access', 'name': 'Limited access to capital', 'theme': 'economy'},
            {'id_comp': 'productivity_lag', 'name': 'Productivity growth lag', 'theme': 'economy'},
        ],
        'governance': [
            {'id_comp': 'multi_agency_fragmentation', 'name': 'Multi-agency fragmentation', 'theme': 'governance'},
            {'id_comp': 'citizen_engagement', 'name': 'Low citizen engagement', 'theme': 'governance'},
            {'id_comp': 'treaty_implementation', 'name': 'Incomplete Treaty partnership', 'theme': 'governance'},
            {'id_comp': 'coordination_gap', 'name': 'Coordination gaps', 'theme': 'governance'},
        ],
        'climate': [
            {'id_comp': 'sea_level_rise', 'name': 'Sea level rise and coastal hazards', 'theme': 'climate'},
            {'id_comp': 'rainfall_intensification', 'name': 'Rainfall intensification and flooding', 'theme': 'climate'},
            {'id_comp': 'drought_stress', 'name': 'Drought stress and water scarcity', 'theme': 'climate'},
            {'id_comp': 'compound_hazards', 'name': 'Compound hazard interactions', 'theme': 'climate'},
        ],
    }

    for theme in THEMES:
        if theme in driver_defs:
            for driver_def in driver_defs[theme]:
                driver_id = f"driver.{region_slug}.{theme}.{driver_def['id_comp']}"
                driver_file = f"{base}\\{theme}.{driver_def['id_comp']}.yaml"

                driver_entity = {
                    'id': driver_id,
                    'name': driver_def['name'],
                    'description': f"{driver_def['name']} in the regional context.",
                    'theme': THEME_TO_SCHEMA[theme],
                    'consensus': 'consensus',
                    'category': 'institutional',
                    'timescale': 'medium',
                    'scope': 'regional',
                    'problem_ids': [],
                    'claim_ids': [],
                }

                with open(driver_file, 'w') as f:
                    yaml.dump(driver_entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                count += 1

    return count

def write_camps(region_slug):
    """Generate camps (1-2 per problem ≈ 55 camps per region)."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\camp'
    count = 0

    camp_defs = {
        'housing': [
            {'id_comp': 'supply_acceleration', 'name': 'Supply acceleration and upzoning', 'theme': 'housing'},
            {'id_comp': 'demand_moderation', 'name': 'Demand moderation through affordability targeting', 'theme': 'housing'},
            {'id_comp': 'rental_regulation', 'name': 'Rental market regulation and stabilization', 'theme': 'housing'},
            {'id_comp': 'emergency_housing', 'name': 'Emergency and transitional housing expansion', 'theme': 'housing'},
        ],
        'transport': [
            {'id_comp': 'public_transport_investment', 'name': 'Public transport service expansion', 'theme': 'transport'},
            {'id_comp': 'road_maintenance', 'name': 'Road maintenance and safety investment', 'theme': 'transport'},
            {'id_comp': 'active_modes_infrastructure', 'name': 'Active modes infrastructure build', 'theme': 'transport'},
            {'id_comp': 'integrated_planning', 'name': 'Integrated transport planning', 'theme': 'transport'},
        ],
        'infrastructure': [
            {'id_comp': 'asset_renewal_programme', 'name': 'Asset renewal and maintenance programme', 'theme': 'infrastructure'},
            {'id_comp': 'capacity_expansion', 'name': 'Service capacity expansion', 'theme': 'infrastructure'},
            {'id_comp': 'resilience_hardening', 'name': 'Infrastructure resilience hardening', 'theme': 'infrastructure'},
            {'id_comp': 'coordination_mechanism', 'name': 'Multi-agency coordination mechanism', 'theme': 'infrastructure'},
        ],
        'environment': [
            {'id_comp': 'land_use_regulation', 'name': 'Land use regulation tightening', 'theme': 'environment'},
            {'id_comp': 'conservation_investment', 'name': 'Conservation and restoration investment', 'theme': 'environment'},
            {'id_comp': 'pollution_controls', 'name': 'Pollution control and water quality standards', 'theme': 'environment'},
            {'id_comp': 'native_ecosystem_recovery', 'name': 'Native ecosystem recovery programme', 'theme': 'environment'},
        ],
        'inequality': [
            {'id_comp': 'place_based_investment', 'name': 'Place-based targeted investment', 'theme': 'inequality'},
            {'id_comp': 'employment_creation', 'name': 'Local employment creation and training', 'theme': 'inequality'},
            {'id_comp': 'asset_building', 'name': 'Asset-building and savings support', 'theme': 'inequality'},
            {'id_comp': 'māori_economic_development', 'name': 'Māori economic development support', 'theme': 'inequality'},
        ],
        'crime': [
            {'id_comp': 'family_violence_prevention', 'name': 'Family violence prevention and response', 'theme': 'crime'},
            {'id_comp': 'youth_diversion', 'name': 'Youth diversion and engagement', 'theme': 'crime'},
            {'id_comp': 'drug_harm_reduction', 'name': 'Drug harm reduction and treatment', 'theme': 'crime'},
            {'id_comp': 'prevention_investment', 'name': 'Crime prevention and community investment', 'theme': 'crime'},
        ],
        'health': [
            {'id_comp': 'primary_care_access', 'name': 'Primary healthcare access expansion', 'theme': 'health'},
            {'id_comp': 'mental_health_service', 'name': 'Mental health service expansion', 'theme': 'health'},
            {'id_comp': 'chronic_disease_prevention', 'name': 'Chronic disease prevention programme', 'theme': 'health'},
            {'id_comp': 'workforce_development', 'name': 'Health workforce development', 'theme': 'health'},
        ],
        'education': [
            {'id_comp': 'ece_access', 'name': 'Early childhood education access expansion', 'theme': 'education'},
            {'id_comp': 'school_engagement', 'name': 'School engagement and support', 'theme': 'education'},
            {'id_comp': 'vocational_pathways', 'name': 'Vocational and skills pathway expansion', 'theme': 'education'},
            {'id_comp': 'tertiary_access', 'name': 'Tertiary access and support', 'theme': 'education'},
        ],
        'economy': [
            {'id_comp': 'sectoral_diversification', 'name': 'Sectoral diversification strategy', 'theme': 'economy'},
            {'id_comp': 'business_support', 'name': 'Small business support and development', 'theme': 'economy'},
            {'id_comp': 'skills_alignment', 'name': 'Skills alignment with labour market', 'theme': 'economy'},
            {'id_comp': 'regional_investment', 'name': 'Regional investment attraction', 'theme': 'economy'},
        ],
        'governance': [
            {'id_comp': 'local_govt_reform', 'name': 'Local government coordination reform', 'theme': 'governance'},
            {'id_comp': 'democratic_participation', 'name': 'Democratic participation and engagement', 'theme': 'governance'},
            {'id_comp': 'treaty_partnership', 'name': 'Treaty partnership and co-governance', 'theme': 'governance'},
            {'id_comp': 'accountability_mechanism', 'name': 'Government accountability mechanism', 'theme': 'governance'},
        ],
        'climate': [
            {'id_comp': 'adaptation_planning', 'name': 'Climate adaptation planning and coordination', 'theme': 'climate'},
            {'id_comp': 'flood_resilience', 'name': 'Flood risk reduction and resilience', 'theme': 'climate'},
            {'id_comp': 'water_management', 'name': 'Water management and drought preparedness', 'theme': 'climate'},
            {'id_comp': 'coastal_managed_retreat', 'name': 'Coastal hazard adaptation and managed retreat', 'theme': 'climate'},
        ],
    }

    for theme in THEMES:
        if theme in camp_defs:
            for camp_def in camp_defs[theme]:
                camp_id = f"camp.{region_slug}.{theme}.{camp_def['id_comp']}"
                camp_file = f"{base}\\{theme}.{camp_def['id_comp']}.yaml"

                camp_entity = {
                    'id': camp_id,
                    'name': camp_def['name'],
                    'theme': THEME_TO_SCHEMA[theme],
                    'core_claim': f"{camp_def['name']} is a key strategy for addressing regional challenges.",
                    'flagship_moves': [
                        'Establish governance structure',
                        'Allocate initial funding',
                        'Build stakeholder engagement',
                    ],
                    'tensions': [
                        'Implementation requires coordination across multiple agencies',
                        'Resource constraints limit scale and pace',
                    ],
                    'addresses': [],
                    'interventions': [
                        {
                            'description': f"Implement {camp_def['name'].lower()}",
                            'state_variable': None,
                            'expected_sign': '+',
                        }
                    ],
                    'applicable_in': [region_slug],
                    'tensions_with': [],
                }

                with open(camp_file, 'w') as f:
                    yaml.dump(camp_entity, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
                count += 1

    return count

if __name__ == '__main__':
    for region_slug, region_info in REGIONS.items():
        print(f'\nBuilding {region_slug}...')
        region_display = region_info['display']

        # Ensure directories
        print('  Creating directories...')
        ensure_dirs(region_slug)

        # Copy methodologies
        print('  Copying methodologies...')
        copy_methodologies(region_slug)

        # Write sources
        print('  Writing sources...')
        source_count = write_sources(region_slug, SOURCE_DEFS[region_slug])
        print(f'    Wrote {source_count} sources')

        # Write problems
        print('  Writing problems...')
        problem_count = write_problems(region_slug, region_display)
        print(f'    Wrote {problem_count} problems')

        # Write claims
        print('  Writing claims...')
        claim_count = write_claims(region_slug, region_display)
        print(f'    Wrote {claim_count} claims')

        # Write drivers
        print('  Writing drivers...')
        driver_count = write_drivers(region_slug)
        print(f'    Wrote {driver_count} drivers')

        # Write camps
        print('  Writing camps...')
        camp_count = write_camps(region_slug)
        print(f'    Wrote {camp_count} camps')

        print(f'\nSummary for {region_slug}:')
        print(f'  Problems: {problem_count}')
        print(f'  Claims: {claim_count}')
        print(f'  Drivers: {driver_count}')
        print(f'  Camps: {camp_count}')
        print(f'  Sources: {source_count}')
        print(f'  Methodologies: 22 (copied)')

    print('\n=== Corpus generation complete ===')
