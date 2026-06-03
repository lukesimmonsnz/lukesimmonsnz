---
title: "Family violence load with thin specialist support"
section: crime
subpage: family_violence
order: 2
updated: 2026-04-26
summary: >
  Health NZ Tasman reports family-violence notifications up around 18 percent in 2023 against 2022. Golden Bay and rural Tasman have limited access to specialist support; referral times to regional services in Nelson exceed four weeks.
status: draft
generated_from: problem.tasman.crime.family_violence
---

# Family violence load with thin specialist support

<p class="horizon-band">Analysis horizon: 10yr</p>



## Notifications rising faster than capacity

An 18 percent year-on-year rise in notifications outstrips any plausible workforce expansion at specialist-services level. Existing wait times — already over four weeks in Mohua — lengthen further (claim.tasman.crime.family_violence_claim).


## Rural geography raises the cost of support

Specialist support assumes a face-to-face service, often weekly, often on short notice. For Mohua and Murchison residents, that cost is the Takaka Hill or the drive to Nelson. The combination of distance and wait time produces de facto exclusion from services that exist on paper.


---


## Drivers

The following structural drivers contribute to this problem.


### Low-density policing geography



- **Category:** physical
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing crime challenges.

**Flagship moves:**

- Implement evidence-based crime policy in Tasman
- Increase investment in crime services and infrastructure
- Build cross-sector partnerships to address crime challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for crime (state variable: `crime_outcome_index`, sign: +)
- Secondary intervention for crime (state variable: `crime_service_access`, sign: +)


---

## Claims cited on this page

- **Health NZ Tasman (2023) reports family violence notifications increased 18% in 2023 vs 2022. Golden Bay and rural Tasman have limited access to specialist support; referral times to regional services (Nelson) exceed 4 weeks.** [value: 18 percent increase; 2023] *(confidence: medium)* — Health Outcomes Tasman Region 2023; Tasman District Council Annual Plan 2024.

---

## Further reading


- **Health Outcomes Tasman Region 2023** — Health New Zealand (Health New Zealand), 2023 — <https://www.health.govt.nz>

- **Tasman District Council Annual Plan 2024** — Tasman District Council (Tasman District Council), 2024 — <https://www.tasman.govt.nz>


---

## Technical notes

*State variables:* fv_notification_rate, specialist_referral_wait_weeks.

*Constraints:* rural_service_economics, client_safety_face_to_face_requirements.

*Inputs:* specialist_workforce_capacity, telehealth_specialist_provision.


*Feedback loops:*

- `Long waits deter help-seeking, which shifts presentation to crisis points, which raises the cost of intervention per case.`


---

*Generated from `problem.tasman.crime.family_violence` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
