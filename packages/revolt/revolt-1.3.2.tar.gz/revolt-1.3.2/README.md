# revolt

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/revolt/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/revolt)
[![PyPI](https://img.shields.io/pypi/v/revolt.svg?style=flat-square)](https://pypi.python.org/pypi/revolt/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/revolt?style=flat-square)](https://pypi.python.org/pypi/revolt/)
[![Python Version](https://img.shields.io/pypi/pyversions/revolt.svg?style=flat-square)](https://pypi.python.org/pypi/revolt/)

Value substitutor for [district42](https://github.com/nikitanovosibirsk/district42) schema

(!) Work in progress, breaking changes are possible until v2.0 is released

## Installation

```sh
pip3 install revolt
```

## Usage

```python
from district42 import schema
from revolt import substitute

UserSchema = schema.dict({
    "id": schema.int,
    "name": schema.str | schema.none,
    "id_deleted": schema.bool,
})

substituted = substitute(UserSchema, {"id": 1, "name": "Bob"})

# syntax sugar
substituted = UserSchema % {"id": 1, "name": "Bob"}
```
