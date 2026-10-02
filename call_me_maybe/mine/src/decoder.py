"""Token-by-token constrained decoding loop for function calls."""

from collections.abc import Sequence
from typing import Protocol

from pydantic import BaseModel, ConfigDict

from src.errors import CallMeMaybeError
from src.json_grammar import FunctionCallGrammar
from src.token_selector import TokenSelectionError
from src.token_selector import select_best_valid_token
from src.token_vocabulary import TokenVocabulary


class DecodingError(CallMeMaybeError):
    """Raised when constrained decoding cannot produce a complete call."""


class ConstrainedModel(Protocol):
    """Public model operations required by the decoding loop."""

    def encode(self, text: str) -> list[int]:
        """Encode the prepared prompt."""
        ...

    def decode(self, token_ids: Sequence[int]) -> str:
        """Decode generated token identifiers."""
        ...

    def next_token_logits(
        self,
        input_ids: Sequence[int],
    ) -> list[float]:
        """Return logits for the token following the full context."""
        ...


class DecodingResult(BaseModel):
    """Validated output of one constrained decoding run."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    text: str
    token_ids: tuple[int, ...]


def decode_function_call(
    model: ConstrainedModel,
    grammar: FunctionCallGrammar,
    vocabulary: TokenVocabulary,
    prepared_prompt: str,
    *,
    max_new_tokens: int = 128,
) -> DecodingResult:
    """Generate one complete function call under grammar constraints."""
    if not prepared_prompt.strip():
        raise DecodingError("Prepared prompt must not be empty")
    if type(max_new_tokens) is not int or max_new_tokens <= 0:
        raise DecodingError("max_new_tokens must be a positive integer")

    prompt_ids = model.encode(prepared_prompt)
    if not prompt_ids:
        raise DecodingError("Prepared prompt encoded to an empty token list")

    generated_ids: list[int] = []
    while True:
        generated_text = model.decode(generated_ids)
        if grammar.is_complete(generated_text):
            return DecodingResult(
                text=generated_text,
                token_ids=tuple(generated_ids),
            )

        if len(generated_ids) >= max_new_tokens:
            break

        forced_text = grammar.forced_continuation(generated_text)
        if forced_text:
            forced_ids = model.encode(generated_text + forced_text)
            forced_decoding = model.decode(forced_ids)
            if forced_decoding != generated_text + forced_text:
                raise DecodingError(
                    "Model tokenizer could not encode forced grammar text"
                )
            if len(forced_ids) > max_new_tokens:
                break
            generated_ids = forced_ids
            continue

        context_ids = [*prompt_ids, *generated_ids]
        logits = model.next_token_logits(context_ids)
        try:
            selected_id = select_best_valid_token(
                model=model,
                grammar=grammar,
                vocabulary=vocabulary,
                generated_ids=generated_ids,
                logits=logits,
            )
        except TokenSelectionError as error:
            step = len(generated_ids) + 1
            raise DecodingError(
                f"Token selection failed at generation step {step}: {error}"
            ) from error
        generated_ids.append(selected_id)

    generated_text = model.decode(generated_ids)
    if grammar.is_complete(generated_text):
        return DecodingResult(
            text=generated_text,
            token_ids=tuple(generated_ids),
        )
    raise DecodingError(
        f"Function call was not complete after {max_new_tokens} tokens"
    )
