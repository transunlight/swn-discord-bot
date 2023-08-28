"""
Constants:
- SKILLS
- COMBAT_SKILLS
- PSYCHIC_SKILLS

"""

from __future__ import annotations


SKILLS: tuple[str, ...] = (
    "Administer",
    "Connect",
    "Exert",
    "Fix",
    "Heal",
    "Know",
    "Lead",
    "Notice",
    "Perform",
    "Pilot",
    "Program",
    "Punch",
    "Shoot",
    "Sneak",
    "Stab",
    "Survive",
    "Talk",
    "Trade",
    "Work",
)
"""Tuple containing all non-psychic skills"""


COMBAT_SKILLS: tuple[str, ...] = (
    "Punch",
    "Shoot",
    "Stab",
)
"""Tuple containing all combat skills"""


PSYCHIC_SKILLS: tuple[str, ...] = (
    "Biopsionics",
    "Metapsionics",
    "Precognition",
    "Telekinesis",
    "Telepathy",
    "Teleportation",
)
"""Tuple containing all psychic skills"""
