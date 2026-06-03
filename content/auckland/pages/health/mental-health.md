---
title: "Mental Health Access and Capacity"
section: health
subpage: mental-health
order: 1
updated: 2026-04-26
summary: >
  Approximately 80% of Aucklanders seeking mental health referral for moderate conditions are declined or waitlisted. Youth (15-24) mental health ED presentations have increased 50% since 2018; CAMHS waitlists exceed 12 months. The mental health workforce vacancy rate exceeds 20% for clinical psychology and psychiatry. The debate is whether community stepped-care expansion or acute inpatient infrastructure investment is the priority.

status: draft
generated_from: problem.auckland.health.mental_health
---

# Mental Health Access and Capacity

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## The rationing trap

New Zealand's mental health system is rationed to severe and enduring illness by resource constraint; moderate-need presentations are declined or placed on waitlists that exceed the window of effective early intervention. The consequence is that mild presentations that could be resolved in six community sessions escalate to acute crises requiring inpatient admission at ten times the cost. The system is spending on the wrong end of the treatment cascade.


## Youth as the acute pressure point

The 50% rise in youth ED mental health presentations since 2018 is concentrated in self-harm and suicidal ideation. CAMHS is not resourced to see these young people within a clinically meaningful timeframe; families wait 12 months on a waitlist for a 15-year-old in acute distress. This is not a borderline resource allocation problem — it is a clinical safety issue.


---

## References



- **Te Pou Mental Health Workforce Survey 2023**, 2023 — <https://www.tepou.co.nz/resources/workforce-survey>

- **Health New Zealand Te Whatu Ora Annual Report 2023**, 2023 — <https://www.tewhatuora.govt.nz/publications/annual-report-2023>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Digital Environment and Social Isolation



- **Category:** cultural
- **Timescale:** medium
- **Consensus:** contested

#### Mental Health Underfunding Relative to Burden



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Acute Mental Health Infrastructure and Inpatient Capacity

Auckland's acute mental health system is dangerously under-capacity; the shortage of psychiatric inpatient beds forces premature discharge and re-presentation cycles. Building new acute and sub-acute mental health facilities, and expanding forensic psychiatric capacity, is the priority — community expansion cannot safely substitute for inpatient care for severe illness.

**Flagship moves:**

- Fund 100 additional adult acute psychiatric inpatient beds in Auckland by 2028.
- Build a dedicated child and adolescent mental health inpatient facility for the Auckland region.
- Expand forensic psychiatric capacity to reduce the transfer backlog from corrections to health.

**Tensions:**

- Inpatient psychiatric facilities are the highest-cost mental health investment; the same capital would fund many more community interventions, with better evidence for mild-to-moderate presentations.

- A focus on acute infrastructure does not address the prevention and early intervention gap; building beds for a crisis that could have been prevented upstream is a symptom not a solution.


**Interventions on the system:**

- Fund a new 80-bed CAMHS inpatient and day programme facility in the Auckland region with 2028 opening target.
 (state variable: `youth_mh_acute_waitlist`, sign: -) (relaxes: `CAMHS inpatient bed deficit`)
- Increase adult acute psychiatric bed count in Auckland by 100 through a combination of new build and repurposed ward conversion.
 (state variable: `psychiatric_boarding_rate`, sign: -)


#### Community Mental Health Expansion and Step-Down Care

The mental health crisis in Auckland is a capacity crisis; the system is rationed to severe acute need and cannot absorb moderate-need presentations. Expanding the stepped-care model — low-intensity digital and peer support, community counselling, and primary care psychology — would intercept people before they reach acute thresholds, reducing pressure on specialist services and inpatient capacity.

**Flagship moves:**

- Fund 50 additional community mental health teams across Auckland, with a 15-case-per-clinician cap.
- Establish free primary care psychology sessions (up to 6 per year) for all enrolled Auckland patients.
- Fund kaupapa Maori and Pacific Island mental health providers to serve their communities in Auckland.

**Tensions:**

- Stepped-care capacity expansion requires training pipeline growth that takes 5-7 years; short-run demand cannot be met by training alone and requires immediate international recruitment.

- Community models work best for mild-to-moderate presentations; severe and enduring illness still requires specialist and inpatient capacity that community expansion does not replace.


**Interventions on the system:**

- Fund six free counselling sessions per year through enrolled GP practices in Auckland, delivered by trained counsellors on GP referral.
 (state variable: `mh_unmet_moderate_need_rate`, sign: -) (relaxes: `Cost barrier to community mental health access`)
- Establish 10 kaupapa Maori and Pacific mental health clinics in South and West Auckland, with culturally responsive assessment and treatment.
 (state variable: `maori_pacific_mh_access_rate`, sign: +)


### Claims cited on this page

- **Specialist mental health services in Auckland are rationed to those with severe and enduring illness; an estimated 80% of people with moderate mental health conditions who seek referral are declined or waitlisted. Community mental health team caseloads in Auckland's district are among the highest in the country.
** [value: 80 percent declined or waitlisted; 2022-2023] *(confidence: medium)* — Te Pou Mental Health Workforce Survey 2023; Health New Zealand Te Whatu Ora Annual Report 2023.
- **Youth mental health presentations to Auckland EDs have increased by approximately 50% since 2018; youth (15-24) are the fastest growing group presenting to acute mental health services, yet specialist child and adolescent mental health service (CAMHS) waitlists in Auckland exceed 12 months for non-acute referrals.
** [value: 50 percent increase; 2018-2023] *(confidence: medium)* — Health New Zealand Te Whatu Ora Annual Report 2023.
- **Mental health and addiction workforce vacancy rates in Auckland exceed 20% for clinical psychology and psychiatry posts; the median wait for a first psychiatry appointment in the community sector is over six months, and training pipeline numbers are insufficient to close the gap within a decade at current enrolment rates.
** [value: 20 percent vacancy; 2022-2023] *(confidence: medium)* — Te Pou Mental Health Workforce Survey 2023.

### Systems-model notes

*State variables:* mh_unmet_moderate_need_rate, youth_mh_acute_waitlist, maori_pacific_mh_access_rate, psychiatric_boarding_rate.

*Constraints:* Training pipeline: psychology and psychiatry training takes 7+ years; no short-run workforce fix, Capital constraint: inpatient facilities require multi-year capital projects, Rationing: acute threshold rationing excludes moderate need and worsens long-run outcomes.

*Inputs:* community_mental_health_team_count, inpatient_bed_count, primary_care_psychology_sessions, workforce_vacancy_rate.


*Feedback loops:*

- `Unmet moderate need → crisis → acute presentation → inpatient admission → premature discharge → re-presentation`
- `Youth social isolation → anxiety/depression → school disengagement → youth justice contact`


</details>

---

*Generated from `problem.auckland.health.mental_health` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
