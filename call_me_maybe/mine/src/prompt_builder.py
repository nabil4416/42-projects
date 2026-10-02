"""Build a function-calling prompt from validated project inputs.

Prompting guides the model; token-level validity will be enforced separately
by the constrained decoder. This module does not call the LLM or SDK.
"""

import json
from collections.abc import Sequence

from src.models import FunctionDefinition, PromptInput


def build_prompt(
    definitions: Sequence[FunctionDefinition],
    request: PromptInput,
) -> str:
    """Prepare a prompt using the supplied function definitions and request.

    Args:
        definitions: Already validated function definitions from the parser.
        request: An already validated user request.

    Raises:
        ValueError: If no functions are available or names are duplicated.
    """
    if not definitions:
        raise ValueError("Cannot build a prompt without function definitions")

    names = [definition.name for definition in definitions]
    if len(names) != len(set(names)):
        raise ValueError("Cannot build a prompt with duplicate function names")

    # Returns are intentionally omitted: function calling needs the callable
    # name and its input schema, not the type of the value returned later.
    functions_json = json.dumps(
        [
            {
                "name": definition.name,
                "description": definition.description,
                "parameters": {
                    parameter_name: parameter.model_dump(
                        mode="json",
                        by_alias=True,
                        exclude_none=True,
                    )
                    for parameter_name, parameter in (
                        definition.parameters.items()
                    )
                },
            }
            for definition in definitions
        ],
        ensure_ascii=False,
        separators=(",", ":"),
    )
    # JSON-encode the request so that quotes and newlines remain unambiguous.
    request_json = json.dumps(request.prompt, ensure_ascii=False)
    has_regex_argument = any(
        "regex" in parameter_name.casefold()
        for definition in definitions
        for parameter_name in definition.parameters
    )
    regex_instruction = (
        " For regex arguments, use the bare pattern without / delimiters or "
        "leading/trailing .*; prefer [0-9]+ for runs of digits."
        if has_regex_argument
        else ""
    )

    return (
        "Select exactly one function and extract its arguments. "
        "Use only the listed functions, exact parameter names, JSON types, "
        f"and enum values.{regex_instruction} "
        "Output only compact JSON with exactly this shape: "
        '{"fn_name":"name","args":{...}}. No prose or Markdown.\n'
        f"Functions:{functions_json}\n"
        f"Request:{request_json}\n"
    )
