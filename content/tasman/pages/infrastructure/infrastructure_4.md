---
title: "Takaka Hill resilience and closure exposure"
section: infrastructure
subpage: infrastructure_4
order: 4
updated: 2026-04-26
summary: >
  SH60 over the Takaka Hill — Mohua's only road link — is vulnerable to slips, washouts, and fog. Twelve major closures occurred between 2018 and 2023, isolating Golden Bay for two to five days each. Waka Kotahi has scheduled NZD 18 million of resilience and real-time hazard monitoring works for 2024-2026.
status: draft
generated_from: problem.tasman.infrastructure.infrastructure_4
---

# Takaka Hill resilience and closure exposure

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Closure is not a tail event

Twelve major closures in five years means SH60 over the Takaka Hill was unusable for at least 24 days in that window — likely materially more once short closures and single-lane operations are included (claim.tasman.infrastructure.infrastructure_4_claim).


## Resilience investment versus alternative-route investment

The current Waka Kotahi programme strengthens the existing alignment rather than providing redundancy. A second road into Mohua is geographically and fiscally implausible, so resilience-on-the-only-route is the realistic policy lever — but leaves residual closure risk that resilience cannot fully eliminate.


---


## Drivers

The following structural drivers contribute to this problem.


### Single-route exposure to weather and geology



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing infrastructure challenges.

**Flagship moves:**

- Prioritise three-waters infrastructure renewal in Tasman urban centres
- Establish a multi-year capital works programme for wastewater and stormwater upgrades
- Apply for central government infrastructure co-funding to supplement council rates

**Tensions:**

- Infrastructure renewal requires significant capital expenditure that strains small council budgets.
- Prioritising upgrades may delay other community investment needs.

**Interventions on the system:**

- Accelerate infrastructure renewal investment in Tasman (state variable: `infrastructure_condition_index`, sign: +)
- Prioritise water and wastewater upgrades (state variable: `service_coverage`, sign: +)


---

## Claims cited on this page

- **Takaka Hill (SH60 to Golden Bay) is prone to slips, washouts, and fog; 12 major closures occurred 2018-2023, isolating Golden Bay for 2-5 days per event. Waka Kotahi is upgrading drainage and installing real-time hazard monitoring; resilience work is scheduled 2024-2026 at NZD 18 million investment.** [value: 12 major road closures (2018-2023); 2018-2023] — Waka Kotahi State Highway Network – Tasman Region 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Waka Kotahi State Highway Network – Tasman Region 2023** — Waka Kotahi NZ Transport Agency (Waka Kotahi), 2023 — <https://www.nzta.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* sh60_major_closure_count, resilience_capex_completed.

*Constraints:* no_alternative_road_alignment, geological_terrain_instability.

*Inputs:* waka_kotahi_resilience_funding, real_time_hazard_monitoring_coverage.


*Feedback loops:*

- `Closure events accelerate population thinning and service withdrawal in Mohua, which weakens the demand case for the resilience investment that would reduce future closures.`


---

*Generated from `problem.tasman.infrastructure.infrastructure_4` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
