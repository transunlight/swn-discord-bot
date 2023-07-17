"""
Module defining classes:
- Sextuple
- Attributes

Used for storing attributes of a character
"""

from __future__ import annotations

from .consts import ATTRIBUTES
from .utils import check_attributes
from .dice import d6_3


class Attribute:
    """Class for holding a single attribute"""

    __slots__ = ["__score", "mod"]

    def __init__(self, score: int = None):
        self.mod = None
        self.score = score or d6_3()

    @property
    def score(self):
        """Score of the attribute"""
        return self.__score

    @score.setter
    def score(self, value: int):
        Attribute.check_score(value)
        self.__score = value
        self.mod = self.get_mod()

    def __repr__(self) -> str:
        return f"Attribute(score={self.score}, mod={self.mod})"

    def get_mod(self) -> int:
        """Return the modifier for this attribute"""
        return (self.score - 10 if self.score > 10 else self.score - 8) // 4

    @classmethod
    def check_score(cls, score) -> None:
        """Check whether score is in [3, 18]"""
        if not 3 <= score <= 18:
            raise ValueError(f"Value of {score} is out-of-bounds")


class Attributes:
    """Class for holding attributes for a character"""

    __slots__ = ATTRIBUTES

    def __init__(self, **kwargs):
        if kwargs:
            check_attributes("Attributes", self.__slots__, kwargs.keys())
            for key, value in kwargs.items():
                setattr(self, key, Attribute(value))
        else:
            for key in self.__slots__:
                setattr(self, key, Attribute())

    def __repr__(self) -> str:
        return f"Attributes({[getattr(self, attr).score for attr in self.__slots__]})"

    def __setattr__(self, __name: str, __value: Attribute | int) -> None:
        if isinstance(__value, Attribute):
            super().__setattr__(__name, __value)
        elif isinstance(__value, int):
            getattr(self, __name).score = __value
        else:
            raise TypeError(f"can only assign int or Attribute to {__name}")
