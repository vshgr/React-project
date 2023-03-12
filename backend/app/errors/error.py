from typing import Any, List, Literal, Optional

from pydantic import BaseModel, Field


class BaseError(BaseModel):
    type: Optional[str] = Field(...)
    message: str

    def __hash__(self):
        return hash((self.type, self.message))


class ValidationError(BaseError):
    type: Literal['fieldValidationError']
    value: Any
    field: Optional[str]

    def __hash__(self):
        return hash((self.type, self.value, self.field, self.message))


class ErrorMessage(BaseModel):
    message: str
    errors: List[BaseError]
