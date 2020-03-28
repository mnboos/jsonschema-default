import jsonschema_instance as js


def test_array():
    obj = js.create_from("./schemas/array/string.json")
    assert obj == {"array": [""]}
