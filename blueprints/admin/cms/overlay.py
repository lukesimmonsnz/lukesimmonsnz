"""Preview overlay — wave 3 item 4 (δ).

See docs/CMS-IMPL-WAVE-3.md §4.

A request-scoped intercept of ``Path.read_text`` / ``Path.read_bytes``
via ``contextvars.ContextVar``. When a preview render is in flight,
reads of the page's source paths return the **draft** bytes instead of
the on-disk bytes — without modifying the working tree.

Contract (precise):
    F_p^Ω(q) =
      M(p, D(p))_q   if q ∈ S(p) ∧ D(p) ≠ ⊥
      F(q)            otherwise

Implementation: candidate B from W3-1 ratified, in narrowly-scoped form.
The monkey-patch on ``Path.read_text`` / ``Path.read_bytes`` is the
universal intercept; only paths in the active overlay's ``intercepts``
dict are diverted, so the patch is a no-op for unrelated reads.

Currently in scope:
  - DIRECT_MD pages (blog, methodology, blog index)
  - HYBRID single-source slot pages (davidsimmons/<slot>, region sections)

NOT in scope (preview falls back to published version):
  - PROJECTED corpus / pattern pages — preview requires the corpus
    render pipeline to be re-runnable against in-memory YAML, which
    is a deeper refactor of content/<region>/tools/render.py.
"""
from __future__ import annotations

from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterator


# ---------------- overlay state ----------------------------------------


@dataclass(frozen=True)
class Overlay:
    """A request-scoped mapping from canonical paths to draft bytes.

    Paths are stored as **resolved absolute** Paths so equality checks
    inside the read-text intercept are robust against relative-path
    callers and symlinks.
    """
    intercepts: dict[Path, bytes] = field(default_factory=dict)

    def get(self, path: Path) -> bytes | None:
        try:
            resolved = path.resolve()
        except OSError:
            return None
        return self.intercepts.get(resolved)


_active: ContextVar[Overlay | None] = ContextVar(
    "cms_preview_overlay", default=None,
)


@contextmanager
def overlay_active(overlay: Overlay) -> Iterator[None]:
    """Activate ``overlay`` for the duration of the with-block.

    Uses ContextVar.set/reset so the overlay correctly tears down on
    both success and exception paths. Nesting is not supported in v1
    (an inner ``overlay_active`` overrides the outer for its scope and
    restores on exit).
    """
    token = _active.set(overlay)
    try:
        yield
    finally:
        _active.reset(token)


# ---------------- monkey-patch -----------------------------------------


_real_read_text = Path.read_text
_real_read_bytes = Path.read_bytes
_installed = False


def _intercepted_read_text(self: Path, *args, **kwargs) -> str:
    overlay = _active.get()
    if overlay is not None:
        data = overlay.get(self)
        if data is not None:
            # Decode according to caller's encoding= kwarg (default utf-8).
            encoding = kwargs.get("encoding") or (args[0] if args else "utf-8")
            errors = kwargs.get("errors") or (args[1] if len(args) > 1 else "strict")
            return data.decode(encoding, errors=errors)
    return _real_read_text(self, *args, **kwargs)


def _intercepted_read_bytes(self: Path) -> bytes:
    overlay = _active.get()
    if overlay is not None:
        data = overlay.get(self)
        if data is not None:
            return data
    return _real_read_bytes(self)


def install() -> None:
    """Install the read-intercept monkey-patches. Idempotent.

    Called once from ``app.py`` after the app factory completes. Safe
    to call multiple times — subsequent invocations are no-ops.
    """
    global _installed
    if _installed:
        return
    Path.read_text = _intercepted_read_text   # type: ignore[method-assign]
    Path.read_bytes = _intercepted_read_bytes  # type: ignore[method-assign]
    _installed = True


def uninstall() -> None:
    """Restore the original Path methods. Test-only."""
    global _installed
    if not _installed:
        return
    Path.read_text = _real_read_text          # type: ignore[method-assign]
    Path.read_bytes = _real_read_bytes        # type: ignore[method-assign]
    _installed = False
