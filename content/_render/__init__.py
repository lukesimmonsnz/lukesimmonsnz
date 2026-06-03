"""Unified render dispatcher (§0 row 3 of DASHBOARD-SPEC.md).

Per the ratified spec, the dashboard depends on a single render entry point
parameterised by region. The 16 sibling ``content/<region>/tools/render.py``
modules retain authoritative logic; this package dispatches to them so the
dashboard does not need to know per-region call conventions.

A future PI pass may collapse the dispatched-to modules into one canonical
implementation; the dispatcher is the migration seam that lets that happen
without touching dashboard call sites.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path
from typing import Iterable

# Region slugs must match the directory name under content/ (with hyphens).
# Module imports use the underscore form (Python identifier rule).
REGIONS: tuple[str, ...] = (
    "auckland",
    "bay-of-plenty",
    "canterbury",
    "gisborne",
    "hawkes-bay",
    "manawatu-whanganui",
    "marlborough",
    "nelson",
    "northland",
    "otago",
    "southland",
    "taranaki",
    "tasman",
    "waikato",
    "wellington",
    "west-coast",
)


def _slug_to_module(region: str) -> str:
    return region.replace("-", "_")


def _import_render(region: str):
    """Dynamically import content.<region>.tools.render with the per-region
    tools/ directory placed first on sys.path (each region's render.py does
    ``sys.path.insert(0, _TOOLS_DIR)`` to import its own ``graph`` and
    ``lint`` modules; we replicate that contract here)."""
    if region not in REGIONS:
        raise ValueError(f"unknown region: {region!r}")
    tools_dir = (
        Path(__file__).resolve().parent.parent / region / "tools"
    )
    if not tools_dir.is_dir():
        raise FileNotFoundError(f"missing tools dir for {region}: {tools_dir}")
    tools_str = str(tools_dir)
    if tools_str not in sys.path:
        sys.path.insert(0, tools_str)
    module_name = f"content.{_slug_to_module(region)}.tools.render"
    return importlib.import_module(module_name)


def render_section(region: str, section: str) -> int:
    """Re-render the consolidated essay for one (region, section)."""
    mod = _import_render(region)
    return mod.main(["--section", section])


def render_all_sections(region: str) -> int:
    """Re-render every section's consolidated essay for a region."""
    mod = _import_render(region)
    return mod.main(["--all-sections"])


def render(region: str, entity_id: str | None = None) -> int:
    """Dashboard entry point.

    ``entity_id`` semantics:
      * ``None``           → re-render every section of the region.
      * ``"problem.<...>"`` → re-render only the problem's section
                              (consolidated essay collapses leaves).
      * any other entity   → re-render every section of the region
                              (Driver/Camp/Claim edits can affect any
                              section that links them; cheap conservative
                              default until a per-entity dependency graph
                              is implemented — left as a PI delta).
    """
    if entity_id is None:
        return render_all_sections(region)

    if entity_id.startswith("problem."):
        # graph.load_graph() owns the section lookup — call render_section
        # via the per-region module so the renderer's lint gate runs.
        mod = _import_render(region)
        # Lazy import the graph loader to read the problem's section field.
        sys.path.insert(
            0,
            str(Path(__file__).resolve().parent.parent / region / "tools"),
        )
        graph_mod = importlib.import_module(
            f"content.{_slug_to_module(region)}.tools.graph"
        )
        graph = graph_mod.load_graph()
        problem = graph.entities.get(entity_id)
        if problem is None:
            return mod.main(["--all-sections"])
        section = problem.get("section")
        if not section:
            return mod.main(["--all-sections"])
        return mod.main(["--section", section])

    # Non-problem entity: conservative full re-render.
    return render_all_sections(region)


def iter_regions() -> Iterable[str]:
    yield from REGIONS
