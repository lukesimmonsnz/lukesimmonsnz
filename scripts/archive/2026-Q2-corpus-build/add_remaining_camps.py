#!/usr/bin/env python3
"""
Add camps for remaining unaddressed problems.
"""

import yaml
from pathlib import Path

REMAINING_OTAGO_CAMPS = [
    {'id': 'camp.otago.transport.queenstown_transit_demand', 'name': 'Queenstown Traffic Demand Management',
     'theme': 'transport', 'core_claim': 'Congestion pricing and visitor management reduce traffic on SH6.',
     'flagship_moves': ['Implement congestion pricing on SH6 approach',
                        'Visitor reservation system for peak periods',
                        'Shuttle and transit services for tourists'],
     'tensions': ['Tourism industry resistance',
                  'Equity concerns for workers'],
     'addresses': ['problem.otago.transport.queenstown_congestion'],
     'interventions': [],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.crime.queenstown_visitor_management', 'name': 'Queenstown Visitor Management and Safety',
     'theme': 'crime', 'core_claim': 'Visitor information, venue management, and police visibility reduce visitor crime.',
     'flagship_moves': ['Visitor safety orientation and conduct expectations',
                        'Enhanced venue safety standards and training',
                        'Increased police patrols in CBD'],
     'tensions': ['Tourism image concerns',
                  'Police resource constraints'],
     'addresses': ['problem.otago.crime.queenstown_visitor_crime'],
     'interventions': [],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.economy.university_investment', 'name': 'University Investment and Anchor Institution Strategy',
     'theme': 'economy', 'core_claim': 'Strategic investment in University of Otago sustains Dunedin economy.',
     'flagship_moves': ['Crown funding commitment to University',
                        'University-led research and innovation hubs',
                        'Student and staff retention strategies'],
     'tensions': ['Fiscal constraints',
                  'University autonomy and mission questions'],
     'addresses': ['problem.otago.economy.university_economy'],
     'interventions': [],
     'applicable_in': ['otago'], 'tensions_with': []},
]

REMAINING_SOUTHLAND_CAMPS = [
    # Southland camps for root problems without camps
]

def write_camps(region_slug, camps):
    """Write camps."""
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / f'content/{region_slug}/data'

    for camp in camps:
        camp_id = camp['id'].split('.')[-1]
        with open(base_path / 'camp' / f'{camp_id}.yaml', 'w') as f:
            yaml.dump(camp, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"✓ {region_slug}: {len(camps)} camps added")

# Execute
if __name__ == '__main__':
    write_camps('otago', REMAINING_OTAGO_CAMPS)
    write_camps('southland', REMAINING_SOUTHLAND_CAMPS)
    print("\n✓ Remaining camps added")
