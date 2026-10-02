"""Select the highest-logit token allowed by the JSON grammar."""

from collections.abc import Sequence
from typing import Protocol

import numpy as np

from src.errors import CallMeMaybeError
from src.json_grammar import FunctionCallGrammar
from src.token_vocabulary import TokenVocabulary, TokenVocabularyError


class TokenSelectionError(CallMeMaybeError):
    """Raised when constrained token selection cannot continue."""


class TokenDecoder(Protocol):
    """Public decoding operation needed during token selection."""

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decode generated token identifiers into text."""
        ...


def select_best_valid_token(
    model: TokenDecoder,
    grammar: FunctionCallGrammar,
    vocabulary: TokenVocabulary,
    generated_ids: Sequence[int],
    logits: Sequence[float],
) -> int:
    """Return the best-scoring token that preserves a valid prefix."""
    if len(logits) == 0:
        raise TokenSelectionError("Cannot select a token from empty logits")

    try:
        vocabulary.validate_logits_size(len(logits))
    except TokenVocabularyError as error:
        raise TokenSelectionError(str(error)) from error

    generated = list(generated_ids)
    current_text = model.decode(generated)
    if not grammar.is_valid_prefix(current_text):
        raise TokenSelectionError(
            "Generated tokens do not decode to a valid grammar prefix"
        )
    if grammar.is_complete(current_text):
        raise TokenSelectionError(
            "Function call is already complete; no token is required"
        )

    known_token_ids = tuple(vocabulary.tokens_by_id)
    logit_array = np.asarray(logits, dtype=np.float64)
    token_array = np.fromiter(
        known_token_ids,
        dtype=np.int64,
        count=len(known_token_ids),
    )
    known_logits = logit_array[token_array]
    if not np.isfinite(known_logits).all():
        raise TokenSelectionError(
            "Known vocabulary tokens must have finite logits"
        )

    ranking = np.lexsort((token_array, -known_logits))
    ranked_token_ids = token_array[ranking]
    for token_id in ranked_token_ids:
        candidate_id = int(token_id)
        candidate_text = model.decode([*generated, candidate_id])
        if candidate_text == current_text:
            continue
        if grammar.is_valid_prefix(candidate_text):
            return candidate_id

    raise TokenSelectionError(
        "No vocabulary token can continue the JSON grammar"
    )
