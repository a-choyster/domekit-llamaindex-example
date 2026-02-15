# DomeKit + LlamaIndex Agent
#
# This agent talks to DomeKit's OpenAI-compatible endpoint on localhost:8080.
# From LlamaIndex's perspective, DomeKit is just another OpenAI API. But behind
# the scenes, DomeKit policy-checks every tool call against domekit.yaml and
# writes an append-only audit log to audit.jsonl. The agent never knows the
# difference -- privacy enforcement is invisible.

import os
import sqlite3

from llama_index.core import Settings
from llama_index.core.agent import ReActAgent
from llama_index.core.tools import FunctionTool
from llama_index.llms.openai import OpenAI

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "papers.db")


# ---------------------------------------------------------------------------
# LLM -- pointed at DomeKit instead of OpenAI
# ---------------------------------------------------------------------------

llm = OpenAI(
    model="llama3.1:8b",
    base_url="http://localhost:8080/v1",
    api_key="not-needed",
)

Settings.llm = llm


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

def sql_query(query: str) -> str:
    """Execute a read-only SQL query against the research papers database.

    The database has a single table called `papers` with columns:
        id, title, authors, year, journal, abstract, citations

    Args:
        query: A SELECT SQL statement to run against the papers database.

    Returns:
        The query results formatted as readable text.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        cursor = conn.execute(query)
        rows = cursor.fetchall()
        if not rows:
            return "No results found."
        # Format rows as readable text
        columns = rows[0].keys()
        lines = []
        for row in rows:
            parts = [f"{col}: {row[col]}" for col in columns]
            lines.append(" | ".join(parts))
        return "\n".join(lines)
    except Exception as e:
        return f"SQL error: {e}"
    finally:
        conn.close()


def read_file(file_path: str) -> str:
    """Read a text file from the data/ directory.

    Args:
        file_path: Path to the file, relative to the project root (must be inside data/).

    Returns:
        The contents of the file as a string.
    """
    base = os.path.dirname(__file__)
    full_path = os.path.normpath(os.path.join(base, file_path))
    # Basic safety check -- must stay inside data/
    data_dir = os.path.normpath(os.path.join(base, "data"))
    if not full_path.startswith(data_dir):
        return "Error: access denied. Only files inside data/ can be read."
    try:
        with open(full_path) as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {file_path}"


sql_tool = FunctionTool.from_defaults(fn=sql_query)
read_tool = FunctionTool.from_defaults(fn=read_file)


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------

agent = ReActAgent.from_tools(
    tools=[sql_tool, read_tool],
    llm=llm,
    verbose=True,
    system_prompt=(
        "You are a helpful research assistant with access to a SQLite database "
        "of academic papers. Use the sql_query tool to answer questions about "
        "papers, authors, publication years, journals, citations, and abstracts. "
        "The table is called `papers` with columns: id, title, authors, year, "
        "journal, abstract, citations. Always use SELECT queries only."
    ),
)


def main():
    print("Research Papers Agent (powered by DomeKit + LlamaIndex)")
    print("Type your question, or 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        response = agent.chat(user_input)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
