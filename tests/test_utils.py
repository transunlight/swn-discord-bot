"""Test utils.py"""

import pytest

from base.utils import check_attributes


def test_check_attributes():
    attr_1 = ["a", "b", "c", "d", "e"]
    attr_2 = ["a", "b", "c", "d", "e"]
    attr_3 = ["f", "g", "h", "i", "j"]

    check_attributes("test", attr_1, attr_2)
    with pytest.raises(AttributeError):
        check_attributes("test", attr_1, attr_3)
