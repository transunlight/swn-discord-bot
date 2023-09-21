"""
Module defining classes:
- Inventory
- Item

"""

from __future__ import annotations

from fractions import Fraction
from math import ceil

from attrs import define, field, frozen

from .utils import TechLevel


@frozen
class Item:
    """Class for item"""

    cost: int
    name: str
    encumbrance: Fraction
    description: str
    tech_level: TechLevel


@define
class Inventory:
    """Class for inventory"""

    readied: dict[Item, int] = field(factory=dict, init=False)
    stowed: dict[Item, int] = field(factory=dict, init=False)
    e_credits: int = field(default=0, init=False)

    @property
    def readied_encumbrance(self) -> int:
        """Encumbrance of all readied items"""
        return sum(ceil(item.encumbrance * cnt) for item, cnt in self.readied.items())

    @property
    def stowed_encumbrance(self) -> int:
        """Encumbrance of all stowed items"""
        return sum(ceil(item.encumbrance * cnt) for item, cnt in self.stowed.items())

    @property
    def credits(self) -> int:
        """Total credits"""
        return self.e_credits
