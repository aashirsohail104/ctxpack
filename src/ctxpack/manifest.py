"""Manifest construction and one-line summary."""

from typing import Dict, List


def build_manifest(
    budget: int,
    used: int,
    included: List[Dict],
    excluded: List[Dict],
) -> Dict:
    """Assemble the manifest dict per SPEC.md §Manifest Schema."""
    return {
        "budget": budget,
        "used": used,
        "included": included,
        "excluded": excluded,
    }


def one_line_summary(
    included_count: int,
    used: int,
    budget: int,
    excluded_count: int,
) -> str:
    return f"ctxpack: {included_count} files included ({used}/{budget} tokens), {excluded_count} files excluded\n"
