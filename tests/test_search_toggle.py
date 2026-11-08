"""Tests for when the header search is rendered (issue #112)."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

TOGGLE = 'href="#collapseExample"'
SEARCHBOX = 'id="collapseExample"'


def _build(config: dict) -> Path:
    root = Path(tempfile.mkdtemp())
    (root / "docs").mkdir()
    (root / "docs" / "index.md").write_text("# Home\n", encoding="utf-8")
    full = {"site_name": "Test", **config}
    full["theme"] = {"name": "simple-blog", **config.get("theme", {})}
    (root / "mkdocs.yml").write_text(yaml.safe_dump(full), encoding="utf-8")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
        cwd=root,
        check=True,
    )
    return root / "site"


class SearchToggleTests(unittest.TestCase):
    def test_default_renders_toggle_and_searchbox(self) -> None:
        site = _build({})
        html = (site / "index.html").read_text()
        self.assertIn(TOGGLE, html)
        self.assertIn(SEARCHBOX, html)
        self.assertTrue((site / "search.html").exists())

    def test_without_search_plugin_hides_toggle(self) -> None:
        html = (_build({"plugins": []}) / "index.html").read_text()
        self.assertNotIn(TOGGLE, html)
        self.assertNotIn(SEARCHBOX, html)

    def test_without_search_page_hides_toggle(self) -> None:
        site = _build({"theme": {"include_search_page": False}})
        html = (site / "index.html").read_text()
        self.assertFalse((site / "search.html").exists())
        self.assertNotIn(TOGGLE, html)
        self.assertNotIn(SEARCHBOX, html)


if __name__ == "__main__":
    unittest.main()
