"""Render Problem entities and Section consolidations to Markdown pages.

Two modes:

    # Per-leaf (legacy; still used for diff/cite-check, no longer routed)
    python content/auckland/tools/render.py --all
    python content/auckland/tools/render.py problem.auckland.transport.accessibility

    # Per-section (new canonical output for consolidated section pages)
    python content/auckland/tools/render.py --all-sections
    python content/auckland/tools/render.py --section transport

Per-section output goes to ``pages/_sections/<section>.md``; the underscore
prefix keeps it out of the per-leaf rglob the blueprint uses for legacy
listings.

The renderer always runs ``lint.main()`` first and refuses to render if the
graph has any errors.
"""

from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

_TOOLS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_TOOLS_DIR))

from graph import WellingtonGraph, load_graph  # noqa: E402
from lint import main as lint_main             # noqa: E402

_REGION = _TOOLS_DIR.parent.name  # e.g. "auckland"

# Section display titles. Mirrors the SECTION_TITLES in blueprints/auckland.py;
# kept local so render.py is standalone.
_SECTION_TITLES: dict[str, str] = {
    "transport": "Transport",
    "housing": "Housing",
    "environment": "Environment",
    "climate": "Climate adaptation",
    "inequality": "Inequality",
    "crime": "Crime and safety",
    "health": "Health",
    "education": "Education",
    "economy": "Economy and labour",
    "governance": "Governance",
    "infrastructure": "Infrastructure",
    "framing": "Framing",
}


def _build_env(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(enabled_extensions=("html",)),
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )


# ---------------------------------------------------------------------------
# APA citation helpers (APA 7th-edition author-date style)
# ---------------------------------------------------------------------------

# Common NZ-research acronyms left uppercase when title-casing source IDs.
_ACRONYMS = frozenset({
    "NZ", "NZIER", "MBIE", "MOH", "MOE", "MSD", "MOJ", "MFE",
    "MPI", "MFAT", "DPMC", "ATAP", "OECD", "IMF", "ICNZ", "RNZ",
    "DOC", "MIT", "GP", "CRL", "LTP", "RFP", "PWC", "NZTA", "NZSL",
    "WCRC", "TLA", "RMA", "FENZ", "DIA", "GDP", "RD", "AT",
    "LSF", "WCC", "ECE", "RSE", "TPK", "RBNZ", "EPB", "TEU",
    "ACC", "TPO", "CCO", "DHB", "GIS", "SH", "SH1", "SH35",
    "MDRS", "TIF", "FAR", "PIAAC", "CGT",
})


def _author_surname(chunk: str) -> str:
    """Return the surname from a single-author chunk.

    Handles 'Surname, Initial.' (returns 'Surname') and bare names
    (returns chunk as-is).
    """
    chunk = chunk.strip().rstrip(".")
    if "," in chunk:
        head, tail = chunk.split(",", 1)
        head = head.strip()
        tail = tail.strip()
        # If the bit after the comma looks like initials ("L.", "L. and",
        # "L. M."), treat the head as the surname.
        if tail and (len(tail) <= 4 or "." in tail.split()[0]):
            return head
    return chunk


def _derive_org_from_source_id(source_id: str) -> str:
    """Best-effort organisation name from a source ID, used as last-resort
    citation key when both `author` and `publisher` are missing.

    Strips the `source.` prefix and any trailing 4-digit year, then
    title-cases each underscore-separated chunk. Known acronyms are
    upper-cased.
    """
    sid = source_id
    if sid.startswith("source."):
        sid = sid[len("source."):]
    parts = sid.rsplit("_", 1)
    if len(parts) == 2 and parts[1].isdigit() and len(parts[1]) == 4:
        sid = parts[0]
    chunks = sid.split("_")
    out: list[str] = []
    for c in chunks:
        if c.upper() in _ACRONYMS:
            out.append(c.upper())
        else:
            out.append(c.title())
    return " ".join(out) if out else "Anon"


def _split_authors(author: str) -> list[str]:
    """Split a multi-author string into surnames.

    Handles 'A and B', 'A & B', 'A; B', and 'Surname, Initial. and
    Surname, Initial.' patterns.
    """
    if not author:
        return []
    s = author.replace(" and ", "|").replace(" & ", "|").replace("; ", "|")
    chunks = [c.strip() for c in s.split("|") if c.strip()]
    return [_author_surname(c) for c in chunks]


def _resolve_author(source: dict) -> str:
    """Pick the citation author, preferring author field over publisher,
    falling back to a derived org name from the source ID."""
    author = (source.get("author") or "").strip()
    if author:
        return author
    publisher = (source.get("publisher") or "").strip()
    if publisher:
        return publisher
    return _derive_org_from_source_id(source.get("id") or "")


def _apa_short(source: dict) -> str:
    """In-text citation: '(Author, Year)' content (without parens).

    Org authors return as-is; personal authors collapse to surname(s).
    Three-or-more authors collapse to 'First et al.'.
    Year falls back to 'n.d.'.
    """
    author = _resolve_author(source)
    year = source.get("year")
    year_s = str(year) if year is not None else "n.d."
    surnames = _split_authors(author)
    if len(surnames) <= 1:
        cite_author = author if not surnames else surnames[0]
    elif len(surnames) == 2:
        cite_author = f"{surnames[0]} & {surnames[1]}"
    else:
        cite_author = f"{surnames[0]} et al."
    return f"{cite_author.rstrip('.')}, {year_s}"


def _apa_full(source: dict) -> str:
    """APA 7-style full reference for the References list.

    Format: 'Author. (Year). *Title*. Publisher. URL'
    Publisher is omitted if it equals author (org-as-author case).
    Trailing periods on author are normalised to a single period.
    """
    author = _resolve_author(source).rstrip(".")
    year = source.get("year")
    year_s = str(year) if year is not None else "n.d."
    title = (source.get("title") or "Untitled").strip().rstrip(".")
    publisher = (source.get("publisher") or "").strip().rstrip(".")
    url = (source.get("url") or "").strip()
    parts = [f"{author}. ({year_s}). <em>{title}</em>."]
    if publisher and publisher != author:
        parts.append(f"{publisher}.")
    if url:
        parts.append(f'<a href="{url}">{url}</a>')
    return " ".join(parts)


def _sort_camps(camps: list[dict]) -> list[dict]:
    return sorted(camps, key=lambda c: c["name"].casefold())


def _sort_drivers(drivers: list[dict]) -> list[dict]:
    return sorted(drivers, key=lambda d: d["name"].casefold())


def _resolve_issue(graph: WellingtonGraph, problem: dict) -> dict:
    """Resolve a problem and its dependent drivers/camps/claims."""
    pid = problem["id"]
    drivers = _sort_drivers([
        d for d in graph.all_of_type("driver")
        if pid in d.get("problem_ids", [])
    ])
    camps = _sort_camps([
        c for c in graph.all_of_type("camp")
        if pid in c.get("addresses", [])
    ])
    claim_ids = problem.get("claim_ids", [])
    claims = [graph.require(cid) for cid in claim_ids if cid in graph.entities]
    return {
        "problem": problem,
        "drivers": drivers,
        "camps": camps,
        "claims": claims,
    }


def render_problem(
    graph: WellingtonGraph,
    problem_id: str,
    pages_dir: Path,
    env: Environment,
) -> Path:
    problem = graph.require(problem_id)
    issue = _resolve_issue(graph, problem)
    sources_by_id = {s["id"]: s for s in graph.all_of_type("source")}

    template = env.get_template("subpage.md.j2")
    rendered = template.render(
        problem=problem,
        drivers=issue["drivers"],
        camps=issue["camps"],
        claims=issue["claims"],
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


def render_section(
    graph: WellingtonGraph,
    section: str,
    pages_dir: Path,
    env: Environment,
) -> Path:
    """Render one section's full consolidated essay to pages/_sections/<section>.md."""
    problems = sorted(
        [
            p for p in graph.all_of_type("problem")
            if p.get("section") == section
        ],
        key=lambda p: (p.get("order", 99), p.get("subpage", "")),
    )
    if not problems:
        raise ValueError(f"No problems found for section '{section}' in {_REGION}")

    issues = [_resolve_issue(graph, p) for p in problems]

    sources_by_id = {s["id"]: s for s in graph.all_of_type("source")}

    # Deduplicate sources across all claims, preserving first-seen order.
    seen: list[str] = []
    for issue in issues:
        for claim in issue["claims"]:
            for sid in claim.get("source_ids", []):
                if sid not in seen and sid in sources_by_id:
                    seen.append(sid)
    deduped_sources = [sources_by_id[sid] for sid in seen]

    # Build APA short forms ("Stats NZ, 2024") and full references for
    # every cited source. Per-problem in-text clusters use the short
    # form; the References section uses the full APA-formatted entry.
    source_apa_short_by_id = {sid: _apa_short(sources_by_id[sid]) for sid in seen}
    apa_full_references = [_apa_full(sources_by_id[sid]) for sid in seen]
    # Sort references alphabetically by APA short form for the References
    # list (canonical APA practice). Keep an index for href anchors.
    references_sorted = sorted(
        zip(seen, apa_full_references, strict=True),
        key=lambda pair: source_apa_short_by_id[pair[0]].casefold(),
    )
    references_for_template = [
        {"id": sid, "apa": full, "anchor": f"ref-{i + 1}"}
        for i, (sid, full) in enumerate(references_sorted)
    ]
    anchor_by_id = {sid: f"ref-{i + 1}" for i, (sid, _full) in enumerate(references_sorted)}

    # Per-problem in-text clusters: list of {short, anchor} dicts in
    # alphabetical order, one entry per distinct cited source.
    for issue in issues:
        cited_ids: list[str] = []
        for claim in issue["claims"]:
            for sid in claim.get("source_ids", []):
                if sid in source_apa_short_by_id and sid not in cited_ids:
                    cited_ids.append(sid)
        cited_ids.sort(key=lambda sid: source_apa_short_by_id[sid].casefold())
        issue["apa_citations"] = [
            {"short": source_apa_short_by_id[sid], "anchor": anchor_by_id[sid]}
            for sid in cited_ids
        ]

    # Union of horizon bands across all issues, in canonical order.
    _HORIZON_ORDER = ["decade", "generation", "century"]
    horizon_set: set[str] = set()
    for issue in issues:
        for h in (issue["problem"].get("time_horizons") or []):
            horizon_set.add(h)
    horizon_union = [h for h in _HORIZON_ORDER if h in horizon_set]

    template = env.get_template("section.md.j2")
    rendered = template.render(
        region=_REGION,
        section=section,
        section_title=_SECTION_TITLES.get(section, section.replace("_", " ").title()),
        section_lede="",  # placeholder; can be authored later
        issues=issues,
        deduped_sources=deduped_sources,
        sources_by_id=sources_by_id,
        references=references_for_template,
        horizon_union=horizon_union,
        generated_at=date.today().isoformat(),
    )

    output_dir = pages_dir / "_sections"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{section}.md"
    output_path.write_text(rendered, encoding="utf-8")
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("problem_id", nargs="?", help="Fully qualified Problem id")
    parser.add_argument("--all", action="store_true", help="Render every Problem entity (legacy per-leaf)")
    parser.add_argument("--section", help="Render one section's consolidated page")
    parser.add_argument("--all-sections", action="store_true", help="Render every section's consolidated page")
    parser.add_argument("--skip-lint", action="store_true", help="Render even if lint fails (dangerous)")
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

    if args.all_sections:
        sections = sorted({
            p["section"] for p in graph.all_of_type("problem") if p.get("section")
        })
        for sec in sections:
            output = render_section(graph, sec, pages_dir, env)
            print(f"Rendered section {sec} -> {output.relative_to(graph.root)}")
        return 0

    if args.section:
        output = render_section(graph, args.section, pages_dir, env)
        print(f"Rendered section {args.section} -> {output.relative_to(graph.root)}")
        return 0

    if args.all:
        targets = [p["id"] for p in graph.all_of_type("problem")]
    elif args.problem_id:
        targets = [args.problem_id]
    else:
        parser.error("Must supply a problem id, --all, --section, or --all-sections")
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
