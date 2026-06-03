---
title: "Outcome gaps driven by distance to specialist care"
section: health
subpage: health_outcomes
order: 1
updated: 2026-04-26
summary: >
  Life expectancy in Tasman is around 80.2 years, just below the national 81.1, with a 3.9-year gap between Māori and non-Māori. Avoidable mortality runs roughly 15 percent above the national benchmark, driven heavily by delays in accessing specialist services from Golden Bay and Murchison.
status: draft
generated_from: problem.tasman.health.health_outcomes
---

# Outcome gaps driven by distance to specialist care

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Distance is a clinical variable

When the nearest emergency, surgical, and maternity capacity is at Nelson Hospital, the time-from-onset to treatment for stroke, cardiac, obstetric and trauma events is longer for residents of Mohua and Murchison than for residents of Richmond. That time difference shows up as worse population-level outcomes (claim.tasman.health.health_outcomes_claim).


## Equity layered on top of geography

The 3.9-year Māori life-expectancy gap is not explained by rurality alone — it tracks national patterns of deprivation, chronic-disease burden, and primary-care access. Within Tasman, those drivers are concentrated in Motueka, Murchison, and parts of Mohua.


---


## Drivers

The following structural drivers contribute to this problem.


### Distance to Nelson Hospital



- **Category:** physical
- **Timescale:** permanent
- **Consensus:** consensus

### Rural clinician recruitment and retention deficit



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing health challenges.

**Flagship moves:**

- Implement evidence-based health policy in Tasman
- Increase investment in health services and infrastructure
- Build cross-sector partnerships to address health challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for health (state variable: `health_outcome_index`, sign: +)
- Secondary intervention for health (state variable: `health_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing health challenges.

**Flagship moves:**

- Implement evidence-based health policy in Tasman
- Increase investment in health services and infrastructure
- Build cross-sector partnerships to address health challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for health (state variable: `health_outcome_index`, sign: +)
- Secondary intervention for health (state variable: `health_service_access`, sign: +)


---

## Claims cited on this page

- **Health NZ Tasman (2023) shows life expectancy at birth is 80.2 years (national average 81.1). Māori life expectancy is 76.3 years, a 3.9-year gap. Avoidable mortality is 15% higher than national benchmark, driven by delays in accessing specialist services from Golden Bay and Murchison.** [value: 80.2 years life expectancy; 2023] — Health Outcomes Tasman Region 2023; Stats NZ Census 2023.

---

## Further reading


- **Health Outcomes Tasman Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* life_expectancy_at_birth, avoidable_mortality_rate.

*Constraints:* geographic_distance_to_nelson_hospital, workforce_supply.

*Inputs:* primary_care_access_density, specialist_referral_throughput.


*Feedback loops:*

- `Worse outcomes increase the cost of secondary and tertiary care relative to primary, which diverts funding away from the primary-care services that would prevent the secondary load.`


---

*Generated from `problem.tasman.health.health_outcomes` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
