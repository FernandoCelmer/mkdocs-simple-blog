"""Tests for mkdocs_simple_blog.plugin.slug."""

from __future__ import annotations

import unittest

from mkdocs_simple_blog.plugin.slug import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercases_and_hyphenates_spaces(self) -> None:
        self.assertEqual(slugify("Python Guides"), "python-guides")

    def test_collapses_underscores_and_spaces_into_single_hyphen(self) -> None:
        self.assertEqual(slugify("a__b  c"), "a-b-c")

    def test_strips_punctuation(self) -> None:
        self.assertEqual(slugify('C++ "Notes": Vol 1'), "c-notes-vol-1")

    def test_strips_leading_and_trailing_whitespace(self) -> None:
        self.assertEqual(slugify("  Django  "), "django")

    def test_empty_string_returns_empty_string(self) -> None:
        self.assertEqual(slugify(""), "")
