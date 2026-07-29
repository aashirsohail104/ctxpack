"""Task tokenization."""

from typing import Set

from .constants import STOPWORDS


def parse_task(task_desc: str) -> Set[str]:
    """Tokenize the task description for keyword overlap scoring.

    Lowercases, splits on whitespace, drops tokens shorter than 3 chars
    and the stopword set from :mod:`ctxpack.constants`.
    """
    tokens = task_desc.lower().split()
    return {t for t in tokens if len(t) >= 3 and t not in STOPWORDS}
