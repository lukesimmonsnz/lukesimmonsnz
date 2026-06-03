"""Block-tree serializer — v2-1 implementation.

Spec:    docs/CMS-SPEC-v2.md §3.3
Wave:    docs/CMS-IMPL-WAVE-v2-1.md §5

Locality property (the load-bearing invariant):

    Let s be a parse input, t = parse(s), and t' a tree obtained by
    editing exactly one node n of t (with n.dirty = True). Then for
    every node m ≠ n in t', the bytes contributed by m to
    serialize(t', s) equal the bytes m contributed in s.

        ∀ m ≠ n,  contrib_m(σ(t', s)) = contrib_m(s)

This is mechanically realised by the rule:

    if not node.dirty:
        emit source[node.span.start:node.span.end]
    else:
        emit canonical_form(node)

The serializer never reformats untouched bytes — the v2 analogue of
v1's _split_frontmatter raw-text approach.
"""

from __future__ import annotations

import re

from .tree import Block, BlockTree, RawSpan


# ---------------------------------------------------------------------------
# Attribute quoting
# ---------------------------------------------------------------------------

_BARE_RE = re.compile(r'^[A-Za-z0-9_./#-]+$')


def quote_attr(value: str) -> str:
    """Render a single attribute value using v2-1.5 canonical quoting rules.

    Bare-value form when value matches ``r'[A-Za-z0-9_./#-]+'``; otherwise
    double-quoted with ``\\`` and ``"`` escaped.

    >>> quote_attr("article")
    'article'
    >>> quote_attr("A title with spaces")
    '"A title with spaces"'
    >>> quote_attr('He said \\"hi\\"')
    '"He said \\\\\\"hi\\\\\\""'
    """
    if _BARE_RE.match(value):
        return value
    escaped = value.replace('\\', '\\\\').replace('"', '\\"')
    return f'"{escaped}"'


# ---------------------------------------------------------------------------
# Internal canonical-form emitter
# ---------------------------------------------------------------------------

def _emit_block(block: Block, source: str) -> str:
    """Canonical form for a dirty Block.

    Format::

        {colons}{name}[{{attrs}}]\\n
        {body_str}
        {colons}\\n

    Where ``body_str`` is the recursive serialization of child nodes
    (preserving verbatim bytes for unedited descendants), and ``colons``
    = ``':' * (2 + block.level)``.

    Args:
        block:  A Block with ``dirty=True``.
        source: The original parse input (passed through for verbatim
                emission of clean descendants).
    """
    colons = ':' * (2 + block.level)

    # Open marker
    if block.attrs:
        attrs_inner = ' '.join(
            f'{k}={quote_attr(v)}' for k, v in block.attrs
        )
        open_line = f'{colons}{block.kind}{{{attrs_inner}}}'
    else:
        open_line = f'{colons}{block.kind}'

    # Body
    if isinstance(block.body, str):
        body_str = block.body
    else:
        # BlockTree — recurse; clean descendants emit verbatim from source
        body_str = serialize(block.body, source)

    # Close marker
    close_line = colons

    # Full block: open\n + body (may end with \n) + close\n
    return f'{open_line}\n{body_str}{close_line}\n'


# ---------------------------------------------------------------------------
# Public serialize
# ---------------------------------------------------------------------------

def serialize(tree: BlockTree, source: str) -> str:
    """Re-emit a BlockTree as Markdown source.

    Args:
        tree:   The (possibly edited) BlockTree.
        source: The original parse input. Clean (dirty=False) nodes
                re-emit verbatim from source[span.start:span.end].

    Returns:
        The serialized Markdown body. The round-trip identity
        ``serialize(parse(s), s) == s`` holds when the tree is unedited.

    Locality: editing node n (setting n.dirty=True) only changes the
    bytes contributed by n; all m ≠ n emit verbatim from source.
    """
    parts: list[str] = []

    for node in tree:
        if isinstance(node, str):
            # Raw string elements — e.g. from test mutations that place a
            # bare str inside a tuple body. Emit directly.
            parts.append(node)
        elif isinstance(node, RawSpan):
            # Always verbatim — RawSpan is never dirty.
            parts.append(node.text)
        elif isinstance(node, Block):
            if not node.dirty:
                # Verbatim from source — the locality invariant.
                parts.append(source[node.span.start:node.span.end])
            else:
                parts.append(_emit_block(node, source))

    return ''.join(parts)
