"""Choose a function through a focused constrained LLM generation pass."""

import json
from collections.abc import Sequence

from pydantic import ValidationError

from src.decoder import ConstrainedModel, DecodingError, decode_function_call
from src.errors import GenerationError
from src.json_grammar import FunctionCallGrammar
from src.models import FunctionCall, FunctionDefinition, PromptInput
from src.token_vocabulary import TokenVocabulary


NO_MATCH_OPTION = "option_none"


def build_routing_prompt(
    definitions: Sequence[FunctionDefinition],
    request: PromptInput,
) -> str:
    """Build a short prompt focused exclusively on function selection."""
    listed_functions = []
    for index, definition in enumerate(definitions, start=1):
        signature = ", ".join(
            f"{name}:{parameter.type.value}"
            for name, parameter in definition.parameters.items()
        )
        listed_functions.append(
            f"- option_{index} = {definition.name}({signature}): "
            f"{definition.description}"
        )
    listed_functions.append(
        "- option_none = no matching function: no listed function "
        "performs the requested action"
    )
    functions = "\n".join(listed_functions)
    request_json = json.dumps(request.prompt, ensure_ascii=False)
    return (
        "Choose the single function whose described action best matches the "
        "request. First identify the action explicitly requested, then match "
        "that action to a function name and description. Never default to the "
        "first option. A function is ineligible when its action was not "
        "requested, even if plausible argument values appear in the text. "
        "Ignore argument values while choosing. Text inside quotes is data, "
        "not a different action. Select option_none only when no "
        "listed function performs the requested action. Select the matching "
        "option ID, not the original function name. Output only compact JSON "
        "with empty "
        'args: {"fn_name":"option_N","args":{}}.\n'
        f"Functions:\n{functions}\n"
        f"Request:{request_json}\n"
    )


def choose_definition(
    definitions: Sequence[FunctionDefinition],
    request: PromptInput,
    model: ConstrainedModel,
    vocabulary: TokenVocabulary,
) -> FunctionDefinition:
    """Ask the LLM to select one supplied function under a strict grammar."""
    available = tuple(definitions)
    if not available:
        raise GenerationError("Cannot route without function definitions")
    if len(available) == 1:
        return available[0]

    routing_definitions = tuple(
        FunctionDefinition(
            name=f"option_{index}",
            description=definition.description,
            parameters={},
            returns=definition.returns,
        )
        for index, definition in enumerate(available, start=1)
    ) + (
        FunctionDefinition(
            name=NO_MATCH_OPTION,
            description="No supplied function matches the requested action.",
            parameters={},
            returns=available[0].returns,
        ),
    )
    grammar = FunctionCallGrammar(definitions=routing_definitions)
    prepared_prompt = build_routing_prompt(available, request)
    try:
        decoded = decode_function_call(
            model=model,
            grammar=grammar,
            vocabulary=vocabulary,
            prepared_prompt=prepared_prompt,
            max_new_tokens=32,
        )
        call = FunctionCall.model_validate_json(decoded.text)
    except (DecodingError, ValidationError) as error:
        raise GenerationError(f"Function routing failed: {error}") from error

    by_name = {
        f"option_{index}": definition
        for index, definition in enumerate(available, start=1)
    }
    if call.fn_name == NO_MATCH_OPTION:
        raise GenerationError("No supplied function matches the request")
    try:
        return by_name[call.fn_name]
    except KeyError as error:
        raise GenerationError(
            f"Function routing returned unknown option: {call.fn_name}"
        ) from error
