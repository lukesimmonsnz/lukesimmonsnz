---
title: "Treaty Co-Governance and Maori Participation"
section: governance
subpage: treaty-co-governance
order: 2
updated: 2026-04-26
summary: >
  Treaty co-governance arrangements have expanded but remain politically contested. Auckland's mana whenua have statutory roles that have not consistently translated into substantive influence. 70% of New Zealand Maori are urban; urban Maori governance bodies lack the formal status of mana whenua iwi. The core debate is whether Treaty obligations require structural co-governance or can be fulfilled through equal citizenship frameworks and economic settlements.

status: draft
generated_from: problem.auckland.governance.treaty_co_governance
---

# Treaty Co-Governance and Maori Participation

<p class="horizon-band">Analysis horizon: 10yr · 50yr · 100yr</p>



## The urban Maori gap

The Treaty co-governance debate focuses primarily on mana whenua iwi and their relationship with the Crown over land and natural resources. This is important, but it does not address the governance needs of the majority of Auckland's Maori population — urban Maori who are not primarily connected to their rohe and whose relationship with governance is through general democratic channels that systematically under-represent them. Any serious Treaty partnership framework for Auckland must address both dimensions.


## The constitutional tension

The debate between Treaty partnership and equal citizenship is not resolvable through evidence; it is a values dispute about the constitutional foundations of New Zealand governance. New Zealand has not chosen to resolve it legislatively; the result is ongoing political conflict that consumes governance bandwidth without producing clarity. Both camps present genuine arguments; neither can be dismissed as simply wrong.


---

## References



- **Waitangi Tribunal Reports and Findings 2023**, 2023 — <https://www.waitangitribunal.govt.nz/reports/>

- **Auckland Council Long-Term Plan 2024-2034** — Auckland Council (Auckland Council), 2024 — <https://www.aucklandcouncil.govt.nz/plans-projects-policies-reports-bylaws/our-plans-strategies/long-term-plan/Pages/default.aspx>

- **Statistics New Zealand — 2023 Census of Population and Dwellings** (Statistics New Zealand (Stats NZ)), 2023 — <https://www.stats.govt.nz/tools/2023-census-place-summaries/auckland-region>


<details class="technical-appendix" markdown="1">
<summary><strong>Technical details</strong> — drivers, solution camps, claims, and systems model</summary>

### Drivers


The following structural drivers contribute to this problem.


#### Political Contestation of Co-Governance



- **Category:** cultural
- **Timescale:** long
- **Consensus:** contested

#### Treaty Implementation Gap in Urban Governance



- **Category:** institutional
- **Timescale:** long
- **Consensus:** contested


### Solution camps

A number of distinct positions recur in policy debates on this issue. Each is defensible on its own terms; none is obviously correct. Presented in alphabetical order without ranking.


#### Equal Citizenship and Universal Suffrage

Democratic legitimacy requires equal political weight for all citizens regardless of ethnicity; co-governance arrangements that give Maori a structural veto or joint authority over public decisions violate the principle of equal citizenship. The Crown can fulfil Treaty obligations through Treaty settlements (asset return, economic redress) without creating permanent ethnic differentiation in public governance structures.

**Flagship moves:**

- Remove ethnicity-based appointment provisions from Auckland Council governance structures.
- Direct Treaty fulfilment through economic settlements and asset return rather than governance co-design.
- Increase Maori electoral participation through community engagement and lowering barriers to standing for election.

**Tensions:**

- Removing co-governance provisions does not address the power imbalance that produced them; a formal equality that ignores structural disadvantage is not substantive equality.

- Economic settlements without governance rights have historically not translated into political influence for Maori; the Treaty guarantee of tino rangatiratanga requires governance, not just property.


**Interventions on the system:**

- Replace ethnicity-based Auckland Council advisory and appointment mechanisms with deprivation-indexed community representation that benefits Maori communities without ethnic specification.
 (state variable: `community_equity_representation_index`, sign: +)
- Fund targeted electoral participation programmes for Maori and Pacific Aucklanders to increase representation through general democratic channels.
 (state variable: `south_west_auckland_voter_turnout`, sign: +)


#### Treaty Partnership and Tino Rangatiratanga

The Treaty of Waitangi guarantees tino rangatiratanga — the authority of Maori to exercise self-determination over their people, lands, and taonga. Co-governance of natural resources and public services affecting Maori is a fulfilment of this obligation, not a departure from democracy; the Treaty is a constitutional foundation that shapes how democracy operates in New Zealand, not an exception to it.

**Flagship moves:**

- Entrench the Independent Maori Statutory Board's role in Auckland Council with binding recommendations on Treaty obligations.
- Establish a formal co-governance mechanism for Auckland's natural resources (harbours, freshwater, whenua) with mana whenua.
- Fund urban Maori governance bodies (Manukau Urban Maori Authority, etc.) with equivalent status to mana whenua for decisions affecting Auckland Maori.

**Tensions:**

- Co-governance based on ethnicity is contested in constitutional terms; arguments about democratic equality are not simply bad faith — they reflect genuine disagreement about how the Treaty relates to universal suffrage.

- The distinction between mana whenua (iwi with Treaty claims to Auckland land) and urban Maori creates a governance hierarchy within Maoridom that some pan-tribal organisations and activists reject.


**Interventions on the system:**

- Legislate binding Treaty compliance obligations for Auckland Council decisions affecting natural resources and Maori communities, with enforcement through Waitangi Tribunal fast-track process.
 (state variable: `treaty_compliance_index`, sign: +) (relaxes: `Non-binding status of IMSB recommendations`)
- Establish and fund an Urban Maori Co-Governance body for Auckland with equal status to mana whenua on decisions affecting Auckland Maori regardless of tribal affiliation.
 (state variable: `urban_maori_governance_representation`, sign: +)


### Claims cited on this page

- **Treaty of Waitangi co-governance arrangements — where Crown and Maori exercise joint decision-making authority over natural resources, public services, or geographical areas — have expanded significantly since the 2017 Whanganui River and 2021 Three Waters reform proposals; the model is contested, with supporters arguing it fulfils Treaty obligations and critics arguing it creates a parallel governance structure inconsistent with democratic equality.
** — Waitangi Tribunal Reports and Findings 2023.
- **Auckland's mana whenua iwi (Ngati Whatua Orakei, Te Kawerau a Maki, and others) have statutory roles in Auckland Council decision-making through the Independent Maori Statutory Board and various RMA processes; these roles have not consistently translated into substantive influence over decisions affecting Maori communities, particularly in South Auckland where many Maori are urban migrants disconnected from their rohe.
** *(confidence: medium)* — Auckland Council Long-Term Plan 2024-2034; Waitangi Tribunal Reports and Findings 2023.
- **Urban migration of low-income households seeking employment, education, and housing has reshaped New Zealand's demographic geography; approximately 70% of the population now lives in urban areas, with Auckland attracting the largest migration inflow. These urban populations are concentrated in high-deprivation urban wards with limited local decision-making power, amplifying the democratic deficit for residents of South and West Auckland, who are disproportionately Māori and Pacific.** [value: 70 percent urban; 2018-2023] — Waitangi Tribunal Reports and Findings 2023; Statistics New Zealand — 2023 Census of Population and Dwellings.

### Systems-model notes

*State variables:* treaty_compliance_index, urban_maori_governance_representation, community_equity_representation_index, south_west_auckland_voter_turnout.

*Constraints:* Constitutional ambiguity: Treaty as constitutional foundation vs. Treaty as settlement mechanism is legally unresolved, Urban-rohe gap: mana whenua governance does not serve urban Maori disconnected from rohe, Political instability: co-governance arrangements are subject to reversal with government change.

*Inputs:* imsb_binding_authority, urban_maori_cog_body_funding, deprivation_indexed_representation, electoral_participation_programme.


*Feedback loops:*

- `Governance exclusion → lower policy responsiveness to Maori needs → worse outcomes → reduced legitimacy of system`
- `Political contestation → implementation instability → relationship breakdown → less effective partnership`


</details>

---

*Generated from `problem.auckland.governance.treaty_co_governance` on 2026-05-06. Do not hand-edit. Edit the entity files under the region's `data/` directory and re-run the region's render.py.*
