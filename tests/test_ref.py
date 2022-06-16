import jsonschema_default as js
import pytest


def test_simple_ref():
    obj = js.create_from("./schemas/ref/simple.json")
    assert obj == {"billing_address": {"street": "samplestreet", "city": "", "state": ""}}


def test_ref_cycle():
    with pytest.raises(Exception, match="Cyclic refs are not allowed") as excinfo:
        js.create_from("./schemas/ref/cycle.json")
