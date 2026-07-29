"""Compact directory tree builder."""

import os
import sys
from typing import List

from .constants import (
    NOISE_DIRS,
    NOISE_EXTENSIONS,
    NOISE_FILES,
    TREE_BRANCH,
    TREE_LAST,
    TREE_PIPE,
    TREE_SPACE,
)


def build_tree(root_path: str) -> str:
    """Return a compact Unicode box-drawing tree of ``root_path``.

    Noise directories and files are skipped, matching the scanner's
    filter so the tree stays in sync with the bundle.
    """
    root_name = os.path.basename(os.path.abspath(root_path))
    lines: List[str] = [f"{root_name}/"]

    def _walk(dirpath: str, prefix: str, is_last_stack: List[bool]) -> None:
        try:
            entries = sorted(os.listdir(dirpath))
        except OSError:
            sys.stderr.write(f"ctxpack: warning: cannot read directory: {dirpath}\n")
            return

        filtered: List[str] = []
        for e in entries:
            full = os.path.join(dirpath, e)
            if os.path.isdir(full) and e in NOISE_DIRS:
                continue
            if not os.path.isdir(full) and (
                e in NOISE_FILES or os.path.splitext(e)[1].lower() in NOISE_EXTENSIONS
            ):
                continue
            filtered.append(e)

        for i, entry in enumerate(filtered):
            is_last = i == len(filtered) - 1
            is_last_stack.append(is_last)

            full = os.path.join(dirpath, entry)
            if os.path.isdir(full):
                connector = TREE_LAST if is_last else TREE_BRANCH
                lines.append(f"{prefix}{connector}{entry}/")
                sub_prefix = prefix + (TREE_SPACE if is_last else TREE_PIPE)
                _walk(full, sub_prefix, is_last_stack)
            else:
                connector = TREE_LAST if is_last else TREE_BRANCH
                lines.append(f"{prefix}{connector}{entry}")

            is_last_stack.pop()

    _walk(root_path, "", [])
    return "\n".join(lines)
