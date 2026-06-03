---
title: "School-to-Work and School-to-Tertiary Transition"
section: education
subpage: secondary-transition
order: 2
updated: 2026-04-26
summary: >
  Approximately 12-15% of Auckland 15-24 year olds are NEET; the rate is substantially higher for Maori and Pacific youth in South and West Auckland. Secondary curriculum is structured around university entry rather than vocational pathways; employers report foundational skill gaps in school leavers. Network exclusion disadvantages Maori and Pacific school leavers at the transition point where informal connections matter most.

status: draft
generated_from: problem.auckland.education.secondary_transition
---

# School-to-Work and School-to-Tertiary Transition

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The NEET cliff

The school-to-work transition is where educational disadvantage converts to labour market disadvantage. A young Maori man from South Auckland who leaves school at 17 without NCEA Level 2 and without a vocational pathway is in a structurally dangerous position: too under-credentialled for most employment, without the networks to access jobs filled informally, and without the skills or capital to be self-employed. The NEET rate at 18-20 is the educational outcome that most directly predicts the long-run inequality outcomes documented elsewhere in this graph.


## Pathway versus achievement

The tension between vocational pathway investment and academic excellence focus is partly false: both are needed. But they address different parts of the distribution. University access programmes help the 50-60% of Maori and Pacific students who attain NCEA Level 2 but do not proceed to university; vocational pathways help the 30-40% who do not reach that threshold. A system that invests only in the upper part of the distribution while the lower part falls into NEET status is not addressing the problem.


---

## References



- **Ministry of Education School Performance Data 2023**, 2023 — <https://www.educationcounts.govt.nz/statistics>

- **Tertiary Education Commission Annual Report 2023**, 2023 — <https://www.tec.govt.nz/about/publications/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Credential Inflation and Network Exclusion



- **Category:** economic
- **Timescale:** long
- **Consensus:** contested

#### School-to-Work Transition Gap



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Academic Achievement and University Access

The achievement gap for Maori and Pacific students is an academic achievement gap, not a pathways gap; the solution is higher NCEA attainment so that Maori and Pacific students have genuine access to university pathways rather than being channelled into vocational tracks. Investing in academic support, tutoring, and university access programmes gives students more options, not fewer.

**Flagship moves:**

- Fund academic mentoring and tutoring programmes in South and West Auckland secondary schools, targeting NCEA Level 2 and 3.
- Expand university bridging and access programmes (e.g. Manawa Aho) for Maori and Pacific Auckland students.
- Invest in high-quality school library and learning infrastructure in decile 1-3 Auckland schools.

**Tensions:**

- University access programmes help those who reach NCEA Level 3; they do not help the 30-40% of Maori and Pacific students who do not attain NCEA Level 2, for whom vocational and trades pathways are the relevant alternative.

- Academic focus without addressing attendance means that increased academic support is received by a smaller fraction of the target population than intended.


**Interventions on the system:**

- Fund after-school academic tutoring for 5,000 Maori and Pacific Auckland secondary students per year, delivered by near-peer tutors from the same communities.
 (state variable: `ncea_attainment_maori_pacific`, sign: +)
- Expand Manawa Aho and equivalent university access programmes to cover all Auckland decile 1-3 secondary schools with 20 places per school per year.
 (state variable: `university_enrolment_rate_maori_pacific`, sign: +)


#### Vocational Pathway Investment and Industry Partnership

Auckland's economy needs both university graduates and skilled tradespeople; the current system produces far more of the former pathway than the latter in terms of support and prestige. Investing in vocational and trades pathways in secondary schools — dual enrolment with ITPs, school-based apprenticeships, and industry partnerships — gives non-university-bound students a structured transition to viable employment and reduces NEET rates.

**Flagship moves:**

- Fund dual enrolment between Auckland secondary schools and ITPs for years 12-13 vocational learners.
- Establish employer-school partnership programmes in South and West Auckland trades and services industries.
- Establish a Gateway programme expansion to all Auckland decile 1-5 secondary schools.

**Tensions:**

- Vocational tracking risks concentrating Maori and Pacific students in lower-status pathways rather than addressing the academic achievement deficit that limits university access; it must be genuinely a parallel pathway, not a consolation route.

- ITP capacity in Auckland is constrained; dual enrolment programmes require ITP places that are currently at capacity in high-demand trades like construction and electrical.


**Interventions on the system:**

- Fund dual enrolment for 2,000 Auckland secondary school students per year in ITP trades programmes, with transport support and a $1,000 completion incentive.
 (state variable: `neet_rate_maori_pacific`, sign: -) (relaxes: `Absence of structured vocational pathway for non-university-bound students`)
- Expand Gateway employer placement programme to all Auckland decile 1-5 secondary schools with 10 placements per school per year and employer incentive payments.
 (state variable: `school_to_employment_transition_rate`, sign: +)


### Claims cited on this page

- **Approximately 12-15% of Auckland 15-24 year olds are not in employment, education, or training (NEET); rates are highest in high-deprivation suburbs of South and West Auckland, where barriers to further study and entry-level employment are most acute. NEET status at 18-20 is the strongest predictor of long-run disadvantage in income, health, and housing outcomes.** *(confidence: medium)* — Ministry of Education School Performance Data 2023; Tertiary Education Commission Annual Report 2023.
- **Auckland's secondary curriculum is dominated by academic NCEA pathways; vocational and trades pathways are underresourced and carry lower social status despite offering viable labour market entry for students not pursuing university. The result is that students who are not university-bound receive less support and fewer structured options at the school-to-work transition.
** *(confidence: medium)* — Tertiary Education Commission Annual Report 2023.
- **Auckland employers consistently report that school leavers lack foundational literacy, numeracy, and workplace readiness skills; the gap is largest for Maori and Pacific school leavers from South and West Auckland, reflecting both lower NCEA attainment and thinner networks connecting school to employer opportunity.
** *(confidence: medium)* — Tertiary Education Commission Annual Report 2023.

### Systems-model notes

*State variables:* neet_rate_maori_pacific, school_to_employment_transition_rate, ncea_attainment_maori_pacific, university_enrolment_rate_maori_pacific.

*Constraints:* ITP capacity: dual enrolment requires ITP places that are at capacity in high-demand trades, Tracking risk: vocational pathway investment must be genuinely parallel, not a lower-status default, Attendance: 40% absenteeism means transition support reaches a fraction of the target population.

*Inputs:* vocational_dual_enrolment_places, gateway_programme_schools, academic_tutoring_reach, university_access_programme_places.


*Feedback loops:*

- `NEET at 18-20 → income disadvantage → housing disadvantage → intergenerational poverty`
- `School-to-work network exclusion → lower first job quality → lower career trajectory`


</details>

---

*Generated from `problem.auckland.education.secondary_transition` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
