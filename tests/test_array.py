import jsonschema_default as js


def test_string_array():
    obj = js.create_from("./schemas/array/string.json")
    assert obj == {"array": []}


def test_string_array_with_length():
    obj = js.create_from("./schemas/array/minItems.json")
    assert obj == {"array": ["", "", ""]}
