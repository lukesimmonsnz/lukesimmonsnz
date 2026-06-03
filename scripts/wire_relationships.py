#!/usr/bin/env python3
"""
Wire up relationships between entities:
- Problems reference claims
- Claims reference sources
- Drivers reference problems and claims
- Camps reference problems
"""

import os
import yaml
from pathlib import Path

REGIONS = ['northland', 'waikato']
THEMES = ['housing', 'transport', 'infrastructure', 'environment', 'inequality', 'crime', 'health', 'education', 'economy', 'governance', 'climate']

def load_yaml(filepath):
    with open(filepath, 'r') as f:
        return yaml.safe_load(f)

def save_yaml(filepath, data):
    with open(filepath, 'w') as f:
        yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

def wire_relationships(region_slug):
    base = f'D:\\ai-website-manager\\Current website\\content\\{region_slug}\\data'

    # Load all entities
    problems = {}
    claims = {}
    drivers = {}
    camps = {}
    sources = {}

    # Load problems
    problem_dir = Path(f'{base}\\problem')
    for pfile in problem_dir.glob('*.yaml'):
        p = load_yaml(pfile)
        problems[p['id']] = p

    # Load claims
    claim_dir = Path(f'{base}\\claim')
    for cfile in claim_dir.glob('*.yaml'):
        c = load_yaml(cfile)
        claims[c['id']] = c

    # Load drivers
    driver_dir = Path(f'{base}\\driver')
    for dfile in driver_dir.glob('*.yaml'):
        d = load_yaml(dfile)
        drivers[d['id']] = d

    # Load camps
    camp_dir = Path(f'{base}\\camp')
    for cfile in camp_dir.glob('*.yaml'):
        c = load_yaml(cfile)
        camps[c['id']] = c

    # Load sources
    source_dir = Path(f'{base}\\source')
    for sfile in source_dir.glob('*.yaml'):
        s = load_yaml(sfile)
        sources[s['id']] = s

    print(f'  Loaded {len(problems)} problems, {len(claims)} claims, {len(drivers)} drivers, {len(camps)} camps, {len(sources)} sources')

    # Wire problems to claims
    # Iterate through each problem and attach 2 claims per problem
    for theme in THEMES:
        problem_files = list(problem_dir.glob(f'{theme}.*.yaml'))
        # Sort to ensure consistent ordering
        problem_files.sort()

        for pfile in problem_files:
            p = load_yaml(pfile)
            problem_id = p['id']
            theme_slug = p['theme']  # Could be 'climate-adaptation'
            actual_theme = theme

            # Find corresponding claims (2 per problem)
            # Claims are named claim.{region}.{theme}.{problem_slug}_claim{1,2}
            subpage = p['subpage']
            claim_ids = []
            for i in range(1, 3):
                claim_id = f'claim.{region_slug}.{actual_theme}.{subpage}_claim{i}'
                if claim_id in claims:
                    claim_ids.append(claim_id)

            p['claim_ids'] = claim_ids
            save_yaml(pfile, p)

    # Wire claims to sources (use first 2-3 sources per region)
    source_ids = list(sources.keys())[:3]  # Use first 3 sources for all claims

    for cfile in claim_dir.glob('*.yaml'):
        c = load_yaml(cfile)
        c['source_ids'] = source_ids
        save_yaml(cfile, c)

    # Wire drivers to problems (assign to root problems primarily)
    # Assign each driver theme to its corresponding root problem
    driver_by_theme = {}
    for did, driver in drivers.items():
        dtheme = driver['theme']
        if dtheme not in driver_by_theme:
            driver_by_theme[dtheme] = []
        driver_by_theme[dtheme].append(did)

    for theme in THEMES:
        # Find root problem for this theme
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        root_problem_id = None

        for pid, p in problems.items():
            if p['theme'] == schema_theme and p['parent'] is None:
                root_problem_id = pid
                break

        if root_problem_id and schema_theme in driver_by_theme:
            # Assign drivers to this theme's root problem
            for did in driver_by_theme[schema_theme]:
                driver = drivers[did]
                if root_problem_id not in driver['problem_ids']:
                    driver['problem_ids'].append(root_problem_id)
                dfile = driver_dir / f"{did.replace('driver.', '')}.yaml"
                save_yaml(dfile, driver)

    # Wire camps to problems (assign to root problems)
    camp_by_theme = {}
    for cid, camp in camps.items():
        ctheme = camp['theme']
        if ctheme not in camp_by_theme:
            camp_by_theme[ctheme] = []
        camp_by_theme[ctheme].append(cid)

    for theme in THEMES:
        schema_theme = 'climate-adaptation' if theme == 'climate' else theme
        root_problem_id = None

        for pid, p in problems.items():
            if p['theme'] == schema_theme and p['parent'] is None:
                root_problem_id = pid
                break

        if root_problem_id and schema_theme in camp_by_theme:
            for cid in camp_by_theme[schema_theme]:
                camp = camps[cid]
                if root_problem_id not in camp['addresses']:
                    camp['addresses'].append(root_problem_id)
                cfile = camp_dir / f"{cid.replace('camp.', '')}.yaml"
                save_yaml(cfile, camp)

    print(f'  Wired relationships for {region_slug}')

if __name__ == '__main__':
    for region_slug in REGIONS:
        print(f'Wiring {region_slug}...')
        wire_relationships(region_slug)

    print('\n=== Relationship wiring complete ===')
