---
title: "Sea-level rise risk in low-lying Wellington areas"
section: climate
subpage: sea-level-rise
order: 2
updated: 2026-04-26
summary: >
  Sea-level rise threatens significant areas of low-lying Wellington, including Petone Foreshore, Rongotai, parts of Porirua Harbour, and the Hutt River mouth. These areas include key transport infrastructure, residential neighbourhoods, and industrial land on reclaimed harbour margins.
status: draft
generated_from: problem.wellington.climate.sea_level_rise
---

# Sea-level rise risk in low-lying Wellington areas

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Petone and Rongotai exposure

Wellington's Petone Foreshore is among the most exposed low-lying coastal areas in the region, with modelled flood risk increasing substantially by 2100 even under moderate sea-level rise scenarios. Rongotai, where Wellington Airport is located, faces similar low-lying exposure (claim.wellington.climate.sea_level_projection_petone).


## Exposure of low-lying areas

Thousands of properties and key transport routes — including the Hutt Road and the rail line along the harbour shore — sit in areas projected to experience increased flood and storm surge frequency within the current planning horizon for infrastructure (claim.wellington.climate.low_lying_area_exposure).


---


## Drivers

The following structural drivers contribute to this problem.


### Global sea-level rise from climate change



- **Category:** climate
- **Timescale:** long
- **Consensus:** consensus

### Reclaimed land coastal exposure to sea-level rise



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Sea-level rise under climate change



- **Category:** climate
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Coastal Adaptation Planning for Sea Level Rise

Wellington requires a funded regional coastal adaptation plan with clear timelines for managed retreat and protection decisions.

**Flagship moves:**

- Commission Wellington Regional Coastal Adaptation Plan under the forthcoming Coastal Adaptation Act
- Property disclosure scheme for coastal risk within planning horizons
- Crown-funded buy-out scheme for highest-risk coastal homes (Category 3 equivalent)

**Tensions:**

- Property buy-outs require significant Crown funding that competes with other priorities
- Planning horizons for SLR are inherently uncertain, making firm commitment difficult

**Interventions on the system:**

- Develop Wellington Regional Coastal Adaptation Plan with 2040 and 2100 SLR scenarios and clear property-tier categorisation (state variable: `coastal_adaptation_plan_completeness`, sign: +)


---

## Claims cited on this page

- **Wellington's Petone Foreshore — a low-lying reclaimed coastal area in Lower Hutt — is projected to experience increasing flood and storm surge frequency under medium sea-level rise scenarios (0.4–0.7 m by 2100), threatening road, rail, and residential assets on the foreshore.** — New Zealand Sea Level Rise Guidance: Updated Projections 2023; Greater Wellington State of the Environment Report 2022.
- **Thousands of Wellington region properties and key transport routes — including the Hutt Road, the rail line along the harbour shore, and the Rongotai isthmus — sit in areas projected to experience increased flood and storm-surge frequency within the planning horizon of current infrastructure investments.** *(confidence: medium)* — New Zealand Sea Level Rise Guidance: Updated Projections 2023; Wellington City Council Climate Change Action Plan 2023.

---

## Further reading


- **New Zealand Sea Level Rise Guidance: Updated Projections 2023** (Ministry for the Environment), 2023 — <https://environment.govt.nz/publications/coastal-hazards-and-climate-change-guidance/>

- **Greater Wellington State of the Environment Report 2022** (Greater Wellington Regional Council), 2022 — <https://www.gw.govt.nz/environment/state-of-the-environment/>

- **Wellington City Council Climate Change Action Plan 2023** (Wellington City Council), 2023 — <https://www.wellington.govt.nz/environment-and-sustainability/climate-change>


---

## Technical notes

*State variables:* sea_level_cm_above_1990, at_risk_property_count.

*Constraints:* existing_development_on_reclaimed_land, managed_retreat_feasibility.

*Inputs:* global_temperature_pathway, managed_retreat_investment.


*Feedback loops:*

- `Adaptation investment deferral: long time horizons for sea-level rise allow near-term political cycles to defer investment; each cycle of deferral increases eventual adaptation cost.`


---

*Generated from `problem.wellington.climate.sea_level_rise` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
