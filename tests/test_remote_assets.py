"""Tests for the remote_assets theme option (issue #100)."""

from __future__ import annotations

import unittest
from typing import Any

import yaml
from jinja2 import ChoiceLoader, DictLoader, Environment, FileSystemLoader
from mkdocs.theme import Theme

from .fixtures import THEME_DIR, mkdocs_config

GOOGLE_FONTS = "fonts.googleapis.com"
FONT_AWESOME = "font-awesome.min.css"
HIGHLIGHTJS = "highlight.min.js"

CHILD_TEMPLATE = (
    '{% extends "base.html" %}'
    '{% block fonts %}<link rel="stylesheet" href="local/fira.css">{% endblock %}'
    '{% block icons %}<link rel="stylesheet" href="local/fa.css">{% endblock %}'
)


def _env() -> Environment:
    env = Environment(
        loader=ChoiceLoader(
            [
                DictLoader({"child.html": CHILD_TEMPLATE}),
                FileSystemLoader(str(THEME_DIR)),
            ]
        ),
        autoescape=True,
    )
    env.filters["url"] = lambda path: path
    return env


def _render(template: str = "base.html", **theme_overrides: Any) -> str:
    config_dict = mkdocs_config()
    theme_config = config_dict["theme"].copy()
    theme_config.update(theme_overrides)
    config_dict["theme"] = type("Theme", (), theme_config)()
    config_dict["hljs_languages"] = theme_config["hljs_languages"]
    config_dict["extra"] = {}
    config_obj = type("Config", (), config_dict)()

    return (
        _env()
        .get_template(template)
        .render(
            config=config_obj,
            page=None,
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )
    )


class RemoteAssetsDefaultTests(unittest.TestCase):
    def test_theme_yml_defaults_to_true(self) -> None:
        config = yaml.safe_load((THEME_DIR / "mkdocs_theme.yml").read_text())
        self.assertIs(config["remote_assets"], True)

    def test_runtime_theme_exposes_default(self) -> None:
        self.assertIs(Theme(name="simple-blog").get("remote_assets"), True)

    def test_unset_option_keeps_remote_assets(self) -> None:
        html = _render()
        self.assertIn(GOOGLE_FONTS, html)
        self.assertIn(FONT_AWESOME, html)


class RemoteAssetsEnabledTests(unittest.TestCase):
    def test_loads_fonts_and_icons(self) -> None:
        html = _render(remote_assets=True)
        self.assertIn(GOOGLE_FONTS, html)
        self.assertIn(FONT_AWESOME, html)

    def test_loads_highlightjs_when_enabled(self) -> None:
        html = _render(remote_assets=True, highlightjs=True)
        self.assertIn(HIGHLIGHTJS, html)
        self.assertIn("hljs.highlightAll()", html)


class RemoteAssetsDisabledTests(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _render(remote_assets=False, highlightjs=True)

    def test_skips_google_fonts(self) -> None:
        self.assertNotIn(GOOGLE_FONTS, self.html)

    def test_skips_font_awesome(self) -> None:
        self.assertNotIn(FONT_AWESOME, self.html)

    def test_skips_highlightjs(self) -> None:
        self.assertNotIn(HIGHLIGHTJS, self.html)
        self.assertNotIn("hljs.highlightAll()", self.html)

    def test_keeps_local_stylesheets(self) -> None:
        self.assertIn("assets/css/bootstrap.min.css", self.html)
        self.assertIn("assets/css/main.min.css", self.html)


SHIELDS = "img.shields.io"


def _render_module(name: str, **theme_overrides: Any) -> str:
    config_dict = mkdocs_config()
    theme_config = config_dict["theme"].copy()
    theme_config.update(theme_overrides)
    config_dict["theme"] = type("Theme", (), theme_config)()
    config_dict["repo_url"] = "https://github.com/owner/repo"
    config_dict["repo_name"] = "owner/repo"
    config_obj = type("Config", (), config_dict)()
    return (
        _env()
        .get_template(f"modules/{name}")
        .render(config=config_obj, nav=[])
    )


class RemoteAssetsModulesTests(unittest.TestCase):
    def test_source_badges_load_by_default(self) -> None:
        self.assertIn(
            SHIELDS, _render_module("source.html", remote_assets=True)
        )

    def test_source_badges_skipped_when_disabled(self) -> None:
        html = _render_module("source.html", remote_assets=False)
        self.assertNotIn(SHIELDS, html)
        self.assertIn("owner/repo", html)

    def test_search_toggle_uses_font_awesome_by_default(self) -> None:
        html = _render_module("header.html", remote_assets=True)
        self.assertIn('class="fa fa-search"', html)
        self.assertNotIn("<svg", html)

    def test_search_toggle_falls_back_to_inline_svg(self) -> None:
        html = _render_module("header.html", remote_assets=False)
        self.assertNotIn('class="fa fa-search"', html)
        self.assertIn("<svg", html)

    def test_search_toggle_has_accessible_label(self) -> None:
        for enabled in (True, False):
            html = _render_module("header.html", remote_assets=enabled)
            self.assertIn('aria-label="Search"', html)


class FontAndIconBlockOverrideTests(unittest.TestCase):
    def setUp(self) -> None:
        self.html = _render("child.html")

    def test_fonts_block_is_overridable(self) -> None:
        self.assertIn("local/fira.css", self.html)
        self.assertNotIn(GOOGLE_FONTS, self.html)

    def test_icons_block_is_overridable(self) -> None:
        self.assertIn("local/fa.css", self.html)
        self.assertNotIn(FONT_AWESOME, self.html)

    def test_override_keeps_rest_of_styles_block(self) -> None:
        self.assertIn("assets/css/bootstrap.min.css", self.html)
        self.assertIn("assets/css/main.min.css", self.html)


if __name__ == "__main__":
    unittest.main()
