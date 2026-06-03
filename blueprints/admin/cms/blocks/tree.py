"""AST types for the block-directive layer (CMS v2).

Spec: docs/CMS-SPEC-v2.md §3.
Wave: docs/CMS-IMPL-WAVE-v2-1.md §3.

Mathematical posture
--------------------
A parsed Markdown body is a `BlockTree` — an ordered, immutable
sequence of `Node = Block | RawSpan`. Plain Markdown between blocks is
captured as `RawSpan` and never reformatted by the v2 layer; inline
Markdown rendering is the responsibility of the renderer (markdown-it,
mistune, etc.) at template time, not this module.

The byte-preservation invariant (round-trip identity, §3.3 of the spec)
hangs on `SourceSpan`: every node carries the byte-range it occupied in
the original parse input, and the serializer (when a node is `dirty=False`)
re-emits via `source[span.start:span.end]` rather than canonicalising.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class SourceSpan:
    """Half-open byte range into the parse input string.

    `source[span.start:span.end]` reproduces the node's original bytes
    when `dirty=False` on the carrying Block, or always for RawSpan.
    """
    start: int
    end:   int

    def slice_of(self, source: str) -> str:
        return source[self.start:self.end]


@dataclass(frozen=True)
class RawSpan:
    """Verbatim source between (or before / after) directive blocks.

    `text` is byte-identical to `source[span.start:span.end]`. The
    parser MUST satisfy this invariant — tests in
    tests/cms/test_block_roundtrip.py exercise it indirectly via the
    round-trip property.
    """
    text: str
    span: SourceSpan


# Attrs preserve the order they appeared in the source. The serializer
# emits them in this order for clean blocks (§5 of the wave doc); for
# dirty blocks the editor is responsible for choosing the order it
# wants serialized.
Attrs = tuple[tuple[str, str], ...]


@dataclass(frozen=True)
class Block:
    """A directive block, either container or leaf.

    Container blocks (registry.container=True) carry a recursive
    `body: BlockTree`; leaf blocks carry a verbatim `body: str`. The
    parser dispatches on the registry to decide.

    `dirty` distinguishes "emit verbatim from span" from "emit canonical
    form" at serialization. The editor sets it on any node whose attrs
    or body it has structurally modified. A block with a dirty descendant
    is itself dirty only if its own attrs changed; otherwise its open /
    close marker bytes can stay verbatim and only its body gets
    re-serialized.
    """
    kind:  str
    attrs: Attrs
    body:  "BlockTree | str"
    span:  SourceSpan
    level: int                # 0 ⇒ "::", 1 ⇒ ":::", 2 ⇒ "::::", …
    dirty: bool = False


Node = Union[Block, RawSpan]
BlockTree = tuple[Node, ...]
