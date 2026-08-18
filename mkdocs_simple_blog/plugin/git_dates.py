"""Derives a page's creation/revision dates straight from git history,
replacing the need for the mkdocs-git-revision-date-localized-plugin
dependency for the common case.
"""

from __future__ import annotations

import datetime
import os
import subprocess

from .dates import format_date


class GitDatesResolver:
    """Reads a file's first and last commit dates via plain `git log`,
    for pages that don't set `date`/`updated` in front matter.

    Shells out to plain `git` rather than adding an extra dependency
    for this one lookup. Falls back to today's date (the build date)
    when the file has no git history yet, or isn't in a git repository
    at all -- e.g. building from a source tarball.
    """

    def created_date(self, path: str) -> str:
        """Return the formatted date of the file's first commit."""
        return self._formatted_date(path, follow=True, oldest=True)

    def revision_date(self, path: str) -> str:
        """Return the formatted date of the file's last commit."""
        return self._formatted_date(path, follow=False, oldest=False)

    def _formatted_date(self, path: str, *, follow: bool, oldest: bool) -> str:
        command = ["git", "-c", "safe.directory=*", "log", "--format=%aI"]

        if follow:
            command.append("--follow")
        else:
            command.append("-1")
        command += ["--", os.path.basename(path)]

        try:
            result = subprocess.run(  # noqa: S603
                command,
                capture_output=True,
                text=True,
                cwd=os.path.dirname(path),
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            return self._build_date()
        if result.returncode != 0 or not result.stdout.strip():
            return self._build_date()

        lines = result.stdout.strip().splitlines()
        raw_date = lines[-1] if oldest else lines[0]

        try:
            parsed = datetime.datetime.fromisoformat(raw_date)
        except ValueError:
            return self._build_date()
        return format_date(parsed.date())

    def _build_date(self) -> str:
        return format_date(datetime.date.today())
