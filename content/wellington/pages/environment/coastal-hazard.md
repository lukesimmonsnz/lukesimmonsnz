---
title: "Coastal erosion and sea-level rise risk in Wellington"
section: environment
subpage: coastal-hazard
order: 4
updated: 2026-04-26
summary: >
  Wellington's coastal margins — particularly Petone Foreshore, Lyall Bay, and the Kāpiti Coast — face growing coastal erosion and flooding risk from sea-level rise and increased storm intensity. The combination of subsidence risk from earthquake activity and sea-level rise creates compound exposure in low-lying areas.
status: draft
generated_from: problem.wellington.environment.coastal_hazard
---

# Coastal erosion and sea-level rise risk in Wellington

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Sea level projections for Wellington

Wellington is projected to experience 0.4–1.0 m of sea-level rise by 2100 under medium-to-high emissions scenarios, with the upper end representing a credible planning horizon for long-lived coastal infrastructure (claim.wellington.environment.sea_level_projection_2100).


## Coastal erosion

Several Wellington coastal sections including Lyall Bay and parts of the Kāpiti Coast are experiencing measurable erosion rates. Rising sea levels will accelerate these dynamics and increase the frequency of storm-surge overtopping events at Petone Foreshore (claim.wellington.environment.coastal_erosion_rate).


---


## Drivers

The following structural drivers contribute to this problem.


### Legacy coastal development in hazard zones



- **Category:** institutional
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


### Coastal Protection Infrastructure Investment

Sea walls, tide gates, and foreshore protection can defend existing coastal assets for at least 30–50 years while longer-term adaptation plans are developed.

**Flagship moves:**

- Upgrade Petone Foreshore protection works to 1m SLR standard
- Install tide gates on key storm drain outfalls in Miramar and Seaview
- Dynamic revetment programme using locally sourced rock armour

**Tensions:**

- Hard protection creates lock-in and may worsen adjacent erosion
- 30-50 year protection horizon may not match residual property lifetimes in highest-risk areas

**Interventions on the system:**

- Fund coastal protection upgrade for Petone Foreshore to $80M standard with GWRC/WCC/Crown co-funding (state variable: `coastal_protection_standard`, sign: +)


### Managed Coastal Retreat

Low-lying coastal properties in Wellington should be subject to planned retreat as sea-level rise projections make long-term protection uneconomic.

**Flagship moves:**

- Establish rolling easement policy for Petone Foreshore and Miramar low-lying areas
- Voluntary buy-out scheme for highest-risk coastal properties
- Prohibit new insurance-ineligible development in 1-in-100-year coastal flood zones

**Tensions:**

- Property rights implications of managed retreat are legally and politically contested
- Buy-out valuations may be insufficient to fund equivalent housing elsewhere

**Interventions on the system:**

- Designate Petone Foreshore and Seaview as priority coastal adaptation zones with planning controls reflecting 2100 SLR projections (state variable: `coastal_exposure_population`, sign: -)


---

## Claims cited on this page

- **Wellington is projected to experience 0.4–1.0 m of sea-level rise by 2100 under medium-to-high emissions scenarios, with the upper bound representing a credible planning horizon for long-lived coastal infrastructure such as roads, rail, and port facilities.** — New Zealand Sea Level Rise Guidance: Updated Projections 2023.
- **Several Wellington coastal sections including parts of Lyall Bay beach and the Kāpiti Coast are experiencing measurable erosion rates that will be accelerated by sea-level rise, with storm-surge overtopping events at Petone Foreshore projected to increase in frequency over the coming decades.** *(confidence: medium)* — New Zealand Sea Level Rise Guidance: Updated Projections 2023; Greater Wellington State of the Environment Report 2022.

---

## Further reading


- **New Zealand Sea Level Rise Guidance: Updated Projections 2023** (Ministry for the Environment), 2023 — <https://environment.govt.nz/publications/coastal-hazards-and-climate-change-guidance/>

- **Greater Wellington State of the Environment Report 2022** (Greater Wellington Regional Council), 2022 — <https://www.gw.govt.nz/environment/state-of-the-environment/>


---

## Technical notes

*State variables:* sea_level_cm_above_1990_baseline, coastal_erosion_rate_m_per_year.

*Constraints:* coastal_development_legacy, managed_retreat_political_feasibility.

*Inputs:* global_temperature_pathway, storm_surge_frequency.


*Feedback loops:*

- `Storm-erosion amplification: sea-level rise reduces the protective buffer of beaches and dunes, increasing the erosion damage from each storm event of the same intensity.`


---

*Generated from `problem.wellington.environment.coastal_hazard` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
