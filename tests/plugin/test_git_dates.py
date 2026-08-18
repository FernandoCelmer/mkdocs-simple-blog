"""Tests for mkdocs_simple_blog.plugin.git_dates."""

from __future__ import annotations

import datetime
import os
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


class GitDatesResolverUtcTimezoneTests(unittest.TestCase):
    """Regression test for a real CI-only failure: with TZ=UTC (the
    default on GitHub Actions runners), git's `%aI` emits a trailing
    "Z" instead of a numeric "+00:00" offset. `datetime.fromisoformat`
    only accepts "Z" from Python 3.11 onward, so on 3.9/3.10 parsing
    silently raised ValueError and every date fell back to the build
    date -- while working fine on any developer machine not set to UTC.
    """

    def setUp(self) -> None:
        self.resolver = GitDatesResolver()
        self.repo_dir = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.repo_dir, ignore_errors=True)

        self._original_tz = os.environ.get("TZ")
        os.environ["TZ"] = "UTC"
        self.addCleanup(self._restore_tz)

        self._run("git", "init", "-q")
        self._run("git", "config", "user.email", "test@example.com")
        self._run("git", "config", "user.name", "Test")

        self.file_path = self.repo_dir / "post.md"
        self.file_path.write_text("content", encoding="utf-8")
        self._run("git", "add", "post.md")
        self._run(
            "git", "commit", "-q", "--date=2024-01-05T10:00:00", "-m", "first"
        )

    def _restore_tz(self) -> None:
        if self._original_tz is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = self._original_tz

    def _run(self, *args: str) -> None:
        subprocess.run(  # noqa: S603
            args,
            cwd=self.repo_dir,
            check=True,
            capture_output=True,
        )

    def test_z_suffixed_author_date_is_parsed_under_utc(self) -> None:
        raw = subprocess.run(  # noqa: S603
            ["git", "log", "-1", "--format=%aI"],
            cwd=self.repo_dir,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
        self.assertTrue(
            raw.endswith("Z"), f"expected a Z-suffixed date, got {raw!r}"
        )
        self.assertEqual(
            self.resolver.created_date(str(self.file_path)),
            "January 5, 2024",
        )
