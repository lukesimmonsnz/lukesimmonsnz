---
title: "Education achievement and attainment gaps"
section: education
subpage: achievement
order: 1
updated: 2026-04-26
summary: >
  Hawke's Bay students achieve NCEA levels and tertiary entry at rates below the national average. Significant gaps exist between high-deprivation and more affluent schools, reflecting resource differentials, teacher turnover, and the compounding effect of household poverty on study conditions. Cyclone Gabrielle disrupted schooling in 2023, with high-deprivation communities sustaining the most prolonged disruption.
status: draft
generated_from: problem.hawkes_bay.education.achievement
---

# Education achievement and attainment gaps

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## NCEA Attainment

NCEA Level 2 attainment in Hawke's Bay is approximately 78%, compared to 85% nationally. Māori attainment is 65%.


## Tertiary Entry

University entrance qualification rates in Hawke's Bay are approximately 32%, compared to 42% nationally. Pacific student entry rates are particularly low at 15%.


---


## Drivers

The following structural drivers contribute to this problem.


### Childhood poverty limiting learning readiness



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### School resource allocation inequity



- **Category:** institutional
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

- **NCEA Level 2 attainment in Hawke's Bay stands at 78%, below the national average (84%), with widest gaps in Hastings and Wairoa. Curriculum delivery constraints (teacher shortages, limited STEM provision) and socioeconomic stress (food insecurity, housing instability, family violence) directly correlate with lower Level 2 completion rates, particularly among Māori and Pasifika students.** [value: 78 percent; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Maori NCEA Level 3 attainment in Hawke's Bay is 65%, below the national Maori average of 72%. Hastings and Wairoa schools report elevated absenteeism; teacher recruitment shortages in rural areas compound curriculum delivery gaps, particularly in mathematics and science. Socioeconomic deprivation and family stress correlate with lower qualification rates, limiting career pathways for Maori school leavers.** [value: 65 percent NCEA Level 3 attainment (Maori); 2023] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* ncea_l2_attainment_rate_percent, achievement_gap_maori_pakeha_percentage_points.

*Constraints:* school_resource_equity, teacher_supply_to_high_need_schools.

*Inputs:* poverty_and_learning_readiness, teacher_quality_distribution.


*Feedback loops:*

- `Achievement gaps limit tertiary access; career opportunity gaps follow; intergenerational poverty repeats.`


---

*Generated from `problem.hawkes_bay.education.achievement` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
