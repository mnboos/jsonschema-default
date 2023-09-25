import jsonschema_default as js


def test_ref_schema():
    obj = js.create_from("./schemas/ref/ref_schema.json")
    assert obj == {
        "street": "samplestreet",
        "city": "samplecity",
        "state": "samplestate",
    }


def test_ref_schema_check_missing():
    obj = js.create_from("./schemas/ref/ref_schema.json", check_missing=True)
    assert obj == {
        "street": "samplestreet",
        "city": "samplecity",
        "state": "samplestate",
    }
