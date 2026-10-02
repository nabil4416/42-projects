"""Tests for multi-prompt constrained-generation orchestration."""

from collections.abc import Sequence

import pytest

from src.errors import GenerationError
from src.models import FunctionDefinition, PromptInput
from src.pipeline import generate_results, parse_generated_call
from src.token_vocabulary import TokenVocabulary


COMPLETE_CALL = '{"fn_name":"fn_ping","args":{}}'


class DeterministicModel:
    """Model double for a call whose entire output is grammar-forced."""

    def __init__(self) -> None:
        self.encoded_prompts: list[str] = []

    def encode(self, text: str) -> list[int]:
        """Encode prepared prompts and the forced complete call."""
        if text == COMPLETE_CALL:
            return [1]
        self.encoded_prompts.append(text)
        return [100]

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decode the only forced generated token sequence."""
        if not token_ids:
            return ""
        if list(token_ids) == [1]:
            return COMPLETE_CALL
        return "invalid"

    def next_token_logits(self, input_ids: Sequence[int]) -> list[float]:
        """Fail if deterministic grammar text requests model inference."""
        raise AssertionError("Logits should not be requested")


class BrokenForcedEncodingModel(DeterministicModel):
    """Model whose tokenizer cannot reproduce the forced JSON text."""

    def decode(self, token_ids: Sequence[int]) -> str:
        """Return invalid text for every non-empty generated sequence."""
        return "" if not token_ids else "broken"


def make_definition() -> FunctionDefinition:
    """Build the deterministic no-argument function definition."""
    return FunctionDefinition.model_validate(
        {
            "name": "fn_ping",
            "description": "Ping a service.",
            "parameters": {},
            "returns": {"type": "string"},
        }
    )


def make_vocabulary() -> TokenVocabulary:
    """Build a minimal vocabulary unused by deterministic insertion."""
    return TokenVocabulary(tokens_by_id={0: "unused"})


def test_parse_generated_call_uses_exact_internal_contract() -> None:
    call = parse_generated_call(COMPLETE_CALL)

    assert call.fn_name == "fn_ping"
    assert call.args == {}


@pytest.mark.parametrize(
    "text",
    [
        "not json",
        '{"name":"fn_ping","parameters":{}}',
        '{"fn_name":"fn_ping","args":{},"extra":true}',
    ],
)
def test_parse_generated_call_rejects_invalid_payload(text: str) -> None:
    with pytest.raises(GenerationError):
        parse_generated_call(text)


def test_generates_one_result_per_prompt_and_reports_progress() -> None:
    prompts = [PromptInput(prompt="First"), PromptInput(prompt="Second")]
    model = DeterministicModel()
    progress: list[tuple[int, int, str]] = []

    results = generate_results(
        definitions=[make_definition()],
        prompts=prompts,
        model=model,
        vocabulary=make_vocabulary(),
        on_progress=lambda index, total, entry: progress.append(
            (index, total, entry.fn_name)
        ),
    )

    assert [result.model_dump() for result in results] == [
        {"prompt": "First", "fn_name": "fn_ping", "args": {}},
        {"prompt": "Second", "fn_name": "fn_ping", "args": {}},
    ]
    assert progress == [(1, 2, "fn_ping"), (2, 2, "fn_ping")]
    assert len(model.encoded_prompts) == 2


def test_failure_identifies_prompt_position() -> None:
    prompts = [PromptInput(prompt="First"), PromptInput(prompt="Second")]

    with pytest.raises(GenerationError, match="Prompt 1/2 failed"):
        generate_results(
            definitions=[make_definition()],
            prompts=prompts,
            model=BrokenForcedEncodingModel(),
            vocabulary=make_vocabulary(),
        )


def test_empty_prompt_sequence_returns_empty_results() -> None:
    results = generate_results(
        definitions=[make_definition()],
        prompts=[],
        model=DeterministicModel(),
        vocabulary=make_vocabulary(),
    )

    assert results == []
