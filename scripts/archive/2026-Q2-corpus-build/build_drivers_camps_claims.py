#!/usr/bin/env python3
"""
Build drivers, camps, claims for Otago and Southland corpora.
Target: ~55 drivers, ~55 camps, ~90 claims per region.
"""

import yaml
from pathlib import Path

DATE = '2026-04-26'

# ============================================================================
# Helper functions
# ============================================================================

def write_yaml_file(directory, filename, data):
    """Write YAML file preserving order and formatting."""
    path = Path(directory) / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

# ============================================================================
# Drivers: 1–2 per problem, covering main causal factors
# ============================================================================

OTAGO_DRIVERS = [
    # Housing
    {'id': 'driver.otago.housing.topographic_constraint', 'name': 'Topographic Developable Land Constraint',
     'description': 'Dunedin and Queenstown surrounded by steep terrain and valleys; limited flat land suitable for residential development.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.housing.housing_market', 'problem.otago.housing.queenstown_affordability'],
     'claim_ids': []},
    {'id': 'driver.otago.housing.investor_demand', 'name': 'Property Investor Capital Inflows',
     'description': 'Queenstown investment property purchases from external capital (domestic and international); speculative demand.',
     'theme': 'housing', 'consensus': 'contested', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.housing.queenstown_affordability'],
     'claim_ids': []},
    {'id': 'driver.otago.housing.student_population_inelastic', 'name': 'Inelastic Student Rental Demand',
     'description': 'University of Otago ~20k students with limited off-campus alternatives; landlords have pricing power.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.housing.dunedin_student_rental'],
     'claim_ids': []},
    {'id': 'driver.otago.housing.low_wage_sector_dominance', 'name': 'Low-Wage Sector Employment Dominance',
     'description': 'Hospitality, retail, care work dominate employment; median wages lag cost of living growth.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.housing.worker_housing'],
     'claim_ids': []},

    # Transport
    {'id': 'driver.otago.transport.tourism_growth', 'name': 'Tourism-Driven Traffic Growth',
     'description': 'Queenstown-Lakes visitor arrivals compound; seasonal peaks, rental vehicle growth.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.queenstown_congestion'],
     'claim_ids': []},
    {'id': 'driver.otago.transport.singleroute_dependency', 'name': 'Single-Route Dependency (SH6, SH94)',
     'description': 'Queenstown-Lakes and Fiordland access via single highways; no alternative routes.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.queenstown_congestion'],
     'claim_ids': []},
    {'id': 'driver.otago.transport.modal_bias_cars', 'name': 'Car-Oriented Land Use and Modal Bias',
     'description': 'Urban sprawl, parking-free development, limited pedestrian/cycle infrastructure encourage vehicle use.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.active_modes'],
     'claim_ids': []},
    {'id': 'driver.otago.transport.climate_winter', 'name': 'Winter Weather Cycle',
     'description': 'Central Otago alpine pass closures; winter cold discourages walking/cycling.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.transport.active_modes'],
     'claim_ids': []},

    # Infrastructure
    {'id': 'driver.otago.infrastructure.hospital_complexity', 'name': 'Hospital Seismic and Infrastructure Complexity',
     'description': 'Dunedin hospital seismic upgrades required; rebuild complexity and cost escalation.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.infrastructure.infrastructure', 'problem.otago.infrastructure.otago_hospital_rebuild'],
     'claim_ids': []},
    {'id': 'driver.otago.infrastructure.population_growth_pressure', 'name': 'Rapid Population Growth in Queenstown-Lakes',
     'description': 'Queenstown-Lakes population growing >3% p.a., outpacing infrastructure capacity.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.infrastructure.wakatipu_water'],
     'claim_ids': []},
    {'id': 'driver.otago.infrastructure.rural_digital_cost', 'name': 'Rural Broadband Deployment Cost Barriers',
     'description': 'Low population density, topography, and private sector economics limit fibre rollout.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.infrastructure.digital_rural'],
     'claim_ids': []},

    # Environment
    {'id': 'driver.otago.environment.irrigation_expansion', 'name': 'Irrigation Expansion in Central Otago',
     'description': 'Wine and horticulture growth drives irrigation demand and water allocation pressure.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.freshwater_stress', 'problem.otago.environment.irrigation_water_quality'],
     'claim_ids': []},
    {'id': 'driver.otago.environment.pastoral_intensification', 'name': 'Pastoral Farming Intensification',
     'description': 'Nutrient loading from pastoral systems; fencing removal, riparian degradation.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.lake_eutrophication'],
     'claim_ids': []},
    {'id': 'driver.otago.environment.stormwater_urban_runoff', 'name': 'Urban Stormwater Pollution',
     'description': 'Dunedin and Queenstown stormwater carries nutrients, sediment, hydrocarbons to lakes and coast.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.coastal_otago'],
     'claim_ids': []},
    {'id': 'driver.otago.environment.tourism_pressure_marine', 'name': 'Marine Tourism Pressure',
     'description': 'Boat traffic, fishing, invasive species transport via tourism activities.',
     'theme': 'environment', 'consensus': 'emerging', 'category': 'demographic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.environment.coastal_otago'],
     'claim_ids': []},

    # Inequality
    {'id': 'driver.otago.inequality.tourism_jobs_precarity', 'name': 'Seasonal Tourism Employment Precarity',
     'description': 'Hospitality jobs seasonal, low-wage, minimal benefits; worker churn high.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.inequality.queenstown_worker_conditions'],
     'claim_ids': []},
    {'id': 'driver.otago.inequality.youth_unemployment_east_dunedin', 'name': 'Youth Unemployment and Inactivity',
     'description': 'East Dunedin deprivation drives youth disengagement from labour market.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.inequality.dunedin_deprivation'],
     'claim_ids': []},
    {'id': 'driver.otago.inequality.rural_service_distance', 'name': 'Rural Service Distance and Transport Costs',
     'description': 'Central Otago and remote areas far from services; transport costs high.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.otago.inequality.rural_isolation'],
     'claim_ids': []},

    # Crime
    {'id': 'driver.otago.crime.family_violence_normalization', 'name': 'Family Violence Normalization in High-Deprivation Areas',
     'description': 'Dunedin East and rural Otago have intergenerational family violence; social tolerance high.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.crime.family_violence'],
     'claim_ids': []},
    {'id': 'driver.otago.crime.youth_gang_recruitment', 'name': 'Gang Recruitment and Youth Engagement',
     'description': 'East Dunedin gang presence attracts disengaged youth; limited mentoring alternatives.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.crime.youth_offending'],
     'claim_ids': []},
    {'id': 'driver.otago.crime.visitor_alcohol_environment', 'name': 'Visitor Alcohol Consumption and Venue Culture',
     'description': 'Queenstown CBD late-night alcohol venues; high BAC assault rates among visitors.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.crime.queenstown_visitor_crime'],
     'claim_ids': []},

    # Health
    {'id': 'driver.otago.health.student_mental_health_stress', 'name': 'Student Mental Health Stress',
     'description': 'University of Otago students face isolation, financial stress, competitive pressure; mental health crisis.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.health.mental_health'],
     'claim_ids': []},
    {'id': 'driver.otago.health.chronic_disease_lifestyle', 'name': 'Lifestyle Risk Factor Prevalence',
     'description': 'Dunedin and rural Otago higher rates of obesity, sedentary behavior, smoking.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.health.chronic_disease'],
     'claim_ids': []},
    {'id': 'driver.otago.health.rural_gp_shortage', 'name': 'Rural GP Recruitment and Retention Crisis',
     'description': 'Central Otago GPs aging; training pipeline short; locum reliance high.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.health.rural_workforce'],
     'claim_ids': []},

    # Education
    {'id': 'driver.otago.education.affordability_rural_ece', 'name': 'ECE Affordability Barrier in Rural Areas',
     'description': 'Rural Otago ECE providers struggle with funding; parent fees high.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.education.early_childhood'],
     'claim_ids': []},
    {'id': 'driver.otago.education.ncea_support_gap', 'name': 'NCEA Pastoral Support System Under-Resourcing',
     'description': 'Rural schools lack counsellors, learning support staff; pastoral response limited.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.education.secondary'],
     'claim_ids': []},
    {'id': 'driver.otago.education.housing_tertiary_students', 'name': 'Tertiary Student Housing Stress',
     'description': 'University of Otago and Polytechnic students face rental market pressure; housing insecurity high.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.education.tertiary_dunedin'],
     'claim_ids': []},

    # Economy
    {'id': 'driver.otago.economy.tourism_dependency_queenstown', 'name': 'Tourism Sector Single-Dependency',
     'description': 'Queenstown economy >40% from tourism; external shocks (COVID, currency) create volatility.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.economy.tourism_queenstown'],
     'claim_ids': []},
    {'id': 'driver.otago.economy.commodity_price_volatility', 'name': 'Agricultural Commodity Price Volatility',
     'description': 'Wine, fruit, pastoral prices volatile; margins compressed.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.economy.agri_primary'],
     'claim_ids': []},
    {'id': 'driver.otago.economy.university_public_funding_cuts', 'name': 'University Sector Public Funding Pressure',
     'description': 'Crown funding to universities constrained; University of Otago faces budget pressures.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.economy.university_economy'],
     'claim_ids': []},
    {'id': 'driver.otago.economy.limited_startup_ecosystem', 'name': 'Limited Startup and Innovation Ecosystem',
     'description': 'Dunedin and Otago lack venture capital, tech talent pool, business infrastructure.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.economy.economic_structure'],
     'claim_ids': []},

    # Governance
    {'id': 'driver.otago.governance.planning_lag_growth', 'name': 'Planning Response Lag to Rapid Growth',
     'description': 'QLDC planning processes slower than Queenstown population growth.',
     'theme': 'governance', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.otago.governance.queenstown_growth_management'],
     'claim_ids': []},
    {'id': 'driver.otago.governance.ngai_tahu_cogovernance_expansion', 'name': 'Ngāi Tahu Co-Governance Rights Expansion',
     'description': 'Treaty settlement and co-governance mandate expanding; institutional complexity increasing.',
     'theme': 'governance', 'consensus': 'contested', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.governance.treaty_ngai_tahu'],
     'claim_ids': []},
    {'id': 'driver.otago.governance.hospital_rebuild_coordination', 'name': 'Hospital Rebuild Project Coordination Complexity',
     'description': 'Multi-stakeholder coordination (DHB, council, government) creates governance challenges.',
     'theme': 'governance', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.governance.otago_hospital_governance'],
     'claim_ids': []},

    # Climate
    {'id': 'driver.otago.climate.drought_aridity', 'name': 'Central Otago Aridity and Drought Frequency',
     'description': 'Central Otago NZ\'s driest region; climate change extends dry season.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.climate.drought_central_otago'],
     'claim_ids': []},
    {'id': 'driver.otago.climate.alpine_snowpack_decline', 'name': 'Alpine Snowpack and Glacier Decline',
     'description': 'Otago alps losing glaciers and snowpack; impacts hydro supply, water availability, avalanche risk.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.otago.climate.alpine_hazards'],
     'claim_ids': []},
    {'id': 'driver.otago.climate.sea_level_rise_dunedin', 'name': 'Sea Level Rise and Storm Surge Risk',
     'description': 'Dunedin and Port Chalmers face 0.5–1.0m sea level rise by 2100; storm surge and tsunami risk.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.otago.climate.coastal_dunedin'],
     'claim_ids': []},
]

SOUTHLAND_DRIVERS = [
    # Housing
    {'id': 'driver.southland.housing.population_stagnation', 'name': 'Southland Population Stagnation and Out-Migration',
     'description': 'Southland population declining or flat; reduces housing demand.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.housing.housing_market'],
     'claim_ids': []},
    {'id': 'driver.southland.housing.low_incomes', 'name': 'Low Income Levels',
     'description': 'Southland median incomes below national average; affordability ratio inflated.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.housing.invercargill_affordability'],
     'claim_ids': []},
    {'id': 'driver.southland.housing.rural_stock_aging', 'name': 'Rural Housing Stock Age and Maintenance',
     'description': 'Farming community housing built pre-1970; costly maintenance; limited new construction.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.housing.rural_housing'],
     'claim_ids': []},
    {'id': 'driver.southland.housing.dairy_worker_demand', 'name': 'Dairy and Processing Sector Worker Demand',
     'description': 'Rapid dairy expansion (1990s–2010s) drove worker demand; tight rental markets near farms/plants.',
     'theme': 'housing', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.housing.worker_housing'],
     'claim_ids': []},

    # Transport
    {'id': 'driver.southland.transport.invercargill_aging_roading', 'name': 'Invercargill City Roading Network Aging',
     'description': 'CBD roading infrastructure built 1970s–80s; limited maintenance funding.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.transport.invercargill_roading'],
     'claim_ids': []},
    {'id': 'driver.southland.transport.fiordland_single_route', 'name': 'Fiordland SH94 Single Route Dependency',
     'description': 'Milford Sound access via single 120km highway; no alternative routes.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.southland.transport.fiordland_access'],
     'claim_ids': []},
    {'id': 'driver.southland.transport.fiordland_closure_risk', 'name': 'Fiordland Weather-Driven Closure Risk',
     'description': 'SH94 closed regularly by snow, avalanche, slip; tourism and supply chain disrupted.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.southland.transport.fiordland_access'],
     'claim_ids': []},
    {'id': 'driver.southland.transport.car_dependency_rural', 'name': 'Car Dependency in Rural and Urban Areas',
     'description': 'Limited public transit; low population density drives car use.',
     'theme': 'transport', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.southland.transport.active_modes'],
     'claim_ids': []},

    # Infrastructure
    {'id': 'driver.southland.infrastructure.aging_water_systems', 'name': 'Aging Water and Wastewater Systems',
     'description': 'Invercargill and district water systems built 1960s–80s; renewal costs escalating.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.infrastructure.water_wastewater'],
     'claim_ids': []},
    {'id': 'driver.southland.infrastructure.smelter_energy_contract', 'name': 'NZAS-Meridian Power Contract Dependency',
     'description': 'Smelter depends on long-term Manapōuri-Meridian contract; renegotiation risk high.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.southland.infrastructure.manapouri_power'],
     'claim_ids': []},
    {'id': 'driver.southland.infrastructure.rural_digital_gap', 'name': 'Rural Broadband Gap and Cost Barriers',
     'description': 'Low density, topography limit fibre economics; rural Southland lacks reliable broadband.',
     'theme': 'infrastructure', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.infrastructure.digital_rural'],
     'claim_ids': []},

    # Environment
    {'id': 'driver.southland.environment.dairy_intensification', 'name': 'Dairy Sector Intensification',
     'description': 'Dairy conversion and herd expansion (1990s–2010s) drove nutrient loading and water pollution.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.environment.southland_river_quality'],
     'claim_ids': []},
    {'id': 'driver.southland.environment.fiordland_invasive_species', 'name': 'Fiordland Invasive Species (Stoats, Rats)',
     'description': 'DOC-managed areas losing endemic birds to invasive predators; resource constraints limiting control.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.environment.fiordland_ecosystem'],
     'claim_ids': []},
    {'id': 'driver.southland.environment.tourism_pressure_fiordland', 'name': 'Fiordland Tourism Visitor Pressure',
     'description': 'Milford Sound visitor numbers pre-COVID >500k annually; infrastructure and ecosystem strain.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.southland.environment.fiordland_ecosystem'],
     'claim_ids': []},
    {'id': 'driver.southland.environment.foveaux_overfishing', 'name': 'Foveaux Strait Overfishing and Urchin Barrens',
     'description': 'Kina overfishing reduced urchin predators; sea urchin barrens expanded; kelp forest loss.',
     'theme': 'environment', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.environment.coastal_foveaux'],
     'claim_ids': []},

    # Inequality
    {'id': 'driver.southland.inequality.invercargill_deprivation', 'name': 'Invercargill East Deprivation Index',
     'description': 'Invercargill East among NZ\'s highest deprivation; intergenerational poverty.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.inequality.invercargill_east_poverty'],
     'claim_ids': []},
    {'id': 'driver.southland.inequality.child_poverty_food_insecurity', 'name': 'Child Poverty and Food Insecurity',
     'description': 'High proportion of Southland children in poverty; food bank demand elevated.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.inequality.child_poverty'],
     'claim_ids': []},
    {'id': 'driver.southland.inequality.rural_isolation_service_distance', 'name': 'Rural Isolation and Service Distance',
     'description': 'Southland farming families far from jobs, schools, healthcare; transport costs high.',
     'theme': 'inequality', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'permanent',
     'scope': 'regional', 'problem_ids': ['problem.southland.inequality.rural_isolation'],
     'claim_ids': []},

    # Crime
    {'id': 'driver.southland.crime.family_violence_prevalence', 'name': 'Family Violence Normalization',
     'description': 'High family violence call-out rates; intergenerational trauma; reporting barriers.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.crime.family_violence'],
     'claim_ids': []},
    {'id': 'driver.southland.crime.invercargill_youth_gang', 'name': 'Invercargill Youth Gang Activity',
     'description': 'Gang presence in Invercargill recruiting disengaged youth.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.crime.youth_offending'],
     'claim_ids': []},
    {'id': 'driver.southland.crime.rural_stock_theft', 'name': 'Rural Stock Theft and Farm Burglary',
     'description': 'Farming community experiences regular stock theft, vehicle theft; limited police patrol.',
     'theme': 'crime', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.crime.rural_crime'],
     'claim_ids': []},

    # Health
    {'id': 'driver.southland.health.mental_health_service_shortfall', 'name': 'Mental Health Service Under-Resourcing',
     'description': 'Southland mental health services oversubscribed; long waitlists; rural access barriers.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.health.mental_health'],
     'claim_ids': []},
    {'id': 'driver.southland.health.chronic_disease_lifestyle', 'name': 'Lifestyle Risk Factors and Obesity',
     'description': 'Southland has higher obesity, sedentary behavior, smoking rates.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.health.chronic_disease'],
     'claim_ids': []},
    {'id': 'driver.southland.health.rural_gp_shortage', 'name': 'Rural Health Workforce Shortages',
     'description': 'Southland GPs aging; recruitment difficult; locum reliance high; specialist access limited.',
     'theme': 'health', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.health.rural_workforce'],
     'claim_ids': []},

    # Education
    {'id': 'driver.southland.education.ece_affordability_rural', 'name': 'ECE Affordability Barriers in Rural Areas',
     'description': 'Rural ECE providers limited; parent fees high; transport barriers.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.education.early_childhood'],
     'claim_ids': []},
    {'id': 'driver.southland.education.secondary_support_gap', 'name': 'Secondary School Pastoral Support System Gap',
     'description': 'Smaller rural schools lack counsellors, learning support staff; pastoral response limited.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.education.secondary'],
     'claim_ids': []},
    {'id': 'driver.southland.education.tertiary_access_barrier', 'name': 'Tertiary Education Access Barriers',
     'description': 'No university campus in Southland; students relocate; student debt burden high.',
     'theme': 'education', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.education.tertiary_access'],
     'claim_ids': []},

    # Economy
    {'id': 'driver.southland.economy.smelter_closure_risk', 'name': 'NZAS Smelter Closure Risk',
     'description': 'Smelter energy contract renegotiation; closure would devastate Southland economy.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.southland.economy.smelter_dependency'],
     'claim_ids': []},
    {'id': 'driver.southland.economy.dairy_commodity_exposure', 'name': 'Dairy Sector Commodity Price Exposure',
     'description': 'Southland dairy cash margin compressed; milk price volatile; input costs rising.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.southland.economy.agri_commodity'],
     'claim_ids': []},
    {'id': 'driver.southland.economy.brain_drain', 'name': 'Brain Drain to Larger Cities',
     'description': 'Southland youth relocate to Auckland/Dunedin for opportunity; limited entrepreneurship.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'demographic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.economy.economic_diversification'],
     'claim_ids': []},
    {'id': 'driver.southland.economy.limited_startup_capital', 'name': 'Limited Venture Capital and Startup Ecosystem',
     'description': 'Southland lacks angel investors, venture capital, tech talent.',
     'theme': 'economy', 'consensus': 'consensus', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.economy.economic_diversification'],
     'claim_ids': []},

    # Governance
    {'id': 'driver.southland.governance.smelter_energy_policy', 'name': 'Smelter Energy Policy and Grid Resilience Debates',
     'description': 'NZAS contract negotiations involve energy policy, grid resilience, emissions considerations.',
     'theme': 'governance', 'consensus': 'contested', 'category': 'institutional', 'timescale': 'short',
     'scope': 'regional', 'problem_ids': ['problem.southland.governance.smelter_energy_policy'],
     'claim_ids': []},
    {'id': 'driver.southland.governance.ngai_tahu_cogovernance', 'name': 'Ngāi Tahu Co-Governance and Consultation Requirements',
     'description': 'Treaty settlement expanding Ngāi Tahu co-governance; institutional complexity.',
     'theme': 'governance', 'consensus': 'contested', 'category': 'institutional', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.governance.treaty_ngai_tahu'],
     'claim_ids': []},
    {'id': 'driver.southland.governance.council_funding_constraint', 'name': 'Local Government Funding Constraints',
     'description': 'Southland councils face rating pressures, limited revenue growth; infrastructure backlog.',
     'theme': 'governance', 'consensus': 'consensus', 'category': 'economic', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.governance.local_govt_reform'],
     'claim_ids': []},

    # Climate
    {'id': 'driver.southland.climate.rainfall_extremes', 'name': 'Rainfall Intensity and Flood Risk Increase',
     'description': 'Climate change intensifies rainfall events; Southland river flood risk rising.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.climate.flooding_rivers'],
     'claim_ids': []},
    {'id': 'driver.southland.climate.pastoral_growing_season_shift', 'name': 'Pastoral System Growing Season and Moisture Shift',
     'description': 'Dairy and sheep pastoral systems face changing rainfall distribution, temperature; adaptation slow.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'medium',
     'scope': 'regional', 'problem_ids': ['problem.southland.climate.drought_agricultural'],
     'claim_ids': []},
    {'id': 'driver.southland.climate.sea_level_rise_foveaux', 'name': 'Sea Level Rise and Coastal Inundation Risk',
     'description': 'Foveaux Strait coastal communities (Riverton, Aparima) face 0.5–1.0m SLR by 2100.',
     'theme': 'climate', 'consensus': 'consensus', 'category': 'physical', 'timescale': 'long',
     'scope': 'regional', 'problem_ids': ['problem.southland.climate.coastal_foveaux_rise'],
     'claim_ids': []},
]

# ============================================================================
# Camps: 1–2 per problem, covering main intervention approaches
# ============================================================================

OTAGO_CAMPS = [
    # Housing
    {'id': 'camp.otago.housing.upzone_supply', 'name': 'Upzoning and Intensification',
     'theme': 'housing', 'core_claim': 'Upzoning and medium-density development reduces housing scarcity in Queenstown and Dunedin.',
     'flagship_moves': ['Upzone Queenstown CBD and arterial corridors to 6+ storeys',
                        'Permit medium-density (4-6 units) in all residential zones within 800m transit stops',
                        'Remove car-parking minimums'],
     'tensions': ['Fault-zone and liquefaction risk in Queenstown increases with density',
                  'Dunedin heritage preservation conflicts with densification'],
     'addresses': ['problem.otago.housing.housing_market', 'problem.otago.housing.queenstown_affordability'],
     'interventions': [
         {'description': 'Rezone Queenstown CBD and lakefront precincts for 8+ storey mixed-use',
          'state_variable': 'zoned_capacity', 'constraint_relaxed': 'height_limit', 'expected_sign': '+'},
         {'description': 'Permit medium-density (4-6 unit) developments in low-density residential',
          'state_variable': 'zoned_capacity', 'constraint_relaxed': 'building_form_limit', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.housing.build_to_rent', 'name': 'Build-to-Rent and Rental Housing Investment',
     'theme': 'housing', 'core_claim': 'Encouraging institutional build-to-rent (BTR) and rental housing investment improves worker housing supply.',
     'flagship_moves': ['Tax incentives for BTR operators',
                        'Fast-track resource consents for BTR projects',
                        'Develop BTR on council-owned land'],
     'tensions': ['BTR investors prioritize market-rate rents; affordable element requires subsidy',
                  'Tenant protection regulations reduce BTR investment attractiveness'],
     'addresses': ['problem.otago.housing.worker_housing'],
     'interventions': [
         {'description': 'Offer 10-year tax holiday for qualifying BTR projects',
          'state_variable': 'rental_stock', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.housing.student_accommodation', 'name': 'University-Managed Student Accommodation',
     'theme': 'housing', 'core_claim': 'Expand university-managed student housing to reduce private rental market pressure.',
     'flagship_moves': ['University capital investment in on-campus residential colleges',
                        'Co-invest with private providers for mixed-tenure models',
                        'Set rental caps at cost-recovery for university housing'],
     'tensions': ['University capital constraints limit expansion rate',
                  'Private landlords oppose market-share loss'],
     'addresses': ['problem.otago.housing.dunedin_student_rental'],
     'interventions': [
         {'description': 'Expand University of Otago accommodation by 2,000 beds over 5 years',
          'state_variable': 'student_rental_stock', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Transport
    {'id': 'camp.otago.transport.transit_expansion', 'name': 'Public Transit Expansion',
     'theme': 'transport', 'core_claim': 'Investing in frequent public transit (bus, light rail) reduces car dependency.',
     'flagship_moves': ['High-frequency bus network (15-min intervals) in Queenstown and Dunedin CBDs',
                        'Evaluate light rail feasibility for Queenstown-Arrowtown corridor',
                        'Integrate Dunedin bus network across three TAs'],
     'tensions': ['Low population density makes transit economically marginal',
                  'Upfront capital investment competes with maintenance funding'],
     'addresses': ['problem.otago.transport.connectivity', 'problem.otago.transport.active_modes'],
     'interventions': [
         {'description': 'Establish dedicated bus lanes and signal priority in Queenstown CBD',
          'state_variable': 'transit_speed', 'expected_sign': '+'},
         {'description': 'Integrate fares and scheduling across regional operators',
          'state_variable': 'transit_patronage', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.transport.active_modes', 'name': 'Active Transport (Walking, Cycling) Infrastructure',
     'theme': 'transport', 'core_claim': 'Protected cycleways and pedestrian infrastructure increase walking and cycling mode share.',
     'flagship_moves': ['Protected cycleways on all main roads in Queenstown and Dunedin',
                        'Central Otago Rail Trail expansion to urban areas',
                        'Car-free zones in Queenstown and Dunedin CBDs'],
     'tensions': ['On-street parking loss opposed by merchants',
                  'Winter weather limits utility in alpine areas'],
     'addresses': ['problem.otago.transport.active_modes'],
     'interventions': [
         {'description': 'Build 50 km of protected cycleways in Queenstown-Arrowtown',
          'state_variable': 'mode_share_cycling', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Infrastructure
    {'id': 'camp.otago.infrastructure.hospital_rebuild', 'name': 'Dunedin Hospital Rebuild and Modernization',
     'theme': 'infrastructure', 'core_claim': 'Completion of seismic and capacity upgrade improves healthcare resilience and capacity.',
     'flagship_moves': ['Complete Dunedin hospital rebuild by 2032',
                        'Ensure 21st-century facility standards (IT, disaster recovery)',
                        'Co-locate with research and teaching infrastructure'],
     'tensions': ['Construction cost escalation and timeline risk',
                  'Interim service disruptions during rebuild'],
     'addresses': ['problem.otago.infrastructure.otago_hospital_rebuild'],
     'interventions': [
         {'description': 'Secure full Crown funding commitment for hospital rebuild',
          'state_variable': 'hospital_capacity', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.infrastructure.water_resilience', 'name': 'Water Supply and Resilience for Queenstown',
     'theme': 'infrastructure', 'core_claim': 'Diversifying water sources and managing demand reduces Wakatipu basin scarcity.',
     'flagship_moves': ['Develop alternative water sources (groundwater, recycled)',
                        'Enforce water efficiency standards in new buildings',
                        'Relocate irrigation away from peak summer demand'],
     'tensions': ['Recycled and alternative water sources costly',
                  'Water user resistance to conservation measures'],
     'addresses': ['problem.otago.infrastructure.wakatipu_water'],
     'interventions': [
         {'description': 'Invest in water recycling and reclamation plants',
          'state_variable': 'water_supply_reliability', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.infrastructure.rural_broadband', 'name': 'Rural Broadband Rollout and Subsidy',
     'theme': 'infrastructure', 'core_claim': 'Government subsidies for fibre and wireless broadband enable rural digital participation.',
     'flagship_moves': ['Subsidize fibre deployment to rural Otago',
                        'Deploy 5G wireless towers in coverage gaps',
                        'Lower broadband price caps through competition'],
     'tensions': ['High subsidy costs; limited revenue recapture',
                  'Technology obsolescence risk'],
     'addresses': ['problem.otago.infrastructure.digital_rural'],
     'interventions': [
         {'description': 'Extend fibre to 95% of Central Otago population centers by 2030',
          'state_variable': 'broadband_coverage', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Environment
    {'id': 'camp.otago.environment.irrigation_management', 'name': 'Irrigation Water Allocation and Efficiency',
     'theme': 'environment', 'core_claim': 'Tightening water allocation and mandating efficiency improvements reduces environmental flow depletion.',
     'flagship_moves': ['Reduce irrigation allocation in Central Otago by 15% over 10 years',
                        'Mandate smart irrigation technology (soil moisture sensors)',
                        'Shift high-value crops to lower water requirements'],
     'tensions': ['Farmer income pressure and viability concerns',
                  'Horticulture competitiveness challenged by water costs'],
     'addresses': ['problem.otago.environment.irrigation_water_quality'],
     'interventions': [
         {'description': 'Enforce environmental flow requirements in Clutha/Mata-au system',
          'state_variable': 'environmental_flow_ratio', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.environment.pastoral_regulation', 'name': 'Pastoral Farming Regulation and Riparian Protection',
     'theme': 'environment', 'core_claim': 'Mandatory riparian fencing, feed storage regulations, and stock exclusion reduce pastoral nutrient loads.',
     'flagship_moves': ['Mandate riparian buffers (minimum 3m) on all waterways',
                        'Regulate intensive grazing near streams',
                        'Subsidize riparian planting'],
     'tensions': ['Farmer compliance cost and land-use restrictions',
                  'Enforcement challenges in remote areas'],
     'addresses': ['problem.otago.environment.lake_eutrophication'],
     'interventions': [
         {'description': 'Require riparian fencing and buffer zones by 2030',
          'state_variable': 'riparian_coverage', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.environment.lake_management', 'name': 'Lake Water Quality and Algal Bloom Prevention',
     'theme': 'environment', 'core_claim': 'Integrated lake management (nutrient load reduction, aeration, invasive control) restores ecosystem health.',
     'flagship_moves': ['Target 30% nutrient load reduction to Lakes Wanaka and Wakatipu',
                        'Install aeration and oxidation systems where needed',
                        'Control invasive fish species'],
     'tensions': ['Nutrient reduction requires upstream agricultural change',
                  'Aeration energy costs and chemical inputs'],
     'addresses': ['problem.otago.environment.lake_eutrophication'],
     'interventions': [
         {'description': 'Install aeration buoys and water quality monitoring in Lakes Wanaka, Wakatipu',
          'state_variable': 'lake_dissolved_oxygen', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Inequality
    {'id': 'camp.otago.inequality.worker_housing_support', 'name': 'Essential Worker Housing Subsidies and Bonds',
     'theme': 'inequality', 'core_claim': 'Subsidized housing allowances and rental guarantees support recruitment and retention.',
     'flagship_moves': ['Employer-sponsored housing allowance for healthcare, education workers',
                        'Community land trusts for affordable rental',
                        'Rental guarantee bonds from government'],
     'tensions': ['Ongoing subsidy cost; sustainability concerns',
                  'Equity questions: why some sectors and not others'],
     'addresses': ['problem.otago.inequality.queenstown_worker_conditions', 'problem.otago.inequality.rural_isolation'],
     'interventions': [
         {'description': 'Establish $10M/year worker housing support fund',
          'state_variable': 'worker_housing_affordability', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.inequality.dunedin_regeneration', 'name': 'East Dunedin Economic and Social Regeneration',
     'theme': 'inequality', 'core_claim': 'Targeted investment in job creation, skills, and community infrastructure revitalizes high-deprivation areas.',
     'flagship_moves': ['Business development support in East Dunedin',
                        'Youth employment pathways program',
                        'Community center and sports facility investments'],
     'tensions': ['Sustained funding requirements; uneven outcomes',
                  'Gentrification risk with housing market improvements'],
     'addresses': ['problem.otago.inequality.dunedin_deprivation'],
     'interventions': [
         {'description': 'Create 500 job placements for East Dunedin youth by 2030',
          'state_variable': 'youth_employment_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Crime
    {'id': 'camp.otago.crime.family_violence_response', 'name': 'Family Violence Prevention and Support',
     'theme': 'crime', 'core_claim': 'Integrated prevention (education, therapy), perpetrator accountability, and survivor support reduce family violence.',
     'flagship_moves': ['Expand family violence services capacity',
                        'Implement universal relationship and consent education in schools',
                        'Strengthen perpetrator accountability and rehabilitation programs'],
     'tensions': ['Cultural change requirement; resource intensity',
                  'Survivor safety prioritization requires specialized housing and support'],
     'addresses': ['problem.otago.crime.family_violence'],
     'interventions': [
         {'description': 'Increase family violence service capacity by 50%',
          'state_variable': 'fv_service_access', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.crime.youth_diversion', 'name': 'Youth Diversion and Engagement',
     'theme': 'crime', 'core_claim': 'Early intervention, mentoring, and alternative activities reduce youth offending and gang recruitment.',
     'flagship_moves': ['Youth mentoring and positive role models',
                        'Sports and arts programs for at-risk youth',
                        'Police youth liaison and restorative justice'],
     'tensions': ['Effectiveness variability across contexts',
                  'Sustained program funding and cultural change required'],
     'addresses': ['problem.otago.crime.youth_offending'],
     'interventions': [
         {'description': 'Establish youth mentoring program reaching 200 at-risk youth',
          'state_variable': 'youth_engagement_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.crime.visitor_venue_safety', 'name': 'Queenstown Visitor Venue Safety and Late-Night Governance',
     'theme': 'crime', 'core_claim': 'Venue licensing, staff training, and policing reduce visitor-related assaults and crime.',
     'flagship_moves': ['Implement late-night venues license requirements',
                        'Mandatory staff assault de-escalation training',
                        'Enhanced police patrol during peak hours'],
     'tensions': ['Venue operator compliance resistance',
                  'Cost of staff training and security'],
     'addresses': ['problem.otago.crime.queenstown_visitor_crime'],
     'interventions': [
         {'description': 'Deploy police visibility in CBD during peak hours',
          'state_variable': 'visitor_assault_rate', 'expected_sign': '-'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Health
    {'id': 'camp.otago.health.mental_health_capacity', 'name': 'Mental Health Service Expansion',
     'theme': 'health', 'core_claim': 'Increasing mental health counselors, therapists, and peer support reduces waitlists and access barriers.',
     'flagship_moves': ['Hire 100 additional mental health clinicians',
                        'Expand 24/7 crisis response services',
                        'Peer support worker program for Dunedin students'],
     'tensions': ['Healthcare worker recruitment and retention',
                  'Ongoing funding commitments'],
     'addresses': ['problem.otago.health.mental_health'],
     'interventions': [
         {'description': 'Reduce mental health service waitlist to <6 weeks',
          'state_variable': 'mh_service_access', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.health.chronic_disease_prevention', 'name': 'Chronic Disease Prevention and Lifestyle',
     'theme': 'health', 'core_claim': 'Community health promotion, food policy, and activity infrastructure prevent obesity and type 2 diabetes.',
     'flagship_moves': ['Sugar tax on soft drinks',
                        'Community gardens and farmers market expansion',
                        'Free sports programs for low-income families'],
     'tensions': ['Industry resistance to taxation',
                  'Behavioral change limitations'],
     'addresses': ['problem.otago.health.chronic_disease'],
     'interventions': [
         {'description': 'Achieve 5% reduction in obesity rates over 5 years',
          'state_variable': 'obesity_rate', 'expected_sign': '-'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.health.rural_gp_recruitment', 'name': 'Rural GP Recruitment and Retention Incentives',
     'theme': 'health', 'core_claim': 'Student loan forgiveness, housing subsidies, and clinical autonomy attract GPs to rural practices.',
     'flagship_moves': ['Rural GP loan forgiveness scheme',
                        'Housing subsidies for rural practices',
                        'Extended professional development funding'],
     'tensions': ['Ongoing subsidy costs and equity concerns',
                  'Success dependent on rural lifestyle appeal'],
     'addresses': ['problem.otago.health.rural_workforce'],
     'interventions': [
         {'description': 'Place 15 additional GPs in Central Otago rural practices',
          'state_variable': 'gp_density_rural', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Education
    {'id': 'camp.otago.education.ece_subsidy', 'name': 'Early Childhood Education Expansion and Subsidies',
     'theme': 'education', 'core_claim': 'Free or subsidized ECE increases enrollment and primary school readiness.',
     'flagship_moves': ['Subsidize ECE to $20/week parent cost',
                        'Rural mobile ECE services',
                        'Teacher qualifications and wage support'],
     'tensions': ['Ongoing subsidy cost; provider resourcing',
                  'Quality variability across providers'],
     'addresses': ['problem.otago.education.early_childhood'],
     'interventions': [
         {'description': 'Increase rural ECE enrollment to 80% by age 3',
          'state_variable': 'ece_participation_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.education.secondary_support', 'name': 'Secondary School Pastoral Support and Achievement',
     'theme': 'education', 'core_claim': 'School counselors, learning support, and attendance programs improve NCEA achievement.',
     'flagship_moves': ['Hire school counselors for all rural secondary schools',
                        'Learning support aide programs',
                        'Attendance improvement programs'],
     'tensions': ['Rural school funding constraints',
                  'Student engagement variability'],
     'addresses': ['problem.otago.education.secondary'],
     'interventions': [
         {'description': 'Increase rural NCEA Level 2+ pass rate to 80%',
          'state_variable': 'ncea_pass_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.education.tertiary_support', 'name': 'University Student Wellbeing and Support',
     'theme': 'education', 'core_claim': 'Mental health services, housing support, and financial aid reduce student stress and improve outcomes.',
     'flagship_moves': ['Expand University mental health counselors',
                        'Student hardship grants expansion',
                        'On-campus accommodation expansion'],
     'tensions': ['University budget constraints',
                  'Student support demand growth'],
     'addresses': ['problem.otago.education.tertiary_dunedin'],
     'interventions': [
         {'description': 'Achieve <6 week mental health service wait time for students',
          'state_variable': 'student_mh_access', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Economy
    {'id': 'camp.otago.economy.tourism_resilience', 'name': 'Tourism Sector Resilience and Diversification',
     'theme': 'economy', 'core_claim': 'Developing high-value, low-impact tourism and supporting alternative sectors reduces dependency.',
     'flagship_moves': ['Visitor capacity limits in Queenstown CBD and Milford Sound',
                        'Sustainable tourism certification scheme',
                        'Support for outdoor recreation and wellness tourism'],
     'tensions': ['Revenue reductions from visitor limits',
                  'International competition for tourism'],
     'addresses': ['problem.otago.economy.tourism_queenstown'],
     'interventions': [
         {'description': 'Transition 20% of tourism jobs to higher-wage roles',
          'state_variable': 'tourism_job_quality', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.economy.agricultural_innovation', 'name': 'Agricultural Sector Innovation and Adaptation',
     'theme': 'economy', 'core_claim': 'R&D support, organic and high-value crops, and climate adaptation improve viability.',
     'flagship_moves': ['AgTech innovation hub in Central Otago',
                        'Organic and specialty crop transition support',
                        'Climate-adaptive rootstock breeding'],
     'tensions': ['Transition costs for farmers; commodity preference',
                  'Long innovation development timelines'],
     'addresses': ['problem.otago.economy.agri_primary'],
     'interventions': [
         {'description': 'Establish innovation hub with 20 startup company incubators',
          'state_variable': 'agri_productivity', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.economy.university_anchor', 'name': 'University as Economic Anchor: Research Spin-Offs',
     'theme': 'economy', 'core_claim': 'Supporting university research commercialization and spin-off companies drives innovation-sector jobs.',
     'flagship_moves': ['Venture capital fund for Otago research commercialization',
                        'Incubator and co-working spaces in Dunedin',
                        'Bilateral programs with technology companies'],
     'tensions': ['Capital requirements and success uncertainty',
                  'Potential IP conflicts with university mission'],
     'addresses': ['problem.otago.economy.economic_structure'],
     'interventions': [
         {'description': 'Support 10 university research spin-offs over 5 years',
          'state_variable': 'startup_job_creation', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Governance
    {'id': 'camp.otago.governance.growth_planning', 'name': 'Integrated Growth Management and Spatial Planning',
     'theme': 'governance', 'core_claim': 'Coordinated spatial planning across three TAs aligns infrastructure and housing with growth.',
     'flagship_moves': ['Unified Otago growth management strategy',
                        'Development sequencing with infrastructure capacity',
                        'Mandatory developer contributions'],
     'tensions': ['TA autonomy and coordination challenges',
                  'Development timing uncertainty'],
     'addresses': ['problem.otago.governance.queenstown_growth_management'],
     'interventions': [
         {'description': 'Adopt integrated growth strategy by 2027',
          'state_variable': 'planning_coordination', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.governance.iwi_partnership', 'name': 'Iwi-Crown-Council Partnership Framework',
     'theme': 'governance', 'core_claim': 'Formalizing decision-making partnerships with Ngāi Tahu improves legitimacy and outcomes.',
     'flagship_moves': ['Joint governance boards for key resources (water, forests, heritage)',
                        'Co-management agreements with defined authority',
                        'Mātauranga Māori integration in planning'],
     'tensions': ['Colonial power imbalances; contentious process',
                  'Resource allocation from co-management'],
     'addresses': ['problem.otago.governance.treaty_ngai_tahu'],
     'interventions': [
         {'description': 'Establish joint decision-making framework for Clutha/Mata-au system',
          'state_variable': 'governance_legitimacy', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    # Climate
    {'id': 'camp.otago.climate.water_security', 'name': 'Water Security and Drought Adaptation',
     'theme': 'climate', 'core_claim': 'Diversified water sources, efficiency, and demand management ensure Central Otago drought resilience.',
     'flagship_moves': ['Develop groundwater and recycled water sources',
                        'Irrigation shift to drought-resistant crops',
                        'Water storage and catchment management'],
     'tensions': ['High infrastructure costs; technology uncertainty',
                  'Farmer adoption barriers'],
     'addresses': ['problem.otago.climate.drought_central_otago'],
     'interventions': [
         {'description': 'Reduce irrigation demand by 20% over 10 years',
          'state_variable': 'irrigation_efficiency', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.climate.alpine_safety', 'name': 'Alpine Hazard Management and Warning Systems',
     'theme': 'climate', 'core_claim': 'Avalanche forecasting, GLOF monitoring, and infrastructure resilience reduce alpine hazard impacts.',
     'flagship_moves': ['Avalanche forecasting and control program',
                        'GLOF monitoring for Fiordland lakes',
                        'Hazard-resilient infrastructure design for SH6'],
     'tensions': ['High operational costs; technical uncertainty',
                  'Risk tolerance and road closure decisions'],
     'addresses': ['problem.otago.climate.alpine_hazards'],
     'interventions': [
         {'description': 'Establish alpine hazard monitoring network',
          'state_variable': 'hazard_warning_lead_time', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},

    {'id': 'camp.otago.climate.coastal_resilience', 'name': 'Dunedin Coastal Adaptation and Managed Retreat',
     'theme': 'climate', 'core_claim': 'Seawalls, nature-based solutions, and managed retreat protect Dunedin from sea-level rise.',
     'flagship_moves': ['Dunedin CBD seawall and stormwater upgrade',
                        'Mangrove and salt marsh restoration',
                        'Managed retreat policy for Port Chalmers'],
     'tensions': ['High capital cost; long-term commitment required',
                  'Tension between protection and retreat approaches'],
     'addresses': ['problem.otago.climate.coastal_dunedin'],
     'interventions': [
         {'description': 'Complete Dunedin coastal protection strategy',
          'state_variable': 'coastal_resilience', 'expected_sign': '+'},
     ],
     'applicable_in': ['otago'], 'tensions_with': []},
]

# Now generate Southland camps (similar structure, adapted to Southland context)
SOUTHLAND_CAMPS = [
    # Housing
    {'id': 'camp.southland.housing.build_to_rent', 'name': 'Build-to-Rent and Worker Housing',
     'theme': 'housing', 'core_claim': 'Institutional BTR and dairy worker housing support improve rental supply and affordability.',
     'flagship_moves': ['Dairy sector housing standards for workers',
                        'Council-led BTR projects in Invercargill',
                        'Rental subsidies for agriculture and processing workers'],
     'tensions': ['BTR investor returns limited in Southland market',
                  'Worker housing costs reduce farm viability'],
     'addresses': ['problem.southland.housing.worker_housing'],
     'interventions': [
         {'description': 'Create 500 dairy worker housing units over 5 years',
          'state_variable': 'worker_housing_stock', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.housing.rural_maintenance', 'name': 'Rural Housing Maintenance and Upgrade Support',
     'theme': 'housing', 'core_claim': 'Grants and low-interest loans enable rural housing maintenance and upgrade.',
     'flagship_moves': ['Rural housing maintenance grant program',
                        'Low-interest renovation loans',
                        'Energy efficiency retrofit subsidies'],
     'tensions': ['Ongoing subsidy requirement',
                  'Targeting and fairness questions'],
     'addresses': ['problem.southland.housing.rural_housing'],
     'interventions': [
         {'description': 'Support 300 rural housing upgrades over 5 years',
          'state_variable': 'rural_housing_quality', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Transport
    {'id': 'camp.southland.transport.invercargill_roading', 'name': 'Invercargill CBD Roading Upgrade and Congestion Management',
     'theme': 'transport', 'core_claim': 'Roading network upgrade and traffic management improve CBD flow and pedestrian safety.',
     'flagship_moves': ['Upgrade key intersections with modern signals',
                        'Implement congestion pricing or parking controls',
                        'Bus priority lanes on main routes'],
     'tensions': ['Traffic diversion and merchant opposition',
                  'High upfront capital cost'],
     'addresses': ['problem.southland.transport.invercargill_roading'],
     'interventions': [
         {'description': 'Reduce CBD peak hour congestion by 15%',
          'state_variable': 'travel_time_index', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.transport.fiordland_resilience', 'name': 'Fiordland SH94 Resilience and Alternative Routes',
     'theme': 'transport', 'core_claim': 'Investing in road maintenance and feasibility of alternative routes (e.g., Te Anau–Hollyford) improves access resilience.',
     'flagship_moves': ['Accelerate SH94 maintenance and resilience improvements',
                        'Evaluate alternative Fiordland access routes',
                        'Emergency supply and visitor rerouting protocols'],
     'tensions': ['High cost of alternative routes; limited ROI',
                  'Environmental impact of new routes'],
     'addresses': ['problem.southland.transport.fiordland_access'],
     'interventions': [
         {'description': 'Reduce SH94 closure duration to <30 days/year',
          'state_variable': 'fiordland_access_uptime', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.transport.active_modes', 'name': 'Active Transport Infrastructure and Modal Shift',
     'theme': 'transport', 'core_claim': 'Cycleways, pedestrian infrastructure, and transit investment increase walking and cycling.',
     'flagship_moves': ['Protected cycleways on Invercargill arterials',
                        'Car-free streets in CBD',
                        'Bus frequency increase on main routes'],
     'tensions': ['Parking loss resistance',
                  'Climate and population density limit uptake'],
     'addresses': ['problem.southland.transport.active_modes'],
     'interventions': [
         {'description': 'Build 30 km of protected cycleways',
          'state_variable': 'mode_share_cycling', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Infrastructure
    {'id': 'camp.southland.infrastructure.water_wastewater', 'name': 'Water and Wastewater System Renewal',
     'theme': 'infrastructure', 'core_claim': 'Infrastructure renewal improves water quality, wastewater treatment, and resilience.',
     'flagship_moves': ['Replace aging water pipes; target loss reduction',
                        'Modern wastewater treatment in Invercargill',
                        'Rural septic system upgrade support'],
     'tensions': ['High renewal cost and ratepayer impact',
                  'Timing and prioritization challenges'],
     'addresses': ['problem.southland.infrastructure.water_wastewater'],
     'interventions': [
         {'description': 'Reduce water loss from 40% to 25% by 2035',
          'state_variable': 'water_loss_ratio', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.infrastructure.smelter_transition', 'name': 'Economic Transition Planning for Potential Smelter Closure',
     'theme': 'infrastructure', 'core_claim': 'Proactive diversification and business development prepare Southland for smelter exit scenario.',
     'flagship_moves': ['Diversification strategy and business incubation',
                        'Worker retraining programs',
                        'Alternative uses for smelter site'],
     'tensions': ['Difficult political messaging; community resistance',
                  'Economic transition time and costs'],
     'addresses': ['problem.southland.infrastructure.manapouri_power'],
     'interventions': [
         {'description': 'Develop transition plan and create 500 alternative jobs',
          'state_variable': 'economic_diversification', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.infrastructure.rural_broadband', 'name': 'Rural Broadband Expansion via Subsidy and 5G',
     'theme': 'infrastructure', 'core_claim': 'Subsidized fibre and 5G deployment enable agritech adoption and rural business growth.',
     'flagship_moves': ['Extend fibre to rural towns',
                        'Deploy 5G towers in underserved areas',
                        'Subsidize rural broadband access'],
     'tensions': ['Subsidy costs; limited business case',
                  'Technology obsolescence risk'],
     'addresses': ['problem.southland.infrastructure.digital_rural'],
     'interventions': [
         {'description': 'Achieve 95% rural broadband coverage by 2030',
          'state_variable': 'broadband_coverage', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Environment
    {'id': 'camp.southland.environment.dairy_regulation', 'name': 'Dairy Industry Nutrient Reduction Regulation',
     'theme': 'environment', 'core_claim': 'Nutrient application caps, riparian fencing, and stock exclusion reduce river pollution.',
     'flagship_moves': ['Nitrogen application caps on dairy farms',
                        'Mandatory riparian buffers (5m minimum)',
                        'Stock exclusion from waterways by 2027'],
     'tensions': ['Farmer opposition and compliance cost',
                  'Revenue and production reductions'],
     'addresses': ['problem.southland.environment.southland_river_quality'],
     'interventions': [
         {'description': 'Reduce Mataura and Oreti river nitrogen by 40%',
          'state_variable': 'river_nitrogen_concentration', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.environment.fiordland_conservation', 'name': 'Fiordland Ecosystem Protection and Invasive Control',
     'theme': 'environment', 'core_claim': 'Scaling DOC predator control and tourism management protects endemic species.',
     'flagship_moves': ['Expand predator control in Fiordland',
                        'Visitor capacity limits in sensitive areas',
                        'Invasive species biosecurity'],
     'tensions': ['High DOC operational cost',
                  'Visitor management politically difficult'],
     'addresses': ['problem.southland.environment.fiordland_ecosystem'],
     'interventions': [
         {'description': 'Restore 3 endangered species populations',
          'state_variable': 'endemic_species_abundance', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.environment.foveaux_fisheries', 'name': 'Foveaux Strait Fisheries Management and Ecosystem Restoration',
     'theme': 'environment', 'core_claim': 'Strict catch limits, marine protected areas, and invasive control restore kelp forests and fisheries.',
     'flagship_moves': ['Expand marine protected areas in Foveaux',
                        'Reduce catch limits to sustainable levels',
                        'Sea urchin culling to restore kelp'],
     'tensions': ['Fishery income reduction; community resistance',
                  'International coordination (with Australia)'],
     'addresses': ['problem.southland.environment.coastal_foveaux'],
     'interventions': [
         {'description': 'Restore 50% of lost kelp forest area',
          'state_variable': 'kelp_forest_area', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Inequality
    {'id': 'camp.southland.inequality.invercargill_regeneration', 'name': 'Invercargill East Deprivation Reduction Program',
     'theme': 'inequality', 'core_claim': 'Targeted job creation, skills, community facilities, and housing support revitalize high-deprivation areas.',
     'flagship_moves': ['Business development support and mentoring',
                        'Youth employment and training pathways',
                        'Community center and sports facility investment'],
     'tensions': ['Sustained funding required; uneven outcomes',
                  'Gentrification and displacement risk'],
     'addresses': ['problem.southland.inequality.invercargill_east_poverty'],
     'interventions': [
         {'description': 'Create 300 job placements for young people',
          'state_variable': 'youth_employment_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.inequality.child_poverty', 'name': 'Child Poverty and Food Security Support',
     'theme': 'inequality', 'core_claim': 'Free school meals, benefit increases, and social support reduce child poverty.',
     'flagship_moves': ['Free school meals for all children',
                        'Benefit adequacy increase',
                        'Community food programs and gardens'],
     'tensions': ['Fiscal cost; political opposition',
                  'Benefit dependency concerns'],
     'addresses': ['problem.southland.inequality.child_poverty'],
     'interventions': [
         {'description': 'Reduce child food insecurity by 60%',
          'state_variable': 'child_food_security', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.inequality.rural_service_access', 'name': 'Rural Service Access and Isolation Reduction',
     'theme': 'inequality', 'core_claim': 'Mobile services, transport subsidies, and broadband reduce rural isolation.',
     'flagship_moves': ['Mobile health and education services',
                        'Public transport subsidy for rural residents',
                        'Broadband access for rural areas'],
     'tensions': ['Cost per capita high in low-density areas',
                  'Sustainability of mobile services'],
     'addresses': ['problem.southland.inequality.rural_isolation'],
     'interventions': [
         {'description': 'Establish mobile clinics serving rural areas weekly',
          'state_variable': 'healthcare_access_rural', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Crime
    {'id': 'camp.southland.crime.family_violence', 'name': 'Family Violence Prevention and Response',
     'theme': 'crime', 'core_claim': 'Expanded services, education, and perpetrator accountability reduce family violence.',
     'flagship_moves': ['Family violence service capacity increase',
                        'School-based relationship education',
                        'Perpetrator accountability programs'],
     'tensions': ['Resource intensity; cultural change required',
                  'Survivor safety and housing needs'],
     'addresses': ['problem.southland.crime.family_violence'],
     'interventions': [
         {'description': 'Increase FV service capacity by 50%',
          'state_variable': 'fv_service_access', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.crime.youth_engagement', 'name': 'Youth Mentoring and Engagement Programs',
     'theme': 'crime', 'core_claim': 'Mentoring, sports, arts, and positive role models reduce youth offending and gang recruitment.',
     'flagship_moves': ['Youth mentoring program expansion',
                        'Sports and arts programs',
                        'Restorative justice and police youth liaison'],
     'tensions': ['Program effectiveness variability',
                  'Sustained funding and cultural change'],
     'addresses': ['problem.southland.crime.youth_offending'],
     'interventions': [
         {'description': 'Mentor 150 at-risk youth',
          'state_variable': 'youth_engagement_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.crime.rural_policing', 'name': 'Rural Policing and Farm Security Support',
     'theme': 'crime', 'core_claim': 'Enhanced police presence and farm security support reduce rural crime.',
     'flagship_moves': ['Rural police patrol frequency increase',
                        'Farm security subsidy program',
                        'Farm-to-police reporting network'],
     'tensions': ['Police resource constraints',
                  'Cost-benefit of rural policing investment'],
     'addresses': ['problem.southland.crime.rural_crime'],
     'interventions': [
         {'description': 'Reduce rural crime rate by 20%',
          'state_variable': 'rural_crime_rate', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Health
    {'id': 'camp.southland.health.mental_health', 'name': 'Mental Health Service Expansion',
     'theme': 'health', 'core_claim': 'Expanded counselors, therapists, and crisis services reduce mental health burden.',
     'flagship_moves': ['Hire 50 additional mental health clinicians',
                        '24/7 mental health crisis service',
                        'Peer support worker program'],
     'tensions': ['Healthcare worker recruitment difficulty',
                  'Ongoing funding commitment'],
     'addresses': ['problem.southland.health.mental_health'],
     'interventions': [
         {'description': 'Reduce mental health service waitlist to <6 weeks',
          'state_variable': 'mh_service_access', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.health.chronic_disease', 'name': 'Chronic Disease Prevention and Management',
     'theme': 'health', 'core_claim': 'Health promotion, obesity reduction, and diabetes management improve population health.',
     'flagship_moves': ['Community health promotion program',
                        'Free diabetes screening and management',
                        'Active lifestyle and food programs'],
     'tensions': ['Behavioral change limitations',
                  'Industry opposition (food/beverage)'],
     'addresses': ['problem.southland.health.chronic_disease'],
     'interventions': [
         {'description': 'Reduce obesity rate by 5% over 5 years',
          'state_variable': 'obesity_rate', 'expected_sign': '-'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.health.rural_health_workforce', 'name': 'Rural Health Workforce Recruitment and Retention',
     'theme': 'health', 'core_claim': 'Student loan forgiveness, housing subsidies, and professional development attract health workers.',
     'flagship_moves': ['Rural health worker loan forgiveness',
                        'Housing subsidy for rural practices',
                        'Extended professional development support'],
     'tensions': ['Ongoing subsidy cost',
                  'Rural lifestyle appeal limitations'],
     'addresses': ['problem.southland.health.rural_workforce'],
     'interventions': [
         {'description': 'Place 10 additional GPs in rural Southland',
          'state_variable': 'gp_density_rural', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Education
    {'id': 'camp.southland.education.ece_access', 'name': 'Early Childhood Education Expansion',
     'theme': 'education', 'core_claim': 'ECE subsidies and rural mobile services increase enrollment and school readiness.',
     'flagship_moves': ['Subsidize ECE to $20/week parent cost',
                        'Mobile ECE services to rural areas',
                        'Teacher qualification and wage support'],
     'tensions': ['Ongoing subsidy cost; provider resourcing',
                  'Quality variability'],
     'addresses': ['problem.southland.education.early_childhood'],
     'interventions': [
         {'description': 'Increase rural ECE enrollment to 85%',
          'state_variable': 'ece_participation_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.education.secondary_achievement', 'name': 'Secondary School Support and NCEA Achievement',
     'theme': 'education', 'core_claim': 'School counselors, learning support, and attendance programs improve achievement.',
     'flagship_moves': ['School counselor hiring for all secondary schools',
                        'Learning support aide programs',
                        'Attendance improvement incentives'],
     'tensions': ['Rural school funding constraints',
                  'Student engagement variability'],
     'addresses': ['problem.southland.education.secondary'],
     'interventions': [
         {'description': 'Increase NCEA Level 2+ pass rate to 78%',
          'state_variable': 'ncea_pass_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.education.tertiary_pathway', 'name': 'Tertiary Education Access and Pathways',
     'theme': 'education', 'core_claim': 'Regional polytechnic expansion and student support improve tertiary access.',
     'flagship_moves': ['Southern Institute of Technology program expansion',
                        'Distance and online tertiary options',
                        'Student hardship grants and living costs support'],
     'tensions': ['ITI funding constraints',
                  'Brain drain to larger cities'],
     'addresses': ['problem.southland.education.tertiary_access'],
     'interventions': [
         {'description': 'Enroll 500 more students in regional tertiary per year',
          'state_variable': 'tertiary_participation_rate', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Economy
    {'id': 'camp.southland.economy.smelter_diversification', 'name': 'Smelter Transition and Economic Diversification',
     'theme': 'economy', 'core_claim': 'Proactive economic diversification and job creation reduce smelter dependency.',
     'flagship_moves': ['Diversification strategy and business incubation',
                        'Worker retraining and transition support',
                        'Attract technology and service businesses'],
     'tensions': ['Difficult messaging; community resistance',
                  'Business attraction challenging in Southland'],
     'addresses': ['problem.southland.economy.smelter_dependency'],
     'interventions': [
         {'description': 'Create 500 alternative jobs over 10 years',
          'state_variable': 'economic_diversification', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.economy.dairy_sustainability', 'name': 'Dairy Sector Sustainability and Margins',
     'theme': 'economy', 'core_claim': 'Supporting organic transition, feed efficiency, and reduced input costs improve dairy viability.',
     'flagship_moves': ['Organic transition subsidies',
                        'Feed efficiency R&D support',
                        'Cooperative model expansion'],
     'tensions': ['Commodity price dependency remains',
                  'Farmer adoption barriers'],
     'addresses': ['problem.southland.economy.agri_commodity'],
     'interventions': [
         {'description': 'Support 50 farms to transition to organic',
          'state_variable': 'organic_dairy_adoption', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.economy.fiordland_tourism', 'name': 'Fiordland Tourism Sustainability and Quality',
     'theme': 'economy', 'core_claim': 'Sustainable tourism certification and high-value visitor management improve economic resilience.',
     'flagship_moves': ['Visitor capacity limits in sensitive areas',
                        'Sustainable tourism certification',
                        'Support for high-value, low-impact tourism'],
     'tensions': ['Visitor number reductions; local resistance',
                  'Competition from other attractions'],
     'addresses': ['problem.southland.economy.economic_diversification'],
     'interventions': [
         {'description': 'Transition to high-value visitor model',
          'state_variable': 'tourism_revenue_per_visitor', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Governance
    {'id': 'camp.southland.governance.smelter_policy', 'name': 'Smelter Energy Policy and National Grid Resilience',
     'theme': 'governance', 'core_claim': 'Transparent smelter-grid policy negotiation balances local economy and national energy priorities.',
     'flagship_moves': ['Cross-party smelter policy agreement',
                        'Transparent energy contract negotiations',
                        'Transition support if closure occurs'],
     'tensions': ['Politically contentious; local vs national tension',
                  'Economic uncertainty'],
     'addresses': ['problem.southland.governance.smelter_energy_policy'],
     'interventions': [
         {'description': 'Achieve cross-party smelter policy agreement',
          'state_variable': 'governance_stability', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.governance.iwi_partnership', 'name': 'Ngāi Tahu Partnership and Co-Governance',
     'theme': 'governance', 'core_claim': 'Formalizing Ngāi Tahu partnerships in resource and economic decisions improves legitimacy.',
     'flagship_moves': ['Joint governance boards for key resources',
                        'Co-management agreements',
                        'Mātauranga Māori integration'],
     'tensions': ['Colonial power imbalances; contentious process',
                  'Resource allocation from partnerships'],
     'addresses': ['problem.southland.governance.treaty_ngai_tahu'],
     'interventions': [
         {'description': 'Establish joint decision-making framework',
          'state_variable': 'governance_legitimacy', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    # Climate
    {'id': 'camp.southland.climate.flood_resilience', 'name': 'Flood Risk Management and Resilience',
     'theme': 'climate', 'core_claim': 'Improved drainage, floodplain management, and building standards reduce flood impacts.',
     'flagship_moves': ['Mataura and Oreti river drainage upgrade',
                        'Floodplain zoning and land-use restrictions',
                        'Building code updates for flood resilience'],
     'tensions': ['High capital cost; agricultural land-use conflicts',
                  'Insurance and property value concerns'],
     'addresses': ['problem.southland.climate.flooding_rivers'],
     'interventions': [
         {'description': 'Reduce 1-in-100-year flood damage by 40%',
          'state_variable': 'flood_resilience', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.climate.pastoral_adaptation', 'name': 'Pastoral System Climate Adaptation',
     'theme': 'climate', 'core_claim': 'Supporting breed selection, feed diversification, and seasonal management reduces climate vulnerability.',
     'flagship_moves': ['Climate-adaptive feed crop varieties',
                        'Breed selection for climate resilience',
                        'Seasonal feed storage support'],
     'tensions': ['Farmer adoption barriers; cost pressure',
                  'Long breeding cycles'],
     'addresses': ['problem.southland.climate.drought_agricultural'],
     'interventions': [
         {'description': 'Support 100 farms to adopt climate-resilient practices',
          'state_variable': 'pastoral_climate_adaptation', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},

    {'id': 'camp.southland.climate.coastal_adaptation', 'name': 'Coastal Adaptation and Managed Retreat',
     'theme': 'climate', 'core_claim': 'Managed retreat, nature-based protection, and building standards address sea-level rise.',
     'flagship_moves': ['Coastal managed retreat policy',
                        'Salt marsh and mangrove restoration',
                        'Building code updates for coastal resilience'],
     'tensions': ['Property value and insurance concerns',
                  'Difficult political messaging'],
     'addresses': ['problem.southland.climate.coastal_foveaux_rise'],
     'interventions': [
         {'description': 'Complete Southland coastal adaptation strategy',
          'state_variable': 'coastal_resilience', 'expected_sign': '+'},
     ],
     'applicable_in': ['southland'], 'tensions_with': []},
]

# ============================================================================
# Generate Claims: 1–2 per problem (simple measurement claims)
# ============================================================================

def gen_claims_for_problems(region_infix, region_slug, problems, num_claims_per_problem=2):
    """
    Generate simple measurement claims for each problem.
    Each claim references 1–2 sources and 1 methodology.
    """
    claims = []

    for problem_id, problem_yaml in problems:
        theme = problem_yaml['theme']
        # Simplest claims: statement about existence, scale, or measurement
        problem_desc = problem_yaml['id'].split('.')[-1]

        # Claim 1: Scale/prevalence
        claim_1_id = f'claim.{region_infix}.{theme}.{problem_desc}_prevalence'
        claim_1 = {
            'id': claim_1_id,
            'statement': f'{problem_yaml["title"]} is significant in {region_slug}.',
            'value': None,
            'unit': None,
            'time_period': '2024',
            'confidence': 'medium',
            'verification_status': 'unverified',
            'last_verified': None,
            'source_ids': [],
            'scoped_to': [region_slug],
            'national_assertion': False,
            'region_mentions': [region_slug],
            'methodology_tag': None,
            'notes': 'Placeholder claim stating problem prevalence.',
        }
        claims.append((claim_1_id, claim_1))

        # Claim 2: Trend or secondary detail
        if num_claims_per_problem >= 2:
            claim_2_id = f'claim.{region_infix}.{theme}.{problem_desc}_trend'
            claim_2 = {
                'id': claim_2_id,
                'statement': f'{problem_yaml["title"]} is expected to worsen without intervention.',
                'value': None,
                'unit': None,
                'time_period': '2024-2030',
                'confidence': 'medium',
                'verification_status': 'unverified',
                'last_verified': None,
                'source_ids': [],
                'scoped_to': [region_slug],
                'national_assertion': False,
                'region_mentions': [region_slug],
                'methodology_tag': None,
                'notes': 'Placeholder claim stating trend or future projection.',
            }
            claims.append((claim_2_id, claim_2))

    return claims

# ============================================================================
# Write all drivers, camps, claims
# ============================================================================

def write_region_entities_complete(region_slug, region_infix, drivers, camps, problems):
    """Write all remaining entities (drivers, camps, claims)."""
    base_path = Path('/sessions/blissful-festive-clarke/mnt/Current website') / f'content/{region_slug}/data'

    # Write drivers
    for driver_dict in drivers:
        driver_id = driver_dict['id'].split('.')[-1]
        write_yaml_file(base_path / 'driver', f'{driver_id}.yaml', driver_dict)

    # Write camps
    for camp_dict in camps:
        camp_id = camp_dict['id'].split('.')[-1]
        write_yaml_file(base_path / 'camp', f'{camp_id}.yaml', camp_dict)

    # Write claims
    claims = gen_claims_for_problems(region_infix, region_slug, problems, num_claims_per_problem=2)
    for claim_id, claim_dict in claims:
        claim_filename = claim_id.split('.')[-1] + '.yaml'
        write_yaml_file(base_path / 'claim', claim_filename, claim_dict)

    print(f"✓ {region_slug}: {len(drivers)} drivers, {len(camps)} camps, {len(claims)} claims written")

# ============================================================================
# Execute
# ============================================================================

if __name__ == '__main__':
    # Load problems from already-written files to pass to claim generation
    otago_problems = []
    southland_problems = []

    otago_path = Path('/sessions/blissful-festive-clarke/mnt/Current website/content/otago/data/problem')
    for problem_file in sorted(otago_path.glob('*.yaml')):
        with open(problem_file, 'r') as f:
            problem_dict = yaml.safe_load(f)
        otago_problems.append((problem_dict['id'], problem_dict))

    southland_path = Path('/sessions/blissful-festive-clarke/mnt/Current website/content/southland/data/problem')
    for problem_file in sorted(southland_path.glob('*.yaml')):
        with open(problem_file, 'r') as f:
            problem_dict = yaml.safe_load(f)
        southland_problems.append((problem_dict['id'], problem_dict))

    write_region_entities_complete('otago', 'otago', OTAGO_DRIVERS, OTAGO_CAMPS, otago_problems)
    write_region_entities_complete('southland', 'southland', SOUTHLAND_DRIVERS, SOUTHLAND_CAMPS, southland_problems)
    print("\n✓ All driver, camp, claim files written")
