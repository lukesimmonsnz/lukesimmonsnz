#!/usr/bin/env python3
"""
Build complete Northland and Waikato corpora using direct string templates.
"""

import os
from pathlib import Path
from datetime import datetime

REGIONS = ['northland', 'waikato']
THEMES = ['housing', 'transport', 'infrastructure', 'environment', 'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate']

REGION_DISPLAY = {
    'northland': 'Te Tai Tokerau Northland',
    'waikato': 'Waikato',
}

def write_file(path, content):
    """Write a file ensuring directory exists."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def problem_template(problem_id, title, theme, section, subpage, parent, order, summary, region, claim_ids):
    """Generate YAML for a problem."""
    manifests_in = f"- {region}\n"
    claim_ids_yaml = "\n".join([f"- {cid}" for cid in claim_ids])

    return f"""id: {problem_id}
title: {title}
theme: {theme}
section: {section}
subpage: {subpage}
parent: {parent}
order: {order}
updated: '2026-04-26'
summary: {summary}
manifests_in:
{manifests_in}systems_model:
  state_variables: []
  inputs: []
  constraints: []
  feedback_loops: []
narrative:
- heading: Overview
  body: {summary}
claim_ids:
{claim_ids_yaml}
status: draft
"""

def claim_template(claim_id, statement, region, source_ids):
    """Generate YAML for a claim."""
    sources_yaml = "\n".join([f"- {sid}" for sid in source_ids])
    return f"""id: {claim_id}
statement: {statement}
value: null
unit: null
time_period: '2024'
confidence: medium
verification_status: cited_only
last_verified: null
source_ids:
{sources_yaml}
scoped_to:
- {region}
national_assertion: false
region_mentions:
- {region}
methodology_tag: null
notes: null
"""

def driver_template(driver_id, name, description, theme):
    """Generate YAML for a driver."""
    return f"""id: {driver_id}
name: {name}
description: {description}
theme: {theme}
consensus: consensus
category: institutional
timescale: medium
scope: regional
problem_ids: []
claim_ids: []
"""

def camp_template(camp_id, name, theme, region):
    """Generate YAML for a camp."""
    return f"""id: {camp_id}
name: {name}
theme: {theme}
core_claim: {name} is a key strategy.
flagship_moves:
- Establish governance
- Allocate funding
- Build engagement
tensions:
- Implementation requires coordination
- Resource constraints limit scale
addresses: []
interventions:
- description: Implement {name.lower()}
  state_variable: null
  expected_sign: '+'
applicable_in:
- {region}
tensions_with: []
"""

def source_template(source_id, title, region):
    """Generate YAML for a source."""
    return f"""id: {source_id}
title: {title}
author: Regional agencies
publisher: Government/Community
year: 2023
url: null
type: government
credibility: authoritative
geo_granularity:
- {region}
notes: null
"""

# Problem specifications
PROBLEMS = {
    'housing': {
        'root': ('affordability', 'housing unaffordability', 'Housing has become structurally unaffordable, driven by supply constraints, demand pressure, and limited policy coordination.'),
        'children': [
            ('land_supply', 'constrained residential land supply', 'Usable residential land supply is restricted by physical constraints, zoning rules, and infrastructure capacity.'),
            ('rental_market', 'rental market affordability and security', 'Renters face rising costs and housing insecurity, with limited inventory and weak tenure protections.'),
            ('homelessness', 'homelessness and housing stress', 'Extreme housing stress manifests in rough sleeping, family homelessness, and emergency shelter demand.'),
        ]
    },
    'transport': {
        'root': ('connectivity', 'transport connectivity challenges', 'Transport networks constrain regional connectivity and access to employment and services.'),
        'children': [
            ('roading', 'road network adequacy', 'Regional roading networks suffer from deferred maintenance, safety risks, and capacity constraints.'),
            ('public_transport', 'public transport coverage and viability', 'Public transport is limited in frequency, route coverage, and service integration.'),
            ('active_modes', 'active travel infrastructure', 'Walking and cycling infrastructure gaps discourage active mode uptake.'),
        ]
    },
    'infrastructure': {
        'root': ('deficit', 'infrastructure deficit and ageing', 'Critical infrastructure is ageing, under-maintained, and insufficient to support regional growth.'),
        'children': [
            ('water', 'water supply and demand management', 'Water supply is constrained by availability, quality, and competition between uses.'),
            ('wastewater', 'wastewater treatment and stormwater', 'Wastewater and stormwater systems are stressed by growth and environmental standards.'),
            ('digital', 'digital connectivity', 'Digital infrastructure gaps create rural accessibility and affordability barriers.'),
        ]
    },
    'environment': {
        'root': ('degradation', 'environmental degradation and pressure', 'Environmental systems face pressure from land use, pollution, and climate change.'),
        'children': [
            ('water_quality', 'freshwater quality', 'Freshwater quality is degraded by agricultural runoff, urban discharge, and land use intensification.'),
            ('biodiversity', 'terrestrial and aquatic biodiversity', 'Native biodiversity is threatened by habitat loss, invasive species, and predation.'),
            ('coastal', 'coastal environments and marine resources', 'Coastal habitats and fisheries are under pressure from development, pollution, and overharvesting.'),
        ]
    },
    'inequality': {
        'root': ('deprivation', 'deprivation and inequality', 'Deprivation is concentrated geographically and affects health, education, and economic outcomes.'),
        'children': [
            ('child_poverty', 'child poverty and welfare', 'Child poverty limits life-course development and intergenerational mobility.'),
            ('ethnic_gap', 'ethnic and indigenous outcome gaps', 'Māori and Pacific peoples experience persistent gaps in income, health, and achievement.'),
            ('geographic', 'geographic and rural deprivation', 'Remote and rural areas experience economic decline and service withdrawal.'),
        ]
    },
    'crime': {
        'root': ('safety', 'crime and personal safety', 'Crime and violence undermine community safety and wellbeing.'),
        'children': [
            ('family_violence', 'family and domestic violence', 'Family violence is endemic and disproportionately affects vulnerable populations.'),
            ('youth_offending', 'youth crime and offending', 'Youth offending is driven by deprivation, disengagement, and limited opportunity.'),
            ('drug_crime', 'drug-related crime and harm', 'Methamphetamine and other drug use fuels acquisitive and violent crime.'),
        ]
    },
    'health': {
        'root': ('outcomes', 'health outcomes and access', 'Health outcomes are poor and inequitably distributed across the population.'),
        'children': [
            ('mental_health', 'mental health and wellbeing', 'Mental health problems are rising, especially among young people and Māori.'),
            ('chronic_disease', 'chronic disease burden', 'Chronic diseases including diabetes, obesity, and CVD are prevalent and preventable.'),
            ('workforce', 'health workforce and services', 'Health workforce shortages limit service capacity and accessibility.'),
        ]
    },
    'education': {
        'root': ('achievement', 'educational achievement and equity', 'Educational achievement is low and unequally distributed by ethnicity, gender, and deprivation.'),
        'children': [
            ('early_childhood', 'early childhood education access', 'Early childhood education participation is limited by cost and availability.'),
            ('secondary', 'secondary school engagement and attainment', 'Secondary school disengagement and low NCEA attainment limit employment prospects.'),
            ('tertiary', 'tertiary education and skills', 'Tertiary participation is limited and skill mismatches persist in labour market.'),
        ]
    },
    'economy': {
        'root': ('development', 'economic development and growth', 'Economic growth is constrained by sectoral concentration, low productivity, and limited diversification.'),
        'children': [
            ('employment', 'employment and job quality', 'Employment is characterized by low wages, job insecurity, and limited career advancement.'),
            ('productivity', 'labour and multi-factor productivity', 'Productivity growth is weak relative to national trends and peer regions.'),
            ('business', 'small business viability and growth', 'Small business formation and survival are hampered by capital access and market constraints.'),
        ]
    },
    'governance': {
        'root': ('challenges', 'governance and democratic participation', 'Governance structures and processes do not adequately serve community needs and expectations.'),
        'children': [
            ('local_govt', 'local government capacity and coordination', 'Local government agencies lack capacity, coordination, and community connection.'),
            ('treaty', 'Treaty partnership and iwi engagement', 'Māori partnership in governance is incomplete and hampered by institutional barriers.'),
            ('accountability', 'government accountability and transparency', 'Government accountability mechanisms are weak and citizen participation is low.'),
        ]
    },
    'climate': {
        'root': ('risk', 'climate change adaptation and resilience', 'Climate change poses multiple hazards to which adaptation is insufficient.'),
        'children': [
            ('flooding', 'flood risk and resilience', 'Rainfall intensification and river flooding pose increasing risks to development and infrastructure.'),
            ('drought', 'drought and water scarcity', 'Drought stress is increasing, threatening agricultural production and water security.'),
            ('coastal', 'coastal hazards and sea level rise', 'Sea level rise and storm surge threaten coastal infrastructure and settlements.'),
        ]
    },
}

CLAIM_STATEMENTS = {
    'housing.affordability': ['Housing affordability has deteriorated with median multiples reaching unsustainable levels.', 'Population growth has outpaced residential development.'],
    'housing.land_supply': ['Developable land is restricted by geographic and infrastructure constraints.', 'Zoned capacity exceeds deliverable supply.'],
    'housing.rental_market': ['Rental costs exceed affordability thresholds.', 'Rental vacancy rates are critically low.'],
    'housing.homelessness': ['Homelessness has increased significantly.', 'Emergency housing demand exceeds services.'],
    'transport.connectivity': ['Transport network topology creates connectivity bottlenecks.', 'Networks constrain rural employment access.'],
    'transport.roading': ['Road maintenance backlogs threaten safety.', 'Roading capacity is inadequate.'],
    'transport.public_transport': ['Public transport frequency is insufficient.', 'Service fragmentation creates barriers.'],
    'transport.active_modes': ['Active travel infrastructure gaps limit adoption.', 'Safety concerns discourage active modes.'],
    'infrastructure.deficit': ['Critical infrastructure is aging and inadequate.', 'Deferred maintenance creates risks.'],
    'infrastructure.water': ['Water availability is constrained seasonally.', 'Water quality fails environmental standards.'],
    'infrastructure.wastewater': ['Wastewater treatment is stressed by growth.', 'Stormwater discharge impacts environment.'],
    'infrastructure.digital': ['Rural broadband connectivity is inadequate.', 'Digital affordability excludes vulnerable groups.'],
    'environment.degradation': ['Environmental degradation is driven by land use.', 'Ecosystem services are declining.'],
    'environment.water_quality': ['Freshwater quality is degraded by runoff.', 'Waterway contamination affects health.'],
    'environment.biodiversity': ['Native habitat is declining.', 'Invasive species threaten endemic fauna.'],
    'environment.coastal': ['Coastal development increases hazard exposure.', 'Fisheries stocks are declining.'],
    'inequality.deprivation': ['Deprivation is geographically concentrated.', 'Deprivation drives poor outcomes.'],
    'inequality.child_poverty': ['Child material hardship rates are high.', 'Poverty limits early development.'],
    'inequality.ethnic_gap': ['Māori experience persistent income gaps.', 'Health outcome gaps reflect barriers.'],
    'inequality.geographic': ['Rural incomes lag urban equivalents.', 'Service withdrawal creates gaps.'],
    'crime.safety': ['Crime rates exceed national averages in deprived areas.', 'Community confidence is declining.'],
    'crime.family_violence': ['Family violence incidents have increased.', 'Violence affects vulnerable groups.'],
    'crime.youth_offending': ['Youth offending rates are highest among disengaged youth.', 'Recidivism is high.'],
    'crime.drug_crime': ['Methamphetamine use fuels acquisitive crime.', 'Drug crime is concentrated in deprived areas.'],
    'health.outcomes': ['Health outcomes are below national averages.', 'Health inequities reflect barriers.'],
    'health.mental_health': ['Mental health demand exceeds capacity.', 'Youth mental health rates are elevated.'],
    'health.chronic_disease': ['Obesity prevalence contributes to disease burden.', 'Chronic disease management is hampered.'],
    'health.workforce': ['GP shortages limit primary care access.', 'Health workforce is unevenly distributed.'],
    'education.achievement': ['NCEA attainment rates are below average.', 'Achievement gaps are largest for Māori.'],
    'education.early_childhood': ['ECE participation is lower in deprived areas.', 'Cost is a significant barrier.'],
    'education.secondary': ['Secondary disengagement leads to high truancy.', 'NCEA gaps persist across subjects.'],
    'education.tertiary': ['Tertiary participation is below average.', 'First-generation students face barriers.'],
    'economy.development': ['Economic growth lags national trends.', 'Sectoral concentration limits resilience.'],
    'economy.employment': ['Unemployment rates exceed national averages.', 'Wages are significantly below equivalents.'],
    'economy.productivity': ['Labour productivity is below average.', 'Multi-factor productivity is stagnant.'],
    'economy.business': ['Business formation rates are lower than average.', 'Small business failure exceeds benchmarks.'],
    'governance.challenges': ['Multi-agency governance creates inefficiency.', 'Democratic participation is declining.'],
    'governance.local_govt': ['Local government capacity is constrained.', 'Multi-council coordination is weak.'],
    'governance.treaty': ['Māori partnership remains incomplete.', 'Treaty settlement implementation lags.'],
    'governance.accountability': ['Government accountability mechanisms are weak.', 'Citizen engagement is limited.'],
    'climate.risk': ['Climate change poses multiple hazards.', 'Current adaptation is insufficient.'],
    'climate.flooding': ['Flood risk is increasing.', 'Flood-prone development exposes populations.'],
    'climate.drought': ['Drought stress is increasing.', 'Water security is threatened.'],
    'climate.coastal': ['Sea level rise threatens infrastructure.', 'Storm surge frequency is increasing.'],
}

def build_region(region_slug):
    """Build complete corpus for a region."""
    region_display = REGION_DISPLAY[region_slug]
    base_dir = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data'

    # Generate sources
    source_list = []
    source_titles = [
        'Regional Council Spatial Planning Report',
        'City Council Annual Plan and Reporting',
        'Ministry Statistics and Census Data',
        'Health Service Delivery Report',
        'Police Crime Statistics and Analysis',
        'Education Ministry Performance Report',
        'Economic Development Strategy Report',
        'Environmental State of Environment Report',
        'Transport and Roading Strategy',
        'Housing and Urban Development Report',
        'Social Welfare and Family Support Report',
        'Treaty Settlement Implementation Plan',
        'Infrastructure Asset Management Plan',
        'Digital Connectivity and Access Report',
        'Employment and Labour Market Report',
        'Community Engagement and Governance Report',
    ]

    for i, title in enumerate(source_titles, 1):
        source_id = f'source.{region_slug}_report_{i:02d}'
        source_list.append(source_id)
        content = source_template(source_id, title, region_slug)
        write_file(f'{base_dir}\\source\\{region_slug}_report_{i:02d}.yaml', content)

    print(f'  Created {len(source_list)} sources for {region_slug}')

    # Generate problems and claims
    problem_count = 0
    claim_count = 0

    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        problem_spec = PROBLEMS[theme]

        # Root problem
        root_id_comp, root_title_part, root_summary = problem_spec['root']
        root_prob_id = f'problem.{region_slug}.{theme}.{root_id_comp}'

        claim_ids = [
            f'claim.{region_slug}.{theme}.{root_id_comp}_claim1',
            f'claim.{region_slug}.{theme}.{root_id_comp}_claim2',
        ]

        prob_title = f'{region_display}: {root_title_part}'
        content = problem_template(root_prob_id, prob_title, schema_theme, theme, root_id_comp, 'null', 1, root_summary, region_slug, claim_ids)
        write_file(f'{base_dir}\\problem\\{theme}.{root_id_comp}.yaml', content)
        problem_count += 1

        # Create claims for root
        key = f'{theme}.{root_id_comp}'
        statements = CLAIM_STATEMENTS.get(key, ['Claim 1 about this issue.', 'Claim 2 about this issue.'])
        for j, stmt in enumerate(statements, 1):
            claim_id = f'claim.{region_slug}.{theme}.{root_id_comp}_claim{j}'
            sources = source_list[:2]
            content = claim_template(claim_id, stmt, region_slug, sources)
            write_file(f'{base_dir}\\claim\\{theme}.{root_id_comp}_claim{j}.yaml', content)
            claim_count += 1

        # Child problems
        for child_idx, (child_id_comp, child_title_part, child_summary) in enumerate(problem_spec['children'], start=2):
            child_prob_id = f'problem.{region_slug}.{theme}.{child_id_comp}'

            claim_ids = [
                f'claim.{region_slug}.{theme}.{child_id_comp}_claim1',
                f'claim.{region_slug}.{theme}.{child_id_comp}_claim2',
            ]

            prob_title = f'{region_display}: {child_title_part}'
            content = problem_template(child_prob_id, prob_title, schema_theme, theme, child_id_comp, root_prob_id, child_idx + 1, child_summary, region_slug, claim_ids)
            write_file(f'{base_dir}\\problem\\{theme}.{child_id_comp}.yaml', content)
            problem_count += 1

            # Create claims for child
            key = f'{theme}.{child_id_comp}'
            statements = CLAIM_STATEMENTS.get(key, ['Claim 1 about this issue.', 'Claim 2 about this issue.'])
            for j, stmt in enumerate(statements, 1):
                claim_id = f'claim.{region_slug}.{theme}.{child_id_comp}_claim{j}'
                sources = source_list[:2]
                content = claim_template(claim_id, stmt, region_slug, sources)
                write_file(f'{base_dir}\\claim\\{theme}.{child_id_comp}_claim{j}.yaml', content)
                claim_count += 1

    print(f'  Created {problem_count} problems and {claim_count} claims for {region_slug}')

    # Generate drivers (4 per theme)
    driver_count = 0
    driver_types = ['Regulatory', 'Funding', 'Technical', 'Behavioral']
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        for i in range(1, 5):
            driver_id = f'driver.{region_slug}.{theme}.driver_{i}'
            driver_type = driver_types[i-1]
            name = f'{driver_type} barrier in {theme}'
            description = f'{name} in regional context.'
            content = driver_template(driver_id, name, description, schema_theme)
            write_file(f'{base_dir}\\driver\\{theme}.driver_{i}.yaml', content)
            driver_count += 1

    print(f'  Created {driver_count} drivers for {region_slug}')

    # Generate camps (4 per theme)
    camp_count = 0
    camp_types = ['Policy', 'Investment', 'Community', 'Innovation']
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        for i in range(1, 5):
            camp_id = f'camp.{region_slug}.{theme}.camp_{i}'
            camp_type = camp_types[i-1]
            name = f'{camp_type} response in {theme}'
            content = camp_template(camp_id, name, schema_theme, region_slug)
            write_file(f'{base_dir}\\camp\\{theme}.camp_{i}.yaml', content)
            camp_count += 1

    print(f'  Created {camp_count} camps for {region_slug}')

    return {
        'problems': problem_count,
        'claims': claim_count,
        'drivers': driver_count,
        'camps': camp_count,
        'sources': len(source_list),
    }

if __name__ == '__main__':
    for region_slug in REGIONS:
        print(f'\nBuilding {region_slug}...')
        counts = build_region(region_slug)
        print(f'\n{region_slug} summary:')
        for key, val in counts.items():
            print(f'  {key}: {val}')

    print('\n=== Corpus generation complete ===')
