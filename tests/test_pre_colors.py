"""Regression tests for issue #66 — pre/code text color must track theme."""

import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


class TestPreCodeThemeColors(unittest.TestCase):
    """pre/code blocks must track theme colors instead of a fixed gray."""

    def _read(self, relative_path):
        return (ROOT_DIR / relative_path).read_text()

    def test_style_css_uses_code_fg_token(self):
        css = self._read("mkdocs_simple_blog/assets/css/style.min.css")
        self.assertIn("color:var(--code-fg)", css)
        self.assertNotIn("color:#e5e5e5", css)

    def test_tokens_css_defines_code_fg_per_theme(self):
        css = self._read("mkdocs_simple_blog/assets/css/tokens.min.css")
        self.assertIn("code-fg", css)
