"""Utility functions."""

from functools import reduce
from typing import Any, Mapping


def deep_get(data: Mapping[str, Any], key: str, default: Any = None) -> Any:
    """Get deep key."""

    return reduce(lambda x, y: x.get(y, default), key.split("."), data)
