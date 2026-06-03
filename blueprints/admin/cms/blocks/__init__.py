"""Block-directive parser, AST, and registry for CMS v2.

See docs/CMS-SPEC-v2.md §3 and docs/CMS-IMPL-WAVE-v2-1.md for the
grammar, AST, and round-trip proof obligations.

Public surface:

    from blueprints.admin.cms.blocks import (
        parse, serialize,
        Block, RawSpan, BlockTree, SourceSpan, Attrs,
        BlockParseError,
        load_registry, BlockSpec,
    )
"""

from .tree import Block, RawSpan, BlockTree, SourceSpan, Attrs
from .parser import parse, BlockParseError
from .serializer import serialize
from .registry import load_registry, BlockSpec

__all__ = [
    "Block",
    "RawSpan",
    "BlockTree",
    "SourceSpan",
    "Attrs",
    "parse",
    "serialize",
    "BlockParseError",
    "load_registry",
    "BlockSpec",
]
