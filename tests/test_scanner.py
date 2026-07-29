"""Tests for ctxpack.scanner."""

import os
import unittest

from ctxpack.constants import MAX_FILE_SIZE
from ctxpack.scanner import scan_files
from tests._helpers import make_repo


class TestScanFiles(unittest.TestCase):
    def test_empty_repo(self):
        with make_repo({}) as root:
            included, excluded = scan_files(root)
        self.assertEqual(included, [])
        self.assertEqual(excluded, [])

    def test_picks_up_text_file(self):
        files = {"hello.py": "print('hi')"}
        with make_repo(files) as root:
            included, excluded = scan_files(root)
        self.assertEqual(len(included), 1)
        self.assertEqual(included[0]["path"], "hello.py")
        self.assertEqual(excluded, [])

    def test_filters_git_directory(self):
        files = {".git/HEAD": "ref: refs/heads/main", "main.py": "x = 1"}
        with make_repo(files) as root:
            included, excluded = scan_files(root)
        self.assertEqual([f["path"] for f in included], ["main.py"])
        self.assertTrue(any("Version control" in e["reason"] for e in excluded))

    def test_filters_node_modules(self):
        files = {"node_modules/x/index.js": "x", "src/a.js": "x"}
        with make_repo(files) as root:
            included, excluded = scan_files(root)
        # Windows uses backslashes, POSIX uses forward slashes — compare
        # with os.path.join normalization.
        self.assertEqual(
            [f["path"] for f in included],
            [os.path.join("src", "a.js")],
        )

    def test_filters_lockfile(self):
        files = {"package-lock.json": "{}", "index.js": "x"}
        with make_repo(files) as root:
            included, excluded = scan_files(root)
        self.assertEqual([f["path"] for f in included], ["index.js"])
        self.assertTrue(any("Lockfile" in e["reason"] for e in excluded))

    def test_filters_binary_extension(self):
        files = {"image.png": b"\x89PNG".decode("latin-1"), "main.py": "x"}
        # We need to write a real binary file
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n")
            (Path(d) / "main.py").write_text("x", encoding="utf-8")
            included, excluded = scan_files(d)
        self.assertEqual([f["path"] for f in included], ["main.py"])
        self.assertTrue(any("Image" in e["reason"] for e in excluded))

    def test_filters_oversize(self):
        big = "x" * (MAX_FILE_SIZE + 1)
        with make_repo({"big.txt": big, "small.txt": "ok"}) as root:
            included, excluded = scan_files(root)
        self.assertEqual([f["path"] for f in included], ["small.txt"])
        self.assertTrue(any("Large" in e["reason"] for e in excluded))

    def test_deterministic_order(self):
        files = {"z.txt": "1", "a.txt": "2", "m.txt": "3"}
        with make_repo(files) as root:
            included, _ = scan_files(root)
        self.assertEqual([f["path"] for f in included], ["a.txt", "m.txt", "z.txt"])

    def test_nested_paths(self):
        files = {"a/b/c.py": "x", "a/b/d.py": "x"}
        with make_repo(files) as root:
            included, _ = scan_files(root)
        paths = sorted(f["path"] for f in included)
        # Use os.path.join to remain portable across Windows / POSIX.
        self.assertEqual(paths, [os.path.join("a", "b", "c.py"), os.path.join("a", "b", "d.py")])
