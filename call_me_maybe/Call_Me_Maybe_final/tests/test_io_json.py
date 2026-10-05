"""Tests for input parsing and validation."""

import json
from pathlib import Path

import pytest

from src.errors import InputFileError
from src.io_json import load_function_definitions, load_prompts, write_results
from src.models import OutputEntry


def write_json(path: Path, value: object) -> None:
    """Write a JSON fixture used by a test."""
    path.write_text(json.dumps(value), encoding="utf-8")


def test_loads_supplied_prompts() -> None:
    """Load all prompt fixtures supplied by 42."""
    prompts = load_prompts(Path("data/input/function_calling_tests.json"))
    assert len(prompts) == 11
    assert prompts[0].prompt == "What is the sum of 2 and 3?"


def test_loads_supplied_function_definitions() -> None:
    """Load all function definitions supplied by 42."""
    definitions = load_function_definitions(
        Path("data/input/functions_definition.json")
    )
    assert len(definitions) == 5
    assert definitions[0].name == "fn_add_numbers"


def test_missing_file_has_clear_error(tmp_path: Path) -> None:
    """Convert a missing file into an expected application error."""
    missing = tmp_path / "missing.json"
    with pytest.raises(InputFileError, match="Input file not found"):
        load_prompts(missing)


def test_malformed_json_reports_location(tmp_path: Path) -> None:
    """Include line and column information for malformed JSON."""
    broken = tmp_path / "broken.json"
    broken.write_text('[{"prompt": "hello"}', encoding="utf-8")
    with pytest.raises(InputFileError, match="line 1, column"):
        load_prompts(broken)


def test_wrong_prompt_shape_is_rejected(tmp_path: Path) -> None:
    """Reject an object when the input contract requires a list."""
    path = tmp_path / "prompts.json"
    write_json(path, {"prompt": "hello"})
    with pytest.raises(InputFileError, match="Invalid structure"):
        load_prompts(path)


def test_extra_prompt_key_is_rejected(tmp_path: Path) -> None:
    """Reject unrecognized fields instead of silently ignoring them."""
    path = tmp_path / "prompts.json"
    write_json(path, [{"prompt": "hello", "unexpected": True}])
    with pytest.raises(InputFileError, match="extra_forbidden"):
        load_prompts(path)


def test_duplicate_function_names_are_rejected(tmp_path: Path) -> None:
    """Reject ambiguous duplicate function names."""
    definition = {
        "name": "fn_same",
        "description": "A function.",
        "parameters": {},
        "returns": {"type": "string"},
    }
    path = tmp_path / "functions.json"
    write_json(path, [definition, definition])
    with pytest.raises(InputFileError, match="Duplicate function names"):
        load_function_definitions(path)


def test_empty_function_list_is_rejected(tmp_path: Path) -> None:
    """Require at least one callable function."""
    path = tmp_path / "functions.json"
    write_json(path, [])
    with pytest.raises(InputFileError, match="No function definition"):
        load_function_definitions(path)


def test_write_results_uses_exact_required_schema(tmp_path: Path) -> None:
    output = tmp_path / "nested" / "results.json"
    results = [
        OutputEntry(
            prompt="Add two numbers",
            fn_name="fn_add_numbers",
            args={"a": 2.0, "b": 3.0},
        )
    ]

    write_results(output, results)

    assert json.loads(output.read_text(encoding="utf-8")) == [
        {
            "prompt": "Add two numbers",
            "fn_name": "fn_add_numbers",
            "args": {"a": 2.0, "b": 3.0},
        }
    ]
    assert not output.with_suffix(".json.tmp").exists()


def test_output_entry_rejects_legacy_field_names() -> None:
    with pytest.raises(ValueError):
        OutputEntry.model_validate(
            {
                "prompt": "Ping",
                "name": "fn_ping",
                "parameters": {},
            }
        )
