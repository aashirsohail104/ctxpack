"""Tests for ctxpack.tokenize."""

import unittest

from ctxpack.tokenize import parse_task


class TestParseTask(unittest.TestCase):
    def test_lowercases(self):
        self.assertEqual(parse_task("FOO Bar"), {"foo", "bar"})

    def test_drops_short_tokens(self):
        self.assertEqual(parse_task("a be cat"), {"cat"})

    def test_drops_stopwords(self):
        self.assertEqual(parse_task("the quick brown fox"), {"quick", "brown", "fox"})

    def test_empty(self):
        self.assertEqual(parse_task(""), set())

    def test_only_stopwords(self):
        self.assertEqual(parse_task("the and or but"), set())

    def test_preserves_punctuation_attached(self):
        # Tokenization is whitespace-split, so punctuation is part of the token.
        # This matches the spec's behavior.
        self.assertEqual(parse_task("bug, fix!"), {"bug,", "fix!"})
