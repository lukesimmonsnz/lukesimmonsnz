---
title: "Regional greenhouse gas emissions and reduction"
section: climate
subpage: climate_emissions
order: 1
updated: 2026-04-26
summary: >
  Taranaki emissions are driven by oil/gas production, methanol synthesis, and agricultural emissions. Emissions are 2.5x national per-capita average.
status: draft
generated_from: problem.taranaki.climate.climate_emissions
---

# Regional greenhouse gas emissions and reduction

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Regional greenhouse gas emissions and reduction in Taranaki

Taranaki emissions are driven by oil/gas production, methanol synthesis, and agricultural emissions. Emissions are 2.5x national per-capita average.


---


## Drivers

The following structural drivers contribute to this problem.


### Industrial emissions and energy transition pressures



- **Category:** economic
- **Timescale:** medium
- **Consensus:** contested


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Just transition planning

Proactive just transition planning that supports workers and communities dependent on fossil fuels is the most equitable path to decarbonisation.

**Flagship moves:**

- Establish a Taranaki Just Transition Fund funded by a levy on oil and gas production
- Develop retraining programmes for energy sector workers in renewable energy and hydrogen
- Create a regional economic diversification strategy reducing fossil fuel dependence by 2040

**Tensions:**

- Just transition investment may not move fast enough to prevent community economic disruption
- State support for fossil fuel workers may reduce urgency of decarbonisation action

**Interventions on the system:**

- Establish Taranaki Just Transition Fund (state variable: `fossil_fuel_employment_share`, sign: -)
- Retraining programmes for energy workers (state variable: `renewable_energy_employment`, sign: +)


### Regulatory emissions reduction

Binding emissions reduction targets and agricultural emissions pricing create the necessary market signals for decarbonisation.

**Flagship moves:**

- Apply He Waka Eke Noa pricing to Taranaki agricultural emissions
- Fast-track renewable energy consenting and grid connection for regional projects
- Mandate emissions intensity reporting for all major industrial facilities

**Tensions:**

- Emissions pricing may accelerate farm financial stress before adaptation options are available
- Industrial transition costs could trigger business departure from the region

**Interventions on the system:**

- Agricultural emissions pricing under He Waka Eke Noa (state variable: `agricultural_emissions_intensity`, sign: -)
- Renewable energy consenting fast-track (state variable: `renewable_energy_capacity`, sign: +)


---

## Claims cited on this page

- **Taranaki's industrial emissions from oil and gas operations (Methanex, Todd Energy, OMV) historically represented 5-8% of NZ's greenhouse gas inventory. The region accounts for ~4-5% of NZ's total emissions, dominated by energy sector processing and fugitive methane from natural gas extraction.** *(confidence: medium)* — New Plymouth District Council Annual Plan 2024.

---

## Further reading


- **New Plymouth District Council Annual Plan 2024** (New Plymouth District Council), 2024


---

## Technical notes

*State variables:* climate_emissions_index.

*Constraints:* climate_emissions_constraint.

*Inputs:* climate_emissions_input_1.


*Feedback loops:*

- `Feedback: climate_emissions`


---

*Generated from `problem.taranaki.climate.climate_emissions` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
