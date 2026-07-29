"""Small utilities shared across modules."""

import math


def count_tokens(text: str) -> int:
    """Count tokens using the spec rule: ``ceil(len(text) / 4)``.

    Every character counts: whitespace, newlines, punctuation. No external
    tokenizers are used — the rule is deterministic and identical across
    all implementations.
    """
    return math.ceil(len(text) / 4)


def escape_markdown(text: str) -> str:
    """Escape characters that would change heading/list semantics in markdown."""
    return text.replace("#", "\\#").replace("<", "\\<").replace(">", "\\>")
