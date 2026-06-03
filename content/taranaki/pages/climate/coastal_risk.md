---
title: "Coastal hazards and sea-level rise adaptation"
section: climate
subpage: coastal_risk
order: 2
updated: 2026-04-26
summary: >
  Coastal areas including New Plymouth face sea-level rise and storm surge risk. Adaptation options are underdeveloped.
status: draft
generated_from: problem.taranaki.climate.coastal_risk
---

# Coastal hazards and sea-level rise adaptation

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Coastal hazards and sea-level rise adaptation in Taranaki

Coastal areas including New Plymouth face sea-level rise and storm surge risk. Adaptation options are underdeveloped.


---


## Drivers

The following structural drivers contribute to this problem.


### Coastal erosion and agricultural climate risk



- **Category:** climate
- **Timescale:** long
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

- **Taranaki's 115km coastline faces sea-level rise projections of 0.5-1.2m by 2100 (RCP 6.0), combined with increased storminess and wave heights. Coastal settlements (New Plymouth, Opunake) and agricultural land in coastal plains face progressive inundation and saltwater intrusion risks affecting dairy and horticulture.** *(confidence: medium)* — New Plymouth District Council Annual Plan 2024.

---

## Further reading


- **New Plymouth District Council Annual Plan 2024** (New Plymouth District Council), 2024


---

## Technical notes

*State variables:* coastal_risk_index.

*Constraints:* coastal_risk_constraint.

*Inputs:* coastal_risk_input_1.


*Feedback loops:*

- `Feedback: coastal_risk`


---

*Generated from `problem.taranaki.climate.coastal_risk` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
