"""Tests for mkdocs_simple_blog.plugin.git_dates."""

from __future__ import annotations

import datetime
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from mkdocs_simple_blog.plugin.dates import format_date
from mkdocs_simple_blog.plugin.git_dates import GitDatesResolver

TODAY = format_date(datetime.date.today())


class GitDatesResolverOutsideRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = GitDatesResolver()

    def test_created_date_outside_git_repo_falls_back_to_build_date(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "untracked.md")
            Path(path).write_text("content", encoding="utf-8")
            self.assertEqual(self.resolver.created_date(path), TODAY)

    def test_revision_date_outside_git_repo_falls_back_to_build_date(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = str(Path(tmp) / "untracked.md")
            Path(path).write_text("content", encoding="utf-8")
            self.assertEqual(self.resolver.revision_date(path), TODAY)


class GitDatesResolverInRepoTests(unittest.TestCase):
    def setUp(self) -> None:
        self.resolver = GitDatesResolver()
        self.repo_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.repo_dir, ignore_errors=True)
        self._run("git", "init", "-q")
        self._run("git", "config", "user.email", "test@example.com")
        self._run("git", "config", "user.name", "Test")

        self.file_path = self.repo_dir / "post.md"
        self.file_path.write_text("first version", encoding="utf-8")
        self._run("git", "add", "post.md")
        self._run(
            "git",
            "commit",
            "-q",
            "--date=2024-01-05T10:00:00",
            "-m",
            "first",
        )

        self.file_path.write_text("second version", encoding="utf-8")
        self._run("git", "add", "post.md")
        self._run(
            "git",
            "commit",
            "-q",
            "--date=2024-06-15T10:00:00",
            "-m",
            "second",
        )

    def _run(self, *args: str) -> None:
        subprocess.run(  # noqa: S603
            args,
            cwd=self.repo_dir,
            check=True,
            capture_output=True,
        )

    def test_created_date_returns_first_commit_date(self) -> None:
        self.assertEqual(
            self.resolver.created_date(str(self.file_path)), "January 5, 2024"
        )

    def test_revision_date_returns_last_commit_date(self) -> None:
        self.assertEqual(
            self.resolver.revision_date(str(self.file_path)), "June 15, 2024"
        )

    def test_untracked_file_in_repo_falls_back_to_build_date(self) -> None:
        untracked = self.repo_dir / "untracked.md"
        untracked.write_text("content", encoding="utf-8")
        self.assertEqual(self.resolver.created_date(str(untracked)), TODAY)
        self.assertEqual(self.resolver.revision_date(str(untracked)), TODAY)

    def test_created_date_honors_locale(self) -> None:
        from mkdocs_simple_blog.plugin import dates

        if not dates._HAS_BABEL:
            self.skipTest("babel not installed")
        self.assertEqual(
            self.resolver.created_date(str(self.file_path), locale="pt"),
            "5 de janeiro de 2024",
        )
