"""Jinja date-formatting filter shared by modules/content.html."""

from __future__ import annotations

from typing import Any

_MONTHS = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def format_date(value: Any) -> Any:
    """Format a date-like value as 'Month D, YYYY'.

    Used by modules/content.html to render manual `date`/`updated` front
    matter fields consistently with mkdocs-git-revision-date-localized's
    pre-formatted output (the fallback when no manual override is set).
    """
    if value is None or value == "":
        return value
    if (
        hasattr(value, "year")
        and hasattr(value, "month")
        and hasattr(value, "day")
    ):
        return f"{_MONTHS[value.month - 1]} {value.day}, {value.year}"
    return value
