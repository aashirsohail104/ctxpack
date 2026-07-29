"""Tests for ctxpack.ranker."""

import unittest

from ctxpack.extension import get_extension_score
from ctxpack.ranker import rank_files
from tests._helpers import make_repo


class TestGetExtensionScore(unittest.TestCase):
    def test_python_scores_10(self):
        self.assertEqual(get_extension_score("a.py"), 10)

    def test_markdown_scores_7(self):
        self.assertEqual(get_extension_score("a.md"), 7)

    def test_json_scores_3(self):
        self.assertEqual(get_extension_score("a.json"), 3)

    def test_unknown_scores_2(self):
        self.assertEqual(get_extension_score("a.weird"), 2)

    def test_makefile_filename(self):
        self.assertEqual(get_extension_score("Makefile"), 6)


class TestRankFiles(unittest.TestCase):
    def test_no_keywords_sorts_by_path(self):
        files = {"z.py": "z content", "a.py": "a content"}
        with make_repo(files) as root:
            included, _ = scan_helper(root)
            ranked, excluded = rank_files(included, set())
        self.assertEqual([r[0] for r in ranked], ["a.py", "z.py"])
        self.assertEqual(excluded, [])

    def test_keyword_overlap_increases_score(self):
        files = {
            "agent.py": "agent runs a task and the task runs the agent again",
            "config.json": "{}",
        }
        with make_repo(files) as root:
            included, _ = scan_helper(root)
            ranked, _ = rank_files(included, {"agent", "task"})
        # agent.py should rank first
        self.assertEqual(ranked[0][0], "agent.py")

    def test_unreadable_file_excluded(self):
        # Build a repo with a file that has invalid UTF-8 bytes
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "binary.py").write_bytes(b"\xff\xfe\x00bad")
            (Path(d) / "good.py").write_text("ok", encoding="utf-8")
            included, _ = scan_helper(d)
            ranked, excluded = rank_files(included, set())
        paths = [r[0] for r in ranked]
        self.assertEqual(paths, ["good.py"])
        self.assertTrue(any("Binary" in e["reason"] for e in excluded))


def scan_helper(root: str):
    from ctxpack.scanner import scan_files
    return scan_files(root)
