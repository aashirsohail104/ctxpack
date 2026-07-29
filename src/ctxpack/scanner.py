"""File-system scanner with noise filtering.

Walks ``root_path`` recursively, applies the noise patterns from
:mod:`ctxpack.constants`, and returns a deterministic (sorted) list of
candidate files plus the paths that were filtered out (with reasons).
"""

import os
from typing import Dict, List, Tuple

from .constants import (
    MAX_FILE_SIZE,
    NOISE_DIRS,
    NOISE_EXTENSIONS,
    NOISE_FILES,
    NOISE_DIR_REASONS,
)


def _get_noise_dir_reason(name: str) -> str:
    return NOISE_DIR_REASONS.get(name, "Build/dependency artifact")


def _get_noise_file_reason(name: str) -> str:
    if name in NOISE_FILES:
        if "lock" in name.lower():
            return "Lockfile -- auto-generated"
        return "IDE/OS metadata file"
    _, ext = os.path.splitext(name)
    if ext.lower() in NOISE_EXTENSIONS:
        ext_lower = ext.lower()
        if ext_lower in (".pyc", ".pyo"):
            return "Python bytecode"
        if ext_lower in (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp", ".ico", ".icns", ".svg"):
            return "Image file"
        if ext_lower in (".mp3", ".mp4", ".avi", ".mov", ".wmv", ".flv", ".mkv", ".webm", ".wav", ".flac", ".ogg", ".m4a"):
            return "Media file"
        if ext_lower in (".zip", ".tar", ".gz", ".bz2", ".xz", ".rar", ".7z", ".zst"):
            return "Archive file"
        if ext_lower in (".exe", ".dll", ".so", ".dylib", ".bin", ".wasm"):
            return "Binary file"
        if ext_lower in (".o", ".obj", ".class", ".jar", ".war"):
            return "Compiled artifact"
        if ext_lower in (".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"):
            return "Document file"
        if ext_lower in (".ttf", ".otf", ".woff", ".woff2", ".eot"):
            return "Font file"
        if ext_lower in (".map",):
            return "Source map"
        return "Binary/artifact file"
    return "Unknown noise file"


def scan_files(root_path: str) -> Tuple[List[Dict], List[Dict]]:
    """Walk ``root_path`` and return (included, excluded) file lists.

    Each entry is a dict with ``path`` (relative) and, for included files,
    ``full_path`` (absolute) and ``size``. Excluded entries have ``path`` and
    ``reason``. Both lists are sorted by path for determinism.
    """
    included: List[Dict] = []
    excluded: List[Dict] = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        rel_dir = os.path.relpath(dirpath, root_path)
        if rel_dir == ".":
            rel_dir = ""

        filtered: List[str] = []
        for d in dirnames:
            if d in NOISE_DIRS:
                excluded.append({
                    "path": os.path.join(rel_dir, d) if rel_dir else d,
                    "reason": _get_noise_dir_reason(d),
                })
            else:
                filtered.append(d)
        dirnames[:] = filtered

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.join(rel_dir, filename) if rel_dir else filename

            if filename in NOISE_FILES or os.path.splitext(filename)[1].lower() in NOISE_EXTENSIONS:
                excluded.append({
                    "path": rel_path,
                    "reason": _get_noise_file_reason(filename),
                })
                continue

            try:
                size = os.path.getsize(full_path)
            except OSError as e:
                excluded.append({"path": rel_path, "reason": f"Unreadable: {e}"})
                continue

            if size > MAX_FILE_SIZE:
                excluded.append({"path": rel_path, "reason": "Large file (>1 MB) -- may be generated"})
                continue

            included.append({"path": rel_path, "full_path": full_path, "size": size})

    included.sort(key=lambda x: x["path"])
    excluded.sort(key=lambda x: x["path"])
    return included, excluded
