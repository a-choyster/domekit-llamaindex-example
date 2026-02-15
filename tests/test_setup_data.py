"""Tests for setup_data.py — verifies the papers database is created correctly."""

import os
import sqlite3
import subprocess
import sys

import pytest

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "papers.db")
SETUP_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "setup_data.py")


@pytest.fixture(autouse=True)
def fresh_db():
    """Re-run setup_data before each test to ensure a clean database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_db_file_created():
    assert os.path.exists(DB_PATH)


def test_papers_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='papers'"
    )
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) == 1


def test_papers_table_has_correct_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("PRAGMA table_info(papers)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    assert columns == ["id", "title", "authors", "year", "journal", "abstract", "citations"]


def test_papers_table_has_12_rows():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM papers")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 12


def test_all_papers_have_non_empty_fields():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT title, authors, year, journal, abstract FROM papers")
    for row in cursor.fetchall():
        assert row[0], "title should not be empty"
        assert row[1], "authors should not be empty"
        assert row[2] > 0, "year should be positive"
        assert row[3], "journal should not be empty"
        assert row[4], "abstract should not be empty"
    conn.close()


def test_all_papers_have_positive_citations():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT title, citations FROM papers WHERE citations <= 0")
    bad = cursor.fetchall()
    conn.close()
    assert len(bad) == 0, f"Papers with non-positive citations: {bad}"


def test_setup_is_idempotent():
    """Running setup twice should not cause errors or duplicate data."""
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM papers")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 12
