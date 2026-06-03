---
title: "Chronic disease prevalence and management"
section: health
subpage: chronic-disease
order: 2
updated: 2026-04-26
summary: >
  Type 2 diabetes, cardiovascular disease, and respiratory disease are prevalent in Hawke's Bay at rates above national average. Obesity and smoking are risk factors. Primary care capacity for disease management is constrained.
status: draft
generated_from: problem.hawkes_bay.health.chronic_disease
---

# Chronic disease prevalence and management

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Diabetes

Type 2 diabetes prevalence in Hawke's Bay is approximately 8%, compared to 6% nationally. Māori prevalence is 15%.


## Cardiovascular Disease

Cardiovascular disease mortality in Hawke's Bay is approximately 150 per 100,000, compared to 120 nationally. Risk factor management in primary care is suboptimal.


---


## Drivers

The following structural drivers contribute to this problem.


### Limited preventive care and health promotion investment



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Primary care service expansion

Primary care service expansion is the primary strategy.

**Flagship moves:**

- Implement Primary care service expansion across the region

**Tensions:**

- Implementation requires sustained funding

**Interventions on the system:**

- Primary care service expansion intervention (state variable: `primary_care_expansion_index`, sign: +) (relaxes: `primary_care_expansion_constraint`)


---

## Claims cited on this page

- **Health service access in Hawkes Bay is constrained by workforce shortage and geographic isolation. Nursing vacancies and GP shortages are acute in rural areas; specialist services require travel, delaying diagnoses and treatment for chronic and acute conditions.** [value: 8 percent prevalence; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* type_2_diabetes_prevalence_percent, cardiovascular_disease_mortality_rate.

*Constraints:* primary_care_gp_capacity, chronic_disease_management_programme_funding.

*Inputs:* obesity_prevalence, smoking_prevalence.


*Feedback loops:*

- `Unmanaged disease increases complications; hospital admissions rise; primary care overwhelmed; disease management deferred; worse outcomes result.`


---

*Generated from `problem.hawkes_bay.health.chronic_disease` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
