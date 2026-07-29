"""Budget manager: select files into a markdown bundle.

Implements the spec's head-only truncation policy. Files whose section
would exceed the remaining budget are head-truncated and a
``[... TRUNCATED ...]`` marker is appended.
"""

import os
from typing import Dict, List, Tuple

from .constants import EXT_TO_LANG, TRUNCATION_MARKER
from .utils import count_tokens, escape_markdown


def _build_fence(content: str) -> str:
    """Return a backtick fence longer than the longest run in ``content``."""
    max_bt = 0
    bt_count = 0
    for ch in content:
        if ch == "`":
            bt_count += 1
            if bt_count > max_bt:
                max_bt = bt_count
        else:
            bt_count = 0
    return "`" * max(max_bt + 1, 3)


def _file_section(
    file_path: str,
    content: str,
) -> Tuple[str, int]:
    """Build the full (un-truncated) markdown section for one file."""
    _, ext = os.path.splitext(file_path)
    lang = EXT_TO_LANG.get(ext.lower(), "")

    file_header = f"### {escape_markdown(file_path)}\n\n"
    fence = _build_fence(content)
    code_start = f"{fence}{lang}\n"
    code_end = f"\n{fence}\n\n"

    section = file_header + code_start + content + code_end
    return section, count_tokens(section)


def bundle_files(
    ranked_files: List[Tuple[str, str, float, int]],
    budget: int,
    tree_str: str,
    task_desc: str,
    root_path: str,
) -> Tuple[str, int, List[Dict], List[Dict], bool]:
    """Assemble the markdown bundle, respecting the token budget.

    Returns ``(bundle, used_tokens, included, excluded, tree_included)``.
    """
    project_name = os.path.basename(os.path.abspath(root_path))

    header = f"# ctxpack bundle -- {project_name}\n\n"
    task_section = f"## Task\n\n{task_desc}\n\n"

    base = header + task_section
    base_tokens = count_tokens(base)

    if base_tokens > budget:
        bundle = base[: max(1, budget * 4)]
        return bundle, count_tokens(bundle), [], [], False

    bundle_parts: List[str] = [header, task_section]
    remaining = budget - base_tokens
    included: List[Dict] = []
    excluded: List[Dict] = []
    tree_included = False

    tree_full = f"## Project Structure\n\n```\n{tree_str}\n```\n\n"
    tree_cost = count_tokens(tree_full)

    if tree_cost <= remaining:
        bundle_parts.append(tree_full)
        remaining -= tree_cost
        tree_included = True

    for file_path, content, score, content_tokens in ranked_files:
        _, ext = os.path.splitext(file_path)
        lang = EXT_TO_LANG.get(ext.lower(), "")

        file_header = f"### {escape_markdown(file_path)}\n\n"
        fence = _build_fence(content)
        code_start = f"{fence}{lang}\n"
        code_end = f"\n{fence}\n\n"

        overhead = file_header + code_start + code_end
        overhead_tokens = count_tokens(overhead)
        total_needed = overhead_tokens + content_tokens

        if total_needed <= remaining:
            section = file_header + code_start + content + code_end
            bundle_parts.append(section)
            remaining -= count_tokens(section)
            included.append({
                "path": file_path,
                "tokens": count_tokens(section),
                "reason": f"Relevance score: {score:.4f}",
            })
        elif overhead_tokens < remaining:
            trunc_overhead = file_header + code_start + TRUNCATION_MARKER + code_end
            max_content_chars = remaining * 4 - len(trunc_overhead)
            if max_content_chars > 0:
                truncated = content[:max_content_chars]
                section = file_header + code_start + truncated + TRUNCATION_MARKER + code_end
                bundle_parts.append(section)
                remaining -= count_tokens(section)
                included.append({
                    "path": file_path,
                    "tokens": count_tokens(section),
                    "truncated": True,
                    "reason": "Head-only truncation: file too large for remaining budget",
                })
            else:
                excluded.append({"path": file_path, "reason": "File overhead exceeds remaining budget"})
        else:
            excluded.append({"path": file_path, "reason": "File too large for remaining budget"})

    bundle = "".join(bundle_parts)
    used = count_tokens(bundle)
    return bundle, used, included, excluded, tree_included
