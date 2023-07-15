"""Test skills.py"""
# pylint: disable=protected-access

from unittest.mock import patch, call, create_autospec
from contextlib import nullcontext as does_not_raise

import pytest

from base.skills import Skill, Skills, AbstractSkills, PsychicSkills


@pytest.fixture(name="mock_skill")
def _mock_skill():
    return create_autospec(Skill, spec_set=True, instance=True)


# @pytest.fixture(name="mock_abstract_skills")
# def _mock_abstract_skills():
#     return create_autospec(AbstractSkills, spec_set=True, instance=True)


attrs = [f"val_{i}" for i in range(5)]
param = {f"val_{i}": i for i in range(5)}


@pytest.fixture(name="mock_concrete_skills")
def _mock_concrete_skills():
    return create_autospec(
        TestAbstractSkills.ConcreteSkills, spec_set=True, instance=True
    )


class TestSkill:
    @pytest.mark.parametrize("level", [None, 0, 1, 2, 3, 4])
    def test_init(self, level):
        skill = Skill(level)
        assert skill.level == level

    @pytest.mark.parametrize("level", [None, 0, 1, 2, 3, 4])
    def test_repr(self, mock_skill, level):
        mock_skill.level = level
        assert (
            Skill.__repr__(mock_skill)
            == "Skill(" + ("Untrained" if level is None else f"level={level}") + ")"
        )

    @pytest.mark.parametrize("inc", [None, 0, 1, 2, 3, 4])
    @pytest.mark.parametrize("lvl", [None, 0, 1, 2, 3, 4])
    def test_train(self, mock_skill, lvl, inc):
        mock_skill.level = lvl

        lvl_val = -1 if lvl is None else lvl
        inc_val = 1 if inc is None else inc

        error = (inc_val == 0) or (inc_val + lvl_val > 4)
        expectation = pytest.raises(ValueError) if error else does_not_raise()

        with expectation:
            if inc is None:
                Skill.train(mock_skill)
            else:
                Skill.train(mock_skill, inc)
            assert mock_skill.level == inc_val + lvl_val

        if error:
            print(expectation)
            assert mock_skill.level == lvl


class TestAbstractSkills:
    class ConcreteSkills(AbstractSkills):
        """Implementation of AbstractSkills for testing"""

        __slots__ = attrs

    @pytest.mark.parametrize("params", [{}, param])
    @patch("base.skills.Skill", autospec=True, side_effect=attrs)
    def test_init(self, mock_skill_class, params):
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

    def test_repr(self, mock_concrete_skills):
        mock_concrete_skills.get_all.return_value = param
        assert (
            AbstractSkills.__repr__(mock_concrete_skills)
            == "Skills(" + ", ".join([f"{k}={v}" for k, v in param.items()]) + ")"
        )
        mock_concrete_skills.get_all.assert_called_once()

    @pytest.mark.parametrize("attr", attrs)
    def test_get(self, mock_concrete_skills, attr):
        assert (
            AbstractSkills.get(mock_concrete_skills, attr)
            == getattr(mock_concrete_skills, attr).level
        )

    @pytest.mark.parametrize("skills", [["val_0", "val_1", "val_2"]])
    def test_get_all(self, mock_concrete_skills, skills):
        mock_concrete_skills.__slots__ = attrs
        mock_concrete_skills.get.side_effect = (
            lambda skill: skill if skill in skills else None
        )
        assert AbstractSkills.get_all(mock_concrete_skills) == {
            skill: skill for skill in skills
        }

    @pytest.mark.parametrize("train_dict", [{"val_0": 1, "val_1": 2}])
    def test_train(self, mock_concrete_skills, train_dict):
        AbstractSkills.train(mock_concrete_skills, train_dict)
        for attr, value in train_dict.items():
            getattr(mock_concrete_skills, attr).train.assert_called_once_with(value)


def test_class_skills():
    # Test __slots__?
    assert Skills.mro()[1] == AbstractSkills


def test_class_psychic_skills():
    # Test __slots__?
    assert PsychicSkills.mro()[1] == AbstractSkills
