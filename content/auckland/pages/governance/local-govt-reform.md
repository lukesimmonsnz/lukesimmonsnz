---
title: "Local Government Structure and Revenue"
section: governance
subpage: local-govt-reform
order: 1
updated: 2026-04-26
summary: >
  Auckland's 2010 amalgamation projected efficiency savings that have not materialised at scale. CCOs operate with limited democratic accountability. The three waters centralisation debate exposed deep tensions between scale efficiency and democratic control. Auckland Council's mandate substantially exceeds its revenue instruments; rates alone cannot fund the infrastructure and services a growing city of 1.8 million requires. The debate is between revenue reform and devolution as the primary response.

status: draft
generated_from: problem.auckland.governance.local_govt_reform
---

# Local Government Structure and Revenue

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The revenue-mandate mismatch

Auckland Council is responsible for the infrastructure, services, and planning decisions of a large city. It finances this responsibility primarily through a property tax (general rates) that grows more slowly than the economy, creates regressive distributional effects, and generates intense political resistance to necessary increases. The result is chronic under-investment in the infrastructure Auckland needs, not because the money does not exist in the economy but because the fiscal instrument does not capture it.


## Scale versus accountability

The three waters debate was at its core about this tradeoff: a national water entity could borrow more cheaply and invest at scale; but it was not accountable to the communities whose water it managed. The same tension runs through Auckland Council's CCO model. There is no optimal resolution — only a series of institutional design choices that trade one value against another.


---

## References



- **Auckland Council Long-Term Plan 2024-2034** — Auckland Council (Auckland Council), 2024 — <https://www.aucklandcouncil.govt.nz/plans-projects-policies-reports-bylaws/our-plans-strategies/long-term-plan/Pages/default.aspx>

- **Department of Prime Minister and Cabinet: Three Waters Reform Review 2023**, 2023 — <https://www.dpmc.govt.nz/three-waters>

- **Future for Local Government Review - He Piki Tūranga, He Piki Kōtuku** — Review into the Future for Local Government Panel (chaired by Jim Palmer) (Department of Internal Affairs), 2023 — <https://www.futureforlocalgovernment.govt.nz/the-review/the-final-report/>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Funding-Mandate Mismatch in Local Government



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus

#### Scale-Accountability Tradeoff in Local Governance



- **Category:** institutional
- **Timescale:** long
- **Consensus:** consensus


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Devolution and Community Control

Auckland's governance problem is not primarily a revenue problem but a control problem; too many decisions are made at the super-city level when they should be made at the local board or community level. Genuine devolution of decision-making — with commensurate funding — to local boards and Maori/Pacific community organisations produces better-calibrated outcomes because those closest to problems have the most relevant knowledge.

**Flagship moves:**

- Transfer decision-making authority over local parks, community facilities, and local roads to local boards with dedicated budgets.
- Fund community-controlled development organisations in South and West Auckland with capital and decision-making authority.
- Require Council to delegate to local boards rather than consult them on all decisions with primarily local impact.

**Tensions:**

- Genuine devolution with commensurate funding reduces the Council's ability to cross-subsidise high-need areas from high-revenue areas; fragmented funding may produce more inequality, not less.

- Local boards lack professional governance and technical capacity for complex capital decisions; devolution without capacity-building produces poor procurement and accountability outcomes.


**Interventions on the system:**

- Transfer $200M of Auckland Council's annual discretionary budget to local boards with binding authority over local parks, community facilities, and local road maintenance.
 (state variable: `local_board_decision_authority_index`, sign: +)
- Fund 5 community-controlled development organisations in South and West Auckland wards, with capital grants and authority to develop community-owned assets.
 (state variable: `community_self_determination_index`, sign: +)


#### Local Government Revenue Reform

Auckland Council cannot fulfil its mandate with rates as its primary revenue instrument; rates are regressive, grow slowly, and create political pressure against necessary infrastructure investment. Revenue reform — a local share of GST, a development levy with automatic adjustment, or a land value tax replacing general rates — gives Auckland the revenue base to match its infrastructure and service responsibilities.

**Flagship moves:**

- Legislate a 1% Auckland GST share returned to Council for infrastructure investment.
- Introduce an automatic infrastructure development levy on all new Auckland developments.
- Commission a transition plan for Auckland to move from current value general rates to site value (land) rates.

**Tensions:**

- A local GST share requires Crown-Council revenue sharing legislation that the Crown has historically resisted; political economy of central government ceding revenue is unfavourable.

- Land value tax transition is complex for existing landowners; the transition period creates windfall and hardship effects that require mitigation.


**Interventions on the system:**

- Legislate a 1 percentage point GST return to Auckland Council from GST collected within the Auckland region, estimated at $400-500M per year at current GST levels.
 (state variable: `council_revenue_adequacy_index`, sign: +) (relaxes: `Revenue growth constraint from rates-only base`)
- Introduce a mandatory infrastructure development contribution schedule for Auckland with automatic annual CPI adjustment, replacing the current negotiated consent condition system.
 (state variable: `infrastructure_cost_recovery_rate`, sign: +)


### Claims cited on this page

- **Auckland's 2010 super-city amalgamation reduced council numbers from 8 to 1 and was projected to deliver $2.9 billion in efficiency savings; independent reviews have found that savings have not materialised at projected scale, coordination costs increased, and community representation in local decision-making has diminished, particularly outside the urban core.
** *(confidence: medium)* — Auckland Council Long-Term Plan 2024-2034.
- **Auckland's seven CCOs (AT, Watercare, Eke Panuku, ATEED, etc.) operate with significant autonomy; board appointments, executive remuneration, and strategic decisions are made at arm's length from elected members. Public scrutiny of CCO performance is limited by commercial sensitivity provisions; loss-making CCO operations have persisted without triggering democratic accountability mechanisms.
** *(confidence: medium)* — Auckland Council Long-Term Plan 2024-2034.
- **The three waters (drinking water, wastewater, stormwater) reform debate exposed fundamental tensions in New Zealand local government about the appropriate scale of infrastructure entities; the Crown's proposed centralisation was rejected partly on democratic accountability grounds, with councils and Maori arguing that community ownership and iwi co-governance rights were extinguished by national entity proposals.
** — Department of Prime Minister and Cabinet: Three Waters Reform Review 2023.
- **The Future for Local Government Review (final report June 2023, "He Piki Turanga, He Piki Kotuku") delivered 17 substantive recommendations, including a structural shift to Te Tiriti-based partnership in local government, expanded local-government revenue tools beyond property rates, and a reframing of local government's purpose. Auckland's CCO governance model and post-amalgamation accountability gaps were referenced as a working example. Subsequent governments have implemented the recommendations only partially as of 2026.
** [value: 17 substantive recommendations; 2023] — Future for Local Government Review - He Piki Tūranga, He Piki Kōtuku.

### Systems-model notes

*State variables:* council_revenue_adequacy_index, infrastructure_cost_recovery_rate, local_board_decision_authority_index, community_self_determination_index.

*Constraints:* Crown-Council revenue sharing: political economy of central government ceding GST is unfavourable, Devolution capacity: local boards lack technical capacity for complex capital decisions, Cross-subsidy: devolution with ring-fenced budgets reduces ability to redistribute from affluent to deprived areas.

*Inputs:* gst_share_legislation, development_contribution_schedule, local_board_budget_transfer, community_org_capital_grants.


*Feedback loops:*

- `Revenue inadequacy → deferred infrastructure → higher future cost → wider fiscal gap`
- `Centralised decisions → community disengagement → lower mandate quality → less effective governance`


</details>

---

*Generated from `problem.auckland.governance.local_govt_reform` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
