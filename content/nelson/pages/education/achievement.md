---
title: "NCEA achievement gap by decile and ethnicity"
section: education
subpage: achievement
order: 1
updated: 2026-04-26
summary: >
  About 72 percent of Nelson secondary students achieve NCEA Level 2 or above, against approximately 78 percent nationally. Within that headline are large gaps: Maori students achieve at 58 percent against 80 percent for Pakeha, and decile 1-3 schools achieve at 64 percent against 82 percent at decile 9-10. Transitions to tertiary or trades remain below optimal.
status: draft
generated_from: problem.nelson.education.achievement
---

# NCEA achievement gap by decile and ethnicity

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Headline gap and its composition

Nelson's overall NCEA achievement sits modestly below the national average, but the more important pattern is the internal gap between high- and low-decile schools (claim.nelson.education.achievement_claim). The gap maps closely onto household income and accumulated material deprivation rather than onto school quality alone.


## Pathway after Year 13

Even where Level 2 is achieved, post-school pathways are thin. Only about 32 percent of Nelson secondary leavers progress directly to tertiary education, against around 48 percent nationally; many leave for university in Wellington or further south. The result is structural out-migration of the most-qualified school leavers and weak in-region labour-market signal back to schools about pathway value.


---


## Drivers

The following structural drivers contribute to this problem.


### Household material deprivation and school-readiness gap



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Tertiary-pathway thinness and out-migration of leavers



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 1

A response strategy addressing education challenges.

**Flagship moves:**

- Implement evidence-based education policy in Nelson
- Increase investment in education services and infrastructure
- Build cross-sector partnerships to address education challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for education (state variable: `education_outcome_index`, sign: +)
- Secondary intervention for education (state variable: `education_service_access`, sign: +)


### Response: Camp 2

A response strategy addressing education challenges.

**Flagship moves:**

- Implement evidence-based education policy in Nelson
- Increase investment in education services and infrastructure
- Build cross-sector partnerships to address education challenges

**Tensions:**

- Implementation requires sustained political will and cross-sector coordination.
- Resource constraints may limit the pace of change.

**Interventions on the system:**

- Primary intervention for education (state variable: `education_outcome_index`, sign: +)
- Secondary intervention for education (state variable: `education_service_access`, sign: +)


---

## Claims cited on this page

- **NCEA achievement in Nelson schools shows mixed outcomes. 2023 MOE data reports that 72% of Nelson secondary students achieved NCEA Level 2 or above, compared to 78% nationally. Achievement gaps are significant by decile and ethnicity: Maori students achieve Level 2 at 58% vs. 80% for Pakeha; students in decile 1-3 schools achieve at 64% vs. 82% in decile 9-10 schools. Transitions to tertiary or trades remain below optimal.** [value: 72 percent achieving NCEA Level 2 or above; 2023] — Education Outcomes Nelson Region 2023.

---

## Further reading


- **Education Outcomes Nelson Region 2023** — Ministry of Education (Ministry of Education), 2023 — <https://www.education.govt.nz>


---

## Technical notes

*State variables:* ncea_l2_pass_rate_pct, decile_pass_rate_gap_pp, post_school_tertiary_progression_pct.

*Constraints:* specialist_teacher_supply, deprivation_concentration.

*Inputs:* per_pupil_funding, school_workforce_supply, household_income.


*Feedback loops:*

- `Out-migration-signal feedback: high-achieving leavers exit the region for university, weakening the local skilled-labour pool and dampening aspirational signals back into schools.`


---

*Generated from `problem.nelson.education.achievement` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
