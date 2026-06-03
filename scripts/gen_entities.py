#!/usr/bin/env python3
"""Generate YAML entity files for Northland and Waikato."""
import os
from pathlib import Path

def write(path, content):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)

for region in ['northland', 'waikato']:
    base = f'D:\\ai-website-manager\\Current website\\content\\{region}\\data'

    # Create 16 sources
    for i in range(1, 17):
        content = f"""id: source.{region}_report_{i:02d}
title: Report {i}
author: Agencies
publisher: Government
year: 2023
url: null
type: government
credibility: authoritative
geo_granularity:
- {region}
notes: null
"""
        write(f'{base}\\source\\report_{i:02d}.yaml', content)

print('Created sources for both regions')
