"""Shared test helpers.

When tests are discovered from the project root, Python's auto-path
machinery adds the root to ``sys.path``. That makes the file
``./ctxpack.py`` (the CLI shim) the ``ctxpack`` module, which then
fails to expose the real package's submodules. We fix that by removing
the project root from ``sys.path`` and prepending ``src/`` before any
``ctxpack`` import happens.

This module is imported very early by every test file, so the
sys.path correction takes effect for the whole test run.
"""

import os
import shutil
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator


REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES = REPO_ROOT / "tests" / "fixtures" / "repos"
_SRC = REPO_ROOT / "src"

# Project root on sys.path would shadow the package; remove it.
_root_str = str(REPO_ROOT)
sys.path[:] = [p for p in sys.path if os.path.normcase(p) != os.path.normcase(_root_str)]

# Ensure the real package directory comes first.
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))


@contextmanager
def tempdir() -> Iterator[str]:
    """Yield a temp directory that is cleaned up on exit."""
    with tempfile.TemporaryDirectory() as d:
        yield d


def _write(path: Path, content) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(content, str):
        path.write_text(content, encoding="utf-8")
    else:
        path.write_bytes(content)


@contextmanager
def make_repo(files: dict) -> Iterator[str]:
    """Create a temp repo with ``{relpath: content}`` mapping and yield its path."""
    with tempfile.TemporaryDirectory() as d:
        root = Path(d)
        for rel, content in files.items():
            _write(root / rel, content)
        yield d


def run_ctxpack(*args: str) -> tuple[int, str, str]:
    """Invoke ``ctxpack`` as a subprocess and return (rc, stdout, stderr)."""
    env = os.environ.copy()
    # Make the real package importable inside the subprocess without
    # relying on the parent's sys.path.
    existing = env.get("PYTHONPATH", "")
    env["PYTHONPATH"] = (
        str(_SRC) + (os.pathsep + existing if existing else "")
    )
    cmd = [sys.executable, str(REPO_ROOT / "ctxpack.py"), *args]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, encoding="utf-8", timeout=30, env=env
    )
    return proc.returncode, proc.stdout, proc.stderr
