from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

from graph.state import AgentState

SYSTEM_PROMPT = """You are a senior code reviewer.
You will receive a Python code snippet. Analyse it and provide:
1. Potential bugs or logic errors.
2. Performance or security concerns.
3. Specific, actionable improvement suggestions.

After the analysis, provide an improved version of the code that applies your suggestions.

Finally, make a status decision:
- "approved" if the code is acceptable (only minor style issues, no critical bugs).
- "needs_fix" if the code has critical bugs or significant logic errors.

Format your response exactly as:
--- REVIEW ---
<your analysis here>

--- IMPROVED CODE ---
<improved python code here>

--- STATUS ---
approved

CRITICAL: If the user's request is in French, ALL docstrings and comments MUST be in French. If in English, use English. Never mix languages."""


def make_reviewer_node(llm: ChatOpenAI):
    """Retourne un nœud LangGraph qui évalue le code et décide s'il faut le renvoyer au codeur."""

    def reviewer_node(state: AgentState) -> dict:
        prompt = (
            f"Original user request:\n{state['task']}\n\n"
            f"Code to review:\n\n{state['code']}"
        )
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=prompt),
        ]
        response = llm.invoke(messages)
        content = response.content

        review_text = content
        improved_code = state["code"]  # fallback: keep original if parsing fails
        status = "approved"            # fallback: be optimistic if parsing fails

        if "--- IMPROVED CODE ---" in content:
            parts = content.split("--- IMPROVED CODE ---", 1)
            review_text = parts[0].replace("--- REVIEW ---", "").strip()
            remainder = parts[1]

            if "--- STATUS ---" in remainder:
                code_part, status_part = remainder.split("--- STATUS ---", 1)
                improved_code = code_part.strip()
                status = "needs_fix" if "needs_fix" in status_part.lower() else "approved"
            else:
                improved_code = remainder.strip()

        return {"review": review_text, "code": improved_code, "status": status}

    return reviewer_node
