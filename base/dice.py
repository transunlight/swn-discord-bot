"""
Easy to use dice

Defines:
- `d{6, 8, 20}` : Dice
- `p{2, 3, 4}d6`: Dice pools
- `d6_{2, 3, 4}`: Functions

"""

from __future__ import annotations

from dyce import H, P

d6, d8, d20 = H(6), H(8), H(20)

p2d6, p3d6, p4d6 = 2 @ P(6), 3 @ P(6), 4 @ P(6)

d6_2, d6_3, d6_4 = p2d6.h().roll, p3d6.h().roll, p4d6.h().roll
