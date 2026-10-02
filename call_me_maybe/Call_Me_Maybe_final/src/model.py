"""Public, minimal adapter around the LLM SDK used by the decoder."""

from collections.abc import Sequence
from pathlib import Path
from typing import Protocol

from llm_sdk import Small_LLM_Model  # type: ignore[attr-defined]


MODEL_NAME = "Qwen/Qwen3-0.6B"


class EncodedBatch(Protocol):
    """Shape needed from the tensor returned by the SDK."""

    def tolist(self) -> list[list[int]]:
        """Return the encoded batch as regular Python lists."""
        ...


class ModelBackend(Protocol):
    """Public SDK methods required by the constrained decoder."""

    def encode(self, text: str) -> EncodedBatch:
        """Encode text as a batch containing token identifiers."""
        ...

    def decode(self, ids: list[int]) -> str:
        """Decode token identifiers into text."""
        ...

    def get_logits_from_input_ids(
        self,
        input_ids: list[int],
    ) -> list[float]:
        """Return the next-token logits."""
        ...

    def get_path_to_tokenizer_file(self) -> str:
        """Return the path to the public tokenizer description."""
        ...


class QwenModel:
    """Expose only the public SDK operations needed by this project."""

    def __init__(self, backend: ModelBackend | None = None) -> None:
        """Use an injected public backend or load the required Qwen model."""
        self._backend = backend or Small_LLM_Model(model_name=MODEL_NAME)

    def encode(self, text: str) -> list[int]:
        """Encode one text and remove the SDK's batch dimension."""
        encoded_rows = self._backend.encode(text).tolist()
        if len(encoded_rows) != 1:
            raise ValueError("encode() must return exactly one token row")

        token_ids = encoded_rows[0]
        if any(type(token_id) is not int for token_id in token_ids):
            raise ValueError("encode() returned a non-integer token id")
        return token_ids

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decode a sequence of token identifiers through the SDK."""
        ids = self._validated_token_ids(token_ids)
        return self._backend.decode(ids)

    def next_token_logits(
        self,
        input_ids: Sequence[int],
    ) -> list[float]:
        """Return logits for the token following ``input_ids``."""
        ids = self._validated_token_ids(input_ids)
        return self._backend.get_logits_from_input_ids(ids)

    def tokenizer_file_path(self) -> Path:
        """Return the tokenizer path supplied by the public SDK API."""
        return Path(self._backend.get_path_to_tokenizer_file())

    @staticmethod
    def _validated_token_ids(token_ids: Sequence[int]) -> list[int]:
        """Copy and validate token identifiers passed to the SDK."""
        ids = list(token_ids)
        if any(type(token_id) is not int for token_id in ids):
            raise ValueError("token ids must all be integers")
        return ids
