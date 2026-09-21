"""Application entry point for python -m src."""

import sys

from src.cli import parse_args
from src.errors import CallMeMaybeError
from src.io_json import load_function_definitions, load_prompts


def main() -> int:
    """Validate project inputs before the decoding phase is implemented."""
    args = parse_args()
    try:
        definitions = load_function_definitions(args.functions_definition)
        prompts = load_prompts(args.input)
    except CallMeMaybeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        f"Validated {len(definitions)} function definitions "
        f"and {len(prompts)} prompts."
    )
    print("The constrained decoding engine is the next implementation step.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
