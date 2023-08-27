"""
Module defines classes:
- Attribute
- Attributes

Used for storing attributes of a character
"""

from __future__ import annotations

from attrs import define, field, frozen
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


@frozen
class Attributes:
    """
    Class for holding attributes:
        strength, dexterity, constitution, intelligence, wisdom, charisma
    """

    strength: Attribute = field(converter=Attribute)
    dexterity: Attribute = field(converter=Attribute)
    constitution: Attribute = field(converter=Attribute)
    intelligence: Attribute = field(converter=Attribute)
    wisdom: Attribute = field(converter=Attribute)
    charisma: Attribute = field(converter=Attribute)

    def __str__(self):
        return (
            f"**STR**: {self.strength!s}"
            f"**DEX**: {self.dexterity!s}"
            f"**CON**: {self.constitution!s}"
            f"**INT**: {self.intelligence!s}"
            f"**WIS**: {self.wisdom!s}"
            f"**CHA**: {self.charisma!s}"
        )
