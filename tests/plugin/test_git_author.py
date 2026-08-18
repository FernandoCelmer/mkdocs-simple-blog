"""Tests for mkdocs_simple_blog.plugin.git_author."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from mkdocs_simple_blog.plugin.git_author import GitAuthorResolver


class GitAuthorResolverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = GitAuthorResolver()

    def test_avatar_from_email_github_with_numeric_id_prefix(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "123456+FernandoCelmer@users.noreply.github.com"
        )
        self.assertEqual(avatar, "https://github.com/FernandoCelmer.png")

    def test_avatar_from_email_github_without_id_prefix(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "FernandoCelmer@users.noreply.github.com"
        )
        self.assertEqual(avatar, "https://github.com/FernandoCelmer.png")

    def test_avatar_from_email_gitlab(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "fernandocelmer@users.noreply.gitlab.com"
        )
        self.assertEqual(avatar, "https://gitlab.com/fernandocelmer.png")

    def test_avatar_from_email_bitbucket(self) -> None:
        avatar = self.resolver.avatar_from_email(
            "abc123+fernandocelmer@users.noreply.bitbucket.org"
        )
        self.assertEqual(
            avatar, "https://bitbucket.org/fernandocelmer/avatar/"
        )

    def test_avatar_from_email_unrecognized_domain_returns_empty(self) -> None:
        self.assertEqual(
            self.resolver.avatar_from_email("someone@example.com"), ""
        )

    def test_avatar_from_email_empty_returns_empty(self) -> None:
        self.assertEqual(self.resolver.avatar_from_email(""), "")

    def test_author_and_email_outside_git_repo_returns_empty(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "untracked.md")
            Path(path).write_text("content", encoding="utf-8")
            name, email = self.resolver.author_and_email(path)
        self.assertEqual((name, email), ("", ""))
