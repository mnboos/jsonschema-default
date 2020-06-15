# jsonschema-instance

A Python package that creates default objects from a JSON schema.

## Note
This is not a validator. Inputs should be valid JSON schemas. For Python you can use the [jsonschema](https://github.com/Julian/jsonschema) package to validate schemas.

## Installation
```
pip install jsonschema-default
```

## Usage
```python
import jsonschema_default

default_obj = jsonschema_default.create_from("<schema>")
```

## Development
- Install and configure [Poetry](https://python-poetry.org/)

```bash
pip install --user poetry
```

See [Installation](https://python-poetry.org/docs/#installation) for the official guide.

- Install the dependencies using 

```bash
# Configure poetry to create a local venv directory
poetry config virtualenvs.in-project true

poetry install
```