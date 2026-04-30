from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from graph.state import AgentState

BASE_PROMPT = """You are a senior Python developer.
Write clean, well-structured Python code with:
- Clear docstrings for every function and class.
- Type annotations on all function signatures.
- Meaningful variable names.

Return only the Python code block. No prose, no explanation outside the code.
CRITICAL: If the user's request is in French, ALL docstrings and comments MUST be in French. If in English, use English. Never mix languages."""

RETRY_PROMPT = """You are a senior Python developer.
Your previous code was reviewed and needs improvement.
Address every point raised in the review below, then rewrite the code completely.

Return only the Python code block. No prose, no explanation outside the code.
CRITICAL: If the user's request is in French, ALL docstrings and comments MUST be in French. If in English, use English. Never mix languages."""


def make_coder_node(llm: ChatOpenAI):
    """Retourne un nœud LangGraph qui génère (ou régénère) du code Python."""

    def coder_node(state: AgentState) -> dict:
        if state["iterations"] == 0:
            # First attempt — no prior review
            system_prompt = BASE_PROMPT
            user_message = state["task"]
        else:
            # Re-attempt — include reviewer feedback and/or execution errors
            system_prompt = RETRY_PROMPT
            user_message = f"Original task: {state['task']}\n\n"

            if state.get("review"):
                user_message += f"Reviewer feedback:\n{state['review']}\n\n"

            if state.get("execution_result") and not state.get("execution_passed"):
                user_message += f"Test execution errors:\n{state['execution_result']}"

        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
        response = llm.invoke(messages)
        return {"code": response.content, "iterations": state["iterations"] + 1}

    return coder_node
