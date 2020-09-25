from xeger import Xeger
import json
from typing import Union, Dict, Callable
from pathlib import Path


def create_from(schema: Union[dict, str, Path]):
    schema: dict
    if isinstance(schema, Path):
        schema = json.loads(schema.read_text())
    elif isinstance(schema, str):
        try:
            schema = json.loads(schema)
        except json.decoder.JSONDecodeError:
            path = Path(schema)
            if path.is_file():
                schema = json.loads(path.read_text())

    obj = {}
    properties = schema.get("properties", {})
    for p in properties:
        prop: dict = properties[p]
        obj[p] = _get_default(name=p, prop=prop, schema=schema)
    return obj


def _get_default(name: str, prop: dict, schema: dict):
    ref = prop.get("$ref")
    prop_type = prop.get("type", None)
    if not ref:
        if isinstance(prop_type, list):
            prop_type = prop_type[0]
        if prop_type not in __generators:
            raise RuntimeError(f"Property '{name}' has an invalid type: {prop_type}")

    default = prop.get("default")
    if default is None:
        if ref:
            default = _create_ref(name=ref, schema=schema)
        else:
            generator = __generators[prop_type]
            enum = prop.get("enum")
            if enum:
                default = enum[0]
            else:
                default = generator(name, prop, schema)

    return default


def _create_string(name: str, prop: dict, schema: dict):
    min_length = prop.get("minLength", 0)
    max_length = prop.get("maxLength")
    pattern = prop.get("pattern")
    default = " " * min_length
    if pattern:
        limit = max_length if max_length else 10
        x = Xeger(limit=limit)
        default = x.xeger(pattern)
    return default


def _create_number(name: str, prop: dict, schema: dict):
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


def _create_array(name: str, prop: dict, schema: dict):
    nr_items = prop.get("minItems", 0)
    default = [_get_default(name=name, prop=prop["items"], schema=schema) for _ in range(nr_items)]
    return default


def _create_null(name: str, prop: dict, schema: dict):
    return None


def _create_boolean(name: str, prop: dict, schema: dict):
    return False


def _create_object(name: str, prop: dict, schema: dict):
    default = {}
    props = prop["properties"]
    for p in props:
        default[p] = _get_default(name=p, prop=props[p], schema=schema)
    return default


def _create_ref(name: str, schema: {}) -> any:
    is_web = name.lower().startswith("http://") or name.lower().startswith("https://")
    path: str
    file, path = name.split("#")
    if file:
        schema = json.loads(Path(file).read_text())
    elem = schema
    for path_parth in path.lstrip("/").split("/"):
        elem = elem[path_parth]
    return _get_default("", elem, schema=schema)


__generators: Dict[str, Callable[[str, dict, dict], any]] = {
    "string": _create_string,
    "integer": _create_number,
    "number": _create_number,
    "array": _create_array,
    "boolean": _create_boolean,
    "object": _create_object,
    "null": _create_null,
}
