"""Tests for the public Qwen SDK adapter."""

from pathlib import Path
from typing import cast

import pytest

import src.model as model_module
from src.model import MODEL_NAME, ModelBackend, QwenModel


class FakeEncodedBatch:
    """Small tensor substitute used without loading Qwen."""

    def __init__(self, rows: list[list[int]]) -> None:
        self.rows = rows

    def tolist(self) -> list[list[int]]:
        """Return the configured token rows."""
        return self.rows


class RecordingBackend:
    """Record calls made to the public SDK surface."""

    def __init__(self) -> None:
        self.encoded_texts: list[str] = []
        self.decoded_ids: list[list[int]] = []
        self.logit_inputs: list[list[int]] = []
        self.encoded_rows = [[11, 22, 33]]

    def encode(self, text: str) -> FakeEncodedBatch:
        """Return predictable token identifiers."""
        self.encoded_texts.append(text)
        return FakeEncodedBatch(self.encoded_rows)

    def decode(self, ids: list[int]) -> str:
        """Return predictable decoded text."""
        self.decoded_ids.append(ids)
        return "decoded text"

    def get_logits_from_input_ids(
        self,
        input_ids: list[int],
    ) -> list[float]:
        """Return predictable next-token logits."""
        self.logit_inputs.append(input_ids)
        return [0.25, -1.0, 3.5]

    def get_path_to_tokenizer_file(self) -> str:
        """Return a predictable public tokenizer path."""
        return "/tmp/qwen-tokenizer.json"


def make_model() -> tuple[QwenModel, RecordingBackend]:
    """Build an adapter backed by the lightweight test double."""
    backend = RecordingBackend()
    model = QwenModel(backend=cast(ModelBackend, backend))
    return model, backend


def test_default_backend_uses_required_qwen_model(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    received_names: list[str] = []
    backend = RecordingBackend()

    def fake_factory(model_name: str) -> RecordingBackend:
        received_names.append(model_name)
        return backend

    monkeypatch.setattr(model_module, "Small_LLM_Model", fake_factory)

    QwenModel()

    assert MODEL_NAME == "Qwen/Qwen3-0.6B"
    assert received_names == [MODEL_NAME]


def test_encode_delegates_to_public_sdk_method() -> None:
    model, backend = make_model()

    token_ids = model.encode("prepared prompt")

    assert token_ids == [11, 22, 33]
    assert backend.encoded_texts == ["prepared prompt"]


def test_decode_delegates_to_public_sdk_method() -> None:
    model, backend = make_model()

    text = model.decode((11, 22, 33))

    assert text == "decoded text"
    assert backend.decoded_ids == [[11, 22, 33]]


def test_next_token_logits_delegates_to_public_sdk_method() -> None:
    model, backend = make_model()

    logits = model.next_token_logits([11, 22])

    assert logits == [0.25, -1.0, 3.5]
    assert backend.logit_inputs == [[11, 22]]


def test_tokenizer_file_path_uses_public_sdk_method() -> None:
    model, _ = make_model()

    tokenizer_path = model.tokenizer_file_path()

    assert tokenizer_path == Path("/tmp/qwen-tokenizer.json")


def test_encode_rejects_unexpected_batch_shape() -> None:
    model, backend = make_model()
    backend.encoded_rows = [[1], [2]]

    with pytest.raises(ValueError, match="exactly one token row"):
        model.encode("text")


@pytest.mark.parametrize("token_ids", [[1, "2"], [True, 2]])
def test_token_operations_reject_non_integer_ids(
    token_ids: list[object],
) -> None:
    model, _ = make_model()

    with pytest.raises(ValueError, match="must all be integers"):
        model.decode(cast(list[int], token_ids))


def test_caller_token_list_is_not_mutated() -> None:
    model, _ = make_model()
    token_ids = [11, 22]

    model.next_token_logits(token_ids)

    assert token_ids == [11, 22]
