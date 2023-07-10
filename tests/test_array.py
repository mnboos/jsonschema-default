import jsonschema_default as js


def test_string_array():
    obj = js.create_from("./schemas/array/string.json")
    assert obj == {"array": []}


def test_string_array_with_length():
    obj = js.create_from("./schemas/array/minItems.json")
    assert len(obj["array"]) == 3


def test_array_one_of():
    obj = js.create_from("./schemas/array/oneOf.json")
    assert obj == {"array": ["foobar"]}


def test_array_any_of():
    obj = js.create_from("./schemas/array/anyOf.json")
    assert obj == {"array": ["anyof string"]}
