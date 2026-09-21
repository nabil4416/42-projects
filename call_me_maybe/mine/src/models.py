"""Validated data models for project inputs and internal results."""

from enum import Enum
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ValueType(str, Enum):
    """Parameter types supported by the function schema."""

    STRING = "string"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    NULL = "null"


class StrictModel(BaseModel):
    """Base model rejecting fields not declared by the schema."""

    model_config = ConfigDict(extra="forbid")


class ParameterDefinition(StrictModel):
    """Describe one function parameter."""

    type: ValueType
    allowed_values: list[Any] | None = Field(default=None, alias="enum")


class ReturnDefinition(StrictModel):
    """Describe a function return value."""

    type: ValueType


class FunctionDefinition(StrictModel):
    """Describe one callable function exposed to the LLM."""

    name: str
    description: str
    parameters: dict[str, ParameterDefinition]
    returns: ReturnDefinition

    @field_validator("name", "description")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        """Reject empty or whitespace-only identifiers and descriptions."""
        if not value.strip():
            raise ValueError("must not be empty")
        return value

    @field_validator("parameters")
    @classmethod
    def reject_blank_parameter_names(
        cls,
        value: dict[str, ParameterDefinition],
    ) -> dict[str, ParameterDefinition]:
        """Reject empty parameter names."""
        if any(not name.strip() for name in value):
            raise ValueError("parameter names must not be empty")
        return value


class PromptInput(StrictModel):
    """Represent one natural-language request."""

    prompt: str


class FunctionCall(StrictModel):
    """Represent an internal function call before output serialization."""

    name: str
    parameters: dict[str, Any]


class OutputEntry(StrictModel):
    """Represent one result using the subject's current output contract."""

    prompt: str
    name: str
    parameters: dict[str, Any]
