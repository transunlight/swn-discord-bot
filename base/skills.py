"""
Module defines classes:
- Skill

Used for storing skills of a character
"""


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
