from pathlib import Path
from typing import Union

from . import main
from .options import DefaultOptions


def create_from(schema: Union[dict, str, Path], default_options: DefaultOptions | None = None) -> dict:
    return main.JsonSchemaDefault(schema, parent=None).generate(options=default_options)
