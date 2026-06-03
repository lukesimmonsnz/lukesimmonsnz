"""Block registry loader — mechanical (no PI mastery surface).

Spec: docs/CMS-SPEC-v2.md §3.4
Wave: docs/CMS-IMPL-WAVE-v2-1.md §6

Reads `content/_blocks/registry.yaml` into a kind → BlockSpec dict.
The parser uses `container` to decide whether a block's body is
recursive (BlockTree) or a verbatim string (leaf body). The renderer
(wave v2-3) uses `template` to dispatch to the right Jinja partial.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import yaml


REGISTRY_PATH = Path("content/_blocks/registry.yaml")


@dataclass(frozen=True)
class BlockSpec:
    kind:      str
    container: bool                 # True ⇒ body is BlockTree, False ⇒ str
    attrs:     tuple[str, ...]      # declared attr names (informational)
    required:  tuple[str, ...]      # subset of attrs (informational)
    template:  str                  # Jinja partial path under templates/


def load_registry(path: Path | None = None) -> dict[str, BlockSpec]:
    """Read the block registry YAML into a kind → BlockSpec dict.

    Args:
        path: Optional override path (for testing). Defaults to
              content/_blocks/registry.yaml.

    Returns:
        A dict keyed by `kind` (e.g. "callout", "columns") containing
        BlockSpec entries.

    Raises:
        FileNotFoundError: if the registry file is missing.
        ValueError:       if a block entry is malformed (missing 'kind'
                          or 'template').
    """
    target = path or REGISTRY_PATH
    raw = yaml.safe_load(target.read_text(encoding="utf-8"))
    if not raw or "blocks" not in raw:
        raise ValueError(f"{target}: missing top-level 'blocks' key")

    out: dict[str, BlockSpec] = {}
    for spec in raw["blocks"]:
        if "kind" not in spec or "template" not in spec:
            raise ValueError(f"{target}: block entry missing 'kind' or 'template': {spec!r}")
        out[spec["kind"]] = BlockSpec(
            kind      = spec["kind"],
            container = bool(spec.get("container", False)),
            attrs     = tuple(spec.get("attrs", [])),
            required  = tuple(spec.get("required", [])),
            template  = spec["template"],
        )
    return out


def is_container(kind: str, registry: dict[str, BlockSpec] | None = None) -> bool:
    """Helper used by the parser to dispatch body shape (BlockTree vs str).

    If `kind` is not in the registry, returns False (parser treats unknown
    kinds as leaf, matching the markdown-it / mdx convention).
    """
    reg = registry if registry is not None else load_registry()
    spec = reg.get(kind)
    return bool(spec and spec.container)
