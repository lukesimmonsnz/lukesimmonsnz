"""Full-text search across all region research pages and NZ patterns.

Index is built once at app startup (``build_search_index``) and stored on
``app.config['SEARCH_INDEX']``.  Each entry is a dict:

    {
        "title":   str,
        "summary": str,
        "section": str,
        "region":  str,           # e.g. "auckland"
        "url":     str,           # e.g. "/research/auckland/housing/affordable-rentals/"
        "text":    str,           # lowercased searchable blob
    }

``GET /search/?q=<query>`` filters the index and returns up to MAX_RESULTS
matches ranked by a simple hit-count heuristic.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml
from flask import Blueprint, current_app, render_template, request

search_bp = Blueprint("search", __name__)

_MAX_RESULTS = 30
_SNIPPET_WORDS = 30  # words of context around first match

# All 16 region slugs in URL form
_REGIONS = [
    "northland", "auckland", "waikato", "bay-of-plenty", "gisborne",
    "hawkes-bay", "taranaki", "manawatu-whanganui", "wellington",
    "tasman", "nelson", "marlborough", "west-coast", "canterbury",
    "otago", "southland",
]

_NZ_THEME_TITLES: dict[str, str] = {
    "housing": "Housing", "transport": "Transport",
    "infrastructure": "Infrastructure", "environment": "Environment",
    "inequality": "Inequality", "crime": "Crime & safety",
    "health": "Health", "education": "Education", "economy": "Economy",
    "governance": "Governance", "climate-adaptation": "Climate adaptation",
    "climate": "Climate adaptation",
}


def _region_label(slug: str) -> str:
    return slug.replace("-", " ").title()


def _strip_md(text: str) -> str:
    """Remove markdown markup, leaving searchable prose."""
    text = re.sub(r"^---.*?---\s*", "", text, flags=re.DOTALL)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\*{1,3}(.*?)\*{1,3}", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"`[^`]+`", "", text)
    return re.sub(r"\s+", " ", text).strip()


def _snippet(plain_text: str, query_words: list[str], n: int = _SNIPPET_WORDS) -> str:
    """Return n words of context around the first query hit, or the opening."""
    words = plain_text.split()
    lwords = [w.lower() for w in words]
    for qw in query_words:
        for i, w in enumerate(lwords):
            if qw in w:
                start = max(0, i - 4)
                end = min(len(words), i + n - 4)
                snippet = " ".join(words[start:end])
                if start > 0:
                    snippet = "..." + snippet
                if end < len(words):
                    snippet += "..."
                return snippet
    return " ".join(words[:n]) + ("..." if len(words) > n else "")


def _index_nz_patterns(content_root: Path) -> list[dict]:
    """Index NZ national patterns for search."""
    entries: list[dict] = []
    pattern_dir = content_root / "nz" / "data" / "pattern"
    if not pattern_dir.is_dir():
        return entries
    for path in sorted(pattern_dir.glob("*.yaml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if not isinstance(data, dict) or "id" not in data:
            continue
        title = data.get("title") or path.stem
        summary = str(data.get("summary") or "")
        theme = data.get("theme") or "unknown"
        theme_label = _NZ_THEME_TITLES.get(theme, theme.replace("-", " ").title())
        narrative_parts: list[str] = []
        for block in (data.get("narrative") or []):
            narrative_parts.append(block.get("heading") or "")
            narrative_parts.append(block.get("body") or "")
        plain = " ".join(narrative_parts)
        url = f"/research/nz/{theme}/"
        entries.append({
            "title": title,
            "summary": summary.strip(),
            "section": theme_label,
            "region": "Aotearoa New Zealand",
            "region_slug": "nz",
            "url": url,
            "text": (title + " " + summary + " " + plain).lower(),
            "_plain": plain,
        })
    return entries


def build_search_index(content_root: Path) -> list[dict]:
    """Scan all region pages/ directories and NZ patterns; return index entries."""
    index: list[dict] = _index_nz_patterns(content_root)

    for region in _REGIONS:
        pages_dir = content_root / region / "pages"
        if not pages_dir.is_dir():
            continue
        region_label = _region_label(region)
        for section_dir in sorted(pages_dir.iterdir()):
            if not section_dir.is_dir():
                continue
            section = section_dir.name
            section_label = section.replace("-", " ").title()
            for page_file in sorted(section_dir.glob("*.md")):
                raw = page_file.read_text(encoding="utf-8")
                fm: dict = {}
                fm_match = re.match(r"^---\s*\n(.*?)\n---", raw, re.DOTALL)
                if fm_match:
                    try:
                        fm = yaml.safe_load(fm_match.group(1)) or {}
                    except Exception:
                        pass
                title = fm.get("title") or page_file.stem.replace("-", " ").title()
                summary = fm.get("summary") or ""
                plain = _strip_md(raw)
                url = f"/research/{region}/{section}/{page_file.stem}/"
                index.append({
                    "title": title,
                    "summary": str(summary).strip(),
                    "section": section_label,
                    "region": region_label,
                    "region_slug": region,
                    "url": url,
                    "text": (title + " " + str(summary) + " " + plain).lower(),
                    "_plain": plain,
                })

    return index


def _search(index: list[dict], query: str) -> list[dict]:
    """Score and rank index entries against a query string."""
    if not query or not query.strip():
        return []
    words = [w.lower() for w in re.split(r"\s+", query.strip()) if len(w) >= 2]
    if not words:
        return []

    results = []
    for entry in index:
        text = entry["text"]
        title_lc = entry["title"].lower()
        summary_lc = entry["summary"].lower()
        hits = 0
        for w in words:
            if w in title_lc:
                hits += 4
            if w in summary_lc:
                hits += 2
            if w in text:
                hits += 1
        if hits > 0:
            results.append((hits, entry))

    results.sort(key=lambda x: x[0], reverse=True)
    out = []
    for hits, entry in results[:_MAX_RESULTS]:
        out.append({
            "title": entry["title"],
            "url": entry["url"],
            "region": entry["region"],
            "section": entry["section"],
            "snippet": _snippet(entry["_plain"], words),
        })
    return out


@search_bp.route("/search/")
def search():
    q = (request.args.get("q") or "").strip()
    results: list[dict] = []
    if q:
        index = current_app.config.get("SEARCH_INDEX", [])
        results = _search(index, q)
    return render_template("search/index.html", q=q, results=results)
