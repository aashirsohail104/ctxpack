"""ctxpack — token-budgeted context bundler for AI coding assistants.

Thin CLI shim that routes to the real package under ``src/ctxpack/``.
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = str(Path(__file__).resolve().parent)
_SRC = str(Path(_ROOT) / "src")

# Strip the root directory from sys.path so import ctxpack finds
# src/ctxpack/ instead of this shim file.
sys.path = [p for p in sys.path if p != _ROOT]
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

from ctxpack.cli import main  # noqa: E402

if __name__ == "__main__":
    sys.exit(main())
