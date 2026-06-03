"""Lint the Wellington knowledge base.

Runs JSON Schema validation (via graph.load_graph) and all cross-entity
invariants from content/_schema/invariants.py (P1–P18).

Exit 0 if the graph is clean, 1 otherwise.

Usage::

    # from repo root
    python content/canterbury/tools/lint.py

    # from the tools/ directory
    python lint.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Allow direct script execution from tools/ or repo root.
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))                        # tools/ for graph.py
sys.path.insert(0, str(_HERE.parent.parent.parent))   # repo root for content._schema

from graph import load_graph  # noqa: E402

# Import invariants from the shared schema package.
try:
    from content._schema.invariants import run_all  # noqa: E402
except ImportError:
    # Fallback: insert content/_schema parent explicitly.
    _SCHEMA_PARENT = _HERE.parent.parent.parent
    sys.path.insert(0, str(_SCHEMA_PARENT))
    from content._schema.invariants import run_all  # noqa: E402


def main() -> int:
    graph = load_graph()

    # ── Phase 1: JSON Schema validation ──────────────────────────────────────
    schema_errors = list(graph.validation_errors)

    # ── Phase 2: Cross-entity invariants (P1–P18) ────────────────────────────
    result = run_all(graph)

    # ── Report ────────────────────────────────────────────────────────────────
    total_errors = schema_errors + result.errors
    total_warnings = result.warnings

    if total_warnings:
        print(f"Warnings ({len(total_warnings)}):")
        for w in total_warnings:
            print(f"  W  {w}")

    if not total_errors and not total_warnings:
        print(
            f"OK — {len(graph.entities)} entities; "
            f"0 schema errors; 0 invariant errors; 0 warnings."
        )
        return 0

    if not total_errors:
        print(
            f"OK (with warnings) — {len(graph.entities)} entities; "
            f"0 errors; {len(total_warnings)} warning(s)."
        )
        return 0

    print(f"\nFAIL — {len(total_errors)} error(s) across {len(graph.entities)} entities:")
    if schema_errors:
        print(f"\n  Schema validation ({len(schema_errors)}):")
        for msg in schema_errors:
            print(f"    E  {msg}")
    if result.errors:
        print(f"\n  Invariant violations ({len(result.errors)}):")
        for msg in result.errors:
            print(f"    E  {msg}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
