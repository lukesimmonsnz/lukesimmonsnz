---
title: "Alpine Fault Seismic Hazard & Preparedness"
section: climate
subpage: alpine_fault_earthquake
order: 1
updated: 2026-04-26
summary: >
  The Alpine Fault has ruptured in M7+ earthquakes every 200-350 years; last rupture was ~1717. Seismic science (GNS 2022) estimates ~15% probability of M7+ rupture in next 50 years. Canterbury lies in the rupture zone; ground shaking, landslides, liquefaction, and possible tsunami are severe. Critical infrastructure (Lyttelton Port, Christchurch Hospital, transport corridors) would be severely disrupted for months. Preparedness and resilience planning is incomplete.

status: draft
generated_from: problem.canterbury.climate.alpine_fault_earthquake
---

# Alpine Fault Seismic Hazard & Preparedness

<p class="horizon-band">Analysis horizon: 50yr · 100yr</p>



## Historic hazard, modern risk

1717 Alpine Fault rupture caused widespread damage (documented in oral histories, geological evidence). Modern Christchurch (1.4M population, $200B+ assets) is far more vulnerable. Hospital, airport, water systems, port are not seismically resilient to M7+. Post-2011 earthquake improvements help but are incomplete. Insurance for Alpine Fault risk is increasingly expensive or unavailable.


---


## Drivers

The following structural drivers contribute to this problem.


### Alpine Fault Seismic Hazard (M7+ probability ~15% in 50yr)



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Earthquake-Resilient Critical Infrastructure Upgrade

Prioritized seismic upgrade of critical infrastructure (hospital, water treatment, port) to M7+ standards ensures continuity during Alpine Fault rupture.

**Flagship moves:**

- Key intervention for Earthquake-Resilient Critical Infrastructure Upgrade

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Prioritized seismic upgrade of critical infrastructure (hospital, water treatment, port) to M7+ standards ensures continuity during Alpine Fault rupture. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


### Integrated Hazard Planning & Critical Infrastructure Resilience

Unified climate and seismic risk planning ensures critical infrastructure (port, hospital, water, transport) is resilient to compound hazards.

**Flagship moves:**

- Key intervention for Integrated Hazard Planning & Critical Infrastructure Resilience

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Unified climate and seismic risk planning ensures critical infrastructure (port, hospital, water, transport) is resilient to compound hazards. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Alpine Fault seismic hazard in Canterbury remains elevated. GNS Science (2022) estimated 15% probability of M7.0+ rupture within 50 years; such an event would cause widespread damage to critical infrastructure (Lyttelton Port, Christchurch Hospital, SH1/73).** [value: 15 percent probability (50yr); 2022] *(confidence: medium)* — GNS Science Alpine Fault Hazard Assessment 2022.
- **Critical infrastructure in Canterbury (Lyttelton Port Authority, Christchurch International Airport, regional hospitals) faces compounded seismic, flood, and drought hazards. 2010-2011 earthquakes (185 dead, $40B damage) demonstrated infrastructure fragility; post-earthquake rebuilding still ongoing for some health and transport assets.** [value: 65 percent adequacy; 2023] *(confidence: medium)* — GNS Science Alpine Fault Hazard Assessment 2022.
- **Project AF8 is a multi-agency South Island civil-defence planning programme that prepares for the response to an anticipated magnitude-8 Alpine Fault earthquake. The project models a multi-day to multi-week disruption of South Island critical infrastructure - road and rail corridors (especially SH73 / TranzAlpine), Lyttelton Port, electricity and telecommunications networks - with Christchurch as the major population centre most exposed to ground-shaking and cascading service-disruption effects.
** [value: 8 moment magnitude (anticipated rupture); 2021] *(confidence: medium)* — Project AF8 - South Island Alpine Fault Magnitude 8 Earthquake Response Planning.

---

## Further reading


- **GNS Science Alpine Fault Hazard Assessment 2022** (GNS Science), 2022 — <https://www.gns.cri.nz/>

- **Project AF8 - South Island Alpine Fault Magnitude 8 Earthquake Response Planning** — Project AF8 (multi-agency) (Emergency Management Otago / National Emergency Management Agency), 2021 — <https://www.af8.org.nz/>


---

## Technical notes

*State variables:* critical_infrastructure_seismic_resilience_score, building_code_compliance_rate_essential_facilities, emergency_response_supply_stockpile_adequacy, insurance_underwriting_in_high_hazard_zones.

*Constraints:* retrofit_cost_and_funding, seismic_uncertainty.

*Inputs:* building_retrofit_investment_rate, emergency_preparedness_funding, insurance_market_pricing.


*Feedback loops:*

- `Dynamic feedback mechanisms drive alpine fault seismic hazard & preparedness.`


---

*Generated from `problem.canterbury.climate.alpine_fault_earthquake` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
