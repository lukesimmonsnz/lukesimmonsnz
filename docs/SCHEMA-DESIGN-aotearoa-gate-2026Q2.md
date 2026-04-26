# Layer 1a verification gate — Schema design (Aotearoa)

Gate ref: `CLAUDE.md` §9.1
Artifact under review: `docs/SCHEMA-DESIGN-aotearoa.md` (PI-ratified 2026-04-25)
Verifier: Opus
Date: 2026-04-25 (Q2)
Mode: tool-state, predicate-level findings only.

Verdict (top-line): **CHANGES_REQUESTED**. One BLOCKING type-inconsistency, four SUBSTANTIVE defects, eleven FORMAL defects, three ADVISORY items. Non-blocking ratification possible if BLOCKING and SUBSTANTIVE items are adjudicated by PI.

Severity legend:
- `[B]` BLOCKING — predicate is type-inconsistent, contradicts the inventory, or refers to an undefined symbol that prevents discharge in Layer 1c.
- `[S]` SUBSTANTIVE — gap is closed partially, strengthened silently, or omits a methodology from the seed registry.
- `[F]` FORMAL — predicate is intelligible but not strictly closed (free names, ellipsis, tacit functions).
- `[A]` ADVISORY — placement / terminology / minor.

---

## Check 1 — every cross-entity invariant in §3 is a closed first-order formula

Eighteen predicates inspected: P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P15, P16, P17, P18.

### 1.1 `[B] BLOCKING` — P3 type-inconsistency on `E_cites`

§3.3 P3, fourth conjunct:
```
∧ (∃ s ∈ V_Source. (p, s) ∈ E_cites)        — at least one direct Source citation
```
where `p ∈ V_Problem`. §2 row 1 defines:
```
| cites | Claim → Source | Many |
```
i.e. `E_cites \subseteq V_\mathrm{Claim} \times V_\mathrm{Source}`. The predicate $\langle p, s \rangle \in E_\mathrm{cites}$ with $p \in V_\mathrm{Problem}$ is not well-typed under the §2 inventory. Two repairs are possible (PI to choose):

(a) Extend §2 to admit $E_\mathrm{cites} \subseteq (V_\mathrm{Claim} \cup V_\mathrm{Problem}) \times V_\mathrm{Source}$ — restoring Auckland's `problem.source_ids` directly as a `cites` edge. P3 then well-typed.

(b) Rewrite the conjunct Claim-mediated:
$$\exists c \in V_\mathrm{Claim}, s \in V_\mathrm{Source}.\ (p, c) \in E_\mathrm{evidenced\_by} \land (c, s) \in E_\mathrm{cites}.$$
This makes Claim the sole `cites` source vertex.

Auckland's `problem.schema.json` line 65 (`source_ids: minItems: 1`) currently grounds (a). The migration doc §2 row 1 says `cites: Claim → Source` only. The design straddles both. Adjudication required.

### 1.2 `[F]` — P1 free symbol `refs`

```
P1: ∀ v ∈ V. ∀ u ∈ refs(v). u ∈ V
```
`refs` not in §0 alphabet $\{V, E, \tau, \lambda, V_T, E_r\}$. Convention is clear (any ID-string referenced by $v$'s YAML attributes), but the function is undefined. Closure of $\mathrm{refs}: V \to 2^{(\mathrm{IdString})}$ should be specified as the union over a finite set of attribute projections.

### 1.3 `[F]` — P10 unbound indices

```
P10: ¬∃ c₁,…,c_k ∈ V_Claim. (cᵢ, c_{i+1}) ∈ E_supersedes ∧ c_k = c₁
```
Free variables: `i`, `k`. Ellipsis is informal. Strict form:
$$\neg \exists k \geq 2.\ \exists c_1,\dots,c_k \in V_\mathrm{Claim}.\ \big(\forall i \in \{1,\dots,k-1\}: (c_i, c_{i+1}) \in E_\mathrm{supersedes}\big) \land c_k = c_1.$$
Or equivalently: the transitive closure $E_\mathrm{supersedes}^+$ is irreflexive.

### 1.4 `[F]` — P11 direction underspecified

`E_supersedes` direction (newer→older or older→newer) is asserted only by the verb's natural-language reading. No formal pinning in §2. P11's correctness depends on the unstated convention. State explicitly: $(c, c') \in E_\mathrm{supersedes} \iff c \text{ supersedes } c'$.

### 1.5 `[F]` — P14 attribute/edge confusion

```
P14: ∀ c ∈ V_Claim with c.methodology_tag ≠ ⊥.
       ∃ μ ∈ V_Methodology. id(μ) = c.methodology_tag
```
But §2 has `follows: Claim → Methodology` as an *edge*. P14 reasons over an *attribute* `methodology_tag` and an `id : V_\mathrm{Methodology} \to \mathrm{IdString}` function. The relationship between $(c, \mu) \in E_\mathrm{follows}$ and $c.\mathrm{methodology\_tag} = \mathrm{id}(\mu)$ is not stated. Two parallel encodings of the same fact; resolution rule (graph-build materialisation) is implicit.

Coverage relation P1 vs P14 also unstated: if `methodology_tag` ∈ refs(c), then P14 ⊆ P1 (redundant). If not, P14 is necessary. PI to disambiguate.

### 1.6 `[S]` — P16 free predicate `quantitative`

```
P16: ∀ c ∈ V_Claim. quantitative(c) → c.methodology_tag ≠ ⊥
```
`quantitative` defined in §5.5 prose ("derived predicate `quantitative ⟺ value ≠ ⊥` at graph-build time"). Not stated inside §3. Inline the definition for the predicate to be self-contained:
$$\mathrm{quantitative}(c) \iff c.\mathrm{value} \neq \bot.$$

### 1.7 `[S]` — P6 `nat` open enumeration

§3 helper: "$\mathrm{nat}(s)$ is true iff $s$ contains a national-keyword". The set of national-keywords is not enumerated anywhere in §3 or §4. Closure requires either (i) an explicit finite set $K_\mathrm{nat} \subset \Sigma^*$ pinned in the methodology registry, or (ii) lifting `nat` to a typed flag on Claim removed from `statement(c)` text. Currently underdetermined.

### 1.8 `[S]` — P7 `ment` informal

Same defect class as 1.7. "$\mathrm{ment}(s, r)$ is true iff $s$ mentions Region $r$ by canonical name" requires (i) a fixed canonical-name map $\mathrm{name} : \mathrm{Region} \to \Sigma^*$ and (ii) a fixed substring relation, OR (iii) replacement by a structural typed reference. Neither is provided.

### 1.9 `[S]` — P5 external regex dependency

```
helpers: cmp(s) is true iff statement s matches the comparison-pattern regex
         of §5a Rule R3 of the migration doc
```
§5a was not loaded into the gate's input scope (per scope: §§ 2, A.5 only). The predicate body of `cmp` is exogenous to `SCHEMA-DESIGN-aotearoa.md`. For self-containedness, the regex (or a typed structural alternative) should be transcluded into §3 or §4.

### 1.10 `[F]` — P15 informal substring relation

```
P15: ∀ p ∈ V_Problem. ∀ f ∈ figures(p).
       ∃ s ∈ narrative(p). identifier(f) ∈ body(s)
```
`identifier(f) ∈ body(s)` overloads $\in$: figure id (string) "in" narrative body (string). Mathematically: $\mathrm{identifier}(f) \sqsubseteq \mathrm{body}(s)$ where $\sqsubseteq$ is the substring relation.

Placement note `[A]`: P15 is intra-entity (figures and narrative both fields of the *same* Problem). Belongs in JSON Schema's `oneOf`/`if-then` machinery if expressible, otherwise in `invariants.py` — either way it is not a *cross-entity* invariant. §3 placement is defensible (JSON Schema cannot cross between two array fields of the same object easily) but inconsistent with the §3 framing.

### 1.11 `[F]` — P17 `engagement_recorded` undefined

```
P17: ∀ c ∈ V_Claim. iwi_scope(c) ≠ ∅ → engagement_recorded(c)
```
`engagement_recorded(c)` glossed as "a per-claim provenance flag pointing at a `migration_log.yaml` entry". No formal definition. Pin as:
$$\mathrm{engagement\_recorded}(c) \iff \exists e \in \mathrm{migration\_log}.\ \mathrm{refers\_to}(e, c).$$
Or replace with a typed attribute `c.engagement_record_id : MigrationLogId | \bot` and require non-bottom. Currently free.

### 1.12 `[F]` — P12 ill-conditioned disjunct

```
κ(n) = issue → p = ⊥ ∨ κ(p) = issue
```
Under the universal quantifier $\forall (n, p) \in E_\mathrm{parent}$, $p$ ranges over *existing* parents — $p = \bot$ is unreachable. The intended semantics ("issues may be roots OR sub-issues of issues") requires a different binder:
$$\forall n \in V_\mathrm{IbisNode}.\ \kappa(n) = \mathrm{issue} \implies \big(\neg \exists p.\ (n, p) \in E_\mathrm{parent}\big) \lor \big(\forall p.\ (n, p) \in E_\mathrm{parent} \to \kappa(p) = \mathrm{issue}\big).$$
Or treat `parent` as a partial function $V_\mathrm{IbisNode} \to V_\mathrm{IbisNode} \cup \{\bot\}$ and split the predicate accordingly.

### 1.13 `[S]` — P5 admits comparison-claim self-pinning

```
P5: cmp(c) ∧ |scoped_to(c)| ≥ 2
    → ∃ μ. (c, μ) ∈ E_follows
    ∧ ∀ r ∈ scoped_to(c). ∃ c′ ≠ c. r ∈ scoped_to(c′) ∧ (c′, μ) ∈ E_follows
```
Nothing constrains $c'$ to be a non-comparison claim. A 16-region rollup could be "pinned" by another 16-region rollup under the same methodology, satisfying P5 without any per-region Instance ever existing. If the load-bearing intent (per migration doc §2) is that comparison claims must be backed by *Instance*-level evidence, the predicate must add $|\mathrm{scoped\_to}(c')| = 1$ to the pinning conjunct. PI adjudication: feature or oversight?

### 1.14 `[F]` — P3, P4 use undeclared attribute functions

`flagship_moves(k)`, `tensions(k)`, `interventions(k)`, `figures(p)`, `narrative(p)` are projections from YAML fields, not edges. §0 defines $\tau, \lambda, V_T, E_r$ — attribute-projection notation is not formalised. Convention is clear; pedantic closure requires either a §0 addendum ("for any attribute name $a$ defined on type $T$, $a : V_T \to \mathrm{val}(a)$ projects the YAML field") or rewriting in edge form where possible.

### Check 1 verdict

`CHANGES_REQUESTED`. One BLOCKING (1.1), four SUBSTANTIVE (1.6, 1.7, 1.8, 1.9, 1.13 — five), eight FORMAL. P3 must be resolved before Layer 1b/1c can compile invariants without ambiguity.

---

## Check 2 — every methodology in §4 traces to a specific line of `lint.py` or a specific JSON Schema field

Twelve registry seed entries inspected.

### 2.1 Trace verification (positive)

| # | id | claimed source | located | verdict |
|---|---|---|---|---|
| 1 | `graph_referential_closure_v1` | `lint._check_referenced_ids_exist` | `lint.py:21–29` | ✓ |
| 2 | `claim_must_cite_v1` | `lint._check_evidence_has_source` + JSON Schema `min_length=1` | `lint.py:44–49`; `evidence.schema.json:19` | ✓ (terminology nit, see 2.2) |
| 3 | `problem_subgraph_minimum_v1` | `lint._check_problem_minimums` | `lint.py:32–41` | ✓ |
| 4 | `camp_completeness_v1` | `lint._check_camp_completeness` | `lint.py:52–63` | ✓ |
| 5 | `figure_in_narrative_v1` | `lint._check_figure_references` | `lint.py:66–80` | ✓ |
| 6 | `source_typology_v1` | `source.schema.json#type` enum | `source.schema.json:16` | ✓ |
| 7 | `source_credibility_tier_v1` | `source.schema.json#credibility` enum | `source.schema.json:17` | ✓ |
| 8 | `claim_provenance_v1` | `evidence.schema.json#confidence` × `verification_status` | `evidence.schema.json:16–17` | ✓ |
| 9 | `driver_consensus_v1` | `driver.schema.json#consensus` | `driver.schema.json:13` | ✓ |
| 10 | `driver_category_taxonomy_v1` | `driver.schema.json#category` | `driver.schema.json:14` | ✓ |
| 11 | `camp_intervention_sign_v1` | `camp.schema.json#interventions[*].expected_sign` | `camp.schema.json:27` | ✓ |
| 12 | `problem_systems_model_v1` | `problem.schema.json#systems_model` | `problem.schema.json:21–31` | ✓ |

All 12 trace.

### 2.2 `[A]` — terminology nit on entry #2

`min_length=1` (string-length keyword) does not exist in JSON Schema for arrays. The constraint at `evidence.schema.json:19` is `minItems: 1`. Rename for accuracy.

### 2.3 `[S]` — omissions: implicit methodologies in source schemas not lifted

Three Auckland enums encode methodological commitments and are not entries in §4:

(a) **`driver.schema.json:17` — `timescale` enum** `{short, medium, long, permanent}`. This is a temporal-classification methodology applied to drivers; equal in standing to `driver_consensus_v1` and `driver_category_taxonomy_v1`. Recommend `driver_timescale_v1`.

(b) **`response.schema.json:13` — `actor` enum** `{crown, council, ccos, iwi, market, community, third-sector}` (7-value sectoral typology). §5.7 ratifies keeping this enum *and* adding a typed Actor reference, but the enum itself is not seeded in §4. Recommend `response_sector_typology_v1`.

(c) **`actor.schema.json:12` — `type` enum** `{iwi, hapu, crown-agency, council, ccos, political-party, ngo, academic-institution, business, individual, tribunal}` (11-value institutional typology). Distinct from (b) — the response sector enum is a 7-class abstraction over actors, not a refinement. Recommend `actor_institutional_typology_v1`.

These three are SUBSTANTIVE — they are existing methodological commitments that the §4 prose claims to seed exhaustively ("Every methodology currently *implicit* in `content/auckland/tools/lint.py` and the eight Auckland JSON Schemas is lifted"). The claim does not hold for (a)–(c).

### 2.4 `[A]` — borderline omissions (workflow vs methodology)

The following enums are workflow-status, not methodologies, and reasonable to exclude:

- `evidence.schema.json:17` `verification_status` — partially lifted into `claim_provenance_v1`; OK.
- `problem.schema.json:66` `status` enum `{draft-v0, draft, review, published}` — content lifecycle.
- `response.schema.json:14` `status` enum `{active, proposed, retired, modified}` — policy lifecycle.
- `problem.schema.json:57` `figures[*].status` enum `{placeholder, draft, final}` — figure lifecycle.

PI may choose to lift any of these as `*_lifecycle_v1` methodologies; current omission is defensible.

### 2.5 `[S]` — predicate-to-methodology coverage gap

§3 has 18 predicates; §4 seeds 12 methodologies. Predicates without methodology-registry entries: P5, P6, P7, P8, P9, P10, P11, P12, P13, P14, P16, P17, P18 (13 of 18). Eight of these (P5, P6, P7, P8, P9, P14, P16, P17) are *new* invariants the design introduces — §4 prose explicitly defers quantitative-comparison methodologies. ACCEPTED.

But P10, P11 (supersession DAG / freshness), P12, P13 (IBIS structural typing), P18 (symmetric closure of `tensions_with`) are structural invariants the design itself fixes. They are not deferred in the prose. They should either appear in the §4 registry as `kind: graph_invariant` entries or §4 should explicitly state that structural invariants on new entity types are deferred to Layer 1c. Currently silent.

### Check 2 verdict

`CHANGES_REQUESTED`. Three SUBSTANTIVE omissions (2.3 a/b/c) plus one coverage-gap silence (2.5). No FORMAL or BLOCKING defects. The §4 prose claim of exhaustiveness over Auckland's existing implicit choices is false until 2.3 is closed.

---

## Check 3 — §5 exhaustive over schema-design decisions

§5 has nine ratified items: 5.1 Theme, 5.2 Region taxonomy granularity, 5.3 IbisNode shape, 5.4 Iwi parallel taxonomy, 5.5 Quantitative vs symbolic claim, 5.6 Pattern threshold, 5.7 Response.actor, 5.8 Methodology mandatoriness, 5.9 evidence→claim rename.

The following decisions are made elsewhere in §1, §2, §3, §4 and are not surfaced in §5.

### 3.1 `[S]` — Edge-vs-field asymmetry between Camp and Response

§1 row `Camp`: `applicable_in: list[Region]`, `efficacy_in: list[Region]` — fields.
§1 row `Response`: `applies_in: list[Region]` — modelled as edge `applies_in: Response → Region` in §2.
Both are spatial-scope predicates on solution entities. The asymmetry (Camp uses YAML lists, Response uses edges) is unmotivated in §5. Either both should be edges (uniform graph projection) or both fields (uniform YAML idiom). PI choice not surfaced.

### 3.2 `[S]` — IBIS edge decomposition

§2 has three IBIS edges: `parent`, `supports`, `contradicts`. An equivalent design uses one edge `parent` plus a typed `kind` on the parent edge (`kind ∈ {hierarchy, pro, con}`). Decomposition into three edges affects:
- $|\mathcal{R}|$ (16 vs 14)
- P12 enforcement (clean) vs typed-edge reformulation
- query patterns over E_supports vs over E_parent[kind=pro]

Decision silently embedded in §2; not raised as a §5 trade-off despite §5.3 (IbisNode shape) being adjacent.

### 3.3 `[S]` — P5's existence-of-pinning strengthening

Migration doc §2 requires "comparison claims have ≥2 regions and require shared methodology_tag". P5 strengthens this with an existence quantifier:
$$\forall r \in \mathrm{scoped\_to}(c).\ \exists c' \neq c.\ r \in \mathrm{scoped\_to}(c') \land (c', \mu) \in E_\mathrm{follows}.$$

Authoring cost implication: an $n$-region comparison requires $n$ pinning claims under the same methodology. For $n = 16$, this is 16 mandatory companion claims per comparison. This is a substantive methodological commitment — load-bearing for content scaling — that does not appear as a §5 line item. Per Check 1.13 above, the predicate also admits self-pinning by other comparisons, weakening the intent.

### 3.4 `[S]` — `evidenced_by` polymorphic source set

§2 row `evidenced_by`: `{Problem, Pattern, Camp, Driver, Response} → Claim`. Five source types, two excluded (Indicator, Actor). The exclusion is unstated. Why is an Indicator definition not evidenced by Claims? Why is an Actor's role-claim not evidenced by Claims? Decision silently embedded.

### 3.5 `[S]` — National/region NLP predicates as schema invariants

P6 (national keyword) and P7 (region mention) introduce regex/NLP-style predicates over `statement(c)` *as schema-level invariants*. The alternative — requiring authors to encode `national_assertion: bool` and `region_mentions: list[Region]` as typed YAML fields, eliminating string-pattern matching — was not enumerated. Existence of NLP-derived invariants in the schema layer is itself a design decision. Silent.

### 3.6 `[A]` — `Indicator` rename from `metric`

§1.1 lifts `metric → Indicator`. Reason given: "§2 working list" (migration doc). Not a §5 line item. Renames in §5.9 (only `evidence → claim`) but `metric → Indicator` is a parallel rename of equal scope. ADVISORY — could be folded into §5.9.

### 3.7 `[A]` — `tensions_with` symmetry materialisation

P18 enforces $(k, k') \in E_\mathrm{tensions\_with} \to (k', k) \in E_\mathrm{tensions\_with}$ at the graph layer. Alternative: store as symmetric closure at query time, leaving YAML asymmetric. Decision (materialise) silently fixed by §2 row 18 ("Sym") and P18. Layer 1c implementation cost difference is small but real.

### 3.8 `[A]` — Methodology as typed entity

§1.2 declares `Methodology` "must be a typed entity". This is the most substantive type-system decision (the registry shape in §4 depends on it). Surfaced inline in §1.2 prose but not as a §5 ratified item. Recommend a §5.10 ratifying it explicitly even though the choice is forced by §4's registry shape.

### Check 3 verdict

`CHANGES_REQUESTED`. Five SUBSTANTIVE silent decisions (3.1, 3.2, 3.3, 3.4, 3.5) and three ADVISORY (3.6, 3.7, 3.8). The §5 set is **not** exhaustive over schema-design decisions. Defect 3.3 is the most consequential — P5 is the load-bearing predicate and its strengthening over the migration doc is a strategic content-scaling commitment.

---

## Check 4 — design closes the §2 / §A.5 epistemic gap

Migration doc §2 demands closure on three concerns; §A.5 demands closure on six PR-time review checks. Map each to schema-layer closure.

### 4.1 Pattern vs Instance distinction

Migration doc §2: Pattern has `manifests_in: list[Region]` (≥2 implied); Instance is region-specific; Pattern cites Instances; Instance invokes Pattern.

Schema design closure:
- `Pattern` is structural (§1).
- P8: $|\mathrm{manifests\_in}(\pi)| \geq 2 \land \exists c.\ (\pi, c) \in E_\mathrm{evidenced\_by}$ — type-defining.
- `invokes: Claim → Pattern` (§2 row 14) — present.

Closure: ✓ at the Pattern type-axiom level.

`[A]` Note: `Instance` as a distinct entity name is not introduced. Instance is unified into `Claim` (a Claim with $|\mathrm{scoped\_to}| = 1$ has Instance semantics). Defensible flattening, but the migration doc's vocabulary is not preserved. Downstream readers expecting `Instance` as a node type will need to translate. See defect 3.6 / 3.x for related rename-omissions.

### 4.2 Comparison-claim consistency

Migration doc §2: "comparison claims have ≥2 regions and require shared `methodology_tag` across compared regions, otherwise raise."

Schema design closure: P5. Closed and strengthened (see Check 1.13 and 3.3). The strengthening implies authoring cost — flag for PI ratification.

Closure: ✓ (over-closure).

### 4.3 Claim provenance discipline

Migration doc §2 / §A.5 items 2, 3, 4:
- Every Claim cites a Source — closed by P2 ✓
- Methodology consistency across compared regions — closed by P5 ✓
- Region-scope alignment with statement language — closed by P6 (national) and P7 (region-mention) — closed but with informal `nat`, `ment` (Check 1.7, 1.8)
- Neutrality / value-loaded verbs — referenced in §3.7 prose ("intra-entity, lives in JSON Schema") but no methodology entry in §4 (`neutrality_lint_v1` absent)

`[S]` 4.3.1 — Neutrality not seeded. Per migration doc §A.5 item 5 ("Check the claim is neutral in framing; flag value-loaded verbs"), this is an explicit Opus PR-time gate. The schema layer can either (a) seed `neutrality_lint_v1` as a JSON-Schema-discharged regex over banned verbs, or (b) explicitly defer to Opus runtime. §3.7 implies (a) but §4 does not seed it — the design is internally inconsistent on this point.

### 4.4 §A.5 items not closable at schema layer

Items 1, 5, 6 of §A.5 (citation actually supports claim; per-claim linkage; stake-of-reputation) are runtime-Opus judgements, not schema invariants. Schema-layer closure not expected. ✓

### 4.5 `[B]` — P14 + P16 + Auckland legacy: latent backwards-compat hazard

Migration doc §2 backwards-compat clause:

> Existing nodes without `methodology_tag` get a placeholder `legacy_v0` tag and are flagged by lint until a real tag is supplied.

Auckland's `evidence.schema.json` admits `value: number | string | null` (line 12). Some existing Auckland evidence has `value ≠ ⊥`. Under §5.5, `quantitative(c) \iff c.\mathrm{value} \neq \bot`. P16 then fires: `c.methodology_tag ≠ ⊥`. P14 then requires the tag to resolve to a registered Methodology.

§4 does **not** seed `legacy_v0` in the registry. At rename PR time (per §5.9), Auckland's quantitative claims will violate either P16 (if tag absent) or P14 (if tagged `legacy_v0` but unregistered). Design has no legacy-bridge methodology.

Repairs (PI to choose):
(a) Seed `legacy_v0` in §4 with `kind: provenance_tier` and `description: "placeholder for un-pinned Auckland quantitative claims; lint warns until replaced"`.
(b) Gate P16 activation behind a feature flag deferred until all 69 Auckland entities are re-tagged.
(c) Restate `quantitative(c)` to also require an explicit `quantitative: bool` on Claim, and false for Auckland legacy (matches migration doc §5b's earlier proposal — overruled in §5.5).

Currently the design is internally inconsistent with the migration doc's backwards-compat plan. Promote to BLOCKING because P14+P16 will fail closed-form on the ratified rename PR (§5.9) without one of the three repairs.

### Check 4 verdict

`CHANGES_REQUESTED`. (a), (b), (c) of migration doc §2 substantively closed at the schema layer. §A.5 items 2, 3 closed; item 4 (neutrality) referenced but unseeded (defect 4.3.1, SUBSTANTIVE); items 1, 5, 6 properly out of schema scope. **One BLOCKING latent inconsistency (4.5)** between the new P14/P16 invariants and the migration doc's `legacy_v0` backwards-compat plan; manifests at §5.9 rename PR time.

---

## Aggregate verdict

| Check | Verdict | Defects |
|---|---|---|
| 1. Closed first-order formulas | CHANGES_REQUESTED | 1 BLOCKING (P3 type-inconsistency on E_cites), 5 SUBSTANTIVE, 8 FORMAL |
| 2. Methodology traceability | CHANGES_REQUESTED | 3 SUBSTANTIVE omissions (timescale, response-sector, actor-type), 1 SUBSTANTIVE coverage gap, 1 ADVISORY (terminology) |
| 3. §5 exhaustiveness | CHANGES_REQUESTED | 5 SUBSTANTIVE silent decisions, 3 ADVISORY |
| 4. §2/§A.5 gap closure | CHANGES_REQUESTED | 1 BLOCKING (legacy_v0 / P14+P16 backwards-compat hazard), 1 SUBSTANTIVE (neutrality unseeded), 1 ADVISORY (Instance vocabulary unification) |

**Gate disposition**: do **not** auto-promote to Layer 1b. Two BLOCKING items (1.1 P3 type-inconsistency on `E_cites`; 4.5 latent legacy bridge under P14/P16) require PI adjudication before JSON Schema authoring begins. The remaining SUBSTANTIVE defects are tractable in a single revision pass.

Adjudication queue for PI (priority order):
1. Defect 1.1 — repair option (a) extend `cites` codomain, or (b) Claim-mediate P3.
2. Defect 4.5 — repair option (a) seed `legacy_v0`, (b) gate P16, or (c) restate `quantitative` as explicit field.
3. Defect 3.3 — accept or weaken P5's per-region pinning existential.
4. Defect 1.13 — add $|\mathrm{scoped\_to}(c')| = 1$ constraint to P5 pinning, or accept self-pinning.
5. Defects 2.3 (a/b/c) — add three methodology-registry entries.
6. Remaining FORMAL and ADVISORY items batched into a single notation-cleanup pass.

---

## Addendum — PI ratification of gate findings (2026-04-25)

PI accepted all recommendations. Per-item disposition:

### BLOCKING items — dissolved

- **1.1 (P3 / `E_cites` type-inconsistency)**: dissolved by Auckland delete-and-rebuild posture. Repair (b) — Claim-mediate the P3 source-citation conjunct — accepted as the canonical pathway:
  $$\exists c \in V_\mathrm{Claim}, s \in V_\mathrm{Source}.\ (p, c) \in E_\mathrm{evidenced\_by} \land (c, s) \in E_\mathrm{cites}.$$
  No two-track citation; all source provenance flows through Claim.
- **4.5 (P14 + P16 / `legacy_v0` cascade)**: dissolved by Auckland delete-and-rebuild. No legacy quantitative claims to bridge; P14/P16 satisfiable on greenfield data; `legacy_v0` not seeded.

### Auckland posture — newly ratified

- **Delete-and-rebuild**: existing `content/auckland/data/` corpus discarded under the schema migration. Reauthored from a clean slate against the new `content/_schema/` canonical schema. §5.9 rename PR machinery is obsolete; §9.3 schema-migration gate criterion changes from "all 69 existing Auckland entities still validate" to "the rebuilt Auckland corpus validates against the new schema".

### Item 2 — P5 strengthened to Instance-pinning ($P5'$)

Accepted:
$$P5':\ \mathrm{cmp}(c) \land |\mathrm{scoped\_to}(c)| \geq 2 \implies \exists \mu.\ (c, \mu) \in E_\mathrm{follows} \land \forall r \in \mathrm{scoped\_to}(c).\ \exists c' \neq c.\ \mathrm{scoped\_to}(c') = \{r\} \land (c', \mu) \in E_\mathrm{follows}.$$

Each region in scope must have its own Instance-level claim (singleton `scoped_to`) under the same methodology. Comparison-claim self-pinning eliminated. Operational softening: lint downgrades to warning for any region $r$ where $\le 3$ regions are populated overall; promotes to error after the third populated region.

### Item 3 — Methodology registry extended

Three entries added to §4:

| id | source | kind | discharged_by |
|---|---|---|---|
| `driver_timescale_v1` | `driver.schema.json:17` enum | source_typology | json_schema |
| `response_sector_typology_v1` | `response.schema.json:13` enum | source_typology | json_schema |
| `actor_institutional_typology_v1` | `actor.schema.json:12` enum | source_typology | json_schema |

§4 seed grows from 12 to 15.

### Item 4 — Silent design decisions ratified

- **3.1**: Camp's `applicable_in` and `efficacy_in` lifted from YAML fields to edges. Two new edge types: $E_\mathrm{applicable\_in}, E_\mathrm{efficacy\_in} \subseteq V_\mathrm{Camp} \times V_\mathrm{Region}$. $|\mathcal{R}|$ grows from 16 to 18.
- **3.2**: IBIS edge decomposition (`parent`, `supports`, `contradicts` as three edges) retained. Matches Rittel's IBIS taxonomy; cleanest P12 enforcement.
- **3.4**: `evidenced_by` polymorphic source set $\{Problem, Pattern, Camp, Driver, Response\} \to Claim$ retained. Indicator excluded (definitional artifact, evidence base is methodology via $E_\mathrm{follows}$); Actor excluded (existence-claims are Source-referenced; contested claims live as Claim nodes about the Actor). Justification to be inlined into §2 prose during Layer 1a-cleanup.
- **3.5**: P6 / P7 reformulated as structural predicates over typed YAML fields. New Claim attributes:
  - `national_assertion: bool` (default `false`)
  - `region_mentions: list[Region]` (default `[]`)

  Reformulated invariants:
  $$P6':\ \forall c \in V_\mathrm{Claim}.\ c.\mathrm{national\_assertion} \implies \mathtt{nz} \in \mathrm{scoped\_to}(c).$$
  $$P7':\ \forall c \in V_\mathrm{Claim}, r \in \mathrm{Region}.\ r \in c.\mathrm{region\_mentions} \implies r \in \mathrm{scoped\_to}(c).$$

  NLP-style helpers `nat(s)` and `ment(s, r)` eliminated from §3. Defects 1.7 and 1.8 dissolved. A separate, downgradeable lint warning may perform canonical-name matching against `statement(c)` to flag missing `region_mentions` tags, but the schema invariant is structural.

### Item 5 — Notation cleanup pass scheduled

Single Sonnet session, narrowly scoped. Discharges remaining FORMAL defects: P1 (`refs` definition in §0), P10 (transitive-closure irreflexivity), P11 (direction pinned in §2 row 12), P12 (partial-function reformulation, $\bot$ disjunct elimination), P14 (resolution rule between `methodology_tag` and $E_\mathrm{follows}$), P15 (substring relation $\sqsubseteq$), P17 (`engagement_recorded` formalised or dropped). No strategic content; Layer 1b begins after cleanup completes.

### Layer 1a closure status

- Schema design ratified (2026-04-25, prior).
- Gate complete (2026-04-25, this report).
- All findings adjudicated; ratifications recorded.
- Cleanup pass pending; on its completion, Layer 1b is unblocked.

End of gate report.
