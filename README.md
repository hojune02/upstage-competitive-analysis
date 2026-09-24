# Document extraction comparison

This repository compares structured extraction from documents with the OpenAI and Claude APIs. The scripts use the same invoice or medical prompt for each provider and save the raw response, latency, token usage, and an estimated API cost in JSON.

It is a small testbed, not a model ranking. The [`results/`](results/) directory contains example runs; there is no labeled answer set or automated accuracy score here. Read the source documents and outputs together before drawing a conclusion about either model.

## Repository map

- [`prompts.py`](prompts.py) defines the invoice and medical extraction instructions.
- [`run_openai.py`](run_openai.py) calls the OpenAI Responses API.
- [`run_claude.py`](run_claude.py) calls the Anthropic Messages API.
- [`documents/`](documents/) contains the example inputs; [`results/`](results/) contains saved outputs.

Both scripts accept `--file`, `--workflow invoice|medical`, and an optional `--runs` count. They require the relevant provider SDK, `python-dotenv`, and a valid API key in the environment. Provider prices and model names are configured in the scripts; verify current pricing before using the cost estimates.

Check that you have permission to process and publish any new documents before adding them to this repository, especially documents containing personal or medical details.
