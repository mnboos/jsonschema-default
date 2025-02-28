import jsonschema_default as js


def test_object():
    obj = js.create_from("./schemas/object/object.json")
    assert isinstance(obj["string"], str)
