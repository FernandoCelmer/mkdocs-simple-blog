"""Regression tests for issue #84 — generic a:hover rules must not
override componentized link-based elements (buttons, pills, tags).
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent.parent


class LinkHoverScopeTests(unittest.TestCase):
    def _read(self, relative_path: str) -> str:
        return (ROOT_DIR / relative_path).read_text()

    def test_source_css_scopes_generic_hover_rule_to_classless_anchors(
        self,
    ) -> None:
        css = self._read("template/assets/css/main.css")
        self.assertIn("a:not([class]):focus", css)
        self.assertIn("a:not([class]):hover", css)

    def test_source_css_drops_important_from_generic_hover_rule(self) -> None:
        css = self._read("template/assets/css/main.css")
        rule = css.split("a:not([class]):hover", 1)[1].split("}", 1)[0]
        self.assertNotIn("!important", rule)

    def test_no_unscoped_a_hover_rule_with_important_remains(self) -> None:
        """A bare `a:hover{...!important...}` (no class/attribute scoping)
        would beat any `.btn:hover`/`.cta:hover`/`.tag:hover` component rule
        on specificity even when both carry `!important` -- see issue #84.
        """
        for relative_path in (
            "template/assets/css/main.css",
            "mkdocs_simple_blog/assets/css/main.min.css",
        ):
            css = self._read(relative_path)
            for match in re.finditer(r"([^{}]+)\{([^{}]*)\}", css):
                selector, body = match.group(1), match.group(2)
                if "!important" not in body:
                    continue
                for single_selector in selector.split(","):
                    single_selector = single_selector.strip()
                    if re.fullmatch(r"a(:focus|:hover)+", single_selector):
                        self.fail(
                            f"Unscoped '{single_selector}' with !important "
                            f"in {relative_path} will override componentized "
                            "links (see issue #84)"
                        )

    def test_shipped_minified_css_scopes_generic_hover_rule(self) -> None:
        css = self._read("mkdocs_simple_blog/assets/css/main.min.css")
        self.assertIn("a:not([class]):hover", css)
