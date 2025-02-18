import json
import re
from pathlib import Path

import jsonschema_default as js


def test_min_length():
    obj = js.create_from("./schemas/string/minLength.json")
    val = obj["string"]
    min_length = 2
    assert isinstance(val, str) and len(val) >= min_length


def test_regex():
    schema_path = "./schemas/string/regex.json"
    schema = json.loads(Path(schema_path).read_text())
    obj = js.create_from(schema_path)
    result_string = obj["string"]
    pattern = schema["properties"]["string"]["pattern"]
    assert re.fullmatch(pattern=pattern, string=result_string), (
        f"Pattern '{pattern}' does not match string: {result_string}"
    )
