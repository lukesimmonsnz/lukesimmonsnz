---
title: "Ethnic income and wellbeing gaps"
section: inequality
subpage: ethnic-gap
order: 2
updated: 2026-04-26
summary: >
  Hawke's Bay has entrenched income, employment, and health disparities concentrated in high-deprivation communities. Median household income in the most affected communities is approximately 25% below the regional average; unemployment is three times higher than in lower-deprivation areas. These gaps reflect structural barriers including seasonal labour market dependence, limited tertiary access, and occupational concentration in lower-wage roles.
status: draft
generated_from: problem.hawkes_bay.inequality.ethnic_gap
---

# Ethnic income and wellbeing gaps

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## Income Disparity

Median Māori household income in Hawke's Bay is approximately $64k, compared to $92k for European households — a gap of 30%.


## Employment Gap

Māori unemployment in Hawke's Bay is approximately 12%, compared to 4% for European residents. Overrepresentation in low-wage occupations.


---


## Drivers

The following structural drivers contribute to this problem.


### Geographic concentration of deprivation



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Place-based investment in deprived neighbourhoods

Targeted investment in deprived suburbs (Flaxmere, West Napier) in education, jobs, and community services breaks cycles of concentrated disadvantage.

**Flagship moves:**

- Establish Flaxmere Revitalisation Zone with 10-year dedicated funding
- Co-design neighbourhood improvement plans with iwi and community
- Attract employers to locate training hubs in deprived suburbs, not CBD

**Tensions:**

- Targeted place-based investment may be seen as unfairly advantaging one community
- Without complementary social support, infrastructure investment may attract gentrification and displacement

**Interventions on the system:**

- Co-fund schools in Flaxmere and West Napier to attract quality teachers and expand support services (state variable: `school_resource_equity_index`, sign: +)
- Establish job training and placement hubs in deprived neighbourhoods to improve labour market attachment (state variable: `employment_access_index`, sign: +)


---

## Claims cited on this page

- **Median household income in Hawke's Bay's high-deprivation communities is approximately $64,000, compared to $80,000 for the broader regional average — a 20% gap reflecting occupational concentration in seasonal agricultural work, retail, and lower-wage service employment.** [value: 64 NZD thousands; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.
- **Unemployment in Hawke's Bay's high-deprivation communities is approximately 12%, roughly twice the regional average, reflecting dependence on seasonal horticultural and agricultural labour with high variability and limited year-round employment pathways.** [value: 12 percent unemployment; 2024] *(confidence: medium)* — Census 2023: Hawke''s Bay Regional Profile.

---

## Further reading


- **Census 2023: Hawke''s Bay Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>


---

## Technical notes

*State variables:* median_maori_household_income_dollars, maori_unemployment_rate_percent.

*Constraints:* historical_land_dispossession, ongoing_discrimination.

*Inputs:* education_achievement_gap, occupational_segregation.


*Feedback loops:*

- `Lower education limits job access; occupational segregation suppresses wages; limited household assets constrain next generation; gaps persist.`


---

*Generated from `problem.hawkes_bay.inequality.ethnic_gap` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
