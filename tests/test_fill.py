import pytest

import jsonschema_default as js
from jsonschema_default.errors import RefCycleError


def test_fill_empty():
    obj = {}
    js.fill_from("../schemas/empty.json", target=obj)
    assert obj == {}


def test_fill_const():
    obj = {}
    js.fill_from("../schemas/const.json", target=obj)
    assert obj == {"string": "hello world"}


def test_fill_const_prefilled():
    obj = {"string": "blub"}
    js.fill_from("../schemas/const.json", target=obj)
    assert obj == {"string": "blub"}


def test_fill_nested():
    obj = {"a": {"a.1": "blub"}}
    js.fill_from("../schemas/object/nestedObject.json", target=obj)
    assert obj == {"a": {"a.1": "blub", "a.2": 123}}


def test_fill_empty_list_stays_empty():
    obj = {"array": []}
    js.fill_from("../schemas/array/anyOf.json", target=obj)
    assert obj == {"array": []}
