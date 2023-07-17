"""Test attributes.py"""
# pylint: disable=protected-access

from unittest.mock import patch, call, PropertyMock, create_autospec
from contextlib import nullcontext as does_not_raise
from itertools import cycle

import pytest

from base.attributes import Attribute, Attributes


attributes = [
    "strength",
    "dexterity",
    "constitution",
    "intelligence",
    "wisdom",
    "charisma",
]
scores = [3, 7, 10, 11, 14, 18]
mods = [-2, -1, 0, 0, 1, 2]
attribute_scores = dict(zip(attributes, scores))
attribute_mods = dict(zip(attributes, mods))


@pytest.fixture(name="mock_attr")
def _mock_attr():
    return create_autospec(Attribute, spec_set=True, instance=True)


@pytest.fixture(name="mock_attr_score")
def _mock_attr_score():
    def _method(score):
        return create_autospec(Attribute, spec_set=True, instance=True, score=score)

    return _method


@pytest.fixture(name="mock_attrs")
def _mock_attrs():
    return create_autospec(Attributes, spec_set=True, instance=True)


@pytest.fixture(name="mock_filled_attrs")
def _mock_filled_attrs(mock_attrs, mock_attr_score):
    mock_attrs.__slots__ = attributes
    for attr, value in attribute_scores.items():
        setattr(mock_attrs, attr, mock_attr_score(value))
    return mock_attrs


class TestAttribute:
    @pytest.mark.parametrize("score", scores + [None])
    @patch("base.attributes.d6_3", return_value="roll")
    @patch("base.attributes.Attribute.score", new_callable=PropertyMock)
    def test_init(self, mock_score, mock_3d6, score):
        attr = Attribute(score)
        assert attr.mod is None
        mock_score.assert_called_once_with(score or "roll")
        if score is None:
            mock_3d6.assert_called_once()

    @pytest.mark.parametrize("score", scores)
    @patch("base.attributes.Attribute.check_score")
    def test_score(self, mock_check_score, mock_attr, score):
        Attribute.score.fset(mock_attr, score)
        mock_check_score.assert_called_once_with(score)
        mock_attr.get_mod.assert_called_once()
        assert Attribute.score.fget(mock_attr) == score

    @pytest.mark.parametrize(["score", "mod"], zip(scores, mods))
    def test_repr(self, mock_attr, score, mod):
        mock_attr.score = score
        mock_attr.mod = mod
        assert Attribute.__repr__(mock_attr) == f"Attribute(score={score}, mod={mod})"

    @pytest.mark.parametrize(["score", "mod"], zip(scores, mods))
    def test_get_mod(self, mock_attr, score, mod):
        mock_attr.score = score
        assert Attribute.get_mod(mock_attr) == mod

    @pytest.mark.parametrize(
        ["score", "expectation"],
        list(zip(scores, cycle([does_not_raise()])))
        + list(zip([2, 20], cycle([pytest.raises(ValueError)]))),
    )
    def test_check_score(self, score, expectation):
        with expectation:
            Attribute.check_score(score)


class TestAttributes:
    @pytest.mark.parametrize("attr_scores", [{}, attribute_scores])
    @patch("base.attributes.Attribute", autospec=True, return_value="attr")
    @patch("base.attributes.check_attributes", autospec=True)
    @patch("base.attributes.Attributes.__setattr__", autospec=True)
    def test_init(
        self,
        mock_setattr,
        mock_check_attributes,
        mock_attribute,
        attr_scores,
    ):
        _attr = Attributes(**attr_scores)

        if attr_scores:
            mock_check_attributes.assert_called_once_with(
                "Attributes", attributes, attr_scores.keys()
            )

        if attr_scores:
            mock_attribute.assert_has_calls([call(val) for val in scores])
        else:
            mock_attribute.assert_has_calls([call()] * 6)
        assert mock_attribute.call_count == 6

        mock_setattr.assert_has_calls([call(_attr, key, "attr") for key in attributes])
        assert mock_setattr.call_count == 6

    def test_repr(self, mock_filled_attrs):
        assert Attributes.__repr__(mock_filled_attrs) == f"Attributes({scores})"

    @pytest.mark.parametrize(
        "value, expectation",
        list(zip(scores + ["attribute"], cycle([does_not_raise()])))
        + [("other", pytest.raises(TypeError))],
    )
    @pytest.mark.parametrize("key", attributes)
    def test_setattr(self, mock_attrs, mock_attr, key, value, expectation):
        if value == "attribute":
            value = mock_attr
        org_val = getattr(mock_attrs, key)
        with expectation:
            Attributes.__setattr__(mock_attrs, key, value)
            assert getattr(mock_attrs, key).score == (
                value if isinstance(value, int) else value.score
            )
        if value == "other":
            assert getattr(mock_attrs, key) == org_val
