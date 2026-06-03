---
title: "Cyclone-damaged housing stock"
section: housing
subpage: cyclone-damaged-stock
order: 2
updated: 2026-04-26
summary: >
  Cyclone Gabrielle (Feb 2023) caused widespread structural damage and loss of homes. Repair and rebuild processes are slow and costly, with many households displaced. Insurance gaps and cost barriers delay recovery.
status: draft
generated_from: problem.hawkes_bay.housing.cyclone_damaged_stock
---

# Cyclone-damaged housing stock

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Scale of Damage

Approximately 3,600 homes in Hawke's Bay sustained major damage or destruction from Cyclone Gabrielle. Many remain uninhabitable as of April 2026, more than 3 years later.


## Repair Backlog

Shortage of builders and construction materials has created a multi-year repair backlog. Many owners cannot afford out-of-pocket repair costs despite insurance settlements.


---


## Drivers

The following structural drivers contribute to this problem.


### Post-Cyclone Gabrielle housing scarcity and repair backlog



- **Category:** physical
- **Timescale:** medium
- **Consensus:** consensus

### Restrictive residential zoning and development constraints



- **Category:** regulatory
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Seismic retrofit mandate for vulnerable housing stock

Systematic seismic strengthening of earthquake-prone buildings and vulnerable housing stock reduces risk and supports post-cyclone resilience.

**Flagship moves:**

- Mandate seismic strengthening of all territorial authority-owned buildings within 10 years
- Offer ratepayer-funded seismic retrofit grants for private residential properties in high-risk zones
- Integrate seismic strengthening into rebuild support post-Cyclone Gabrielle

**Tensions:**

- High upfront retrofit costs create affordability barriers for low-income homeowners
- Retrofit requirements may trigger property sales if owners cannot afford costs

**Interventions on the system:**

- Identify and retrofit earthquake-prone residential buildings in Napier and Hastings (state variable: `seismic_stock_vulnerability_index`, sign: -)
- Establish ratepayer-funded retrofit grant scheme for owner-occupiers (state variable: `retrofit_completion_rate`, sign: +)


### Upzoning and intensification

Removing zoning restrictions and enabling medium-density development across Napier and Hastings urban areas is the primary lever to improve housing affordability.

**Flagship moves:**

- Implement NPS-UD density requirements across all territorial authorities
- Permit 6-storey residential buildings within 800m of Napier CBD and Hastings CBD
- Remove minimum car-parking requirements in city centres

**Tensions:**

- Intensification in flood-prone and post-cyclone-damaged land raises safety risks
- Infrastructure capacity (water, wastewater) is strained in rebuilt areas
- Heritage character areas create political resistance to blanket upzoning

**Interventions on the system:**

- Amend district plans to allow 3-6 storey residential development in urban zones (state variable: `residential_density_allowance`, sign: +)
- Fast-track resource consent for developments meeting design standards (state variable: `housing_consent_processing_time`, sign: -)


---

## Claims cited on this page

- **Cyclone Gabrielle damaged stock remains estimated at 3,600 dwellings; 12 months post-event (Feb 2024) approximately 40% were still in repair or temporary accommodation. Rental market tightness intensified post-Cyclone as insurers moved repairs out-of-scope and landlords deferred reinstatement. Repair cost inflation (labour, materials) and supply chain constraints extended timelines, deepening housing crisis for displaced low-income households.** [value: 3600 dwellings; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* damaged_dwellings_count, repair_completion_rate.

*Constraints:* material_supply_delays, skilled_labour_shortage.

*Inputs:* insurance_coverage_gaps, builder_capacity_constraint.


*Feedback loops:*

- `Prolonged displacement reduces spending in local economy; business closures lower wages; capacity to fund repairs diminishes.`


---

*Generated from `problem.hawkes_bay.housing.cyclone_damaged_stock` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
