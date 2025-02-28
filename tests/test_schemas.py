from types import NoneType

import pytest

import jsonschema_default as js


def test_empty():
    obj = js.create_from("./schemas/empty.json")
    assert obj == {}


def test_simple():
    obj = js.create_from("./schemas/simple.json")
    assert isinstance(obj["string"], str)
    assert isinstance(obj["boolean"], bool)
    assert isinstance(obj["null"], NoneType)


def test_const():
    obj = js.create_from("./schemas/const.json")
    assert obj == {"string": "hello world"}


def test_property_type_list():
    obj = js.create_from("./schemas/prop_type_list.json")
    assert isinstance(obj["stringorint"], str)


def test_property_type_list_empty():
    with pytest.raises(RuntimeError):
        js.create_from("./schemas/prop_type_list_empty.json")


def test_missing_type():
    with pytest.raises(RuntimeError):
        js.create_from("./schemas/unknown_type.json")
