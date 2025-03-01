import json
import re
from pathlib import Path

import jsonschema_default as js
from jsonschema_default import DefaultOptions


def test_min_length():
    obj = js.create_from("../schemas/string/minLength.json")
    val = obj["string"]
    min_length = 2
    assert isinstance(val, str) and len(val) >= min_length


def test_max_length():
    obj = js.create_from("../schemas/string/maxLength.json")
    val = obj["string"]
    max_length = 2
    assert isinstance(val, str) and len(val) <= max_length


def test_unbound_length():
    options = DefaultOptions(string_min_length=7, string_max_length=7)

    obj = js.create_from("../schemas/string/unbound.json", default_options=options)
    assert options.string_min_length <= len(obj["string"]) <= options.string_max_length


def test_regex():
    schema_path = "../schemas/string/regex.json"
    schema = json.loads(Path(schema_path).read_text())
    obj = js.create_from(schema_path)
    result_string = obj["string"]
    pattern = schema["properties"]["string"]["pattern"]
    assert re.fullmatch(pattern=pattern, string=result_string), (
        f"Pattern '{pattern}' does not match string: {result_string}"
    )
