from pathlib import Path
from typing import Union

from . import main
from .main import DefaultOptions


def create_from(schema: Union[dict, str, Path], default_options: Union[DefaultOptions, None] = None) -> dict:
    return main.JsonSchemaDefault(schema, parent=None).generate(options=default_options)


def fill_from(
    schema: Union[dict, str, Path], target: dict, default_options: Union[DefaultOptions, None] = None
) -> None:
    main.JsonSchemaDefault(schema, parent=None).fill(target=target, options=default_options)
