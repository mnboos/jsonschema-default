import pytest

from jsonschema_default import DefaultOptions


def test_string_min_length_not_negative():
    with pytest.raises(ValueError):
        DefaultOptions(string_min_length=-5)


def test_string_max_length_gt_min_length():
    with pytest.raises(ValueError):
        DefaultOptions(string_min_length=5, string_max_length=4)
