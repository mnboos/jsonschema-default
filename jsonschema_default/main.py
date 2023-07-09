import json
import random
import string
from pathlib import Path
from typing import Union, Any
from loguru import logger

import rstr


class JsonSchemaDefault:

    def __init__(self, schema: Union[dict, str, Path]):
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

        self.schema: dict = schema

    def _string(self):
        min_length = self.schema.get("minLength", 1)
        max_length = self.schema.get("maxLength", 10)
        pattern = self.schema.get("pattern")
        default: str
        if pattern:
            default = rstr.xeger(pattern)
        else:
            default = rstr.rstr(string.ascii_letters, min_length, max_length)
        return default

    def _number(self):
        default = 0
        minimum = self.schema.get("minimum")
        maximum = self.schema.get("maximum")
        exclusive_minimum = self.schema.get("exclusiveMinimum")
        multiple_of = self.schema.get("multipleOf")

        if minimum is not None:
            default = minimum
        if maximum is not None and minimum is None:
            default = maximum
        if exclusive_minimum is not None:
            default = exclusive_minimum + 1
        if multiple_of is not None:
            default = default + (multiple_of - (default % multiple_of))
        return default

    def _array(self):
        nr_items = self.schema.get("minItems", 0)
        item_schema = self.schema.get("items", {})
        gen = JsonSchemaDefault(item_schema)
        return [gen.generate() for _ in range(nr_items)]

    def _object(self):
        default = {}
        props: dict[str, dict] = self.schema.get("properties", {})
        for name, schema in props.items():
            default[name] = JsonSchemaDefault(schema).generate()
        return default

    def from_ref(self, ref: str) -> any:
        # is_web = name.lower().startswith(("http://", "https://"))
        path: str
        file, path = ref.split("#")
        if file:
            schema = json.loads(Path(file).read_text())
        else:
            schema = self.schema
        elem = schema
        for path_parth in path.lstrip("/").split("/"):
            elem = elem[path_parth]
        ref_schema = {**elem, "definitions": schema.get("definitions")}
        return JsonSchemaDefault(ref_schema).generate()

    def generate(self):
        ref = self.schema.get("$ref")
        one_of = self.schema.get("oneOf", None)
        any_of = self.schema.get("anyOf", None)

        assert one_of is None or len(one_of)
        assert any_of is None or len(any_of)

        if ref:
            return self.from_ref(ref)
        elif one_of or any_of:
            s = one_of[0] if one_of else any_of[0]
            return JsonSchemaDefault(s).generate()

        result: Any
        if "default" in self.schema:
            result = self.schema["default"]
        elif "const" in self.schema:
            result = self.schema["const"]
        else:
            t = self.schema.get("type", "object")

            if isinstance(t, list):
                if not t:
                    raise RuntimeError("Type must not be an empty list")
                t = t[0]

            if t == "string":
                result = self._string()
            elif t == "number" or t == "integer":
                result = self._number()
            elif t == "array":
                result = self._array()
            elif t == "boolean":
                result = bool(random.randint(0, 1))
            elif t == "null":
                result = None
            elif t == "object":
                result = self._object()
            else:
                logger.warning("Schema error: {}", self.schema)
                raise RuntimeError(f"Unknown type: {t}")
        return result







