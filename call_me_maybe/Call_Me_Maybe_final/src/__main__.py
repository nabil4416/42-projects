"""Application entry point for python -m src."""

import sys
from time import perf_counter

from src.cli import parse_args
from src.errors import CallMeMaybeError, ModelSetupError
from src.io_json import load_function_definitions, load_prompts, write_results
from src.model import QwenModel
from src.models import OutputEntry
from src.pipeline import generate_results
from src.token_vocabulary import TokenVocabulary


def _show_progress(index: int, total: int, entry: OutputEntry) -> None:
    """Report completed prompts without exposing internal model reasoning."""
    print(f"[{index}/{total}] {entry.fn_name}")


def _load_runtime() -> tuple[QwenModel, TokenVocabulary]:
    """Initialize Qwen and its vocabulary with a clear CLI failure."""
    try:
        model = QwenModel()
        vocabulary = TokenVocabulary.from_file(
            model.tokenizer_file_path()
        )
        return model, vocabulary
    except Exception as error:
        raise ModelSetupError(
            f"Could not initialize Qwen runtime: {error}"
        ) from error


def main(argv: list[str] | None = None) -> int:
    """Generate all constrained calls and write the requested JSON file."""
    args = parse_args(argv)
    try:
        definitions = load_function_definitions(args.functions_definition)
        prompts = load_prompts(args.input)
        print(
            f"Loaded {len(definitions)} function definitions "
            f"and {len(prompts)} prompts."
        )
        print("Loading Qwen/Qwen3-0.6B...")
        model, vocabulary = _load_runtime()

        started = perf_counter()
        results = generate_results(
            definitions=definitions,
            prompts=prompts,
            model=model,
            vocabulary=vocabulary,
            on_progress=_show_progress,
        )
        write_results(args.output, results)
        elapsed = perf_counter() - started
    except CallMeMaybeError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    print(
        f"Wrote {len(results)} results to {args.output} "
        f"in {elapsed:.3f} seconds."
    )
    return 0


try:
    raise SystemExit(main())
except KeyboardInterrupt:
    print("\nInterrupted by user.")
    raise SystemExit(130)


if __name__ == "__main__":
    raise SystemExit(main())
