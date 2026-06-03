---
title: "State Highway 2 flood and slip resilience"
section: transport
subpage: sh2-resilience
order: 2
updated: 2026-04-26
summary: >
  SH2 is vulnerable to landslides and flooding through Kaweka and Kawekas gaps. Cyclone Gabrielle caused multi-week closures. Limited alternate routes force diversions 100+ km. Maintenance and resilience investment is underfunded.
status: draft
generated_from: problem.hawkes_bay.transport.sh2_resilience
---

# State Highway 2 flood and slip resilience

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Vulnerability

SH2 passes through three narrow gorges (Gentle Annie, Kaweka, Kawekas) prone to landslips. Cyclone Gabrielle caused four major slips blocking all traffic.


## Economic Impact

Each SH2 closure forces trucks onto 130km+ alternate routes (via Waipawa/Taihape), adding 4+ hours to transit time and raising logistics costs region-wide.


---


## Drivers

The following structural drivers contribute to this problem.


### State Highway 2 terrain and climate vulnerability



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### State Highway 2 resilience and redundancy

Systematic investment in SH2 maintenance, slope stabilisation, and development of alternate north-south routes improves regional connectivity and economic resilience.

**Flagship moves:**

- Implement a 10-year SH2 resilience programme with $2 billion investment in slip prevention and drainage
- Develop business cases for coastal transport route alternatives (rail revival, coastal highway)
- Establish emergency response protocols for rapid SH2 restoration post-closures

**Tensions:**

- Alternative routes (rail, coastal) require massive upfront investment with uncertain returns
- Coastal alternatives raise environmental and Māori land tenure issues

**Interventions on the system:**

- Stabilise Gentle Annie, Kaweka, and Kawekas gorges with engineered slope works (state variable: `sh2_closure_frequency_events_per_year`, sign: -)
- Enhance drainage and early warning systems to reduce landslip risk (state variable: `soil_saturation_monitoring_coverage`, sign: +)


---

## Claims cited on this page

- **Transport connectivity in Hawkes Bay is limited outside major urban centers, forcing private vehicle dependence. Public transit is sparse; road freight reliance increases logistics costs; geographic isolation constrains workforce mobility and business access to markets.** [value: 4 weeks; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* sh2_closure_days_per_year, resilience_investment_gap_dollars.

*Constraints:* maintenance_budget_constraint, terrain_engineering_cost.

*Inputs:* terrain_slope_steepness, rainfall_intensification.


*Feedback loops:*

- `Underfunded maintenance increases closure frequency; business relocates; tax base erodes; maintenance budget shrinks further.`


---

*Generated from `problem.hawkes_bay.transport.sh2_resilience` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
