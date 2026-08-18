"""URL-safe slug generation, used for generated category/tag page paths."""

from __future__ import annotations

import re


def slugify(value: str) -> str:
    value = re.sub(r"[^\w\s-]", "", value).strip().lower()
    return re.sub(r"[\s_]+", "-", value)
