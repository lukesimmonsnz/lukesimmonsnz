---
title: "Tertiary Education Access and Completion"
section: education
subpage: tertiary-access
order: 3
updated: 2026-04-26
summary: >
  Maori and Pacific tertiary students in Auckland face completion rates 15-20 percentage points below NZ European, driven primarily by financial and housing stress rather than academic underperformance. Auckland rental costs are not adequately reflected in student allowances, forcing paid work that competes with study. Simultaneously, Auckland faces skills shortages in construction, health, and engineering while some tertiary fields are oversupplied.

status: draft
generated_from: problem.auckland.education.tertiary_access
---

# Tertiary Education Access and Completion

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Completion as the real measure

Auckland tertiary institutions enrol large numbers of Maori and Pacific students; the problem is not enrolment but completion. A student who enrols, studies for two years, and withdraws for financial reasons has no qualification, carries student debt, and is in a worse labour market position than if they had taken a shorter vocational qualification. The completion gap is the measure that matters, and it points squarely at Auckland's housing cost as the mechanism.


## Mismatch and the Auckland economy

Auckland's construction sector is running below capacity partly because of skilled worker shortages; its hospitals and aged care facilities are staffing from the Philippines and India because domestic training pipelines are insufficient. Fixing this mismatch is partly an information problem (students do not see wage premiums in shortage fields), partly an affordability problem (shortage-field programmes in health and engineering are expensive), and partly an ITP capacity problem. All three have addressable policy interventions.


---

## References



- **Tertiary Education Commission Annual Report 2023**, 2023 — <https://www.tec.govt.nz/about/publications/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Financial and Housing Barriers to Tertiary Completion



- **Category:** economic
- **Timescale:** medium
- **Consensus:** consensus

#### Tertiary-Labour Market Mismatch



- **Category:** institutional
- **Timescale:** long
- **Consensus:** contested


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Auckland Living Cost Support for Tertiary Students

The primary barrier to Maori and Pacific tertiary completion in Auckland is financial; housing and living costs consume study time through forced paid work. Auckland-specific student allowance supplements calibrated to Auckland rental costs would reduce dropout rates at lower fiscal cost than the long-run social cost of non-completion. Universal free tertiary tuition is insufficient without addressing the living cost gap.

**Flagship moves:**

- Introduce an Auckland Cost of Living Supplement to student allowances of $150/week for Auckland-enrolled students from low-income families.
- Expand student accommodation guarantees at Auckland University and AUT for first-year students from high-deprivation Auckland areas.
- Fund targeted bursaries for Maori and Pacific students in high-demand fields (health, engineering, construction) to incentivise completion.

**Tensions:**

- Auckland-specific allowance supplements create a geographic funding disparity; students in other cities face different cost pressures and the equity logic of Auckland-specific supplements is contestable.

- Living cost support addresses the symptom (financial stress) rather than the cause (Auckland housing unaffordability); without housing cost reduction, the supplement merely tracks rental inflation.


**Interventions on the system:**

- Introduce a $150/week Auckland cost of living supplement to student allowances for students enrolled at Auckland tertiary institutions from NZDep decile 8-10 backgrounds.
 (state variable: `tertiary_completion_rate_maori_pacific`, sign: +) (relaxes: `Gap between student allowance and Auckland rental cost`)
- Fund 500 targeted completion bursaries of $5,000 per year for Maori and Pacific students in health, engineering, and construction programmes at Auckland institutions.
 (state variable: `skills_shortage_fields_enrolment`, sign: +)


#### Labour-Market Aligned Tertiary Investment

Tertiary investment should be directed to fields where Auckland has labour shortages; subsidising fields with poor employment outcomes while health, trades, and engineering remain under-enrolled produces skills mismatches that harm both graduates and employers. Performance- based funding that rewards completion and employment outcomes in high-demand fields provides better returns than unconditional per-student funding.

**Flagship moves:**

- Weight performance-based tertiary funding to completion rates and employment outcomes in high-demand fields.
- Fund industry-designed micro-credential programmes in construction, health, and digital skills at Auckland ITPs.
- Publish comprehensive field-of-study employment and wage outcome data to inform student enrolment decisions.

**Tensions:**

- Labour market signals are lagging; fields that appear oversupplied today may face shortages when current students graduate in 3-4 years. Performance-based funding may deter investment in fields with long training cycles (medicine, law, engineering) whose graduates have excellent long-run outcomes.

- Fields with poor employment outcomes are often fields with high Maori and Pacific enrolment; outcome-weighted funding may inadvertently reduce resources for institutions serving these communities.


**Interventions on the system:**

- Introduce field-of-study employment outcome weighting into PBRF and TEC funding, increasing the weight on completion and employment in high-shortage fields by 20%.
 (state variable: `skills_shortage_fields_enrolment`, sign: +)
- Fund 10 industry-designed micro-credential programmes at Auckland ITPs in construction, health care, and digital skills with employer co-design and guaranteed pathway to employment.
 (state variable: `tertiary_completion_rate_maori_pacific`, sign: +)


### Claims cited on this page

- **Tertiary completion in Auckland is sharply correlated with secondary school decile and student income. Students from low-income families entering tertiary study face barriers to completion: housing cost burden, part-time work, inadequate student support. Completion rates are lowest among students from high-deprivation neighborhoods and low-decile schools; Māori and Pacific students are concentrated in these cohorts, producing gaps in credentials and long-term income outcomes.** — Tertiary Education Commission Annual Report 2023.
- **Auckland housing costs consume a disproportionate share of student allowances and loan living costs; students from low-income families studying in Auckland face a structural deficit between Crown-funded living support and actual Auckland rental costs, forcing paid work that competes with study time and increases dropout risk.
** — Tertiary Education Commission Annual Report 2023.
- **Auckland faces simultaneous tertiary graduate oversupply in some fields and acute skilled worker shortages in construction, health, engineering, and trades; the mismatch reflects tertiary enrolment patterns that do not track labour market signals, partly because student choice is not well-informed by wage and employment outcome data.
** *(confidence: medium)* — Tertiary Education Commission Annual Report 2023.

### Systems-model notes

*State variables:* tertiary_completion_rate_maori_pacific, skills_shortage_fields_enrolment, student_paid_work_hours, dropout_rate_first_year.

*Constraints:* Housing cost: Auckland rents not reflected in national allowance calibration, Funding lag: field-of-study labour market signals lag actual graduation by 3-4 years, Equity tension: outcome-weighted funding may reduce resources for high-Maori-Pacific-enrolment institutions.

*Inputs:* auckland_living_cost_supplement, targeted_completion_bursaries, performance_based_funding_weight, micro_credential_programme_count.


*Feedback loops:*

- `Financial stress → paid work → study time reduction → lower completion → no qualification premium`
- `Skills shortage → wage premium → enrolment growth → 3-year lag before supply reaches market`


</details>

---

*Generated from `problem.auckland.education.tertiary_access` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
