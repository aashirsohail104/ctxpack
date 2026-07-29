"""Tests for ctxpack.utils."""

import math
import unittest

from ctxpack.utils import count_tokens, escape_markdown


class TestCountTokens(unittest.TestCase):
    def test_zero_length(self):
        self.assertEqual(count_tokens(""), 0)

    def test_four_chars_is_one_token(self):
        # ceil(4/4) = 1
        self.assertEqual(count_tokens("abcd"), 1)

    def test_five_chars_is_two_tokens(self):
        # ceil(5/4) = 2
        self.assertEqual(count_tokens("abcde"), 2)

    def test_one_char_is_one_token(self):
        # ceil(1/4) = 1
        self.assertEqual(count_tokens("a"), 1)

    def test_matches_math_ceil(self):
        for n in (0, 1, 3, 4, 5, 7, 8, 9, 16, 17, 100, 1023, 1024, 1025):
            with self.subTest(n=n):
                self.assertEqual(count_tokens("x" * n), math.ceil(n / 4))


class TestEscapeMarkdown(unittest.TestCase):
    def test_escapes_heading_marker(self):
        self.assertEqual(escape_markdown("# H1"), "\\# H1")

    def test_escapes_lt_gt(self):
        self.assertEqual(escape_markdown("a < b > c"), "a \\< b \\> c")

    def test_escapes_all_at_once(self):
        self.assertEqual(escape_markdown("# <x>"), "\\# \\<x\\>")

    def test_no_change_when_safe(self):
        self.assertEqual(escape_markdown("hello world"), "hello world")
