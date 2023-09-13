"""
Module defines classes:
- Attribute

Used for storing attributes of a character
"""

from __future__ import annotations

from attrs import define, field
from attrs.validators import instance_of, le, ge


@define
class Attribute:
    """
    Class for holding a single attribute

    Attributes
    ----------
    score : int
        score corresponding to the attribute
    mod   : int
        modifier corresponding to the attribute
    """

    score: int = field(validator=[instance_of(int), ge(3), le(18)])

    @property
    def mod(self) -> int:
        """Modifier of the attribute"""
        return (self.score - 10 if self.score > 10 else self.score - 8) // 4

    def __str__(self) -> str:
        return f"{self.score} ({self.mod:+})"
