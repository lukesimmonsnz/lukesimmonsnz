"""CMS source search & replace — wave 4 item 10 (η).

See docs/CMS-IMPL-WAVE-4.md §10.

Walks the editable surface per request (W4-3 ratified: in-memory rebuild;
no persistent index), returns a flat list of (page_id, line_no, line,
context) match tuples for a query.

Replace operates **only via drafts** (§10.5 invariant): find a match,
apply find→replace to the body text, ``drafts.put_draft`` with the new
content. Never writes directly to disk; PI publishes per-page through
the normal ``cms.publish`` pipeline.

Replace is supported for DIRECT_MD and HYBRID single-source pages only
(the trivial-projection set). PROJECTED corpus replace is gated on
the corpus projection (α-rest) and currently raises NotImplementedError.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from blueprints.admin.cms import drafts
from blueprints.admin.cms.resolver import (
    LockKind, PageKind, REGIONS, _CONTENT, resolve,
)


_PROJECT_ROOT = Path(__file__).resolve().parents[3]
_DOCS = _PROJECT_ROOT / "docs"


@dataclass(frozen=True)
class Match:
    page_id: str            # canonical URL — keys cms.db.drafts
    path:    Path           # source file
    line_no: int            # 1-indexed
    line:    str            # the matching line (rstripped)
    before:  str            # ≤2 lines of preceding context
    after:   str            # ≤2 lines of following context

    def to_dict(self) -> dict:
        return {
            "page_id": self.page_id,
            "path":    str(self.path),
            "line_no": self.line_no,
            "line":    self.line,
            "before":  self.before,
            "after":   self.after,
        }


# ---------------- file enumeration --------------------------------------


def _enumerate_searchable() -> list[tuple[str, Path]]:
    """Return (page_id, source_path) tuples for every editable surface.

    Coverage:
      - DIRECT_MD: content/blog/*.md (skip _index/_drafts), docs/METHODOLOGY.md
      - HYBRID:    content/davidsimmons/*.md (slot files)
      - PROJECTED: content/<region>/data/problem/*.yaml across all 16 regions,
                   content/nz/data/pattern/*.yaml

    SETTINGS pages are skipped — they are JSON blobs in cms.db, not files.
    """
    out: list[tuple[str, Path]] = []

    blog = _CONTENT / "blog"
    if blog.is_dir():
        for p in sorted(blog.glob("*.md")):
            if p.stem.startswith("_"):
                continue
            out.append((f"/blog/{p.stem}/", p))

    methodology = _DOCS / "METHODOLOGY.md"
    if methodology.is_file():
        out.append(("/research/methodology/", methodology))

    davidsimmons = _CONTENT / "davidsimmons"
    if davidsimmons.is_dir():
        for p in sorted(davidsimmons.glob("*.md")):
            out.append((f"/davidsimmons/{p.stem}/", p))

    for region in sorted(REGIONS):
        problems = _CONTENT / region / "data" / "problem"
        if not problems.is_dir():
            continue
        for p in sorted(problems.glob("*.yaml")):
            stem = p.stem      # e.g. "transport.congestion"
            if "." not in stem:
                continue
            theme, _, slug = stem.partition(".")
            out.append((f"/research/{region}/{theme}/{slug}/", p))

    nz_pattern = _CONTENT / "nz" / "data" / "pattern"
    if nz_pattern.is_dir():
        for p in sorted(nz_pattern.glob("*.yaml")):
            # NZ patterns share /research/nz/<theme>/ — multiple files per
            # page. Use the file path as the page_id approximation; replace
            # operations on these are gated until pattern_form_A ships.
            stem = p.stem
            theme = stem.partition(".")[0] if "." in stem else stem
            out.append((f"/research/nz/{theme}/", p))

    return out


# ---------------- find --------------------------------------------------


def _build_pattern(query: str, whole_word: bool) -> re.Pattern[str]:
    """Compile a case-insensitive regex from the query string.

    ``whole_word`` wraps the escaped query in ``\\b`` boundaries to
    avoid matching inside larger words (W4-4 ratified default).
    """
    body = re.escape(query)
    if whole_word:
        body = r"\b" + body + r"\b"
    return re.compile(body, re.IGNORECASE)


def find_matches(query: str, whole_word: bool = True,
                 limit: int = 500) -> list[Match]:
    """Scan editable sources; return matches up to ``limit`` total.

    Each match yields one entry per matching line. Multiple matches in
    a single line collapse to one entry (the line is the unit of UI
    presentation).
    """
    if not query.strip():
        return []
    pat = _build_pattern(query, whole_word)
    out: list[Match] = []
    for page_id, path in _enumerate_searchable():
        try:
            with open(path, "r", encoding="utf-8", newline="") as f:
                lines = f.read().splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines):
            if pat.search(line) is None:
                continue
            before = "\n".join(lines[max(0, i - 2):i])
            after  = "\n".join(lines[i + 1:i + 3])
            out.append(Match(
                page_id=page_id,
                path=path,
                line_no=i + 1,
                line=line.rstrip(),
                before=before,
                after=after,
            ))
            if len(out) >= limit:
                return out
    return out


# ---------------- replace (via drafts only) -----------------------------


class ReplaceError(ValueError):
    """Raised when a replace operation cannot be fulfilled."""


def apply_replaces(
    find: str,
    replace: str,
    page_ids: list[str],
    whole_word: bool = True,
) -> dict[str, int]:
    """Apply find→replace to selected pages, persisting as drafts.

    Returns ``{page_id: substitution_count}`` for pages where a draft
    was created. Pages with zero substitutions are omitted from the
    return.

    Replace via drafts only (§10.5 invariant). Direct file writes are
    intentionally not supported.

    PROJECTED pages with stubbed projections raise NotImplementedError
    inside ``ref.projection.load`` and are skipped (entry omitted from
    the return dict; PI sees this as "0 pages updated" if every selected
    page is PROJECTED).
    """
    if not find:
        raise ReplaceError("find string must be non-empty")
    pat = _build_pattern(find, whole_word)
    out: dict[str, int] = {}

    for page_id in page_ids:
        ref = resolve(page_id)
        if ref is None or ref.lock != LockKind.EDITABLE:
            continue

        # Replace is supported for kinds whose projection round-trips
        # cleanly: DIRECT_MD and single-source HYBRID (slot_md/section_md).
        # PROJECTED is gated on the corpus/pattern projections (α-rest);
        # for now we attempt projection.load and skip on NotImplementedError.
        try:
            state = ref.projection.load(ref.source_paths)
        except NotImplementedError:
            continue
        except Exception:
            continue

        new_body, body_n = pat.subn(replace, state.body)
        new_fm = state.frontmatter
        fm_n = 0
        if new_fm is not None:
            new_fm, fm_n = pat.subn(replace, new_fm)
        total = body_n + fm_n
        if total == 0:
            continue

        base_sha = drafts.hash_concat(ref.source_paths)
        drafts.put_draft(
            page_id=page_id,
            body=new_body,
            frontmatter=new_fm,
            base_sha=base_sha,
            by_user=None,
        )
        out[page_id] = total

    return out
