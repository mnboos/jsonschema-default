import pytest

import jsonschema_default as js


def test_minimum():
    obj = js.create_from("./schemas/number/min.json")
    assert obj == {"number": 10, "integer": 1337}


def test_multipleof():
    obj = js.create_from("./schemas/number/multipleOf.json")
    assert obj == {"number": 11}


def test_multipleof_with_minimum():
    obj = js.create_from("./schemas/number/multipleOf_with_minimum.json")
    assert obj == {"number": 12}


def test_negative_maximum():
    obj = js.create_from("./schemas/number/negative_max.json")
    assert obj == {"number": -10}


def test_invalid_minmax():
    with pytest.raises(ValueError):
        js.create_from("./schemas/number/invalid_minmax.json")


def test_exclusive_min():
    obj = js.create_from("./schemas/number/exclusive_min.json")
    assert obj == {"number": 11}


def test_min_and_exclusive_min():
    obj = js.create_from("./schemas/number/min_and_exclusive_min.json")
    assert obj == {"number": 12}


def test_invalid_exclusive_min():
    with pytest.raises(ValueError):
        js.create_from("./schemas/number/invalid_exclusive_min.json")


def test_default():
    """
    If a default is defined in the schema, the generated value should be the default.
    :return:
    """

    obj = js.create_from("./schemas/number/default.json")
    assert obj == 0
