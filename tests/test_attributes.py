"""Test attributes.py"""

from __future__ import annotations

from contextlib import nullcontext as does_not_raise
from typing import TYPE_CHECKING

import pytest

from base.attributes import Attribute

if TYPE_CHECKING:
    from typing import Any

    from pytest import FixtureRequest


class TestAttribute:
    @pytest.fixture(params=[3, 7, 10, 11, 14, 18])
    def score(self, request: FixtureRequest) -> int:
        """Fixture to inject a score"""
        return request.param

    @pytest.fixture
    def mod(self, score: int) -> int:
        """Fixture to inject a modifier"""
        if score == 3:
            return -2
        if score <= 7:
            return -1
        if score <= 13:
            return 0
        if score <= 17:
            return 1
        return 2

    @pytest.fixture(params=[2, 3, 7, 10, 11, 14, 18, 20])
    def ext_score(self, request: FixtureRequest):
        """Fixture to inject a score from an extended range"""
        return request.param

    @pytest.fixture
    def exception(self, ext_score: int):
        """Fixture to inject appropriate exception handling context"""
        return does_not_raise() if 3 <= ext_score <= 18 else pytest.raises(ValueError)

    @pytest.fixture
    def string(self, score: int, mod: int):
        """Inject appropriate string as output of __str__"""
        return f"{score} ({mod:+})"

    def test_mod(self, score: int, mod: int):
        attr = Attribute(score)
        assert attr.mod == mod

    def test_str(self, score: int, string: str):
        assert str(Attribute(score)) == string

    def test_validator_init(self, ext_score: int, exception: Any):
        with exception:
            Attribute(ext_score)

    def test_validator_set(self, ext_score: int, exception: Any):
        attr = Attribute(10)
        with exception:
            attr.score = ext_score
