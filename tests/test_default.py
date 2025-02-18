import jsonschema_default as js


def test_default():
    obj = js.create_from("./schemas/default/default.json")
    assert obj == {"number": 0}


def test_default_and_const():
    """
    If both 'default' and 'const' are defined, 'default' has higher precedence
    :return:
    """

    obj = js.create_from("./schemas/default/default_and_const.json")
    assert obj == {"number": 0}
