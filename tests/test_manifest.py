"""Tests for ctxpack.manifest."""

import unittest

from ctxpack.manifest import build_manifest, one_line_summary


class TestBuildManifest(unittest.TestCase):
    def test_schema_keys(self):
        m = build_manifest(1000, 800, [{"path": "a.py", "tokens": 100, "reason": "r"}], [])
        self.assertEqual(set(m.keys()), {"budget", "used", "included", "excluded"})
        self.assertEqual(m["budget"], 1000)
        self.assertEqual(m["used"], 800)
        self.assertEqual(len(m["included"]), 1)
        self.assertEqual(m["excluded"], [])

    def test_excluded_passed_through(self):
        m = build_manifest(100, 50, [], [{"path": "x.lock", "reason": "Lockfile"}])
        self.assertEqual(m["excluded"][0]["path"], "x.lock")
        self.assertEqual(m["excluded"][0]["reason"], "Lockfile")

    def test_truncated_flag_preserved(self):
        inc = [{"path": "a.py", "tokens": 10, "reason": "r", "truncated": True}]
        m = build_manifest(100, 10, inc, [])
        self.assertTrue(m["included"][0]["truncated"])


class TestOneLineSummary(unittest.TestCase):
    def test_format(self):
        s = one_line_summary(3, 800, 1000, 12)
        self.assertEqual(s, "ctxpack: 3 files included (800/1000 tokens), 12 files excluded\n")

    def test_zero(self):
        s = one_line_summary(0, 0, 100, 0)
        self.assertEqual(s, "ctxpack: 0 files included (0/100 tokens), 0 files excluded\n")
