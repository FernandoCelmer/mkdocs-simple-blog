"""Derives a post's author name and avatar straight from git history."""

from __future__ import annotations

import os
import re
import subprocess


class GitAuthorResolver:
    """Derives a post's author name and avatar straight from git history,
    for posts whose front matter doesn't set `author`/`avatar`/`github`.

    Avatar detection recognizes GitHub, GitLab and Bitbucket no-reply
    commit emails and builds that provider's avatar-by-username URL
    directly -- no API call, no extra dependency. Shells out to plain
    `git` rather than adding a GitPython dependency for this one lookup.
    """

    _PROVIDER_NOREPLY_PATTERNS = [
        (
            re.compile(
                r"^(?:\d+\+)?([^@]+)@users\.noreply\.github\.com$",
                re.IGNORECASE,
            ),
            "https://github.com/{username}.png",
        ),
        (
            re.compile(
                r"^([^@]+)@users\.noreply\.gitlab\.com$", re.IGNORECASE
            ),
            "https://gitlab.com/{username}.png",
        ),
        (
            re.compile(
                r"^(?:[^@]+\+)?([^@]+)@users\.noreply\.bitbucket\.org$",
                re.IGNORECASE,
            ),
            "https://bitbucket.org/{username}/avatar/",
        ),
    ]

    def author_and_email(self, path: str) -> tuple[str, str]:
        """Return (name, email) of the file's last git commit author.

        Falls back to ("", "") if the file has no git history yet, or
        the project isn't a git repository at all (e.g. building from a
        source tarball).
        """
        try:
            result = subprocess.run(  # noqa: S603
                ["git", "log", "-1", "--format=%an\x1f%ae", "--", path],  # noqa: S607
                capture_output=True,
                text=True,
                cwd=os.path.dirname(path),
                timeout=5,
            )
        except (OSError, subprocess.SubprocessError):
            return "", ""
        if result.returncode != 0 or not result.stdout.strip():
            return "", ""
        name, _, email = result.stdout.strip().partition("\x1f")
        return name, email

    def avatar_from_email(self, email: str) -> str:
        """Match a known git-hosting no-reply email and build that
        provider's avatar URL. Returns "" for anything else (a personal
        email, a self-hosted GitLab/Bitbucket instance, ...) -- use the
        `avatar` front matter field directly in that case.
        """
        if not email:
            return ""
        email = email.strip()
        for pattern, template in self._PROVIDER_NOREPLY_PATTERNS:
            match = pattern.match(email)
            if match:
                return template.format(username=match.group(1))
        return ""
