#!/usr/bin/env python3
"""Fix Nelson corpus."""

import yaml
from pathlib import Path

region_dir = "nelson"
region_slug = "nelson"

THEMES = {
    "housing": ["affordability", "land_supply", "rental_market", "infrastructure_cost"],
    "transport": ["connectivity", "connectivity_2", "connectivity_3", "connectivity_4"],
    "infrastructure": ["infrastructure", "infrastructure_2", "infrastructure_3", "infrastructure_4"],
    "environment": ["coastal_environment", "sea_level_risk", "water_quality", "marine_ecosystem"],
    "inequality": ["inequality_root", "child_poverty", "rental_affordability_gap", "rural_isolation"],
    "crime": ["safety", "family_violence", "youth_offending", "drug_crime"],
    "health": ["health_outcomes", "mental_health", "chronic_disease", "workforce"],
    "education": ["achievement", "early_childhood", "secondary", "tertiary_access"],
    "economy": ["economic_structure", "economic_2", "economic_3", "economic_4"],
    "governance": ["governance_root", "growth_management", "treaty", "capacity"],
    "climate": ["climate_risk", "climate_2", "climate_3", "climate_4"],
}

def write_problem(problem_id, parent_id, theme, order):
    path = Path(f"content/{region_dir}/data/problem") / f"{theme}.{problem_id}.yaml"
    data = {
        "id": f"problem.{region_dir}.{theme}.{problem_id}",
        "title": f"Problem: {problem_id.replace('_', ' ').title()}",
        "theme": theme,
        "section": "climate-adaptation" if theme == "climate" else theme,
        "subpage": problem_id,
        "parent": parent_id,
        "order": order,
        "updated": "2026-04-26",
        "summary": f"Description of {problem_id} in {region_dir}.",
        "manifests_in": [region_slug],
        "systems_model": {"state_variables": [], "inputs": [], "constraints": [], "feedback_loops": []},
        "narrative": [],
        "claim_ids": [],
        "status": "draft"
    }
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

def write_claim(claim_id, theme, problem_id):
    path = Path(f"content/{region_dir}/data/claim") / f"{theme}.{claim_id}.yaml"
    data = {
        "id": f"claim.{region_dir}.{theme}.{claim_id}",
        "statement": f"Claim regarding {claim_id.replace('_', ' ')} in {region_dir}.",
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

def write_driver(driver_id, theme, problem_ids):
    path = Path(f"content/{region_dir}/data/driver") / f"{theme}.{driver_id}.yaml"
    data = {
        "id": f"driver.{region_dir}.{theme}.{driver_id}",
        "name": f"Driver: {driver_id.replace('_', ' ').title()}",
        "description": f"A structural driver contributing to {theme} challenges.",
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

def write_camp(camp_id, theme, problem_ids):
    path = Path(f"content/{region_dir}/data/camp") / f"{theme}.{camp_id}.yaml"
    data = {
        "id": f"camp.{region_dir}.{theme}.{camp_id}",
        "name": f"Response: {camp_id.replace('_', ' ').title()}",
        "theme": theme,
        "core_claim": f"A response strategy addressing {theme} challenges.",
        "flagship_moves": [],
        "tensions": [],
        "addresses": problem_ids,
        "interventions": [],
        "applicable_in": [region_slug],
        "tensions_with": []
    }
    with open(path, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)

# Delete all existing files
import glob
for f in glob.glob(f"content/{region_dir}/data/problem/*.yaml"):
    Path(f).unlink()
for f in glob.glob(f"content/{region_dir}/data/claim/*.yaml"):
    Path(f).unlink()
for f in glob.glob(f"content/{region_dir}/data/driver/*.yaml"):
    Path(f).unlink()
for f in glob.glob(f"content/{region_dir}/data/camp/*.yaml"):
    Path(f).unlink()

for theme, problem_list in THEMES.items():
    root_problem = problem_list[0]
    children = problem_list[1:]

    write_problem(root_problem, None, theme, 1)
    for order, child in enumerate(children, 2):
        write_problem(child, root_problem, theme, order)

    for problem in problem_list:
        claim_id = f"{problem}_claim"
        write_claim(claim_id, theme, f"problem.{region_dir}.{theme}.{problem}")

    for driver_idx in range(1, 3):
        driver_id = f"driver_{driver_idx}"
        problem_ids = [f"problem.{region_dir}.{theme}.{root_problem}",
                       f"problem.{region_dir}.{theme}.{children[driver_idx - 1] if driver_idx <= len(children) else children[0]}"]
        write_driver(driver_id, theme, problem_ids)

    for camp_idx in range(1, 3):
        camp_id = f"camp_{camp_idx}"
        problem_ids = [f"problem.{region_dir}.{theme}.{root_problem}",
                       f"problem.{region_dir}.{theme}.{children[camp_idx - 1] if camp_idx <= len(children) else children[0]}"]
        write_camp(camp_id, theme, problem_ids)

print("Nelson fixed")
