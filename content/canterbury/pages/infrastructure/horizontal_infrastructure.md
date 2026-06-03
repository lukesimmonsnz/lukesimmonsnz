---
title: "Horizontal Infrastructure Servicing Strain"
section: infrastructure
subpage: horizontal_infrastructure
order: 1
updated: 2026-04-26
summary: >
  Water supply, wastewater, and stormwater networks across Christchurch and growth districts are strained by urban densification and greenfield expansion. Water losses in aging pipelines exceed 25%; wastewater capacity in Christchurch CBD is near saturation; stormwater systems fail in heavy rainfall events (>50mm/24hr).

status: draft
generated_from: problem.canterbury.infrastructure.horizontal_infrastructure
---

# Horizontal Infrastructure Servicing Strain

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Aging and expanding networks collide

Christchurch's water and wastewater networks contain significant pre-1970s assets (~35% of pipes). Replacement rates lag deterioration; water loss in some suburbs reaches 30%. Simultaneous growth in Waimakariri/Selwyn requires new trunk infrastructure, straining budgets.


---


## Drivers

The following structural drivers contribute to this problem.


### Aging Water & Wastewater Asset Stock



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Growth-Driven Three Waters Demand



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Three Waters Infrastructure Co-Investment & Reform

Combining central government co-funding with council capex and development contributions creates sustainable three-waters replacement cycle.

**Flagship moves:**

- Key intervention for Three Waters Infrastructure Co-Investment & Reform

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Combining central government co-funding with council capex and development contributions creates sustainable three-waters replacement cycle. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Three Waters Public-Private Partnership (PPP) Models

PPP structures for water treatment, asset delivery, and operation can attract private capital and improve efficiency while retaining public ownership.

**Flagship moves:**

- Key intervention for Three Waters Public-Private Partnership (PPP) Models

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- PPP structures for water treatment, asset delivery, and operation can attract private capital and improve efficiency while retaining public ownership. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Christchurch's water supply distribution network loses approximately 25% of treated water to leaks, pipe breaks, and theft. This loss rate is above the national urban average (23%) and reflects aging water mains (many 50+ years old installed post-1960s rapid suburban expansion). Network age, corrosive soils in some zones, and deferred maintenance from earthquake rebuild prioritization are primary drivers. Council's pipe replacement programme targets a reduction to 18% by 2035, requiring NZD 1.2 billion capital investment.** [value: 25 percent water loss; 2023] *(confidence: medium)* — State of the Environment Report—Freshwater and Land 2023.
- **Christchurch's main wastewater treatment plants (Bromley, Kingsford Terrace, Pūrāngī) operate at 85% capacity utilization, with peak wet-weather flows occasionally exceeding design. Projected growth in Selwyn and Waimakariri districts (fastest-growing regions in NZ, +3–4% annually) will exceed current capacity by 2035 without investment. Overflows to the Avon-Heathcote estuary remain a compliance risk in extreme rainfall events; stormwater separation in key drainage zones is an emerging priority.** [value: 85 percent utilization; 2024] *(confidence: medium)* — Christchurch City Council Annual Plan 2024-2025.

---

## Further reading


- **State of the Environment Report—Freshwater and Land 2023** (Environment Canterbury), 2023 — <https://www.ecan.govt.nz/about-us/planning/state-of-the-environment/>

- **Christchurch City Council Annual Plan 2024-2025** (Christchurch City Council), 2024 — <https://www.ccc.govt.nz/the-council/planning-strategy-and-policy/annual-plan/>


---

## Technical notes

*State variables:* water_main_asset_condition_index, water_loss_percentage, wastewater_treatment_capacity_utilization, stormwater_flooding_event_frequency.

*Constraints:* three_waters_infrastructure_debt, climate_change_rainfall_intensification.

*Inputs:* population_growth, urban_intensification_rate, rainfall_intensity, asset_renewal_investment.


*Feedback loops:*

- `Dynamic feedback mechanisms drive horizontal infrastructure servicing strain.`


---

*Generated from `problem.canterbury.infrastructure.horizontal_infrastructure` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
