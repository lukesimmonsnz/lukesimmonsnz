---
title: "Health workforce shortage in Wellington"
section: health
subpage: workforce-shortage
order: 4
updated: 2026-04-26
summary: >
  Wellington faces acute health workforce shortages across nursing, general practice, and specialist roles. The shortage is driven by global competition for health workers, domestic pipeline constraints, and wage gaps relative to Australia. Workforce gaps directly limit the capacity of Wellington's health system to meet demand.
status: draft
generated_from: problem.wellington.health.workforce_shortage
---

# Health workforce shortage in Wellington

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Nurse vacancy rates

Wellington Regional Hospital and affiliated services have carried nursing vacancy rates above 15% in some wards, requiring ongoing agency and overseas nurse recruitment to maintain minimum safe staffing ratios (claim.wellington.health.nurse_vacancy_rate).


## GP pipeline risk

Wellington's general practice workforce is ageing, with a significant share of GPs expected to retire within the next decade and insufficient domestic training and recruitment to replace them at the current population growth rate (claim.wellington.health.gp_retirement_pipeline).


---


## Drivers

The following structural drivers contribute to this problem.


### Ageing GP workforce and retirement pipeline



- **Category:** demographic
- **Timescale:** medium
- **Consensus:** consensus

### Australia-NZ nurse wage differential



- **Category:** economic
- **Timescale:** long
- **Consensus:** consensus

### Primary care GP shortage



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Health Workforce Training and Retention Pipeline

Addressing Wellington's health workforce shortage requires sustained investment in training, rural/Māori recruitment, and retention incentives.

**Flagship moves:**

- Expand clinical training places at Wellington medical and nursing schools
- Rural health bonding scheme for GPs and nurses committing to underserved areas
- Māori health workforce scholarships and community health worker pathways

**Tensions:**

- Training pipeline benefits accrue over 5–10 years; short-term workforce gap remains
- Bonding schemes have high administrative overhead and variable compliance

**Interventions on the system:**

- Increase Wellington clinical training places by 30% with targeted Māori and Pasifika entry pathways (state variable: `health_workforce_vacancy_rate`, sign: -)


### International Health Worker Recruitment

Targeted international recruitment with streamlined registration can address Wellington's immediate health workforce shortage within 2–3 years.

**Flagship moves:**

- Fast-track registration for IMGs from comparable healthcare systems
- Settlement support packages for international health workers in Wellington
- Telemedicine arrangements with international providers for specialist shortages

**Tensions:**

- International recruitment depletes health workforces in lower-income source countries
- IMGs may not stay in Wellington beyond bonding periods without retention support

**Interventions on the system:**

- Run targeted Wellington health workforce recruitment campaign in UK and Australia with settlement support packages (state variable: `health_workforce_vacancy_rate`, sign: -)


---

## Claims cited on this page

- **Wellington Regional Hospital and affiliated DHB services reported nursing vacancies above 15% in 2023-2024, driven by burnout from pandemic response, Wellington Fault earthquake preparedness planning, and workforce migration to regional areas with lower cost-of-living pressure.** [value: 15 percent nurse vacancy rate; 2022-2024] *(confidence: medium)* — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23.
- **Wellington's general practice workforce is ageing, with a significant share of GPs expected to retire within the next decade and insufficient domestic training and international recruitment to replace them at the rate required by Wellington's population growth trajectory.** *(confidence: medium)* — Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23.

---

## Further reading


- **Health New Zealand Te Whatu Ora Wellington Region Annual Report 2022/23** (Health New Zealand), 2023 — <https://www.tewhatuora.govt.nz/>


---

## Technical notes

*State variables:* nurse_vacancy_rate, gp_per_capita_ratio.

*Constraints:* australia_wage_differential, training_pipeline_capacity.

*Inputs:* international_migration_of_clinicians, domestic_training_output.


*Feedback loops:*

- `Burnout-attrition loop: workforce shortages increase workload for remaining staff; burnout and attrition increase; vacancy rate rises further.`


---

*Generated from `problem.wellington.health.workforce_shortage` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
