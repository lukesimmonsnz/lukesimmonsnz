# CMS-IMPL-WAVE-v2-1 — Block parser, AST, seed library

**Status:** design artefact — wave v2-1 of `CMS-SPEC-v2.md` §17.
**PI directive (2026-05-02):** *"Begin §17 wave plan in dependency order,
preserving the conceptual gaps marked at §14."*
**Implementation gap regime:** AST type signatures, grammar, and
round-trip proof obligations stated; PI completes the parser body and
the locality-preserving serializer. The block library Jinja partials
(wave v2-3) and the visual-editor partials (wave v2-2) consume these
contracts.

---

## 1. Scope of this wave

| Item | Surface | PI mastery? |
|---|---|---|
| 1.1 | Grammar — formal definition of `::name{attrs}` directive blocks with nested `:::`, `::::` levels | No (specified here) |
| 1.2 | AST types — `Block`, `RawSpan`, `BlockTree`, `Attrs`, `SourceSpan` | No (specified here) |
| 1.3 | Parser contract `parse : str → BlockTree` with proof obligation | **Yes — §3.3 of CMS-SPEC-v2** |
| 1.4 | Serializer contract `serialize : BlockTree → str` with locality preservation | **Yes — §3.3** |
| 1.5 | Block registry loader — reads `content/_blocks/registry.yaml` | No |
| 1.6 | Twelve seed blocks + three section blocks declared in `registry.yaml` | No |
| 1.7 | Round-trip test corpus + harness | No (corpus authored here; harness exercises PI's parser) |

Out of scope (subsequent waves):

- Visual editor cell rendering (v2-2)
- Block Jinja partials at `templates/blocks/*.html` (v2-3)
- Section blocks' full-bleed CSS (v2-9)

---

## 2. Grammar (v2-1.1)

In ABNF-flavoured notation, with whitespace handling spelled out:

```abnf
document       = *( raw-span / block )

block          = open-marker name [ attrs ] LF body LF close-marker
open-marker    = level-colons                      ; level ≥ 2
close-marker   = level-colons                      ; same level as opener
level-colons   = 2*COLON                           ; "::" at level 0; ":::" at depth-1; "::::" at depth-2; …

name           = 1*( ALPHA / DIGIT / "-" / "_" )

attrs          = "{" *attr-pair "}"
attr-pair      = WSP key "=" value
key            = 1*( ALPHA / DIGIT / "-" / "_" )
value          = bare-value / quoted-value
bare-value     = 1*( VCHAR-without-WSP-RBRACE )
quoted-value   = DQUOTE *(QCHAR / escape) DQUOTE
escape         = "\" ( DQUOTE / "\" )

body           = *( raw-span / block-deeper )       ; mixed: raw text + deeper-nested blocks
block-deeper   = block whose level-colons ≥ enclosing-level+1

raw-span       = 1*( CHAR-not-starting-a-marker )    ; verbatim source bytes
```

**Nesting via colon-count.** A block opened with `::` (level 0) must contain
only deeper blocks opened with `:::` or higher. A block opened with `:::`
(level 1) closes with `:::`, never `::`. This matches MyST/MDX
convention and disambiguates the close marker without backtracking.

**Marker recognition.** A `level-colons` token is recognised only at
the start of a line (preceding character is `\n` or start-of-document)
and followed by either an identifier (open) or LF (close). Other `:`
sequences inside a paragraph are raw text.

**Attribute closing brace tolerance.** A `{` that is not part of a
recognised `attrs` opener (e.g. `{tag}` syntax inside a paragraph)
remains raw text. The parser only treats `{` as significant when
following an `open-marker name`.

---

## 3. AST (v2-1.2)

```python
# blueprints/admin/cms/blocks/tree.py

from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class SourceSpan:
    start:  int    # byte offset, inclusive
    end:    int    # byte offset, exclusive


@dataclass(frozen=True)
class RawSpan:
    """Verbatim source between (or before / after) directive blocks.

    Plain Markdown — paragraphs, headings, lists, images, etc. Not parsed
    into MD AST at this layer. The renderer hands `text` to the
    Markdown engine at render time.
    """
    text:   str
    span:   SourceSpan


# Attrs preserve insertion order. v2-10 round-trip requires that
# untouched blocks emit attrs in the same order they appeared in source.
Attrs = tuple[tuple[str, str], ...]    # ordered, immutable


@dataclass(frozen=True)
class Block:
    kind:    str                  # "callout", "image", "columns", …
    attrs:   Attrs                # ordered key=value pairs
    body:    "BlockTree | str"    # nested for container blocks; str for leaf
    span:    SourceSpan           # full source range, including markers
    level:   int                  # 0 for top-level "::", 1 for ":::", …
    dirty:   bool = False         # set True when editor mutates this node
    # invariant: when dirty=False, source[span.start:span.end] reproduces
    # the block's original on-disk bytes, modulo trailing-LF normalisation.


Node     = Union[Block, RawSpan]
BlockTree = tuple[Node, ...]      # ordered, immutable
```

**Why `dirty` on `Block`.** The serializer's locality property
(§3.3 below) needs a marker to distinguish *"emit canonical form"* from
*"emit verbatim from `span`"*. The editor sets `dirty=True` on any node
it has structurally modified; `dirty` propagates upward only along the
path of modified ancestors (parent of a dirty child is itself dirty
*only if the parent's own attrs changed*; otherwise the parent's marker
bytes can stay verbatim and only its body is rerendered).

**Why `body` is union-typed.** Container blocks (`callout`, `columns`,
`hero`, `column`) recursively contain `BlockTree`. Leaf blocks (`code`,
`image`, `embed`, `divider`) carry a `str` body. The block registry
(§5) declares which kinds are containers; the parser dispatches on it.

---

## 4. Parser contract (v2-1.3) — **PI mastery surface**

```python
# blueprints/admin/cms/blocks/parser.py

from .tree import BlockTree


def parse(md: str) -> BlockTree:
    """Parse a Markdown body into a BlockTree.

    Source-of-truth: the on-disk MD body (the part *after* the
    frontmatter splice in v1's _split_frontmatter). Frontmatter is
    handled upstream in resolver.py and is NOT this function's concern.

    Round-trip obligation (§3.3 of CMS-SPEC-v2):
        serialize(parse(s)) ≡ s

    where ≡ is byte equality modulo a single trailing LF. Specifically:

    1. Plain-MD content (RawSpan) emits verbatim — the parser MUST
       capture inter-block raw text into RawSpan nodes whose `text` is
       byte-identical to the source slice.
    2. Block markers, attributes, and (for leaf blocks) bodies emit
       verbatim — the parser MUST record `span` for each Block such that
       md[span.start:span.end] reconstructs the original on-disk bytes.
    3. Nested block bodies are themselves BlockTree; (1)–(2) apply
       recursively.

    Failure modes:
    - Unmatched open marker → raise BlockParseError with line/column.
    - Mismatched close-marker level → raise BlockParseError.
    - Malformed attrs → raise BlockParseError.
    """
    raise NotImplementedError(
        "PI mastery surface — see CMS-SPEC-v2.md §3.3 and "
        "CMS-IMPL-WAVE-v2-1.md §4. Implement the parser to satisfy "
        "the round-trip identity exercised by tests/cms/test_block_roundtrip.py."
    )


class BlockParseError(ValueError):
    """Raised on malformed directive syntax."""
    def __init__(self, message: str, line: int, col: int):
        super().__init__(f"{message} (line {line}, col {col})")
        self.line = line
        self.col = col
```

**Mathematical mechanics — what PI implements.**

The parser is naturally a two-pass tokenize-then-tree algorithm, but the
spec does not mandate the algorithm. The proof obligation is the contract
above. Two viable strategies:

*Strategy A — line-oriented scanner.* Walk lines; classify each as
open-marker, close-marker, or content. Maintain a stack of open
`(level, kind, attrs, body_start)` frames. On close-marker matching the
top frame's level, pop and emit a `Block`. On EOF with non-empty stack,
raise `BlockParseError`.

Complexity: $O(n)$ in body length, $O(d)$ in nesting depth $d$.

*Strategy B — recursive-descent over a regex pre-tokenizer.* Tokenize
markers as `(MARKER_OPEN, level, name, attrs, line)` and
`(MARKER_CLOSE, level, line)`; everything else is `RAW`. Then
recursive-descent: `parse_doc` accumulates a sequence of `RawSpan` and
`parse_block(level)` results; `parse_block(level)` consumes its
matching close.

Complexity: same. Strategy A is canonically the simpler implementation;
strategy B yields a cleaner stack trace on malformed input.

**The byte-preservation mechanism — the load-bearing detail.** Each
`Block` and `RawSpan` carries a `SourceSpan` referring back to the
original `md` string. The serializer (§4 below) uses `md[span.start:span.end]`
verbatim for any node where `dirty=False`. This is the mathematical
analogue of v1's `_split_frontmatter` raw-text approach: never round-trip
through a normalising representation.

---

## 5. Serializer contract (v2-1.4) — **PI mastery surface**

```python
# blueprints/admin/cms/blocks/serializer.py

from .tree import BlockTree, Block, RawSpan


def serialize(tree: BlockTree, source: str) -> str:
    """Re-emit a BlockTree as Markdown source.

    `source` is the original parse input; clean (dirty=False) nodes
    re-emit verbatim from `source[span.start:span.end]`. Dirty nodes
    re-emit canonically.

    Locality property (§3.3 of CMS-SPEC-v2):

        Let s be a parse input, t = parse(s), and t' a tree obtained by
        editing exactly one node n of t (with n.dirty := True).
        Then for every node m ≠ n in t', the bytes contributed by m to
        serialize(t', s) equal the bytes m contributed in s.

    That is: editing one block does not perturb sibling bytes.

    Canonical form for dirty Blocks:
        - Markers: ":" * (2 + level) + name + (attrs?) + "\n" ... "\n" + close-markers
        - Attrs: "{" + " ".join(f"{k}={quote(v)}" for k,v in attrs) + "}"
        - quote(v): unquoted if v matches r'[A-Za-z0-9_-]+', else "..." with " and \\ escaped
        - Body: recursive serialize for container kinds; verbatim str for leaf kinds
    """
    raise NotImplementedError(
        "PI mastery surface — see CMS-SPEC-v2.md §3.3 and "
        "CMS-IMPL-WAVE-v2-1.md §5. Implement the serializer to satisfy "
        "the locality property exercised by tests/cms/test_block_roundtrip.py."
    )
```

**The two identities, restated.**

$$\sigma(P(s), s) = s \qquad \text{(round-trip on clean tree)}$$

$$\forall m \neq n,\; \mathrm{contrib}_m(\sigma(t', s)) = \mathrm{contrib}_m(s) \qquad \text{(locality on edit)}$$

where $\mathrm{contrib}_m$ is the byte-range a node contributes to the
serialized output.

The two identities together imply the full round-trip property
$\sigma(P(s)) = s$ pointwise per node, plus the
*"editing one block does not perturb sibling bytes"* invariant the v1
`_split_frontmatter` work earned at the frontmatter level.

---

## 6. Block registry (v2-1.5) — mechanical

```python
# blueprints/admin/cms/blocks/registry.py

from dataclasses import dataclass
from pathlib import Path
import yaml

REGISTRY_PATH = Path("content/_blocks/registry.yaml")


@dataclass(frozen=True)
class BlockSpec:
    kind:        str
    container:   bool                # True ⇒ body is BlockTree, False ⇒ str
    attrs:       tuple[str, ...]     # declared attr names (informational)
    required:    tuple[str, ...]     # subset of attrs
    template:    str                 # Jinja partial path under templates/blocks/


def load_registry() -> dict[str, BlockSpec]:
    """Read content/_blocks/registry.yaml into a kind → BlockSpec dict."""
    raw = yaml.safe_load(REGISTRY_PATH.read_text(encoding="utf-8"))
    return {
        spec["kind"]: BlockSpec(
            kind       = spec["kind"],
            container  = spec.get("container", False),
            attrs      = tuple(spec.get("attrs", [])),
            required   = tuple(spec.get("required", [])),
            template   = spec["template"],
        )
        for spec in raw["blocks"]
    }
```

The parser uses `load_registry()` only for the `container` flag (to
decide whether `body` is `BlockTree` or `str`). The renderer uses the
full spec to dispatch to the right Jinja partial.

---

## 7. Round-trip test harness (v2-1.7)

The harness has two layers:

**Layer 1 — fixture round-trip (`test_fixture_roundtrip`).**

```python
# tests/cms/test_block_roundtrip.py  (Pytest)

import pytest
from pathlib import Path
from blueprints.admin.cms.blocks.parser import parse
from blueprints.admin.cms.blocks.serializer import serialize

FIXTURES = Path("tests/cms/fixtures/blocks").glob("*.md")


@pytest.mark.parametrize("path", list(FIXTURES), ids=lambda p: p.stem)
def test_fixture_roundtrip(path):
    src = path.read_text(encoding="utf-8")
    tree = parse(src)
    out = serialize(tree, src)
    assert out == src, f"round-trip mismatch on {path.name}"
```

**Layer 2 — locality property (`test_locality`).**

```python
def test_locality_callout_edit():
    src = (Path("tests/cms/fixtures/blocks/02_callout.md")
           .read_text(encoding="utf-8"))
    tree = parse(src)

    # Find the callout, mutate its body, mark dirty.
    edited = _mutate_block(tree, kind="callout",
                           new_body="Mutated body line 1.\nMutated body line 2.")
    out = serialize(edited, src)

    # Expectation: pre-callout RawSpan and post-callout RawSpan emit verbatim.
    assert out.startswith(_prefix_through_open_marker(src, edited))
    assert out.endswith(_suffix_after_close_marker(src, edited))
```

PI provides `_mutate_block`, `_prefix_through_open_marker`,
`_suffix_after_close_marker` — these are test plumbing, not parser
mechanics, so they are PI's to write per the project's "code as theory"
posture.

---

## 8. Seed corpus (v2-1.7)

Eight fixture files under `tests/cms/fixtures/blocks/`, each
hand-authored, covering the surface area of the grammar:

| Fixture | Exercises |
|---|---|
| `01_paragraph_only.md` | No blocks — pure RawSpan. Round-trip is trivially the identity. |
| `02_callout.md` | Single top-level block with attrs (type, title). |
| `03_image_leaf.md` | Leaf block (no body). Self-closing edge case if grammar supports it. |
| `04_columns_nested.md` | `::columns` containing `::: column` × 2. Two-level nesting. |
| `05_callout_in_column.md` | `::columns` → `::: column` → `:::: callout`. Three-level nesting. |
| `06_attrs_quoted.md` | Attrs with spaces, escaped quotes, and bare-value mix. |
| `07_mixed_md_and_blocks.md` | Headings, paragraphs, image, then a callout, then more MD. |
| `08_consecutive_blocks.md` | Two top-level blocks back-to-back with one blank line between. |

Each fixture is **byte-stable**: PI MUST NOT reformat them when adding
or amending. `git diff` on a fixture file means a parser/grammar regression.

---

## 9. Verification gate (PI sign-off)

Wave v2-1 closes when:

1. `pytest tests/cms/test_block_roundtrip.py` passes 8/8 round-trip tests.
2. `pytest tests/cms/test_block_roundtrip.py::test_locality_*` passes for
   at least three locality scenarios (callout edit, columns reorder,
   attr-only change).
3. Parsing a corpus of v1 blog posts (5 posts) against `parse` returns
   a `BlockTree` of all-`RawSpan` nodes (no false-positive directive
   recognition in plain-MD content). Verifiable with:

   ```bash
   python -c "
   from pathlib import Path
   from blueprints.admin.cms.blocks.parser import parse
   for p in Path('content/blog').glob('*.md'):
       body = p.read_text(encoding='utf-8').split('---', 2)[2]
       tree = parse(body)
       assert all(type(n).__name__ == 'RawSpan' for n in tree), p.name
   "
   ```

4. Linting clean — `parser.py`, `serializer.py`, `tree.py`, `registry.py`
   import without raising (the `NotImplementedError` is in function bodies,
   not at import time).

---

## 10. Dependent waves unlocked

| Wave | Now buildable |
|---|---|
| v2-2 | Visual editor partials — render each `Block` / `RawSpan` as a UI cell |
| v2-3 | Block Jinja partials — `templates/blocks/<kind>.html` per registry entry |
| v2-9 | Section blocks (`section-hero`, `section-feature-grid`, `section-cta`) — special-case full-bleed CSS in their partials |

v2-4 (theme presets), v2-5 (media transforms), v2-6 (template slots),
v2-8 (SEO panel) are independent of the parser and can run in parallel.
