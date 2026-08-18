"""Regression tests for issue #92 -- page-dates divider duplicating
blog_list's own first-item border on pages with no body content.
"""

from __future__ import annotations

import unittest
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader

from mkdocs_simple_blog.plugin.dates import format_date

from .fixtures import THEME_DIR


def _url_filter(path: str) -> str:
    return path


def _template_env() -> Environment:
    env = Environment(loader=FileSystemLoader(str(THEME_DIR)), autoescape=True)
    env.filters["url"] = _url_filter
    env.filters["fmt_date"] = format_date
    return env


class PageDatesDividerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = _template_env()
        self.template = self.env.get_template("modules/content.html")

    def _render(self, content: str) -> str:
        config = SimpleNamespace(theme=SimpleNamespace(components=None))
        page = SimpleNamespace(
            title="Blog",
            content=content,
            meta={"date": "2024-01-05"},
            file=None,
        )
        return self.template.render(config=config, page=page)

    def test_no_divider_when_page_has_no_body_content(self) -> None:
        html = self._render("")
        self.assertIn("page-dates", html)
        self.assertNotIn("page-dates-divider", html)

    def test_divider_present_when_page_has_body_content(self) -> None:
        html = self._render("<p>Some real body text.</p>")
        self.assertIn("page-dates-divider", html)
