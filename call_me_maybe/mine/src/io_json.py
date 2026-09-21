"""Read and validate JSON inputs and write JSON outputs."""

import json
from pathlib import Path
from typing import Any, TypeVar

from pydantic import BaseModel, TypeAdapter, ValidationError

from src.errors import InputFileError
from src.models import FunctionDefinition, OutputEntry, PromptInput


ModelT = TypeVar("ModelT", bound=BaseModel)


def _read_json(path: Path) -> Any:
    """Read a JSON file and translate expected failures into clear errors."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            return json.load(stream)
    except FileNotFoundError as exc:
        raise InputFileError(f"Input file not found: {path}") from exc
    except PermissionError as exc:
        message = f"Permission denied while reading: {path}"
        raise InputFileError(message) from exc
    except json.JSONDecodeError as exc:
        message = (
            f"Invalid JSON in {path} at line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        )
        raise InputFileError(message) from exc
    except OSError as exc:
        raise InputFileError(f"Could not read {path}: {exc}") from exc


def _load_model_list(
    path: Path,
    adapter: TypeAdapter[list[ModelT]],
) -> list[ModelT]:
    """Load a JSON array and validate every element with Pydantic."""
    raw_data = _read_json(path)
    try:
        return adapter.validate_python(raw_data)
    except ValidationError as exc:
        raise InputFileError(f"Invalid structure in {path}:\n{exc}") from exc


def load_prompts(path: Path) -> list[PromptInput]:
    """Load validated prompt entries."""
    adapter = TypeAdapter(list[PromptInput])
    return _load_model_list(path, adapter)


def load_function_definitions(path: Path) -> list[FunctionDefinition]:
    """Load function definitions and reject duplicate function names."""
    adapter = TypeAdapter(list[FunctionDefinition])
    definitions = _load_model_list(path, adapter)
    names = [definition.name for definition in definitions]
    duplicates = sorted({name for name in names if names.count(name) > 1})
    if duplicates:
        joined = ", ".join(duplicates)
        raise InputFileError(f"Duplicate function names in {path}: {joined}")
    if not definitions:
        raise InputFileError(f"No function definition found in: {path}")
    return definitions


def write_results(path: Path, results: list[OutputEntry]) -> None:
    """Write validated results, creating the output directory as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = [result.model_dump(mode="json") for result in results]
    temporary_path = path.with_suffix(f"{path.suffix}.tmp")
    try:
        with temporary_path.open("w", encoding="utf-8") as stream:
            json.dump(payload, stream, indent=2, ensure_ascii=False)
            stream.write("\n")
        temporary_path.replace(path)
    except OSError as exc:
        raise InputFileError(f"Could not write {path}: {exc}") from exc
