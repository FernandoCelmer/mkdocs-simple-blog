"""Regression tests for issue #68 — custom theme.colors must render."""

import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

THEME_DIR = Path(__file__).parent.parent / "mkdocs_simple_blog"


def _config():
    theme = type(
        "Theme",
        (),
        {
            "favicon": None,
            "theme_style": "",
            "sidebar": True,
            "highlightjs": False,
            "colors": {
                "text": "black",
                "title": "black",
                "primary": "black",
                "background": "white",
            },
            "components": {},
        },
    )()
    return type(
        "Config",
        (),
        {
            "theme": theme,
            "site_name": "Test",
            "site_author": None,
            "extra": {},
        },
    )()


class TestCustomColors(unittest.TestCase):
    """config.theme.colors.* must resolve to real CSS variable values."""

    def setUp(self):
        env = Environment(loader=FileSystemLoader(str(THEME_DIR)))
        env.filters["url"] = lambda p: p  # MkDocs registers this at runtime; stub required here
        self.html = env.get_template("base.html").render(
            config=_config(),
            page=None,
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

    def test_primary_color_resolved(self):
        self.assertIn("--primary: var(--color-black);", self.html)

    def test_text_color_resolved(self):
        self.assertIn("--text: var(--color-black);", self.html)

    def test_title_color_resolved(self):
        self.assertIn("--title: var(--color-black);", self.html)

    def test_background_color_resolved(self):
        self.assertIn("--background: var(--color-white);", self.html)

    def test_no_broken_brace_literal(self):
        self.assertNotIn("{ {", self.html)  # original split-brace artifact from #68
        self.assertNotIn("config.theme.colors", self.html)  # catch unevaluated Jinja refs
