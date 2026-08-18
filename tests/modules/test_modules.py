"""Tests for theme modules."""

from __future__ import annotations

import datetime
import unittest
from types import SimpleNamespace

from jinja2 import Environment, FileSystemLoader
from mkdocs.utils.templates import url_filter

from mkdocs_simple_blog.plugin.dates import format_date

from ..fixtures import THEME_DIR

MODULES_DIR = THEME_DIR / "modules"


class ModulesDirectoryTests(unittest.TestCase):
    def test_modules_directory_exists(self) -> None:
        self.assertTrue(MODULES_DIR.exists())
        self.assertTrue(MODULES_DIR.is_dir())

    def test_required_modules_exist(self) -> None:
        required_modules = [
            "content.html",
            "copyright.html",
            "dropdown-menu.html",
            "footer.html",
            "head_extra_links.html",
            "header.html",
            "menu.html",
            "preview.html",
            "search.html",
            "searchbox.html",
            "sidebar.html",
            "source.html",
        ]
        for module in required_modules:
            with self.subTest(module=module):
                self.assertTrue((MODULES_DIR / module).exists())


class ModuleContentTests(unittest.TestCase):
    EMPTY_MODULES_ALLOWED = {"head_extra_links.html"}

    def test_modules_are_valid_html(self) -> None:
        for module_path in MODULES_DIR.glob("*.html"):
            if module_path.name in self.EMPTY_MODULES_ALLOWED:
                continue
            with self.subTest(module=module_path.name):
                content = module_path.read_text()
                self.assertGreater(len(content), 0)
                self.assertTrue("{" in content or "<" in content)

    def test_header_module_structure(self) -> None:
        content = (MODULES_DIR / "header.html").read_text()
        self.assertTrue(
            "nav" in content.lower() or "navbar" in content.lower()
        )

    def test_footer_module_structure(self) -> None:
        content = (MODULES_DIR / "footer.html").read_text()
        self.assertTrue(
            "footer" in content.lower() or "copyright" in content.lower()
        )

    def test_sidebar_module_structure(self) -> None:
        content = (MODULES_DIR / "sidebar.html").read_text()
        self.assertTrue(
            "nav" in content.lower()
            or "sidebar" in content.lower()
            or "menu" in content.lower()
        )


class ModulesLoadAsTemplatesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(MODULES_DIR)),
            autoescape=True,
        )
        # Modules use MkDocs' `url` filter (registered by mkdocs.theme.Theme
        # at render time) to normalize hrefs -- register it here too,
        # otherwise Jinja fails to compile any module that uses it outside a
        # soft frame (an `if`/conditional expression), e.g. inside a `for` loop.
        self.env.filters["url"] = url_filter
        self.env.filters["fmt_date"] = format_date

    def test_modules_can_be_loaded(self) -> None:
        for module_path in MODULES_DIR.glob("*.html"):
            with self.subTest(module=module_path.name):
                template = self.env.get_template(module_path.name)
                self.assertIsNotNone(template)


class BlogListDateFormattingTests(unittest.TestCase):
    """A post's raw `datetime.date` must render through `fmt_date` in the
    card templates, matching what `content.html` already does for the
    post page itself -- otherwise the list shows "2024-01-01" while the
    post page shows "January 1, 2024" for the same date."""

    def setUp(self) -> None:
        self.env = Environment(
            loader=FileSystemLoader(str(MODULES_DIR)), autoescape=True
        )
        self.env.filters["url"] = lambda path: path
        self.env.filters["fmt_date"] = format_date
        self.post = {
            "title": "A",
            "url": "post/a/",
            "date": datetime.date(2024, 1, 1),
            "category": "",
            "tags": [],
            "author": "",
            "avatar_url": "",
            "description": "",
            "image": "",
        }

    def test_featured_layout_formats_the_date(self) -> None:
        template = self.env.get_template("blog_list_featured.html")
        html = template.render(
            blog_posts=[self.post],
            config=SimpleNamespace(theme=SimpleNamespace(blog=None)),
        )
        self.assertIn("January 1, 2024", html)
        self.assertNotIn("2024-01-01", html)

    def test_compact_layout_formats_the_date(self) -> None:
        template = self.env.get_template("blog_list_compact.html")
        html = template.render(
            blog_posts=[self.post],
            config=SimpleNamespace(theme=SimpleNamespace(blog=None)),
        )
        self.assertIn("January 1, 2024", html)
        self.assertNotIn("2024-01-01", html)
