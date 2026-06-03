---
title: "Port of Napier access and efficiency"
section: transport
subpage: napier-port-access
order: 2
updated: 2026-04-26
summary: >
  Port of Napier is NZ's second-busiest export port. Road congestion in Napier central to port affects efficiency; rail access is underused; coastal hazards threaten port infrastructure expansion and long-term viability.
status: draft
generated_from: problem.hawkes_bay.transport.napier_port_access
---

# Port of Napier access and efficiency

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Export Dependency

Napier port handles approximately 8 million tonnes annually, including apple, wine, and general cargo exports essential to Hawke's Bay economy.


## Urban Congestion

Port trucks compete for road space with urban traffic. Peak-hour congestion around Napier CBD extends port dwell times and raises logistics costs.


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

- **Transport connectivity in Hawkes Bay is limited outside major urban centers, forcing private vehicle dependence. Public transit is sparse; road freight reliance increases logistics costs; geographic isolation constrains workforce mobility and business access to markets.** [value: 8 million tonnes; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* port_throughput_million_tonnes, urban_port_congestion_index.

*Constraints:* central_business_district_footprint, coastal_hazard_exposure.

*Inputs:* sh2_port_access_bottleneck, urban_land_use_constraint.


*Feedback loops:*

- `Congestion increases transport costs; some exports bypass Napier; port revenue constraints limit expansion; infrastructure renewal deferred.`


---

*Generated from `problem.hawkes_bay.transport.napier_port_access` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
