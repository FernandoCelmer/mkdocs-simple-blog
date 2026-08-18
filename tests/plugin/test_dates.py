"""Tests for mkdocs_simple_blog.plugin.dates."""

from __future__ import annotations

import datetime
import unittest

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
