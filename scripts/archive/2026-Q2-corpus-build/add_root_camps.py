#!/usr/bin/env python3
"""
Add generic camps for remaining root problems.
"""

import yaml
from pathlib import Path

OTAGO_ROOT_CAMPS = [
    {'id': 'camp.otago.environment.integrated_catchment', 'name': 'Integrated Catchment Management',
     'theme': 'environment', 'core_claim': 'Coordinated management across land use and water addresses freshwater stress.',
     'flagship_moves': ['Catchment-scale planning and limits',
                        'Land-use zoning to protect riparian and aquatic ecosystems',
                        'Sustainable water allocation framework'],
     'tensions': ['Agricultural user resistance',
                  'Coordination complexity'],
     'addresses': ['problem.otago.environment.freshwater_stress'],
     'interventions': [
         {'description': 'Implement catchment-scale water limits',
          'state_variable': 'water_sustainability', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.health.holistic_health', 'name': 'Holistic Population Health Strategy',
     'theme': 'health', 'core_claim': 'Integrated public health, primary care, and health equity approach improves health outcomes.',
     'flagship_moves': ['Health promotion and disease prevention programs',
                        'Equitable primary care access and quality',
                        'Health equity focus in policy'],
     'tensions': ['Funding constraints',
                  'Behavioral change difficulty'],
     'addresses': ['problem.otago.health.health_outcomes'],
     'interventions': [
         {'description': 'Implement regional health equity strategy',
          'state_variable': 'health_equity', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.education.equity_support', 'name': 'Educational Equity and Support Systems',
     'theme': 'education', 'core_claim': 'Targeted support for disadvantaged students improves educational achievement.',
     'flagship_moves': ['School-level support systems (counselors, learning aids)',
                        'Disadvantaged student targeting and funding',
                        'Community and family engagement'],
     'tensions': ['School capacity and funding',
                  'Targeting and fairness debates'],
     'addresses': ['problem.otago.education.achievement'],
     'interventions': [
         {'description': 'Implement equity-focused school support system',
          'state_variable': 'educational_equity', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.inequality.structural_equity', 'name': 'Structural Inequality Reduction Strategy',
     'theme': 'inequality', 'core_claim': 'Addressing root causes of inequality (jobs, education, housing) reduces disparities.',
     'flagship_moves': ['Economic opportunity and job creation',
                        'Affordable housing development',
                        'Educational and skills pathways'],
     'tensions': ['High cost and long-term commitment',
                  'Sectoral coordination challenges'],
     'addresses': ['problem.otago.inequality.inequality'],
     'interventions': [
         {'description': 'Implement region-wide inequality reduction strategy',
          'state_variable': 'inequality_index', 'expected_sign': '-'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.crime.safety_ecosystem', 'name': 'Community Safety Ecosystem Strengthening',
     'theme': 'crime', 'core_claim': 'Integrated approach to community safety (prevention, policing, support) reduces crime.',
     'flagship_moves': ['Community-based crime prevention',
                        'Police-community partnership',
                        'Offender support and rehabilitation'],
     'tensions': ['Community engagement complexity',
                  'Police resource constraints'],
     'addresses': ['problem.otago.crime.safety'],
     'interventions': [
         {'description': 'Build community safety partnerships',
          'state_variable': 'community_safety_perception', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.infrastructure.renewal_program', 'name': 'Infrastructure Renewal and Upgrade Program',
     'theme': 'infrastructure', 'core_claim': 'Systematic infrastructure renewal improves resilience and service quality.',
     'flagship_moves': ['Infrastructure condition assessment and planning',
                        'Prioritized renewal schedule and funding',
                        'Asset management and maintenance'],
     'tensions': ['High cost and funding constraints',
                  'Service disruption during renewal'],
     'addresses': ['problem.otago.infrastructure.infrastructure'],
     'interventions': [
         {'description': 'Implement 10-year infrastructure renewal program',
          'state_variable': 'infrastructure_condition', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.governance.hospital_system', 'name': 'Southern DHB Governance and Planning',
     'theme': 'governance', 'core_claim': 'Strengthened DHB governance and planning ensures healthcare resilience.',
     'flagship_moves': ['Hospital rebuild completion and planning',
                        'Health system integration and efficiency',
                        'Workforce and service planning'],
     'tensions': ['Governance complexity across sectors',
                  'Service delivery pressures'],
     'addresses': ['problem.otago.governance.otago_hospital_governance'],
     'interventions': [
         {'description': 'Establish integrated DHB governance framework',
          'state_variable': 'health_system_resilience', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.climate.adaptation_framework', 'name': 'Climate Change Adaptation Framework',
     'theme': 'climate-adaptation', 'core_claim': 'Region-wide climate adaptation planning and investment reduces climate risk.',
     'flagship_moves': ['Climate risk assessment and adaptation planning',
                        'Infrastructure climate resilience investment',
                        'Sector-specific adaptation pathways'],
     'tensions': ['Upfront investment cost',
                  'Uncertainty in climate impacts'],
     'addresses': ['problem.otago.climate.climate_risk'],
     'interventions': [
         {'description': 'Develop and implement region-wide climate adaptation strategy',
          'state_variable': 'climate_adaptation_readiness', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},
]

SOUTHLAND_ROOT_CAMPS = [
    {'id': 'camp.southland.environment.river_restoration', 'name': 'Southland Rivers Restoration Program',
     'theme': 'environment', 'core_claim': 'Multi-stakeholder river restoration addresses degradation and restores ecosystem.',
     'flagship_moves': ['Nutrient and pollution reduction strategy',
                        'Riparian restoration and fencing',
                        'Alternative agricultural practices'],
     'tensions': ['Farmer cooperation and cost',
                  'Long restoration timeline'],
     'addresses': ['problem.southland.environment.freshwater_degradation'],
     'interventions': [
         {'description': 'Reduce river nutrient levels by 50%',
          'state_variable': 'river_water_quality', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.health.health_system', 'name': 'Southland Health System Strengthening',
     'theme': 'health', 'core_claim': 'Strengthening health workforce and services improves health outcomes.',
     'flagship_moves': ['Rural health workforce recruitment and retention',
                        'Primary care access expansion',
                        'Health promotion and prevention programs'],
     'tensions': ['Recruitment difficulty',
                  'Funding constraints'],
     'addresses': ['problem.southland.health.health_outcomes'],
     'interventions': [
         {'description': 'Improve rural health access',
          'state_variable': 'health_access_equity', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.education.regional_schools', 'name': 'Regional School Support and Development',
     'theme': 'education', 'core_claim': 'Supporting rural and small schools improves educational achievement.',
     'flagship_moves': ['School support network and shared services',
                        'Teacher recruitment and professional development',
                        'Curriculum breadth and technology access'],
     'tensions': ['School autonomy vs support',
                  'Funding and resourcing constraints'],
     'addresses': ['problem.southland.education.achievement'],
     'interventions': [
         {'description': 'Improve rural school achievement outcomes',
          'state_variable': 'ncea_achievement_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.inequality.deprivation_reduction', 'name': 'Deprivation and Inequality Reduction',
     'theme': 'inequality', 'core_claim': 'Targeted support for high-deprivation communities reduces structural inequality.',
     'flagship_moves': ['Community-led economic development',
                        'Social service and support coordination',
                        'Youth opportunity pathways'],
     'tensions': ['Community trust and engagement',
                  'Sustained funding requirement'],
     'addresses': ['problem.southland.inequality.deprivation'],
     'interventions': [
         {'description': 'Reduce deprivation index in high-deprivation areas',
          'state_variable': 'deprivation_index', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.crime.community_safety', 'name': 'Community Safety and Youth Engagement',
     'theme': 'crime', 'core_claim': 'Community-based crime prevention and youth engagement reduce crime and offending.',
     'flagship_moves': ['Youth mentoring and engagement programs',
                        'Community policing and partnerships',
                        'Crime prevention through environmental design'],
     'tensions': ['Community engagement difficulty',
                  'Police resource constraints'],
     'addresses': ['problem.southland.crime.safety'],
     'interventions': [
         {'description': 'Establish youth mentoring program',
          'state_variable': 'youth_engagement_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.climate.climate_adaptation', 'name': 'Southland Climate Adaptation Strategy',
     'theme': 'climate-adaptation', 'core_claim': 'Region-wide climate adaptation planning reduces climate impacts.',
     'flagship_moves': ['Climate risk assessment and adaptation planning',
                        'Agricultural adaptation support',
                        'Coastal adaptation planning'],
     'tensions': ['Upfront investment',
                  'Behavioral change'],
     'addresses': ['problem.southland.climate.climate_risk'],
     'interventions': [
         {'description': 'Develop region-wide climate adaptation strategy',
          'state_variable': 'climate_readiness', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},
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
    write_camps('otago', OTAGO_ROOT_CAMPS)
    write_camps('southland', SOUTHLAND_ROOT_CAMPS)
    print("\n✓ Root problem camps added")
