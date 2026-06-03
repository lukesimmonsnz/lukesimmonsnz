"""Block-directive renderer — v2-3.

Spec:    docs/CMS-SPEC-v2.md §3.4
Wave:    v2-3 (block library Jinja partials + registry dispatch)

Public surface
--------------
    render_md_with_blocks(body, jinja_env) -> str

Render pipeline for a Markdown body that may contain ``::directive``
blocks:

    parse(body) -> BlockTree
    for each node:
        RawSpan -> markdown.Markdown.convert(text)
        Block   -> jinja_env.get_template("blocks/<kind>.html").render(...)

Round-trip guarantee: if the body contains no Block nodes (all-RawSpan,
i.e. v1 plain MD), the output is identical to a direct
``markdown.Markdown.convert(body)`` call.
"""

from __future__ import annotations

import re
import markdown as _markdown_lib

from .parser import parse
from .tree import Block, RawSpan, BlockTree

# Blocks whose body must NOT be passed through the markdown renderer.
# (Code bodies are raw text; the template HTML-escapes them itself.)
_SKIP_MD_BODY: frozenset[str] = frozenset({"code"})

# Blocks whose leaf body is inline-only (strip the wrapping <p>).
_INLINE_BODY: frozenset[str] = frozenset({"heading", "button", "divider", "embed"})


def _make_md() -> _markdown_lib.Markdown:
    """Return a fresh Markdown converter."""
    return _markdown_lib.Markdown(
        extensions=["extra", "codehilite", "sane_lists", "smarty"],
        output_format="html5",
    )


def _strip_outer_p(html: str) -> str:
    """Remove a single wrapping <p>...</p> from inline-context output."""
    return re.sub(r"^\s*<p>(.*?)</p>\s*$", r"\1", html.strip(), flags=re.DOTALL)


def _render_tree(tree: BlockTree, md: _markdown_lib.Markdown, jinja_env) -> str:
    """Recursively render a BlockTree to an HTML string."""
    parts: list[str] = []
    for node in tree:
        if isinstance(node, RawSpan):
            if node.text.strip():
                md.reset()
                parts.append(md.convert(node.text))
        elif isinstance(node, Block):
            parts.append(_render_block(node, md, jinja_env))
    return "".join(parts)


def _render_block(block: Block, md: _markdown_lib.Markdown, jinja_env) -> str:
    """Render a single Block to HTML via its Jinja partial."""
    import jinja2

    attrs = dict(block.attrs)

    # Render body
    if isinstance(block.body, str):
        raw = block.body
        if block.kind in _SKIP_MD_BODY:
            body_html = raw          # template does its own escaping
        elif raw.strip():
            md.reset()
            body_html = md.convert(raw)
            if block.kind in _INLINE_BODY:
                body_html = _strip_outer_p(body_html)
        else:
            body_html = ""
    else:
        # Container: body is a nested BlockTree
        body_html = _render_tree(block.body, md, jinja_env)

    # Normalise hyphens -> underscores for template filenames
    # (kind "section-hero" -> template "blocks/section_hero.html")
    template_name = f"blocks/{block.kind.replace('-', '_')}.html"
    try:
        tmpl = jinja_env.get_template(template_name)
        return tmpl.render(attrs=attrs, body=body_html, block=block)
    except jinja2.TemplateNotFound:
        # Graceful fallback: emit body unchanged (unknown block kind)
        return body_html


def render_md_with_blocks(body: str, jinja_env) -> str:
    """Render a Markdown body string that may contain ``::directive`` blocks.

    Args:
        body:      Raw Markdown body text (no frontmatter).
        jinja_env: The Flask app's Jinja2 environment, used to load
                   ``templates/blocks/<kind>.html`` partials.

    Returns:
        An HTML string suitable for ``{{ ... | safe }}`` in a template.

    Backward-compatible: if ``body`` contains no directive blocks the
    output equals ``markdown.Markdown(...).convert(body)``.
    """
    tree = parse(body)

    # Fast path: all-RawSpan tree (v1 plain MD) — byte-identical output
    if all(isinstance(n, RawSpan) for n in tree):
        md = _make_md()
        return md.convert(body)

    return _render_tree(tree, _make_md(), jinja_env)
