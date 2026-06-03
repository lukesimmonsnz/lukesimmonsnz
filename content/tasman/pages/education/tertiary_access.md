---
title: "Direct tertiary progression below national rate"
section: education
subpage: tertiary_access
order: 4
updated: 2026-04-26
summary: >
  Around 28 percent of Tasman school leavers progress directly to tertiary study, compared with a national 46 percent. The nearest university campuses (Massey Albany, University of Canterbury) are three-plus hours away; the cost of relocation is a meaningful filter on lower-income families.
status: draft
generated_from: problem.tasman.education.tertiary_access
---

# Direct tertiary progression below national rate

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Tertiary participation requires relocation

There is no university campus inside Tasman. Nelson Marlborough Institute of Technology offers vocational pathways from a Nelson base; degree study requires moving to Christchurch, Wellington, or further. Relocation cost — bond, rent, separation from work and whānau — sits between secondary completion and tertiary enrolment (claim.tasman.education.tertiary_access_claim).


## Filter by household income

Households able to fund a relocated student are disproportionately higher-income. The same regional gap therefore acts as a class filter on tertiary access, reproducing income inequality across generations rather than narrowing it.


---


## Drivers

The following structural drivers contribute to this problem.


### Tertiary-relocation cost as a class filter



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Response: Camp 2

A response strategy addressing education challenges.

**Flagship moves:**

- Implement evidence-based education policy in Tasman
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

- **Only 28% of Tasman school leavers progress directly to tertiary study (2023), below national rate of 46%. Nearest university campuses (Massey Albany, University of Canterbury) are 3+ hours away; cost of relocation excludes lower-income families from study pathways.** [value: 28 percent direct tertiary progression; 2023] *(confidence: medium)* — Education Outcomes Tasman Region 2023; Stats NZ Census 2023.

---

## Further reading


- **Education Outcomes Tasman Region 2023** — Ministry of Education (Ministry of Education), 2023 — <https://www.education.govt.nz>

- **Stats NZ Census 2023** — Stats NZ / Tatauranga Aotearoa (Statistics New Zealand), 2023 — <https://www.stats.nz/tools/census>


---

## Technical notes

*State variables:* direct_tertiary_progression_rate, school_leaver_destination_distribution.

*Constraints:* no_local_university_campus, relocation_cost_filter.

*Inputs:* regional_scholarship_capacity, online_degree_pathway_enrolment.


*Feedback loops:*

- `Out-migration of tertiary cohorts thins the local graduate workforce, which reduces graduate-level local employers, which reinforces the case for relocation.`


---

*Generated from `problem.tasman.education.tertiary_access` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
