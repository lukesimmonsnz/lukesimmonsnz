"""Lint the Auckland knowledge base.

Runs schema validation (via graph.load_graph) and additional graph invariants
that JSON Schema cannot express — e.g. referenced entity IDs must exist.

Exit code is 0 if the graph is clean, 1 otherwise. Use in pre-commit hooks
or CI.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow running the script directly from the tools/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import Graph, load_graph  # noqa: E402


def _check_referenced_ids_exist(graph: Graph) -> list[str]:
    errors: list[str] = []
    for entity_id, entity in graph.entities.items():
        for ref_id in graph.referenced_ids(entity):
            if ref_id not in graph.entities:
                errors.append(
                    f"{entity_id}: references missing entity '{ref_id}'"
                )
    return errors


def _check_problem_minimums(graph: Graph) -> list[str]:
    errors: list[str] = []
    for problem in graph.all_of_type("problem"):
        required = ("driver_ids", "camp_ids", "evidence_ids", "source_ids")
        for field_name in required:
            if not problem.get(field_name):
                errors.append(
                    f"{problem['id']}: must have at least one {field_name}"
                )
    return errors


def _check_evidence_has_source(graph: Graph) -> list[str]:
    errors: list[str] = []
    for evidence in graph.all_of_type("evidence"):
        if not evidence.get("source_ids"):
            errors.append(f"{evidence['id']}: evidence must cite at least one source")
    return errors


def _check_camp_completeness(graph: Graph) -> list[str]:
    errors: list[str] = []
    for camp in graph.all_of_type("camp"):
        if not camp.get("flagship_moves"):
            errors.append(f"{camp['id']}: camp must list at least one flagship move")
        if not camp.get("tensions"):
            errors.append(f"{camp['id']}: camp must list at least one tension")
        if not camp.get("interventions"):
            errors.append(f"{camp['id']}: camp must list at least one intervention")
        if not camp.get("addresses"):
            errors.append(f"{camp['id']}: camp must address at least one problem")
    return errors


def _check_figure_references(graph: Graph) -> list[str]:
    """For each Problem, figures listed in the figures block should
    each be referenced somewhere in the narrative body (by image path or id)."""
    errors: list[str] = []
    for problem in graph.all_of_type("problem"):
        figures = problem.get("figures") or []
        narrative = problem.get("narrative") or []
        narrative_text = "\n".join(section.get("body", "") for section in narrative)
        for figure in figures:
            identifier = figure.get("image") or figure.get("id")
            if identifier and identifier not in narrative_text:
                errors.append(
                    f"{problem['id']}: figure '{figure.get('id')}' is defined but not referenced in narrative"
                )
    return errors


def main() -> int:
    graph = load_graph()
    errors: list[str] = list(graph.validation_errors)
    errors.extend(_check_referenced_ids_exist(graph))
    errors.extend(_check_problem_minimums(graph))
    errors.extend(_check_evidence_has_source(graph))
    errors.extend(_check_camp_completeness(graph))
    errors.extend(_check_figure_references(graph))

    if not errors:
        print(f"OK — {len(graph.entities)} entities clean.")
        return 0

    print(f"FAIL — {len(errors)} issue(s) in {len(graph.entities)} entities:")
    for msg in errors:
        print(f"  - {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
