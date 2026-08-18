"""Tests for mkdocs_simple_blog.plugin.filters."""

from __future__ import annotations

import unittest

from mkdocs.structure.files import File

from mkdocs_simple_blog.plugin.filters import FilterPageGenerator

from ..fixtures import fake_config


class FilterPageGeneratorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.generator = FilterPageGenerator()
        self.posts = [
            {"title": "A", "category": "Python", "tags": ["python", "django"]},
            {"title": "B", "category": "Python", "tags": ["python"]},
            {"title": "C", "category": "Guides", "tags": []},
        ]

    def test_group_by_category(self) -> None:
        grouped = self.generator.group(
            self.posts, lambda p: [p["category"]] if p["category"] else []
        )
        self.assertEqual([p["title"] for p in grouped["Python"]], ["A", "B"])
        self.assertEqual([p["title"] for p in grouped["Guides"]], ["C"])

    def test_group_by_tags_fans_out_one_post_to_multiple_groups(self) -> None:
        grouped = self.generator.group(self.posts, lambda p: p["tags"])
        self.assertEqual([p["title"] for p in grouped["python"]], ["A", "B"])
        self.assertEqual([p["title"] for p in grouped["django"]], ["A"])

    def test_generate_creates_one_file_per_group_and_returns_its_url(
        self,
    ) -> None:
        files: list[File] = []
        grouped = {"Python": self.posts[:2], "Guides": self.posts[2:]}
        urls = self.generator.generate(
            files,
            fake_config(),
            grouped,
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertEqual(len(files), 2)
        self.assertEqual(urls["Python"], "category/python/")
        self.assertEqual(urls["Guides"], "category/guides/")

    def test_generate_sets_title_and_filter_meta_in_front_matter(self) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            fake_config(),
            {"Python": self.posts[:2]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        content = files[0]._content
        self.assertIn('title: "Category: Python"', content)
        self.assertIn('blog_category: "Python"', content)
        self.assertIn("blog_list: true", content)

    def test_generate_quotes_names_with_colons_and_double_quotes_safely(
        self,
    ) -> None:
        files: list[File] = []
        tricky_name = 'C++ "Notes": Vol 1'
        self.generator.generate(
            files,
            fake_config(),
            {tricky_name: self.posts[:1]},
            base_dir="tag",
            meta_key="blog_tag",
            label="Tag",
        )
        content = files[0]._content
        self.assertIn('blog_tag: "C++ \\"Notes\\": Vol 1"', content)

    def test_generate_omits_manual_heading_when_title_component_is_enabled(
        self,
    ) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            fake_config(components={"title": True}),
            {"Python": self.posts[:1]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertNotIn("\n# Category: Python\n", files[0]._content)

    def test_generate_includes_manual_heading_when_title_component_is_disabled(
        self,
    ) -> None:
        files: list[File] = []
        self.generator.generate(
            files,
            fake_config(components={"title": False}),
            {"Python": self.posts[:1]},
            base_dir="category",
            meta_key="blog_category",
            label="Category",
        )
        self.assertIn("\n# Category: Python\n", files[0]._content)

    def test_generate_disambiguates_colliding_slugs(self) -> None:
        """Names that normalize to the same slug (e.g. "C++" and "C#" both
        slugify to "c") must not collide on the same src_uri -- otherwise
        MkDocs receives two generated files at the same path and either
        aborts the build or silently drops one group's listing page."""
        files: list[File] = []
        urls = self.generator.generate(
            files,
            fake_config(),
            {"C++": self.posts[:1], "C#": self.posts[1:2]},
            base_dir="tag",
            meta_key="blog_tag",
            label="Tag",
        )
        self.assertEqual(len(files), 2)
        self.assertEqual(
            {f.src_uri for f in files}, {"tag/c.md", "tag/c-1.md"}
        )
        self.assertEqual(len(set(urls.values())), 2)

    def test_generate_escapes_newlines_in_yaml_values(self) -> None:
        """An unescaped newline inside a double-quoted YAML scalar breaks
        the generated front matter and can inject bogus keys."""
        files: list[File] = []
        tricky_name = "Python\nmeta_key: injected"
        self.generator.generate(
            files,
            fake_config(),
            {tricky_name: self.posts[:1]},
            base_dir="tag",
            meta_key="blog_tag",
            label="Tag",
        )
        content = files[0]._content
        self.assertIn('blog_tag: "Python\\nmeta_key: injected"', content)
        self.assertNotIn("\ninjected", content)
