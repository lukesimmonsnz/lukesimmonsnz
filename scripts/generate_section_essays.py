"""
Generate consolidated section essays for all non-Auckland regions using
Auckland's section.md.j2 template.

For each of the 15 regions: load the typed entity graph, resolve every
Problem → its Drivers / Camps / Claims, render Auckland's section.md.j2
with that data, write the result to
``content/<region>/pages/_sections/<theme>.md``.

This produces the same essay-style consolidated pages Auckland already has
(one h2 per problem, drivers / camps grouped within, dedup'd References
and a Technical details block once at the bottom).
"""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent

REGIONS = [
    "wellington", "northland", "waikato", "bay-of-plenty", "gisborne",
    "hawkes-bay", "taranaki", "manawatu-whanganui", "nelson", "tasman",
    "marlborough", "west-coast", "canterbury", "otago", "southland",
]

SECTION_TITLES: dict[str, str] = {
    "transport": "Transport",
    "housing": "Housing",
    "environment": "Environment",
    "climate": "Climate adaptation",
    "inequality": "Inequality",
    "crime": "Crime and safety",
    "health": "Health",
    "education": "Education",
    "economy": "Economy",
    "governance": "Governance",
    "infrastructure": "Infrastructure",
}

# Auckland's render template — re-used verbatim. Keeping it as the single
# source of truth means a fix to the essay structure only touches one file.
AUCKLAND_TEMPLATES_DIR = ROOT / "content" / "auckland" / "templates"


def _build_env() -> Environment:
    return Environment(
        loader=FileSystemLoader(str(AUCKLAND_TEMPLATES_DIR)),
        autoescape=select_autoescape(enabled_extensions=("html",)),
        trim_blocks=False,
        lstrip_blocks=False,
        keep_trailing_newline=True,
    )


# ---------------------------------------------------------------------------
# APA citation helpers (mirrors content/auckland/tools/render.py — kept in
# sync by hand since render.py and generate_section_essays.py are separate
# entry points).
# ---------------------------------------------------------------------------

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
    chunk = chunk.strip().rstrip(".")
    if "," in chunk:
        head, tail = chunk.split(",", 1)
        head = head.strip()
        tail = tail.strip()
        if tail and (len(tail) <= 4 or "." in tail.split()[0]):
            return head
    return chunk


def _split_authors(author: str) -> list[str]:
    if not author:
        return []
    s = author.replace(" and ", "|").replace(" & ", "|").replace("; ", "|")
    chunks = [c.strip() for c in s.split("|") if c.strip()]
    return [_author_surname(c) for c in chunks]


def _derive_org_from_source_id(source_id: str) -> str:
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


def _resolve_author(source: dict) -> str:
    author = (source.get("author") or "").strip()
    if author:
        return author
    publisher = (source.get("publisher") or "").strip()
    if publisher:
        return publisher
    return _derive_org_from_source_id(source.get("id") or "")


def _apa_short(source: dict) -> str:
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


def _resolve_issue(graph, problem: dict) -> dict:
    pid = problem["id"]
    drivers = sorted(
        [d for d in graph.all_of_type("driver") if pid in d.get("problem_ids", [])],
        key=lambda d: d["name"].casefold(),
    )
    camps = sorted(
        [c for c in graph.all_of_type("camp") if pid in c.get("addresses", [])],
        key=lambda c: c["name"].casefold(),
    )
    claim_ids = problem.get("claim_ids", [])
    claims = [graph.require(cid) for cid in claim_ids if cid in graph.entities]
    return {"problem": problem, "drivers": drivers, "camps": camps, "claims": claims}


def render_section(graph, region: str, section: str, env: Environment, pages_dir: Path) -> Path | None:
    problems = sorted(
        [p for p in graph.all_of_type("problem") if p.get("section") == section],
        key=lambda p: (p.get("order", 99), p.get("subpage", "")),
    )
    if not problems:
        return None

    issues = [_resolve_issue(graph, p) for p in problems]
    sources_by_id = {s["id"]: s for s in graph.all_of_type("source")}

    # Dedup sources, preserve first-seen order
    seen: list[str] = []
    for issue in issues:
        for claim in issue["claims"]:
            for sid in claim.get("source_ids", []):
                if sid not in seen and sid in sources_by_id:
                    seen.append(sid)
    deduped_sources = [sources_by_id[sid] for sid in seen]

    # APA short form per cited source ('Stats NZ, 2024'); full APA-formatted
    # references ordered alphabetically for the References list.
    source_apa_short_by_id = {sid: _apa_short(sources_by_id[sid]) for sid in seen}
    references_sorted = sorted(
        [(sid, _apa_full(sources_by_id[sid])) for sid in seen],
        key=lambda pair: source_apa_short_by_id[pair[0]].casefold(),
    )
    references_for_template = [
        {"id": sid, "apa": full, "anchor": f"ref-{i + 1}"}
        for i, (sid, full) in enumerate(references_sorted)
    ]
    anchor_by_id = {sid: f"ref-{i + 1}" for i, (sid, _full) in enumerate(references_sorted)}

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

    horizons_order = ["decade", "generation", "century"]
    horizon_set: set[str] = set()
    for issue in issues:
        for h in (issue["problem"].get("time_horizons") or []):
            horizon_set.add(h)
    horizon_union = [h for h in horizons_order if h in horizon_set]

    template = env.get_template("section.md.j2")
    rendered = template.render(
        region=region,
        section=section,
        section_title=SECTION_TITLES.get(section, section.replace("_", " ").title()),
        section_lede="",
        issues=issues,
        deduped_sources=deduped_sources,
        sources_by_id=sources_by_id,
        references=references_for_template,
        horizon_union=horizon_union,
        generated_at=date.today().isoformat(),
    )

    out_dir = pages_dir / "_sections"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{section}.md"
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def main():
    env = _build_env()

    for region in REGIONS:
        # Each region carries its own copy of graph.py — they share an
        # implementation but live in per-region tools/. Import dynamically.
        tools_dir = ROOT / "content" / region / "tools"
        if not tools_dir.is_dir():
            print(f"[skip] {region}: no tools/ directory")
            continue

        # Clean module state between regions to avoid the load_graph cache
        # picking up the previous region's data.
        for mod in ("graph", "lint"):
            sys.modules.pop(mod, None)
        sys.path.insert(0, str(tools_dir))
        try:
            from graph import load_graph  # type: ignore
            graph = load_graph()
        finally:
            sys.path.remove(str(tools_dir))

        pages_dir = ROOT / "content" / region / "pages"

        rendered_count = 0
        skipped_count = 0
        for section in SECTION_TITLES:
            try:
                out = render_section(graph, region, section, env, pages_dir)
                if out:
                    rendered_count += 1
                else:
                    skipped_count += 1
            except Exception as exc:
                print(f"  [err] {region}/{section}: {exc}")
                skipped_count += 1
        print(f"{region}: {rendered_count} rendered, {skipped_count} skipped")


if __name__ == "__main__":
    main()
