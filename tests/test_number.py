import jsonschema_default as js


def test_minimum():
    obj = js.create_from("./schemas/number/min.json")
    assert obj == {"number": 10, "integer": 1337}


def test_multipleof():
    obj = js.create_from("./schemas/number/multipleOf.json")
    assert obj == {"number": 11}


def test_negative_maximum():
    obj = js.create_from("./schemas/number/negative_max.json")
    assert obj == {"number": -10}


def test_default():
    obj = js.create_from("./schemas/number/default.json")
    assert obj == 0
