# JSON Schema Default Generator

Create default objects from jsonschema specifications.

## Installation

```bash
pip install jsonschema_default
```

## Quick Start

```python
from jsonschema_default import create_from

# Your schema can define any level of complexity
schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string", "minLength": 3},
        "age": {"type": "integer", "minimum": 0},
        "email": {"type": "string", "pattern": r"[a-z]+@[a-z]+\.[a-z]+"}
    }
}

# Generate a default object matching your schema
default_object = create_from(schema)
# Output: {'name': 'abc', 'age': 0, 'email': 'example@domain.com'}

# You can also load schemas from files
from pathlib import Path
default_object = create_from(Path("schema.json"))
```

## Feature Support


| Feature Category       | Feature            | Status | Notes                                     |
|------------------------|--------------------|--------|-------------------------------------------|
| **Basic Types**        | `string`           | ✅      | Including length and pattern constraints  |
|                        | `number`/`integer` | ✅      | With range and multiple constraints       |
|                        | `boolean`          | ✅      | Random true/false generation              |
|                        | `array`            | ✅      | Creates arrays with defined item schemas  |
|                        | `object`           | ✅      | Generates nested object structures        |
|                        | `null`             | ✅      |                                           |
| **String Generation**  | `minLength`        | ✅      | Ensures minimum string length             |
|                        | `maxLength`        | ✅      | Limits maximum string length              |
|                        | `pattern`          | ✅      | Generates strings matching regex patterns |
| **Number Generation**  | `minimum`          | ✅      | Sets lower bound                          |
|                        | `maximum`          | ✅      | Sets upper bound                          |
|                        | `exclusiveMinimum` | ✅      | Generates values above minimum            |
|                        | `multipleOf`       | ✅      | Ensures values are multiples              |
| **Array Generation**   | `minItems`         | ✅      | Creates arrays with minimum length        |
|                        | `items`            | ✅      | Applies schema to generate array items    |
| **Schema Composition** | `oneOf`            | ✅      | Uses first schema option                  |
|                        | `anyOf`            | ✅      | Uses first schema option                  |
| **References**         | Local `$ref`       | ✅      | Supports file and definition references   |
| **Default Values**     | `default`          | ✅      | Uses explicit default if provided         |
|                        | `const`            | ✅      | Uses constant value                       |
|                        | `enum`             | ✅      | Uses first enum option                    |

### Complete Feature Overview

This table shows all JSON Schema features and their status in our implementation:

| Feature Category        | Feature               | Status | Notes                             |
|-------------------------|-----------------------|--------|-----------------------------------|
| **Core Functionality**  | Type Generation       | ✅      | All basic JSON types supported    |
|                         | Default Values        | ✅      | Explicit defaults take precedence |
|                         | Constants             | ✅      | Const values are preserved        |
|                         | Enumerations          | ✅      | First enum value is used          |
| **String Constraints**  | Pattern Matching      | ✅      | Generates matching strings        |
|                         | Length Limits         | ✅      | Both min and max enforced         |
|                         | Format                | 🟡️    | Not required for defaults         |
| **Numeric Constraints** | Range Limits          | ✅      | Both inclusive and exclusive      |
|                         | Multiple Of           | ✅      | Ensures value divisibility        |
| **Object Features**     | Properties            | ✅      | Generates all defined properties  |
|                         | Additional Properties | 🟡️️️️ |                                   |
|                         | Pattern Properties    | 🟡️    |                                   |
|                         | Dependencies          | 🟡️    |                                   |
| **Array Features**      | Item Schema           | ✅      | Applied to all items              |
|                         | Tuple Validation      | 🟡️    |                                   |
|                         | Unique Items          | 🟡️    |                                   |
| **Composition**         | AllOf                 | 🟡️    |                                   |
|                         | AnyOf                 | ✅      | Uses first option                 |
|                         | OneOf                 | ✅      | Uses first option                 |
|                         | Not                   | 🟡     |                                   |
| **References**          | Local                 | ✅      | File and definition refs          |
|                         | Remote                | ❌      | Not supported                     |

🟡 This features is not needed to create a default object for a given schema.