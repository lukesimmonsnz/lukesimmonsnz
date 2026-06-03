# Mixed plain Markdown and directive blocks

A paragraph of plain MD with a [link](/research/auckland/) embedded.

## Sub-heading

Another paragraph.

![Plain MD image syntax](/static/media/cc/plain.png)

::callout{type=warning}
A warning callout in the middle of plain content.
::

A paragraph after the block.

```python
# A fenced code block — plain MD, NOT a directive block.
# Round-trip MUST emit this verbatim.
def hello():
    return "world"
```

Final paragraph after the fence.
