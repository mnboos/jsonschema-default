import jsonschema_default as js


def test_empty():
    obj = js.create_from("./schemas/empty.json")
    assert obj == {}


def test_simple():
    obj = js.create_from("./schemas/simple.json")
    assert obj == {"string": "", "number": 0, "boolean": False, "null": None}


def test_object():
    obj = js.create_from("./schemas/object.json")
    assert obj == {"object": {"string": ""}}
