---
title: "Geographic concentration of deprivation in Wellington"
section: inequality
subpage: geographic-deprivation
order: 1
updated: 2026-04-26
summary: >
  Wellington region has extreme geographic concentration of deprivation: Porirua, parts of Hutt Valley (Naenae, Wainuiomata), and some Kāpiti communities have high NZDep scores, while the eastern Wellington suburbs and Te Aro are affluent. This spatial concentration entrenches disadvantage across generations and creates significant disparities in public service quality.
status: draft
generated_from: problem.wellington.inequality.geographic_deprivation
---

# Geographic concentration of deprivation in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Porirua and Hutt Valley deprivation concentrations

Porirua and parts of Lower Hutt contain the highest concentrations of NZDep decile 9–10 meshblocks in the Wellington region, reflecting persistent multi-generational disadvantage in communities with high Māori and Pacific populations (claim.wellington.inequality.porirua_nzdep_score).


## Geographic persistence

Deprivation in Wellington is not randomly distributed — it is heavily concentrated in specific geographic corridors that share limited access to high-wage employment, lower-quality schooling, and reduced public services (claim.wellington.inequality.deprivation_geographic_concentration).


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic concentration of social housing



- **Category:** institutional
- **Timescale:** long
- **Consensus:** mostly-agreed

### Limited transport access to high-wage employment



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Place-Based Investment in Porirua and Hutt Valley

Concentrating social investment in high-deprivation communities through integrated wraparound services is more effective than generic transfers.

**Flagship moves:**

- Establish place-based investment hubs in Cannons Creek, Naenae, and Wainuiomata
- Co-locate housing, health, education, and employment services
- Iwi-led commissioning of social services in high-Māori-population areas

**Tensions:**

- Place-based models risk stigmatising communities through geographic targeting
- Effectiveness evidence is mixed; sustained political commitment is difficult

**Interventions on the system:**

- Establish 3 place-based investment hubs in Cannons Creek, Naenae, and Wainuiomata with 5-year Crown funding commitment (state variable: `service_access_deprived_areas`, sign: +) (relaxes: `geographic_service_gap`)


---

## Claims cited on this page

- **Porirua City contains the highest concentration of NZDep2018 decile 9–10 meshblocks in the Wellington region, with Cannons Creek, Titahi Bay, and parts of Porirua East recording persistent multi-generational deprivation scores above the 90th percentile.** — New Zealand Deprivation Index 2018 (NZDep2018).
- **Deprivation in Wellington is not randomly distributed: high-deprivation meshblocks are concentrated in Porirua City and specific Hutt Valley sub-areas, with these communities sharing limited access to high-wage employment, lower school performance, and reduced public service quality relative to affluent Wellington suburbs.** — New Zealand Deprivation Index 2018 (NZDep2018); Census 2023: Wellington Regional Profile.

---

## Further reading


- **New Zealand Deprivation Index 2018 (NZDep2018)** — Atkinson J, Salmond C, Crampton P (University of Otago / Ministry of Health), 2019 — <https://www.otago.ac.nz/wellington/departments/publichealth/research/hirp/otago020194.html>

- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* nzdep_decile_concentration, median_income_by_suburb.

*Constraints:* transport_access_to_employment, school_quality_sorting.

*Inputs:* social_housing_allocation, labour_market_access.


*Feedback loops:*

- `Neighbourhood sorting: high-deprivation areas attract lower-income households through affordable rents; concentrated poverty reduces local service quality and reduces upward mobility.`


---

*Generated from `problem.wellington.inequality.geographic_deprivation` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
