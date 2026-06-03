---
title: "Golden Bay road-access dependence on a single hill route"
section: transport
subpage: connectivity_2
order: 2
updated: 2026-04-26
summary: >
  Golden Bay / Mohua is reached by road only via SH60 over the Takaka Hill — roughly 105 km and 90 minutes to Nelson Hospital. The hill is exposed to slips, washouts, and fog; closures isolate the community for days at a time and force medical emergencies onto helicopter evacuation.
status: draft
generated_from: problem.tasman.transport.connectivity_2
---

# Golden Bay road-access dependence on a single hill route

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## One hill between Mohua and the rest of the region

Takaka, Collingwood and the wider Golden Bay community depend on SH60 over the Takaka Hill for almost all goods, services, and emergency access. Motueka is roughly 45 minutes away and provides community health services only; the nearest hospital with emergency and maternity capacity is Nelson Hospital, around 90 minutes away (claim.tasman.transport.connectivity_2_claim).


## Closure cost is borne mostly by residents

Twelve major Takaka Hill closures between 2018 and 2023 isolated Golden Bay for two-to-five days each (claim.tasman.infrastructure.infrastructure_4_claim). During those windows, helicopter evacuation costs of NZD 4,500-6,000 per trip act as a regressive surcharge on rural and lower-income households who cannot self-insure against isolation.


---


## Drivers

The following structural drivers contribute to this problem.


### Single-corridor topography of Tasman



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Active Travel and Demand Management

Shifting short trips to walking and cycling reduces vehicle demand, improves liveability, and is the most cost-effective congestion response.

**Flagship moves:**

- Build separated cycling infrastructure on key commuter corridors
- Subsidise e-bike purchase for low-income residents
- Introduce school travel plans to reduce car drop-offs

**Tensions:**

- Active travel requires safety infrastructure investment before behaviour change follows
- Limited budget competes with roading maintenance priorities

**Interventions on the system:**

- Develop connected cycling and walking network linking residential areas to employment and retail centres (state variable: `active_mode_share`, sign: +)


### Response: Camp 1

A response strategy addressing transport challenges.

**Flagship moves:**

- Build dedicated cycling and walking infrastructure connecting Tasman urban centres
- Expand bus frequency and coverage on key corridors
- Develop park-and-ride facilities at key transport nodes

**Tensions:**

- Transport investment requires sustained funding and may face competing regional priorities.
- Mode shift away from private cars faces social resistance in car-dependent communities.

**Interventions on the system:**

- Improve transport connectivity and mode choice in Tasman (state variable: `transport_accessibility`, sign: +)
- Invest in active transport infrastructure (state variable: `active_mode_share`, sign: +)


---

## Claims cited on this page

- **Golden Bay transport isolation is acute: SH60 over Takaka Hill is the sole vehicular access route, approximately 105 km and 90 minutes from Takaka to Nelson. Motueka (45 minutes from Takaka) provides community health services only; the nearest hospital with emergency and maternity capacity is Nelson Hospital. Golden Bay Shuttle (local bus) runs three days per week; school bus services are reduced during holidays. Medical emergencies typically require helicopter evacuation (estimated cost NZD 4,500-6,000).** [value: 90 minutes from Takaka (Golden Bay) to Nelson Hospital; 2024] — Tasman District Council Annual Plan 2024; Health Outcomes Tasman Region 2023.

---

## Further reading


- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>

- **Health Outcomes Tasman Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>


---

## Technical notes

*State variables:* takaka_hill_open_days_per_year, minutes_to_nelson_hospital.

*Constraints:* single_road_alignment, geological_instability_takaka_hill.

*Inputs:* sh60_resilience_capex, rescue_helicopter_capacity.


*Feedback loops:*

- `Each major closure reinforces population thinning of younger and medically-vulnerable residents in Golden Bay, which reduces the political return on resilience investment.`


---

*Generated from `problem.tasman.transport.connectivity_2` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
