"""Render a Problem entity to a Markdown page under content/wellington/pages/.

Usage:

    python content/wellington/tools/render.py problem.wellington.housing.affordability
    python content/wellington/tools/render.py --all

Rendered pages are generated from the entity graph and should not be edited
by hand. Edit the entity YAML under ``data/`` and re-run.

The renderer always runs ``lint.main()`` first and refuses to render if the
graph has any errors, so generated Markdown is only ever produced from a
valid graph.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Allow running from tools/ directory or from repo root.
_TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TOOLS_DIR))

from graph import WellingtonGraph, load_graph  # noqa: E402
from lint import main as lint_main             # noqa: E402


def _build_env(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(enabled_extensions=("html",)),
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )


def _sort_camps(camps: list[dict]) -> list[dict]:
    return sorted(camps, key=lambda c: c["name"].casefold())


def _sort_drivers(drivers: list[dict]) -> list[dict]:
    return sorted(drivers, key=lambda d: d["name"].casefold())


def render_problem(
    graph: WellingtonGraph,
    problem_id: str,
    pages_dir: Path,
    env: Environment,
) -> Path:
    problem = graph.require(problem_id)

    # Drivers: lookup by problem_ids inverse link (driver.problem_ids contains problem_id).
    drivers = _sort_drivers([
        d for d in graph.all_of_type("driver")
        if problem_id in d.get("problem_ids", [])
    ])

    # Camps: lookup by addresses inverse link (camp.addresses contains problem_id).
    camps = _sort_camps([
        c for c in graph.all_of_type("camp")
        if problem_id in c.get("addresses", [])
    ])

    # Claims: resolved from problem.claim_ids.
    claim_ids = problem.get("claim_ids", [])
    claims = [graph.require(cid) for cid in claim_ids if cid in graph.entities]

    # Sources: collect all source entities for lookup by ID.
    sources_by_id = {s["id"]: s for s in graph.all_of_type("source")}

    template = env.get_template("subpage.md.j2")
    rendered = template.render(
        problem=problem,
        drivers=drivers,
        camps=camps,
        claims=claims,
        sources_by_id=sources_by_id,
        generated_at=date.today().isoformat(),
    )

    section = problem.get("section", "misc")
    subpage = problem.get("subpage", problem_id.split(".")[-1])
    output_dir = pages_dir / section
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{subpage}.md"
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "problem_id", nargs="?",
        help="Fully qualified Problem id (e.g. problem.wellington.housing.affordability)"
    )
    parser.add_argument("--all", action="store_true", help="Render every Problem entity")
    parser.add_argument(
        "--skip-lint", action="store_true",
        help="Render even if lint fails (dangerous)"
    )
    args = parser.parse_args(argv)

    if not args.skip_lint:
        lint_status = lint_main()
        if lint_status != 0:
            print("Refusing to render — fix lint errors first. Use --skip-lint to override.")
            return lint_status

    graph = load_graph()
    pages_dir = graph.root / "pages"
    templates_dir = graph.root / "templates"
    env = _build_env(templates_dir)

    if args.all:
        targets = [p["id"] for p in graph.all_of_type("problem")]
    elif args.problem_id:
        targets = [args.problem_id]
    else:
        parser.error("Must supply a problem id or --all")
        return 2

    for pid in targets:
        if pid not in graph.entities:
            print(f"Unknown problem id: {pid}")
            return 1
        output = render_problem(graph, pid, pages_dir, env)
        print(f"Rendered {pid} -> {output.relative_to(graph.root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
