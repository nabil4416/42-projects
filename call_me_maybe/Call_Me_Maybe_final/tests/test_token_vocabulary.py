"""Tests for validated loading of tokenizer vocabulary data."""

import json
from pathlib import Path
from typing import Any

import pytest

from src.token_vocabulary import TokenVocabulary, TokenVocabularyError


def write_tokenizer(
    path: Path,
    vocab: dict[str, Any],
    added_tokens: list[dict[str, Any]] | None = None,
) -> None:
    """Write a minimal tokenizer file for one test."""
    data = {
        "version": "1.0",
        "model": {"type": "BPE", "vocab": vocab},
        "added_tokens": added_tokens or [],
    }
    path.write_text(json.dumps(data), encoding="utf-8")


def test_loads_base_and_added_tokens(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(
        tokenizer_path,
        {"hello": 0, "world": 1},
        [{"id": 3, "content": "<special>", "special": True}],
    )

    vocabulary = TokenVocabulary.from_file(tokenizer_path)

    assert vocabulary.tokens_by_id == {
        0: "hello",
        1: "world",
        3: "<special>",
    }
    assert vocabulary.size == 3
    assert vocabulary.maximum_token_id == 3


def test_missing_file_has_clear_error(tmp_path: Path) -> None:
    missing_path = tmp_path / "missing.json"

    with pytest.raises(TokenVocabularyError, match="not found"):
        TokenVocabulary.from_file(missing_path)


def test_malformed_json_reports_location(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    tokenizer_path.write_text('{"model": ', encoding="utf-8")

    with pytest.raises(TokenVocabularyError, match=r"line 1, column"):
        TokenVocabulary.from_file(tokenizer_path)


@pytest.mark.parametrize(
    "data",
    [
        {},
        {"model": {}},
        {"model": {"vocab": []}},
        {"model": {"vocab": {"token": "zero"}}},
    ],
)
def test_invalid_structure_is_rejected(
    tmp_path: Path,
    data: dict[str, Any],
) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    tokenizer_path.write_text(json.dumps(data), encoding="utf-8")

    with pytest.raises(TokenVocabularyError, match="Invalid tokenizer"):
        TokenVocabulary.from_file(tokenizer_path)


def test_empty_vocabulary_is_rejected(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(tokenizer_path, {})

    with pytest.raises(TokenVocabularyError, match="must not be empty"):
        TokenVocabulary.from_file(tokenizer_path)


def test_conflicting_token_ids_are_rejected(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(
        tokenizer_path,
        {"base": 0},
        [{"id": 0, "content": "different"}],
    )

    with pytest.raises(TokenVocabularyError, match="assigned more than once"):
        TokenVocabulary.from_file(tokenizer_path)


def test_conflict_with_empty_token_is_rejected(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(
        tokenizer_path,
        {"": 0},
        [{"id": 0, "content": "different"}],
    )

    with pytest.raises(TokenVocabularyError, match="assigned more than once"):
        TokenVocabulary.from_file(tokenizer_path)


def test_negative_token_id_is_rejected(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(tokenizer_path, {"invalid": -1})

    with pytest.raises(TokenVocabularyError, match="must not be negative"):
        TokenVocabulary.from_file(tokenizer_path)


def test_unknown_token_id_has_clear_error(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(tokenizer_path, {"known": 0})
    vocabulary = TokenVocabulary.from_file(tokenizer_path)

    with pytest.raises(TokenVocabularyError, match="Unknown token id: 99"):
        vocabulary.token_for_id(99)


def test_logits_size_accepts_unused_ids(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(tokenizer_path, {"zero": 0, "five": 5})
    vocabulary = TokenVocabulary.from_file(tokenizer_path)

    vocabulary.validate_logits_size(8)


def test_logits_size_rejects_unreachable_token_id(tmp_path: Path) -> None:
    tokenizer_path = tmp_path / "tokenizer.json"
    write_tokenizer(tokenizer_path, {"zero": 0, "five": 5})
    vocabulary = TokenVocabulary.from_file(tokenizer_path)

    with pytest.raises(TokenVocabularyError, match="cannot represent"):
        vocabulary.validate_logits_size(5)
