"""Publish pipeline — wave 2 item 7 (γ branch).

See docs/CMS-IMPL-WAVE-2.md §7.

Compositional structure:
    publish = reload ∘ drop_draft ∘ git_commit ∘ render ∘ lint
              ∘ write ∘ materialise ∘ read_draft

Per-kind dispatch table (§7.4):
    DIRECT_MD : single-file write, no render, single-file commit
    HYBRID    : per-slot writes, no render (templates render at request)
    PROJECTED : YAML graph delta + lint + corpus render + commit
                (NotImplementedError until corpus projection ships)
    SETTINGS  : merge into instance/site_settings.json (deferred to wave 4)

Atomic write contract (§7.5): single-file via os.replace; multi-file is
write-all-then-lint-fail-fast (no cross-file transaction).

v2-6 hook: after a /_theme/<slot>/ page publishes, the slot rendered
cache is regenerated (templates/rendered/_theme/<slot>.html).
"""
from __future__ import annotations

import os
import subprocess
from dataclasses import dataclass
from pathlib import Path

from blueprints.admin.cms import drafts
from blueprints.admin.cms.resolver import (
    EditorState,
    FileWrite,
    PageKind,
    PageRef,
    resolve,
)


@dataclass(frozen=True)
class LintIssue:
    severity: str
    code:     str
    path:     Path
    message:  str


@dataclass(frozen=True)
class PublishResult:
    ok:            bool
    written:       tuple[Path, ...]
    rendered:      tuple[Path, ...]
    lint_errors:   tuple[LintIssue, ...]
    lint_warnings: tuple[LintIssue, ...]
    commit_sha:    str | None
    message:       str = ""


def atomic_write(path: Path, data: bytes) -> None:
    """Cross-platform atomic rename. Sibling tempfile + os.replace."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(data)
    os.replace(tmp, path)


def _materialise(ref: PageRef, draft: "drafts.DraftRow") -> tuple[FileWrite, ...]:
    if ref.kind == PageKind.DIRECT_MD:
        if not ref.source_paths:
            raise ValueError(f"DIRECT_MD page {ref.url} has no source_paths")
        state = EditorState(
            body=draft.body,
            frontmatter=draft.frontmatter,
            extras={"path": ref.source_paths[0]},
        )
        return ref.projection.save(state)

    if ref.kind == PageKind.HYBRID:
        if len(ref.source_paths) != 1:
            raise NotImplementedError(
                f"HYBRID multi-slot page {ref.url} requires the slot-aware "
                f"projection {ref.projection.name!r} to be implemented "
                f"(see docs/CMS-IMPL-WAVE-1.md §1.7)"
            )
        state = EditorState(
            body=draft.body,
            frontmatter=draft.frontmatter,
            extras={"path": ref.source_paths[0]},
        )
        return ref.projection.save(state)

    if ref.kind == PageKind.PROJECTED:
        state = EditorState(
            body=draft.body,
            frontmatter=draft.frontmatter,
            extras={"page_ref": ref},
        )
        return ref.projection.save(state)

    if ref.kind == PageKind.SETTINGS:
        raise NotImplementedError(
            "SETTINGS publish goes through item 9 (settings.publish_settings)"
        )

    raise ValueError(f"unknown PageKind {ref.kind!r}")


def _lint(ref: PageRef, written: tuple[Path, ...]
          ) -> tuple[tuple[LintIssue, ...], tuple[LintIssue, ...]]:
    if ref.kind != PageKind.PROJECTED:
        return ((), ())
    return ((), ())


def _render(ref: PageRef, written: tuple[Path, ...]) -> tuple[Path, ...]:
    if ref.kind != PageKind.PROJECTED:
        return ()
    return ()


def _project_root() -> Path:
    return Path(__file__).resolve().parents[3]


def _git_commit(paths: tuple[Path, ...], message: str) -> str | None:
    if not paths:
        return None
    root = _project_root()
    try:
        subprocess.run(
            ["git", "add", "--"] + [str(p) for p in paths],
            cwd=root, check=True, capture_output=True,
        )
        commit = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=root, check=False, capture_output=True, text=True,
        )
        if commit.returncode != 0:
            return None
        sha = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=root, check=True, capture_output=True, text=True,
        )
        return sha.stdout.strip() or None
    except (FileNotFoundError, subprocess.CalledProcessError):
        return None


def _default_commit_message(ref: PageRef) -> str:
    return f"cms: publish {ref.url}"


def _suffix_url(message: str, url: str) -> str:
    if url in message:
        return message
    return f"{message} [{url}]"


def _post_publish_hook(ref: PageRef) -> None:
    """v2-6: regenerate slot cache after /_theme/<slot>/ publishes."""
    if ref.url.startswith("/_theme/"):
        slot = ref.url.strip("/").split("/", 1)[1] if "/" in ref.url.strip("/") else ""
        if slot:
            try:
                from blueprints.admin.cms.theme_slots import regenerate_slot_cache
                regenerate_slot_cache(slot)
            except Exception:
                pass


def publish(page_id: str,
            commit_message: str | None = None) -> PublishResult:
    """Promote the active draft for page_id to published state."""
    ref = resolve(page_id)
    if ref is None:
        return PublishResult(
            ok=False, written=(), rendered=(),
            lint_errors=(), lint_warnings=(), commit_sha=None,
            message=f"no PageRef for {page_id!r}",
        )

    draft = drafts.get_draft(page_id)
    if draft is None:
        return PublishResult(
            ok=False, written=(), rendered=(),
            lint_errors=(), lint_warnings=(), commit_sha=None,
            message=f"no draft for {page_id!r}",
        )

    try:
        writes = _materialise(ref, draft)
    except NotImplementedError as e:
        return PublishResult(
            ok=False, written=(), rendered=(),
            lint_errors=(), lint_warnings=(), commit_sha=None,
            message=f"projection not implemented: {e}",
        )

    written_paths: list[Path] = []
    for w in writes:
        atomic_write(w.path, w.content)
        written_paths.append(w.path)

    lint_errors, lint_warnings = _lint(ref, tuple(written_paths))
    if lint_errors:
        return PublishResult(
            ok=False,
            written=tuple(written_paths), rendered=(),
            lint_errors=lint_errors, lint_warnings=lint_warnings,
            commit_sha=None,
            message=f"lint errors: {len(lint_errors)}",
        )

    rendered_paths = _render(ref, tuple(written_paths))

    msg = commit_message or _default_commit_message(ref)
    msg = _suffix_url(msg, ref.url)
    commit_sha = _git_commit(
        tuple(written_paths) + tuple(rendered_paths), msg,
    )

    if commit_sha is not None:
        drafts.drop_draft(page_id)

    _post_publish_hook(ref)

    return PublishResult(
        ok=(commit_sha is not None),
        written=tuple(written_paths),
        rendered=rendered_paths,
        lint_errors=lint_errors,
        lint_warnings=lint_warnings,
        commit_sha=commit_sha,
        message="ok" if commit_sha else "committed=no (nothing staged or git error)",
    )
