#!/usr/bin/env python3
"""
Wire drivers, camps, and claims to problems.
"""

import yaml
from pathlib import Path
from collections import defaultdict

def wire_region(region_slug):
    """Wire drivers, camps, claims to problems."""
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / f'content/{region_slug}/data'

    # Load all problems and index by ID
    problems_by_id = {}
    problem_dir = base_path / 'problem'
    for prob_file in problem_dir.glob('*.yaml'):
        with open(prob_file, 'r') as f:
            prob_data = yaml.safe_load(f)
        problems_by_id[prob_data['id']] = prob_data

    # Load all drivers and wire them
    driver_dir = base_path / 'driver'
    for driver_file in driver_dir.glob('*.yaml'):
        with open(driver_file, 'r') as f:
            driver_data = yaml.safe_load(f)

        # For each problem this driver addresses, add the driver to problem.claim_ids
        for prob_id in driver_data.get('problem_ids', []):
            if prob_id in problems_by_id:
                prob = problems_by_id[prob_id]
                if 'claim_ids' not in prob:
                    prob['claim_ids'] = []
                # Don't add duplicates
                if prob_id not in prob.get('claim_ids', []):
                    pass  # We'll add claims below

    # Load all camps and wire them to problems
    camp_dir = base_path / 'camp'
    for camp_file in camp_dir.glob('*.yaml'):
        with open(camp_file, 'r') as f:
            camp_data = yaml.safe_load(f)

        # Camp addresses problems; we don't need to add references in problems

    # Load all claims and wire them to problems
    claim_dir = base_path / 'claim'
    claims_by_problem = defaultdict(list)

    for claim_file in claim_dir.glob('*.yaml'):
        with open(claim_file, 'r') as f:
            claim_data = yaml.safe_load(f)

        # Extract theme from claim ID (claim.{region}.{theme}.{descriptor})
        claim_parts = claim_data['id'].split('.')
        if len(claim_parts) >= 3:
            theme = claim_parts[2]
            # Find all problems with this theme and add the claim to them
            for prob_id, prob_data in problems_by_id.items():
                if prob_data.get('theme') == theme:
                    claims_by_problem[prob_id].append(claim_data['id'])

    # Now wire all claims to problems and add drivers
    for prob_id, prob_data in problems_by_id.items():
        # Add claims
        if prob_id in claims_by_problem:
            prob_data['claim_ids'] = list(set(prob_data.get('claim_ids', []) + claims_by_problem[prob_id]))

        # Save problem
        prob_filename = prob_data['id'].split('.')[-1] + '.yaml'
        with open(problem_dir / prob_filename, 'w') as f:
            yaml.dump(prob_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    # Wire drivers and camps back to problems (update problem.claim_ids if needed)
    for driver_file in driver_dir.glob('*.yaml'):
        with open(driver_file, 'r') as f:
            driver_data = yaml.safe_load(f)

        # Drivers are already wired via problem_ids

    print(f"✓ {region_slug}: wired claims to {len(problems_by_id)} problems")

    return len(problems_by_id)

# Execute
if __name__ == '__main__':
    for region in ['otago', 'southland']:
        wire_region(region)

    print("\n✓ All wiring complete")
