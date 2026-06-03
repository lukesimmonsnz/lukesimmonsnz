---
title: "Fragile single-corridor transport network in Wellington"
section: transport
subpage: network-resilience
order: 1
updated: 2026-04-26
summary: >
  Wellington's transport network is structurally fragile: a single coastal corridor carries the dominant share of freight, passenger rail, and road traffic. A major seismic event, infrastructure failure, or weather event on this corridor leaves the region with no viable alternative route. The Cook Strait ferry dependency amplifies this single-point-of-failure characteristic at the national scale.
status: draft
generated_from: problem.wellington.transport.network_resilience
---

# Fragile single-corridor transport network in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The single-corridor problem

Wellington's main transport corridor runs through the Terrace Tunnel and along the Hutt Road — a narrow coastal strip vulnerable to landslip, flooding, and fault rupture. The Terrace Tunnel and Mt Victoria Tunnel, both over 100 years old, form irreplaceable bottlenecks with no alternative alignment (claim.wellington.transport.rail_tunnel_age).


## Network fragility and resilience

A major Wellington Fault rupture would likely close SH1, the Terrace Tunnel, and the rail network simultaneously, severing overland connection to the Hutt Valley and Kāpiti Coast for an extended period (claim.wellington.transport.network_single_corridor_risk).


---


## Drivers

The following structural drivers contribute to this problem.


### Aging tunnel and corridor infrastructure



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus

### Geographic single-corridor constraint



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Post-COVID mode shift and demand uncertainty



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** mostly-agreed


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Rail Network Investment and Hardening

Wellington's rail network is the backbone of regional transport; capital renewal and seismic hardening must be prioritised over road expansion.

**Flagship moves:**

- Full renewal of rolling stock and overhead infrastructure on Hutt and Kapiti lines
- Seismic assessment and hardening of Thorndon and Ngauranga rail cuttings
- Dual-fuel or battery multiple units to reduce diesel dependency

**Tensions:**

- Capital cost displaces other infrastructure investment over multi-year programme
- Rail-centric approach leaves Porirua and eastern suburbs underserved

**Interventions on the system:**

- Commit to 10-year rolling stock renewal programme funded jointly by Crown and GWRC (state variable: `rail_reliability`, sign: +) (relaxes: `deferred_rail_investment`)


### Road Corridor Capacity Expansion

New road tunnels through the Wellington hills are essential to reduce congestion and provide resilient corridors.

**Flagship moves:**

- Progress Mt Victoria second tunnel to construction within this decade
- Advance Terrace Tunnel replacement to four-lane capacity
- Improve SH2 Upper Hutt resilience with alternative alignment

**Tensions:**

- Induced demand will erode congestion benefits within 10–15 years
- Large capital projects crowd out frequent-service public transport investment
- Carbon intensity of construction conflicts with Wellington City's climate commitments

**Interventions on the system:**

- Begin detailed business case for Mt Victoria second tunnel and Terrace Tunnel replacement (state variable: `cross_isthmus_capacity`, sign: +)


---

## Claims cited on this page

- **Wellington's Mt Victoria Tunnel (opened 1931) and Terrace Tunnel (opened 1974) carry the majority of vehicle traffic between the CBD and the eastern suburbs and Hutt Valley corridor; the Mt Victoria Tunnel is over 90 years old and both have no alternative alignment in the event of closure.** [value: 93 years (age of Mt Victoria Tunnel as of 2024); 2024] — Wellington Regional Land Transport Plan 2021–31; NZTA Wellington Transport Corridor: State Highway Performance Report 2023.
- **Wellington's primary transport corridor — along the coastal SH1 and through the Terrace and Mt Victoria tunnels — forms a single failure point for road and rail travel; a major earthquake on the Wellington Fault is modelled to close this corridor simultaneously for an extended period.** — Wellington Fault Earthquake Hazard Assessment; Wellington Regional Land Transport Plan 2021–31.

---

## Further reading


- **Wellington Regional Land Transport Plan 2021–31** (Greater Wellington Regional Council), 2021 — <https://www.gw.govt.nz/transport/regional-land-transport-plan/>

- **NZTA Wellington Transport Corridor: State Highway Performance Report 2023** (NZ Transport Agency Waka Kotahi), 2023 — <https://www.nzta.govt.nz/roads-and-rail/roads/state-highways/>

- **Wellington Fault Earthquake Hazard Assessment** — Van Dissen R et al. (GNS Science), 2022 — <https://www.gns.cri.nz/research/natural-hazards/earthquakes/wellington-fault/>


---

## Technical notes

*State variables:* network_redundancy_score, corridor_daily_vehicle_km.

*Constraints:* geographic_corridor_constraint, tunnel_age_and_condition.

*Inputs:* infrastructure_investment, seismic_event_probability.


*Feedback loops:*

- `Disruption-cost feedback: periodic closures (weather, incidents) demonstrate the fragility, increasing public pressure for redundancy investment but not generating consistent long-term funding.`


---

*Generated from `problem.wellington.transport.network_resilience` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
