import json
import jsonschema_default as js
from pathlib import Path
import re


def test_min_length():
    obj = js.create_from("./schemas/string/minLength.json")
    assert obj == {"string": "  "}


def test_regex():
    schema_path = "./schemas/string/regex.json"
    schema = json.loads(Path(schema_path).read_text())
    obj = js.create_from(schema_path)
    result_string = obj["string"]
    pattern = schema["properties"]["string"]["pattern"]
    assert re.fullmatch(
        pattern=pattern, string=result_string
    ), f"Pattern '{pattern}' does not match string: {result_string}"
