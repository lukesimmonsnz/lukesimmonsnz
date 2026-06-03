---
title: "State-highway closure exposure on SH6 and SH60"
section: transport
subpage: connectivity_3
order: 3
updated: 2026-04-26
summary: >
  SH6 is the sole north-south road route, with sections between Nelson and Blenheim (notably the Whangamoa and Rai saddles) prone to closure from slip, snow, and accident. SH60 to Tasman traverses unstable terrain east of Ruby Bay and has had 4-week closures in the last decade. Alternative routes add more than 90 minutes. Climate change is projected to increase closure frequency and duration, with 2-4 major disruptions annually projected by 2050.
status: draft
generated_from: problem.nelson.transport.connectivity_3
---

# State-highway closure exposure on SH6 and SH60

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Single-corridor risk

The road network has the same single-corridor character as Wellington's coastal SH1, but without the rail backup (claim.nelson.transport.connectivity_3_claim). A single closure event can isolate Nelson from the ferry terminus in Picton and from the Christchurch supply chain simultaneously.


## Resilience investment lag

Specific resilience projects (slip-prone section stabilisation, alternative-route formalisation) sit on the Waka Kotahi pipeline but compete against higher-volume metro projects. Climate-altered closure frequency is starting to shift that calculus, but slowly.


---


## Drivers

The following structural drivers contribute to this problem.


### Topographic and demographic limits on active and public transport



- **Category:** physical
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


---

## Claims cited on this page

- **State Highway vulnerability in Nelson creates resilience risk. SH6 is the sole north-south route; sections between Nelson and Blenheim (particularly Wither Hills Pass) are prone to closure from avalanche, slips, and snow in winter. SH60 (to Tasman) traverses unstable terrain east of Ruby Bay; slips have caused 4-week closures in the last decade. Alternative routes add >90 minutes to journeys. Climate change will increase closure frequency and duration; Waka Kotahi assessments project 2–4 major disruptions annually by 2050. Freight corridors and emergency access are vulnerable; resilience investment in alternative routing or rail is uncertain.** [value: 4 week-long closures on SH60 over past decade; 2014-2024] *(confidence: medium)* — Waka Kotahi State Highway Network – Nelson Region 2023.

---

## Further reading


- **Waka Kotahi State Highway Network – Nelson Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>


---

## Technical notes

*State variables:* sh6_annual_closure_hours, sh60_annual_closure_hours, alt_route_detour_minutes.

*Constraints:* topography, alternative_route_availability.

*Inputs:* nzta_resilience_capex, climate_event_frequency.


*Feedback loops:*

- `Closure-investment feedback: each closure event raises political pressure for resilience investment, but rebuild-to-original is faster than upgrade, so the same vulnerability is repeatedly restored rather than fixed.`


---

*Generated from `problem.nelson.transport.connectivity_3` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
