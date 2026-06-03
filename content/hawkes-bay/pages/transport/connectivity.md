---
title: "Regional transport connectivity and mode diversity"
section: transport
subpage: connectivity
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay faces limited transport mode diversity, heavy car dependence, and exposure of State Highway 2 to flooding and slips. Public transport coverage is sparse outside Napier-Hastings. Active transport networks are fragmented.
status: draft
generated_from: problem.hawkes_bay.transport.connectivity
---

# Regional transport connectivity and mode diversity

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Car Dependence

Approximately 87% of commute trips in Hawke's Bay are by private car. Public transport carries fewer than 2 million passenger journeys per year across a population of 170k.


## SH2 Resilience

State Highway 2 is the only practical north-south corridor. Cyclone Gabrielle demonstrated severe flood and slip vulnerability, with closures lasting weeks.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic isolation and dispersed population



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### State Highway 2 terrain and climate vulnerability



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Public transport investment and subsidies

Public transport investment and subsidies is the primary strategy.

**Flagship moves:**

- Implement Public transport investment and subsidies across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Public transport investment and subsidies intervention (state variable: `public_investment_index`, sign: +) (relaxes: `public_investment_constraint`)


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

- **Transport connectivity in Hawkes Bay is limited outside major urban centers, forcing private vehicle dependence. Public transit is sparse; road freight reliance increases logistics costs; geographic isolation constrains workforce mobility and business access to markets.** [value: 87 percent; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **State Highway 2 closures due to slips, flooding, or earthquakes isolate Wairoa from Napier/Hastings for average 3.5 weeks per major event cycle. Cyclone Gabrielle (Feb 2023) closed SH2 and SH5 for 8+ weeks, stranding Wairoa and cutting agricultural supply chains. Single-road dependency creates critical business continuity and emergency response vulnerabilities; rail infrastructure is freight-only (KiwiRail), lacking passenger resilience alternatives.** [value: 3.5 weeks; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* car_mode_share_percent, public_transport_patronage_per_capita.

*Constraints:* topographic_narrowness_sh2, post_cyclone_resilience_deficits.

*Inputs:* land_use_dispersal, sparse_population_density.


*Feedback loops:*

- `Low patronage defers transit investment; sparse service drives car adoption; congestion and emissions rise; mode shift to transit harder.`


---

*Generated from `problem.hawkes_bay.transport.connectivity` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
