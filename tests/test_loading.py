import json
import re
from pathlib import Path

import pytest

import jsonschema_default as js
from jsonschema_default.errors import LoadError


def test_load_from_path():
    js.create_from(Path("../schemas/string/minLength.json"))


def test_inexisting_file():
    with pytest.raises(LoadError):
        js.create_from("../thisschemadoesnotexist.json")
