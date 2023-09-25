from . import main
from typing import Union
from pathlib import Path


class MissingError(Exception):
    def __init__(self, message: str, missing: list[str]):
        self.message = message
        self.missing = missing


def create_from(schema: Union[dict, str, Path], check_missing: bool = False) -> dict:
    obj = main.JsonSchemaDefault(schema, parent=None, check_missing=check_missing)
    result = obj.generate()

    if check_missing:
        if len(obj.missing) > 0:
            raise MissingError("Missing fields", obj.missing)

    return result
