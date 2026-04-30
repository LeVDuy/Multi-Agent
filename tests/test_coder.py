"""Test du noeud coder : vérifie le choix du prompt et le compteur d'itérations."""
from unittest.mock import MagicMock
from agents.coder import make_coder_node, BASE_PROMPT, RETRY_PROMPT


def fake_llm():
    llm = MagicMock()
    llm.invoke.return_value = MagicMock(content="def foo(): pass")
    return llm


def state(iterations=0, review="", status=""):
    return {
        "task": "Write fibonacci", "code": "", "review": review,
        "tests": "", "status": status, "iterations": iterations,
        "execution_result": "", "execution_passed": False,
    }


def test_premier_essai_utilise_base_prompt():
    llm = fake_llm()
    make_coder_node(llm)(state(iterations=0))
    prompt = llm.invoke.call_args[0][0][0].content
    assert BASE_PROMPT in prompt


def test_retry_utilise_retry_prompt():
    llm = fake_llm()
    make_coder_node(llm)(state(iterations=1, review="Fix bug", status="needs_fix"))
    prompt = llm.invoke.call_args[0][0][0].content
    assert RETRY_PROMPT in prompt


def test_iterations_incremente():
    result = make_coder_node(fake_llm())(state(iterations=0))
    assert result["iterations"] == 1
