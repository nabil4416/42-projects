*This project has been created as part of the 42 curriculum by nkhotbi.*

# Call Me Maybe

## Description

Call Me Maybe converts natural-language requests into validated function calls.
It loads a list of available function definitions and a list of prompts, asks
`Qwen/Qwen3-0.6B` to choose the appropriate function and extract its arguments,
then writes the results as JSON.

The central requirement is that generation is constrained while it happens.
The program does not accept arbitrary model text and repair it afterwards.
At every generation step, it permits only tokens whose decoded text remains a
valid prefix of the expected JSON grammar.

Each output entry has exactly this shape:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "fn_name": "fn_add_numbers",
  "args": {
    "a": 2,
    "b": 3
  }
}
```

## Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Enough disk space for the Python environment and Qwen model files
- Internet access on the first run if the model is not already cached

The required model is downloaded through the supplied `llm_sdk`. An optional
Hugging Face token can be configured to avoid unauthenticated download limits,
but it is not required once the model is cached.

## Installation

Install the locked dependencies from the project root:

```bash
make install
```

The equivalent direct command is:

```bash
uv sync
```

## Usage

Run the supplied input files with the default output path:

```bash
make run
```

This executes:

```bash
uv run python -m src
```

Default paths:

- function definitions: `data/input/functions_definition.json`
- prompts: `data/input/function_calling_tests.json`
- results: `data/output/function_calling_results.json`

Custom paths are supported:

```bash
uv run python -m src \
  --functions_definition path/to/functions.json \
  --input path/to/prompts.json \
  --output path/to/results.json
```

The output directory is created automatically. The result file is written
atomically through a temporary file, so an interrupted write cannot leave a
partially written JSON result at the final path.

## Algorithm

For each prompt, the program performs the following steps:

1. Parse and validate both input files with strict Pydantic models.
2. Load `Qwen/Qwen3-0.6B` through the public API of the supplied `llm_sdk`.
3. Load and validate the model vocabulary from `tokenizer.json`.
4. Ask the LLM to select one function in a short constrained routing pass.
5. Represent routing candidates with neutral identifiers such as `option_1`
   and map the selected identifier back to the original function definition.
6. Build a second prompt containing only the selected function and its schema.
7. Generate the function call token by token under the JSON grammar.
8. Validate the completed call and add the original prompt to the output entry.
9. Write all results as one JSON array.

At a generation choice point, token logits are ranked from highest to lowest.
The decoder selects the highest-scoring token whose decoded text is still a
valid grammar prefix. When the grammar has only one possible continuation, the
decoder inserts that deterministic text without an additional logits request.
Generation stops only when the complete canonical JSON object is valid.

The grammar enforces:

- a declared function name;
- exact argument names and their declared order;
- required arguments;
- JSON strings with valid escaping;
- JSON numbers and integers;
- booleans and null values;
- declared enum values;
- no extra keys, prose, Markdown, or trailing text.

## Design decisions

### Two constrained LLM passes

Function selection is made by the LLM, as required by the subject. A focused
routing pass first chooses among all supplied definitions. Argument extraction
then runs with only that selected definition. This reduces the second grammar's
search space and makes generation faster and more reliable.

Neutral routing identifiers prevent a shared name prefix such as `fn_` from
dominating the first token decision. They do not encode keywords or manually
choose a function: the LLM still makes the semantic selection from every
function name and description.

### Prefix grammar instead of post-processing

`FunctionCallGrammar` recognizes both complete calls and incomplete prefixes.
Invalid branches are rejected before a token is appended. The generated result
therefore already satisfies the expected structure and does not depend on a
JSON repair step.

### Public SDK boundary

`QwenModel` is a small adapter around the public `llm_sdk` methods for encoding,
decoding, logits retrieval, and tokenizer-file access. Application code does
not import or call the underlying model framework directly.

### Strict validation and explicit failures

Pydantic rejects unknown fields and malformed schemas. File, tokenizer,
generation, and output errors are translated into clear application errors.
The CLI exits with a non-zero status instead of producing an unreliable file.

## Project structure

```text
.
├── data/input/              supplied prompts and function definitions
├── llm_sdk/                 SDK supplied for the project
├── src/
│   ├── __main__.py          command-line orchestration
│   ├── cli.py               command-line arguments
│   ├── decoder.py           constrained generation loop
│   ├── io_json.py           input/output and validation errors
│   ├── json_grammar.py      prefix-aware function-call grammar
│   ├── llm_router.py        constrained LLM function selection
│   ├── model.py             public SDK adapter
│   ├── models.py            Pydantic data models
│   ├── pipeline.py          multi-prompt generation pipeline
│   ├── prompt_builder.py    extraction prompt construction
│   ├── token_selector.py    highest-logit valid-token selection
│   └── token_vocabulary.py  tokenizer vocabulary loading
└── tests/                   unit and integration-style tests
```

`data/output/` is intentionally ignored by Git because it contains generated
runtime output.

## Testing and quality checks

Run the complete test suite:

```bash
make test
```

Run the required lint and type checks:

```bash
make lint
```

Run mypy with its strict preset:

```bash
make lint-strict
```

Debug the application with Python's debugger:

```bash
make debug
```

Remove Python and test caches:

```bash
make clean
```

The test suite covers malformed and missing files, strict Pydantic models,
tokenizer loading, JSON prefix grammar states, valid-token selection, forced
grammar continuations, routing, multi-prompt orchestration, output writing,
and command-line error handling. Model-facing tests use deterministic doubles,
so routine tests do not download or load Qwen.

Final verification on the supplied data produced:

- 150 passing pytest cases;
- no Flake8 errors;
- no mypy errors with `--strict`;
- 11 correct function calls out of 11 supplied prompts;
- valid arguments for all 11 calls;
- 145.718 seconds of measured generation time;
- 2 minutes 41.056 seconds of total wall-clock time, including model loading.

These measurements were observed on a personal Linux computer and may vary by
hardware, cache state, and model-download availability.

## Challenges and lessons learned

The main difficulty was not merely producing JSON, but guaranteeing that every
intermediate token could still lead to a valid typed function call. Implementing
a prefix-aware grammar required explicit handling of partial strings, escapes,
numbers, literals, enum values, and canonical separators.

A second challenge was reliable function selection. Routing directly with the
original names introduced tokenization bias because every supplied name begins
with `fn_`. Neutral option identifiers removed that shared-prefix bias while
preserving the required LLM-based semantic decision.

Performance also mattered because checking every possible vocabulary token can
be expensive. Ranking logits with NumPy and inserting grammar-forced text without
an inference call kept the complete supplied workload below the five-minute
limit in the measured run.

## Resources and AI usage

Documentation consulted during development:

- [Python documentation](https://docs.python.org/3/)
- [Pydantic documentation](https://docs.pydantic.dev/)
- [NumPy documentation](https://numpy.org/doc/)
- [uv documentation](https://docs.astral.sh/uv/)
- [Qwen3-0.6B model page](https://huggingface.co/Qwen/Qwen3-0.6B)
- the project subject, evaluation criteria, supplied data, and supplied
  `llm_sdk` source code

AI tools, including ChatGPT/Codex, were used for architecture discussion,
debugging support, test-case suggestions, code review, and documentation
drafting. Suggested changes were inspected, adapted to the project constraints,
and verified with the automated test suite, strict static analysis, and real
Qwen executions on all supplied prompts.

## Known limitations

- Decoding is greedy and deterministic; it selects the highest-logit valid
  token rather than sampling alternatives.
- Performance depends strongly on the available CPU/GPU and model cache.
- The grammar supports the JSON value types declared by the project schema; it
  is not intended to be a general-purpose JSON Schema engine.
- Semantic correctness still depends on the small language model, even though
  structural correctness is guaranteed by the grammar.
