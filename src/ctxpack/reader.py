"""UTF-8 file reader and minification detector."""

from typing import Optional


def read_file(full_path: str) -> Optional[str]:
    """Read a file as UTF-8, stripping a BOM.

    Returns ``None`` on decode error or OS error so callers can decide
    whether to skip the file.
    """
    try:
        with open(full_path, "r", encoding="utf-8", errors="strict") as f:
            content = f.read()
            if content.startswith("﻿"):
                content = content[1:]
            return content
    except (OSError, UnicodeDecodeError):
        return None


def is_minified(content: str) -> bool:
    """Heuristic: single-line file larger than 5000 chars with no newlines."""
    return "\n" not in content.rstrip("\n") and len(content) > 5000
