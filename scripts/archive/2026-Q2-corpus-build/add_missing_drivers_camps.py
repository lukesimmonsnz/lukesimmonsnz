#!/usr/bin/env python3
"""
Add drivers and camps for missing root problems.
"""

import yaml
from pathlib import Path

MISSING_OTAGO_DRIVERS = [
    {'id': 'driver.otago.transport.connectivity_geography', 'name': 'Geographic Fragmentation',
     'description': 'Otago geography fragments the region across mountain ranges and basins.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.connectivity'], 'claim_ids': []},

    {'id': 'driver.otago.infrastructure.aging_assets', 'name': 'Aging Infrastructure Stock',
     'description': 'Dunedin and Otago infrastructure increasingly aging; replacement cycles accelerating.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.infrastructure.infrastructure'], 'claim_ids': []},

    {'id': 'driver.otago.environment.land_use_intensity', 'name': 'Land Use Intensity Expansion',
     'description': 'Agricultural and residential land use intensification increases environmental pressure.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.freshwater_stress'], 'claim_ids': []},

    {'id': 'driver.otago.inequality.structural_disadvantage', 'name': 'Structural Economic Disadvantage',
     'description': 'Historical economic structures create persistent inequality.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.inequality.inequality'], 'claim_ids': []},

    {'id': 'driver.otago.crime.social_disconnection', 'name': 'Social Disconnection and Isolation',
     'description': 'High-deprivation areas have weak social cohesion and community connection.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.crime.safety'], 'claim_ids': []},

    {'id': 'driver.otago.health.structural_health_factors', 'name': 'Structural Health Determinants',
     'description': 'Income, education, housing, and environmental factors drive health outcomes.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.health.health_outcomes'], 'claim_ids': []},

    {'id': 'driver.otago.education.educational_inequality', 'name': 'Educational Inequality by Deprivation',
     'description': 'Deprivation and rural location correlate with lower educational outcomes.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.education.achievement'], 'claim_ids': []},

    {'id': 'driver.otago.governance.institutional_fragmentation', 'name': 'Institutional Fragmentation',
     'description': 'Multiple governance layers (Regional, three TAs, DHB) create coordination challenges.',
     'theme': 'governance', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.governance.governance', 'problem.otago.governance.otago_hospital_governance'], 'claim_ids': []},

    {'id': 'driver.otago.economy.university_public_dependency', 'name': 'University Public Funding Dependency',
     'description': 'University of Otago heavily dependent on Crown funding; budget pressures.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.economy.university_economy'], 'claim_ids': []},

    {'id': 'driver.otago.climate.climate_change_intensity', 'name': 'Climate Change Intensity',
     'description': 'Climate change accelerates; impacts on water, temperature, extreme events.',
     'theme': 'climate-adaptation', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.climate.climate_risk'], 'claim_ids': []},

    {'id': 'driver.otago.environment.coastal_development', 'name': 'Coastal Urban and Industrial Development',
     'description': 'Dunedin and Port Chalmers development increases coastal ecosystem pressure.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.coastal_otago'], 'claim_ids': []},

    {'id': 'driver.otago.transport.southern_link_timeline', 'name': 'Southern Link Motorway Project Delays',
     'description': 'Dunedin Southern Link project timelines and funding pressures delay relief.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.dunedin_southern_link'], 'claim_ids': []},
]

MISSING_OTAGO_CAMPS = [
    {'id': 'camp.otago.transport.dunedin_southern_link_completion', 'name': 'Southern Link Project Completion',
     'theme': 'transport', 'core_claim': 'Completing Dunedin Southern Link motorway relieves congestion and improves regional connectivity.',
     'flagship_moves': ['Secure full project funding and accelerate construction',
                        'Manage traffic diversion during construction',
                        'Integrate with public transit planning'],
     'tensions': ['Construction cost and timeline uncertainty',
                  'Environmental impacts and community disruption'],
     'addresses': ['problem.otago.transport.dunedin_southern_link'],
     'interventions': [
         {'description': 'Complete Southern Link by 2030',
          'state_variable': 'motorway_capacity', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.governance.ota_coordination', 'name': 'Regional Coordination and Governance Integration',
     'theme': 'governance', 'core_claim': 'Strengthening Otago Regional Authority coordination improves cross-TA planning.',
     'flagship_moves': ['Enhance ORC mandate and resourcing for spatial planning',
                        'Establish joint council committees for key issues',
                        'Align three-waters and transport planning'],
     'tensions': ['TA autonomy preservation vs coordination',
                  'Cost of coordination mechanisms'],
     'addresses': ['problem.otago.governance.governance'],
     'interventions': [
         {'description': 'Establish unified growth management strategy',
          'state_variable': 'planning_coordination', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.environment.coast_protection', 'name': 'Coastal Ecosystem Protection',
     'theme': 'environment', 'core_claim': 'Marine protected areas and fishing restrictions restore Otago coast ecosystem.',
     'flagship_moves': ['Expand marine protected areas to 30% of Otago coast',
                        'Strengthen fishing regulations and enforcement',
                        'Invasive species control program'],
     'tensions': ['Fishing community resistance',
                  'DOC resourcing constraints'],
     'addresses': ['problem.otago.environment.coastal_otago'],
     'interventions': [
         {'description': 'Restore kelp forest and fish populations',
          'state_variable': 'coastal_ecosystem_health', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},
]

MISSING_SOUTHLAND_DRIVERS = [
    {'id': 'driver.southland.transport.geographic_isolation', 'name': 'Geographic Isolation',
     'description': 'Southland far from main population centers; limited transport corridors.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.southland.transport.connectivity'], 'claim_ids': []},

    {'id': 'driver.southland.infrastructure.aging_networks', 'name': 'Aging Infrastructure Networks',
     'description': 'Southland water, wastewater, and roading infrastructure aging.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.infrastructure.infrastructure'], 'claim_ids': []},

    {'id': 'driver.southland.environment.pastoral_pollution', 'name': 'Pastoral Production Pollution Legacy',
     'description': 'Decades of pastoral intensification created nutrient and bacterial pollution in rivers.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.environment.freshwater_degradation'], 'claim_ids': []},

    {'id': 'driver.southland.inequality.economic_decline', 'name': 'Economic Decline and Population Stagnation',
     'description': 'Limited economic opportunity drives out-migration and stagnation.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.inequality.deprivation'], 'claim_ids': []},

    {'id': 'driver.southland.crime.community_disconnection', 'name': 'Community Fragmentation and Disengagement',
     'description': 'Declining population and economic change weaken community bonds.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.crime.safety'], 'claim_ids': []},

    {'id': 'driver.southland.health.rural_access_barriers', 'name': 'Rural Healthcare Access Barriers',
     'description': 'Distance, population sparsity, and recruitment difficulty limit health access.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.health.health_outcomes'], 'claim_ids': []},

    {'id': 'driver.southland.education.rural_school_capacity', 'name': 'Rural School Capacity and Resourcing Constraints',
     'description': 'Small rural schools struggle with funding, staffing, and curriculum breadth.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.education.achievement'], 'claim_ids': []},

    {'id': 'driver.southland.governance.council_capacity', 'name': 'Local Government Capacity Constraints',
     'description': 'Southland councils face limited staffing and capability for complex projects.',
     'theme': 'governance', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.governance.governance'], 'claim_ids': []},

    {'id': 'driver.southland.economy.limited_diversification', 'name': 'Limited Economic Diversification',
     'description': 'Economy locked in commodities (dairy, smelter, fisheries); limited alternatives.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.economy.industrial_transition'], 'claim_ids': []},

    {'id': 'driver.southland.climate.rainfall_intensification', 'name': 'Rainfall Intensification',
     'description': 'Climate change drives more intense rainfall events; flood risk rises.',
     'theme': 'climate-adaptation', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.climate.climate_risk'], 'claim_ids': []},
]

MISSING_SOUTHLAND_CAMPS = [
    {'id': 'camp.southland.governance.local_govt_partnership', 'name': 'Enhanced Council Capability and Partnership',
     'theme': 'governance', 'core_claim': 'Strengthening council capability and cross-council partnerships improve governance effectiveness.',
     'flagship_moves': ['Upskill council planning and project management',
                        'Establish regional council working groups',
                        'Improve funding and shared services'],
     'tensions': ['Council autonomy vs partnership',
                  'Cost of upskilling and shared services'],
     'addresses': ['problem.southland.governance.governance'],
     'interventions': [
         {'description': 'Increase council capability in strategic planning',
          'state_variable': 'governance_capacity', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},
]

def write_missing_entities(region_slug, drivers, camps):
    """Write missing drivers and camps."""
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / f'content/{region_slug}/data'

    for driver in drivers:
        driver_id = driver['id'].split('.')[-1]
        with open(base_path / 'driver' / f'{driver_id}.yaml', 'w') as f:
            yaml.dump(driver, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    for camp in camps:
        camp_id = camp['id'].split('.')[-1]
        with open(base_path / 'camp' / f'{camp_id}.yaml', 'w') as f:
            yaml.dump(camp, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"✓ {region_slug}: {len(drivers)} drivers, {len(camps)} camps added")

# Execute
if __name__ == '__main__':
    write_missing_entities('otago', MISSING_OTAGO_DRIVERS, MISSING_OTAGO_CAMPS)
    write_missing_entities('southland', MISSING_SOUTHLAND_DRIVERS, MISSING_SOUTHLAND_CAMPS)
    print("\n✓ All missing entities added")
