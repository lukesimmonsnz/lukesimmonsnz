---
title: "Governance Accountability and Integrity"
section: governance
subpage: accountability
order: 3
updated: 2026-04-26
summary: >
  Auckland Council and CCOs have among New Zealand's highest LGOIMA non-compliance rates. Public trust in Council is declining across all demographics and lowest in Maori and Pacific communities. Audit reports have repeatedly flagged procurement integrity concerns. The debate centres on whether open government (radical transparency) or integrity enforcement (Auditor-General extension, cooling-off periods) is the primary accountability lever.

status: draft
generated_from: problem.auckland.governance.accountability
---

# Governance Accountability and Integrity

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The transparency gap

Auckland spends approximately $4 billion per year. The public cannot easily find out who the Council's major contractors are, what they are paid, or whether they deliver value. The LGOIMA non-compliance pattern is not isolated incompetence; it is an institutional culture that treats information as a liability rather than a public good. Changing this requires structural intervention — automatic publication requirements that do not depend on individual officials' good faith.


## Procurement as the integrity focal point

Procurement is where governance integrity is most consequential and least visible. A 10% overcharge on a $500M infrastructure contract costs ratepayers $50M. The mechanisms that enable overcharging — inadequate competition, conflict of interest in evaluation, post-employment revolving doors — are known and addressable. The absence of systematic Auditor-General oversight of CCO procurement is an accountability gap that persists by institutional inertia rather than design.


---

## References



- **Chief Ombudsman Annual Report 2023**, 2023 — <https://www.ombudsman.parliament.nz/resources/annual-report>

- **Auckland Council Long-Term Plan 2024-2034** — Auckland Council (Auckland Council), 2024 — <https://www.aucklandcouncil.govt.nz/plans-projects-policies-reports-bylaws/our-plans-strategies/long-term-plan/Pages/default.aspx>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Procurement Integrity and Conflict of Interest



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** contested

#### Transparency Deficit and Information Withholding



- **Category:** institutional
- **Timescale:** medium
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Integrity Enforcement and Procurement Reform

Transparency is necessary but insufficient; without enforcement consequences for integrity breaches, publication requirements produce compliance theatre. Strengthening the Auditor-General's mandate over CCOs, imposing cooling-off periods on Council-to- private sector movement, and competitive procurement requirements for all contracts over $2M would restore procurement integrity.

**Flagship moves:**

- Extend Auditor-General jurisdiction to all Auckland CCO contracts and procurement processes.
- Legislate 2-year cooling-off period for senior Council and CCO staff moving to contractors.
- Require competitive tender for all Auckland Council and CCO contracts over $2M with public evaluation criteria.

**Tensions:**

- Extended Auditor-General jurisdiction over CCOs requires legislative change and Auditor-General capacity expansion; current OAG resources are already stretched across central government.

- Cooling-off periods reduce the attractiveness of public sector roles for people with private sector expertise; the talent pipeline for Council may narrow if the post-service constraints are too severe.


**Interventions on the system:**

- Legislate a 24-month cooling-off period for all Auckland Council and CCO staff at CE, GM, and board level before joining contractors doing business with their former employer.
 (state variable: `procurement_integrity_index`, sign: +) (relaxes: `Revolving door conflict of interest structure`)
- Extend Office of the Auditor-General jurisdiction to include all Auckland CCO procurement decisions over $5M, with mandatory post-completion review within 18 months.
 (state variable: `cco_procurement_audit_coverage`, sign: +)


#### Open Government and Radical Transparency

Trust in Auckland Council can only be restored by making its decisions visible in real time; proactive publication of contracts, meeting recordings, performance data, and OIA responses creates an accountability environment where poor decisions are harder to sustain. Open government is not a communications strategy — it is a structural commitment to making governance visible.

**Flagship moves:**

- Proactively publish all Auckland Council and CCO contracts over $500,000 within 30 days of signing.
- Live-stream and archive all governing body and CCO board meetings with searchable transcripts.
- Create a public dashboard tracking Council and CCO performance against LTP commitments in real time.

**Tensions:**

- Proactive disclosure of commercial contracts may reduce the Council's negotiating position in future procurements if counterparties can see all prior pricing; commercial sensitivity provisions exist for legitimate reasons.

- Publishing meeting transcripts and all documentation increases the administrative burden on Council staff and may reduce the quality of internal deliberation if officials self-censor in anticipation of public scrutiny.


**Interventions on the system:**

- Amend Auckland Council's LGOIMA publication schedule to proactively publish all contracts over $500,000 within 30 days of signing, with redaction limited to specific commercial IP provisions.
 (state variable: `council_transparency_index`, sign: +) (relaxes: `Commercial sensitivity provisions used to restrict public access`)
- Create a publicly accessible LTP performance dashboard updated quarterly showing actuals versus targets for all Council and CCO KPIs.
 (state variable: `public_trust_council`, sign: +)


### Claims cited on this page

- **Auckland Council and its CCOs have among the highest OIA and LGOIMA non-compliance rates in New Zealand; the Ombudsman has issued multiple adverse opinions against AT and Auckland Council for delayed, withheld, or inadequate responses to information requests on major infrastructure and development decisions.
** — Chief Ombudsman Annual Report 2023.
- **Public trust in Auckland Council has declined across the amalgamation period; survey data consistently shows that majorities of Aucklanders do not believe the Council listens to them, spends their money well, or makes decisions in their interests. Trust is lowest in high-deprivation areas of South and West Auckland, where infrastructure underinvestment is most visible.** *(confidence: medium)* — Auckland Council Long-Term Plan 2024-2034.
- **Auckland's development and infrastructure sector is characterised by recurrent conflict of interest concerns; the concentration of large contracts with a small number of suppliers, and the revolving door between council staff, CCO management, and private development consultancies, creates procurement integrity risks that have been identified in multiple audit reports.
** *(confidence: medium)* — Chief Ombudsman Annual Report 2023; Auckland Council Long-Term Plan 2024-2034.

### Systems-model notes

*State variables:* council_transparency_index, public_trust_council, procurement_integrity_index, cco_procurement_audit_coverage.

*Constraints:* Commercial sensitivity: legitimate IP protection provisions create cover for inappropriate withholding, OAG capacity: extending CCO jurisdiction requires Auditor-General resource expansion, Talent pipeline: strict post-employment constraints may deter private sector expertise from public sector.

*Inputs:* proactive_contract_publication, ltp_performance_dashboard, cooling_off_period_legislation, oag_jurisdiction_extension.


*Feedback loops:*

- `Low trust → lower engagement → less scrutiny → worse decisions → lower trust`
- `Procurement integrity failure → higher contract costs → fiscal gap → lower service quality → lower trust`


</details>

---

*Generated from `problem.auckland.governance.accountability` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
