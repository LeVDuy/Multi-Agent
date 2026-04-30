"""Point d'entrée CLI.

Usage :
    python main.py
"""
from graph.workflow import build_graph


def main() -> None:
    task = input("Tâche : ").strip()
    if not task:
        return

    graph = build_graph()
    result = graph.invoke({
        "task": task, "code": "", "review": "", "tests": "",
        "status": "", "iterations": 0,
        "execution_result": "", "execution_passed": False,
    })

    separator = "-" * 60
    print(f"\n{separator}")
    print("CODE GÉNÉRÉ")
    print(separator)
    print(result["code"])

    print(f"\n{separator}")
    print("REVUE")
    print(separator)
    print(result["review"])

    print(f"\n{separator}")
    print("TESTS UNITAIRES")
    print(separator)
    print(result["tests"])

    print(f"\n{separator}")
    status = "PASSED" if result["execution_passed"] else "FAILED"
    print(f"EXECUTION ({status}, iterations: {result['iterations']})")
    print(separator)
    print(result["execution_result"])


if __name__ == "__main__":
    main()
