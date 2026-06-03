---
title: "Secondary-to-employment transition failures in Wellington"
section: education
subpage: secondary-transition
order: 3
updated: 2026-04-26
summary: >
  A significant proportion of Wellington's secondary school leavers — concentrated in Porirua and Hutt Valley — are not in employment, education, or training (NEET) within 12 months of leaving school. Vocational pathway provision is insufficient for students who do not follow academic routes.
status: draft
generated_from: problem.wellington.education.secondary_transition
---

# Secondary-to-employment transition failures in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## NEET concentration

The proportion of 15–24-year-olds not in employment, education, or training (NEET) is substantially higher in Porirua and Hutt Valley than in Wellington City, reflecting school disengagement, limited local employment options, and inadequate transition support (claim.wellington.education.neet_rate_wellington).


## Vocational pathway gap

Wellington's secondary education system offers limited vocational pathway provision relative to the academic track, leaving students whose strengths lie in trade and technical areas without a clear post-school route (claim.wellington.education.vocational_pathway_gap).


---


## Drivers

The following structural drivers contribute to this problem.


### Insufficient vocational education pathways at secondary level



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** mostly-agreed

### Multiple school disengagement drivers in high-deprivation areas



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Chronic Absenteeism Intervention

Targeted attendance support for chronically absent students through social workers and family liaison reduces disengagement cascades.

**Flagship moves:**

- School attendance officers for all decile 1–3 schools in Wellington
- Family-school liaison workers funded in highest-absence schools
- Trauma-informed restorative practice to replace punitive suspension responses

**Tensions:**

- Attendance pressure without addressing underlying causes (housing instability, family harm) is ineffective
- Punitive suspension removal requires adequate alternative provision for disrupted classrooms

**Interventions on the system:**

- Deploy attendance support officers in 20 highest-absence Wellington schools with family liaison mandate (state variable: `chronic_absenteeism_rate`, sign: -)


### Vocational and Trades Pathway Expansion

Expanding trades and vocational pathways in Wellington secondary schools reduces disengagement and improves employment outcomes for non-academic students.

**Flagship moves:**

- Trades Academy programme in all Porirua and Hutt secondary schools
- Employer-led gateway programme with Wellington construction sector
- NCEA vocational pathway endorsement parity with academic endorsements

**Tensions:**

- Vocational streaming risks entrenching class and ethnic divisions in education pathways
- Employer demand for gateway students is cyclical and unreliable as a planning basis

**Interventions on the system:**

- Fund Trades Academy expansion to 600 additional Wellington student places across construction, health, and digital sectors (state variable: `secondary_engagement_rate`, sign: +)


---

## Claims cited on this page

- **The proportion of 15–24-year-olds not in employment, education, or training (NEET) is substantially higher in Porirua and Hutt Valley than in Wellington City, reflecting school disengagement, limited local employment options, and inadequate secondary-to-employment transition support.** *(confidence: medium)* — Census 2023: Wellington Regional Profile; Education Counts: Wellington Region Achievement Data 2023.
- **Wellington's secondary education system offers limited vocational pathway provision relative to the academic track, leaving students whose strengths lie in trade and technical areas without a clear post-school education or employment route.** *(confidence: medium)* — Education Counts: Wellington Region Achievement Data 2023.

---

## Further reading


- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>

- **Education Counts: Wellington Region Achievement Data 2023** (Ministry of Education), 2023 — <https://www.educationcounts.govt.nz/statistics>


---

## Technical notes

*State variables:* neet_rate_age_15_24, vocational_qualification_completion_rate.

*Constraints:* mismatch_of_qualification_supply_to_employer_demand.

*Inputs:* employer_apprenticeship_take_up, alternative_education_provision.


*Feedback loops:*

- `Disengagement persistence: students who leave secondary school without qualifications face significant barriers to re-entry into education and have lower lifetime earnings trajectories.`


---

*Generated from `problem.wellington.education.secondary_transition` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
