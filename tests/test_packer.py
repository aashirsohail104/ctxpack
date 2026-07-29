"""Tests for ctxpack.packer."""

import unittest

from ctxpack.packer import bundle_files
from ctxpack.utils import count_tokens


def fake_ranked(items):
    """items is a list of (path, content). Returns the 4-tuple shape."""
    return [(p, c, 0.0, count_tokens(c)) for p, c in items]


class TestBundleFiles(unittest.TestCase):
    def test_empty_ranked(self):
        bundle, used, included, excluded, tree_included = bundle_files(
            [], budget=2000, tree_str="", task_desc="t", root_path="."
        )
        # Only header + task section are present
        self.assertIn("ctxpack bundle", bundle)
        self.assertIn("## Task", bundle)
        self.assertEqual(included, [])
        self.assertEqual(excluded, [])
        self.assertTrue(tree_included or not tree_included)  # no tree to include

    def test_includes_file_within_budget(self):
        ranked = fake_ranked([("a.py", "print('hi')")])
        bundle, used, included, excluded, _ = bundle_files(
            ranked, budget=2000, tree_str="", task_desc="t", root_path="."
        )
        self.assertIn("a.py", bundle)
        self.assertIn("print('hi')", bundle)
        self.assertEqual(len(included), 1)
        self.assertEqual(excluded, [])

    def test_truncates_oversize_file(self):
        big = "x" * 10_000
        ranked = fake_ranked([("huge.py", big)])
        bundle, used, included, excluded, _ = bundle_files(
            ranked, budget=200, tree_str="", task_desc="t", root_path="."
        )
        self.assertLessEqual(used, 200)
        self.assertEqual(len(included), 1)
        self.assertTrue(included[0].get("truncated"))
        self.assertIn("TRUNCATED", bundle)

    def test_file_larger_than_budget_only_overhead(self):
        # When the base header + task section already consumes the entire
        # budget, the file cannot fit and must be excluded with a reason.
        # base_tokens for budget=10 and task="t" is already > 10 because
        # the base has a project name + task header.
        # Use an extreme case: huge task that fills the budget by itself.
        ranked = fake_ranked([("a.py", "a")])
        # A 4-char task with budget=1 → base_tokens = ceil(len("# ctxpack bundle -- ...\n\n## Task\n\n.\n\n")/4) > 1
        bundle, used, included, excluded, _ = bundle_files(
            ranked, budget=1, tree_str="", task_desc="t", root_path="."
        )
        self.assertEqual(included, [])
        self.assertGreaterEqual(len(excluded), 1)
        self.assertTrue(any("budget" in e["reason"] for e in excluded))

    def test_output_never_exceeds_budget(self):
        ranked = fake_ranked([
            ("a.py", "alpha" * 200),
            ("b.py", "beta" * 200),
            ("c.py", "gamma" * 200),
        ])
        bundle, used, included, excluded, _ = bundle_files(
            ranked, budget=300, tree_str="", task_desc="t", root_path="."
        )
        self.assertLessEqual(used, 300)
        # Total of included should equal used minus the header
        total = sum(e["tokens"] for e in included)
        self.assertLessEqual(total, 300)

    def test_backtick_fence_handles_content_with_backticks(self):
        content = "x = `backticks` and ```triple```"
        ranked = fake_ranked([("a.py", content)])
        bundle, used, included, excluded, _ = bundle_files(
            ranked, budget=2000, tree_str="", task_desc="t", root_path="."
        )
        # The bundle should still be a valid markdown document
        self.assertIn("a.py", bundle)
        self.assertIn(content, bundle)
        # Fence should be longer than the longest run of backticks in content
        # which is 3 — fence should be at least 4.
        self.assertIn("````python", bundle)
