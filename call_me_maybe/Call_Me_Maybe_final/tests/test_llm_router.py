"""Tests for LLM-based constrained function selection."""

from collections.abc import Sequence

import pytest

import src.llm_router as router_module
from src.decoder import ConstrainedModel, DecodingResult
from src.json_grammar import FunctionCallGrammar
from src.llm_router import build_routing_prompt, choose_definition
from src.models import FunctionDefinition, PromptInput
from src.token_vocabulary import TokenVocabulary


class NeverUsedModel:
    """Protocol-compatible model for tests that replace the decoder."""

    def encode(self, text: str) -> list[int]:
        """Fail if a test unexpectedly reaches real encoding."""
        raise AssertionError("encode should not be called")

    def decode(self, token_ids: Sequence[int]) -> str:
        """Fail if a test unexpectedly reaches real decoding."""
        raise AssertionError("decode should not be called")

    def next_token_logits(self, input_ids: Sequence[int]) -> list[float]:
        """Fail if a test unexpectedly reaches real inference."""
        raise AssertionError("logits should not be called")


def make_definition(name: str, description: str) -> FunctionDefinition:
    """Build a small definition for routing tests."""
    return FunctionDefinition.model_validate(
        {
            "name": name,
            "description": description,
            "parameters": {"value": {"type": "string"}},
            "returns": {"type": "string"},
        }
    )


def make_vocabulary() -> TokenVocabulary:
    """Build a minimal vocabulary for the replaced decoder."""
    return TokenVocabulary(tokens_by_id={0: "unused"})


def test_routing_prompt_contains_every_dynamic_definition() -> None:
    definitions = [
        make_definition("fn_launch", "Launch a rocket."),
        make_definition("fn_play", "Play a song."),
    ]

    prompt = build_routing_prompt(
        definitions,
        PromptInput(prompt="Launch now"),
    )

    assert "- option_1 = fn_launch: Launch a rocket." in prompt
    assert "- option_2 = fn_play: Play a song." in prompt
    assert 'Request:"Launch now"' in prompt


def test_single_available_function_needs_no_model_choice() -> None:
    definition = make_definition("fn_only", "The only action.")

    selected = choose_definition(
        [definition],
        PromptInput(prompt="Do it"),
        NeverUsedModel(),
        make_vocabulary(),
    )

    assert selected is definition


def test_multiple_functions_are_selected_by_constrained_llm(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    definitions = [
        make_definition("fn_alpha", "Perform alpha."),
        make_definition("fn_beta", "Perform beta."),
    ]
    received_grammars: list[FunctionCallGrammar] = []

    def fake_decode(
        model: ConstrainedModel,
        grammar: FunctionCallGrammar,
        vocabulary: TokenVocabulary,
        prepared_prompt: str,
        *,
        max_new_tokens: int = 128,
    ) -> DecodingResult:
        received_grammars.append(grammar)
        assert "Perform beta" in prepared_prompt
        assert max_new_tokens == 32
        return DecodingResult(
            text='{"fn_name":"option_2","args":{}}',
            token_ids=(1,),
        )

    monkeypatch.setattr(router_module, "decode_function_call", fake_decode)

    selected = choose_definition(
        definitions,
        PromptInput(prompt="Please perform beta"),
        NeverUsedModel(),
        make_vocabulary(),
    )

    assert selected.name == "fn_beta"
    assert len(received_grammars) == 1
    assert all(
        not definition.parameters
        for definition in received_grammars[0].definitions
    )
    assert [
        definition.name
        for definition in received_grammars[0].definitions
    ] == ["option_1", "option_2"]
