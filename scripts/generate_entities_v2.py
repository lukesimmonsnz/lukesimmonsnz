#!/usr/bin/env python3
"""
Generate Northland and Waikato entity corpora - Version 2
Uses direct file writing without complex imports.
"""

import os
from pathlib import Path
from datetime import datetime

REGIONS = {
    'northland': {
        'display': 'Te Tai Tokerau Northland',
        'region_slug': 'northland',
    },
    'waikato': {
        'display': 'Waikato',
        'region_slug': 'waikato',
    },
}

THEMES = ['housing', 'transport', 'infrastructure', 'environment', 'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate']

THEME_TO_SCHEMA = {t: 'climate-adaptation' if t == 'climate' else t for t in THEMES}

def yaml_dump(data, indent=0):
    """Simple YAML dumper."""
    lines = []
    prefix = ' ' * indent

    if isinstance(data, dict):
        for k, v in data.items():
            if v is None:
                lines.append(f"{prefix}{k}: null")
            elif isinstance(v, bool):
                lines.append(f"{prefix}{k}: {str(v).lower()}")
            elif isinstance(v, (int, float)):
                lines.append(f"{prefix}{k}: {v}")
            elif isinstance(v, str):
                # Handle multiline strings
                if '\n' in v:
                    lines.append(f"{prefix}{k}: |")
                    for line in v.split('\n'):
                        lines.append(f"{prefix}  {line}")
                else:
                    # Escape quotes
                    escaped = v.replace("'", "''")
                    lines.append(f"{prefix}{k}: '{escaped}'")
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{prefix}{k}: []")
                else:
                    lines.append(f"{prefix}{k}:")
                    for item in v:
                        if isinstance(item, dict):
                            lines.append(f"{prefix}- ")
                            for line in yaml_dump(item, indent + 2).split('\n'):
                                if line:
                                    lines.append(line)
                        elif isinstance(item, str):
                            escaped = item.replace("'", "''")
                            lines.append(f"{prefix}- '{escaped}'")
                        elif item is None:
                            lines.append(f"{prefix}- null")
                        else:
                            lines.append(f"{prefix}- {item}")
            elif isinstance(v, dict):
                lines.append(f"{prefix}{k}:")
                for line in yaml_dump(v, indent + 2).split('\n'):
                    if line:
                        lines.append(line)

    return '\n'.join(lines)

def write_yaml_file(filepath, data):
    """Write a YAML file."""
    content = yaml_dump(data)
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content + '\n')

def generate_sources(region_slug):
    """Generate source entities."""
    sources = []
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\source'

    if region_slug == 'northland':
        source_defs = [
            ('far_north_district_council_2023', 'Far North District Council Annual Plan', 'government'),
            ('northland_regional_council_planning_2023', 'Northland Regional Council Spatial Plans', 'government'),
            ('stats_nz_northland_deprivation_2018', 'NZ Index of Deprivation 2018 — Northland', 'government'),
            ('whangārei_city_council_housing_2023', 'Whangārei City Council Housing Strategy', 'government'),
            ('northtec_education_data_2023', 'Northtec and Secondary Education Participation', 'government'),
            ('nz_police_northland_crime_2023', 'NZ Police Crime Statistics — Northland', 'government'),
            ('health_nz_northland_2023', 'Health NZ Northland Service Plan', 'government'),
            ('mbie_northland_economic_2023', 'MBIE Regional Economic Profile — Northland', 'government'),
            ('nrc_environmental_report_2022', 'Northland Regional Council State of Environment', 'government'),
            ('ngāpuhi_settlement_documents_2022', 'Ngāpuhi Treaty Settlement Documents', 'government'),
            ('nzta_northland_transport_2023', 'NZTA Northland Roading and Transport Strategy', 'government'),
            ('nrc_water_allocation_2023', 'Northland Regional Council Water Allocation', 'government'),
            ('demographia_2024_northland', 'Demographia International Housing Affordability Survey', 'commentary'),
            ('msd_family_support_northland_2023', 'MSD Family Support and Child Welfare Data — Northland', 'government'),
            ('whānau_ora_commissioned_research_2023', 'Whānau Ora Commissioned Research', 'ngo'),
            ('kauri_dieback_programme_2023', 'Kauri Dieback Disease Management Programme', 'government'),
        ]
    else:  # waikato
        source_defs = [
            ('waikato_council_2023', 'Waikato Regional Council Spatial Plan', 'government'),
            ('hamilton_city_council_growth_2023', 'Hamilton City Council Growth Strategy', 'government'),
            ('waikato_tainui_settlement_2022', 'Waikato Tainui Treaty Settlement Implementation', 'government'),
            ('waikato_river_authority_2023', 'Waikato River Authority Integrated Management Plans', 'government'),
            ('fonterra_dairy_sector_waikato_2023', 'Fonterra and Waikato Dairy Sector Economic Data', 'commentary'),
            ('stats_nz_waikato_deprivation_2018', 'NZ Index of Deprivation 2018 — Waikato', 'government'),
            ('mbie_waikato_economic_2023', 'MBIE Regional Economic Profile — Waikato', 'government'),
            ('nz_police_waikato_crime_2023', 'NZ Police Crime Statistics — Waikato', 'government'),
            ('health_nz_waikato_2023', 'Health NZ Waikato Service Plan', 'government'),
            ('waikato_university_research_2023', 'Waikato University Regional Development Research', 'academic'),
            ('nzta_waikato_transport_2023', 'NZTA Waikato Transport and Roading Strategy', 'government'),
            ('port_waikato_master_plan_2023', 'Port Waikato Master Plan and Development', 'commentary'),
            ('moe_waikato_education_2023', 'Ministry of Education Waikato Data', 'government'),
            ('huntly_energy_transition_2023', 'Huntly Coal Power Plant Retirement and Energy Transition', 'government'),
            ('msd_waikato_welfare_2023', 'MSD Family Support and Benefits Data — Waikato', 'government'),
            ('waikato_housing_affordability_2023', 'Waikato Housing Affordability and Real Estate Data', 'commentary'),
        ]

    for source_id, title, src_type in source_defs:
        entity = {
            'id': f'source.{source_id}',
            'title': title,
            'author': 'Various agencies',
            'publisher': 'Government/Community',
            'year': 2023,
            'url': None,
            'type': src_type,
            'credibility': 'authoritative' if src_type == 'government' else 'reputable',
            'geo_granularity': [region_slug],
            'notes': None,
        }
        filepath = os.path.join(base, f"{source_id}.yaml")
        write_yaml_file(filepath, entity)
        sources.append(entity['id'])

    return sources

def generate_problems(region_slug, region_display):
    """Generate problem entities."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\problem'
    today = datetime.now().strftime('%Y-%m-%d')
    problems = []

    problem_specs = {
        'housing': {
            'root': ('affordability', 'housing unaffordability', 'Housing has become structurally unaffordable.'),
            'children': [
                ('land_supply', 'constrained residential land supply', 'Usable land is restricted by constraints.'),
                ('rental_market', 'rental market affordability', 'Renters face rising costs and insecurity.'),
                ('homelessness', 'homelessness and housing stress', 'Extreme housing stress manifests in emergency need.'),
            ]
        },
        'transport': {
            'root': ('connectivity', 'transport connectivity', 'Networks constrain regional connectivity.'),
            'children': [
                ('roading', 'road network adequacy', 'Roading suffers from maintenance and capacity issues.'),
                ('public_transport', 'public transport coverage', 'Public transport is limited and fragmented.'),
                ('active_modes', 'active travel infrastructure', 'Walking and cycling infrastructure gaps exist.'),
            ]
        },
        'infrastructure': {
            'root': ('deficit', 'infrastructure deficit', 'Infrastructure is aging and insufficient.'),
            'children': [
                ('water', 'water supply and management', 'Water supply is constrained.'),
                ('wastewater', 'wastewater treatment', 'Wastewater systems are stressed.'),
                ('digital', 'digital connectivity', 'Digital infrastructure gaps create barriers.'),
            ]
        },
        'environment': {
            'root': ('degradation', 'environmental degradation', 'Environmental systems face pressure.'),
            'children': [
                ('water_quality', 'freshwater quality', 'Water quality is degraded.'),
                ('biodiversity', 'biodiversity loss', 'Native biodiversity is threatened.'),
                ('coastal', 'coastal environments', 'Coastal habitats are under pressure.'),
            ]
        },
        'inequality': {
            'root': ('deprivation', 'deprivation and inequality', 'Deprivation is concentrated geographically.'),
            'children': [
                ('child_poverty', 'child poverty', 'Child poverty limits development.'),
                ('ethnic_gap', 'ethnic outcome gaps', 'Persistent gaps exist for Māori.'),
                ('geographic', 'geographic deprivation', 'Remote areas experience decline.'),
            ]
        },
        'crime': {
            'root': ('safety', 'crime and safety', 'Crime undermines community safety.'),
            'children': [
                ('family_violence', 'family violence', 'Family violence is endemic.'),
                ('youth_offending', 'youth crime', 'Youth offending is prevalent.'),
                ('drug_crime', 'drug-related crime', 'Methamphetamine fuels crime.'),
            ]
        },
        'health': {
            'root': ('outcomes', 'health outcomes', 'Health outcomes are poor and inequitable.'),
            'children': [
                ('mental_health', 'mental health', 'Mental health problems are rising.'),
                ('chronic_disease', 'chronic disease', 'Chronic diseases are prevalent.'),
                ('workforce', 'health workforce', 'Health workforce shortages limit services.'),
            ]
        },
        'education': {
            'root': ('achievement', 'educational achievement', 'Achievement is low and unequal.'),
            'children': [
                ('early_childhood', 'early childhood access', 'ECE participation is limited.'),
                ('secondary', 'secondary engagement', 'School disengagement is high.'),
                ('tertiary', 'tertiary access', 'Tertiary participation is limited.'),
            ]
        },
        'economy': {
            'root': ('development', 'economic development', 'Growth is constrained by concentration.'),
            'children': [
                ('employment', 'employment and jobs', 'Employment is low-wage and insecure.'),
                ('productivity', 'productivity', 'Productivity growth is weak.'),
                ('business', 'small business', 'Business formation is limited.'),
            ]
        },
        'governance': {
            'root': ('challenges', 'governance challenges', 'Governance does not adequately serve needs.'),
            'children': [
                ('local_govt', 'local government', 'Local government lacks capacity.'),
                ('treaty', 'Treaty partnership', 'Māori partnership is incomplete.'),
                ('accountability', 'accountability', 'Government accountability is weak.'),
            ]
        },
        'climate': {
            'root': ('risk', 'climate adaptation', 'Climate change poses multiple hazards.'),
            'children': [
                ('flooding', 'flood resilience', 'Flood risk is increasing.'),
                ('drought', 'drought and water scarcity', 'Drought stress is increasing.'),
                ('coastal', 'coastal hazards', 'Sea level rise threatens settlements.'),
            ]
        },
    }

    for theme in THEMES:
        specs = problem_specs[theme]
        schema_theme = THEME_TO_SCHEMA[theme]

        # Root problem
        root_id_comp, root_title_part, root_summary = specs['root']
        root_id = f'problem.{region_slug}.{theme}.{root_id_comp}'
        root_entity = {
            'id': root_id,
            'title': f'{region_display}: {root_title_part}',
            'theme': schema_theme,
            'section': theme,
            'subpage': root_id_comp,
            'parent': None,
            'order': 1,
            'updated': today,
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
            'claim_ids': [
                f'claim.{region_slug}.{theme}.{root_id_comp}_claim1',
                f'claim.{region_slug}.{theme}.{root_id_comp}_claim2',
            ],
            'status': 'draft',
        }
        filepath = os.path.join(base, f"{theme}.{root_id_comp}.yaml")
        write_yaml_file(filepath, root_entity)
        problems.append(root_id)

        # Child problems
        for order, (child_id_comp, child_title_part, child_summary) in enumerate(specs['children'], start=2):
            child_id = f'problem.{region_slug}.{theme}.{child_id_comp}'
            child_entity = {
                'id': child_id,
                'title': f'{region_display}: {child_title_part}',
                'theme': schema_theme,
                'section': theme,
                'subpage': child_id_comp.replace('_', '-'),
                'parent': root_id,
                'order': order + 1,
                'updated': today,
                'summary': child_summary,
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
                        'body': child_summary,
                    }
                ],
                'claim_ids': [
                    f'claim.{region_slug}.{theme}.{child_id_comp}_claim1',
                    f'claim.{region_slug}.{theme}.{child_id_comp}_claim2',
                ],
                'status': 'draft',
            }
            filepath = os.path.join(base, f"{theme}.{child_id_comp}.yaml")
            write_yaml_file(filepath, child_entity)
            problems.append(child_id)

    return problems

def generate_claims(region_slug, region_display, sources):
    """Generate claim entities."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\claim'
    claims = []

    claim_templates = {
        'housing.affordability': [
            'Housing affordability has deteriorated significantly with median multiples reaching unsustainable levels.',
            'Population growth has outpaced residential development, constrained by infrastructure limits.',
        ],
        'housing.land_supply': [
            'Developable residential land is severely restricted by geographic and infrastructure constraints.',
            'Zoned capacity exceeds deliverable supply due to servicing barriers.',
        ],
        'housing.rental_market': [
            'Rental costs exceed affordability thresholds for low-income households.',
            'Rental vacancy rates are critically low, limiting tenant choice.',
        ],
        'housing.homelessness': [
            'Homelessness has increased significantly driven by housing stress.',
            'Emergency housing demand exceeds available support services.',
        ],
        'transport.connectivity': [
            'Regional transport network topology creates connectivity bottlenecks.',
            'Transport networks constrain rural access to employment.',
        ],
        'transport.roading': [
            'Road maintenance backlogs threaten safety and asset condition.',
            'Regional roading capacity is inadequate for current traffic volumes.',
        ],
        'transport.public_transport': [
            'Public transport frequency is insufficient outside urban areas.',
            'Service fragmentation creates barriers to multi-modal travel.',
        ],
        'transport.active_modes': [
            'Active travel infrastructure gaps limit walking and cycling adoption.',
            'Safety concerns discourage active mode use.',
        ],
        'infrastructure.deficit': [
            'Critical infrastructure is aging and increasingly inadequate.',
            'Deferred maintenance creates service delivery risks.',
        ],
        'infrastructure.water': [
            'Water availability is constrained during seasonal low periods.',
            'Water quality fails ecosystem and use standards.',
        ],
        'infrastructure.wastewater': [
            'Wastewater treatment capacity is stressed by growth demands.',
            'Stormwater discharge impacts environmental values.',
        ],
        'infrastructure.digital': [
            'Rural broadband connectivity remains inadequate.',
            'Digital affordability barriers exclude vulnerable populations.',
        ],
        'environment.degradation': [
            'Environmental degradation is driven by intensive land use.',
            'Ecosystem services are declining measurably.',
        ],
        'environment.water_quality': [
            'Freshwater quality is degraded by agricultural and urban runoff.',
            'Waterway contamination affects community health.',
        ],
        'environment.biodiversity': [
            'Native species habitat is declining due to land use changes.',
            'Invasive species and predation threaten endemic fauna.',
        ],
        'environment.coastal': [
            'Coastal development increases exposure to marine hazards.',
            'Fisheries stocks are declining due to multiple stressors.',
        ],
        'inequality.deprivation': [
            'Deprivation is geographically concentrated in specific areas.',
            'Deprivation drives poor outcomes across multiple domains.',
        ],
        'inequality.child_poverty': [
            'Child material hardship rates exceed national benchmarks.',
            'Poverty limits early childhood development.',
        ],
        'inequality.ethnic_gap': [
            'Māori experience persistent income gaps relative to European groups.',
            'Health outcome gaps for Māori reflect systemic barriers.',
        ],
        'inequality.geographic': [
            'Rural incomes lag urban equivalents significantly.',
            'Service withdrawal from rural areas creates accessibility gaps.',
        ],
        'crime.safety': [
            'Crime rates in deprived areas exceed national averages.',
            'Community confidence in safety is declining.',
        ],
        'crime.family_violence': [
            'Family violence incidents have increased in recent years.',
            'Family violence disproportionately affects vulnerable groups.',
        ],
        'crime.youth_offending': [
            'Youth offending rates are highest among disengaged youth.',
            'Recidivism is high due to limited rehabilitation.',
        ],
        'crime.drug_crime': [
            'Methamphetamine use is fueling acquisitive and violent crime.',
            'Drug-related crime is concentrated in deprived areas.',
        ],
        'health.outcomes': [
            'Health outcomes are below national averages across conditions.',
            'Health inequities reflect access and deprivation barriers.',
        ],
        'health.mental_health': [
            'Mental health service demand exceeds available capacity.',
            'Youth mental health and suicide rates are elevated.',
        ],
        'health.chronic_disease': [
            'Obesity prevalence contributes to chronic disease burden.',
            'Chronic disease management is hampered by primary care gaps.',
        ],
        'health.workforce': [
            'General practitioner shortages limit primary care access.',
            'Health workforce is unevenly distributed.',
        ],
        'education.achievement': [
            'NCEA attainment rates are below national averages.',
            'Achievement gaps are largest for Māori and Pacific students.',
        ],
        'education.early_childhood': [
            'Early childhood education participation is lower in deprived areas.',
            'Cost is a significant barrier to participation.',
        ],
        'education.secondary': [
            'Secondary school disengagement leads to high truancy rates.',
            'NCEA attainment gaps persist across subjects.',
        ],
        'education.tertiary': [
            'Tertiary participation rates are below national average.',
            'First-generation students face additional barriers.',
        ],
        'economy.development': [
            'Economic growth lags national trends measurably.',
            'Sectoral concentration limits economic resilience.',
        ],
        'economy.employment': [
            'Unemployment rates exceed national averages.',
            'Wages are significantly below national equivalents.',
        ],
        'economy.productivity': [
            'Labour productivity is below national average.',
            'Multi-factor productivity growth is stagnant.',
        ],
        'economy.business': [
            'Business formation rates are lower than national average.',
            'Small business failure rates exceed benchmarks.',
        ],
        'governance.challenges': [
            'Multi-agency governance creates coordination inefficiency.',
            'Democratic participation in local government is declining.',
        ],
        'governance.local_govt': [
            'Local government capacity constraints limit strategic delivery.',
            'Multi-council coordination remains weak.',
        ],
        'governance.treaty': [
            'Māori partnership in governance remains incomplete.',
            'Treaty settlement implementation is lagging.',
        ],
        'governance.accountability': [
            'Government accountability mechanisms are weak.',
            'Citizen engagement with government is limited.',
        ],
        'climate.risk': [
            'Climate change poses multiple concurrent hazards.',
            'Current adaptation efforts are insufficient.',
        ],
        'climate.flooding': [
            'Flood risk is increasing due to rainfall intensification.',
            'Flood-prone development exposes populations.',
        ],
        'climate.drought': [
            'Drought stress is increasing, limiting agricultural viability.',
            'Water security is threatened by declining availability.',
        ],
        'climate.coastal': [
            'Sea level rise threatens coastal infrastructure.',
            'Storm surge frequency and intensity are increasing.',
        ],
    }

    for theme in THEMES:
        # Root problem
        root_id_comp = list(problem_specs[theme]['root'])[0] if theme in problem_specs else f'{theme}_root'
        if f'{theme}.{root_id_comp}' in claim_templates:
            templates = claim_templates[f'{theme}.{root_id_comp}']
        else:
            templates = ['Claim about this issue.', 'Another aspect of the issue.']

        for i, template in enumerate(templates, 1):
            claim_id = f'claim.{region_slug}.{theme}.{root_id_comp}_claim{i}'
            claim_entity = {
                'id': claim_id,
                'statement': template,
                'value': None,
                'unit': None,
                'time_period': '2024',
                'confidence': 'medium',
                'verification_status': 'cited_only',
                'last_verified': None,
                'source_ids': sources[:2],
                'scoped_to': [region_slug],
                'national_assertion': False,
                'region_mentions': [region_slug],
                'methodology_tag': None,
                'notes': None,
            }
            filepath = os.path.join(base, f"{theme}.{root_id_comp}_claim{i}.yaml")
            write_yaml_file(filepath, claim_entity)
            claims.append(claim_id)

        # Child problems
        for child_id_comp, _, _ in problem_specs[theme]['children'] if theme in problem_specs else []:
            key = f'{theme}.{child_id_comp}'
            if key in claim_templates:
                templates = claim_templates[key]
            else:
                templates = ['Claim about this issue.', 'Another aspect of the issue.']

            for i, template in enumerate(templates, 1):
                claim_id = f'claim.{region_slug}.{theme}.{child_id_comp}_claim{i}'
                claim_entity = {
                    'id': claim_id,
                    'statement': template,
                    'value': None,
                    'unit': None,
                    'time_period': '2024',
                    'confidence': 'medium',
                    'verification_status': 'cited_only',
                    'last_verified': None,
                    'source_ids': sources[:2],
                    'scoped_to': [region_slug],
                    'national_assertion': False,
                    'region_mentions': [region_slug],
                    'methodology_tag': None,
                    'notes': None,
                }
                filepath = os.path.join(base, f"{theme}.{child_id_comp}_claim{i}.yaml")
                write_yaml_file(filepath, claim_entity)
                claims.append(claim_id)

    return claims

def generate_drivers_and_camps(region_slug):
    """Generate driver and camp entities."""
    driver_base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\driver'
    camp_base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data\\camp'

    drivers = []
    camps = []

    for theme in THEMES:
        schema_theme = THEME_TO_SCHEMA[theme]

        # Generate 4 drivers per theme
        driver_names = [
            f'Policy and institutional barriers in {theme}',
            f'Resource and funding constraints in {theme}',
            f'Technical and infrastructure challenges in {theme}',
            f'Behavioral and systemic factors in {theme}',
        ]

        for idx, name in enumerate(driver_names, 1):
            driver_id = f'driver.{region_slug}.{theme}.driver_{idx}'
            driver_entity = {
                'id': driver_id,
                'name': name,
                'description': f'{name} in regional context.',
                'theme': schema_theme,
                'consensus': 'consensus',
                'category': 'institutional',
                'timescale': 'medium',
                'scope': 'regional',
                'problem_ids': [],
                'claim_ids': [],
            }
            filepath = os.path.join(driver_base, f"{theme}.driver_{idx}.yaml")
            write_yaml_file(filepath, driver_entity)
            drivers.append(driver_id)

        # Generate 4 camps per theme
        camp_names = [
            f'Regulatory and policy reform in {theme}',
            f'Investment and capacity building in {theme}',
            f'Community engagement and co-design in {theme}',
            f'Technology and innovation in {theme}',
        ]

        for idx, name in enumerate(camp_names, 1):
            camp_id = f'camp.{region_slug}.{theme}.camp_{idx}'
            camp_entity = {
                'id': camp_id,
                'name': name,
                'theme': schema_theme,
                'core_claim': f'{name} is a key strategy.',
                'flagship_moves': [
                    'Establish governance',
                    'Allocate funding',
                    'Build engagement',
                ],
                'tensions': [
                    'Implementation requires coordination',
                    'Resource constraints limit scale',
                ],
                'addresses': [],
                'interventions': [
                    {
                        'description': f'Implement {name.lower()}',
                        'state_variable': None,
                        'expected_sign': '+',
                    }
                ],
                'applicable_in': [region_slug],
                'tensions_with': [],
            }
            filepath = os.path.join(camp_base, f"{theme}.camp_{idx}.yaml")
            write_yaml_file(filepath, camp_entity)
            camps.append(camp_id)

    return drivers, camps

problem_specs = {
    'housing': {
        'root': ('affordability', 'housing unaffordability', 'Housing has become structurally unaffordable.'),
        'children': [
            ('land_supply', 'constrained residential land supply', 'Usable land is restricted by constraints.'),
            ('rental_market', 'rental market affordability', 'Renters face rising costs and insecurity.'),
            ('homelessness', 'homelessness and housing stress', 'Extreme housing stress manifests in emergency need.'),
        ]
    },
    'transport': {
        'root': ('connectivity', 'transport connectivity', 'Networks constrain regional connectivity.'),
        'children': [
            ('roading', 'road network adequacy', 'Roading suffers from maintenance and capacity issues.'),
            ('public_transport', 'public transport coverage', 'Public transport is limited and fragmented.'),
            ('active_modes', 'active travel infrastructure', 'Walking and cycling infrastructure gaps exist.'),
        ]
    },
    'infrastructure': {
        'root': ('deficit', 'infrastructure deficit', 'Infrastructure is aging and insufficient.'),
        'children': [
            ('water', 'water supply and management', 'Water supply is constrained.'),
            ('wastewater', 'wastewater treatment', 'Wastewater systems are stressed.'),
            ('digital', 'digital connectivity', 'Digital infrastructure gaps create barriers.'),
        ]
    },
    'environment': {
        'root': ('degradation', 'environmental degradation', 'Environmental systems face pressure.'),
        'children': [
            ('water_quality', 'freshwater quality', 'Water quality is degraded.'),
            ('biodiversity', 'biodiversity loss', 'Native biodiversity is threatened.'),
            ('coastal', 'coastal environments', 'Coastal habitats are under pressure.'),
        ]
    },
    'inequality': {
        'root': ('deprivation', 'deprivation and inequality', 'Deprivation is concentrated geographically.'),
        'children': [
            ('child_poverty', 'child poverty', 'Child poverty limits development.'),
            ('ethnic_gap', 'ethnic outcome gaps', 'Persistent gaps exist for Māori.'),
            ('geographic', 'geographic deprivation', 'Remote areas experience decline.'),
        ]
    },
    'crime': {
        'root': ('safety', 'crime and safety', 'Crime undermines community safety.'),
        'children': [
            ('family_violence', 'family violence', 'Family violence is endemic.'),
            ('youth_offending', 'youth crime', 'Youth offending is prevalent.'),
            ('drug_crime', 'drug-related crime', 'Methamphetamine fuels crime.'),
        ]
    },
    'health': {
        'root': ('outcomes', 'health outcomes', 'Health outcomes are poor and inequitable.'),
        'children': [
            ('mental_health', 'mental health', 'Mental health problems are rising.'),
            ('chronic_disease', 'chronic disease', 'Chronic diseases are prevalent.'),
            ('workforce', 'health workforce', 'Health workforce shortages limit services.'),
        ]
    },
    'education': {
        'root': ('achievement', 'educational achievement', 'Achievement is low and unequal.'),
        'children': [
            ('early_childhood', 'early childhood access', 'ECE participation is limited.'),
            ('secondary', 'secondary engagement', 'School disengagement is high.'),
            ('tertiary', 'tertiary access', 'Tertiary participation is limited.'),
        ]
    },
    'economy': {
        'root': ('development', 'economic development', 'Growth is constrained by concentration.'),
        'children': [
            ('employment', 'employment and jobs', 'Employment is low-wage and insecure.'),
            ('productivity', 'productivity', 'Productivity growth is weak.'),
            ('business', 'small business', 'Business formation is limited.'),
        ]
    },
    'governance': {
        'root': ('challenges', 'governance challenges', 'Governance does not adequately serve needs.'),
        'children': [
            ('local_govt', 'local government', 'Local government lacks capacity.'),
            ('treaty', 'Treaty partnership', 'Māori partnership is incomplete.'),
            ('accountability', 'accountability', 'Government accountability is weak.'),
        ]
    },
    'climate': {
        'root': ('risk', 'climate adaptation', 'Climate change poses multiple hazards.'),
        'children': [
            ('flooding', 'flood resilience', 'Flood risk is increasing.'),
            ('drought', 'drought and water scarcity', 'Drought stress is increasing.'),
            ('coastal', 'coastal hazards', 'Sea level rise threatens settlements.'),
        ]
    },
}

if __name__ == '__main__':
    for region_slug, region_info in REGIONS.items():
        print(f'Building {region_slug}...')

        region_display = region_info['display']

        print('  Generating sources...')
        sources = generate_sources(region_slug)
        print(f'    Created {len(sources)} sources')

        print('  Generating problems...')
        problems = generate_problems(region_slug, region_display)
        print(f'    Created {len(problems)} problems')

        print('  Generating claims...')
        claims = generate_claims(region_slug, region_display, sources)
        print(f'    Created {len(claims)} claims')

        print('  Generating drivers and camps...')
        drivers, camps = generate_drivers_and_camps(region_slug)
        print(f'    Created {len(drivers)} drivers and {len(camps)} camps')

        print(f'\nComplete for {region_slug}:')
        print(f'  Problems: {len(problems)} (44 × 1 root + 3 children)')
        print(f'  Claims: {len(claims)} (88 × 2 per problem)')
        print(f'  Drivers: {len(drivers)} (44 × 4 per theme)')
        print(f'  Camps: {len(camps)} (44 × 4 per theme)')
        print(f'  Sources: {len(sources)}')
        print(f'  Methodologies: 22 (copied from Wellington)')

    print('\n=== Generation complete ===')
