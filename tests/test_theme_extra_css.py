"""Tests for the theme.extra_css alias (issue #106)."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml


def _stylesheets(html: str) -> list[str]:
    return re.findall(r'<link href="([^"]+)" rel="stylesheet">', html)


class ThemeExtraCssTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(tempfile.mkdtemp())
        docs = root / "docs"
        (docs / "sub").mkdir(parents=True)
        (docs / "index.md").write_text("# Home\n", encoding="utf-8")
        (docs / "sub" / "page.md").write_text("# Page\n", encoding="utf-8")
        (docs / "theme.css").write_text("body{}", encoding="utf-8")
        (docs / "top.css").write_text("body{}", encoding="utf-8")
        config = {
            "site_name": "Test",
            "extra_css": ["top.css"],
            "theme": {
                "name": "simple-blog",
                "extra_css": [
                    "theme.css",
                    "top.css",
                    "https://cdn.example.com/x.css",
                ],
            },
        }
        (root / "mkdocs.yml").write_text(
            yaml.safe_dump(config), encoding="utf-8"
        )
        subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
            cwd=root,
            check=True,
        )
        cls.site = root / "site"

    def test_alias_paths_resolve_on_home_page(self) -> None:
        css = _stylesheets((self.site / "index.html").read_text())
        self.assertIn("theme.css", css)

    def test_alias_paths_resolve_on_nested_page(self) -> None:
        css = _stylesheets(
            (self.site / "sub" / "page" / "index.html").read_text()
        )
        self.assertIn("../../theme.css", css)
        self.assertNotIn("theme.css", css)

    def test_alias_does_not_duplicate_top_level_entry(self) -> None:
        css = _stylesheets(
            (self.site / "sub" / "page" / "index.html").read_text()
        )
        self.assertEqual(css.count("../../top.css"), 1)
        self.assertNotIn("top.css", css)

    def test_absolute_urls_are_kept(self) -> None:
        css = _stylesheets(
            (self.site / "sub" / "page" / "index.html").read_text()
        )
        self.assertIn("https://cdn.example.com/x.css", css)


if __name__ == "__main__":
    unittest.main()
