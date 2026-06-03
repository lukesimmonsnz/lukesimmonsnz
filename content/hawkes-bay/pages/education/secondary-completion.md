---
title: "Secondary school completion and engagement"
section: education
subpage: secondary-completion
order: 2
updated: 2026-04-26
summary: >
  Secondary school retention and completion in Hawke's Bay is below the national average. School disengagement is concentrated in high-deprivation communities, where financial pressure to work, unstable housing, and limited vocational pathway visibility contribute to early leaving. Alternative pathways and trades academies are under-resourced relative to need.
status: draft
generated_from: problem.hawkes_bay.education.secondary_completion
---

# Secondary school completion and engagement

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Completion Rate

Secondary school completion in Hawke's Bay is approximately 81%, compared to 87% nationally. Māori completion is 68%.


## Disengagement

Student suspension rates in Hawke's Bay are 8 per 1,000 students, above the national rate of 6 per 1,000. Māori students represent 60% of suspensions despite being 35% of the student population.


---


## Drivers

The following structural drivers contribute to this problem.


### Childhood poverty limiting learning readiness



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Equity-based school resource allocation

Allocating higher per-student funding to high-deprivation schools and expanding support services narrows achievement gaps.

**Flagship moves:**

- Increase Ministry of Education per-student funding to high-deprivation schools in Flaxmere by 30% over 5 years
- Employ additional teacher aides, reading recovery specialists, and school counsellors in low-decile schools
- Provide scholarships and laptop support for low-income students

**Tensions:**

- Higher funding for disadvantaged schools may be seen as unfair by affluent communities
- Funding increases may not yield achievement gains without complementary teacher quality improvements

**Interventions on the system:**

- Increase per-student funding for high-deprivation schools to match top decile schools (state variable: `per_student_resource_equity`, sign: +)
- Employ additional support staff in low-decile schools (state variable: `school_support_service_availability`, sign: +)


---

## Claims cited on this page

- **Secondary school completion in Hawke's Bay is 81%, below the national average (86%). Hastings and Wairoa schools struggle with student absenteeism (25-30% chronic absence in some schools); school-to-employment transitions are weak, with limited youth apprenticeship pathways. Cyclone Gabrielle disruptions (2023) delayed school operations and assessment schedules in rural areas.** [value: 81 percent completion; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* school_completion_rate_percent, student_suspension_rate_per_1000.

*Constraints:* alternative_education_availability, school_belonging_and_culture.

*Inputs:* student_poverty_and_stress, limited_vocational_pathways.


*Feedback loops:*

- `Disengagement leads to early leaving; limited skills reduce job prospects; unemployment drives reoffending; school engagement investment seems pointless.`


---

*Generated from `problem.hawkes_bay.education.secondary_completion` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
