# python-llm-agent

A lightweight Python LLM agent that uses OpenRouter/OpenAI tooling to inspect files, read content, write files, and execute Python code inside a sandboxed working directory.

## Overview

This project provides a simple AI-assisted code agent with:

- `main.py` as the entrypoint
- an OpenRouter-based chat completion loop
- function-calling support via `call_function.py`
- helper tools under `functions/` for file listing, reading, writing, and Python execution
- a sample sandbox workspace in `calculator/`

## Features

- List files and directories within the sandbox directory
- Read file contents safely with a maximum character limit
- Write or overwrite files inside the permitted working directory
- Execute Python files with optional arguments
- Sample calculator package to validate execution and file access

## Requirements

- Python 3.13+
- `openai==2.44.0`
- `python-dotenv==1.1.0`
- `uv==0.11.26`

## Setup

1. Install dependencies:

```bash
python -m pip install openai==2.44.0 python-dotenv==1.1.0 uv
```

2. Create a `.env` file in the repository root:

```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

## Usage

Run the agent with a prompt:

```bash
uv run main.py "Read calculator/main.py"
```

Enable verbose output:

```bash
uv run main.py "Read calculator/main.py" --verbose
```

The agent sends the prompt to an LLM, then may call helper functions to inspect or modify files under the sandbox.

## Available helper functions

The agent exposes these tools via `call_function.py`:

- `get_files_info(directory)`
  - List a directory's contents relative to the sandbox working directory
- `get_file_content(file_path)`
  - Return file contents with a maximum character limit
- `write_file(file_path, content)`
  - Create or overwrite a file, creating directories as needed
- `run_python_file(file_path, args)`
  - Execute a Python file and return stdout/stderr or errors

## Sandbox directory

All function calls use `calculator/` as the working directory, so operations are restricted to that folder.

## Sample calculator workspace

Included under `calculator/`:

- `calculator/main.py` — CLI calculator entrypoint
- `calculator/pkg/calculator.py` — parser and arithmetic evaluator
- `calculator/pkg/render.py` — JSON output formatter
- `calculator/tests.py` — calculator unit tests
- `calculator/lorem.txt` — sample text file

## Running tests

Run the calculator sample tests:

```bash
uv run calculator/tests.py
```

Test the helper functions directly:

```bash
uv run test_get_file_content.py
uv run test_get_files_info.py
uv run test_run_python_file.py
uv run test_write_file.py
```

## Notes

- The agent uses `openai.OpenAI` with `base_url="https://openrouter.ai/api/v1"`
- `OPENROUTER_API_KEY` must be set in the environment
- `call_function.py` currently routes all helper calls to `calculator/`
