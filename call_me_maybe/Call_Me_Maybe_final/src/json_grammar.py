"""Prefix-aware canonical JSON grammar for function calls."""

import json
import string
from enum import Enum
from math import isfinite

from pydantic import BaseModel, ConfigDict, field_validator

from src.models import FunctionDefinition, ParameterDefinition, ValueType


class _MatchStatus(str, Enum):
    """Internal result of matching text against the grammar."""

    INVALID = "invalid"
    INCOMPLETE = "incomplete"
    COMPLETE = "complete"


class FunctionCallGrammar(BaseModel):
    """Validate complete calls and prefixes of canonical function JSON."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    definitions: tuple[FunctionDefinition, ...]

    @field_validator("definitions")
    @classmethod
    def validate_definitions(
        cls,
        definitions: tuple[FunctionDefinition, ...],
    ) -> tuple[FunctionDefinition, ...]:
        """Reject unusable function sets and invalid enum declarations."""
        if not definitions:
            raise ValueError("at least one function definition is required")

        names = [definition.name for definition in definitions]
        if len(names) != len(set(names)):
            raise ValueError("function names must be unique")

        for definition in definitions:
            for parameter_name, parameter in definition.parameters.items():
                cls._validate_enum(
                    definition.name,
                    parameter_name,
                    parameter,
                )
        return definitions

    def is_valid_prefix(self, text: str) -> bool:
        """Return whether ``text`` can still become one valid call."""
        return self._status(text) is not _MatchStatus.INVALID

    def is_complete(self, text: str) -> bool:
        """Return whether ``text`` is exactly one valid canonical call."""
        return self._status(text) is _MatchStatus.COMPLETE

    def forced_continuation(self, text: str) -> str:
        """Return characters that have exactly one grammar-valid path.

        The returned text stops before the first real choice. It is therefore
        safe for the decoder to append it without requesting model logits.
        """
        if not self.is_valid_prefix(text) or self.is_complete(text):
            return ""

        candidates = self._candidate_characters()
        current = text
        continuation: list[str] = []
        while not self.is_complete(current):
            valid = [
                character
                for character in candidates
                if self.is_valid_prefix(current + character)
            ]
            if len(valid) != 1:
                break
            continuation.append(valid[0])
            current += valid[0]
        return "".join(continuation)

    def _candidate_characters(self) -> tuple[str, ...]:
        """Build characters covering JSON syntax and declared literals."""
        characters = set(string.printable)
        for definition in self.definitions:
            characters.update(self._json_literal(definition.name))
            for parameter_name, parameter in definition.parameters.items():
                characters.update(self._json_literal(parameter_name))
                for value in parameter.allowed_values or []:
                    characters.update(self._json_literal(value))
        return tuple(sorted(characters))

    def _status(self, text: str) -> _MatchStatus:
        """Match text against every available function definition."""
        statuses = {
            self._match_definition(text, definition)
            for definition in self.definitions
        }
        if _MatchStatus.COMPLETE in statuses:
            return _MatchStatus.COMPLETE
        if _MatchStatus.INCOMPLETE in statuses:
            return _MatchStatus.INCOMPLETE
        return _MatchStatus.INVALID

    @classmethod
    def _match_definition(
        cls,
        text: str,
        definition: FunctionDefinition,
    ) -> _MatchStatus:
        """Match text against the canonical call for one function."""
        position, incomplete = cls._consume_literal(
            text,
            0,
            '{"fn_name":' + cls._json_literal(definition.name),
        )
        if incomplete:
            return _MatchStatus.INCOMPLETE
        if position is None:
            return _MatchStatus.INVALID

        position, incomplete = cls._consume_literal(
            text,
            position,
            ',"args":{',
        )
        if incomplete:
            return _MatchStatus.INCOMPLETE
        if position is None:
            return _MatchStatus.INVALID

        parameters = tuple(definition.parameters.items())
        return cls._match_arguments(text, position, parameters, 0)

    @classmethod
    def _match_arguments(
        cls,
        text: str,
        position: int,
        parameters: tuple[tuple[str, ParameterDefinition], ...],
        index: int,
    ) -> _MatchStatus:
        """Match ordered arguments recursively after the args opening."""
        if index == len(parameters):
            end_position, incomplete = cls._consume_literal(
                text,
                position,
                "}}",
            )
            if incomplete:
                return _MatchStatus.INCOMPLETE
            if end_position == len(text):
                return _MatchStatus.COMPLETE
            return _MatchStatus.INVALID

        parameter_name, parameter = parameters[index]
        separator = "" if index == 0 else ","
        argument_literal = (
            separator + cls._json_literal(parameter_name) + ":"
        )
        value_position, incomplete = cls._consume_literal(
            text,
            position,
            argument_literal,
        )
        if incomplete:
            return _MatchStatus.INCOMPLETE
        if value_position is None:
            return _MatchStatus.INVALID

        completed_positions, value_incomplete = cls._match_value(
            text,
            value_position,
            parameter,
        )
        statuses = {
            cls._match_arguments(
                text,
                completed_position,
                parameters,
                index + 1,
            )
            for completed_position in completed_positions
        }
        if _MatchStatus.COMPLETE in statuses:
            return _MatchStatus.COMPLETE
        if value_incomplete or _MatchStatus.INCOMPLETE in statuses:
            return _MatchStatus.INCOMPLETE
        return _MatchStatus.INVALID

    @classmethod
    def _match_value(
        cls,
        text: str,
        position: int,
        parameter: ParameterDefinition,
    ) -> tuple[set[int], bool]:
        """Return completed value positions and any valid partial match."""
        if parameter.allowed_values is not None:
            return cls._match_enum(
                text,
                position,
                parameter.allowed_values,
            )
        if parameter.type is ValueType.STRING:
            return cls._match_string(text, position)
        if parameter.type is ValueType.NUMBER:
            return cls._match_number(text, position, integer_only=False)
        if parameter.type is ValueType.INTEGER:
            return cls._match_number(text, position, integer_only=True)
        if parameter.type is ValueType.BOOLEAN:
            return cls._match_literals(text, position, ("true", "false"))
        return cls._match_literals(text, position, ("null",))

    @classmethod
    def _match_enum(
        cls,
        text: str,
        position: int,
        allowed_values: list[object],
    ) -> tuple[set[int], bool]:
        """Match one of the finite JSON enum representations."""
        literals = tuple(
            cls._json_literal(value) for value in allowed_values
        )
        return cls._match_literals(text, position, literals)

    @classmethod
    def _match_literals(
        cls,
        text: str,
        position: int,
        literals: tuple[str, ...],
    ) -> tuple[set[int], bool]:
        """Match one of several fixed literals at one position."""
        completed_positions: set[int] = set()
        has_incomplete = False
        for literal in literals:
            end_position, incomplete = cls._consume_literal(
                text,
                position,
                literal,
            )
            if end_position is not None:
                completed_positions.add(end_position)
            has_incomplete = has_incomplete or incomplete
        return completed_positions, has_incomplete

    @staticmethod
    def _match_string(text: str, position: int) -> tuple[set[int], bool]:
        """Match a JSON string, including escapes and partial escapes."""
        if position == len(text):
            return set(), True
        if text[position] != '"':
            return set(), False

        cursor = position + 1
        while cursor < len(text):
            character = text[cursor]
            if character == '"':
                return {cursor + 1}, False
            if ord(character) < 0x20:
                return set(), False
            if character != "\\":
                cursor += 1
                continue

            cursor += 1
            if cursor == len(text):
                return set(), True
            escape = text[cursor]
            if escape in '"\\/bfnrt':
                cursor += 1
                continue
            if escape != "u":
                return set(), False

            available = text[cursor + 1:cursor + 5]
            if any(character not in "0123456789abcdefABCDEF"
                   for character in available):
                return set(), False
            if len(available) < 4:
                return set(), True
            cursor += 5
        return set(), True

    @classmethod
    def _match_number(
        cls,
        text: str,
        position: int,
        *,
        integer_only: bool,
    ) -> tuple[set[int], bool]:
        """Match a JSON number or a prefix that may become one."""
        cursor = position
        while cursor < len(text) and text[cursor] not in ",}":
            cursor += 1

        number_text = text[position:cursor]
        state = cls._number_state(number_text, integer_only=integer_only)
        if state is _MatchStatus.INVALID:
            return set(), False
        if state is _MatchStatus.INCOMPLETE:
            if cursor == len(text):
                return set(), True
            return set(), False
        return {cursor}, False

    @staticmethod
    def _number_state(
        value: str,
        *,
        integer_only: bool,
    ) -> _MatchStatus:
        """Run a small deterministic automaton for JSON numbers."""
        state = "start"
        for character in value:
            if state == "start":
                if character == "-":
                    state = "sign"
                elif character == "0":
                    state = "zero"
                elif character in "123456789":
                    state = "integer"
                else:
                    return _MatchStatus.INVALID
            elif state == "sign":
                if character == "0":
                    state = "zero"
                elif character in "123456789":
                    state = "integer"
                else:
                    return _MatchStatus.INVALID
            elif state == "zero":
                if not integer_only and character == ".":
                    state = "dot"
                elif not integer_only and character in "eE":
                    state = "exponent"
                else:
                    return _MatchStatus.INVALID
            elif state == "integer":
                if character in "0123456789":
                    continue
                if not integer_only and character == ".":
                    state = "dot"
                elif not integer_only and character in "eE":
                    state = "exponent"
                else:
                    return _MatchStatus.INVALID
            elif state == "dot":
                if character in "0123456789":
                    state = "fraction"
                else:
                    return _MatchStatus.INVALID
            elif state == "fraction":
                if character in "0123456789":
                    continue
                if character in "eE":
                    state = "exponent"
                else:
                    return _MatchStatus.INVALID
            elif state == "exponent":
                if character in "+-":
                    state = "exponent_sign"
                elif character in "0123456789":
                    state = "exponent_digits"
                else:
                    return _MatchStatus.INVALID
            elif state == "exponent_sign":
                if character in "0123456789":
                    state = "exponent_digits"
                else:
                    return _MatchStatus.INVALID
            elif state == "exponent_digits":
                if character not in "0123456789":
                    return _MatchStatus.INVALID

        if state in {"zero", "integer", "fraction", "exponent_digits"}:
            return _MatchStatus.COMPLETE
        return _MatchStatus.INCOMPLETE

    @staticmethod
    def _consume_literal(
        text: str,
        position: int,
        literal: str,
    ) -> tuple[int | None, bool]:
        """Consume a literal or report a valid truncated prefix."""
        remaining = text[position:]
        if len(remaining) < len(literal):
            return None, literal.startswith(remaining)
        if remaining.startswith(literal):
            return position + len(literal), False
        return None, False

    @staticmethod
    def _json_literal(value: object) -> str:
        """Serialize one canonical compact JSON literal."""
        return json.dumps(
            value,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        )

    @classmethod
    def _validate_enum(
        cls,
        function_name: str,
        parameter_name: str,
        parameter: ParameterDefinition,
    ) -> None:
        """Ensure every enum value agrees with its declared JSON type."""
        if parameter.allowed_values is None:
            return
        if not parameter.allowed_values:
            raise ValueError(
                f"enum for {function_name}.{parameter_name} must not be empty"
            )
        for value in parameter.allowed_values:
            if not cls._matches_type(value, parameter.type):
                raise ValueError(
                    f"enum value for {function_name}.{parameter_name} "
                    f"does not match type {parameter.type.value}"
                )

    @staticmethod
    def _matches_type(value: object, value_type: ValueType) -> bool:
        """Return whether a Python enum value represents the JSON type."""
        if value_type is ValueType.STRING:
            return isinstance(value, str)
        if value_type is ValueType.INTEGER:
            return isinstance(value, int) and not isinstance(value, bool)
        if value_type is ValueType.NUMBER:
            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return False
            return not isinstance(value, float) or isfinite(value)
        if value_type is ValueType.BOOLEAN:
            return isinstance(value, bool)
        return value is None
