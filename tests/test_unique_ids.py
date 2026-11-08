"""Tests for unique element ids in rendered pages (issue #108)."""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import yaml


def _build(theme: dict) -> Path:
    root = Path(tempfile.mkdtemp())
    docs = root / "docs"
    docs.mkdir()
    (docs / "index.md").write_text("# Home\n\n## Section\n", encoding="utf-8")
    (docs / "page.md").write_text(
        "---\nblog_sidebar:\n  tags: true\n---\n# Page\n", encoding="utf-8"
    )
    config = {
        "site_name": "Test",
        "plugins": ["search"],
        "theme": {"name": "simple-blog", **theme},
    }
    (root / "mkdocs.yml").write_text(yaml.safe_dump(config), encoding="utf-8")
    subprocess.run(
        [sys.executable, "-m", "mkdocs", "build", "--strict", "-q"],
        cwd=root,
        check=True,
    )
    return root / "site"


def _duplicate_ids(html: str) -> list[str]:
    counts = Counter(re.findall(r'\sid="([^"]+)"', html))
    return [element_id for element_id, count in counts.items() if count > 1]


class UniqueIdsTests(unittest.TestCase):
    def assert_unique_ids(self, site: Path) -> None:
        for page in site.rglob("*.html"):
            with self.subTest(page=str(page.relative_to(site))):
                self.assertEqual(_duplicate_ids(page.read_text()), [])

    def test_sidebar_layout_has_unique_ids(self) -> None:
        site = _build({"sidebar": True})
        html = (site / "index.html").read_text()
        self.assertIn('id="component-main"', html)
        self.assertEqual(html.count('id="component-content"'), 1)
        self.assert_unique_ids(site)

    def test_default_layout_has_unique_ids(self) -> None:
        self.assert_unique_ids(_build({}))


if __name__ == "__main__":
    unittest.main()
