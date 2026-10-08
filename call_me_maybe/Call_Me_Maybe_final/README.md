*This project has been created as part of the 42 curriculum by nkhotbi.*

# Call Me Maybe

## Description

Call Me Maybe converts natural-language requests into structured function calls.

The program reads a list of available function definitions and a list of natural-language
prompts, uses `Qwen/Qwen3-0.6B` to select the appropriate function and extract its
arguments, and writes the results to a JSON file.

The central requirement of the project is **constrained decoding**. The program does not
simply ask the language model to produce valid JSON and repair it afterwards. Instead,
generation is constrained while it happens: at each step, only token continuations that
remain compatible with the expected JSON structure and function schema are accepted.

The final output is written to:

```text
data/output/function_calls.json
```

Each entry contains exactly:

```json
{
  "prompt": "What is the sum of 2 and 3?",
  "name": "fn_add_numbers",
  "parameters": {
    "a": 2.0,
    "b": 3.0
  }
}
```

The program keeps its internal generated call representation separate from the final
subject output format. Internally, the constrained decoder works with a function name
and its extracted arguments; the output layer serializes the validated result using the
required `prompt`, `name`, and `parameters` keys.

## Instructions

### Requirements

- Python 3.10 or newer
- [`uv`](https://docs.astral.sh/uv/)
- Enough disk space for the Python environment and Qwen model files
- Internet access on the first run if the model is not already cached

The project uses the supplied `llm_sdk` to interact with `Qwen/Qwen3-0.6B`.

An optional Hugging Face token can be configured to avoid unauthenticated download
limits, but it is not required once the model is cached.

### Installation

Install the locked dependencies from the project root:

```bash
make install
```

Equivalent command:

```bash
uv sync
```

### Run

Run the project with the default input and output paths:

```bash
make run
```

Equivalent command:

```bash
uv run python -m src
```

Default paths:

- function definitions: `data/input/functions_definition.json`
- prompts: `data/input/function_calling_tests.json`
- results: `data/output/function_calls.json`

Custom paths are supported:

```bash
uv run python -m src \
  --functions_definition path/to/functions_definition.json \
  --input path/to/function_calling_tests.json \
  --output path/to/function_calls.json
```

The output directory is created automatically.

The result file is written atomically through a temporary file before replacing the
final destination, preventing a partially written JSON file from being left behind if
writing fails.

### Other Makefile commands

Run the test suite:

```bash
make test
```

Run lint and type checks:

```bash
make lint
```

Run strict type checks:

```bash
make lint-strict
```

Run the application with Python's debugger:

```bash
make debug
```

Remove Python and test caches:

```bash
make clean
```

## Example Usage

With the supplied inputs:

```bash
uv run python -m src
```

the program reads:

```text
data/input/functions_definition.json
data/input/function_calling_tests.json
```

and creates:

```text
data/output/function_calls.json
```

Example output:

```json
[
  {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {
      "a": 2.0,
      "b": 3.0
    }
  },
  {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {
      "s": "hello"
    }
  }
]
```

## Algorithm Explanation

For each prompt, the program performs the following steps:

1. Parse and validate the function definitions and prompt files with strict Pydantic
   models.
2. Load `Qwen/Qwen3-0.6B` through the public interface of the supplied `llm_sdk`.
3. Load the tokenizer vocabulary used to map token IDs to their decoded text.
4. Run a constrained routing pass to select one function.
5. Represent routing candidates with neutral identifiers such as `option_1`,
   `option_2`, and so on.
6. Map the selected neutral identifier back to the original function definition.
7. Build a second prompt containing only the selected function and its schema.
8. Generate the function call token by token under `FunctionCallGrammar`.
9. Validate the completed internal call.
10. Attach the original natural-language prompt.
11. Serialize the validated result using exactly `prompt`, `name`, and `parameters`.
12. Write all entries to `data/output/function_calls.json` as one JSON array.

### Constrained token selection

Language models produce logits for possible next tokens. Normally, the next token could
simply be chosen from those logits.

This project adds a structural constraint before accepting a token.

At each generation step:

1. The model produces next-token logits.
2. Candidate tokens are ranked by model score.
3. The decoder checks whether appending a candidate's decoded text would keep the
   current output a valid prefix of the required JSON/function-call grammar.
4. Invalid candidates are rejected.
5. The highest-scoring valid candidate is selected.
6. If the grammar has only one possible continuation, that deterministic text can be
   inserted without an additional model logits request.

Generation stops only when the complete canonical function-call object is valid.

The grammar enforces:

- a function name from the supplied definitions;
- the expected argument names;
- required arguments;
- the declared argument types;
- declared enum values when present;
- valid JSON strings and escaping;
- valid JSON numbers and integers;
- booleans and null values;
- no unexpected keys;
- no Markdown, prose, or trailing text.

The final serialized file therefore remains valid JSON and follows the output contract.

## Design Decisions

### Two constrained LLM passes

The project separates **function selection** from **argument extraction**.

The first pass asks the LLM to choose the function. The second pass performs constrained
generation using only the selected function definition.

This keeps the extraction grammar smaller and reduces the number of possibilities that
must be considered during argument generation.

### Neutral routing identifiers

Routing candidates use identifiers such as:

```text
option_1
option_2
option_3
```

rather than making constrained generation choose directly between the original function
names.

The original function names share prefixes such as `fn_`, which can influence token-level
generation. Neutral option identifiers reduce that shared-prefix effect while preserving
LLM-based semantic selection.

The prompt still contains each original function name and description, so the model makes
the semantic decision. After selection, the option is mapped back to the real function
definition.

An additional `option_none` candidate is included so the router has a constrained
way to represent "no matching function". However, because the semantic choice is still
made by the small language model, unrelated prompts may still be routed incorrectly
instead of selecting `option_none`.

### Prefix-aware grammar instead of JSON repair

`FunctionCallGrammar` accepts valid incomplete prefixes as well as complete calls.

A candidate token is rejected before it is appended if its decoded text would make the
current output impossible to complete according to the schema.

The program therefore does not depend on repairing malformed model output after
generation.

### Public `llm_sdk` boundary

`QwenModel` acts as an adapter around the public `llm_sdk` functionality needed by the
project, including:

- text encoding;
- token decoding;
- logits retrieval;
- tokenizer/vocabulary file access.

The project does not rely on private SDK methods or attributes.

### Strict validation

Pydantic models validate the input structures and reject unexpected fields.

The project also handles expected file and generation failures through explicit
application errors instead of allowing uncontrolled exceptions to terminate execution.

## Project Structure

```text
.
├── data/
│   └── input/                    supplied prompts and function definitions
├── llm_sdk/                      SDK supplied for the project
├── src/
│   ├── __main__.py               command-line orchestration
│   ├── cli.py                    command-line arguments and default paths
│   ├── decoder.py                constrained generation loop
│   ├── io_json.py                JSON input/output and file error handling
│   ├── json_grammar.py           prefix-aware function-call grammar
│   ├── llm_router.py             constrained LLM function selection
│   ├── model.py                  public SDK adapter
│   ├── models.py                 Pydantic data models
│   ├── pipeline.py               multi-prompt generation pipeline
│   ├── prompt_builder.py         extraction prompt construction
│   ├── token_selector.py         valid-token selection from logits
│   └── token_vocabulary.py       tokenizer vocabulary loading
└── tests/                        unit and integration-style tests
```

`data/output/` contains generated runtime output and is intentionally excluded from the
repository.

## Testing Strategy

The project includes automated tests for the main components of the implementation,
including:

- missing and malformed JSON input files;
- strict Pydantic validation;
- tokenizer vocabulary loading;
- JSON grammar prefix states;
- valid-token selection;
- grammar-forced continuations;
- function routing;
- pipeline orchestration;
- output serialization;
- command-line error handling.

Model-facing unit tests use deterministic test doubles where appropriate, so routine
tests do not need to load the full Qwen model.

The complete test suite can be run with:

```bash
uv run pytest
```

or:

```bash
make test
```

The current test suite contains 162 tests.

Real runs are also performed with `Qwen/Qwen3-0.6B` on the supplied prompt set rather
than relying only on mocked model behavior.

## Performance Analysis

The subject requires near-perfect function-selection and argument-extraction accuracy,
100% parseable schema-compliant JSON, and processing of the complete prompt set in under
five minutes.

On the supplied 11-prompt dataset, the current implementation has produced:

- 10 correct function calls out of 11 prompts (`90.9%`);
- valid structured output in `data/output/function_calls.json`;
- complete generation within the five-minute limit in observed runs.

Observed execution time varies with hardware, whether model files are already cached,
and model-loading conditions.

The remaining errors are semantic routing errors rather than malformed JSON: constrained
decoding guarantees structure and schema compatibility, but it cannot guarantee that a
small language model always makes the correct semantic choice.

## Challenges Faced

### Reliable semantic routing

One of the main difficulties was function selection.

Selecting directly among the original function names exposed tokenization effects caused
by shared prefixes such as `fn_`. The routing stage was therefore separated from argument
extraction and neutral `option_N` identifiers were introduced.

This improved routing reliability while keeping the function choice LLM-driven rather
than replacing it with keyword rules or hardcoded heuristics.

### Schema-constrained generation

The decoder must accept incomplete text while rejecting any prefix that can no longer
lead to a valid call.

This required handling:

- partial JSON strings;
- escaped characters;
- numbers and integers;
- booleans and null values;
- enum values;
- separators and delimiters;
- exact function and parameter names.

### Performance

Checking possible vocabulary continuations can be expensive.

The implementation reduces unnecessary model work by ranking token logits and by directly
inserting grammar-forced continuations when only one continuation is possible.

This keeps complete runs below the subject's five-minute target on the tested system.

### Output contract

The constrained decoder uses an internal representation suited to generation, while the
subject requires the final file to contain exactly:

```text
prompt
name
parameters
```

The output layer explicitly converts the validated internal result into that external
format before writing `data/output/function_calls.json`.

## Known Limitations

- `option_none` provides a valid no-match route, but the small LLM may still
  misclassify an unrelated prompt and select an existing function instead.
- Semantic function selection still depends on `Qwen/Qwen3-0.6B`.
- Constrained decoding guarantees structural/schema validity, not perfect semantic
  understanding.
- Decoding is greedy: the implementation selects the highest-scoring valid continuation
  rather than sampling alternatives.
- Performance depends on hardware and model-cache state.
- The grammar implements the value types required by this project and is not intended to
  be a general-purpose JSON Schema engine.

## Resources

Documentation and material used during development:

- Python documentation: https://docs.python.org/3/
- Pydantic documentation: https://docs.pydantic.dev/
- NumPy documentation: https://numpy.org/doc/
- uv documentation: https://docs.astral.sh/uv/
- Qwen3-0.6B model documentation
- the official Call Me Maybe subject
- the supplied `llm_sdk` source code
- the supplied input data

### AI Usage

AI tools, including ChatGPT/Codex, were used for:

- discussing architecture choices;
- reviewing implementation ideas;
- debugging support;
- suggesting test cases;
- reviewing code;
- drafting and improving documentation;
- preparing explanations of constrained decoding and the project architecture.

AI-generated suggestions were reviewed and adapted before being integrated. Changes were
validated with the project's automated tests and real executions using
`Qwen/Qwen3-0.6B`.
