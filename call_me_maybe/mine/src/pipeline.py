"""Orchestrate constrained function-call generation for every prompt."""

import json
from collections.abc import Callable, Sequence

from pydantic import ValidationError

from src.decoder import ConstrainedModel, DecodingError
from src.decoder import decode_function_call
from src.errors import GenerationError
from src.json_grammar import FunctionCallGrammar
from src.llm_router import choose_definition
from src.models import FunctionCall, FunctionDefinition
from src.models import OutputEntry, PromptInput
from src.prompt_builder import build_prompt
from src.token_vocabulary import TokenVocabulary


ProgressCallback = Callable[[int, int, OutputEntry], None]


def parse_generated_call(text: str) -> FunctionCall:
    """Parse the decoder's canonical JSON into the strict internal model."""
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as error:
        raise GenerationError(
            f"Decoder returned malformed JSON: {error.msg}"
        ) from error

    try:
        return FunctionCall.model_validate(payload)
    except ValidationError as error:
        raise GenerationError(
            f"Decoder returned an invalid function-call object: {error}"
        ) from error


def generate_results(
    definitions: Sequence[FunctionDefinition],
    prompts: Sequence[PromptInput],
    model: ConstrainedModel,
    vocabulary: TokenVocabulary,
    *,
    max_new_tokens: int = 64,
    on_progress: ProgressCallback | None = None,
) -> list[OutputEntry]:
    """Generate and validate one output entry for every input prompt."""
    results: list[OutputEntry] = []
    total = len(prompts)

    for index, prompt in enumerate(prompts, start=1):
        try:
            selected = choose_definition(
                definitions=definitions,
                request=prompt,
                model=model,
                vocabulary=vocabulary,
            )
            candidates = (selected,)
            grammar = FunctionCallGrammar(definitions=candidates)
            prepared_prompt = build_prompt(candidates, prompt)
            decoded = decode_function_call(
                model=model,
                grammar=grammar,
                vocabulary=vocabulary,
                prepared_prompt=prepared_prompt,
                max_new_tokens=max_new_tokens,
            )
            call = parse_generated_call(decoded.text)
        except (DecodingError, GenerationError) as error:
            raise GenerationError(
                f"Prompt {index}/{total} failed: {error}"
            ) from error

        entry = OutputEntry(
            prompt=prompt.prompt,
            fn_name=call.fn_name,
            args=call.args,
        )
        results.append(entry)
        if on_progress is not None:
            on_progress(index, total, entry)

    return results
