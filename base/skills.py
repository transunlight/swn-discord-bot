"""
Module defining class:
- Skill
- AbstractSkills
- Skills
- PsychicSkills

Used for storing skills of a character
"""

from abc import ABC

from .consts import SKILLS, PSYCHIC_SKILLS


class Skill:
    """Class for a single skill"""

    __slots__ = ["level"]

    def __init__(self, level: int = None):
        self.level = level

    def __repr__(self) -> str:
        if self.level is None:
            return "Skill(Untrained)"
        return f"Skill(level={self.level})"

    def train(self, inc: int = 1) -> None:
        """Increase the level of the skill"""
        if inc < 1:
            raise ValueError(f"Increment = {inc}, must be at least 1")
        new_level = inc + (-1 if self.level is None else self.level)
        if new_level > 4:
            raise ValueError(f"New level = {new_level}, must be at most 4")
        self.level = new_level


class AbstractSkills(ABC):
    """Abstract class for storing multiple skills"""

    __slots__ = []

    def __init__(self, **kwargs):
        ex_attrs = list(set(kwargs.keys()) - set(self.__slots__))
        if len(ex_attrs) > 0:
            raise AttributeError(
                f"'{type(self).__name__}' does not have attributes '{ex_attrs}'"
            )

        for skill in self.__slots__:
            if skill in kwargs:
                setattr(self, skill, Skill(kwargs[skill]))
            else:
                setattr(self, skill, Skill())

    def __repr__(self) -> str:
        return (
            "Skills("
            + ", ".join([f"{skill}={level}" for skill, level in self.get_all().items()])
            + ")"
        )

    def get(self, skill: str) -> int:
        """Return level corresponding to `skill`"""
        return getattr(self, skill).level

    def get_all(self) -> dict:
        """Return dict containing all trained skills"""
        return {
            skill: self.get(skill)
            for skill in self.__slots__
            if self.get(skill) is not None
        }

    def train(self, skills: dict) -> None:
        """Train the skills by the levels given"""
        for key, value in skills.items():
            getattr(self, key).train(value)


class Skills(AbstractSkills):
    """Class for storing non-psychic skills"""

    __slots__ = SKILLS


class PsychicSkills(AbstractSkills):
    """Class for storing psychic skills"""

    __slots__ = PSYCHIC_SKILLS
