---
title: "Tertiary education access and completion"
section: education
subpage: tertiary-access
order: 2
updated: 2026-04-26
summary: >
  Tertiary education participation in Hawke's Bay is below national average. Cost barriers, limited vocational pathway support, and distance to universities (Massey in Palmerston North, 1.5 hours away) are barriers. Living cost support is inadequate.
status: draft
generated_from: problem.hawkes_bay.education.tertiary_access
---

# Tertiary education access and completion

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Participation

Tertiary education participation in Hawke's Bay is approximately 35%, compared to 42% nationally. Pacific student participation is 18%.


## Cost Barrier

Students attending Massey University in Palmerston North face minimum living costs of $25,000 per year (rent, food, transport). Student loan debt averages $28,000 at graduation.


---


## Drivers

The following structural drivers contribute to this problem.


### School resource allocation inequity



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Literacy and numeracy support programmes

Literacy and numeracy support programmes is the primary strategy.

**Flagship moves:**

- Implement Literacy and numeracy support programmes across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Literacy and numeracy support programmes intervention (state variable: `literacy_support_index`, sign: +) (relaxes: `literacy_support_constraint`)


---

## Claims cited on this page

- **Tertiary education participation in Hawke's Bay (age 18-25) is 35%, substantially below the national average (48%). Cost barriers, limited tertiary provision beyond Wairarapa Institute of Technology, and geographic remoteness (especially Wairoa) restrict access. School-leavers often migrate to Wellington/Auckland for tertiary study, creating brain drain and limited return migration to regional jobs.** [value: 35 percent participation; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* tertiary_participation_rate_percent, tertiary_completion_rate_percent.

*Constraints:* local_tertiary_provision, vocational_training_availability.

*Inputs:* student_loan_burden, living_cost_barriers.


*Feedback loops:*

- `High loan debt deters participation; low participation limits skill supply; wage suppression follows; tertiary access remains unaffordable.`


---

*Generated from `problem.hawkes_bay.education.tertiary_access` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
