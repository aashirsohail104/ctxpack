"""File ranker: combines task keyword overlap with extension priority.

Implements the algorithm in ``SPEC.md §Ranking Strategy``:

1. Tokenize --task into lowercase tokens, filter stopwords and short tokens.
2. For each file, count task-token occurrences, normalize by content length.
3. Score extension: .py/.js/.ts=10, .md=7, .json=3, others=2.
4. Final = (keyword_ratio * 0.6) + (extension_score / 10 * 0.4).
5. Sort descending.

Returns a list of ``(path, content, score, tokens)`` tuples plus the
files that were unreadable or minified and therefore excluded.
"""

import os
import sys
from typing import Dict, List, Set, Tuple

from .constants import EXT_TO_LANG
from .extension import get_extension_score
from .reader import is_minified, read_file
from .utils import count_tokens


def _detect_language(path: str) -> str:
    _, ext = os.path.splitext(path)
    return EXT_TO_LANG.get(ext.lower(), "")


def rank_files(
    included_files: List[Dict],
    task_keywords: Set[str],
) -> Tuple[List[Tuple[str, str, float, int]], List[Dict]]:
    """Score and sort files. See module docstring for the formula."""
    excluded: List[Dict] = []

    if not task_keywords:
        ranked: List[Tuple[str, str, float, int]] = []
        for f in included_files:
            content = read_file(f["full_path"])
            if content is None:
                excluded.append({"path": f["path"], "reason": "Binary or unreadable file"})
                continue
            if is_minified(content):
                excluded.append({"path": f["path"], "reason": "Minified file"})
                continue
            ranked.append((f["path"], content, 0.0, count_tokens(content)))
        ranked.sort(key=lambda x: x[0])
        return ranked, excluded

    try:
        scored: List[Tuple[str, str, float, int]] = []
        for f in included_files:
            content = read_file(f["full_path"])
            if content is None:
                excluded.append({"path": f["path"], "reason": "Binary or unreadable file"})
                continue
            if is_minified(content):
                excluded.append({"path": f["path"], "reason": "Minified file"})
                continue

            content_lower = content.lower()
            content_len = len(content_lower)
            if content_len == 0:
                kw_ratio = 0.0
            else:
                matches = sum(content_lower.count(kw) for kw in task_keywords)
                kw_ratio = matches / content_len

            ext_score = get_extension_score(f["path"])
            final = (kw_ratio * 0.6) + ((ext_score / 10.0) * 0.4)

            scored.append((f["path"], content, final, count_tokens(content)))

        scored.sort(key=lambda x: (-x[2], x[0]))
        return scored, excluded
    except Exception as e:
        sys.stderr.write(f"ctxpack: error: ranking failed -- {e}\n")
        sys.exit(1)
