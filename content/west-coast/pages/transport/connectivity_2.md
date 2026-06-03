---
title: "Problem: Connectivity 2"
section: transport
subpage: connectivity_2
order: 2
updated: 2026-04-26
summary: >
  Description of connectivity_2 in west-coast.
status: draft
generated_from: problem.west_coast.transport.connectivity_2
---

# Problem: Connectivity 2

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Transport challenge

Problem: Connectivity 2 is a key dimension of the broader transport challenge facing the region.


---


## Drivers

The following structural drivers contribute to this problem.


### Driver: Driver 1



- **Category:** institutional
- **Timescale:** long
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


### Pass Route Resilience and Emergency Access

West Coast communities need guaranteed road access via alpine passes year-round; NZTA investment in pass resilience and alternative transport is a strategic national priority.

**Flagship moves:**

- Upgrade weather resilience of Arthur's Pass SH73, Lewis Pass SH7, and Haast Pass SH6
- Develop contingency air freight and passenger access for extended closure events
- Establish real-time pass condition monitoring and early warning systems

**Tensions:**

- Full climate-proofing of alpine passes is technically and financially prohibitive
- Some level of weather closure is unavoidable given geography

**Interventions on the system:**

- Fund West Coast alpine highway resilience upgrades (state variable: `alpine_pass_closure_days`, sign: -)


---

## Claims cited on this page

- **Haast Pass (State Highway 6) is the only road connection between West Coast and Otago/Southland regions. The pass experiences frequent closures from avalanche risk, rockfall, and slips (average 3-5 days/year closed). Winter conditions are severe. Alternate route via Gore-Greymouth is 4+ hours longer. Haast Pass closure isolates West Coast economically and socially from the south. Infrastructure resilience and alternate route options are critically needed but underfunded.** [value: 4 days closure per year (average); 2010-2024] *(confidence: medium)* — Waka Kotahi State Highway Network – West Coast Region 2023; West Coast Regional Council Annual Plan 2024.

---

## Further reading


- **Waka Kotahi State Highway Network – West Coast Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>

- **West Coast Regional Council Annual Plan 2024** — West Coast Regional Council (West Coast Regional Council), 2024 — <https://www.wcrc.govt.nz>


---

## Technical notes

*State variables:* transport_accessibility.

*Constraints:* implementation_capacity.



---

*Generated from `problem.west_coast.transport.connectivity_2` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
