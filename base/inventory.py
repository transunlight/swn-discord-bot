"""
Module defining classes:
- Item

"""

from __future__ import annotations

from fractions import Fraction

from attrs import frozen

from .utils import TechLevel


@frozen
class Item:
    """Class for item"""

    cost: int
    name: str
    encumbrance: Fraction
    description: str
    tech_level: TechLevel
