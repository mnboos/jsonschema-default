from xeger import Xeger
import json
from typing import Union, Dict, Callable, Any
from pathlib import Path


def create_from(schema: Union[dict, str, Path]) -> dict:
    """
    Creates a default object for the specified schema
    :param schema:
    :return:
    """
    if isinstance(schema, Path):
        schema = json.loads(schema.read_text())
    elif isinstance(schema, str):
        try:
            schema = json.loads(schema)
        except json.decoder.JSONDecodeError:
            path = Path(schema)
            if path.is_file():
                schema = json.loads(path.read_text())

    schema: dict
    if schema.get("properties", None) is None and schema.get("$ref", None) is not None:
        return _get_default(name="", prop=schema, schema=schema)

    properties = schema.get("properties", {})
    obj = {p: _get_default(name=p, prop=prop, schema=schema) for p, prop in properties.items()}
    return obj


def _get_default(name: str, prop: dict, schema: dict, from_ref: bool = False) -> Any:
    """
    Main function creating the default value for a property
    :param name: The name of the property to initialize
    :param prop: The details of the property
    :param schema: The whole schema
    :return:
    """

    default = None
    if "default" in prop:
        default = prop.get("default")
    elif "const" in prop:
        default = prop.get("const")
    ref = prop.get("$ref")
    prop_type = prop.get("type", None)
    one_of = prop.get("oneOf", None)
    any_of = prop.get("anyOf", None)
    if ref and from_ref:
        raise RuntimeError("Cyclic refs are not allowed")

    if not ref:
        if isinstance(prop_type, list):
            prop_type = prop_type[0]
        elif one_of:
            assert isinstance(one_of, list), f"oneOf '{one_of}' is supposed to be a list"
            default = _get_default(name, one_of[0], schema)
        elif any_of:
            assert isinstance(any_of, list), f"anyOf '{any_of}' is supposed to be a list"
            default = _get_default(name, any_of[0], schema)
        if not one_of and not any_of and prop_type not in __generators:
            raise RuntimeError(f"Property '{name}' has an invalid type: {prop_type}")

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
    """
    Creates a default string
    :param name:
    :param prop:
    :param schema:
    :return:
    """
    min_length = prop.get("minLength", 0)
    max_length = prop.get("maxLength")
    regex_pattern = prop.get("pattern")
    default = " " * min_length
    if regex_pattern:
        limit = max_length if max_length else 10
        x = Xeger(limit=limit)
        default = x.xeger(regex_pattern)
    return default


def _create_number(name: str, prop: dict, schema: dict):
    """
    Creates a default number, respecting the following constraints (if specified in the schema)
      - minimum
      - maximum
      - exclusiveMinimum
      - multipleOf
    :param name:
    :param prop:
    :param schema:
    :return:
    """
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
    props = prop.get("properties")
    if props:
        for p in props:
            default[p] = _get_default(name=p, prop=props[p], schema=schema)
    return default


def _create_ref(name: str, schema: {}) -> any:
    # is_web = name.lower().startswith(("http://", "https://"))
    path: str
    file, path = name.split("#")
    if file:
        schema = json.loads(Path(file).read_text())
    elem = schema
    for path_parth in path.lstrip("/").split("/"):
        elem = elem[path_parth]
    ref_schema = {**elem, "definitions": schema.get("definitions")}
    return create_from(ref_schema)


__generators: Dict[str, Callable[[str, dict, dict], any]] = {
    "string": _create_string,
    "integer": _create_number,
    "number": _create_number,
    "array": _create_array,
    "boolean": _create_boolean,
    "object": _create_object,
    "null": _create_null,
}
