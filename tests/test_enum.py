import jsonschema_default as js


def test_min_length():
    obj = js.create_from("./schemas/enum/enum.json")
    assert obj == {"enum_string": "hello"}
