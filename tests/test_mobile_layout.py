"""Tests for the mobile layout CSS (issue #107)."""

from __future__ import annotations

import re
import unittest

from .fixtures import THEME_DIR

MEDIA_CSS = THEME_DIR / "assets" / "css" / "media.min.css"
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


if __name__ == "__main__":
    unittest.main()
