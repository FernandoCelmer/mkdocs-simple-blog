"""Regression tests for issue #66 — pre/code text color must track theme."""

import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent


class TestPreCodeThemeColors(unittest.TestCase):
    """pre/code blocks must track theme colors instead of a fixed gray."""

    def _read(self, relative_path):
        return (ROOT_DIR / relative_path).read_text()

    def test_source_pre_uses_background_variable(self):
        css = self._read("template/assets/css/main.css")
        self.assertIn("color: var(--background);", css)
        self.assertNotIn("color: #e5e5e5;", css)

    def test_shipped_minified_css_uses_background_variable(self):
        css = self._read("mkdocs_simple_blog/assets/css/main.min.css")
        self.assertIn("color:var(--background)", css)
        self.assertNotIn("color:#e5e5e5", css)

    def test_template_minified_css_uses_background_variable(self):
        css = self._read("template/assets/css/main.min.css")
        self.assertIn("color:var(--background)", css)
        self.assertNotIn("color:#e5e5e5", css)
