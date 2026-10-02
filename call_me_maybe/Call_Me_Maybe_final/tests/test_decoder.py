"""Tests for the complete constrained decoding loop."""

from collections.abc import Sequence

import pytest
from pydantic import ValidationError

from src.decoder import DecodingError, DecodingResult
from src.decoder import decode_function_call
from src.json_grammar import FunctionCallGrammar
from src.models import FunctionDefinition
from src.token_vocabulary import TokenVocabulary


FORCED_PREFIX = '{"fn_name":"fn_echo","args":{"value":"'
COMPLETE_CALL = FORCED_PREFIX + 'AB"}}'
PARTIAL_CALLS = (
    FORCED_PREFIX + "A",
    FORCED_PREFIX + "AB",
    FORCED_PREFIX + 'AB"',
)


class ScriptedModel:
    """Small deterministic model used to test the decoding loop."""

    def __init__(self) -> None:
        self.prompt_ids = [100, 101]
        self.logit_inputs: list[list[int]] = []
        self.decode_inputs: list[list[int]] = []

    def encode(self, text: str) -> list[int]:
        """Encode the prompt and grammar-forced generated text."""
        if text == "prepared prompt":
            return list(self.prompt_ids)
        if text == FORCED_PREFIX:
            return [9]
        if text == COMPLETE_CALL:
            return [9, 0, 1, 2, 8]
        return [7]

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decode the scripted generation prefixes."""
        ids = list(token_ids)
        self.decode_inputs.append(ids)
        if not ids:
            return ""
        if ids == [9]:
            return FORCED_PREFIX
        if ids == [9, 0]:
            return PARTIAL_CALLS[0]
        if ids == [9, 0, 1]:
            return PARTIAL_CALLS[1]
        if ids == [9, 0, 1, 2]:
            return PARTIAL_CALLS[2]
        if ids == [9, 0, 1, 2, 8]:
            return COMPLETE_CALL
        return "invalid"

    def next_token_logits(
        self,
        input_ids: Sequence[int],
    ) -> list[float]:
        """Make the next scripted token the highest-scoring candidate."""
        ids = list(input_ids)
        self.logit_inputs.append(ids)
        generated_ids = ids[len(self.prompt_ids):]
        if generated_ids == [9]:
            return [10.0, 1.0, 0.0]
        if generated_ids == [9, 0]:
            return [0.0, 10.0, 1.0]
        return [0.0, 1.0, 10.0]


class EmptyEncodingModel(ScriptedModel):
    """Model whose prepared prompt unexpectedly encodes to no tokens."""

    def encode(self, text: str) -> list[int]:
        """Return an invalid empty encoding."""
        return []


class ImpossibleModel(ScriptedModel):
    """Model whose known tokens cannot continue the grammar."""

    def decode(self, token_ids: Sequence[int]) -> str:
        """Keep the empty prefix valid but make every token invalid."""
        ids = list(token_ids)
        return "" if not ids else "not json"


class UnforcedGrammar(FunctionCallGrammar):
    """Grammar variant used to reach token-selection failures directly."""

    def forced_continuation(self, text: str) -> str:
        """Disable deterministic insertion for this isolated error test."""
        return ""


def make_grammar() -> FunctionCallGrammar:
    """Build the function-call grammar used by decoder tests."""
    definition = FunctionDefinition.model_validate(
        {
            "name": "fn_echo",
            "description": "Echo a value.",
            "parameters": {"value": {"type": "string"}},
            "returns": {"type": "string"},
        }
    )
    return FunctionCallGrammar(definitions=(definition,))


def make_vocabulary() -> TokenVocabulary:
    """Build the three-token vocabulary used by the scripted model."""
    return TokenVocabulary(
        tokens_by_id={0: "first", 1: "second", 2: "third"}
    )


def test_decodes_until_function_call_is_complete() -> None:
    model = ScriptedModel()

    result = decode_function_call(
        model,
        make_grammar(),
        make_vocabulary(),
        "prepared prompt",
    )

    assert result.text == COMPLETE_CALL
    assert result.token_ids == (9, 0, 1, 2, 8)


def test_logits_receive_prompt_and_generated_tokens() -> None:
    model = ScriptedModel()

    decode_function_call(
        model,
        make_grammar(),
        make_vocabulary(),
        "prepared prompt",
    )

    assert model.logit_inputs == [
        [100, 101, 9],
        [100, 101, 9, 0],
        [100, 101, 9, 0, 1],
    ]


def test_grammar_decodes_only_generated_tokens() -> None:
    model = ScriptedModel()

    decode_function_call(
        model,
        make_grammar(),
        make_vocabulary(),
        "prepared prompt",
    )

    assert all(
        not ids or ids[0] != model.prompt_ids[0]
        for ids in model.decode_inputs
    )


def test_stops_without_requesting_logits_after_completion() -> None:
    model = ScriptedModel()

    decode_function_call(
        model,
        make_grammar(),
        make_vocabulary(),
        "prepared prompt",
    )

    assert len(model.logit_inputs) == 3


def test_completion_on_last_allowed_token_succeeds() -> None:
    result = decode_function_call(
        ScriptedModel(),
        make_grammar(),
        make_vocabulary(),
        "prepared prompt",
        max_new_tokens=5,
    )

    assert result.text == COMPLETE_CALL


def test_token_limit_raises_clear_error() -> None:
    with pytest.raises(DecodingError, match="not complete after 4 tokens"):
        decode_function_call(
            ScriptedModel(),
            make_grammar(),
            make_vocabulary(),
            "prepared prompt",
            max_new_tokens=4,
        )


@pytest.mark.parametrize("max_new_tokens", [0, -1, True, 1.5])
def test_rejects_invalid_token_limit(max_new_tokens: object) -> None:
    with pytest.raises(DecodingError, match="positive integer"):
        decode_function_call(
            ScriptedModel(),
            make_grammar(),
            make_vocabulary(),
            "prepared prompt",
            max_new_tokens=max_new_tokens,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize("prepared_prompt", ["", "   ", "\n\t"])
def test_rejects_blank_prepared_prompt(prepared_prompt: str) -> None:
    with pytest.raises(DecodingError, match="must not be empty"):
        decode_function_call(
            ScriptedModel(),
            make_grammar(),
            make_vocabulary(),
            prepared_prompt,
        )


def test_rejects_empty_prompt_encoding() -> None:
    with pytest.raises(DecodingError, match="empty token list"):
        decode_function_call(
            EmptyEncodingModel(),
            make_grammar(),
            make_vocabulary(),
            "prepared prompt",
        )


def test_wraps_token_selection_error_with_step() -> None:
    with pytest.raises(DecodingError, match="generation step 1"):
        definition = make_grammar().definitions[0]
        decode_function_call(
            ImpossibleModel(),
            UnforcedGrammar(definitions=(definition,)),
            make_vocabulary(),
            "prepared prompt",
        )


def test_decoding_result_rejects_extra_fields() -> None:
    with pytest.raises(ValidationError):
        DecodingResult(
            text=COMPLETE_CALL,
            token_ids=(0, 1, 2),
            unexpected=True,  # type: ignore[call-arg]
        )


def test_decoding_result_is_frozen() -> None:
    result = DecodingResult(text=COMPLETE_CALL, token_ids=(0, 1, 2))

    with pytest.raises(ValidationError):
        result.text = "changed"
