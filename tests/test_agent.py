"""Tests for agent.py — verifies imports, configuration, and tool definitions."""

import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


def test_llamaindex_imports():
    """LlamaIndex packages are installed and importable."""
    from llama_index.core import Settings
    from llama_index.core.agent import ReActAgent
    from llama_index.core.tools import FunctionTool
    from llama_index.llms.openai_like import OpenAILike


def test_agent_module_imports():
    """agent.py imports without errors."""
    import agent


def test_llm_configured_for_domekit():
    """LLM points at DomeKit's local endpoint, not OpenAI."""
    import agent

    # Check the base URL contains localhost:8080
    base_url = str(agent.llm.api_base)
    assert "localhost:8080" in base_url


def test_two_tools_defined():
    """Agent should have sql_tool and read_tool."""
    import agent

    assert agent.sql_tool is not None
    assert agent.read_tool is not None


def test_sql_tool_function_works():
    """sql_query function should execute against the papers DB."""
    import agent

    # Setup DB first
    import subprocess
    setup = os.path.join(os.path.dirname(__file__), "..", "setup_data.py")
    subprocess.run([sys.executable, setup], check=True, capture_output=True)

    result = agent.sql_query("SELECT COUNT(*) as cnt FROM papers")
    assert "12" in result


def test_read_file_blocks_traversal():
    """read_file should block path traversal attempts."""
    import agent

    result = agent.read_file("../../etc/passwd")
    assert "denied" in result.lower() or "error" in result.lower()


def test_agent_object_exists():
    """The ReActAgent should be instantiated."""
    import agent

    assert agent.agent is not None
