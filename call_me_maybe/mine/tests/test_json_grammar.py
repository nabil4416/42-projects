"""Tests for the prefix-aware canonical function-call grammar."""

from typing import Any

import pytest
from pydantic import ValidationError

from src.json_grammar import FunctionCallGrammar
from src.models import FunctionDefinition


def make_definition(
    name: str,
    parameters: dict[str, dict[str, Any]],
) -> FunctionDefinition:
    """Build one validated function definition for grammar tests."""
    return FunctionDefinition.model_validate(
        {
            "name": name,
            "description": f"Description for {name}",
            "parameters": parameters,
            "returns": {"type": "string"},
        }
    )


def make_grammar(*definitions: FunctionDefinition) -> FunctionCallGrammar:
    """Build a grammar from the supplied definitions."""
    return FunctionCallGrammar(definitions=definitions)


def assert_every_prefix_is_valid(
    grammar: FunctionCallGrammar,
    complete_call: str,
) -> None:
    """Assert every truncation remains a valid grammar prefix."""
    for end in range(len(complete_call) + 1):
        assert grammar.is_valid_prefix(complete_call[:end]), end


def test_every_prefix_of_complete_call_is_valid() -> None:
    grammar = make_grammar(
        make_definition("fn_greet", {"name": {"type": "string"}})
    )
    call = '{"fn_name":"fn_greet","args":{"name":"Isaac"}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


def test_forces_shared_structure_before_function_choice() -> None:
    grammar = make_grammar(
        make_definition("fn_add", {"a": {"type": "number"}}),
        make_definition("fn_greet", {"name": {"type": "string"}}),
    )

    assert grammar.forced_continuation("") == '{"fn_name":"fn_'


def test_forcing_stops_before_free_form_value() -> None:
    grammar = make_grammar(
        make_definition("fn_greet", {"name": {"type": "string"}})
    )
    prefix = '{"fn_name":"fn_greet","args":{'

    assert grammar.forced_continuation(prefix) == '"name":"'


def test_forcing_resumes_after_string_value() -> None:
    grammar = make_grammar(
        make_definition("fn_greet", {"name": {"type": "string"}})
    )
    prefix = '{"fn_name":"fn_greet","args":{"name":"Shrek"'

    assert grammar.forced_continuation(prefix) == "}}"


def test_complete_or_invalid_text_has_no_forced_continuation() -> None:
    grammar = make_grammar(make_definition("fn_ping", {}))
    complete = '{"fn_name":"fn_ping","args":{}}'

    assert grammar.forced_continuation(complete) == ""
    assert grammar.forced_continuation("invalid") == ""


def test_complete_call_rejects_extra_text() -> None:
    grammar = make_grammar(make_definition("fn_ping", {}))
    call = '{"fn_name":"fn_ping","args":{}}'

    assert grammar.is_complete(call)
    assert not grammar.is_valid_prefix(call + " trailing")
    assert not grammar.is_complete(call + "\n")


@pytest.mark.parametrize(
    "invalid_call",
    [
        ' {"fn_name":"fn_ping","args":{}}',
        '{"name":"fn_ping","args":{}}',
        '{"fn_name":"fn_unknown","args":{}}',
        '{"fn_name":"fn_ping", "args":{}}',
    ],
)
def test_rejects_noncanonical_structure(invalid_call: str) -> None:
    grammar = make_grammar(make_definition("fn_ping", {}))

    assert not grammar.is_valid_prefix(invalid_call)


def test_function_definitions_are_not_hard_coded() -> None:
    grammar = make_grammar(make_definition("fn_launch_rocket", {}))
    call = '{"fn_name":"fn_launch_rocket","args":{}}'

    assert grammar.is_complete(call)


def test_argument_order_is_canonical() -> None:
    grammar = make_grammar(
        make_definition(
            "fn_add",
            {"a": {"type": "integer"}, "b": {"type": "integer"}},
        )
    )
    canonical = '{"fn_name":"fn_add","args":{"a":1,"b":2}}'
    reversed_arguments = '{"fn_name":"fn_add","args":{"b":2,"a":1}}'

    assert grammar.is_complete(canonical)
    assert not grammar.is_valid_prefix(reversed_arguments)


@pytest.mark.parametrize(
    "value",
    [
        '""',
        '"plain text"',
        '"quote: \\""',
        '"backslash: \\\\"',
        '"café"',
        '"unicode: \\u263A"',
    ],
)
def test_accepts_json_strings(value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_text", {"value": {"type": "string"}})
    )
    call = f'{{"fn_name":"fn_text","args":{{"value":{value}}}}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


@pytest.mark.parametrize(
    "value",
    ['"bad\\x"', '"line\nbreak"', '42', '"unterminated}}'],
)
def test_rejects_invalid_strings(value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_text", {"value": {"type": "string"}})
    )
    call = f'{{"fn_name":"fn_text","args":{{"value":{value}}}}}'

    assert not grammar.is_complete(call)


def test_partial_unicode_escape_remains_valid_prefix() -> None:
    grammar = make_grammar(
        make_definition("fn_text", {"value": {"type": "string"}})
    )
    prefix = '{"fn_name":"fn_text","args":{"value":"\\u26'

    assert grammar.is_valid_prefix(prefix)
    assert not grammar.is_complete(prefix)


@pytest.mark.parametrize(
    "value",
    ["0", "-1", "42", "3.14", "-0.25", "1e3", "1E-2", "999999999999999999999"],
)
def test_accepts_json_numbers(value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_number", {"value": {"type": "number"}})
    )
    call = f'{{"fn_name":"fn_number","args":{{"value":{value}}}}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


@pytest.mark.parametrize(
    "value",
    ["01", "+1", ".5", "--1", "1.", "1e", "1e+", "1٢"],
)
def test_rejects_invalid_complete_numbers(value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_number", {"value": {"type": "number"}})
    )
    call = f'{{"fn_name":"fn_number","args":{{"value":{value}}}}}'

    assert not grammar.is_complete(call)


@pytest.mark.parametrize("partial_value", ["-", "1.", "1e", "1e+"])
def test_accepts_recoverable_number_prefixes(partial_value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_number", {"value": {"type": "number"}})
    )
    prefix = (
        '{"fn_name":"fn_number","args":{"value":'
        + partial_value
    )

    assert grammar.is_valid_prefix(prefix)
    assert not grammar.is_complete(prefix)


def test_integer_rejects_decimal_number() -> None:
    grammar = make_grammar(
        make_definition("fn_integer", {"value": {"type": "integer"}})
    )
    integer_call = '{"fn_name":"fn_integer","args":{"value":-42}}'
    decimal_call = '{"fn_name":"fn_integer","args":{"value":4.2}}'

    assert grammar.is_complete(integer_call)
    assert not grammar.is_valid_prefix(decimal_call)


@pytest.mark.parametrize("value", ["true", "false"])
def test_accepts_booleans(value: str) -> None:
    grammar = make_grammar(
        make_definition("fn_flag", {"enabled": {"type": "boolean"}})
    )
    call = f'{{"fn_name":"fn_flag","args":{{"enabled":{value}}}}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


def test_accepts_null() -> None:
    grammar = make_grammar(
        make_definition("fn_null", {"value": {"type": "null"}})
    )
    call = '{"fn_name":"fn_null","args":{"value":null}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


@pytest.mark.parametrize("value", ['"fast"', '"safe"'])
def test_accepts_declared_enum_values(value: str) -> None:
    grammar = make_grammar(
        make_definition(
            "fn_mode",
            {"mode": {"type": "string", "enum": ["fast", "safe"]}},
        )
    )
    call = f'{{"fn_name":"fn_mode","args":{{"mode":{value}}}}}'

    assert_every_prefix_is_valid(grammar, call)
    assert grammar.is_complete(call)


def test_rejects_value_outside_enum() -> None:
    grammar = make_grammar(
        make_definition(
            "fn_mode",
            {"mode": {"type": "string", "enum": ["fast", "safe"]}},
        )
    )
    call = '{"fn_name":"fn_mode","args":{"mode":"slow"}}'

    assert not grammar.is_valid_prefix(call)


def test_rejects_missing_and_additional_arguments() -> None:
    grammar = make_grammar(
        make_definition("fn_greet", {"name": {"type": "string"}})
    )
    missing = '{"fn_name":"fn_greet","args":{}}'
    additional = (
        '{"fn_name":"fn_greet","args":{'
        '"name":"Isaac","extra":true}}'
    )

    assert not grammar.is_valid_prefix(missing)
    assert not grammar.is_valid_prefix(additional)


def test_rejects_empty_definition_set() -> None:
    with pytest.raises(ValidationError, match="at least one"):
        FunctionCallGrammar(definitions=())


def test_rejects_duplicate_function_names() -> None:
    first = make_definition("fn_same", {})
    second = make_definition("fn_same", {})

    with pytest.raises(ValidationError, match="must be unique"):
        make_grammar(first, second)


@pytest.mark.parametrize(
    ("parameter_type", "enum_value"),
    [("string", 1), ("integer", True), ("boolean", "true"), ("null", 0)],
)
def test_rejects_enum_value_with_wrong_type(
    parameter_type: str,
    enum_value: object,
) -> None:
    definition = make_definition(
        "fn_bad_enum",
        {"value": {"type": parameter_type, "enum": [enum_value]}},
    )

    with pytest.raises(ValidationError, match="does not match type"):
        make_grammar(definition)
