"""Command-line argument parsing."""

import argparse
from collections.abc import Sequence
from pathlib import Path


DEFAULT_FUNCTIONS = Path("data/input/functions_definition.json")
DEFAULT_INPUT = Path("data/input/function_calling_tests.json")
DEFAULT_OUTPUT = Path("data/output/function_calls.json")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    """Parse paths accepted by the mandatory command."""
    parser = argparse.ArgumentParser(
        description="Generate constrained function calls from prompts."
    )
    parser.add_argument(
        "--functions_definition",
        type=Path,
        default=DEFAULT_FUNCTIONS,
        help="path to the JSON function definitions",
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=DEFAULT_INPUT,
        help="path to the JSON prompts",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="path to the generated JSON results",
    )
    return parser.parse_args(argv)
