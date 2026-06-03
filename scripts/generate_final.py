#!/usr/bin/env python3
import os
from pathlib import Path

REGIONS = ['northland', 'waikato']
THEMES = ['housing', 'transport', 'infrastructure', 'environment', 'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate']

REGION_DISPLAY = {'northland': 'Te Tai Tokerau Northland', 'waikato': 'Waikato'}

PROBLEM_SPECS = {
    'housing': [('affordability', 'housing unaffordability', 'Structural unaffordability driven by supply constraints.'),
                [('land_supply', 'land supply', 'Land restricted by constraints.'),
                 ('rental_market', 'rental affordability', 'Renters face rising costs.'),
                 ('homelessness', 'homelessness', 'Housing stress manifests in emergency need.')]],
    'transport': [('connectivity', 'transport connectivity', 'Networks constrain connectivity.'),
                  [('roading', 'road adequacy', 'Roading suffers from maintenance issues.'),
                   ('public_transport', 'public transport', 'Public transport is limited.'),
                   ('active_modes', 'active travel', 'Infrastructure gaps discourage active modes.')]],
    'infrastructure': [('deficit', 'infrastructure deficit', 'Infrastructure is aging and insufficient.'),
                       [('water', 'water supply', 'Water supply is constrained.'),
                        ('wastewater', 'wastewater', 'Wastewater systems are stressed.'),
                        ('digital', 'digital connectivity', 'Digital gaps create barriers.')]],
    'environment': [('degradation', 'environmental degradation', 'Environmental systems face pressure.'),
                    [('water_quality', 'water quality', 'Freshwater quality is degraded.'),
                     ('biodiversity', 'biodiversity', 'Native biodiversity is threatened.'),
                     ('coastal', 'coastal environments', 'Coastal habitats are under pressure.')]],
    'inequality': [('deprivation', 'deprivation and inequality', 'Deprivation is concentrated geographically.'),
                   [('child_poverty', 'child poverty', 'Child poverty limits development.'),
                    ('ethnic_gap', 'ethnic gaps', 'Persistent gaps exist for Māori.'),
                    ('geographic', 'geographic deprivation', 'Remote areas experience decline.')]],
    'crime': [('safety', 'crime and safety', 'Crime undermines community safety.'),
              [('family_violence', 'family violence', 'Family violence is endemic.'),
               ('youth_offending', 'youth crime', 'Youth offending is prevalent.'),
               ('drug_crime', 'drug crime', 'Methamphetamine fuels crime.')]],
    'health': [('outcomes', 'health outcomes', 'Health outcomes are poor and inequitable.'),
               [('mental_health', 'mental health', 'Mental health problems are rising.'),
                ('chronic_disease', 'chronic disease', 'Chronic diseases are prevalent.'),
                ('workforce', 'health workforce', 'Health workforce shortages exist.')]],
    'education': [('achievement', 'educational achievement', 'Achievement is low and unequal.'),
                  [('early_childhood', 'early childhood', 'ECE participation is limited.'),
                   ('secondary', 'secondary engagement', 'School disengagement is high.'),
                   ('tertiary', 'tertiary access', 'Tertiary participation is limited.')]],
    'economy': [('development', 'economic development', 'Growth is constrained by concentration.'),
                [('employment', 'employment', 'Employment is low-wage and insecure.'),
                 ('productivity', 'productivity', 'Productivity growth is weak.'),
                 ('business', 'small business', 'Business formation is limited.')]],
    'governance': [('challenges', 'governance challenges', 'Governance does not adequately serve needs.'),
                   [('local_govt', 'local government', 'Local government lacks capacity.'),
                    ('treaty', 'Treaty partnership', 'Māori partnership is incomplete.'),
                    ('accountability', 'accountability', 'Government accountability is weak.')]],
    'climate': [('risk', 'climate adaptation', 'Climate change poses multiple hazards.'),
                [('flooding', 'flood resilience', 'Flood risk is increasing.'),
                 ('drought', 'drought and water', 'Drought stress is increasing.'),
                 ('coastal', 'coastal hazards', 'Sea level rise threatens settlements.')]],
}

def yaml_str(data, indent=0):
    lines = []
    prefix = ' ' * indent
    if isinstance(data, dict):
        for k, v in data.items():
            if v is None:
                lines.append(f"{prefix}{k}: null")
            elif isinstance(v, list):
                if not v:
                    lines.append(f"{prefix}{k}: []")
                else:
                    lines.append(f"{prefix}{k}:")
                    for item in v:
                        if isinstance(item, dict):
                            lines.append(f"{prefix}- ")
                            for line in yaml_str(item, indent+2).split('\n'):
                                if line: lines.append(line)
                        else:
                            lines.append(f"{prefix}- {item}")
            elif isinstance(v, dict):
                lines.append(f"{prefix}{k}:")
                for line in yaml_str(v, indent+2).split('\n'):
                    if line: lines.append(line)
            else:
                lines.append(f"{prefix}{k}: {v}")
    return '\n'.join(lines)

def write_yaml(path, data):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(yaml_str(data) + '\n')

def build_region(region):
    display = REGION_DISPLAY[region]
    base = f'D:\\ai-website-manager\\Current website\\content\\{region}\\data'

    # Sources
    sources = []
    for i in range(1, 17):
        sid = f'source.{region}_report_{i:02d}'
        sources.append(sid)
        data = {
            'id': sid,
            'title': f'Regional Report {i}',
            'author': 'Regional agencies',
            'publisher': 'Government',
            'year': 2023,
            'url': None,
            'type': 'government',
            'credibility': 'authoritative',
            'geo_granularity': [region],
            'notes': None,
        }
        write_yaml(f'{base}\\source\\{region}_report_{i:02d}.yaml', data)

    # Problems
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        root_spec, child_specs = PROBLEM_SPECS[theme]
        root_id, root_title, root_summary = root_spec

        # Root problem
        root_pid = f'problem.{region}.{theme}.{root_id}'
        root_data = {
            'id': root_pid,
            'title': f'{display}: {root_title}',
            'theme': schema_theme,
            'section': theme,
            'subpage': root_id,
            'parent': None,
            'order': 1,
            'updated': '2026-04-26',
            'summary': root_summary,
            'manifests_in': [region],
            'systems_model': {'state_variables': [], 'inputs': [], 'constraints': [], 'feedback_loops': []},
            'narrative': [{'heading': 'Overview', 'body': root_summary}],
            'claim_ids': [f'claim.{region}.{theme}.{root_id}_claim1', f'claim.{region}.{theme}.{root_id}_claim2'],
            'status': 'draft',
        }
        write_yaml(f'{base}\\problem\\{theme}.{root_id}.yaml', root_data)

        # Root claims
        for j in [1, 2]:
            cid = f'claim.{region}.{theme}.{root_id}_claim{j}'
            cdata = {
                'id': cid,
                'statement': f'Claim about {root_title}.',
                'value': None,
                'unit': None,
                'time_period': '2024',
                'confidence': 'medium',
                'verification_status': 'cited_only',
                'last_verified': None,
                'source_ids': sources[:2],
                'scoped_to': [region],
                'national_assertion': False,
                'region_mentions': [region],
                'methodology_tag': None,
                'notes': None,
            }
            write_yaml(f'{base}\\claim\\{theme}.{root_id}_claim{j}.yaml', cdata)

        # Child problems
        for order, (child_id, child_title, child_summary) in enumerate(child_specs, start=2):
            child_pid = f'problem.{region}.{theme}.{child_id}'
            cdata = {
                'id': child_pid,
                'title': f'{display}: {child_title}',
                'theme': schema_theme,
                'section': theme,
                'subpage': child_id,
                'parent': root_pid,
                'order': order + 1,
                'updated': '2026-04-26',
                'summary': child_summary,
                'manifests_in': [region],
                'systems_model': {'state_variables': [], 'inputs': [], 'constraints': [], 'feedback_loops': []},
                'narrative': [{'heading': 'Overview', 'body': child_summary}],
                'claim_ids': [f'claim.{region}.{theme}.{child_id}_claim1', f'claim.{region}.{theme}.{child_id}_claim2'],
                'status': 'draft',
            }
            write_yaml(f'{base}\\problem\\{theme}.{child_id}.yaml', cdata)

            # Child claims
            for j in [1, 2]:
                ccid = f'claim.{region}.{theme}.{child_id}_claim{j}'
                ccdata = {
                    'id': ccid,
                    'statement': f'Claim about {child_title}.',
                    'value': None,
                    'unit': None,
                    'time_period': '2024',
                    'confidence': 'medium',
                    'verification_status': 'cited_only',
                    'last_verified': None,
                    'source_ids': sources[:2],
                    'scoped_to': [region],
                    'national_assertion': False,
                    'region_mentions': [region],
                    'methodology_tag': None,
                    'notes': None,
                }
                write_yaml(f'{base}\\claim\\{theme}.{child_id}_claim{j}.yaml', ccdata)

    # Drivers
    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        for i in range(1, 5):
            did = f'driver.{region}.{theme}.driver_{i}'
            ddata = {
                'id': did,
                'name': f'Driver {i} for {theme}',
                'description': f'Driver {i} description.',
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
                'name': f'Camp {i} for {theme}',
                'theme': schema_theme,
                'core_claim': f'Camp {i} is a strategy.',
                'flagship_moves': ['Move 1', 'Move 2', 'Move 3'],
                'tensions': ['Tension 1', 'Tension 2'],
                'addresses': [],
                'interventions': [{'description': 'Intervention', 'state_variable': None, 'expected_sign': '+'}],
                'applicable_in': [region],
                'tensions_with': [],
            }
            write_yaml(f'{base}\\camp\\{theme}.camp_{i}.yaml', cdata)

    print(f'Built {region}: 44 problems, 88 claims, 44 drivers, 44 camps, 16 sources')

if __name__ == '__main__':
    for region in REGIONS:
        build_region(region)
    print('Done!')
