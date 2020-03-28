import json
from typing import Union
from pathlib import Path


__valid_types = {
    "string",
    "number",
    "object",
    "array",
    "boolean",
    "null",
}


def create_from(schema: Union[str, Path]):
    schema: dict
    if isinstance(schema, Path):
        schema = json.loads(schema.read_text())
    elif isinstance(schema, str):
        path = Path(schema)
        if path.is_file():
            schema = json.loads(path.read_text())
        else:
            schema = json.loads(schema)

    obj = {}
    properties = schema.get("properties", {})
    for p in properties:
        prop: dict = properties[p]
        obj[p] = _get_default(name=p, prop=prop)
    return obj


def _get_default(name: str, prop: dict):
    prop_type = prop.get("type", None)
    if prop_type not in __valid_types:
        raise RuntimeError(f"Property '{name}' has an invalid type: {prop_type}")

    if prop_type == "string":
        min_length = prop.get("minLength", 0)
        return " " * min_length
    elif prop_type == "number":
        default = 0
        minimum = prop.get("minimum")
        maximum = prop.get("maximum")
        exclusive_minimum = prop.get("exclusiveMinimum")
        multiple_of = prop.get("multipleOf")
        if minimum is not None:
            default = minimum
        if maximum is not None and minimum is None:
            default = maximum
        if exclusive_minimum is not None:
            default = exclusive_minimum + 1
        if multiple_of is not None:
            default = default + (multiple_of - (default % multiple_of))
        return default
    elif prop_type == "array":
        nr_items = prop.get("minItems", 1)
        items = [_get_default(name=name, prop=prop["items"]) for _ in range(nr_items)]
        return items

    elif prop_type == "boolean":
        return False
    elif prop_type == "null":
        return None
    elif prop_type == "object":
        val = {}
        props = prop["properties"]
        for p in props:
            val[p] = _get_default(name=p, prop=props[p])
        return val
