"""ctxpack — token-budgeted context bundler for AI coding assistants.

Public entry point. Use ``ctxpack.main()`` to invoke programmatically or
run the script directly.
"""

from .cli import main

__all__ = ["main"]
__version__ = "1.0.0"
