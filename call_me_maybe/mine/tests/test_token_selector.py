"""Tests for selecting the best grammar-compatible token."""

from collections.abc import Sequence
from math import nan

import pytest

from src.json_grammar import FunctionCallGrammar
from src.models import FunctionDefinition
from src.token_selector import TokenSelectionError
from src.token_selector import select_best_valid_token
from src.token_vocabulary import TokenVocabulary


class FakeDecoder:
    """Decode configured token sequences without loading an LLM."""

    def __init__(self, decoded: dict[tuple[int, ...], str]) -> None:
        self.decoded = decoded
        self.calls: list[tuple[int, ...]] = []

    def decode(self, token_ids: Sequence[int]) -> str:
        """Return the configured text and record the public API call."""
        key = tuple(token_ids)
        self.calls.append(key)
        return self.decoded.get(key, "invalid")


def make_grammar() -> FunctionCallGrammar:
    """Build a minimal no-argument function-call grammar."""
    definition = FunctionDefinition.model_validate(
        {
            "name": "fn_ping",
            "description": "Ping the service.",
            "parameters": {},
            "returns": {"type": "string"},
        }
    )
    return FunctionCallGrammar(definitions=(definition,))


def make_vocabulary(*token_ids: int) -> TokenVocabulary:
    """Build a vocabulary containing the requested identifiers."""
    return TokenVocabulary(
        tokens_by_id={token_id: f"token-{token_id}" for token_id in token_ids}
    )


def test_selects_highest_logit_valid_token() -> None:
    model = FakeDecoder(
        {
            (): "",
            (0,): "Sure",
            (1,): "{",
            (2,): '{"',
        }
    )

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(0, 1, 2),
        [],
        [10.0, 4.0, 7.0],
    )

    assert selected == 2
    assert model.calls == [(), (0,), (2,)]


def test_ignores_reserved_logit_positions() -> None:
    model = FakeDecoder({(): "", (1,): "{", (2,): '{"'})

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(1, 2),
        [],
        [1000.0, 2.0, 1.0, 500.0],
    )

    assert selected == 1
    assert (0,) not in model.calls
    assert (3,) not in model.calls


def test_skips_token_that_adds_no_visible_text() -> None:
    model = FakeDecoder({(): "", (0,): "", (1,): "{"})

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(0, 1),
        [],
        [9.0, 1.0],
    )

    assert selected == 1


def test_equal_logits_use_lower_token_id_deterministically() -> None:
    model = FakeDecoder({(): "", (1,): "{", (2,): '{"'})

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(1, 2),
        [],
        [0.0, 5.0, 5.0],
    )

    assert selected == 1


def test_numpy_ranking_handles_unsorted_vocabulary_ids() -> None:
    model = FakeDecoder({(): "", (1,): "{", (2,): '{"'})
    vocabulary = TokenVocabulary(
        tokens_by_id={2: "second", 1: "first"}
    )

    selected = select_best_valid_token(
        model,
        make_grammar(),
        vocabulary,
        [],
        [0.0, 4.0, 4.0],
    )

    assert selected == 1


def test_selection_continues_existing_generated_prefix() -> None:
    model = FakeDecoder(
        {
            (8,): "{",
            (8, 0): "{bad",
            (8, 1): '{"',
        }
    )

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(0, 1),
        [8],
        [10.0, 2.0],
    )

    assert selected == 1


def test_accepts_token_that_completes_the_call() -> None:
    complete_call = '{"fn_name":"fn_ping","args":{}}'
    partial_call = complete_call[:-1]
    model = FakeDecoder({(8,): partial_call, (8, 1): complete_call})

    selected = select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(1),
        [8],
        [0.0, 3.0],
    )

    assert selected == 1


def test_raises_when_no_token_can_continue() -> None:
    model = FakeDecoder({(): "", (0,): "bad", (1,): "also bad"})

    with pytest.raises(TokenSelectionError, match="No vocabulary token"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(0, 1),
            [],
            [2.0, 1.0],
        )


def test_rejects_invalid_existing_prefix() -> None:
    model = FakeDecoder({(8,): "not json"})

    with pytest.raises(TokenSelectionError, match="valid grammar prefix"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(0),
            [8],
            [1.0],
        )


def test_rejects_selection_after_complete_call() -> None:
    complete_call = '{"fn_name":"fn_ping","args":{}}'
    model = FakeDecoder({(8,): complete_call})

    with pytest.raises(TokenSelectionError, match="already complete"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(0),
            [8],
            [1.0],
        )


def test_rejects_empty_logits() -> None:
    model = FakeDecoder({(): ""})

    with pytest.raises(TokenSelectionError, match="empty logits"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(0),
            [],
            [],
        )


def test_rejects_logits_too_short_for_vocabulary() -> None:
    model = FakeDecoder({(): ""})

    with pytest.raises(TokenSelectionError, match="cannot represent"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(2),
            [],
            [1.0, 2.0],
        )


def test_rejects_non_finite_known_logit() -> None:
    model = FakeDecoder({(): ""})

    with pytest.raises(TokenSelectionError, match="finite logits"):
        select_best_valid_token(
            model,
            make_grammar(),
            make_vocabulary(0),
            [],
            [nan],
        )


def test_inputs_are_not_mutated() -> None:
    model = FakeDecoder({(8,): "{", (8, 0): '{"'})
    generated_ids = [8]
    logits = [1.0]

    select_best_valid_token(
        model,
        make_grammar(),
        make_vocabulary(0),
        generated_ids,
        logits,
    )

    assert generated_ids == [8]
    assert logits == [1.0]
