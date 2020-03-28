import jsonschema_instance as js


def test_min_length():
    obj = js.create_from("./schemas/string/minLength.json")
    assert obj == {"string": "  "}
