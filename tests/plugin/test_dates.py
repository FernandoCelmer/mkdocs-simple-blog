"""Tests for mkdocs_simple_blog.plugin.dates."""

from __future__ import annotations

import datetime
import unittest

from mkdocs_simple_blog.plugin import dates
from mkdocs_simple_blog.plugin.dates import format_date


class FormatDateTests(unittest.TestCase):
    def test_formats_date_object_as_month_day_year(self) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 1, 5)), "January 5, 2024"
        )

    def test_formats_datetime_object(self) -> None:
        self.assertEqual(
            format_date(datetime.datetime(2023, 12, 17, 10, 30)),
            "December 17, 2023",
        )

    def test_december_is_last_month_index(self) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 12, 1)), "December 1, 2024"
        )

    def test_none_passes_through_unchanged(self) -> None:
        self.assertIsNone(format_date(None))

    def test_empty_string_passes_through_unchanged(self) -> None:
        self.assertEqual(format_date(""), "")

    def test_non_date_value_passes_through_unchanged(self) -> None:
        self.assertEqual(format_date("already a string"), "already a string")


class FormatDateLocaleTests(unittest.TestCase):
    """Only meaningful when babel is installed -- see FormatDateNoBabelTests
    for the fallback path exercised when it isn't."""

    def setUp(self) -> None:
        if not dates._HAS_BABEL:
            self.skipTest("babel not installed")

    def test_portuguese_locale_uses_localized_month_names(self) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 1, 5), locale="pt"),
            "5 de janeiro de 2024",
        )

    def test_spanish_locale_uses_localized_month_names(self) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 1, 5), locale="es"),
            "5 de enero de 2024",
        )

    def test_defaults_to_english_when_locale_omitted(self) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 1, 5)), "January 5, 2024"
        )


class FormatDateNoBabelTests(unittest.TestCase):
    """Simulates babel being unavailable (an optional mkdocs dependency),
    exercising the hardcoded-English fallback path."""

    def setUp(self) -> None:
        self._original = dates._HAS_BABEL
        dates._HAS_BABEL = False
        self.addCleanup(setattr, dates, "_HAS_BABEL", self._original)

    def test_falls_back_to_english_month_table_regardless_of_locale(
        self,
    ) -> None:
        self.assertEqual(
            format_date(datetime.date(2024, 1, 5), locale="pt"),
            "January 5, 2024",
        )
