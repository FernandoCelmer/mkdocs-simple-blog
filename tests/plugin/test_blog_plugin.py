"""Tests for mkdocs_simple_blog.plugin.BlogPlugin."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from mkdocs.structure.files import File

from mkdocs_simple_blog.plugin import BlogPlugin, BlogPluginConfig

from ..fixtures import fake_config, make_file, write_post


class BlogPluginTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.temp_dir, ignore_errors=True)
        self.plugin = BlogPlugin()
        self.plugin.config = BlogPluginConfig()
        self.plugin.config.load_dict({})

    def _write(
        self, rel_path: str, front_matter: str, body: str = "content"
    ) -> None:
        write_post(self.temp_dir, rel_path, front_matter, body)

    def _file(self, rel_path: str) -> File:
        return make_file(self.temp_dir, rel_path)

    def test_posts_missing_title_or_date_are_excluded(self) -> None:
        self._write("post/no-title.md", "date: 2024-01-01")
        self._write("post/no-date.md", "title: No Date")
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")

        files = [
            self._file("post/no-title.md"),
            self._file("post/no-date.md"),
            self._file("post/valid.md"),
        ]
        self.plugin.on_files(files, config=fake_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "Valid")

    def test_non_post_pages_are_ignored(self) -> None:
        self._write("index.md", "title: Home\ndate: 2024-01-01")
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")

        files = [self._file("index.md"), self._file("post/valid.md")]
        self.plugin.on_files(files, config=fake_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "Valid")

    def test_non_markdown_files_under_posts_dir_are_ignored(self) -> None:
        self._write("post/valid.md", "title: Valid\ndate: 2024-01-01")
        image_path = self.temp_dir / "post" / "cover.png"
        image_path.write_bytes(b"\x89PNG")

        files = [self._file("post/valid.md"), self._file("post/cover.png")]
        self.plugin.on_files(files, config=fake_config())

        self.assertEqual(len(self.plugin.posts), 1)

    def test_posts_sorted_by_date_descending(self) -> None:
        self._write("post/oldest.md", "title: Oldest\ndate: 2022-01-01")
        self._write("post/newest.md", "title: Newest\ndate: 2024-06-01")
        self._write("post/middle.md", "title: Middle\ndate: 2023-03-15")

        files = [
            self._file("post/oldest.md"),
            self._file("post/newest.md"),
            self._file("post/middle.md"),
        ]
        self.plugin.on_files(files, config=fake_config())

        titles = [post["title"] for post in self.plugin.posts]
        self.assertEqual(titles, ["Newest", "Middle", "Oldest"])

    def test_custom_posts_dir(self) -> None:
        self.plugin.config = BlogPluginConfig()
        self.plugin.config.load_dict({"posts_dir": "articles"})

        self._write("articles/a.md", "title: A\ndate: 2024-01-01")
        self._write("post/b.md", "title: B\ndate: 2024-01-01")

        files = [self._file("articles/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=fake_config())

        self.assertEqual(len(self.plugin.posts), 1)
        self.assertEqual(self.plugin.posts[0]["title"], "A")

    def test_category_and_tag_listing_pages_are_generated(self) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ncategory: Python\ntags:\n  - python\n  - django",
        )
        self._write(
            "post/b.md",
            "title: B\ndate: 2024-01-01\ncategory: Python\ntags:\n  - python",
        )

        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=fake_config())

        generated_uris = {
            f.src_uri for f in files if f.src_uri.startswith("categ")
        }
        self.assertIn("category/python.md", generated_uris)

        tag_uris = {f.src_uri for f in files if f.src_uri.startswith("tag/")}
        self.assertEqual(tag_uris, {"tag/python.md", "tag/django.md"})

    def test_blog_categories_and_tags_urls_point_to_generated_pages(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-01-01\ncategory: Python\ntags:\n  - python",
        )

        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=fake_config())

        self.assertEqual(
            self.plugin.blog_categories["Python"], "category/python/"
        )
        self.assertEqual(self.plugin.blog_tags["python"], "tag/python/")

    def test_on_page_context_scopes_blog_posts_to_the_generated_category_page(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ncategory: Python\ntags: []",
        )
        self._write(
            "post/b.md",
            "title: B\ndate: 2024-01-01\ncategory: Guides\ntags: []",
        )
        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=fake_config())

        page = SimpleNamespace(meta={"blog_category": "Python"})
        context = self.plugin.on_page_context(
            {}, page=page, config=fake_config(), nav=None
        )

        self.assertEqual([p["title"] for p in context["blog_posts"]], ["A"])

    def test_on_page_context_scopes_blog_posts_to_the_generated_tag_page(
        self,
    ) -> None:
        self._write(
            "post/a.md",
            "title: A\ndate: 2024-02-01\ntags:\n  - python\n  - django",
        )
        self._write(
            "post/b.md", "title: B\ndate: 2024-01-01\ntags:\n  - django"
        )
        files = [self._file("post/a.md"), self._file("post/b.md")]
        self.plugin.on_files(files, config=fake_config())

        page = SimpleNamespace(meta={"blog_tag": "python"})
        context = self.plugin.on_page_context(
            {}, page=page, config=fake_config(), nav=None
        )

        self.assertEqual([p["title"] for p in context["blog_posts"]], ["A"])

    def test_on_page_context_defaults_to_full_post_list_on_ordinary_pages(
        self,
    ) -> None:
        self._write("post/a.md", "title: A\ndate: 2024-01-01")
        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=fake_config())

        page = SimpleNamespace(meta={})
        context = self.plugin.on_page_context(
            {}, page=page, config=fake_config(), nav=None
        )

        self.assertEqual(context["blog_posts"], self.plugin.posts)

    def test_on_page_context_handles_none_page(self) -> None:
        self._write("post/a.md", "title: A\ndate: 2024-01-01")
        files = [self._file("post/a.md")]
        self.plugin.on_files(files, config=fake_config())

        context = self.plugin.on_page_context(
            {}, page=None, config=fake_config(), nav=None
        )

        self.assertEqual(context["blog_posts"], self.plugin.posts)
