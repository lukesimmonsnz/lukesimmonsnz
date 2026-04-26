# CLAUDE.md — persistent project memory

This file is loaded into context at the start of every Claude session that
works in this directory. Keep it tight; high signal-density; pointers to
deeper documents rather than restating them.

---

## 1. Project identity

This repository is the source for **lukesimmonsnz.kiwi**, a personal Flask
site deployed via Cloudflare Pages. Two parallel concerns live in this repo:

1. **The personal site** (stable) — blog, projects, contact, biography of
   David Roy Simmons, computer/climate/medical science research notes.
2. **The Auckland → Aotearoa research migration** (active development) —
   scaling the existing Auckland regional research project into a unified
   national framework covering all 16 regions of New Zealand.

The active development arc is the second one. The first should not regress.

---

## 2. PI / Tool dynamic

Luke Simmons is the **Principal Investigator (PI)**. Claude is a
**Research Assistant / Computational Tool**. The dynamic:

- Defer to PI strategic direction. Do not redirect or relitigate ratified
  decisions.
- **Maintain the conceptual gap**: explain mathematical mechanics; do not
  hand over turn-key proofs or full implementations. Leave final derivations
  and hyperparameter choices for the PI.
- Use LaTeX for formal notation. Prefer equations and rigorous definitions
  over long-winded text.
- No unsolicited life advice or moralising.
- If the PI says **"Tool Mode"**, strip all conversational tone and return
  raw data / mathematical logic only.

---

## 3. Session discipline

Per Appendix A of `docs/MIGRATION-auckland-to-aotearoa.md`:

- **Tier-pin each session.** A session that does only claim-extraction pins
  Haiku; a session that does only orchestration pins Opus. Mixed-tier
  sessions force the highest tier used across all turns — wasteful.
- **Topic-pin each session.** Do not let a schema-design session bleed into
  a JSON Schema authoring session. Fresh context, narrow file-loading.
- **Default routing:** Haiku for mechanical extraction; Sonnet for design,
  judgement, drafting; Opus reserved for verification gates only.
- **Local fallback:** `qwen2.5:7b` (general) and `qwen2.5-coder:7b`
  (code-gen) via Ollama at `localhost:11434`. NLI / embeddings via the
  parallel `.venv-ml/` daemon at `localhost:5001` (when implemented).

---

## 4. Architecture, one paragraph

Flask app factory in `app.py` registers five blueprints: `main`, `research`
(`/research/`), `davidsimmons` (`/davidsimmons/`), `blog` (`/blog/`),
`auckland` (`/research/auckland/`). Content lives under `content/`:
`content/auckland/` is region-typed (typed entity YAML in `data/`,
JSON-Schema-validated, rendered to Markdown by
`content/auckland/tools/render.py`, lint-gated by
`content/auckland/tools/lint.py`); `content/blog/` is flat dated Markdown
with frontmatter. Templates in `templates/`. Internal docs (RFCs,
architecture notes, this file) in `docs/` — never in `content/`. Blog and
weekly-digest agents in `agent/` call local Ollama. Build deploys via
Cloudflare Wrangler. Detail in `docs/ARCHITECTURE.md`.

---

## 5. Aotearoa migration: ratified decisions

These are **frozen**. Do not reopen without explicit PI instruction.

| # | Decision |
|---|---|
| 1 | **Architecture**: unified-with-region-facets. Single Flask site, region-tagged typed entity graph, URL `/research/<region>/<theme>/`. National rollups are *projections* over Pattern nodes, not a separate region. |
| 2 | **Schema technology**: hybrid. JSON Schema in `content/_schema/*.schema.json` is canonical (declarative, language-agnostic). Pydantic models generated from JSON Schema, used only at the LLM extraction boundary for validate-and-retry. Cross-entity invariants as Python predicates in `content/_schema/invariants.py`. |
| 3 | **Schema location**: shared `content/_schema/`. Auckland's existing `content/auckland/schema/` will migrate into it, not the other way around. |
| 4 | **Methodology registry**: seeded from Auckland's existing implicit choices (currently encoded in `content/auckland/tools/lint.py`). |
| 5 | **Claim vs Evidence**: rename `evidence` → `claim`. Evidence is a **role** carried by edges (`evidenced_by`, `supports`), not a node type. |
| 6 | **Response vs Policy**: keep Auckland's `response` as-is; drop the migration doc's narrower `Policy` from the new inventory. |
| 7 | **Local model stack**: `qwen2.5:7b` and `qwen2.5-coder:7b` confirmed installed. Parallel `.venv-ml/` for torch / transformers / sentence-transformers; FastAPI daemon on `localhost:5001` for NLI and embeddings. Flask process never imports torch. |
| 8 | **Schema design open questions**: all nine §5 items in `docs/SCHEMA-DESIGN-aotearoa.md` ratified as PI-recommended (2026-04-25). Notable: IbisNode is a first-class entity; Region is a tiered enum (RegionalCouncil ∪ TerritorialAuthority ∪ National) with TA-level data deferred until ≥3 regions populated; iwi/rohe is a parallel spatial axis; Pattern's national-rollup threshold lives in the rendering layer, not the schema; `Response.actor` keeps the sector enum AND adds an optional typed Actor reference. |
| 9 | **Schema design gate findings ratified (2026-04-25)** — `docs/SCHEMA-DESIGN-aotearoa-gate-2026Q2.md`. (a) **Auckland delete-and-rebuild**: existing 69-entity corpus discarded; reauthored from clean slate against new `content/_schema/`. §5.9 rename-PR machinery obsolete. (b) P3 source-citation conjunct **Claim-mediated** (no Problem→Source `cites` edge). (c) **P5'**: comparison claim must be backed by Instance-level pinning (singleton `scoped_to`) per region; lint warns until 3rd region populated, then errors. (d) **P6' / P7'**: typed YAML fields `national_assertion: bool` and `region_mentions: list[Region]` replace NLP-style `nat`/`ment` predicates. (e) Camp's `applicable_in` / `efficacy_in` **lifted to edges** (uniform with Response's `applies_in`); \|R\| = 18. (f) Methodology registry **extended** with `driver_timescale_v1`, `response_sector_typology_v1`, `actor_institutional_typology_v1` (\|§4\| = 15). (g) `evidenced_by` exclusion of Indicator and Actor **semantically justified**. (h) **Notation cleanup pass scheduled** before Layer 1b begins. |
| 9 | **Schema design gate findings ratified (2026-04-25)** — `docs/SCHEMA-DESIGN-aotearoa-gate-2026Q2.md`. (a) **Auckland delete-and-rebuild**: existing 69-entity corpus discarded; reauthored from clean slate against new `content/_schema/`. §5.9 rename-PR machinery obsolete. (b) P3 source-citation conjunct **Claim-mediated** (no Problem→Source `cites` edge). (c) **P5'**: comparison claim must be backed by Instance-level pinning (singleton `scoped_to`) per region; lint warns until 3rd region populated, then errors. (d) **P6' / P7'**: typed YAML fields `national_assertion: bool` and `region_mentions: list[Region]` replace NLP-style `nat`/`ment` predicates. (e) Camp's `applicable_in` / `efficacy_in` **lifted to edges** (uniform with Response's `applies_in`); \|R\| = 18. (f) Methodology registry **extended** with `driver_timescale_v1`, `response_sector_typology_v1`, `actor_institutional_typology_v1` (\|§4\| = 15). (g) `evidenced_by` exclusion of Indicator and Actor **semantically justified**. (h) **Notation cleanup pass scheduled** before Layer 1b begins. |

---

## 6. Aotearoa migration: layer status

Layers are dependency-ordered, not calendar-ordered. Each layer's
correctness is a precondition for the next.

| Layer | Description | Status |
|---|---|---|
| 0 | Ratify §1 architecture | **Done** (2026-04-25) |
| 0.5 | Verify local model stack | **Done** (2026-04-25) |
| 0.5b | Bootstrap parallel `.venv-ml/` + FastAPI daemon | **Done** (2026-04-25) |
| 1a | Schema design — typed-graph diagram + edge inventory + methodology seed | **Gate-closed** (2026-04-25) — `docs/SCHEMA-DESIGN-aotearoa-gate-2026Q2.md`; all findings ratified (§5 row 9). |
| 1a-cleanup | Notation pass over `SCHEMA-DESIGN-aotearoa.md` discharging gate's FORMAL items (P1, P10, P11, P12, P14, P15, P17) plus inlining ratified amendments (P3 Claim-mediation, P5', P6'/P7', edge lifts, three new methodology entries, `evidenced_by` justification) | **Done** (2026-04-25) |
| 1b | JSON Schema authoring from approved design | **Done** (2026-04-25) — 13 files in `content/_schema/`; all pass Draft202012Validator meta-schema check and `$ref` closure. `claim.schema.json` tail corruption (engagement_record_id.type truncated) repaired 2026-04-26; re-audited clean. |
| 1c | Cross-entity invariants in Python | **Done** (2026-04-26) — `content/_schema/invariants.py`; 18 predicates + 3 helpers + `run_all` orchestrator; 48-check audit clean. `methodology_tag` and `methodology.id` both use the full prefixed form `"methodology.<slug>_vN"` (Option C ratified 2026-04-26; `claim.schema.json`, `methodology.schema.json`, and P14 updated). `run_all` tail corruption (`else` body and two warning-predicate calls truncated) repaired 2026-04-26; full 19-symbol audit clean. |
| 2 | Refactor `blueprints/auckland.py` → `RegionBlueprintFactory` | **Gate-closed** (2026-04-26) — `blueprints/region.py` factory; `blueprints/auckland.py` reduced to one-liner; Opus gate passed all 14 checks. |
| 3 | National (`nz`) Pattern-rollup query function + template | **Done** (2026-04-26) — `content/nz/tools/query.py`; `blueprints/nz.py`; `templates/nz/{index,theme}.html`; Pattern corpus at `content/nz/data/pattern/`; 6-check smoke suite green. |
| 4a | Auckland corpus rebuild — reauthor all Auckland themes against `content/_schema/` (delete-and-rebuild posture, §5 row 9a) | **Gate-closed (2026-04-26)** — **426 entities** (51 Source, 22 Methodology, 123 Claim, 93 Driver, 91 Camp, 46 Problem); **426/426 JSON Schema OK; `run_all` 0 errors 0 warnings**. All 11 themes: 1 root + ≥3 children each. Opus corpus gate (§9 item 3) **PASSED 2026-04-26** — 14-check suite clean; PI sign-off required before merge. Notes: (a) inequality `income_polarisation` child added to reach 3 children; (b) entity IDs use `climate` slug (regex `[a-z0-9_.]` forbids hyphens) while `theme:` field carries `climate-adaptation` enum — schema-enforced, not an inconsistency. |
| 4b | Wellington as proof region (full §A.4 sequence) | Blocked on PI sign-off + merge of 4a |
| 5 | Quarterly archive CI job (SEP pattern) | Blocked on 4b |

**Update this table by hand as work progresses.** It is the truth-source
for "where are we right now".

---

## 7. Pointer files

| Concern | File |
|---|---|
| Aotearoa migration plan + Appendix A (model routing) | `docs/MIGRATION-auckland-to-aotearoa.md` |
| Schema design output (when produced) | `docs/SCHEMA-DESIGN-aotearoa.md` |
| Site architecture in detail | `docs/ARCHITECTURE.md` |
| Auckland data pipeline | `docs/AUCKLAND-DATA-PIPELINE.md` |
| Sitemap (auto-generated) | `docs/SITEMAP.md` |
| Cloudflare deploy notes | `docs/CLOUDFLARE-DEPLOY.md` |
| Auckland schema (current, will migrate) | `content/auckland/schema/*.schema.json` |
| Auckland lint (methodology source) | `content/auckland/tools/lint.py` |
| Auckland renderer | `content/auckland/tools/render.py` |
| Auckland graph loader | `content/auckland/tools/graph.py` |
| Blog agents | `agent/daily_post.py`, `agent/weekly_post.py` |

---

## 8. Open questions awaiting PI input

None currently open. Layer 1a design questions resolved in the 2026-04-25
ratification of `docs/SCHEMA-DESIGN-aotearoa.md` §5 (see §5 row 8). Gate
findings resolved 2026-04-25 (see §5 row 9). Next questions will surface
either during the Layer 1a-cleanup notation pass or once Layer 1b JSON
Schema authoring begins.

---

## 9. Verification gates yet to occur

Per §A.5 of the migration doc, Opus verification gates are non-negotiable
at these points. Do not bypass.

1. **Schema design gate** (end of Layer 1a): **COMPLETE** (2026-04-25) — see
   `docs/SCHEMA-DESIGN-aotearoa-gate-2026Q2.md`. All findings ratified per
   §5 row 9. Cleanup pass (Layer 1a-cleanup) scheduled before Layer 1b
   authoring begins.
2. **Blueprint refactor gate** (end of Layer 2): Opus verifies all current
   Auckland routes are byte-identical post-refactor.
3. **Schema migration gate** (end of Layer 1c / Layer 4a): **PASSED 2026-04-26** —
   426 entities, 0 schema errors, 0 invariant errors. All 11 themes structurally
   correct (1 root + ≥3 children each). Opus ran 14-check suite; PASS verdict issued.
   **PI sign-off required before merge to `main`.** Model pin: Opus.
4. **Per-region-theme content gates** (recurring, one per PR in steady-state).

PI signs off on each gate output before merge.

---

## 10. Hard rules

- **Do not place RFCs, planning docs, or methodology notes in `content/`**.
  Content/ is for routed, user-facing pages only. Internal docs go in
  `docs/`.
- **Do not pre-empt blueprint scaffolding** for `nz` or other regions
  before Layer 2 (the `RegionBlueprintFactory` refactor).
- **Do not author JSON Schema** before the design session output is
  approved by PI.
- **Do not merge to `main`** without the appropriate Opus gate.
- **Do not modify `content/auckland/`** during the schema migration
  without first verifying the lint passes in a dry-run.
- **Do not touch `data/messages.jsonl`** (contact-form submissions —
  treated as user data; gitignored).
- **Do not write to `_site/`** by hand — it is the build output, not source.
- **Working branch**: `aotearoa-migration`. Do not commit to `main`
  during the migration arc.

---

## 11. Working environment

- Hardware scope: Local PC, RTX 3070 (8 GB VRAM), standard consumer
  workstation. No cloud-scale anything.
- OS: Windows. `.bat` launchers (`start.bat`, `stop.bat`) for the Flask
  dev server. Line endings: `core.autocrlf = false` to preserve mixed
  CRLF/LF.
- Python venv: `.venv/` (Flask + lint stack only — small, fast).
- ML venv (when bootstrapped): `.venv-ml/` (torch, transformers,
  sentence-transformers — isolated from Flask).
- Ollama at `localhost:11434`; ML daemon at `localhost:5001` (when
  implemented).

---

## 12. Bootstrap for design / authoring sessions

When opening a new fresh session for Aotearoa migration work, paste a
short prompt of this shape:

> Mode: Sonnet (or Haiku / Opus per layer)
> Scope: Layer X — [one-line description]
> Inputs to load: [narrow file list]
> Output: [single artifact name]
> Constraints: honour ratified decisions in CLAUDE.md §5; do not
> relitigate. Maintain implementation gap. Mathematical predicates
> over the graph as first-order logic.

The bootstrap stays short because this `CLAUDE.md` carries the rest.
