from types import NoneType

import jsonschema_default as js


def test_empty():
    obj = js.create_from("./schemas/empty.json")
    assert obj == {}


def test_simple():
    obj = js.create_from("./schemas/simple.json")
    assert type(obj["string"]) == str
    assert type(obj["boolean"]) == bool
    assert type(obj["null"]) == NoneType


def test_const():
    obj = js.create_from("./schemas/const.json")
    assert obj == {"string": "hello world"}


def test_object():
    obj = js.create_from("./schemas/object.json")
    assert type(obj["string"]) == str


def test_property_type_list():
    obj = js.create_from("./schemas/prop_type_list.json")
    assert type(obj["stringorint"]) == str
