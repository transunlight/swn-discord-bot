"""Test skills.py"""
# pylint: disable=protected-access

from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING

import pytest

from base.skills import Skill

if TYPE_CHECKING:
    from pytest import FixtureRequest


class TestSkill:
    @pytest.fixture(params=[None, 0, 1, 2, 3, 4])
    def level(self, request: FixtureRequest) -> int | None:
        """Fixture to inject level"""
        return request.param

    @pytest.fixture
    def skill(self, level: int | None) -> Skill:
        """Fixture to inject a Skill object with a given level"""
        return Skill() if level is None else Skill(level)

    def test_init(self, level: int | None, skill: Skill):
        assert skill.level == level

    def test_repr(self, level: int | None, skill: Skill):
        assert repr(skill) == f"Skill(level={level})"

    @pytest.mark.parametrize("increment", [None, 0, 1, 2, 3, 4])
    def test_train(self, level: int | None, skill: Skill, increment: int | None):
        lvl_val = -1 if level is None else level
        inc_val = 1 if increment is None else increment

        error = (inc_val == 0) or (inc_val + lvl_val > 4)
        expectation = pytest.raises(ValueError) if error else does_not_raise()

        with expectation:
            if increment is None:
                skill.train()
            else:
                skill.train(increment)
            assert skill.level == inc_val + lvl_val

        if error:
            print(expectation)
            assert skill.level == level
