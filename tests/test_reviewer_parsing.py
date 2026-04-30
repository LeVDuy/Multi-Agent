"""Test du parsing reviewer : vérifie l'extraction de REVIEW, CODE et STATUS."""
from unittest.mock import MagicMock
from agents.reviewer import make_reviewer_node


def fake_llm(text):
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content=text)
    return llm


def state():
    return {
        "task": "Write a function", "code": "def foo(): pass",
        "review": "", "tests": "", "status": "", "iterations": 1,
        "execution_result": "", "execution_passed": False,
    }


def test_parse_approved():
    text = "--- REVIEW ---\nOK\n\n--- IMPROVED CODE ---\ndef foo(): return 1\n\n--- STATUS ---\napproved"
    result = make_reviewer_node(fake_llm(text))(state())
    assert result["status"] == "approved"
    assert "def foo(): return 1" in result["code"]


def test_parse_needs_fix():
    text = "--- REVIEW ---\nBug\n\n--- IMPROVED CODE ---\ndef foo(): return 2\n\n--- STATUS ---\nneeds_fix"
    result = make_reviewer_node(fake_llm(text))(state())
    assert result["status"] == "needs_fix"


def test_fallback_si_format_inconnu():
    result = make_reviewer_node(fake_llm("Réponse libre sans format."))(state())
    assert result["status"] == "approved"
    assert result["code"] == "def foo(): pass"
