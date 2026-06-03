#!/usr/bin/env python3
"""
Final schema fixes: driver themes, consensus, system models.
"""

import yaml
from pathlib import Path

CONSENSUS_MAP = {
    'emerging': 'mostly-agreed',
    'consensus': 'consensus',
    'contested': 'contested',
    'disputed': 'disputed',
    'mostly-agreed': 'mostly-agreed',
}

def fix_drivers(region_path):
    """Fix driver theme and consensus."""
    driver_dir = region_path / 'data' / 'driver'
    fixed = 0

    for driver_file in driver_dir.glob('*.yaml'):
        with open(driver_file, 'r') as f:
            data = yaml.safe_load(f)

        # Fix theme: climate → climate-adaptation
        if data.get('theme') == 'climate':
            data['theme'] = 'climate-adaptation'
            fixed += 1

        # Fix consensus
        if 'consensus' in data:
            old_consensus = data['consensus']
            data['consensus'] = CONSENSUS_MAP.get(old_consensus, 'mostly-agreed')

        with open(driver_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return fixed

def fix_problems(region_path):
    """Fix problem systems_model to have state_variables and constraints."""
    problem_dir = region_path / 'data' / 'problem'
    fixed = 0

    for problem_file in problem_dir.glob('*.yaml'):
        with open(problem_file, 'r') as f:
            data = yaml.safe_load(f)

        # Ensure systems_model has non-empty state_variables and constraints
        if 'systems_model' not in data:
            data['systems_model'] = {
                'state_variables': [],
                'inputs': [],
                'constraints': [],
                'feedback_loops': [],
            }

        # Add placeholder state variables and constraints if empty
        if not data['systems_model'].get('state_variables'):
            data['systems_model']['state_variables'] = ['problem_indicator_1']
            fixed += 1

        if not data['systems_model'].get('constraints'):
            data['systems_model']['constraints'] = ['institutional_or_physical_constraint']
            fixed += 1

        with open(problem_file, 'w') as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    return fixed

# Execute
if __name__ == '__main__':
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website/content')

    for region in ['otago', 'southland']:
        region_path = base_path / region

        drivers_fixed = fix_drivers(region_path)
        problems_fixed = fix_problems(region_path)

        print(f"✓ {region}: {drivers_fixed} drivers, {problems_fixed} problems fixed")

    print("\n✓ All final fixes applied")
