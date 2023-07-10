import jsonschema_default as js


def test_oneof():
    obj = js.create_from("./schemas/oneOf/oneof_bool.json")
    assert isinstance(obj, bool) and obj
