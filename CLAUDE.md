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

---

## 6. Aotearoa migration: layer status

Layers are dependency-ordered, not calendar-ordered. Each layer's
correctness is a precondition for the next.

| Layer | Description | Status |
|---|---|---|
| 0 | Ratify §1 architecture | **Done** (2026-04-25) |
| 0.5 | Verify local model stack | **Done** (2026-04-25) |
| 0.5b | Bootstrap parallel `.venv-ml/` + FastAPI daemon | **Not started** |
| 1a | Schema design — typed-graph diagram + edge inventory + methodology seed | **Not started** — next session |
| 1b | JSON Schema authoring from approved design | Blocked on 1a |
| 1c | Cross-entity invariants in Python | Blocked on 1a |
| 2 | Refactor `blueprints/auckland.py` → `RegionBlueprintFactory` | Blocked on 1 |
| 3 | National (`nz`) Pattern-rollup query function + template | Blocked on 1 |
| 4 | Wellington as proof region (full §A.4 sequence) | Blocked on 2 + 3 |
| 5 | Quarterly archive CI job (SEP pattern) | Blocked on 4 |

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

- **`IbisNode` shape** (Layer 1a, design session): first-class node type, or
  a role any `Claim` plays within an `Issue` subgraph? Are `Issue`s
  separate entities, or `Problem` nodes flagged `is_contested: true`?
  Mathematical bar: a separate type doubles type count for marginal gain
  if Issues map cleanly to Problems.
- **Region taxonomy granularity**: 16 regions only, or 16 regions + 67
  Territorial Authorities as sub-regions in the same enum?
- **National threshold**: at how many regions does a Pattern qualify as
  "national" for `/research/nz/` rollup pages? (Doc suggests ≥ 10 as a
  rule of thumb; not ratified.)

---

## 9. Verification gates yet to occur

Per §A.5 of the migration doc, Opus verification gates are non-negotiable
at these points. Do not bypass.

1. **Schema design gate** (end of Layer 1a): Opus verifies the typed-graph
   design is internally consistent, every cross-entity invariant is
   stated as a first-order predicate, and the design closes the §2 §A.5
   epistemic gap.
2. **Blueprint refactor gate** (end of Layer 2): Opus verifies all current
   Auckland routes are byte-identical post-refactor.
3. **Schema migration gate** (end of Layer 1c, when Auckland migrates into
   shared schema): Opus verifies all 69 existing Auckland entities still
   validate.
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
