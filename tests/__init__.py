"""tests/ — unittest suite for ctxpack.

Run from the project root::

    python -m unittest discover -s tests -t .

Or, after ``pip install -e .``::

    python -m unittest discover -s tests

The package import path is corrected at import time so the real
``ctxpack`` package is found regardless of the discover root.
"""

import os
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_SRC = _ROOT / "src"
_root_str = str(_ROOT)
sys.path[:] = [p for p in sys.path if os.path.normcase(p) != os.path.normcase(_root_str)]
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
