"""Extension-based priority scoring."""

import os

from .constants import EXTENSION_SCORES, FILENAME_SCORES


def get_extension_score(filepath: str) -> int:
    """Return the priority score for ``filepath`` based on its extension.

    Falls back to filename-based scores (``Makefile``, ``Dockerfile``) and
    finally to ``2`` for everything else.
    """
    _, ext = os.path.splitext(filepath)
    if ext:
        return EXTENSION_SCORES.get(ext.lower(), 2)
    basename = os.path.basename(filepath)
    return FILENAME_SCORES.get(basename.lower(), 2)
