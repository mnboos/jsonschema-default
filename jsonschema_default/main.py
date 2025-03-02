import abc
import json
import logging
import random
import string
from pathlib import Path
from typing import Any, Optional, Union

import rstr

from jsonschema_default.errors import LoadError, RefCycleError


class DefaultOptions:
    def __init__(self, *, make_random: bool = False, string_min_length=1, string_max_length=10):
        if string_min_length < 0:
            raise ValueError("string_min_length must not be negative")
        if string_min_length > string_max_length:
            raise ValueError("string_min_length must be smaller or equal than string_max_length")

        self.make_random = make_random

        self.string_min_length = string_min_length
        self.string_max_length = string_max_length


class JsonSchemaDefault:
    def __init__(
        self,
        schema: Union[dict, str, Path],
        parent: Optional["JsonSchemaDefault"],
        from_refs: Optional[list[str]] = None,
    ):
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
                    raise LoadError(f"Schema could not be loaded from file: {path}") from e

        assert isinstance(schema, dict), f"Schema is not a dict: {schema}"
        self.schema = schema

    def root_schema(self):
        return self.parent.root_schema() if self.parent else self

    def get(self, prop: str, default=None) -> Union[Any, None]:
        return self.schema.get(prop, default)

    @property
    def ref(self):
        return self.get("$ref")

    @property
    def one_of(self):
        return self.get("oneOf")

    @property
    def any_of(self):
        return self.get("anyOf")

    @property
    def enum(self):
        return self.get("enum")

    @property
    def type(self):
        t = self.schema.get("type", "object")
        if isinstance(t, list):
            if not t:
                raise RuntimeError("Type must not be an empty list")
            t = t[0]
        return t

    @property
    def default(self):
        return self.get("default", None)

    @property
    def const(self):
        return self.get("const", None)

    def generate(self, options: Union[DefaultOptions, None] = None) -> Any:
        if options is None:
            options = DefaultOptions()

        ref = self.ref
        one_of = self.one_of
        any_of = self.any_of
        enum = self.enum

        assert one_of is None or len(one_of)
        assert any_of is None or len(any_of)
        assert enum is None or isinstance(enum, list)

        if ref:
            return RefDefault(ref=ref, schema=self, options=options).make_default()
        elif one_of or any_of:
            s = one_of[0] if one_of else any_of[0]
            return JsonSchemaDefault(s, parent=self).generate(options=options)

        result: Any
        if "default" in self.schema:
            result = self.default
        elif "const" in self.schema:
            result = self.const
        elif self.enum:
            result = self.enum[0]
        else:
            default_maker: SchemaDefaultBase
            if self.type == "string":
                default_maker = StringDefault(schema=self, options=options)
            elif self.type == "number" or self.type == "integer":
                default_maker = IntegerDefault(schema=self, options=options)
            elif self.type == "boolean":
                default_maker = BooleanDefault(schema=self, options=options)
            elif self.type == "array":
                default_maker = ArrayDefault(schema=self, options=options)
            elif self.type == "null":
                default_maker = NullDefault(schema=self, options=options)
            elif self.type == "object":
                default_maker = ObjectDefault(schema=self, options=options)
            else:
                logging.error("Schema error, unknown property type: {}", self.schema)
                raise RuntimeError(f"Schema error, unknown property type: {self.type}")

            result = default_maker.make_default()

        return result

    def fill(self, target: dict, options: DefaultOptions):
        res = self.generate(options=options)

        def assign_recursive(to: dict, src: dict) -> None:
            if isinstance(src, dict):
                for k, v in src.items():
                    to.setdefault(k, to.get(k, v))
                    child = to.get(k)
                    if isinstance(child, dict):
                        assign_recursive(to=child, src=src[k])

        assign_recursive(to=target, src=res)


class SchemaDefaultBase(abc.ABC):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        self.schema = schema
        self.options = options

    @abc.abstractmethod
    def make_default(self):
        pass


class StringDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)

    def _make(self, *, min_length: int, max_length: int):
        return (
            rstr.xeger(self.pattern)
            if self.pattern
            else rstr.rstr(alphabet=string.ascii_letters, start_range=min_length, end_range=max_length)
        )

    @property
    def min_length(self):
        return self.schema.get("minLength", self.options.string_min_length)

    @property
    def max_length(self):
        return self.schema.get("maxLength", max(self.min_length, self.options.string_max_length))

    @property
    def pattern(self):
        return self.schema.get("pattern")

    def make_default(self):
        min_length = self.min_length if self.min_length is not None else self.options.string_min_length
        max_length = self.max_length if self.max_length is not None else self.options.string_max_length
        return self._make(min_length=min_length, max_length=max_length)


class BooleanDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)

    def make_default(self):
        return bool(random.randint(0, 1))


class ArrayDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)

    @property
    def min_items(self):
        return self.schema.get("minItems", 0)

    @property
    def items(self):
        return self.schema.get("items", {})

    def make_default(self):
        nr_items = self.min_items
        item_schema = self.items
        gen = JsonSchemaDefault(item_schema, parent=self.schema)
        return [gen.generate(self.options) for _ in range(nr_items)]


class NullDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)

    def make_default(self):
        return None


class RefDefault(SchemaDefaultBase):
    def __init__(self, *, ref: str, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)
        self.ref = ref

    def make_default(self):
        if self.ref in self.schema.ref_path:
            raise RefCycleError(refs=[*self.schema.ref_path, self.ref])

        root_schema = self.schema.root_schema().schema

        # is_web = name.lower().startswith(("http://", "https://"))
        path: str
        file, path = self.ref.split("#")
        schema = json.loads(Path(file).read_text()) if file else root_schema
        elem = schema
        for path_parth in path.lstrip("/").split("/"):
            assert path_parth in elem, f"Expected key '{path_parth}' expected but not found in: {elem}"
            elem = elem[path_parth]
        ref_schema = {**elem, "definitions": root_schema.get("definitions")}
        return JsonSchemaDefault(ref_schema, parent=self.schema, from_refs=[*self.schema.ref_path, self.ref]).generate(
            self.options
        )


class ObjectDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)

    @property
    def properties(self) -> dict[str, Any]:
        return self.schema.get("properties", {})

    def make_default(self):
        default = {}
        for name, schema in self.properties.items():
            prop_schema = JsonSchemaDefault(schema=schema, parent=self.schema)
            default[name] = prop_schema.generate(options=self.options)
        return default


class IntegerDefault(SchemaDefaultBase):
    def __init__(self, *, schema: JsonSchemaDefault, options: DefaultOptions):
        super().__init__(schema=schema, options=options)
        if self.minimum is not None and self.maximum is not None and self.minimum > self.maximum:
            raise ValueError("minimum must be smaller or equal than maximum")
        if self.exclusive_minimum is not None and self.maximum is not None and self.exclusive_minimum >= self.maximum:
            raise ValueError("exclusiveMinimum must be smaller than maximum")

    @property
    def minimum(self) -> Union[int, None]:
        return self.schema.get("minimum", None)

    @property
    def maximum(self) -> Union[int, None]:
        return self.schema.get("maximum", None)

    @property
    def exclusive_minimum(self) -> Union[int, None]:
        return self.schema.get("exclusiveMinimum", None)

    @property
    def multiple_of(self) -> Union[int, None]:
        return self.schema.get("multipleOf", None)

    def make_default(self):
        default: int
        if self.minimum is not None:
            default = self.minimum
        elif self.maximum is not None and self.minimum is None:
            default = self.maximum
        elif self.exclusive_minimum is not None:
            default = self.exclusive_minimum + 1
        else:
            default = 0

        if self.multiple_of is not None:
            default = default + (self.multiple_of - (default % self.multiple_of))

        return default
