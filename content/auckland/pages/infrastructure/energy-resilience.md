---
title: "Energy infrastructure resilience and electrification"
section: infrastructure
subpage: energy-resilience
order: 3
updated: 2026-04-26
summary: >
  Auckland's electricity supply is transmission-dependent, relying on long lines from Waikato and Northland to serve a city that generates relatively little power locally. The 1998 CBD blackout demonstrated the consequences of transmission failure; resilience has improved but N-1 and N-2 risk remains. Simultaneously, electrification of transport and heating will add 1–2 GW of new demand by 2040, requiring proactive grid investment and demand management to avoid supply security risks. The window to invest ahead of demand is now.

status: draft
generated_from: problem.auckland.infrastructure.energy_resilience
---

# Energy infrastructure resilience and electrification

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Transmission dependency

Auckland is an electricity consumer, not a generator. Its power comes via long transmission lines from Waikato geothermal and hydro, and Northland gas peakers. The 1998 Auckland CBD power crisis — when four underground cables failed within weeks of each other, leaving the city centre without power for five weeks — remains the reference event for what transmission failure looks like for a major city. Infrastructure investment since 1998 has improved resilience, but N-1 and N-2 scenarios on the main transmission corridors still pose significant risk to Auckland's electricity supply.


## The electrification challenge

Decarbonising transport and heating is both a policy objective and an accelerating market trend. If Auckland's vehicle fleet is predominantly electric by 2040, charging demand alone could require 1–2 GW of additional capacity serving the region. This is a known planning challenge with a known lead time: grid investment decisions made now determine the resilience and cost of the electricity system in 2035–2040. Acting ahead of demand is substantially cheaper than reacting to it.


---

## References



- **Electricity Authority — Wholesale and Retail Market Review 2023** (Electricity Authority (New Zealand)), 2023 — <https://www.ea.govt.nz/industry/market-oversight/>

- **Infrastructure New Zealand — State of Infrastructure Report 2023** (Infrastructure New Zealand), 2023 — <https://www.infrastructure.org.nz/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Electrification-driven electricity demand growth



- **Category:** economic
- **Timescale:** medium
- **Consensus:** mostly-agreed

#### Transmission-dependent electricity supply



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Distributed generation and battery storage

Transmission risk and electrification demand can both be addressed by building generation and storage close to Auckland's load centres: rooftop solar, grid-scale battery storage at grid injection points, and demand-side management that shifts EV charging to off-peak periods. Distributed resilience is inherently more robust than centralised supply — a battery at the substation level cannot be knocked out by a single transmission fault.

**Flagship moves:**

- Mandate solar-ready construction standards for all new residential and commercial buildings, with pre-wiring for battery storage
- Fund grid-scale battery storage (500 MW by 2030) at the major Auckland grid exit points to provide 4-hour resilience against transmission outages
- Deploy smart EV charging management across the Auckland network, shifting 80% of overnight charging to off-peak windows to flatten the demand curve

**Tensions:**

- Rooftop solar primarily benefits owner-occupiers with suitable roof orientation and sufficient income to invest; renters and apartment dwellers — who have the highest need for energy cost reduction — are largely excluded from direct solar benefits.

- Battery storage at current costs is expensive per unit of resilience; the economics improve rapidly as battery prices fall but the investment case for 2025 deployment is marginal without subsidy.


**Interventions on the system:**

- Grid-scale battery storage programme: 500 MW / 2 GWh installed at the five largest Auckland grid exit points by 2030, providing 4-hour resilience against N-1 transmission outage.
 (state variable: `grid_resilience_hours`, sign: +) (relaxes: `transmission dependency for Auckland electricity supply`)
- Smart EV charging standard: all new EV chargers installed from 2026 must be smart-capable and enrolled in the AT demand- management programme, shifting off-peak charging to reduce coincident peak demand.
 (state variable: `peak_electricity_demand`, sign: -)


#### Grid reinforcement and local generation

Distributed storage and demand management reduce but cannot eliminate Auckland's transmission dependency. Reinforcing the transmission and sub-transmission network, building new local generation (offshore wind, large-scale battery), and hardening the CBD underground cable network are the structural solutions to supply security — distributed generation supplements but does not substitute for a robust grid.

**Flagship moves:**

- Advance Transpower's Auckland capacity investment programme, including new HVDC interconnection and substation upgrades, ahead of electrification demand growth
- Progress feasibility of Northland offshore wind generation as a new local supply source reducing Auckland's transmission dependency
- Replace aging CBD underground cable infrastructure with modern high-capacity cables and N-1 redundancy on all critical feeders

**Tensions:**

- Grid reinforcement capital costs are very large and are ultimately borne by all electricity consumers through transmission charges; the cost-benefit depends on future demand scenarios that are inherently uncertain.

- New generation investment competes with distributed solar and storage for the same decarbonisation investment pool; a grid- centric approach may delay the distributed resilience benefits of a decentralised energy system.


**Interventions on the system:**

- Accelerate Transpower's Auckland 400 kV reinforcement programme, bringing forward substation upgrades by 5 years to provide N-1 security ahead of electrification demand growth.
 (state variable: `grid_resilience_hours`, sign: +) (relaxes: `aging transmission infrastructure with insufficient N-1 redundancy`)
- Fund offshore wind feasibility study and consenting programme for a 500 MW Northland offshore wind farm to provide local generation reducing transmission dependency by 2035.
 (state variable: `local_generation_share`, sign: +)


### Claims cited on this page

- **Auckland's electricity supply depends on long transmission lines from Waikato and Northland hydro and geothermal generation, making it vulnerable to transmission outages. The 1998 Auckland CBD power crisis — when four major cables failed simultaneously, blacking out the city centre for five weeks — demonstrated the fragility of the system. While resilience has improved since 1998, Auckland remains exposed to N-1 and N-2 transmission failure scenarios that could cause extended outages affecting critical infrastructure.
** — Electricity Authority — Wholesale and Retail Market Review 2023; Infrastructure New Zealand — State of Infrastructure Report 2023.
- **Electrification of Auckland's transport fleet and household heating will materially increase electricity demand over the next 20 years. If Auckland's ~700,000 vehicles are predominantly electric by 2040, charging demand alone could require 1–2 GW of additional generation and transmission capacity serving the region — roughly 20–40% above current peak demand. Managing the coincident-charging risk and funding the grid upgrades required is a material infrastructure planning challenge beginning now.
** *(confidence: medium)* — Electricity Authority — Wholesale and Retail Market Review 2023.

### Systems-model notes

*State variables:* grid_resilience_hours, local_generation_share, peak_electricity_demand.

*Constraints:* Transmission dependency: most Auckland electricity sourced from outside the region, Aging CBD cable infrastructure with limited N-1 redundancy on some feeders, Electrification demand growth will outpace current grid capacity without investment.

*Inputs:* ev_fleet_size, renewable_generation_investment, transmission_reinforcement, smart_charging_deployment.


*Feedback loops:*

- `EV adoption → peak charging demand → grid stress → outage risk → investment need`
- `Distributed generation → reduced transmission dependency → lower outage risk (resilience dividend)`


</details>

---

*Generated from `problem.auckland.infrastructure.energy_resilience` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
