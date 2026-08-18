"""Tests for mkdocs_simple_blog.plugin.collector."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from mkdocs_simple_blog.plugin.collector import PostCollector

from ..fixtures import FakeGitAuthorResolver


class PostCollectorTests(unittest.TestCase):
    def _file(self, url: str = "post/a/") -> SimpleNamespace:
        return SimpleNamespace(abs_src_path="/docs/post/a.md", url=url)

    def test_uses_front_matter_author_and_github(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "author": "Fernando Celmer",
                "github": "FernandoCelmer",
            },
            self._file(),
        )
        self.assertEqual(post["author"], "Fernando Celmer")
        self.assertEqual(post["github"], "FernandoCelmer")
        self.assertEqual(
            post["avatar_url"], "https://github.com/FernandoCelmer.png"
        )

    def test_falls_back_to_theme_blog_defaults(self) -> None:
        collector = PostCollector(
            {"author": "Fernando Celmer", "github": "FernandoCelmer"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "Fernando Celmer")
        self.assertEqual(
            post["avatar_url"], "https://github.com/FernandoCelmer.png"
        )

    def test_front_matter_overrides_theme_blog_defaults(self) -> None:
        collector = PostCollector(
            {"author": "Fernando Celmer", "github": "FernandoCelmer"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "author": "Guest Writer",
                "github": "guestwriter",
            },
            self._file(),
        )
        self.assertEqual(post["author"], "Guest Writer")
        self.assertEqual(post["github"], "guestwriter")

    def test_avatar_field_takes_priority_over_github(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "github": "FernandoCelmer",
                "avatar": "https://example.com/me.png",
            },
            self._file(),
        )
        self.assertEqual(post["avatar_url"], "https://example.com/me.png")

    def test_theme_blog_avatar_used_as_fallback(self) -> None:
        collector = PostCollector(
            {"avatar": "https://example.com/default.png"},
            FakeGitAuthorResolver(),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["avatar_url"], "https://example.com/default.png")

    def test_falls_back_to_git_author_when_no_author_anywhere(self) -> None:
        collector = PostCollector(
            {},
            FakeGitAuthorResolver(name="Git Author", email="git@example.com"),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "Git Author")

    def test_git_author_disabled_via_config(self) -> None:
        collector = PostCollector(
            {"git_author": False},
            FakeGitAuthorResolver(name="Git Author", email="git@example.com"),
        )
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["author"], "")

    def test_description_and_image_default_to_empty_string(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["description"], "")
        self.assertEqual(post["image"], "")

    def test_description_and_image_are_collected(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {
                "title": "A",
                "date": "2024-01-01",
                "description": "An excerpt",
                "image": "assets/cover.png",
            },
            self._file(),
        )
        self.assertEqual(post["description"], "An excerpt")
        self.assertEqual(post["image"], "assets/cover.png")

    def test_tags_default_to_empty_list(self) -> None:
        collector = PostCollector({}, FakeGitAuthorResolver())
        post = collector.build(
            {"title": "A", "date": "2024-01-01"}, self._file()
        )
        self.assertEqual(post["tags"], [])

    def test_read_front_matter_parses_yaml_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "post.md"
            path.write_text(
                "---\ntitle: A\ndate: 2024-01-01\n---\n\nbody",
                encoding="utf-8",
            )
            meta = PostCollector.read_front_matter(str(path))
        self.assertEqual(meta["title"], "A")
