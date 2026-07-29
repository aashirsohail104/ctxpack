"""Pytest discovery shim — lets ``python -m unittest`` work without pytest.

The project uses stdlib ``unittest``. ``tests/conftest.py`` exists so that
``pytest`` (if a developer chooses to run it) does not complain about an
empty conftest. The actual test discovery is done by ``unittest`` via
``tests/__init__.py`` re-exports below.
"""
