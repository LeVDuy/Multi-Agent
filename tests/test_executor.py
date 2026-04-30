"""Test de l'executor : vérifie l'exécution réelle du code et des tests."""
from agents.executor import executor_node, strip_markdown_fences


def state(code, tests):
    return {
        "task": "", "code": code, "review": "", "tests": tests,
        "status": "", "iterations": 1,
        "execution_result": "", "execution_passed": False,
    }


def test_supprime_balises_python():
    assert strip_markdown_fences("```python\ndef foo(): pass\n```") == "def foo(): pass"


def test_garde_code_sans_balises():
    assert strip_markdown_fences("def foo(): pass") == "def foo(): pass"


def test_code_correct_passe():
    result = executor_node(state(
        code="def add(a, b):\n    return a + b",
        tests="def test_add():\n    assert add(1, 2) == 3",
    ))
    assert result["execution_passed"] is True


def test_code_bugge_echoue():
    result = executor_node(state(
        code="def add(a, b):\n    return a - b",
        tests="def test_add():\n    assert add(1, 2) == 3",
    ))
    assert result["execution_passed"] is False


def test_erreur_syntaxe_echoue():
    result = executor_node(state(
        code="def add(a, b)\n    return a + b",
        tests="def test_add():\n    assert add(1, 2) == 3",
    ))
    assert result["execution_passed"] is False

