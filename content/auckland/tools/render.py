"""Render a Problem entity to a Markdown page under content/auckland/pages/.

Usage:

    python tools/render.py problem.housing.land
    python tools/render.py --all

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

# Allow running from tools/ directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from graph import Graph, load_graph  # noqa: E402
from lint import main as lint_main  # noqa: E402


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


def _resolve_entities(graph: Graph, ids: list[str]) -> list[dict]:
    return [graph.require(entity_id) for entity_id in ids]


def render_problem(graph: Graph, problem_id: str, pages_dir: Path, env: Environment) -> Path:
    problem = graph.require(problem_id)

    camps = _sort_camps(_resolve_entities(graph, problem.get("camp_ids", [])))
    evidence = _resolve_entities(graph, problem.get("evidence_ids", []))
    sources = _resolve_entities(graph, problem.get("source_ids", []))
    sources_by_id = {s["id"]: s for s in graph.all_of_type("source")}

    template = env.get_template("subpage.md.j2")
    rendered = template.render(
        problem=problem,
        camps=camps,
        evidence=evidence,
        sources=sources,
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
    parser.add_argument("problem_id", nargs="?", help="Fully qualified Problem id (e.g. problem.housing.land)")
    parser.add_argument("--all", action="store_true", help="Render every Problem entity")
    parser.add_argument("--skip-lint", action="store_true", help="Render even if lint fails (dangerous)")
    args = parser.parse_args(argv)

    if not args.skip_lint:
        lint_status = lint_main()
        if lint_status != 0:
            print("Refusing to render — fix lint errors first. Use --skip-lint to override.")
            return lint_status

    graph = load_graph()
    root = graph.root
    pages_dir = root / "pages"
    templates_dir = root / "templates"
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
        print(f"Rendered {pid} -> {output.relative_to(root)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
