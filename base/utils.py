"""
Utility functions:
- check_attributes(str, Iterable, Iterable)

"""

from __future__ import annotations

from typing import Iterable


def check_attributes(class_name: str, attr: Iterable, args: Iterable):
    """Raise error if passed attributes are not same as class attributes."""
    if set(args) != set(attr):
        raise AttributeError(
            f"'{class_name}' requires attributes {list(attr)}, was given {list(args)}"
        )
