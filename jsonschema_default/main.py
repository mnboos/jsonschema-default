import json
import logging
import random
import string
from pathlib import Path
from typing import Any, Optional, Union

import rstr


class JsonSchemaDefault:
    def __init__(
        self,
        schema: Union[dict, str, Path],
        parent: Optional["JsonSchemaDefault"],
        from_refs: Optional[list[str]] = None,
    ):
        """
        Creates a default object for the specified schema
        :param schema:
        :return:
        """

        self.parent = parent
        self.ref_path: list[str] = from_refs if from_refs else []

        if isinstance(schema, Path):
            schema = json.loads(schema.read_text())
        elif isinstance(schema, str):
            try:
                schema = json.loads(schema)
            except json.decoder.JSONDecodeError as e:
                path = Path(schema)
                if path.is_file():
                    schema = json.loads(path.read_text())
                else:
                    raise RuntimeError(f"Schema could not be loaded from file: {path}") from e

        assert isinstance(schema, dict), f"Schema is not a dict: {schema}"
        self.schema: dict = schema

    def _string(self):
        min_length = self.schema.get("minLength", 1)
        # Make sure that the max length is at least as big as the min length
        max_length = self.schema.get("maxLength", max(min_length, 10))
        pattern = self.schema.get("pattern")
        default = rstr.xeger(pattern) if pattern else rstr.rstr(string.ascii_letters, min_length, max_length)
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
        gen = JsonSchemaDefault(item_schema, parent=self)
        return [gen.generate() for _ in range(nr_items)]

    def _object(self):
        default = {}
        props: dict[str, dict] = self.schema.get("properties", {})
        for name, schema in props.items():
            default[name] = JsonSchemaDefault(schema, parent=self).generate()
        return default

    def _root(self):
        return self.parent._root() if self.parent else self

    def ref(self, ref: str) -> any:
        if ref in self.ref_path:
            raise RuntimeError("Ref cycle detected")

        root_schema = self._root().schema

        # is_web = name.lower().startswith(("http://", "https://"))
        path: str
        file, path = ref.split("#")
        schema = json.loads(Path(file).read_text()) if file else root_schema
        elem = schema
        for path_parth in path.lstrip("/").split("/"):
            assert path_parth in elem, f"Expected key '{path_parth}' expected but not found in: {elem}"
            elem = elem[path_parth]
        ref_schema = {**elem, "definitions": root_schema.get("definitions")}
        return JsonSchemaDefault(ref_schema, parent=self, from_refs=[ref, *self.ref_path]).generate()

    def generate(self):
        ref = self.schema.get("$ref")
        one_of = self.schema.get("oneOf")
        any_of = self.schema.get("anyOf")
        enum = self.schema.get("enum")

        assert one_of is None or len(one_of)
        assert any_of is None or len(any_of)
        assert enum is None or isinstance(enum, list)

        if ref:
            return self.ref(ref)
        elif one_of or any_of:
            s = one_of[0] if one_of else any_of[0]
            return JsonSchemaDefault(s, parent=self).generate()

        result: Any
        if "default" in self.schema:
            result = self.schema["default"]
        elif "const" in self.schema:
            result = self.schema["const"]
        else:
            t = self.type()

            if enum:
                result = enum[0]
            elif t == "string":
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
                logging.warning("Schema error: {}", self.schema)
                raise RuntimeError(f"Unknown type: {t}")
        return result

    def type(self):
        t = self.schema.get("type", "object")
        if isinstance(t, list):
            if not t:
                raise RuntimeError("Type must not be an empty list")
            t = t[0]
        return t
