"""Test skills.py"""
# pylint: disable=protected-access

from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING
from unittest.mock import call, create_autospec, patch

import pytest

from base.skills import Skill, AbstractSkills

if TYPE_CHECKING:
    from unittest.mock import Mock

    from pytest import FixtureRequest


# @pytest.fixture(name="mock_abstract_skills")
# def _mock_abstract_skills():
#     return create_autospec(AbstractSkills, spec_set=True, instance=True)


attrs: tuple[str, ...] = tuple(f"val_{i}" for i in range(5))
param: dict[str, int] = {f"val_{i}": i for i in range(5)}


@pytest.fixture(name="_mock_concrete_skills")
def mock_concrete_skills():
    """Fixture which creates Mock of ConcreteSkills"""
    return create_autospec(
        TestAbstractSkills.ConcreteSkills, spec_set=True, instance=True
    )


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


class TestAbstractSkills:
    class ConcreteSkills(AbstractSkills):
        """Implementation of AbstractSkills for testing"""

        __slots__ = attrs

    @pytest.mark.parametrize("params", [{}, param])
    @patch("base.skills.Skill", autospec=True, side_effect=attrs)
    def test_init(self, mock_skill_class: Mock, params: dict[str, int]):
        with pytest.raises(AttributeError) as info:
            _obj = TestAbstractSkills.ConcreteSkills(val=1)
        assert "'ConcreteSkills' does not have attributes '['val']'" == str(info.value)

        obj = TestAbstractSkills.ConcreteSkills(**params)
        mock_skill_class.assert_has_calls(
            [call(i) for _, i in params.items()] or ([call()] * 5)
        )
        assert mock_skill_class.call_count == 5
        for attr in attrs:
            assert getattr(obj, attr) == attr

    def test_repr(self, _mock_concrete_skills: Mock):
        _mock_concrete_skills.get_all.return_value = param
        assert (
            AbstractSkills.__repr__(_mock_concrete_skills)
            == "Skills(" + ", ".join([f"{k}={v}" for k, v in param.items()]) + ")"
        )
        _mock_concrete_skills.get_all.assert_called_once()

    @pytest.mark.parametrize("attr", attrs)
    def test_get(self, _mock_concrete_skills: Mock, attr: str):
        assert (
            AbstractSkills.get(_mock_concrete_skills, attr)
            == getattr(_mock_concrete_skills, attr).level
        )

    @pytest.mark.parametrize("skills", [["val_0", "val_1", "val_2"]])
    def test_get_all(self, _mock_concrete_skills: Mock, skills: list[str]):
        _mock_concrete_skills.__slots__ = attrs
        _mock_concrete_skills.get.side_effect = (
            lambda skill: skill if skill in skills else None
        )
        assert AbstractSkills.get_all(_mock_concrete_skills) == {
            skill: skill for skill in skills
        }

    @pytest.mark.parametrize("train_dict", [{"val_0": 1, "val_1": 2}])
    def test_train(self, _mock_concrete_skills: Mock, train_dict: dict[str, int]):
        AbstractSkills.train(_mock_concrete_skills, train_dict)
        for attr, value in train_dict.items():
            getattr(_mock_concrete_skills, attr).train.assert_called_once_with(value)
