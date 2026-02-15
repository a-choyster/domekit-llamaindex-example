# DomeKit + LlamaIndex Example

A LlamaIndex agent that uses [DomeKit](https://github.com/a-choyster/domekit) as its LLM backend for permission-controlled tool execution and audit logging. DomeKit is an open-source local-first AI runtime with enforced privacy boundaries. It exposes an OpenAI-compatible API, so LlamaIndex talks to it like any OpenAI endpoint -- but behind the scenes, every tool call is policy-checked against `domekit.yaml` and written to an append-only audit log.

## Prerequisites

- **Python 3.11+**
- **Ollama** installed with the `llama3.1:8b` model pulled:
  ```bash
  ollama pull llama3.1:8b
  ```
- **DomeKit** cloned and installed -- see [DomeKit repo](https://github.com/a-choyster/domekit) for instructions

## Setup

1. **Clone this repo**

   ```bash
   git clone https://github.com/a-choyster/domekit-llamaindex-example.git
   cd domekit-llamaindex-example
   ```

2. **Create a virtual environment and install dependencies**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```

3. **Generate the sample database**

   ```bash
   python setup_data.py
   ```

   This creates `data/papers.db` with ~12 sample CS/AI research papers.

4. **Start DomeKit with the included manifest**

   In a separate terminal, from the DomeKit installation directory:

   ```bash
   domekit serve --manifest /path/to/this/repo/domekit.yaml
   ```

   DomeKit will start listening on `http://localhost:8080`.

5. **Run the agent**

   ```bash
   python agent.py
   ```

## What to expect

The agent can answer questions about research papers stored in the SQLite database. Try prompts like:

- "What papers were published after 2020?"
- "Summarize the paper with the most citations."
- "Which authors have published on reinforcement learning?"

Under the hood, DomeKit intercepts every tool call the LlamaIndex agent makes and checks it against the policy in `domekit.yaml`. Only `sql_query` and `read_file` are allowed, only `data/papers.db` is accessible, and no outbound network requests are permitted.

## Checking the audit log

Every tool invocation is recorded in `audit.jsonl`. Inspect it with:

```bash
cat audit.jsonl | python -m json.tool --json-lines
```

Each entry contains the tool name, arguments, timestamp, and whether the call was allowed or denied.

## Links

- [DomeKit](https://github.com/a-choyster/domekit) -- the open-source local-first AI runtime
