"""Tests for the complete command-line orchestration without loading Qwen."""

import json
from pathlib import Path

import pytest

import src.__main__ as main_module
from src.token_vocabulary import TokenVocabulary
from tests.test_pipeline import DeterministicModel


def write_inputs(directory: Path) -> tuple[Path, Path]:
    """Write one function and one prompt for an isolated CLI run."""
    functions = directory / "functions.json"
    prompts = directory / "prompts.json"
    functions.write_text(
        json.dumps(
            [
                {
                    "name": "fn_ping",
                    "description": "Ping a service.",
                    "parameters": {},
                    "returns": {"type": "string"},
                }
            ]
        ),
        encoding="utf-8",
    )
    prompts.write_text(
        json.dumps([{"prompt": "Ping now"}]),
        encoding="utf-8",
    )
    return functions, prompts


def test_main_generates_and_writes_results(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    functions, prompts = write_inputs(tmp_path)
    output = tmp_path / "output" / "results.json"
    runtime = (
        DeterministicModel(),
        TokenVocabulary(tokens_by_id={0: "unused"}),
    )
    monkeypatch.setattr(main_module, "_load_runtime", lambda: runtime)

    exit_code = main_module.main(
        [
            "--functions_definition",
            str(functions),
            "--input",
            str(prompts),
            "--output",
            str(output),
        ]
    )

    assert exit_code == 0
    assert json.loads(output.read_text(encoding="utf-8")) == [
        {"prompt": "Ping now", "name": "fn_ping", "parameters": {}}
    ]
    stdout = capsys.readouterr().out
    assert "[1/1] fn_ping" in stdout
    assert f"Wrote 1 results to {output}" in stdout


def test_main_reports_input_error_without_loading_model(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    model_loaded = False

    def fail_if_loaded() -> tuple[object, object]:
        nonlocal model_loaded
        model_loaded = True
        raise AssertionError("model should not load")

    monkeypatch.setattr(main_module, "_load_runtime", fail_if_loaded)

    exit_code = main_module.main(
        ["--input", str(tmp_path / "missing.json")]
    )

    assert exit_code == 1
    assert not model_loaded
    assert "Input file not found" in capsys.readouterr().err
