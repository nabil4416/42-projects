"""Orchestrate constrained function-call generation for every prompt."""

import json
from collections.abc import Callable, Sequence
import re
from pydantic import ValidationError

from src.decoder import ConstrainedModel, DecodingError
from src.decoder import decode_function_call
from src.errors import GenerationError
from src.json_grammar import FunctionCallGrammar
from src.llm_router import choose_definition
from src.models import FunctionCall, FunctionDefinition
from src.models import OutputEntry, PromptInput, ValueType
from src.prompt_builder import build_prompt
from src.token_vocabulary import TokenVocabulary


ProgressCallback = Callable[[int, int, OutputEntry], None]


def normalize_arguments(
    call: FunctionCall,
    definition: FunctionDefinition,
) -> dict[str, object]:
    """Normalize JSON values to the exact declared parameter types.

    JSON does not distinguish ``3`` from ``3.0`` semantically, but Python
    callables may enforce ``float`` at runtime.  A schema ``number`` is
    therefore serialized as a float, while ``integer`` remains an int.
    """
    normalized: dict[str, object] = {}
    for name, parameter in definition.parameters.items():
        value = call.args[name]
        if parameter.type is ValueType.NUMBER and isinstance(value, int):
            value = float(value)
        normalized[name] = value
    return normalized


def find_non_source_string_arguments(
    call: FunctionCall,
    definition: FunctionDefinition,
    request: PromptInput,
) -> tuple[str, ...]:
    """Return string arguments whose value is absent from the request."""
    suspicious: list[str] = []

    for name, parameter in definition.parameters.items():
        if parameter.type is not ValueType.STRING:
            continue

        value = call.args[name]
        if isinstance(value, str) and value not in request.prompt:
            suspicious.append(name)

    return tuple(suspicious)


def source_string_candidates(
    request: PromptInput,
    *,
    max_words: int = 12,
) -> tuple[str, ...]:
    """Return plausible verbatim string spans from the request."""
    text = request.prompt
    candidates: set[str] = set()

    stripped = text.strip()
    if stripped:
        candidates.add(stripped)

    # Preserve explicitly quoted values without their quote delimiters.
    for match in re.finditer(r"""(['"])(.*?)\1""", text):
        value = match.group(2)
        if value:
            candidates.add(value)

    # Text following a colon is often an explicit supplied value.
    for index, character in enumerate(text):
        if character == ":":
            value = text[index + 1:].strip()
            if value:
                candidates.add(value)

    # Generate contiguous spans while preserving their original characters.
    words = list(re.finditer(r"\S+", text))
    for start in range(len(words)):
        limit = min(len(words), start + max_words)
        for end in range(start, limit):
            value = text[
                words[start].start():words[end].end()
            ].strip()
            if value:
                candidates.add(value)

    return tuple(
        sorted(
            candidates,
            key=lambda value: (-len(value), value),
        )
    )


def build_source_constrained_definition(
    definition: FunctionDefinition,
    request: PromptInput,
    suspicious: tuple[str, ...],
) -> FunctionDefinition | None:
    """Constrain one suspicious string argument to exact request substrings."""
    if len(suspicious) != 1:
        return None

    string_parameters = [
        name
        for name, parameter in definition.parameters.items()
        if parameter.type is ValueType.STRING
    ]

    if len(string_parameters) != 1:
        return None

    parameter_name = suspicious[0]
    if parameter_name != string_parameters[0]:
        return None

    candidates = explicit_source_string_candidates(request)
    if not candidates:
        return None

    parameters = dict(definition.parameters)
    parameter = parameters[parameter_name]
    parameters[parameter_name] = parameter.model_copy(
        update={"allowed_values": list(candidates)}
    )

    return definition.model_copy(
        update={"parameters": parameters}
    )


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


def explicit_source_string_candidates(
    request: PromptInput,
) -> tuple[str, ...]:
    """Return high-confidence explicit string values from the request."""
    _, separator, suffix = request.prompt.partition(":")
    if separator:
        value = suffix.strip()
        if value:
            return (value,)

    return ()


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

            suspicious = find_non_source_string_arguments(
                call,
                selected,
                prompt,
            )

            constrained_definition = build_source_constrained_definition(
                selected,
                prompt,
                suspicious,
            )

            if constrained_definition is not None:
                recovery_grammar = FunctionCallGrammar(
                    definitions=(constrained_definition,)
                )
                recovery_prompt = build_prompt(
                    (constrained_definition,),
                    prompt,
                )
                recovered = decode_function_call(
                    model=model,
                    grammar=recovery_grammar,
                    vocabulary=vocabulary,
                    prepared_prompt=recovery_prompt,
                    max_new_tokens=max_new_tokens,
                )
                call = parse_generated_call(recovered.text)

        except (DecodingError, GenerationError) as error:
            raise GenerationError(
                f"Prompt {index}/{total} failed: {error}"
            ) from error

        entry = OutputEntry(
            prompt=prompt.prompt,
            fn_name=call.fn_name,
            args=normalize_arguments(call, selected),
        )
        results.append(entry)
        if on_progress is not None:
            on_progress(index, total, entry)

    return results
