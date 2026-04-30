import os
import subprocess
import sys
import tempfile
import re

from graph.state import AgentState


def strip_markdown_fences(text: str) -> str:
    """Supprime les blocs ```python ... ``` autour du code si présents."""
    text = text.strip()
    pattern = r"^```(?:python)?\s*\n(.*?)```\s*$"
    match = re.match(pattern, text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text


def executor_node(state: AgentState) -> dict:
    """Exécute le code + les tests dans un répertoire temporaire via subprocess.

    Écrit le code dans module.py et les tests dans test_module.py,
    puis lance pytest. Retourne le résultat (stdout/stderr) et le statut.
    """
    code = strip_markdown_fences(state["code"])
    tests = strip_markdown_fences(state["tests"])

    with tempfile.TemporaryDirectory() as tmpdir:
        code_path = os.path.join(tmpdir, "module.py")
        test_path = os.path.join(tmpdir, "test_module.py")

        with open(code_path, "w") as f:
            f.write(code)

        test_content = f"from module import *\n\n{tests}"
        with open(test_path, "w") as f:
            f.write(test_content)

        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_path, "-v", "--tb=short"],
            capture_output=True,
            text=True,
            timeout=30,
            cwd=tmpdir,
        )

    output = result.stdout + result.stderr
    passed = result.returncode == 0

    return {"execution_result": output, "execution_passed": passed}
