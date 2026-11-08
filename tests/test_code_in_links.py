"""Tests for inline code inside links (issue #127)."""

from __future__ import annotations

import unittest

from .fixtures import THEME_DIR

CSS_DIR = THEME_DIR / "assets" / "css"


class CodeInLinksCssTests(unittest.TestCase):
    def setUp(self) -> None:
        self.main_css = (CSS_DIR / "main.min.css").read_text()
        self.bootstrap_css = (CSS_DIR / "bootstrap.min.css").read_text()

    def test_bootstrap_makes_code_inherit_link_color(self) -> None:
        self.assertIn("a>code{color:inherit}", self.bootstrap_css)

    def test_theme_restores_code_foreground_inside_links(self) -> None:
        self.assertIn("a>code{color:var(--code-fg)}", self.main_css)

    def test_code_background_and_foreground_differ(self) -> None:
        root_css = (CSS_DIR / "root.min.css").read_text()
        self.assertIn("--code-bg:var(--primary)", root_css)
        self.assertIn("--code-fg:var(--background)", root_css)


if __name__ == "__main__":
    unittest.main()
