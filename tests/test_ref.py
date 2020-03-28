import jsonschema_instance as js


def test_simple_ref():
    obj = js.create_from("./schemas/ref/simple.json")
    assert obj == {"billing_address": {"street": "samplestreet", "city": "", "state": ""}}
