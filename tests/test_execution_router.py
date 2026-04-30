"""Test du routeur execution : vérifie le comportement après exécution des tests."""
from graph.workflow import execution_router, MAX_ITERATIONS


def state(passed=False, iterations=0):
    return {
        "task": "", "code": "", "review": "", "tests": "",
        "status": "", "iterations": iterations,
        "execution_result": "", "execution_passed": passed,
    }


def test_tests_passent_va_vers_end():
    assert execution_router(state(passed=True)) == "end"


def test_tests_echouent_retourne_au_coder():
    assert execution_router(state(passed=False, iterations=1)) == "coder"


def test_tests_echouent_bloque_a_la_limite():
    assert execution_router(state(passed=False, iterations=MAX_ITERATIONS)) == "end"
