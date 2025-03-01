import pytest

import jsonschema_default as js
from jsonschema_default.errors import RefCycleError


def test_simple_ref():
    obj = js.create_from("../schemas/ref/simple.json")
    assert obj == {"billing_address": {"street": "mystreet", "city": "mycity", "state": "mystate"}}


def test_ref_cycle():
    with pytest.raises(RefCycleError) as exc:
        js.create_from("../schemas/ref/cycle.json")
    assert "#/definitions/alice -> #/definitions/bob -> #/definitions/alice" in str(exc.value)


def test_any_of():
    obj = js.create_from("../schemas/ref/anyOf.json")
    assert obj == {"person": {"name": "alice"}}


def test_thing():
    obj = js.create_from("../schemas/ref/thing.json")
    assert obj == {"thing": "foo"}


def test_deep_ref():
    obj = js.create_from("../schemas/ref/abcd.json")
    assert obj == {"abcd": "foobar"}


def test_streetaddress():
    obj = js.create_from("../schemas/ref/streetaddress.json")
    assert obj == {
        "address": {"street": {"block": 123, "name": "Default STREET NAME value"}},
        "first_name": "Default NAME value",
        "last_name": "Default LAST NAME value",
    }
