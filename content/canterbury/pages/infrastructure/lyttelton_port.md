---
title: "Lyttelton Port Infrastructure & Resilience"
section: infrastructure
subpage: lyttelton_port
order: 2
updated: 2026-04-26
summary: >
  Lyttelton Port (Eastland) is Canterbury's primary import-export gateway, handling ~30% of NZ's container traffic. Post-earthquake damage (2011) and ongoing seismic vulnerability create operational risk; port company faces capital constraints for berth modernization and earthquake-resilience upgrades.

status: draft
generated_from: problem.canterbury.infrastructure.lyttelton_port
---

# Lyttelton Port Infrastructure & Resilience

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Critical infrastructure at seismic risk

Lyttelton Port survived the 2011 quakes with significant damage and downtime. Port Company faces aging berth infrastructure and constrained capital for modernization. An Alpine Fault rupture (M7.0+) could disable the port for 6-12 months, disrupting NZ's container supply chain.


---


## Drivers

The following structural drivers contribute to this problem.


### Alpine Fault Seismic Hazard



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Lyttelton Port Seismic Resilience Upgrade

Targeted capital investment in berth seismic strengthening and operational redundancy (satellite container handling) reduces Alpine Fault rupture exposure.

**Flagship moves:**

- Key intervention for Lyttelton Port Seismic Resilience Upgrade

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Targeted capital investment in berth seismic strengthening and operational redundancy (satellite container handling) reduces Alpine Fault rupture exposure. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Lyttelton Port of Christchurch handled 2.1 million TEU (Twenty-foot Equivalent Units) in 2023, serving South Island import/export traffic. The port is South Island's busiest, handling ~40% of South Island container traffic and serving as the primary gateway for Canterbury's $40 billion rebuild, dairy exports (milk powder, cheese), and wine shipments (Waipara region). Post-COVID recovery to 2.1M TEU represents 85% of pre-2020 peak; seasonal fluctuation is pronounced due to agricultural export concentration.** [value: 2.1 million TEU; 2023] *(confidence: medium)* — Christchurch City Council Annual Plan 2024-2025.
- **Alpine Fault seismic hazard in Canterbury remains elevated. GNS Science (2022) estimated 15% probability of M7.0+ rupture within 50 years; such an event would cause widespread damage to critical infrastructure (Lyttelton Port, Christchurch Hospital, SH1/73).** [value: 9 months estimated downtime; 2024] *(confidence: medium)* — GNS Science Alpine Fault Hazard Assessment 2022.

---

## Further reading


- **Christchurch City Council Annual Plan 2024-2025** (Christchurch City Council), 2024 — <https://www.ccc.govt.nz/the-council/planning-strategy-and-policy/annual-plan/>

- **GNS Science Alpine Fault Hazard Assessment 2022** (GNS Science), 2022 — <https://www.gns.cri.nz/>


---

## Technical notes

*State variables:* port_throughput_teu, berth_utilization_rate, asset_seismic_resilience_index.

*Constraints:* port_company_capex_budget, alpine_fault_rupture_risk.

*Inputs:* regional_trade_volume, ship_size_growth, seismic_event_occurrence.


*Feedback loops:*

- `Dynamic feedback mechanisms drive lyttelton port infrastructure & resilience.`


---

*Generated from `problem.canterbury.infrastructure.lyttelton_port` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
