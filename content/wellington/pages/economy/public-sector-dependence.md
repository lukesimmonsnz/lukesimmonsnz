---
title: "Wellington's structural dependence on public sector employment"
section: economy
subpage: public-sector-dependence
order: 1
updated: 2026-04-26
summary: >
  Wellington's economy is structurally dependent on public sector employment to a degree unmatched in any other New Zealand city. This dependence creates acute vulnerability to government policy shifts — as demonstrated by the 2024 public sector restructuring — and limits the economy's resilience and private sector diversification.
status: draft
generated_from: problem.wellington.economy.public_sector_dependence
---

# Wellington's structural dependence on public sector employment

<p class="horizon-band">Analysis horizon: 10yr · 50yr</p>



## Public sector concentration

Approximately 28% of Wellington's employed workforce is in the public sector — central government, state-owned enterprises, and local government combined — compared to approximately 16% nationally (claim.wellington.economy.public_sector_employment_share).


## 2024 restructuring impact

The 2024 public sector restructuring resulted in thousands of redundancies across Wellington-based government agencies, producing the largest single-year contraction in Wellington's public sector employment in decades and triggering measurable local economic effects (claim.wellington.economy.public_sector_restructuring_2024).


---


## Drivers

The following structural drivers contribute to this problem.


### 2024 fiscal consolidation and public sector headcount reduction



- **Category:** institutional
- **Timescale:** short
- **Consensus:** consensus

### Government location policy concentrating employment in Wellington



- **Category:** institutional
- **Timescale:** permanent
- **Consensus:** consensus


---

## Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


### Economic Diversification Beyond Public Sector

Wellington must actively cultivate a private sector technology and creative economy to reduce dependence on government employment.

**Flagship moves:**

- Wellington tech sector accelerator with Crown co-investment
- Film and creative industries support through WREDA and Screen Wellington
- Export-oriented business attraction incentives for Wellington CBD

**Tensions:**

- Private sector clusters are geographically self-reinforcing; Auckland-Auckland dominance is hard to reverse
- Government subsidy for specific sectors risks picking winners with poor ROI

**Interventions on the system:**

- Establish Wellington Innovation District around Courtenay Place and Te Whanganui-a-Tara waterfront with anchor tenants (state variable: `private_sector_employment_share`, sign: +)


### Public Sector Employment Stability and Anchor Role

Wellington's public sector concentration is a stability asset, not a liability; policy should focus on anchoring Crown functions in Wellington rather than diversifying away.

**Flagship moves:**

- Legislate minimum Crown agency headcount floors for Wellington
- Reverse 2024 public sector restructuring redundancies
- Expand public service graduate intake in Wellington

**Tensions:**

- Legislating employment floors limits government operational flexibility
- Reversing restructuring requires significant fiscal reversal

**Interventions on the system:**

- Introduce Public Service Crown Functions Wellington Policy requiring ministerial sign-off for relocations out of Wellington (state variable: `public_sector_employment_level`, sign: +)


---

## Claims cited on this page

- **Approximately 28% of Wellington's employed workforce is in the public sector (central government, state-owned enterprises, and local government combined), compared to approximately 16% nationally — reflecting Wellington's role as the national capital and seat of government.** [value: 28 percent of employed workforce in public sector; 2023] *(confidence: medium)* — Census 2023: Wellington Regional Profile; Treasury Budget Economic and Fiscal Update 2024.
- **The 2024 public sector restructuring resulted in the largest single-year contraction in Wellington's public sector employment in recent decades, with thousands of redundancies across central government agencies, triggering measurable local economic effects.** — Treasury Budget Economic and Fiscal Update 2024.

---

## Further reading


- **Census 2023: Wellington Regional Profile** (Stats NZ), 2023 — <https://www.stats.govt.nz/census/2023-census-main-results>

- **Treasury Budget Economic and Fiscal Update 2024** (NZ Treasury), 2024 — <https://www.treasury.govt.nz/publications/efu>


---

## Technical notes

*State variables:* public_sector_employment_share, private_sector_gdp_share.

*Constraints:* government_location_policy, economic_diversification_barriers.

*Inputs:* government_headcount_policy, private_sector_investment.


*Feedback loops:*

- `Government-anchor feedback: high government employment sustains demand for services and housing, which in turn maintains a business environment dependent on government-derived incomes — reducing diversification incentive.`


---

*Generated from `problem.wellington.economy.public_sector_dependence` on 2026-04-26. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
