from pathlib import Path
from typing import Union

from . import main


def create_from(schema: Union[dict, str, Path]) -> dict:
    return main.JsonSchemaDefault(schema, parent=None).generate()
