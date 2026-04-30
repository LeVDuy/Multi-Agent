from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from graph.state import AgentState

SYSTEM_PROMPT = """You are a QA engineer specialising in Python testing.
You will receive a Python code snippet and a code review.
Write a complete pytest test suite that covers:
- Normal/happy path cases.
- Edge cases (empty input, boundary values, etc.).
- Error / exception cases.

Return only the pytest code block. No prose outside the code.
Write test comments and docstrings in the same language as the code's docstrings."""


def make_tester_node(llm: ChatOpenAI):
    """Retourne un nœud LangGraph qui rédige les tests pytest pour le code après revue."""

    def tester_node(state: AgentState) -> dict:
        prompt = (
            f"Original user request:\n{state['task']}\n\n"
            f"Code:\n\n{state['code']}\n\n"
            f"Review notes:\n\n{state['review']}"
        )
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
        response = llm.invoke(messages)
        return {"tests": response.content}

    return tester_node
