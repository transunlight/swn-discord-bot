"""
Utility stuff:
- TechLevel

"""

from __future__ import annotations

from enum import StrEnum


class TechLevel(StrEnum):
    """Class for marking tech level"""

    TL0 = "Neolithic"
    TL1 = "Pre-Gunpowder"
    TL2 = "Early Industrial"
    TL3 = "21st Century"
    TL4 = "Postech"
    TL5 = "Pretech"
    TL6 = "Pretech-Plus"
