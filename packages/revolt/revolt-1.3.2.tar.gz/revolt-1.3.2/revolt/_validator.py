from typing import Any

from district42.types import DictSchema
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator
from valera.errors import MissingKeyValidationError

__all__ = ("SubstitutorValidator",)


class SubstitutorValidator(Validator):
    def visit_dict(self, schema: DictSchema, *,
                   value: Any = Nil, path: Nilable[PathHolder] = Nil,
                   **kwargs: Any) -> ValidationResult:
        result = super().visit_dict(schema, value=value, path=path, **kwargs)
        errors = [e for e in result.get_errors() if not isinstance(e, MissingKeyValidationError)]
        return ValidationResult(errors)
