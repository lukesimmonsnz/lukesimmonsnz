"""Per-page git history + diff + restore — wave 4 closure (θ).

See docs/CMS-IMPL-WAVE-4.md §11.

Read-only over git (§11.5): no checkout, reset, revert.
"""
from __future__ import annotations

import subprocess
from dataclasses import dataclass
from pathlib import Path

from blueprints.admin.cms import drafts
from blueprints.admin.cms.resolver import LockKind, PageKind, resolve


_PROJECT_ROOT = Path(__file__).resolve().parents[3]


@dataclass(frozen=True)
class Commit:
    sha:        str
    short_sha:  str
    author:     str
    date:       str
    subject:    str

    def to_dict(self) -> dict:
        return {
            "sha": self.sha, "short_sha": self.short_sha,
            "author": self.author, "date": self.date,
            "subject": self.subject,
        }


def _git(args: list[str], check: bool = False) -> subprocess.CompletedProcess:
    return subprocess.run(
        ["git"] + args,
        cwd=_PROJECT_ROOT,
        check=check,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _rel(path: Path) -> str:
    try:
        return path.resolve().relative_to(_PROJECT_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


_LOG_FORMAT = "%H%x09%h%x09%an <%ae>%x09%aI%x09%s"


def commits_for_page(page_id: str, limit: int = 50) -> list[Commit]:
    ref = resolve(page_id)
    if ref is None or not ref.source_paths:
        return []
    rels = [_rel(p) for p in ref.source_paths]
    cp = _git([
        "log",
        f"--max-count={int(limit)}",
        f"--pretty=format:{_LOG_FORMAT}",
        "--",
    ] + rels)
    if cp.returncode != 0 or not cp.stdout.strip():
        return []
    out: list[Commit] = []
    for line in cp.stdout.splitlines():
        parts = line.split("\t", 4)
        if len(parts) != 5:
            continue
        out.append(Commit(
            sha=parts[0], short_sha=parts[1],
            author=parts[2], date=parts[3], subject=parts[4],
        ))
    return out


def diff(page_id: str, from_sha: str, to_sha: str | None = None) -> str:
    ref = resolve(page_id)
    if ref is None or not ref.source_paths:
        return ""
    if not _is_safe_sha(from_sha):
        raise ValueError(f"invalid sha: {from_sha!r}")
    if to_sha is not None and not _is_safe_sha(to_sha):
        raise ValueError(f"invalid sha: {to_sha!r}")

    rels = [_rel(p) for p in ref.source_paths]

    if to_sha is None:
        parent_check = _git(["rev-parse", "--verify", f"{from_sha}~"])
        if parent_check.returncode == 0:
            rev_args = [f"{from_sha}~..{from_sha}"]
        else:
            rev_args = ["4b825dc642cb6eb9a060e54bf8d69288fbee4904", from_sha]
    else:
        rev_args = [f"{from_sha}..{to_sha}"]

    cp = _git(["diff"] + rev_args + ["--"] + rels)
    if cp.returncode != 0:
        return cp.stderr or ""
    return cp.stdout


class RestoreError(ValueError):
    """Raised when a restore operation cannot be fulfilled."""


def restore_to_draft(page_id: str, sha: str) -> bool:
    if not _is_safe_sha(sha):
        raise RestoreError(f"invalid sha: {sha!r}")
    ref = resolve(page_id)
    if ref is None:
        raise RestoreError(f"unresolvable page: {page_id!r}")
    if ref.lock != LockKind.EDITABLE:
        raise RestoreError(f"page is {ref.lock.value}, not editable")

    if ref.kind not in (PageKind.DIRECT_MD, PageKind.HYBRID):
        raise RestoreError(
            f"restore not yet supported for {ref.kind.value} "
            f"(gated on α-rest projection bodies)"
        )
    if len(ref.source_paths) != 1:
        raise RestoreError(
            f"multi-source page {page_id} requires the slot-aware "
            f"projection {ref.projection.name!r} to be implemented"
        )

    rel = _rel(ref.source_paths[0])
    cp = _git(["show", f"{sha}:{rel}"])
    if cp.returncode != 0:
        raise RestoreError(
            f"git show failed: {cp.stderr.strip() or 'unknown error'}"
        )
    historical_text = cp.stdout

    from blueprints.admin.cms.resolver import _split_frontmatter  # type: ignore[attr-defined]
    fm, body = _split_frontmatter(historical_text)

    base_sha = drafts.hash_concat(ref.source_paths)
    drafts.put_draft(
        page_id=page_id,
        body=body,
        frontmatter=fm,
        base_sha=base_sha,
        by_user=None,
    )
    return True


def _is_safe_sha(sha: str) -> bool:
    if not sha or not (4 <= len(sha) <= 40):
        return False
    return all(c in "0123456789abcdefABCDEF" for c in sha)
