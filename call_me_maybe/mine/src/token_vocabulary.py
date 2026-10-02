"""Validated access to token identifiers declared by tokenizer.json."""

import json
from json import JSONDecodeError
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from pydantic import ValidationError, field_validator

from src.errors import CallMeMaybeError


class TokenVocabularyError(CallMeMaybeError):
    """Raised when a tokenizer vocabulary cannot be loaded safely."""


class _TokenizerModel(BaseModel):
    """Relevant part of the tokenizer's model section."""

    model_config = ConfigDict(extra="ignore")

    vocab: dict[StrictStr, StrictInt]


class _AddedToken(BaseModel):
    """Relevant fields of one tokenizer added-token entry."""

    model_config = ConfigDict(extra="ignore")

    token_id: StrictInt = Field(alias="id")
    content: StrictStr


class _TokenizerFile(BaseModel):
    """Relevant, validated subset of tokenizer.json."""

    model_config = ConfigDict(extra="ignore")

    model: _TokenizerModel
    added_tokens: list[_AddedToken] = Field(default_factory=list)


class TokenVocabulary(BaseModel):
    """Map token identifiers to their tokenizer representations."""

    model_config = ConfigDict(frozen=True)

    tokens_by_id: dict[int, str]

    @field_validator("tokens_by_id")
    @classmethod
    def reject_invalid_vocabulary(
        cls,
        value: dict[int, str],
    ) -> dict[int, str]:
        """Reject empty vocabularies and negative token identifiers."""
        if not value:
            raise ValueError("token vocabulary must not be empty")
        if any(token_id < 0 for token_id in value):
            raise ValueError("token ids must not be negative")
        return value

    @classmethod
    def from_file(cls, path: str | Path) -> "TokenVocabulary":
        """Load the relevant vocabulary data from tokenizer.json."""
        tokenizer_path = Path(path)
        try:
            with tokenizer_path.open(encoding="utf-8") as file:
                raw_data = json.load(file)
        except FileNotFoundError as error:
            raise TokenVocabularyError(
                f"Tokenizer file not found: {tokenizer_path}"
            ) from error
        except OSError as error:
            raise TokenVocabularyError(
                f"Cannot read tokenizer file {tokenizer_path}: {error}"
            ) from error
        except JSONDecodeError as error:
            raise TokenVocabularyError(
                "Invalid JSON in tokenizer file "
                f"{tokenizer_path} at line {error.lineno}, "
                f"column {error.colno}"
            ) from error

        try:
            tokenizer = _TokenizerFile.model_validate(raw_data)
            tokens_by_id = cls._merge_tokens(tokenizer)
            return cls(tokens_by_id=tokens_by_id)
        except ValidationError as error:
            raise TokenVocabularyError(
                f"Invalid tokenizer structure in {tokenizer_path}: {error}"
            ) from error

    @staticmethod
    def _merge_tokens(tokenizer: _TokenizerFile) -> dict[int, str]:
        """Merge base and added tokens while rejecting ID conflicts."""
        tokens_by_id: dict[int, str] = {}

        for token, token_id in tokenizer.model.vocab.items():
            TokenVocabulary._insert_token(
                tokens_by_id,
                token_id,
                token,
            )
        for added_token in tokenizer.added_tokens:
            TokenVocabulary._insert_token(
                tokens_by_id,
                added_token.token_id,
                added_token.content,
            )
        return tokens_by_id

    @staticmethod
    def _insert_token(
        tokens_by_id: dict[int, str],
        token_id: int,
        token: str,
    ) -> None:
        """Insert a token unless its ID already names another token."""
        if token_id in tokens_by_id and tokens_by_id[token_id] != token:
            raise TokenVocabularyError(
                f"Token id {token_id} is assigned more than once"
            )
        tokens_by_id[token_id] = token

    @property
    def size(self) -> int:
        """Return the number of declared token identifiers."""
        return len(self.tokens_by_id)

    @property
    def maximum_token_id(self) -> int:
        """Return the greatest token identifier in the vocabulary."""
        return max(self.tokens_by_id)

    def token_for_id(self, token_id: int) -> str:
        """Return the tokenizer representation for one identifier."""
        try:
            return self.tokens_by_id[token_id]
        except KeyError as error:
            raise TokenVocabularyError(
                f"Unknown token id: {token_id}"
            ) from error

    def validate_logits_size(self, logits_size: int) -> None:
        """Ensure every known token ID can index the logits vector."""
        if logits_size <= self.maximum_token_id:
            raise TokenVocabularyError(
                f"Logits size {logits_size} cannot represent token id "
                f"{self.maximum_token_id}"
            )
