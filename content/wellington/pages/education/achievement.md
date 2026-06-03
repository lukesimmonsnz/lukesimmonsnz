---
title: "Education achievement gaps in Wellington"
section: education
subpage: achievement
order: 1
updated: 2026-04-26
summary: >
  Wellington's education system produces strongly divergent outcomes across socioeconomic and geographic lines. Students in Porirua and Hutt Valley schools — serving high-deprivation communities — achieve substantially below Wellington City averages at NCEA Level 2. The achievement gap reflects school resourcing differentials, persistent absenteeism, financial pressure to work, and the compounding effect of household poverty on out-of-school study conditions.
status: draft
generated_from: problem.wellington.education.achievement
---

# Education achievement gaps in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## NCEA attainment gap

Māori students in Wellington achieve NCEA Level 2 at approximately 74%, compared to 90% for European students — a persistent gap that has not significantly closed over the past decade despite targeted interventions (claim.wellington.education.ncea_l2_maori_gap).


## Pacific achievement gap

Pacific students in Wellington, concentrated in Porirua schools, face similar achievement gaps compounded by language factors and school-community cultural mismatch (claim.wellington.education.pacific_achievement_gap).


---


## Drivers

The following structural drivers contribute to this problem.


### Inequitable teacher quality distribution



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Poverty and reduced learning readiness



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Equity-Weighted School Resourcing

Directing additional teacher and resource funding to high-deprivation schools in Porirua and Hutt Valley is the most direct lever for closing the achievement gap.

**Flagship moves:**

- Implement equity index funding with 1.5× teacher allocation for decile 1–3 schools
- Specialist literacy and numeracy teacher deployment in lowest-performing schools
- Community education hubs open outside school hours in high-deprivation areas

**Tensions:**

- Teacher allocation without addressing teacher supply does not produce actual teachers
- Equity funding is contested by suburban schools who perceive disadvantage

**Interventions on the system:**

- Implement equity index teacher ratio of 1:15 for all Porirua and Hutt Valley decile 1–3 schools (state variable: `ncea_l2_attainment_low_decile`, sign: +) (relaxes: `teacher_resource_inequity`)


### Kaupapa Māori and Bilingual Education Expansion

Expanding te reo Māori immersion and kaupapa Māori schooling options improves Māori educational achievement and cultural identity outcomes.

**Flagship moves:**

- Establish 2 new kura kaupapa in Porirua and Hutt Valley
- Bilingual class stream in all Porirua primary schools
- Te reo teacher training scholarships at Victoria University of Wellington

**Tensions:**

- Qualified kaiako supply is severely constrained; expansion outpaces teacher availability
- Kura expansion requires capital investment competing with mainstream school rolls

**Interventions on the system:**

- Fund 2 new kura kaupapa in Porirua and Lower Hutt with Ministry of Education capital grant (state variable: `maori_educational_attainment`, sign: +)


---

## Claims cited on this page

- **Māori students in Wellington achieve NCEA Level 2 at approximately 74%, compared to approximately 90% for European students — a persistent gap of 16 percentage points that has not significantly closed over the past decade despite targeted interventions.** [value: 74 percent NCEA Level 2 attainment (Māori); 2022-2023] *(confidence: medium)* — Education Counts: Wellington Region Achievement Data 2023.
- **Students in Porirua schools — where socioeconomic disadvantage, linguistic diversity, and school-community fit challenges are concentrated — face NCEA Level 2 achievement gaps compounded by financial barriers, school resourcing differentials, and insufficient pastoral support for students managing employment and family responsibilities alongside study.** *(confidence: medium)* — Education Counts: Wellington Region Achievement Data 2023.

---

## Further reading


- **Education Counts: Wellington Region Achievement Data 2023** (Ministry of Education), 2023 — <https://www.educationcounts.govt.nz/statistics>


---

## Technical notes

*State variables:* ncea_l2_attainment_rate_maori, achievement_gap_pakeha_maori.

*Constraints:* poverty_and_learning_readiness, teacher_supply_to_high_need_schools.

*Inputs:* school_resource_equity, teacher_quality_distribution.


*Feedback loops:*

- `School-sorting amplification: school choice mechanisms allow higher-income families to concentrate in higher-decile schools; lower-decile schools face increasing resource and reputational disadvantage.`


---

*Generated from `problem.wellington.education.achievement` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
