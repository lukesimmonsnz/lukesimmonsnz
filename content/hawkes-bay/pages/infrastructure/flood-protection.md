---
title: "Flood protection and drainage infrastructure"
section: infrastructure
subpage: flood-protection
order: 2
updated: 2026-04-26
summary: >
  Napier and Hastings urban areas are in low-lying zones prone to river and coastal flooding. Stopbanks and stormwater systems are aging and undersized for climate-intensified rainfall. Hawke's Bay Regional Council is under-resourced for upgrades.
status: draft
generated_from: problem.hawkes_bay.infrastructure.flood_protection
---

# Flood protection and drainage infrastructure

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Flooding Extent

Cyclone Gabrielle caused historic flooding in Hastings, Napier, and rural river valleys. Approximately 2,500 homes experienced inundation.


## Aging Infrastructure

Napier and Hastings flood protection systems were designed for 1-in-50-year events; climate change means such events are now occurring at 1-in-20 frequency.


---


## Drivers

The following structural drivers contribute to this problem.


### Aging pipe and infrastructure asset profiles



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Accelerated infrastructure renewal programme

Accelerated infrastructure renewal programme is the primary strategy.

**Flagship moves:**

- Implement Accelerated infrastructure renewal programme across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Accelerated infrastructure renewal programme intervention (state variable: `accelerated_renewal_index`, sign: +) (relaxes: `accelerated_renewal_constraint`)


### Flood resilience and protection infrastructure

Investing in upgraded stopbanks, stormwater systems, and natural flood defences reduces inundation risk from climate-intensified rainfall and sea-level rise.

**Flagship moves:**

- Upgrade Napier and Hastings stopbanks to 1-in-100-year standard within 10 years
- Invest in stormwater storage and retention ponds across urban areas
- Establish wetland and riparian buffers for flood attenuation

**Tensions:**

- Infrastructure upgrades require $2+ billion investment over 10 years
- Protection infrastructure may increase settlement in flood-prone areas (moral hazard)
- Natural solutions (wetlands, riparian) require land acquisition at high cost

**Interventions on the system:**

- Upgrade Napier and Hastings stopbanks to 1-in-100-year rainfall standard (state variable: `flood_protection_standard_exceedance_days`, sign: -)
- Build stormwater retention ponds and wetland buffers in urban flood-prone zones (state variable: `flood_attenuation_capacity_litres`, sign: +)


---

## Claims cited on this page

- **Infrastructure in Hawkes Bay faces aging assets, deferred maintenance, and resilience gaps. Funding constraints limit system upgrades for climate adaptation, population growth, and earthquake/flood preparedness; coordination challenges delay critical projects.** [value: 2500 dwellings; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* stopbank_standard_exceedance_days, flood_prone_dwelling_count.

*Constraints:* riparian_land_acquisition_cost, engineering_standard_cycles.

*Inputs:* rainfall_intensification_trend, river_stage_increase.


*Feedback loops:*

- `Floods damage property; repairs deplete budgets; deferred maintenance increases future flood risk.`


---

*Generated from `problem.hawkes_bay.infrastructure.flood_protection` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
