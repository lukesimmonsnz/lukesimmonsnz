---
title: "Secondary Education Attainment & Transition"
section: education
subpage: secondary
order: 2
updated: 2026-04-26
summary: >
  Canterbury secondary schools show wide variance in NCEA pass rates (55-95% by school/decile). School engagement is declining in rural and high-deprivation areas; truancy rates in East Christchurch exceed 15%. Transitions to tertiary/employment are unequal; many students from decile 9-10 schools enter low-wage or jobless pathways.

status: draft
generated_from: problem.canterbury.education.secondary
---

# Secondary Education Attainment & Transition

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Disengagement in high-deprivation schools

Secondary students in decile 9-10 schools often lack consistent teacher relationships due to high turnover. Truancy increases year 11-13. NCEA pass rates reflect both student capacity and school support differential.


---


## Drivers

The following structural drivers contribute to this problem.


### School Funding Equity & Decile-Based Distribution



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

### Teacher Recruitment & Retention Challenges (Rural)



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Weighted Equity-Based School Funding

Increasing funding to high-decile schools (weighted by student need) reduces achievement gaps and improves outcomes for disadvantaged students.

**Flagship moves:**

- Key intervention for Weighted Equity-Based School Funding

**Tensions:**

- Implementation complexity in multi-stakeholder environment

**Interventions on the system:**

- Increasing funding to high-decile schools (weighted by student need) reduces achievement gaps and improves outcomes for disadvantaged students. (state variable: `outcome_metric`, sign: +) (relaxes: `constraint_type`)


---

## Claims cited on this page

- **Average ECE fees in Canterbury are NZD 165/week (2023); for single-income households below $80K, fees consume 15-20% of household income. Early childhood participation rates are 5-8 percentage points below national average.** [value: 35 percentage point gap; 2023] *(confidence: medium)* — Ministry of Education—Canterbury Education Achievement 2023.
- **Average ECE fees in Canterbury are NZD 165/week (2023); for single-income households below $80K, fees consume 15-20% of household income. Early childhood participation rates are 5-8 percentage points below national average.** [value: 16.5 percent; 2023] *(confidence: medium)* — Ministry of Education—Canterbury Education Achievement 2023.

---

## Further reading


- **Ministry of Education—Canterbury Education Achievement 2023** (Ministry of Education), 2023 — <https://www.education.govt.nz/>


---

## Technical notes

*State variables:* ncea_level_2_attainment_rate_by_school, school_truancy_rate_by_school_decile, student_engagement_index, secondary_to_tertiary_transition_rate.

*Constraints:* teacher_recruitment_and_retention, school_funding_equity.

*Inputs:* school_teaching_capacity, school_engagement_culture, family_education_aspirations.


*Feedback loops:*

- `Dynamic feedback mechanisms drive secondary education attainment & transition.`


---

*Generated from `problem.canterbury.education.secondary` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
