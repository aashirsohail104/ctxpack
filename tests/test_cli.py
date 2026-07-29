"""End-to-end CLI tests using subprocess."""

import json
import os
import sys
import unittest
from pathlib import Path

from tests._helpers import REPO_ROOT, make_repo, run_ctxpack


class TestCLIExitCodes(unittest.TestCase):
    def test_help(self):
        rc, _, _ = run_ctxpack("--help")
        self.assertEqual(rc, 0)

    def test_missing_path_exits_2(self):
        rc, _, err = run_ctxpack("--task", "t", "--budget", "1000", "--path", "/no/such/dir")
        self.assertEqual(rc, 2)
        self.assertIn("Path not found", err)

    def test_missing_task_exits_1(self):
        rc, _, err = run_ctxpack("--path", ".", "--budget", "1000")
        self.assertEqual(rc, 1)

    def test_missing_budget_exits_1(self):
        rc, _, err = run_ctxpack("--path", ".", "--task", "t")
        self.assertEqual(rc, 1)

    def test_budget_zero_exits_1(self):
        rc, _, err = run_ctxpack("--path", ".", "--task", "t", "--budget", "0")
        self.assertEqual(rc, 1)
        self.assertIn("positive integer", err)

    def test_budget_non_integer_exits_1(self):
        rc, _, err = run_ctxpack("--path", ".", "--task", "t", "--budget", "abc")
        self.assertEqual(rc, 1)
        self.assertIn("must be an integer", err)

    def test_negative_budget_exits_1(self):
        rc, _, err = run_ctxpack("--path", ".", "--task", "t", "--budget", "-1")
        self.assertEqual(rc, 1)

    def test_path_is_file_exits_2(self):
        rc, _, err = run_ctxpack(
            "--path", str(REPO_ROOT / "ctxpack.py"), "--task", "t", "--budget", "1000"
        )
        self.assertEqual(rc, 2)
        self.assertIn("not a directory", err)


class TestCLISuccess(unittest.TestCase):
    def test_basic_run(self):
        with make_repo({"main.py": "print('hello')"}) as root:
            rc, out, err = run_ctxpack(
                "--path", root, "--task", "hello world", "--budget", "4000"
            )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")
        self.assertIn("ctxpack bundle", out)
        self.assertIn("## Task", out)
        self.assertIn("main.py", out)
        # One-line summary on stderr
        self.assertIn("files included", err)

    def test_writes_to_out_file(self):
        with make_repo({"main.py": "x"}) as root:
            out_file = os.path.join(root, "bundle.md")
            rc, _, _ = run_ctxpack(
                "--path", root, "--task", "t", "--budget", "2000", "--out", out_file
            )
        self.assertEqual(rc, 0)
        self.assertTrue(os.path.exists(out_file))
        with open(out_file, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("ctxpack bundle", content)

    def test_writes_manifest(self):
        with make_repo({"main.py": "x"}) as root:
            manifest = os.path.join(root, "manifest.json")
            rc, _, _ = run_ctxpack(
                "--path", root, "--task", "t", "--budget", "2000", "--manifest", manifest
            )
        self.assertEqual(rc, 0)
        with open(manifest, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(set(data.keys()), {"budget", "used", "included", "excluded"})
        self.assertEqual(data["budget"], 2000)

    def test_manifest_excludes_match(self):
        with make_repo({"a.py": "x", ".gitignore": "*.log"}) as root:
            manifest = os.path.join(root, "manifest.json")
            rc, _, _ = run_ctxpack(
                "--path", root, "--task", "t", "--budget", "2000", "--manifest", manifest
            )
        with open(manifest, encoding="utf-8") as f:
            data = json.load(f)
        paths = {e["path"] for e in data["excluded"]}
        self.assertIn(".gitignore", paths)


class TestCLIDeterminism(unittest.TestCase):
    def test_repeat_runs_byte_identical(self):
        with make_repo({"a.py": "alpha\n", "b.py": "beta\n"}) as root:
            a_path = os.path.join(root, "a.md")
            b_path = os.path.join(root, "b.md")
            rc1, _, _ = run_ctxpack(
                "--path", root, "--task", "alpha beta", "--budget", "2000", "--out", a_path
            )
            rc2, _, _ = run_ctxpack(
                "--path", root, "--task", "alpha beta", "--budget", "2000", "--out", b_path
            )
        self.assertEqual(rc1, 0)
        self.assertEqual(rc2, 0)
        with open(a_path, "rb") as f:
            a_bytes = f.read()
        with open(b_path, "rb") as f:
            b_bytes = f.read()
        self.assertEqual(a_bytes, b_bytes, "Bundle output must be byte-identical across runs")


class TestCLIFixtureRepos(unittest.TestCase):
    """Run the CLI against the curated fixture repos in tests/fixtures/repos/."""

    FIXTURES = REPO_ROOT / "tests" / "fixtures" / "repos"

    def test_empty_repo(self):
        rc, _, err = run_ctxpack(
            "--path", str(self.FIXTURES / "empty_repo"),
            "--task", "t", "--budget", "1000",
        )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")

    def test_single_file_repo(self):
        rc, out, err = run_ctxpack(
            "--path", str(self.FIXTURES / "single_file_repo"),
            "--task", "main", "--budget", "2000",
        )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")
        self.assertIn("main.py", out)

    def test_only_markdown_repo(self):
        rc, out, err = run_ctxpack(
            "--path", str(self.FIXTURES / "only_markdown"),
            "--task", "documentation", "--budget", "2000",
        )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")
        self.assertIn("readme.md", out)

    def test_unicode_repo(self):
        rc, out, err = run_ctxpack(
            "--path", str(self.FIXTURES / "unicode_repo"),
            "--task", "agent", "--budget", "4000",
        )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")
        # Chinese filename should be preserved
        self.assertIn("中文", out)

    def test_binary_repo(self):
        rc, _, err = run_ctxpack(
            "--path", str(self.FIXTURES / "binary_repo"),
            "--task", "t", "--budget", "2000",
            "--manifest", str(self.FIXTURES / "binary_repo" / "manifest.json"),
        )
        self.assertEqual(rc, 0, msg=f"stderr={err!r}")
        with open(self.FIXTURES / "binary_repo" / "manifest.json", encoding="utf-8") as f:
            data = json.load(f)
        # The png should be excluded
        excluded_paths = {e["path"] for e in data["excluded"]}
        self.assertIn("image.png", excluded_paths)
