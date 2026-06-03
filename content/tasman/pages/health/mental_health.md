---
title: "Rural mental-health access lag and elevated suicide rate"
section: health
subpage: mental_health
order: 2
updated: 2026-04-26
summary: >
  Mental-health service utilisation in Tasman runs at 8.2 percent of the population, slightly below the national 9.1 percent — but the gap is not a sign of better mental health. Referral wait times in Golden Bay routinely exceed eight weeks, and the Tasman suicide rate of 16.4 per 100,000 sits above the national 15.1.
status: draft
generated_from: problem.tasman.health.mental_health
---

# Rural mental-health access lag and elevated suicide rate

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Lower utilisation, worse outcomes

When access is harder, fewer people present for help and the people who do present do so later. The combination of below-average utilisation and above-average suicide rate is consistent with a service-access deficit rather than a population that needs less support (claim.tasman.health.mental_health_claim).


## Rurality concentrates the access gap

Specialist mental-health capacity is centralised in Nelson; for Mohua and Murchison residents that means a 90-to-120-minute round trip on top of the wait. Eight-week-plus referral times in Golden Bay cannot be closed by telehealth alone where broadband remains patchy.


---


## Drivers

The following structural drivers contribute to this problem.


### Distance to Nelson Hospital



- **Category:** physical
- **Timescale:** permanent
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


---

## Claims cited on this page

- **Health NZ Tasman (2023) documents mental health service utilisation at 8.2% of population, vs national average 9.1%. However, referral wait times exceed 8 weeks in Golden Bay; rural isolation and limited counsellor availability are barriers. Suicide rate stands at 16.4 per 100,000, above national rate of 15.1.** [value: 16.4 suicides per 100,000; 2023] *(confidence: medium)* — Health Outcomes Tasman Region 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Health Outcomes Tasman Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* mental_health_referral_wait_weeks, suicide_rate_per_100k.

*Constraints:* centralised_service_geography, broadband_reach.

*Inputs:* rural_mental_health_workforce, telehealth_capacity.


*Feedback loops:*

- `Long waits deter presentation, which keeps demand statistics low and weakens the case for additional rural capacity.`


---

*Generated from `problem.tasman.health.mental_health` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
