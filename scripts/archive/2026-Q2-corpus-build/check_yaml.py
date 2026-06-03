#!/usr/bin/env python3
"""Check YAML syntax for all modified claims."""
import yaml
from pathlib import Path

regions = ['hawkes-bay', 'taranaki']
errors = []

for region in regions:
    claim_dir = Path(f'content/{region}/data/claim')
    for yaml_file in claim_dir.glob('*.yaml'):
        try:
            with open(yaml_file) as f:
                data = yaml.safe_load(f)
                # Basic check: all required fields present
                required = ['id', 'statement', 'time_period', 'confidence', 'verification_status']
                for field in required:
                    if field not in data:
                        errors.append(f"{yaml_file.name}: missing field '{field}'")
        except Exception as e:
            errors.append(f"{yaml_file.name}: {e}")

if errors:
    print(f"YAML validation errors ({len(errors)}):")
    for err in errors:
        print(f"  {err}")
else:
    print("All YAML files valid!")
