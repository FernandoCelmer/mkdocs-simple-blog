"""Tests for theme_style and colors interaction (issue #103)."""

from __future__ import annotations

import unittest
from typing import Any

from jinja2 import Environment, FileSystemLoader

from .fixtures import THEME_DIR, mkdocs_config

COLORS = {"text": "blue", "title": "red", "primary": "green", "background": "yellow"}


def _render(**theme_overrides: Any) -> str:
    env = Environment(loader=FileSystemLoader(str(THEME_DIR)), autoescape=True)
    env.filters["url"] = lambda path: path
    config_dict = mkdocs_config()
    theme_config = config_dict["theme"].copy()
    theme_config.update(theme_overrides)
    config_dict["theme"] = type("Theme", (), theme_config)()
    config_dict["extra"] = {}
    config_obj = type("Config", (), config_dict)()
    return env.get_template("base.html").render(
        config=config_obj,
        page=None,
        base_url=".",
        extra_css=[],
        extra_javascript=[],
    )


class ThemeColorsTests(unittest.TestCase):
    def assert_colors_applied(self, html: str) -> None:
        for key, value in COLORS.items():
            self.assertIn(f"--{key}: var(--color-{value});", html)

    def test_colors_apply_with_light_theme_style(self) -> None:
        self.assert_colors_applied(_render(theme_style="light", colors=COLORS))

    def test_colors_apply_without_theme_style(self) -> None:
        self.assert_colors_applied(_render(theme_style=None, colors=COLORS))

    def test_dark_theme_style_keeps_dark_palette(self) -> None:
        html = _render(theme_style="dark", colors=COLORS)
        self.assertIn("--background: black;", html)
        self.assertNotIn("var(--color-", html)

    def test_partial_colors_only_render_given_keys(self) -> None:
        html = _render(theme_style="light", colors={"primary": "green"})
        self.assertIn("--primary: var(--color-green);", html)
        self.assertNotIn("--text: var(--color-", html)

    def test_no_colors_renders_no_overrides(self) -> None:
        html = _render(theme_style="light", colors=None)
        self.assertNotIn("var(--color-", html)


if __name__ == "__main__":
    unittest.main()
