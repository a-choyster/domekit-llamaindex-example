"""Tests for domekit.yaml — verifies manifest structure and policy."""

import os

import yaml
import pytest

MANIFEST_PATH = os.path.join(os.path.dirname(__file__), "..", "domekit.yaml")


@pytest.fixture
def manifest():
    with open(MANIFEST_PATH) as f:
        return yaml.safe_load(f)


def test_manifest_loads(manifest):
    assert manifest is not None


def test_app_name(manifest):
    assert manifest["app"]["name"] == "llamaindex-example"


def test_network_outbound_deny(manifest):
    assert manifest["policy"]["network"]["outbound"] == "deny"


def test_tools_allow_list(manifest):
    tools = manifest["policy"]["tools"]["allow"]
    assert "sql_query" in tools
    assert "read_file" in tools


def test_sqlite_allow(manifest):
    assert "data/papers.db" in manifest["policy"]["data"]["sqlite"]["allow"]


def test_filesystem_no_writes(manifest):
    assert manifest["policy"]["data"]["filesystem"]["allow_write"] == []


def test_audit_path(manifest):
    assert manifest["audit"]["path"] == "audit.jsonl"
