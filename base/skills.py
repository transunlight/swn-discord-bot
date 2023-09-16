"""
Module defines classes:
- Skill
- AbstractSkills

Used for storing skills of a character
"""

from abc import ABC


class Skill:
    """
    Class for a single skill

    Attributes
    ----------
    level : int
        level of training in skill, an untrained skill is None

    Methods
    -------
    train(inc=1)
        trains the skill, increasing its level by `inc`
    """

    __slots__ = ["level"]

    def __init__(self, level: int | None = None):
        self.level = level

    def __repr__(self) -> str:
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
    """
    Abstract class for storing multiple skills

    Methods
    -------
    get(skill)
        returns the level of the given skill

    get_all()
        returns a dict containing all trained skills and their levels

    train(skills)
        trains all the skills according to the given dict
    """

    __slots__: tuple[str, ...] = ()

    def __init__(self, **kwargs: int):
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

    def get(self, skill: str) -> int | None:
        """Return level corresponding to `skill`"""
        return getattr(self, skill).level

    def get_all(self) -> dict[str, int]:
        """Return dict containing all trained skills"""
        return {
            skill: level
            for skill in self.__slots__
            if (level := self.get(skill)) is not None
        }

    def train(self, skills: dict[str, int]) -> None:
        """Train the skills by the levels given"""
        for key, value in skills.items():
            getattr(self, key).train(value)
