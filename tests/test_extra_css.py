"""Regression tests for issue #66 — extra_css cascade order in base.html."""

import unittest
from pathlib import Path

from jinja2 import Environment, FileSystemLoader

THEME_DIR = Path(__file__).parent.parent / "mkdocs_simple_blog"


def _config(theme_style="dark"):
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


class TestExtraCssCascade(unittest.TestCase):
    """extra_css must be able to override the theme color variables."""

    def setUp(self):
        env = Environment(loader=FileSystemLoader(str(THEME_DIR)))
        env.filters["url"] = lambda p: p
        self.template = env.get_template("base.html")

    def _render(self, theme_style="dark"):
        return self.template.render(
            config=_config(theme_style),
            page=None,
            base_url=".",
            extra_css=["assets/custom.css"],
            extra_javascript=[],
        )

    def test_extra_css_link_present(self):
        html = self._render()
        self.assertIn('<link href="assets/custom.css" rel="stylesheet">', html)

    def test_extra_css_loads_after_theme_stylesheets(self):
        html = self._render(theme_style="dark")
        self.assertIn(
            'href="assets/css/root.min.css"',
            html,
            "root.min.css link not found in rendered HTML",
        )
        self.assertIn(
            'href="assets/custom.css"',
            html,
            "extra_css link not found in rendered HTML",
        )
        root_css_pos = html.index('href="assets/css/root.min.css"')
        extra_css_pos = html.index('href="assets/custom.css"')
        self.assertLess(
            root_css_pos,
            extra_css_pos,
            "extra_css must load after root.min.css so it can override "
            "CSS variables",
        )
