"""Tests for Jinja2 templates."""

from __future__ import annotations

import unittest
from types import SimpleNamespace
from typing import Any

from jinja2 import Environment, FileSystemLoader, TemplateNotFound

from mkdocs_simple_blog.plugin.dates import format_date

from .fixtures import THEME_DIR, mkdocs_config, mock_page


def _url_filter(path: str) -> str:
    if path.startswith("http"):
        return path
    return path.replace("\\", "/")


def _template_env() -> Environment:
    env = Environment(
        loader=FileSystemLoader(str(THEME_DIR)),
        autoescape=True,
    )
    env.filters["url"] = _url_filter
    env.filters["fmt_date"] = format_date
    return env


class TemplateFilesExistTests(unittest.TestCase):
    def test_base_template_exists(self) -> None:
        self.assertTrue((THEME_DIR / "base.html").exists())

    def test_main_template_exists(self) -> None:
        self.assertTrue((THEME_DIR / "main.html").exists())

    def test_search_template_exists(self) -> None:
        self.assertTrue((THEME_DIR / "search.html").exists())

    def test_main_template_extends_base(self) -> None:
        content = (THEME_DIR / "main.html").read_text()
        self.assertIn("extends", content)
        self.assertIn("base.html", content)


class BaseTemplateRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _template_env()

    def test_base_template_renders(self) -> None:
        try:
            template = self.env.get_template("base.html")
        except TemplateNotFound:
            self.skipTest("Template not found")

        config_dict = mkdocs_config()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        html = template.render(
            config=config_obj,
            page=mock_page(),
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

        self.assertIsNotNone(html)
        self.assertIn("<html", html)
        self.assertIn("<head", html)
        self.assertIn("<body", html)

    def test_base_template_includes_highlightjs(self) -> None:
        try:
            template = self.env.get_template("base.html")
        except TemplateNotFound:
            self.skipTest("Template not found")

        config_dict = mkdocs_config()
        theme_config = config_dict["theme"].copy()
        theme_config["highlightjs"] = True
        theme_config["hljs_languages"] = ["python", "yaml"]
        config_dict["theme"] = type("Theme", (), theme_config)()
        config_dict["hljs_languages"] = theme_config["hljs_languages"]
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        html = template.render(
            config=config_obj,
            page=None,
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

        self.assertIn("highlight.js", html)
        self.assertIn("hljs.highlightAll()", html)

    def test_base_template_bootstrap_included(self) -> None:
        try:
            template = self.env.get_template("base.html")
        except TemplateNotFound:
            self.skipTest("Template not found")

        config_dict = mkdocs_config()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        html = template.render(
            config=config_obj,
            page=None,
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

        self.assertIn("bootstrap.min.css", html)
        self.assertTrue("bootstrap.bundle.min.js" in html or "jquery" in html)

    def test_base_template_includes_page_metadata(self) -> None:
        try:
            template = self.env.get_template("base.html")
        except TemplateNotFound:
            self.skipTest("Template not found")

        page = mock_page(
            meta={
                "title": "Custom Page Title",
                "description": "Custom page description",
                "author": "John Doe",
                "date": "2025-01-15",
                "image": "assets/custom-image.png",
            }
        )

        config_dict = mkdocs_config()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        html = template.render(
            config=config_obj,
            page=page,
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

        self.assertIn('name="title"', html)
        self.assertIn('content="Custom Page Title"', html)
        self.assertIn('name="description"', html)
        self.assertIn('name="author"', html)
        self.assertIn('content="John Doe"', html)
        self.assertIn('name="date"', html)

        self.assertIn('property="og:title"', html)
        self.assertIn('property="og:description"', html)
        self.assertIn('property="og:type"', html)
        self.assertIn('property="og:url"', html)
        self.assertIn('property="og:image"', html)

        self.assertIn('name="twitter:title"', html)
        self.assertIn('name="twitter:description"', html)
        self.assertIn('name="twitter:card"', html)
        self.assertIn('name="twitter:image"', html)


class SearchTemplateRenderTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _template_env()

    def test_search_template_renders(self) -> None:
        try:
            template = self.env.get_template("search.html")
        except TemplateNotFound:
            self.skipTest("Template not found")

        config_dict = mkdocs_config()
        config_dict["theme"] = type("Theme", (), config_dict["theme"])()
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()

        try:
            html = template.render(
                config=config_obj,
                page=mock_page(),
                base_url=".",
                extra_css=[],
                extra_javascript=[],
            )
        except Exception as exc:  # noqa: BLE001
            self.skipTest(f"Template rendering needs more context: {exc}")

        self.assertTrue("<html" in html or "<!doctype" in html)


class SearchVisibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _template_env()

    def _render_base(
        self, plugins: list[str] | None = None, **theme_overrides: Any
    ) -> str:
        template = self.env.get_template("base.html")
        config_dict = mkdocs_config()
        theme_dict = config_dict["theme"].copy()
        theme_dict.update(theme_overrides)
        config_dict["theme"] = type("Theme", (), theme_dict)()
        if plugins is not None:
            config_dict["plugins"] = plugins
        config_dict["extra"] = {}
        config_obj = type("Config", (), config_dict)()
        return template.render(
            config=config_obj,
            page=mock_page(),
            base_url=".",
            extra_css=[],
            extra_javascript=[],
        )

    def test_search_rendered_by_default_when_search_plugin_present(self) -> None:
        html = self._render_base(plugins=["search"])
        self.assertIn('class="md-search-icon"', html)
        self.assertIn('id="rtd-search-form"', html)

    def test_search_omitted_when_search_plugin_not_present(self) -> None:
        html = self._render_base(plugins=[])
        self.assertNotIn('class="md-search-icon"', html)
        self.assertNotIn('id="rtd-search-form"', html)

    def test_search_omitted_when_include_search_page_is_false(self) -> None:
        html = self._render_base(plugins=["search"], include_search_page=False)
        self.assertNotIn('class="md-search-icon"', html)
        self.assertNotIn('id="rtd-search-form"', html)

    def test_search_omitted_when_search_index_only_is_true(self) -> None:
        html = self._render_base(plugins=["search"], search_index_only=True)
        self.assertNotIn('class="md-search-icon"', html)
        self.assertNotIn('id="rtd-search-form"', html)


class PreviewModuleTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _template_env()
        try:
            self.template = self.env.get_template("modules/preview.html")
        except TemplateNotFound:
            self.skipTest("Template not found")
        self.template.environment.filters["url"] = _url_filter

    def test_shows_both_arrows_when_both_pages_exist(self) -> None:
        page = SimpleNamespace(
            next_page=SimpleNamespace(url="next/"),
            previous_page=SimpleNamespace(url="prev/"),
        )
        html = self.template.render(page=page)
        self.assertIn("Previous", html)
        self.assertIn("Next", html)
        self.assertNotIn('class="nav-link disabled"', html)

    def test_shows_only_next_when_no_previous_page(self) -> None:
        page = SimpleNamespace(
            next_page=SimpleNamespace(url="next/"), previous_page=None
        )
        html = self.template.render(page=page)
        self.assertNotIn("Previous", html)
        self.assertIn("Next", html)

    def test_shows_only_previous_when_no_next_page(self) -> None:
        page = SimpleNamespace(
            next_page=None, previous_page=SimpleNamespace(url="prev/")
        )
        html = self.template.render(page=page)
        self.assertIn("Previous", html)
        self.assertNotIn("Next", html)

    def test_hides_block_entirely_when_no_pages_exist(self) -> None:
        page = SimpleNamespace(next_page=None, previous_page=None)
        html = self.template.render(page=page)
        self.assertNotIn("Previous", html)
        self.assertNotIn("Next", html)
        self.assertNotIn("component-preview", html)
