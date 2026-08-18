"""Jinja date-formatting filter shared by modules/content.html."""

from __future__ import annotations

from typing import Any

try:
    from babel.dates import format_date as _babel_format_date

    _HAS_BABEL = True
except ImportError:  # pragma: no cover
    _HAS_BABEL = False

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


def _is_date_like(value: Any) -> bool:
    return (
        hasattr(value, "year")
        and hasattr(value, "month")
        and hasattr(value, "day")
    )


def format_date(value: Any, locale: str = "en") -> Any:
    """Format a date-like value as a long-form localized date.

    Used by modules/content.html to render manual `date`/`updated` front
    matter fields consistently with the git-derived fallback dates.

    Uses `babel` (a direct dependency of this package) for real
    locale-aware month names/date order, e.g. `locale="pt"` renders
    "5 de janeiro de 2024" instead of "January 5, 2024". Falls back to
    a hardcoded English "Month D, YYYY" format if babel is somehow
    unavailable at runtime (mirrors `mkdocs.localization.has_babel`,
    since babel is only an optional dependency of `mkdocs` itself).
    """
    if value is None or value == "":
        return value
    if not _is_date_like(value):
        return value
    if _HAS_BABEL:
        return _babel_format_date(value, format="long", locale=locale)
    return f"{_MONTHS[value.month - 1]} {value.day}, {value.year}"
