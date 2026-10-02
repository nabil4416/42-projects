"""Tests for the standalone prompt builder (no model download needed)."""

import json
from pathlib import Path

import pytest

from src.io_json import load_function_definitions, load_prompts
from src.models import FunctionDefinition, PromptInput
from src.prompt_builder import build_prompt


def make_function(
    name: str = "fn_send_rocket_to_mars",
    parameters: dict[str, object] | None = None,
) -> FunctionDefinition:
    """Make an unknown function to catch hard-coded assumptions."""
    return FunctionDefinition.model_validate(
        {
            "name": name,
            "description": "Launch a rocket to Mars.",
            "parameters": parameters if parameters is not None else {},
            "returns": {"type": "string"},
        }
    )


def extract_functions(prompt: str) -> list[dict[str, object]]:
    """Read the JSON definitions embedded in the prepared prompt."""
    prefix = "Functions:"
    suffix = "\nRequest:"
    encoded = prompt.split(prefix, maxsplit=1)[1].split(suffix, maxsplit=1)[0]
    result = json.loads(encoded)
    assert isinstance(result, list)
    return result


def test_supplied_definitions_are_all_included() -> None:
    definitions = load_function_definitions(
        Path("data/input/functions_definition.json")
    )
    prompt = build_prompt(definitions, PromptInput(prompt="Add two numbers"))
    included = extract_functions(prompt)
    assert len(included) == 5
    assert [item["name"] for item in included] == [
        definition.name for definition in definitions
    ]


def test_descriptions_and_parameters_are_preserved() -> None:
    function = make_function(parameters={"destination": {"type": "string"}})
    prompt = build_prompt([function], PromptInput(prompt="Launch"))
    included = extract_functions(prompt)[0]
    assert included == {
        "name": function.name,
        "description": function.description,
        "parameters": {
            "destination": {"type": "string"},
        },
    }


def test_types_and_enum_values_are_preserved() -> None:
    function = make_function(
        parameters={
            "destination": {"type": "string", "enum": ["Mars", "Venus"]},
            "crew": {"type": "integer"},
        }
    )
    prompt = build_prompt([function], PromptInput(prompt="Go to Mars"))
    parameters = extract_functions(prompt)[0]["parameters"]
    assert parameters == {
        "destination": {"type": "string", "enum": ["Mars", "Venus"]},
        "crew": {"type": "integer"},
    }


def test_request_is_preserved_exactly() -> None:
    request = 'Launch "Ariane"\nvers Mars 🚀'
    prompt = build_prompt([make_function()], PromptInput(prompt=request))
    encoded = (
        prompt.split("Request:", maxsplit=1)[1]
        .strip()
    )
    assert json.loads(encoded) == request


def test_unknown_function_is_supported() -> None:
    function = make_function()
    prompt = build_prompt([function], PromptInput(prompt="Launch to Mars"))
    assert extract_functions(prompt)[0]["name"] == "fn_send_rocket_to_mars"


def test_function_without_parameters_is_supported() -> None:
    prompt = build_prompt([make_function()], PromptInput(prompt="Launch"))
    assert extract_functions(prompt)[0]["parameters"] == {}


def test_multiple_functions_remain_distinct() -> None:
    first = make_function("fn_launch")
    second = make_function("fn_land", {"planet": {"type": "string"}})
    prompt = build_prompt([first, second], PromptInput(prompt="Land on Mars"))
    assert [item["name"] for item in extract_functions(prompt)] == [
        "fn_launch", "fn_land"
    ]


def test_instructions_specify_internal_output_contract() -> None:
    prompt = build_prompt([make_function()], PromptInput(prompt="Launch"))
    assert '{"fn_name":"name","args":{...}}' in prompt
    assert "No prose or Markdown" in prompt


def test_regex_instruction_is_added_from_parameter_name() -> None:
    function = make_function(
        parameters={"regex": {"type": "string"}}
    )
    prompt = build_prompt([function], PromptInput(prompt="Replace"))

    assert "bare pattern without / delimiters" in prompt
    assert "prefer [0-9]+" in prompt


def test_regex_instruction_is_omitted_when_irrelevant() -> None:
    prompt = build_prompt([make_function()], PromptInput(prompt="Launch"))

    assert "bare pattern without / delimiters" not in prompt


def test_empty_request_is_preserved_for_downstream_handling() -> None:
    prompt = build_prompt([make_function()], PromptInput(prompt=""))
    assert prompt.endswith('Request:""\n')


def test_return_schema_is_omitted_as_irrelevant_to_call() -> None:
    prompt = build_prompt([make_function()], PromptInput(prompt="Launch"))

    assert '"returns"' not in prompt


def test_supplied_prompt_stays_compact() -> None:
    definitions = load_function_definitions(
        Path("data/input/functions_definition.json")
    )
    prompt = build_prompt(
        definitions,
        PromptInput(prompt="What is the sum of 265 and 345?"),
    )

    assert len(prompt) < 1200
    assert len(prompt.splitlines()) == 3


def test_no_functions_raises_clear_error() -> None:
    with pytest.raises(ValueError, match="without function definitions"):
        build_prompt([], PromptInput(prompt="Launch"))


def test_duplicate_function_names_raise_clear_error() -> None:
    function = make_function()
    with pytest.raises(ValueError, match="duplicate function names"):
        build_prompt([function, function], PromptInput(prompt="Launch"))


def test_builder_has_no_side_effect_on_inputs() -> None:
    function = make_function(parameters={"crew": {"type": "integer"}})
    original = function.model_dump(mode="json")
    build_prompt([function], PromptInput(prompt="Launch"))
    assert function.model_dump(mode="json") == original


def test_all_supplied_prompts_can_be_built() -> None:
    definitions = load_function_definitions(
        Path("data/input/functions_definition.json")
    )
    requests = load_prompts(Path("data/input/function_calling_tests.json"))
    prompts = [build_prompt(definitions, request) for request in requests]
    assert len(prompts) == 11
    assert all("Functions:" in item for item in prompts)
