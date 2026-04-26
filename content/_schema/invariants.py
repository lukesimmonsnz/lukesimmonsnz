"""Cross-entity invariants for the Aotearoa knowledge graph.

Each function discharges one first-order predicate from §3 of
docs/SCHEMA-DESIGN-aotearoa.md.  JSON Schema handles intra-entity
constraints; this module handles the cross-entity residue that a
JSON Schema validator cannot reach.

Predicate numbering is STABLE — do not renumber.

Severity key
------------
  error   — P1, P2, P3, P4, P5′(*), P6′, P7′, P8, P9, P10, P11,
             P12, P14, P15, P16, P18
  warning — P13  (soft by design, §3.7)
             P17  (soft pending Mana Ōrite governance workflow, §3.10)
  (*)     — P5′ is a *warning* while ``graph.populated_region_count() ≤ 2``;
             it promotes to *error* once the third region is populated
             (CLAUDE.md §5 row 9c, ratified 2026-04-25).

Predicate index
---------------
  §3.1  Structural integrity
        P1   p1_referential_closure
        P10  p10_supersession_acyclicity
        P11  p11_supersession_freshness
  §3.2  Provenance discipline
        P2   p2_claim_must_cite
        P14  p14_methodology_registry_closure
        P16  p16_methodology_for_quantitative
  §3.3  Subgraph completeness
        P3   p3_problem_completeness
        P4   p4_camp_completeness
  §3.4  Region scoping coherence
        P6′  p6_prime_national_coherence
        P7′  p7_prime_region_mention_coherence
        P8   p8_pattern_plural_manifestation
  §3.5  Comparison-claim invariant
        P5′  p5_prime_comparison_consistency
  §3.6  Indicator–Claim coupling
        P9   p9_indicator_unit_coherence
  §3.7  IBIS structural typing
        P12  p12_ibis_parent_typing
        P13  p13_position_pluralism          (warning)
  §3.8  Figure–narrative cross-reference
        P15  p15_figure_in_narrative
  §3.9  Symmetric edges
        P18  p18_camp_tensions_symmetry
  §3.10 Iwi engagement
        P17  p17_iwi_engagement_note         (warning)

Usage
-----
    from content._schema.invariants import run_all
    result = run_all(graph)
    if result.errors:
        sys.exit(1)
"""

from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from datetime import date
from typing import Protocol


# ---------------------------------------------------------------------------
# Comparison-statement patterns  (§5a Rule R3 of MIGRATION doc).
#
# Migration doc line 315 seeds Class A; doc line 337 shows the list form.
# Classes A–E ratified by PI 2026-04-26.
#
# Class F — gap/disparity language — deliberately excluded.
# Pattern would be: r"\b(gap|disparity|difference|differential)\b"
# Exclusion reason: high false-positive rate on non-comparative uses
# ("a gap in the evidence base").  Revisit once Wellington authoring
# surfaces gap-language comparison claims that slip through A–E.
# ---------------------------------------------------------------------------

_COMPARISON_PATTERNS: list[re.Pattern[str]] = [
    # Class A — degree comparative + "than"  (migration doc line 315 seed)
    re.compile(
        r"\b(more|less|higher|lower|greater|fewer|larger|smaller"
        r"|worse|better|cheaper|costlier|faster|slower)\s+than\b",
        re.IGNORECASE,
    ),
    # Class B — "compared to/with"
    re.compile(r"\bcompared\s+(to|with)\b", re.IGNORECASE),
    # Class C — "relative to"
    re.compile(r"\brelative\s+to\b", re.IGNORECASE),
    # Class D — superlative over named set
    re.compile(
        r"\b(highest|lowest|most|fewest|greatest|least)\s+(of|among|across|in)\b",
        re.IGNORECASE,
    ),
    # Class E — "versus" / "vs"
    re.compile(r"\b(versus|vs\.?)\b", re.IGNORECASE),
]


# ---------------------------------------------------------------------------
# Graph protocol — invariant functions consume this interface only.
# The concrete Graph class (built in Layer 2+) must satisfy it.
# ---------------------------------------------------------------------------

class Graph(Protocol):
    """Typed interface consumed by all invariant functions.

    The concrete implementation is the graph builder's responsibility
    (Layer 2).  Every method/attribute here is the minimal surface the
    18 predicates require.
    """

    entities: dict[str, dict]
    """All loaded entities keyed by their ``id`` string."""

    def all_of_type(self, entity_type: str) -> list[dict]:
        """Return all entities whose ``id`` prefix matches *entity_type*.

        E.g. ``all_of_type("claim")`` returns every entity whose ``id``
        starts with ``"claim."``.
        """
        ...

    def referenced_ids(self, entity: dict) -> set[str]:
        """Return the union of all ID-valued attribute values in *entity*.

        Operationalises ``refs(v)`` from §0 of the schema design doc:
        collects every value (and list element) that matches the pattern
        ``^<type>\\.`` across all known ID-bearing fields.
        """
        ...

    def populated_region_count(self) -> int:
        """Return the number of distinct Region values present in the graph.

        "Populated" means the region appears in at least one entity's
        ``scoped_to``, ``manifests_in``, or ``applies_in`` field.
        Used by the P5′ severity warmup gate (warns at ≤ 2, errors at ≥ 3).
        """
        ...


# ---------------------------------------------------------------------------
# Run-all result container
# ---------------------------------------------------------------------------

@dataclass
class LintResult:
    """Collected output of ``run_all``.

    ``errors``   — must be empty for CI to pass.
    ``warnings`` — surfaced to the author; non-blocking.
    """

    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _is_quantitative(claim: dict) -> bool:
    """True iff *claim* carries a non-null ``value`` field.

    Implements the derived ``quantitative`` predicate from ratified §5.5:
    a Claim is implicitly quantitative iff ``value ≠ ⊥`` (no stored bool;
    the field is ``["number", "string", "null"]`` in the JSON Schema).
    Used by P16.
    """
    return claim.get("value") is not None


def _is_comparison(statement: str) -> bool:
    """True iff *statement* matches any pattern in ``_COMPARISON_PATTERNS``.

    Operationalises ``cmp(s)`` from §3 of the schema design.
    Used by P5′.
    """
    return any(p.search(statement) for p in _COMPARISON_PATTERNS)


def _as_of_date(claim: dict) -> date | None:
    """Extract the best available temporal marker from *claim*.

    Preference order:
      1. ``last_verified`` — already an ISO 8601 date string.
      2. Last year parseable from ``time_period``
         (e.g. ``"FY2024"`` → 2024, ``"2018–2023"`` → 2023).

    Returns ``None`` when neither field provides a resolvable date.
    A ``None`` result causes P11 to skip the freshness check for that
    pair (not an error — emit a warning if desired).
    Used by P11.
    """
    lv = claim.get("last_verified")
    if lv:
        try:
            return date.fromisoformat(lv)
        except ValueError:
            pass

    tp = claim.get("time_period")
    if tp:
        # Collect all 4-digit years in the range 1900–2099; take the last.
        # Use digit-boundary assertions (not \b) so "FY2024" → 2024 works
        # (\b fails: both 'Y' and '2' are word chars, no boundary between them).
        years = re.findall(r"(?<!\d)(19\d{2}|20\d{2})(?!\d)", str(tp))
        if years:
            return date(int(years[-1]), 12, 31)

    return None


# ---------------------------------------------------------------------------
# §3.1  Structural integrity
# ---------------------------------------------------------------------------

def p1_referential_closure(graph: Graph) -> list[str]:
    """P1 — Referential closure.

    ∀ v ∈ V. ∀ u ∈ refs(v). u ∈ V

    Every ID-valued attribute across all entity types must resolve to an
    entity that exists in the loaded graph.

    Lifted from Auckland ``_check_referenced_ids_exist``; applies to the
    full new ID-prefix taxonomy:
    ``actor.``, ``camp.``, ``claim.``, ``driver.``, ``ibis.``,
    ``indicator.``, ``methodology.``, ``pattern.``, ``problem.``,
    ``response.``, ``source.``.

    Methodology: ``graph_referential_closure_v1``.

    Returns a list of error strings, one per dangling reference.
    """
    errors: list[str] = []
    for entity in graph.entities.values():
        for ref_id in graph.referenced_ids(entity):
            if ref_id not in graph.entities:
                errors.append(
                    f"P1: '{entity['id']}' references unknown entity '{ref_id}'"
                )
    return errors


def p10_supersession_acyclicity(graph: Graph) -> list[str]:
    """P10 — Supersession acyclicity.

    ¬∃ k ≥ 2. ∃ c₁, …, cₖ ∈ V_Claim.
        (∀ i ∈ {1, …, k−1}: (cᵢ, cᵢ₊₁) ∈ E_supersedes) ∧ cₖ = c₁

    The directed graph induced by ``claim["supersedes_id"]`` must be a
    DAG.  Detect cycles via depth-first search (or Kahn's algorithm over
    the ID → ID adjacency).

    Field read: ``claim["supersedes_id"]``  (nullable str ``^claim\\.``).

    Returns a list of error strings; each entry names the cycle
    (comma-separated member IDs).
    """
    # Build the successor map (each node has at most one successor —
    # a functional graph — so cycle detection is a simple chain-follow).
    succ: dict[str, str] = {}
    for c in graph.all_of_type("claim"):
        sid = c.get("supersedes_id")
        if sid:
            succ[c["id"]] = sid

    errors: list[str] = []
    visited: set[str] = set()     # nodes whose full chain is resolved
    in_cycle: set[str] = set()    # nodes already reported in a cycle

    for start in succ:
        if start in visited or start in in_cycle:
            continue

        # Walk the chain, recording the order for cycle extraction.
        path: list[str] = []
        path_set: set[str] = set()
        cur = start

        while cur in succ and cur not in visited and cur not in path_set:
            path.append(cur)
            path_set.add(cur)
            cur = succ[cur]

        if cur in path_set:
            # cur is the entry point of a cycle; extract the cycle portion.
            cycle_start_idx = path.index(cur)
            cycle = path[cycle_start_idx:]
            key = frozenset(cycle)
            if key not in in_cycle:
                in_cycle.update(cycle)
                errors.append(
                    f"P10: supersession cycle detected: {', '.join(cycle)}"
                )

        visited.update(path)

    return errors


def p11_supersession_freshness(graph: Graph) -> list[str]:
    """P11 — Supersession monotone freshness.

    ∀ (c, c′) ∈ E_supersedes.  as_of(c) > as_of(c′)

    Convention (§2 row 13): the source vertex is the *newer* Claim.
    For each supersession edge the superseding Claim's temporal marker
    must be strictly later than the superseded Claim's.

    ``as_of`` is resolved by ``_as_of_date``; if either Claim lacks a
    temporal marker the pair is skipped (not an error; emit a warning if
    desired).

    Fields read: ``claim["supersedes_id"]``, ``claim["last_verified"]``,
    ``claim["time_period"]``.

    Returns a list of error strings for monotonicity violations.
    """
    claims_by_id: dict[str, dict] = {
        c["id"]: c for c in graph.all_of_type("claim")
    }
    errors: list[str] = []

    for claim in claims_by_id.values():
        sid = claim.get("supersedes_id")
        if not sid:
            continue
        superseded = claims_by_id.get(sid)
        if superseded is None:
            continue  # P1 handles dangling reference

        newer_date = _as_of_date(claim)
        older_date = _as_of_date(superseded)

        if newer_date is None or older_date is None:
            continue  # Undated pair: skipped per spec

        if newer_date <= older_date:
            errors.append(
                f"P11: '{claim['id']}' supersedes '{sid}' but temporal marker "
                f"is not strictly later ({newer_date} ≤ {older_date})"
            )

    return errors


# ---------------------------------------------------------------------------
# §3.2  Provenance discipline
# ---------------------------------------------------------------------------

def p2_claim_must_cite(graph: Graph) -> list[str]:
    """P2 — Claim must cite a source.

    ∀ c ∈ V_Claim. ∃ s ∈ V_Source. (c, s) ∈ E_cites

    ``source_ids`` has ``minItems: 1`` in the JSON Schema; this predicate
    is the cross-entity complement — it checks that the cited IDs
    *resolve* to Source entities (P2 ∩ P1 specialisation).

    Lifted from Auckland ``_check_evidence_has_source``.
    Methodology: ``claim_must_cite_v1``.

    Field read: ``claim["source_ids"]``  (list[str] ``^source\\.``).

    Returns a list of error strings, one per Claim with an unresolved or
    absent source.
    """
    source_ids: set[str] = {s["id"] for s in graph.all_of_type("source")}
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        cid = claim["id"]
        cited = claim.get("source_ids", [])
        for sid in cited:
            if sid not in source_ids:
                errors.append(
                    f"P2: claim '{cid}' cites '{sid}' which is not in V_Source"
                )

    return errors


def p14_methodology_registry_closure(graph: Graph) -> list[str]:
    """P14 — Methodology registry closure.

    ∀ c ∈ V_Claim with c.methodology_tag ≠ ⊥.
        ∃ μ ∈ V_Methodology.  id(μ) = c.methodology_tag

    A specialisation of P1 for ``methodology_tag``, stated separately for
    clarity.  At graph-build time ``methodology_tag`` is materialised as
    ``(c, μ) ∈ E_follows``; this predicate catches dangling tags before
    that step succeeds.

    Fields read: ``claim["methodology_tag"]``  (nullable str
    ``^methodology\\.[a-z][a-z0-9_]*_v[0-9]+$``), ``methodology["id"]``
    (same pattern — ratified Option C, 2026-04-26).

    Returns a list of error strings, one per unresolved methodology tag.
    """
    # Both claim.methodology_tag and methodology.id use the full prefixed form
    # "methodology.<slug>_v<N>" (ratified Option C, 2026-04-26). Direct lookup.
    methodology_ids: set[str] = {
        m["id"] for m in graph.all_of_type("methodology")
    }
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        tag = claim.get("methodology_tag")
        if tag and tag not in methodology_ids:
            errors.append(
                f"P14: claim '{claim['id']}' methodology_tag '{tag}' "
                f"not in V_Methodology"
            )

    return errors


def p16_methodology_for_quantitative(graph: Graph) -> list[str]:
    """P16 — Methodology pinning for quantitative claims.

    ∀ c ∈ V_Claim. quantitative(c) → c.methodology_tag ≠ ⊥

    A Claim is quantitative iff ``value ≠ null`` (see ``_is_quantitative``).
    This predicate applies to *all* quantitative Claims; comparison Claims
    are additionally covered by P5′.

    Fields read: ``claim["value"]``  (number | string | null),
    ``claim["methodology_tag"]``  (nullable str).

    Returns a list of error strings, one per quantitative Claim missing a
    ``methodology_tag``.
    """
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        if _is_quantitative(claim) and not claim.get("methodology_tag"):
            errors.append(
                f"P16: quantitative claim '{claim['id']}' "
                f"(value={claim['value']!r}) has no methodology_tag"
            )

    return errors


# ---------------------------------------------------------------------------
# §3.3  Subgraph completeness  (Auckland methodology, lifted to edge model)
# ---------------------------------------------------------------------------

def p3_problem_completeness(graph: Graph) -> list[str]:
    """P3 — Problem completeness.

    ∀ p ∈ V_Problem.
        (∃ d ∈ V_Driver.  (d, p) ∈ E_causes)       — ≥1 causal Driver
      ∧ (∃ k ∈ V_Camp.    (k, p) ∈ E_addresses)    — ≥1 Camp targeting p
      ∧ (∃ c ∈ V_Claim.   (p, c) ∈ E_evidenced_by) — ≥1 supporting Claim
      ∧ (∃ c ∈ V_Claim, s ∈ V_Source.
             (p, c) ∈ E_evidenced_by ∧ (c, s) ∈ E_cites)
                                                    — source reachable via Claim

    The fourth conjunct is the Claim-mediated source citation ratified
    2026-04-25 (CLAUDE.md §5 row 9b).  The inbound Driver/Camp existence
    must be checked here because those edges originate on Driver and Camp
    — JSON Schema cannot express them from the Problem side.

    Lifted from Auckland ``_check_problem_minimums`` +
    ``_check_evidence_has_source``; updated to the edge-based model.
    Methodology: ``problem_subgraph_minimum_v1``.

    Fields read (inbound edge reconstruction):
      ``driver["problem_ids"]``, ``camp["addresses"]``,
      ``problem["claim_ids"]``, ``claim["source_ids"]``.

    Returns a list of error strings, one per unsatisfied conjunct per
    Problem.
    """
    problems: dict[str, dict] = {
        p["id"]: p for p in graph.all_of_type("problem")
    }
    claims: dict[str, dict] = {
        c["id"]: c for c in graph.all_of_type("claim")
    }
    source_ids: set[str] = {s["id"] for s in graph.all_of_type("source")}

    # Build inbound Driver index: problem_id → set of driver IDs
    problem_to_drivers: dict[str, set[str]] = {pid: set() for pid in problems}
    for d in graph.all_of_type("driver"):
        for pid in d.get("problem_ids", []):
            if pid in problem_to_drivers:
                problem_to_drivers[pid].add(d["id"])

    # Build inbound Camp index: problem_id → set of camp IDs
    problem_to_camps: dict[str, set[str]] = {pid: set() for pid in problems}
    for k in graph.all_of_type("camp"):
        for pid in k.get("addresses", []):
            if pid in problem_to_camps:
                problem_to_camps[pid].add(k["id"])

    errors: list[str] = []

    for pid, problem in problems.items():
        # Conjunct 1: ≥1 inbound Driver
        if not problem_to_drivers[pid]:
            errors.append(
                f"P3: problem '{pid}' has no inbound Driver "
                f"(no driver.problem_ids references it)"
            )

        # Conjunct 2: ≥1 inbound Camp
        if not problem_to_camps[pid]:
            errors.append(
                f"P3: problem '{pid}' has no inbound Camp "
                f"(no camp.addresses references it)"
            )

        # Conjuncts 3 & 4: ≥1 Claim that resolves, with a resolvable Source
        claim_id_list: list[str] = problem.get("claim_ids", [])
        resolving_claims: list[str] = [
            cid for cid in claim_id_list if cid in claims
        ]

        # Conjunct 3: ≥1 claim in V_Claim (cross-entity; JSON Schema guards
        # minItems:1 but not existence in the graph).
        if not resolving_claims:
            errors.append(
                f"P3: problem '{pid}' has no claim_ids that resolve to V_Claim"
            )

        # Conjunct 4: Claim-mediated source reachability
        if resolving_claims:
            has_sourced_claim = any(
                any(sid in source_ids for sid in claims[cid].get("source_ids", []))
                for cid in resolving_claims
            )
            if not has_sourced_claim:
                errors.append(
                    f"P3: problem '{pid}' has no Claim with a resolvable Source "
                    f"(Claim-mediated source reachability not satisfied)"
                )

    return errors


def p4_camp_completeness(graph: Graph) -> list[str]:
    """P4 — Camp completeness.

    ∀ k ∈ V_Camp.
        (∃ p ∈ V_Problem. (k, p) ∈ E_addresses)
      ∧ |flagship_moves(k)| ≥ 1
      ∧ |tensions(k)| ≥ 1
      ∧ |interventions(k)| ≥ 1

    The cardinality conjuncts are also ``minItems: 1`` in the JSON Schema;
    the cross-entity ``(k, p) ∈ E_addresses`` existence — whether the
    referenced Problem is in V_Problem — is the Python residue.

    Lifted from Auckland ``_check_camp_completeness``.
    Methodology: ``camp_completeness_v1``.

    Fields read: ``camp["addresses"]``  (list[str] ``^problem\\.``),
    ``camp["flagship_moves"]``, ``camp["tensions"]``,
    ``camp["interventions"]``.

    Returns a list of error strings, one per unsatisfied conjunct per Camp.
    """
    problem_ids: set[str] = {p["id"] for p in graph.all_of_type("problem")}
    errors: list[str] = []

    for camp in graph.all_of_type("camp"):
        cid = camp["id"]
        addresses: list[str] = camp.get("addresses", [])

        # Cross-entity conjunct: ≥1 referenced Problem exists in V_Problem
        if not any(pid in problem_ids for pid in addresses):
            errors.append(
                f"P4: camp '{cid}' addresses no Problem in V_Problem "
                f"(addresses={addresses})"
            )

        # Intra-entity conjuncts (belt-and-suspenders; JSON Schema also guards):
        if not camp.get("flagship_moves"):
            errors.append(f"P4: camp '{cid}' has no flagship_moves")
        if not camp.get("tensions"):
            errors.append(f"P4: camp '{cid}' has no tensions")
        if not camp.get("interventions"):
            errors.append(f"P4: camp '{cid}' has no interventions")

    return errors


# ---------------------------------------------------------------------------
# §3.4  Region scoping coherence
# ---------------------------------------------------------------------------

def p6_prime_national_coherence(graph: Graph) -> list[str]:
    """P6′ — National coherence (typed YAML field; ratified 2026-04-25).

    ∀ c ∈ V_Claim.  c.national_assertion → "nz" ∈ scoped_to(c)

    If ``national_assertion`` is ``true``, the region value ``"nz"`` must
    appear in ``scoped_to``.  Replaces the former NLP helper ``nat(s)``.

    Fields read: ``claim["national_assertion"]``  (bool, default false),
    ``claim["scoped_to"]``  (list[Region], minItems 1).

    Returns a list of error strings, one per violating Claim.
    """
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        if claim.get("national_assertion", False):
            scoped_to: list[str] = claim.get("scoped_to", [])
            if "nz" not in scoped_to:
                errors.append(
                    f"P6′: claim '{claim['id']}' has national_assertion=true "
                    f"but 'nz' ∉ scoped_to {scoped_to}"
                )

    return errors


def p7_prime_region_mention_coherence(graph: Graph) -> list[str]:
    """P7′ — Region-mention coherence (typed YAML field; ratified 2026-04-25).

    ∀ c ∈ V_Claim, r ∈ Region.  r ∈ c.region_mentions → r ∈ scoped_to(c)

    Every region in ``region_mentions`` must also appear in ``scoped_to``.
    Replaces the former NLP helper ``ment(s, r)``.  A separate, down-
    gradeable lint warning may also perform canonical-name matching against
    ``statement`` to flag *missing* ``region_mentions`` entries; that check
    is not this predicate.

    Fields read: ``claim["region_mentions"]``  (list[Region], default []),
    ``claim["scoped_to"]``  (list[Region]).

    Returns a list of error strings, one per (Claim, region) pair that
    violates the subset relation.
    """
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        scoped_to: set[str] = set(claim.get("scoped_to", []))
        for region in claim.get("region_mentions", []):
            if region not in scoped_to:
                errors.append(
                    f"P7′: claim '{claim['id']}' region_mentions '{region}' "
                    f"but it is not in scoped_to {sorted(scoped_to)}"
                )

    return errors



def p8_pattern_plural_manifestation(graph: Graph) -> list[str]:
    """P8 - Pattern requires plural manifestation.

    For all pi in V_Pattern:
        |manifests_in(pi)| >= 2
      and (exists c in V_Claim. (pi, c) in E_evidenced_by)

    The minItems:2 cardinality on manifests_in is JSON-Schema-expressible;
    the existence of a resolving Claim in V_Claim is the Python residue.

    Type-defining axiom: a node manifesting in only one region is an
    Instance (Claim), not a Pattern.

    Fields read: ``pattern["manifests_in"]``,
    ``pattern["claim_ids"]``  (list[str] ``^claim\\.``, minItems 1).

    Returns a list of error strings, one per unsatisfied conjunct per
    Pattern.
    """
    claim_ids_in_graph: set[str] = {c["id"] for c in graph.all_of_type("claim")}
    errors: list[str] = []

    for pattern in graph.all_of_type("pattern"):
        pid = pattern["id"]

        # Belt-and-suspenders for |manifests_in| >= 2 (JSON Schema primary gate).
        manifests_in: list[str] = pattern.get("manifests_in", [])
        if len(manifests_in) < 2:
            errors.append(
                f"P8: pattern '{pid}' manifests_in has only "
                f"{len(manifests_in)} region(s) (minimum 2 -- type-defining axiom)"
            )

        # Python residue: exists Claim in claim_ids that resolves to V_Claim
        resolving = [
            cid for cid in pattern.get("claim_ids", [])
            if cid in claim_ids_in_graph
        ]
        if not resolving:
            errors.append(
                f"P8: pattern '{pid}' has no claim_ids that resolve to V_Claim"
            )

    return errors


# ---------------------------------------------------------------------------
# §3.5  Comparison-claim invariant
# ---------------------------------------------------------------------------

def p5_prime_comparison_consistency(graph: Graph) -> list[str]:
    """P5' - Cross-region comparison consistency (ratified 2026-04-25).

    For all c in V_Claim where cmp(statement(c)) and |scoped_to(c)| >= 2:
        (a) exists mu in V_Methodology. (c, mu) in E_follows
        (b) for all r in scoped_to(c):
              exists c' in V_Claim. scoped_to(c') = {r}
                                  and c'.methodology_tag = c.methodology_tag
                                  and c' != c

    Prevents methodology drift across regions in comparison claims.

    Severity warmup (CLAUDE.md §5 row 9c):
      populated_region_count() <= 2  -> messages are warnings
      populated_region_count() >= 3  -> messages are errors
    The caller (run_all) resolves severity; this function returns raw messages.

    Implementation: precompute (region, methodology_tag) -> [claim_id]
    singleton index; inner loop is O(1) per region.

    Fields read: ``claim["statement"]``, ``claim["scoped_to"]``,
    ``claim["methodology_tag"]``.

    Returns a list of message strings (caller classifies error vs warning).
    """
    claims: list[dict] = graph.all_of_type("claim")

    # Singleton index: (region, methodology_tag) -> [claim_id, ...]
    # restricted to claims with exactly one region in scoped_to.
    singleton_index: dict[tuple[str, str], list[str]] = defaultdict(list)
    for c in claims:
        scoped: list[str] = c.get("scoped_to", [])
        mtag: str | None = c.get("methodology_tag")
        if len(scoped) == 1 and mtag:
            singleton_index[(scoped[0], mtag)].append(c["id"])

    messages: list[str] = []

    for c in claims:
        stmt: str = c.get("statement", "")
        scoped: list[str] = c.get("scoped_to", [])

        if not (_is_comparison(stmt) and len(scoped) >= 2):
            continue

        cid: str = c["id"]
        mtag: str | None = c.get("methodology_tag")

        # Check (a): methodology_tag required for comparison claims
        if not mtag:
            messages.append(
                f"P5': comparison claim '{cid}' (|scoped_to|={len(scoped)}) "
                f"has no methodology_tag"
            )
            continue  # Cannot evaluate (b) without a methodology tag

        # Check (b): singleton Instance-level Claim per compared region
        for region in scoped:
            candidates: list[str] = singleton_index.get((region, mtag), [])
            if not any(candidate != cid for candidate in candidates):
                messages.append(
                    f"P5': comparison claim '{cid}' has no singleton "
                    f"Instance-level Claim scoped to {{'{region}'}} "
                    f"with methodology_tag='{mtag}'"
                )

    return messages


# ---------------------------------------------------------------------------
# §3.6  Indicator-Claim coupling
# ---------------------------------------------------------------------------

def p9_indicator_unit_coherence(graph: Graph) -> list[str]:
    """P9 - Indicator unit coherence.

    For all c in V_Claim, i in V_Indicator where (c, i) in E_measured_by:
        unit(c) = null  or  unit(c) = unit(i)

    A Claim that names an Indicator via measured_by_ids must either omit
    its own unit (symbolic Claims are permitted to) or agree with the
    Indicator's canonical unit string.

    Stronger formulations (dimensional analysis, SI normalisation) are
    deferred to Indicator v2.

    Fields read: ``claim["measured_by_ids"]``  (list[str] ``^indicator\\.``),
    ``claim["unit"]``  (nullable str),
    ``indicator["unit"]``  (str, required).

    Returns a list of error strings, one per (Claim, Indicator) unit mismatch.
    """
    indicators: dict[str, dict] = {
        i["id"]: i for i in graph.all_of_type("indicator")
    }
    errors: list[str] = []

    for claim in graph.all_of_type("claim"):
        claim_unit: str | None = claim.get("unit")
        if claim_unit is None:
            continue  # Absent unit is always valid

        for iid in claim.get("measured_by_ids", []):
            indicator = indicators.get(iid)
            if indicator is None:
                continue  # P1 catches the dangling reference

            ind_unit: str = indicator.get("unit", "")
            if ind_unit and claim_unit != ind_unit:
                errors.append(
                    f"P9: claim '{claim['id']}' unit='{claim_unit}' != "
                    f"indicator '{iid}' unit='{ind_unit}'"
                )

    return errors


# ---------------------------------------------------------------------------
# §3.7  IBIS structural typing
# ---------------------------------------------------------------------------

def p12_ibis_parent_typing(graph: Graph) -> list[str]:
    """P12 - IBIS parent-typing.

    Let kappa : V_IbisNode -> {issue, position, argument_pro, argument_con}
    and parent : V_IbisNode -> V_IbisNode (partial, from parent_id).

    For all n in V_IbisNode with parent(n) defined:
        kappa(n) = position     -> kappa(parent(n)) = issue
        kappa(n) = argument_pro -> kappa(parent(n)) = position
        kappa(n) = argument_con -> kappa(parent(n)) = position
        kappa(n) = issue        -> kappa(parent(n)) = issue  (sub-issues allowed)

    Root issues (parent_id null or absent) are unconditionally valid.
    Dangling parent_id references are caught independently by P1.

    Fields read: ``ibis_node["kind"]``  (enum, required),
    ``ibis_node["parent_id"]``  (nullable str ``^ibis\\.``).

    Returns a list of error strings, one per parent-typing violation.
    """
    # Valid parent kind for each child kind (§3.7 typing rules)
    VALID_PARENT_KIND: dict[str, str] = {
        "position":     "issue",
        "argument_pro": "position",
        "argument_con": "position",
        "issue":        "issue",    # sub-issues allowed
    }

    ibis_nodes: dict[str, dict] = {
        n["id"]: n for n in graph.all_of_type("ibis")
    }
    errors: list[str] = []

    for node in ibis_nodes.values():
        parent_id: str | None = node.get("parent_id")
        if not parent_id:
            continue  # Root node -- unconditionally valid

        parent = ibis_nodes.get(parent_id)
        if parent is None:
            continue  # P1 catches the dangling reference

        kind: str = node["kind"]
        parent_kind: str = parent["kind"]
        expected: str = VALID_PARENT_KIND[kind]

        if parent_kind != expected:
            errors.append(
                f"P12: ibis_node '{node['id']}' (kind='{kind}') "
                f"has parent '{parent_id}' (kind='{parent_kind}'); "
                f"expected parent kind='{expected}'"
            )

    return errors


def p13_position_pluralism(graph: Graph) -> list[str]:
    """P13 - Position pluralism  (soft WARNING only).

    For all i in V_IbisNode with kappa(i) = issue:
        |{ n in V_IbisNode : parent(n) = i and kappa(n) = position }| >= 2

    An issue with fewer than two child Position nodes is incomplete;
    single-position issues exist legitimately during drafting.

    Severity: WARNING -- never an error.  See §3.7.

    Fields read: ``ibis_node["kind"]``, ``ibis_node["parent_id"]``.

    Returns a list of warning strings, one per under-positioned issue.
    """
    ibis_nodes: dict[str, dict] = {
        n["id"]: n for n in graph.all_of_type("ibis")
    }

    # Count child Position nodes per issue
    issue_position_count: dict[str, int] = defaultdict(int)
    for node in ibis_nodes.values():
        if node["kind"] == "position":
            pid: str | None = node.get("parent_id")
            if pid and pid in ibis_nodes:
                issue_position_count[pid] += 1

    warnings: list[str] = []
    for node in ibis_nodes.values():
        if node["kind"] == "issue":
            count = issue_position_count.get(node["id"], 0)
            if count < 2:
                warnings.append(
                    f"P13: issue '{node['id']}' has {count} child Position "
                    f"node(s); >=2 expected for argumentation pluralism"
                )

    return warnings


# ---------------------------------------------------------------------------
# §3.8  Figure-narrative cross-reference
# ---------------------------------------------------------------------------

def p15_figure_in_narrative(graph: Graph) -> list[str]:
    """P15 - Figure referenced in narrative.

    For all p in V_Problem union V_Pattern, for all f in figures(p):
        exists s in narrative(p). identifier(f) is substring of body(s)

    Every figure in the figures list must be mentioned by substring (its
    id or image path) in at least one narrative section's body.  Applies
    to both Problem and Pattern nodes.

    Lifted from Auckland _check_figure_references, extended to Pattern.
    Methodology: ``figure_in_narrative_v1``.

    Fields read (Problem and Pattern):
      ``*["figures"][*]["id"]``,
      ``*["figures"][*]["image"]``  (may be absent; use id as fallback),
      ``*["narrative"][*]["body"]``.

    Returns a list of error strings, one per unreferenced figure.
    """
    errors: list[str] = []

    candidate_entities: list[dict] = (
        graph.all_of_type("problem") + graph.all_of_type("pattern")
    )

    for entity in candidate_entities:
        figures: list[dict] = entity.get("figures", [])
        if not figures:
            continue

        # Concatenate all narrative bodies for substring search
        all_bodies: str = " ".join(
            sec.get("body", "") for sec in entity.get("narrative", [])
        )

        for fig in figures:
            fig_id: str = fig.get("id", "")
            fig_image: str = fig.get("image", "")

            referenced: bool = (
                (bool(fig_id) and fig_id in all_bodies)
                or (bool(fig_image) and fig_image in all_bodies)
            )

            if not referenced:
                marker: str = fig_id or fig_image or "(unlabelled)"
                errors.append(
                    f"P15: '{entity['id']}' figure '{marker}' is not "
                    f"referenced in any narrative body"
                )

    return errors


# ---------------------------------------------------------------------------
# §3.9  Symmetric edges
# ---------------------------------------------------------------------------

def p18_camp_tensions_symmetry(graph: Graph) -> list[str]:
    """P18 - Camp-tensions symmetry.

    For all (k, k') in E_tensions_with: (k', k) in E_tensions_with

    Authors declare only one direction; this predicate enforces symmetric
    closure before the graph builder materialises the edge set.

    Dangling camp references in tensions_with are covered by P1.

    Field read: ``camp["tensions_with"]``  (list[str] ``^camp\\.``,
    uniqueItems).

    Returns a list of error strings, one per missing reverse edge.
    """
    camps: dict[str, dict] = {c["id"]: c for c in graph.all_of_type("camp")}
    errors: list[str] = []

    for camp in camps.values():
        cid: str = camp["id"]
        for other_id in camp.get("tensions_with", []):
            other = camps.get(other_id)
            if other is None:
                continue  # P1 handles the dangling reference
            if cid not in other.get("tensions_with", []):
                errors.append(
                    f"P18: camp '{cid}' tensions_with '{other_id}' but "
                    f"reverse edge missing ('{other_id}'.tensions_with "
                    f"does not include '{cid}')"
                )

    return errors


# ---------------------------------------------------------------------------
# §3.10  Iwi engagement  (soft)
# ---------------------------------------------------------------------------

def p17_iwi_engagement_note(graph: Graph) -> list[str]:
    """P17 - Iwi-scoped claim engagement note  (soft WARNING).

    For all c in V_Claim: iwi_scope(c) != {} -> c.engagement_record_id != null

    When a Claim names any iwi in iwi_scope, it must carry a non-null
    engagement_record_id referencing an entry in migration_log.yaml.

    Severity: WARNING only, pending the Mana Orite governance workflow
    becoming operational (§3.10).

    Fields read: ``claim["iwi_scope"]``  (list[str], default []),
    ``claim["engagement_record_id"]``  (nullable str).

    Returns a list of warning strings, one per violating Claim.
    """
    warnings: list[str] = []

    for claim in graph.all_of_type("claim"):
        if claim.get("iwi_scope") and not claim.get("engagement_record_id"):
            warnings.append(
                f"P17: claim '{claim['id']}' has iwi_scope="
                f"{claim['iwi_scope']} but no engagement_record_id"
            )

    return warnings


# ---------------------------------------------------------------------------
# Orchestrator
# ---------------------------------------------------------------------------

def run_all(graph: Graph) -> LintResult:
    """Run all 18 invariant predicates against *graph*.

    Routing table
    ~~~~~~~~~~~~~
    Always errors (15 fixed-severity predicates):
        p1_referential_closure, p2_claim_must_cite, p3_problem_completeness,
        p4_camp_completeness, p6_prime_national_coherence,
        p7_prime_region_mention_coherence, p8_pattern_plural_manifestation,
        p9_indicator_unit_coherence, p10_supersession_acyclicity,
        p11_supersession_freshness, p12_ibis_parent_typing,
        p14_methodology_registry_closure, p15_figure_in_narrative,
        p16_methodology_for_quantitative, p18_camp_tensions_symmetry.

    Severity-gated (P5'):
        p5_prime_comparison_consistency:
          warning when populated_region_count() <= 2,
          error   when populated_region_count() >= 3.

    Always warnings:
        p13_position_pluralism, p17_iwi_engagement_note.

    Returns a LintResult.  Callers: sys.exit(1) iff result.errors non-empty.
    """
    result = LintResult()

    # ---- Always-error predicates (15 fixed-severity) ----------------------
    for fn in (
        p1_referential_closure,
        p2_claim_must_cite,
        p3_problem_completeness,
        p4_camp_completeness,
        p6_prime_national_coherence,
        p7_prime_region_mention_coherence,
        p8_pattern_plural_manifestation,
        p9_indicator_unit_coherence,
        p10_supersession_acyclicity,
        p11_supersession_freshness,
        p12_ibis_parent_typing,
        p14_methodology_registry_closure,
        p15_figure_in_narrative,
        p16_methodology_for_quantitative,
        p18_camp_tensions_symmetry,
    ):
        result.errors.extend(fn(graph))

    # ---- P5': severity determined by region-population warmup gate --------
    # CLAUDE.md §5 row 9c: warn while <=2 regions populated, error at >=3.
    p5_messages = p5_prime_comparison_consistency(graph)
    if graph.populated_region_count() >= 3:
        result.errors.extend(p5_messages)
    else:
        result.warnings.extend(p5_messages)

    # ---- Always-warning predicates ----------------------------------------
    result.warnings.extend(p13_position_pluralism(graph))
    result.warnings.extend(p17_iwi_engagement_note(graph))

    return result
