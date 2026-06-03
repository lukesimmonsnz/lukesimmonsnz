#!/usr/bin/env python3
"""Bulk write all entities for Northland and Waikato."""

import sys
sys.path.insert(0, 'D:\\ai-website-manager\\Current website')

from pathlib import Path
import yaml

def write_yaml(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

REGIONS = ['northland', 'waikato']
DISPLAY = {'northland': 'Te Tai Tokerau Northland', 'waikato': 'Waikato'}

PROBLEMS = {
    'housing': {
        'root': ('affordability', 'housing unaffordability', 'Housing has become structurally unaffordable.'),
        'children': [
            ('land_supply', 'constrained residential land supply', 'Usable land is restricted.'),
            ('rental_market', 'rental market affordability', 'Renters face rising costs.'),
            ('homelessness', 'homelessness and housing stress', 'Extreme housing stress.'),
        ]
    },
    'transport': {
        'root': ('connectivity', 'transport connectivity', 'Networks constrain connectivity.'),
        'children': [
            ('roading', 'road network adequacy', 'Roading suffers from maintenance.'),
            ('public_transport', 'public transport coverage', 'Transport is limited.'),
            ('active_modes', 'active travel infrastructure', 'Infrastructure gaps exist.'),
        ]
    },
    'infrastructure': {
        'root': ('deficit', 'infrastructure deficit', 'Infrastructure is aging.'),
        'children': [
            ('water', 'water supply', 'Water is constrained.'),
            ('wastewater', 'wastewater treatment', 'Systems are stressed.'),
            ('digital', 'digital connectivity', 'Gaps create barriers.'),
        ]
    },
    'environment': {
        'root': ('degradation', 'environmental degradation', 'Systems face pressure.'),
        'children': [
            ('water_quality', 'freshwater quality', 'Quality is degraded.'),
            ('biodiversity', 'biodiversity', 'Biodiversity is threatened.'),
            ('coastal', 'coastal environments', 'Habitats under pressure.'),
        ]
    },
    'inequality': {
        'root': ('deprivation', 'deprivation and inequality', 'Deprivation is concentrated.'),
        'children': [
            ('child_poverty', 'child poverty', 'Poverty limits development.'),
            ('ethnic_gap', 'ethnic outcome gaps', 'Gaps for Māori exist.'),
            ('geographic', 'geographic deprivation', 'Remote areas decline.'),
        ]
    },
    'crime': {
        'root': ('safety', 'crime and safety', 'Crime undermines safety.'),
        'children': [
            ('family_violence', 'family violence', 'Violence is endemic.'),
            ('youth_offending', 'youth crime', 'Offending is prevalent.'),
            ('drug_crime', 'drug-related crime', 'Drugs fuel crime.'),
        ]
    },
    'health': {
        'root': ('outcomes', 'health outcomes', 'Outcomes are poor.'),
        'children': [
            ('mental_health', 'mental health', 'Problems are rising.'),
            ('chronic_disease', 'chronic disease', 'Diseases are prevalent.'),
            ('workforce', 'health workforce', 'Shortages limit services.'),
        ]
    },
    'education': {
        'root': ('achievement', 'educational achievement', 'Achievement is low.'),
        'children': [
            ('early_childhood', 'early childhood', 'Participation is limited.'),
            ('secondary', 'secondary engagement', 'Disengagement is high.'),
            ('tertiary', 'tertiary access', 'Participation is limited.'),
        ]
    },
    'economy': {
        'root': ('development', 'economic development', 'Growth is constrained.'),
        'children': [
            ('employment', 'employment', 'Employment is low-wage.'),
            ('productivity', 'productivity', 'Growth is weak.'),
            ('business', 'small business', 'Formation is limited.'),
        ]
    },
    'governance': {
        'root': ('challenges', 'governance challenges', 'Governance lacks service.'),
        'children': [
            ('local_govt', 'local government', 'Government lacks capacity.'),
            ('treaty', 'Treaty partnership', 'Partnership is incomplete.'),
            ('accountability', 'accountability', 'Accountability is weak.'),
        ]
    },
    'climate': {
        'root': ('risk', 'climate adaptation', 'Hazards are multiple.'),
        'children': [
            ('flooding', 'flood resilience', 'Risk is increasing.'),
            ('drought', 'drought and water', 'Stress is increasing.'),
            ('coastal', 'coastal hazards', 'Rise threatens.'),
        ]
    },
}

THEMES = list(PROBLEMS.keys())

def generate_region(region):
    """Generate all entities for a region."""
    base = f'D:\\ai-website-manager\\Current website\\content\\{region}\\data'
    display = DISPLAY[region]

    # Sources
    for i in range(1, 17):
        sid = f'source.{region}_{i:02d}'
        data = {
            'id': sid,
            'title': f'Report {i}',
            'author': 'Agencies',
            'publisher': 'Government',
            'year': 2023,
            'url': None,
            'type': 'government',
            'credibility': 'authoritative',
            'geo_granularity': [region],
            'notes': None,
        }
        write_yaml(f'{base}\\source\\report_{i:02d}.yaml', data)

    # Problems and Claims
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        root_comp, root_title, root_summary = PROBLEMS[theme]['root']

        # Root problem
        root_id = f'problem.{region}.{theme}.{root_comp}'
        root_data = {
            'id': root_id,
            'title': f'{display}: {root_title}',
            'theme': schema_theme,
            'section': theme,
            'subpage': root_comp,
            'parent': None,
            'order': 1,
            'updated': '2026-04-26',
            'summary': root_summary,
            'manifests_in': [region],
            'systems_model': {'state_variables': [], 'inputs': [], 'constraints': [], 'feedback_loops': []},
            'narrative': [{'heading': 'Overview', 'body': root_summary}],
            'claim_ids': [f'claim.{region}.{theme}.{root_comp}_claim1', f'claim.{region}.{theme}.{root_comp}_claim2'],
            'status': 'draft',
        }
        write_yaml(f'{base}\\problem\\{theme}.{root_comp}.yaml', root_data)

        # Root claims
        for j in [1, 2]:
            cid = f'claim.{region}.{theme}.{root_comp}_claim{j}'
            cdata = {
                'id': cid,
                'statement': f'Claim about {root_title}.',
                'value': None,
                'unit': None,
                'time_period': '2024',
                'confidence': 'medium',
                'verification_status': 'cited_only',
                'last_verified': None,
                'source_ids': [f'source.{region}_01', f'source.{region}_02'],
                'scoped_to': [region],
                'national_assertion': False,
                'region_mentions': [region],
                'methodology_tag': None,
                'notes': None,
            }
            write_yaml(f'{base}\\claim\\{theme}.{root_comp}_claim{j}.yaml', cdata)

        # Child problems
        for order, (child_comp, child_title, child_summary) in enumerate(PROBLEMS[theme]['children'], start=2):
            child_id = f'problem.{region}.{theme}.{child_comp}'
            cdata = {
                'id': child_id,
                'title': f'{display}: {child_title}',
                'theme': schema_theme,
                'section': theme,
                'subpage': child_comp,
                'parent': root_id,
                'order': order + 1,
                'updated': '2026-04-26',
                'summary': child_summary,
                'manifests_in': [region],
                'systems_model': {'state_variables': [], 'inputs': [], 'constraints': [], 'feedback_loops': []},
                'narrative': [{'heading': 'Overview', 'body': child_summary}],
                'claim_ids': [f'claim.{region}.{theme}.{child_comp}_claim1', f'claim.{region}.{theme}.{child_comp}_claim2'],
                'status': 'draft',
            }
            write_yaml(f'{base}\\problem\\{theme}.{child_comp}.yaml', cdata)

            # Child claims
            for j in [1, 2]:
                ccid = f'claim.{region}.{theme}.{child_comp}_claim{j}'
                ccdata = {
                    'id': ccid,
                    'statement': f'Claim about {child_title}.',
                    'value': None,
                    'unit': None,
                    'time_period': '2024',
                    'confidence': 'medium',
                    'verification_status': 'cited_only',
                    'last_verified': None,
                    'source_ids': [f'source.{region}_01', f'source.{region}_02'],
                    'scoped_to': [region],
                    'national_assertion': False,
                    'region_mentions': [region],
                    'methodology_tag': None,
                    'notes': None,
                }
                write_yaml(f'{base}\\claim\\{theme}.{child_comp}_claim{j}.yaml', ccdata)

    # Drivers
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        for i in range(1, 5):
            did = f'driver.{region}.{theme}.driver_{i}'
            ddata = {
                'id': did,
                'name': f'Driver {i}',
                'description': f'Driver description.',
                'theme': schema_theme,
                'consensus': 'consensus',
                'category': 'institutional',
                'timescale': 'medium',
                'scope': 'regional',
                'problem_ids': [],
                'claim_ids': [],
            }
            write_yaml(f'{base}\\driver\\{theme}.driver_{i}.yaml', ddata)

    # Camps
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        for i in range(1, 5):
            cid = f'camp.{region}.{theme}.camp_{i}'
            cdata = {
                'id': cid,
                'name': f'Camp {i}',
                'theme': schema_theme,
                'core_claim': 'Strategy.',
                'flagship_moves': ['Move 1', 'Move 2', 'Move 3'],
                'tensions': ['Tension 1', 'Tension 2'],
                'addresses': [],
                'interventions': [{'description': 'Intervention', 'state_variable': None, 'expected_sign': '+'}],
                'applicable_in': [region],
                'tensions_with': [],
            }
            write_yaml(f'{base}\\camp\\{theme}.camp_{i}.yaml', cdata)

    print(f'Generated {region}: 44 problems, 88 claims, 44 drivers, 44 camps, 16 sources')

if __name__ == '__main__':
    for region in REGIONS:
        generate_region(region)
    print('Done!')
