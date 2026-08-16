"""Regression tests for issue #66 — pre/code colors must track theme."""

import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

ROOT_DIR = Path(__file__).parent.parent
THEME_DIR = ROOT_DIR / "mkdocs_simple_blog"


def _config(theme_style="dark", extra_css_theme=None):
    theme = type(
        "Theme",
        (),
        {
            "favicon": None,
            "theme_style": theme_style,
            "sidebar": True,
            "highlightjs": False,
            "colors": {"primary": "black"},
            "components": {},
            "extra_css": extra_css_theme or [],
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


class TestPreCodeThemeColors(unittest.TestCase):
    """pre/code blocks must use dedicated code surface variables."""

    def _read(self, relative_path):
        return (ROOT_DIR / relative_path).read_text()

    def test_style_css_uses_code_fg_token(self):
        css = self._read("mkdocs_simple_blog/assets/css/style.min.css")
        self.assertIn("color:var(--code-fg)", css)
        self.assertNotIn("color:#e5e5e5", css)

    def test_tokens_css_defines_code_fg_per_theme(self):
        css = self._read("mkdocs_simple_blog/assets/css/tokens.min.css")
        self.assertIn("code-fg", css)
        self.assertIn("code-bg", css)


class TestDarkThemeCodeBlocks(unittest.TestCase):
    """Dark theme must keep code blocks on a dark surface (issue #66 follow-up)."""

    def setUp(self):
        env = Environment(loader=FileSystemLoader(str(THEME_DIR)))
        env.filters["url"] = lambda p: p
        self.template = env.get_template("base.html")

    def _render(
        self, theme_style="dark", theme_extra_css=None, extra_css=None
    ):
        return self.template.render(
            config=_config(theme_style, extra_css_theme=theme_extra_css),
            page=None,
            base_url=".",
            extra_css=extra_css or [],
            extra_javascript=[],
        )

    def test_dark_theme_sets_code_surface_variables(self):
        html = self._render(theme_style="dark")
        self.assertIn("--code-bg:", html)
        self.assertIn("--code-fg:", html)
        # Dark code surface, not inverted page colors
        self.assertIn("--code-bg: #1a1a1a;", html)
        self.assertIn("--code-fg: #f5f5f5;", html)

    def test_light_theme_does_not_force_dark_code_vars(self):
        html = self._render(theme_style="light")
        self.assertNotIn("--code-bg: #1a1a1a;", html)

    def test_theme_nested_extra_css_is_linked(self):
        """Users often put extra_css under theme; accept as alias of top-level."""
        html = self._render(
            theme_style="dark",
            theme_extra_css=["assets/style.css"],
            extra_css=[],
        )
        self.assertIn('href="assets/style.css"', html)

    def test_top_level_extra_css_still_works(self):
        html = self._render(
            theme_style="dark",
            extra_css=["assets/custom.css"],
        )
        self.assertIn('href="assets/custom.css"', html)
        tokens_pos = html.index('href="assets/css/tokens.min.css"')
        extra_pos = html.index('href="assets/custom.css"')
        self.assertLess(tokens_pos, extra_pos)
