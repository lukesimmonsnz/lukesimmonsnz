---
title: "Earthquake vulnerability of Wellington's critical lifelines"
section: infrastructure
subpage: earthquake-lifelines
order: 3
updated: 2026-04-26
summary: >
  Wellington's critical lifeline infrastructure — water, wastewater, electricity, transport, and telecommunications — sits across the Wellington and Wairarapa fault systems. A major fault rupture is modelled to produce extended outages across multiple systems simultaneously, with the water network particularly vulnerable to pipe breaks and pump station failure.
status: draft
generated_from: problem.wellington.infrastructure.earthquake_lifelines
---

# Earthquake vulnerability of Wellington's critical lifelines

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Modelled rupture impacts

GNS Science models a Wellington Fault Mw 7.5 rupture causing widespread liquefaction, bridge failures, and water network breaks across lower Hutt and Petone, with projected restoration times of weeks to months for full water supply (claim.wellington.infrastructure.lifeline_vulnerability_assessment).


## CentrePort as precedent

The 2016 Kaikōura earthquake caused significant liquefaction damage to CentrePort Wellington — demonstrating that infrastructure on reclaimed land in the harbour is acutely vulnerable to earthquake shaking at magnitude levels that are credible within Wellington's probabilistic hazard profile (claim.wellington.infrastructure.centreport_kaikoura_damage).


---


## Drivers

The following structural drivers contribute to this problem.


### Fault zone alignment of critical infrastructure



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Liquefaction risk on reclaimed harbour land



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Community Resilience Hubs for Post-Earthquake Response

Decentralised community hubs with food, water, and communications ensure neighbourhood-level resilience without relying on utility restoration.

**Flagship moves:**

- Establish 20 community resilience hubs in Wellington suburbs
- Water storage tanks (10,000L) at each hub with purification capability
- Battery-backed radio communications independent of telecoms grid

**Tensions:**

- Hub model addresses symptoms not causes; does not reduce earthquake damage to infrastructure
- Ongoing maintenance and stock rotation costs fall to councils or communities

**Interventions on the system:**

- Fund 20 community resilience hubs using CDEM budget with co-governance by local community groups (state variable: `community_resilience_coverage`, sign: +)


### Lifeline Utility Seismic Hardening

Critical utility crossings of the Wellington Fault must be hardened or bypassed to ensure post-earthquake recovery within weeks not months.

**Flagship moves:**

- Fault-crossing resilience upgrades for water, gas, and electricity at Wellington Fault crossings
- Dual water supply routes from Wainuiomata and Hutt Valley to the city
- Pre-positioned emergency water storage cisterns at key community hubs

**Tensions:**

- High capital cost for low-probability but high-consequence event
- Prioritisation of seismic hardening may displace routine maintenance budgets

**Interventions on the system:**

- Establish Wellington Lifelines Group investment programme targeting the 12 critical fault crossings (state variable: `post_earthquake_recovery_days`, sign: -)


---

## Claims cited on this page

- **GNS Science modelling indicates that a Wellington Fault Mw 7.5 rupture would cause widespread liquefaction and pipe breaks across lower Hutt and Petone, with projected water supply restoration times of weeks to months for affected areas.** — Wellington Fault Earthquake Hazard Assessment.
- **The November 2016 Kaikōura earthquake (Mw 7.8) caused significant liquefaction damage to CentrePort Wellington on reclaimed harbour land, resulting in estimated losses exceeding NZD 280 million and demonstrating the acute seismic vulnerability of Wellington's port infrastructure.** [value: 280 NZD million (estimated losses); 2016-2018] — Wellington Fault Earthquake Hazard Assessment; Wellington City Council Annual Plan 2024/25.

---

## Further reading


- **Wellington Fault Earthquake Hazard Assessment** — Van Dissen R et al. (GNS Science), 2022 — <https://www.gns.cri.nz/research/natural-hazards/earthquakes/wellington-fault/>

- **Wellington City Council Annual Plan 2024/25** (Wellington City Council), 2024 — <https://www.wellington.govt.nz/your-council/plans-policies-and-bylaws/annual-plan>


---

## Technical notes

*State variables:* lifeline_restoration_time_days, critical_facility_seismic_rating.

*Constraints:* fault_alignment_with_infrastructure_corridors, upgrade_funding_gap.

*Inputs:* fault_rupture_magnitude, infrastructure_seismic_upgrade_rate.


*Feedback loops:*

- `Vulnerability persistence loop: high upgrade costs and competing priorities defer lifeline seismic strengthening; each deferred year increases expected restoration time post-rupture.`


---

*Generated from `problem.wellington.infrastructure.earthquake_lifelines` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
