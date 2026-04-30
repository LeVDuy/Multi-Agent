"""Test du routeur review : vérifie que le routeur envoie au bon noeud."""
from graph.workflow import review_router, MAX_ITERATIONS


def state(status="", iterations=0):
    return {
        "task": "", "code": "", "review": "", "tests": "",
        "status": status, "iterations": iterations,
        "execution_result": "", "execution_passed": False,
    }


def test_approved_va_vers_tester():
    assert review_router(state("approved", 0)) == "tester"


def test_approved_ignore_iterations():
    assert review_router(state("approved", MAX_ITERATIONS)) == "tester"


def test_needs_fix_retourne_au_coder():
    assert review_router(state("needs_fix", 1)) == "coder"


def test_needs_fix_bloque_a_la_limite():
    assert review_router(state("needs_fix", MAX_ITERATIONS)) == "tester"
