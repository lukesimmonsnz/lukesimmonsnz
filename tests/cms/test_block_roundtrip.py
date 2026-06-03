"""Round-trip + locality tests for the v2 block parser/serializer.

Spec:    docs/CMS-SPEC-v2.md §3.3
Wave:    docs/CMS-IMPL-WAVE-v2-1.md §7

These tests exercise the PI mastery surface. They WILL FAIL with
NotImplementedError until parser.py and serializer.py have bodies.
That is expected and intentional — wave v2-1 closes when this suite
turns green.
"""

from __future__ import annotations

import os
from pathlib import Path

import pytest

from blueprints.admin.cms.blocks import parse, serialize
from blueprints.admin.cms.blocks.tree import Block, RawSpan


FIXTURES_DIR = Path(__file__).parent / "fixtures" / "blocks"
FIXTURES = sorted(FIXTURES_DIR.glob("*.md"))


# ─── Layer 1 — round-trip identity ───────────────────────────────────

@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_fixture_roundtrip(path: Path) -> None:
    """For every fixture: serialize(parse(s), s) == s, byte-identical.

    Proof obligation from CMS-SPEC-v2 §3.3:

        σ(P(s), s) = s

    """
    src = path.read_text(encoding="utf-8")
    tree = parse(src)
    out = serialize(tree, src)
    assert out == src, f"round-trip mismatch on {path.name}"


# ─── Layer 2 — locality property ─────────────────────────────────────

def _find_block(tree, kind: str):
    """Walk a BlockTree and return the first Block of the given kind."""
    for node in tree:
        if isinstance(node, Block) and node.kind == kind:
            return node
        if isinstance(node, Block) and isinstance(node.body, tuple):
            found = _find_block(node.body, kind)
            if found is not None:
                return found
    return None


def test_locality_callout_body_edit() -> None:
    """Editing a callout's body must not perturb sibling RawSpan bytes.

    The callout's open-marker, close-marker, and attrs MUST remain
    verbatim if the editor only changed the inner body. The pre-callout
    and post-callout RawSpans MUST emit byte-identically.

    Proof obligation from CMS-SPEC-v2 §3.3:

        ∀ m ≠ n,  contrib_m(σ(t', s)) = contrib_m(s)

    """
    src = (FIXTURES_DIR / "02_callout.md").read_text(encoding="utf-8")
    tree = parse(src)

    callout = _find_block(tree, "callout")
    assert callout is not None, "fixture 02 should contain a callout"

    # Locate the original RawSpan tails — bytes before / after the callout.
    pre_bytes = src[: callout.span.start]
    post_bytes = src[callout.span.end:]

    # Mutate: replace body with new text, mark dirty. (The editor would
    # do this via a higher-level helper; for the test we operate on the
    # frozen dataclass directly via dataclasses.replace.)
    import dataclasses
    new_callout = dataclasses.replace(
        callout,
        body=("Mutated body line 1.\nMutated body line 2.",) if isinstance(callout.body, tuple)
              else "Mutated body line 1.\nMutated body line 2.",
        dirty=True,
    )
    new_tree = tuple(
        new_callout if (isinstance(n, Block) and n.kind == "callout") else n
        for n in tree
    )

    out = serialize(new_tree, src)

    assert out.startswith(pre_bytes), (
        "pre-callout bytes must emit verbatim — locality violation upstream"
    )
    assert out.endswith(post_bytes), (
        "post-callout bytes must emit verbatim — locality violation downstream"
    )


def test_locality_attr_only_edit() -> None:
    """Editing only a block's attrs must not perturb its body bytes.

    If the editor changes a callout's `title` but not its body, the body
    text MUST emit verbatim from source (not re-serialized).
    """
    src = (FIXTURES_DIR / "02_callout.md").read_text(encoding="utf-8")
    tree = parse(src)

    callout = _find_block(tree, "callout")
    assert callout is not None

    # The body, captured from source pre-edit.
    body_text = src[callout.span.start:callout.span.end]
    # We can't directly slice "body within markers" without parser help,
    # so we settle for a coarser invariant: the rendered output for the
    # un-edited body's *content lines* appear unchanged in `out`.

    import dataclasses
    new_attrs = (("type", "warning"), ("title", "Updated title"))
    new_callout = dataclasses.replace(callout, attrs=new_attrs, dirty=True)
    new_tree = tuple(
        new_callout if (isinstance(n, Block) and n.kind == "callout") else n
        for n in tree
    )
    out = serialize(new_tree, src)

    # The original body line must still be present — body bytes preserved.
    assert "Single-track operation through 2026" in out, (
        "attr-only edit must not perturb body bytes"
    )
    # The new title must be in the output.
    assert "Updated title" in out, "new attr value must reach output"


def test_plain_md_yields_only_rawspan() -> None:
    """Pure plain-MD fixture must parse to a tree of only RawSpan nodes.

    No false-positive directive recognition. This is verification gate
    item #3 from CMS-IMPL-WAVE-v2-1.md §9.
    """
    src = (FIXTURES_DIR / "01_paragraph_only.md").read_text(encoding="utf-8")
    tree = parse(src)
    assert all(isinstance(n, RawSpan) for n in tree), (
        f"expected all RawSpan, got kinds: {[type(n).__name__ for n in tree]}"
    )


def test_blog_corpus_is_plain_md() -> None:
    """Existing v1 blog posts contain no directive blocks.

    Verification gate item #3 (CMS-IMPL-WAVE-v2-1.md §9). All 5 v1 blog
    posts MUST parse to a tree of only RawSpan — confirms parsing is a
    purely additive layer over v1 content.
    """
    blog_dir = Path(__file__).resolve().parents[2] / "content" / "blog"
    if not blog_dir.exists():
        pytest.skip(f"blog directory not found at {blog_dir}")

    posts = list(blog_dir.glob("*.md"))
    assert len(posts) >= 1, "expected at least one v1 blog post"

    for post in posts:
        full = post.read_text(encoding="utf-8")
        # Strip frontmatter using v1's convention (--- ... ---).
        parts = full.split("---", 2)
        body = parts[2] if len(parts) == 3 else full
        tree = parse(body)
        assert all(isinstance(n, RawSpan) for n in tree), (
            f"{post.name}: false-positive directive recognition in v1 content; "
            f"got kinds {[type(n).__name__ for n in tree]}"
        )
