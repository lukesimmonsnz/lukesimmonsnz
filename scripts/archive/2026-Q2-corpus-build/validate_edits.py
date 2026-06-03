#!/usr/bin/env python3
"""Validate all YAML files in Hawke's Bay and Taranaki."""
import yaml
from pathlib import Path
import sys

def validate_region(region_slug):
    claim_dir = Path(f'content/{region_slug}/data/claim')
    errors = []
    valid_count = 0

    for yaml_file in sorted(claim_dir.glob('*.yaml')):
        try:
            with open(yaml_file, 'r') as f:
                data = yaml.safe_load(f)

            # Check required fields
            required = ['id', 'statement', 'time_period', 'confidence', 'verification_status']
            for field in required:
                if field not in data:
                    errors.append(f"{yaml_file.name}: missing '{field}'")

            # Check statement is not empty
            stmt = data.get('statement', '').strip()
            if not stmt:
                errors.append(f"{yaml_file.name}: empty statement")
            elif len(stmt) < 20:
                errors.append(f"{yaml_file.name}: suspiciously short statement ({len(stmt)} chars)")

            if not errors or yaml_file.name not in [e.split(':')[0] for e in errors]:
                valid_count += 1

        except Exception as e:
            errors.append(f"{yaml_file.name}: {type(e).__name__}: {e}")

    return valid_count, errors

print("Validating Hawke's Bay...")
hb_valid, hb_errors = validate_region('hawkes-bay')
print(f"  Valid: {hb_valid}")
if hb_errors:
    print(f"  Errors ({len(hb_errors)}):")
    for e in hb_errors[:10]:  # First 10
        print(f"    {e}")
    if len(hb_errors) > 10:
        print(f"    ... and {len(hb_errors) - 10} more")

print("\nValidating Taranaki...")
ta_valid, ta_errors = validate_region('taranaki')
print(f"  Valid: {ta_valid}")
if ta_errors:
    print(f"  Errors ({len(ta_errors)}):")
    for e in ta_errors[:10]:
        print(f"    {e}")

sys.exit(0 if not (hb_errors or ta_errors) else 1)
