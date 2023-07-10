from . import main
from typing import Union
from pathlib import Path


def create_from(schema: Union[dict, str, Path]) -> dict:
    return main.JsonSchemaDefault(schema, parent=None).generate()
