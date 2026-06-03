# METHODOLOGY.md — Aotearoa Research Methodology

**Version:** 1.0 (2026-Q2)
**Citable as:** Simmons, L. (2026). *Methodology for the Aotearoa Regional Research Project*. lukesimmonsnz.kiwi/research. Retrieved from `docs/METHODOLOGY.md` in the site repository.

---

## 1. Purpose

This document is the authoritative description of the methodology used to produce the
Aotearoa regional research content on **lukesimmonsnz.kiwi/research**. It covers the
knowledge representation schema, invariant system, authorship regime, and quality-gate
process. It is intended to be citable as a meta-source in any claim or pattern entity
that references its own methodological basis.

---

## 2. Scope

The research covers all 16 regional councils of Aotearoa New Zealand across 11 policy
themes:

| Slug | Theme |
|---|---|
| `housing` | Housing |
| `transport` | Transport |
| `infrastructure` | Infrastructure |
| `environment` | Environment |
| `inequality` | Inequality |
| `crime` | Crime |
| `health` | Health |
| `education` | Education |
| `economy` | Economy |
| `governance` | Governance |
| `climate-adaptation` | Climate adaptation |

As of 2026-Q2 the corpus contains **3,855 typed entities** across 16 regions plus a
national Pattern layer.

---

## 3. Knowledge representation

### 3.1 Typed entity graph

The corpus is a typed directed graph. Nodes are YAML files validated against
JSON Schema (Draft 2020-12) in `content/_schema/`. Edges are YAML fields carrying
foreign-key references between node IDs. Cross-entity integrity rules that cannot be
expressed in JSON Schema are enforced as Python predicates in
`content/_schema/invariants.py`.

### 3.2 Entity types

| Type | ID prefix | Description |
|---|---|---|
| **Source** | `source.*` | A citable external document, dataset, report, or authority |
| **Methodology** | `methodology.*` | A named analytic method drawn from the methodology registry |
| **Claim** | `claim.*` | A single, falsifiable empirical or normative assertion |
| **Driver** | `driver.*` | A causal or structural force that produces or sustains a Problem |
| **Camp** | `camp.*` | A school of thought, advocacy position, or policy stance |
| **Problem** | `problem.*` | A documented harm or challenge within a region/theme |
| **Pattern** | `pattern.*` | A cross-regional recurring structure (national rollup layer) |
| **Indicator** | `indicator.*` | A quantitative time-series linked to a claim or problem |
| **Actor** | `actor.*` | An institution, agency, or collective with a role in a theme |
| **Response** | `response.*` | A policy intervention or programme addressing a Problem |
| **IbisNode** | `ibis.*` | An IBIS-structured issue/position/argument node |
| **Theme** | `theme.*` | Root descriptor for a region × theme combination |

### 3.3 Edge inventory (18 edge types)

| Edge | Source type | Target type | Semantic |
|---|---|---|---|
| `evidenced_by` | Claim, Problem, Driver | Source | Primary provenance |
| `supports` | Claim | Claim | One claim lends evidential weight to another |
| `challenges` | Claim | Claim | One claim contests another |
| `methodology_tags` | Claim, Driver, Pattern | Methodology | Analytic method applied |
| `cites` | Claim | Source | Claim-mediated citation (P3 architecture) |
| `scoped_to` | Claim | Region | Restricts a comparison claim to a specific region |
| `applies_in` | Response, Camp | Region | Region applicability |
| `applicable_in` | Camp | Region | Camp's regional scope (lifted to edge, §5 row 9e) |
| `efficacy_in` | Camp | Region | Camp's regional efficacy scope |
| `supersedes` | Claim, Problem | Claim, Problem | Version replacement |
| `addresses` | Response, Camp | Problem | Intervention target |
| `driven_by` | Problem | Driver | Causal attribution |
| `part_of` | Problem | Problem | Hierarchical decomposition |
| `parent` | IbisNode | IbisNode | IBIS tree structure |
| `tensions_with` | Camp | Camp | Symmetric ideological tension (P18) |
| `manifests_in` | Pattern | Region | Regions exhibiting the pattern (≥2 required, P8) |
| `claim_ids` | Pattern | Claim | Claims constituting evidence for the pattern |
| `actor_ref` | Response | Actor | Optional typed actor cross-reference |

### 3.4 Region taxonomy

`Region` is a tiered enum:

```
RegionalCouncil  ∪  TerritorialAuthority  ∪  National
```

TA-level disaggregation is deferred until ≥3 regions carry TA-level data. Iwi/rohe is
a *parallel* spatial axis, not a subdivision of the regional council hierarchy.

---

## 4. Invariant system

18 cross-entity predicates are enforced by `content/_schema/invariants.py` at lint time.
Severity is either **error** (blocks merge) or **warning** (logged; does not block).

### §3.1 Structural integrity
| ID | Predicate | Severity |
|---|---|---|
| P1 | `p1_referential_closure` — every cross-entity ID reference resolves to a loaded entity | error |
| P10 | `p10_supersession_acyclicity` — `supersedes` graph is acyclic | error |
| P11 | `p11_supersession_freshness` — superseded entities carry a `deprecated_on` date | error |

### §3.2 Provenance discipline
| ID | Predicate | Severity |
|---|---|---|
| P2 | `p2_claim_must_cite` — every Claim has ≥1 `evidenced_by` Source | error |
| P14 | `p14_methodology_registry_closure` — every `methodology_tags` value exists in the registry | error |
| P16 | `p16_methodology_for_quantitative` — quantitative Claims carry ≥1 `methodology_tags` | error |

### §3.3 Subgraph completeness
| ID | Predicate | Severity |
|---|---|---|
| P3 | `p3_problem_completeness` — every Problem has ≥1 Driver, ≥1 Camp, ≥1 Claim | error |
| P4 | `p4_camp_completeness` — every theme has ≥2 distinct Camps | error |

### §3.4 Region scoping coherence
| ID | Predicate | Severity |
|---|---|---|
| P6′ | `p6_prime_national_coherence` — `national_assertion: true` claims are not tagged with any single region | error |
| P7′ | `p7_prime_region_mention_coherence` — `region_mentions` entries are valid Region enum values | error |
| P8 | `p8_pattern_plural_manifestation` — every Pattern `manifests_in` ≥2 regions | error |

### §3.5 Comparison-claim invariant
| ID | Predicate | Severity |
|---|---|---|
| P5′ | `p5_prime_comparison_consistency` — comparison claims (classes A–E) carry singleton `scoped_to`; warning while ≤2 regions populated, error thereafter | error* |

Comparison classes detected by regex:
- **A** — degree comparative + "than" (higher than, fewer than, …)
- **B** — "compared to/with"
- **C** — "relative to"
- **D** — superlative over named set (highest of, most among, …)
- **E** — "versus" / "vs."

Class F (gap/disparity language) is excluded due to high false-positive rate; revisit
after ≥3 regions surface gap-language slippage.

### §3.6 Indicator–Claim coupling
| ID | Predicate | Severity |
|---|---|---|
| P9 | `p9_indicator_unit_coherence` — Indicator units are consistent within a time-series | error |

### §3.7 IBIS structural typing
| ID | Predicate | Severity |
|---|---|---|
| P12 | `p12_ibis_parent_typing` — IBIS child nodes attach only to valid parent types (Issue → Position → Argument) | error |
| P13 | `p13_position_pluralism` — every IBIS Issue has ≥2 Positions | warning |

### §3.8 Figure–narrative cross-reference
| ID | Predicate | Severity |
|---|---|---|
| P15 | `p15_figure_in_narrative` — every `figure_id` referenced in a narrative exists in the entity | error |

### §3.9 Symmetric edges
| ID | Predicate | Severity |
|---|---|---|
| P18 | `p18_camp_tensions_symmetry` — `tensions_with` edges are bidirectional | error |

### §3.10 Iwi engagement
| ID | Predicate | Severity |
|---|---|---|
| P17 | `p17_iwi_engagement_note` — themes with iwi spatial relevance carry an engagement note | warning |

---

## 5. Methodology registry

The registry lives in `content/_schema/methodology.schema.json` and `methodology/`
entity YAML files per region. All `methodology_tags` values must resolve to a registry
entry (P14). As of 2026-Q2 the registry contains **15 named methods** across 5 groups:

| Group | Entries |
|---|---|
| Statistical | `descriptive_statistics_v1`, `regression_analysis_v1`, `spatial_analysis_v1` |
| Comparative | `comparative_case_study_v1`, `benchmarking_v1`, `cross_regional_comparison_v1` |
| Qualitative | `thematic_analysis_v1`, `document_analysis_v1`, `expert_elicitation_v1`, `policy_mapping_v1` |
| Causal | `counterfactual_analysis_v1`, `driver_timescale_v1` |
| Institutional | `response_sector_typology_v1`, `actor_institutional_typology_v1`, `systematic_review_v1` |

Methodology IDs take the fully-prefixed form `methodology.<slug>_vN`. Version increments
are backward-incompatible; new slugs extend the registry rather than mutating existing
entries.

---

## 6. Source citation requirements

Every Claim must satisfy P2 (`evidenced_by` ≥1 Source). The citation architecture is
**Claim-mediated** (P3 architecture, ratified 2026-04-25): there are no direct
Problem→Source `cites` edges. Source entities carry:

- `id` — `source.<slug>` format
- `title` — full bibliographic title
- `url` — canonical URL or DOI
- `accessed` — ISO 8601 date of access
- `publisher` — issuing organisation
- `type` — one of: `{report, dataset, legislation, academic, news, official_statistics}`

Sources are region-scoped where the issuing authority is regional; national and
international sources are shared across regions.

---

## 7. Authorship regime

All entity YAML files in this corpus are authored by **Luke Simmons** unless otherwise
noted in the entity's `author` field. The authorship regime is:

- **Initial corpus**: human-authored from primary sources; no LLM-generated factual
  claims are published without PI review and source verification.
- **Draft extraction**: where LLM assistance is used at the extraction boundary, output
  is validated against `content/_schema/` via Pydantic models generated from JSON
  Schema, then reviewed by the PI before commit.
- **Quantitative claims**: must carry ≥1 `methodology_tags` entry (P16) and cite a
  primary statistical source (P2).

---

## 8. Lint-gate process

The lint gate must pass before any region corpus is merged:

```
python content/<region>/tools/lint.py
```

The gate runs:
1. **JSON Schema validation** — all entity YAML files validated against their
   corresponding `content/_schema/*.schema.json` (Draft 2020-12, `$ref` closure).
2. **Invariant check** — `content/_schema/invariants.py::run_all(graph)` executed;
   any `result.errors` list item causes a non-zero exit.
3. **Route smoke test** — Flask test client verifies HTTP 200 on index + all section +
   all leaf URLs for the region.

Warnings (`result.warnings`) are logged but do not block merge. All 16 regions passed
the full lint gate at 0 errors / 0 warnings as of 2026-04-26.

---

## 9. Pattern (national rollup) methodology

Patterns are cross-regional recurring structures authored at `content/nz/data/pattern/`.
A Pattern is admitted when:

- It `manifests_in` ≥2 regions (P8); soft threshold ≥4 recommended for publication.
- It carries ≥1 `claim_ids` pointing to real, P1-clean Claim entities.
- It passes the lint gate for `content/nz/`.

Patterns are *projections* over the regional entity graph, not a separate data
collection. National rollup threshold for public display lives in the rendering layer
(`content/nz/tools/query.py`), not in the schema.

---

## 10. Versioning and archival

Corpus snapshots are archived quarterly via `scripts/archive.py` and
`scripts/deploy.py`. Archives are committed to `archives/YYYY-QN/` in git and merged
into `_site/archives/` at deploy time. Each archive is citable using the SEP citation
format rendered by `templates/_partials/cite.html`:

> Simmons, L. (YYYY). *[Theme] — [Region]*. lukesimmonsnz.kiwi. Archived
> YYYY-QN. `https://lukesimmonsnz.kiwi/research/<region>/<theme>/`

Semantic versioning is not applied to individual entities; the corpus version is the
quarterly archive label (e.g., `2026-Q2`).

---

## 11. Known limitations

- **TA-level disaggregation** is not yet implemented; all data is at Regional Council
  granularity. TA-level expansion is gated on ≥3 regions reaching sufficient entity
  density.
- **Iwi/rohe spatial axis** is modelled via `region_mentions` and engagement notes
  (P17) but not yet as a queryable graph dimension.
- **Comparison-claim Class F** (gap/disparity language) is excluded from automated
  detection; manual review is required for gap-language claims.
- **Indicator time-series** entities exist in the schema but are sparsely populated in
  the 2026-Q2 corpus; P9 enforcement is therefore light at present.
- All claims reflect conditions as of their `evidenced_by` source dates. The
  corpus does not constitute legal, financial, or policy advice.
