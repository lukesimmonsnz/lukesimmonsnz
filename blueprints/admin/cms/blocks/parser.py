"""Block-directive parser — v2-1 implementation.

Spec:    docs/CMS-SPEC-v2.md §3.2-§3.3
Wave:    docs/CMS-IMPL-WAVE-v2-1.md §4
Grammar: CMS-IMPL-WAVE-v2-1.md §2

Round-trip proof obligation (§3.3 of CMS-SPEC-v2):

    serialize(parse(s), s) == s            # byte-identical
    locality:  ∀ m ≠ n,  contrib_m(serialize(t', s)) == contrib_m(s)

Strategy A (line-oriented scanner): walk lines, maintain a stack of
open frames. Each Block/RawSpan carries SourceSpan for byte-preservation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Optional

from .tree import Block, BlockTree, RawSpan, SourceSpan, Attrs


# ---------------------------------------------------------------------------
# Compiled regexes
# ---------------------------------------------------------------------------

# Open marker:  ::name{attrs}  or  ::: name  or  ::::name{...}
# Group 1 = colons (2+), Group 2 = kind (word with optional hyphens),
# Group 3 = attrs text (contents of braces, may be empty or absent)
_OPEN_RE = re.compile(r'^(:{2,})\s*([\w][\w-]*)\s*(?:\{(.*)\})?\s*$')

# Close marker: exactly colons, optional trailing whitespace — no name
_CLOSE_RE = re.compile(r'^(:{2,})\s*$')


# ---------------------------------------------------------------------------
# Error type
# ---------------------------------------------------------------------------

class BlockParseError(ValueError):
    """Raised on malformed directive syntax.

    Attributes:
        line, col: 1-indexed source location of the offending token.
    """
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"{message} (line {line}, col {col})")
        self.line = line
        self.col = col


# ---------------------------------------------------------------------------
# Internal frame (stack entry while parsing)
# ---------------------------------------------------------------------------

@dataclass
class _Frame:
    kind:      str
    attrs:     Attrs
    level:     int    # colon_count - 2
    open_start: int   # byte offset of start of open-marker line
    nodes:     List   # accumulated child Node objects (Block | RawSpan)
    raw_start: int    # start of current raw-text accumulation
    container: bool   # True → body is BlockTree; False → body is str


# ---------------------------------------------------------------------------
# Attribute parser
# ---------------------------------------------------------------------------

def parse_attrs(attrs_text: str) -> Attrs:
    """Parse the contents of a ``{...}`` attribute block.

    Grammar::

        attrs       = *attr-pair
        attr-pair   = WSP key "=" value
        bare-value  = 1*( ALPHA / DIGIT / "-" / "_" / "/" / "." / "#" )
        quoted-value = DQUOTE *(QCHAR / escape) DQUOTE
        escape       = "\\\\" | "\\\""

    Returns attrs in source order as a frozen tuple-of-pairs.

    Raises:
        BlockParseError: on malformed pair (missing ``=``, unclosed quote).
    """
    result: list[tuple[str, str]] = []
    s = attrs_text.strip()
    i = 0
    n = len(s)

    while i < n:
        # skip whitespace
        while i < n and s[i] in ' \t':
            i += 1
        if i >= n:
            break

        # read key (stops at '=', whitespace, or end)
        key_start = i
        while i < n and s[i] not in '= \t':
            i += 1
        key = s[key_start:i]
        if not key:
            raise BlockParseError(f"empty attribute key near position {i}", 0, i + 1)

        # skip whitespace before '='
        while i < n and s[i] in ' \t':
            i += 1
        if i >= n or s[i] != '=':
            raise BlockParseError(f"expected '=' after key {key!r}", 0, i + 1)
        i += 1  # consume '='

        # read value
        if i < n and s[i] == '"':
            # quoted value — handles \" and \\ escapes
            i += 1  # consume opening quote
            parts: list[str] = []
            while i < n:
                if s[i] == '\\' and i + 1 < n and s[i + 1] in ('"', '\\'):
                    parts.append(s[i + 1])
                    i += 2
                elif s[i] == '"':
                    i += 1  # consume closing quote
                    break
                else:
                    parts.append(s[i])
                    i += 1
            value = ''.join(parts)
        else:
            # bare value — stops at whitespace
            val_start = i
            while i < n and s[i] not in ' \t':
                i += 1
            value = s[val_start:i]

        result.append((key, value))

    return tuple(result)


# ---------------------------------------------------------------------------
# Main parser
# ---------------------------------------------------------------------------

def parse(md: str) -> BlockTree:
    """Parse a Markdown body into a BlockTree.

    Args:
        md: The Markdown body (NOT including frontmatter — frontmatter is
            handled upstream in resolver._split_frontmatter).

    Returns:
        A BlockTree (tuple of RawSpan and Block nodes).

    Raises:
        BlockParseError: on malformed directive syntax (unmatched marker,
            mismatched close-marker level, malformed attrs).
    """
    from .registry import is_container as _is_container, load_registry
    registry = load_registry()

    stack: list[_Frame] = []
    top_nodes: list = []
    top_raw_start: int = 0
    pos: int = 0

    for line in md.splitlines(keepends=True):
        line_start = pos
        line_end   = pos + len(line)
        pos        = line_end
        stripped   = line.rstrip('\r\n')

        # Inside a leaf block: skip open markers, only watch for matching close
        in_leaf = bool(stack) and not stack[-1].container
        open_m  = None if in_leaf else _OPEN_RE.match(stripped)
        close_m = None if open_m  else _CLOSE_RE.match(stripped)

        if open_m:
            # ── Flush raw text before this open marker ──────────────────
            if stack:
                f = stack[-1]
                text = md[f.raw_start:line_start]
                if text:
                    f.nodes.append(RawSpan(text=text,
                                           span=SourceSpan(f.raw_start, line_start)))
                # f.raw_start stays unchanged; will be reset on child close
            else:
                text = md[top_raw_start:line_start]
                if text:
                    top_nodes.append(RawSpan(text=text,
                                             span=SourceSpan(top_raw_start, line_start)))
                # top_raw_start stays unchanged; reset on frame close

            # ── Parse attrs (tolerant: bad attrs → empty tuple) ─────────
            colons    = open_m.group(1)
            kind      = open_m.group(2)
            attrs_raw = (open_m.group(3) or '').strip()
            try:
                attrs = parse_attrs(attrs_raw) if attrs_raw else ()
            except BlockParseError:
                attrs = ()

            level = len(colons) - 2
            cont  = _is_container(kind, registry)

            # ── Push new frame ───────────────────────────────────────────
            stack.append(_Frame(
                kind=kind, attrs=attrs, level=level,
                open_start=line_start,
                nodes=[], raw_start=line_end,
                container=cont,
            ))

        elif close_m and stack:
            close_level = len(close_m.group(1)) - 2
            if stack[-1].level == close_level:
                # ── Matching close: pop frame and build Block ────────────
                f = stack.pop()

                if f.container:
                    # Flush remaining raw inside container
                    text = md[f.raw_start:line_start]
                    if text:
                        f.nodes.append(RawSpan(text=text,
                                               span=SourceSpan(f.raw_start, line_start)))
                    body: BlockTree | str = tuple(f.nodes)
                else:
                    # Leaf: body is verbatim text between markers
                    body = md[f.raw_start:line_start]

                block = Block(
                    kind=f.kind,
                    attrs=f.attrs,
                    body=body,
                    span=SourceSpan(f.open_start, line_end),
                    level=f.level,
                )

                # Add block to parent frame or top level
                if stack:
                    parent = stack[-1]
                    parent.nodes.append(block)
                    parent.raw_start = line_end
                else:
                    top_nodes.append(block)
                    top_raw_start = line_end
            # else: mismatched colon-count — treat line as raw (tolerant)

        # else: raw line — accumulation is implicit (tracked via raw_start)

    # ── Flush any remaining raw text at top level ───────────────────────
    text = md[top_raw_start:]
    if text:
        top_nodes.append(RawSpan(text=text,
                                 span=SourceSpan(top_raw_start, len(md))))

    return tuple(top_nodes)
