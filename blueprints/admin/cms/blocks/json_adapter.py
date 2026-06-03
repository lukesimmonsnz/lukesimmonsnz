"""BlockTree ↔ JSON adapter for the v2-2 visual editor.

The editor holds the tree client-side as JSON; on every mutation it POSTs
the JSON back, the server re-serializes to MD, and the autosave flow
takes over. JSON is a transport, not a storage format — the source of
truth remains the .md file (with block directives) on disk.
"""
from __future__ import annotations

from .tree import Block, BlockTree, RawSpan, SourceSpan


def tree_to_json(tree: BlockTree) -> list:
    """Convert a BlockTree to a JSON-serializable list.

    Round-trip: tree_from_json(tree_to_json(t)) returns a BlockTree
    semantically equal to t. Note the round-trip loses SourceSpan info —
    nodes coming back from JSON are marked dirty=True so the serializer
    emits canonical form rather than verbatim from source.
    """
    out = []
    for node in tree:
        if isinstance(node, RawSpan):
            out.append({
                "type": "raw",
                "text": node.text,
                "span": [node.span.start, node.span.end],
            })
        elif isinstance(node, Block):
            body = (
                node.body if isinstance(node.body, str)
                else tree_to_json(node.body)
            )
            out.append({
                "type":  "block",
                "kind":  node.kind,
                "attrs": list(node.attrs),    # preserve order
                "body":  body,
                "span":  [node.span.start, node.span.end],
                "level": node.level,
                "dirty": node.dirty,
            })
    return out


def tree_from_json(data: list) -> BlockTree:
    """Convert JSON list back to a BlockTree.

    Marks every node returned as dirty=True (since SourceSpan info is
    no longer authoritative over the original source bytes).
    """
    out = []
    for item in data:
        t = item.get("type")
        if t == "raw":
            sp = item.get("span", [0, len(item["text"])])
            out.append(RawSpan(
                text=item["text"],
                span=SourceSpan(sp[0], sp[1]),
            ))
        elif t == "block":
            body_in = item["body"]
            body = body_in if isinstance(body_in, str) else tree_from_json(body_in)
            sp = item.get("span", [0, 0])
            out.append(Block(
                kind=item["kind"],
                attrs=tuple((k, v) for k, v in item["attrs"]),
                body=body,
                span=SourceSpan(sp[0], sp[1]),
                level=item.get("level", 0),
                dirty=True,    # round-tripped node always emits canonical
            ))
    return tuple(out)
