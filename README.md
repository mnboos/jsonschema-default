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