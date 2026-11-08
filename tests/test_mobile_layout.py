"""Tests for the mobile layout CSS (issue #107)."""

from __future__ import annotations

import re
import unittest

from .fixtures import THEME_DIR

MEDIA_CSS = THEME_DIR / "assets" / "css" / "media.min.css"
TEMPLATE_CSS = THEME_DIR.parent / "template" / "assets" / "css"
MOBILE_QUERY = r"@media only screen and \(max-width:780px\)\{[^@]*?"


class MobileLayoutCssTests(unittest.TestCase):
    def setUp(self) -> None:
        self.css = MEDIA_CSS.read_text()

    def test_container_padding_is_reduced_on_mobile(self) -> None:
        self.assertRegex(
            self.css, MOBILE_QUERY + r"\.container\{padding-left:1%!important"
        )

    def test_rows_do_not_overflow_reduced_container_padding(self) -> None:
        self.assertRegex(
            self.css,
            MOBILE_QUERY
            + r"\.container>\.row\{margin-left:0;margin-right:0\}",
        )

    def test_mobile_row_reset_has_no_stray_braces(self) -> None:
        self.assertEqual(self.css.count("{"), self.css.count("}"))
        self.assertIsNotNone(re.search(r"\.container>\.row\{", self.css))

    def test_template_min_css_matches_theme(self) -> None:
        template_css = (TEMPLATE_CSS / "media.min.css").read_text()
        self.assertEqual(template_css, self.css)

    def test_template_source_css_has_row_reset(self) -> None:
        source = (TEMPLATE_CSS / "media.css").read_text()
        self.assertRegex(
            source,
            r"\.container > \.row \{\s*margin-left: 0;\s*margin-right: 0;",
        )


if __name__ == "__main__":
    unittest.main()
