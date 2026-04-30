from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

from graph.state import AgentState
from agents.coder import make_coder_node
from agents.reviewer import make_reviewer_node
from agents.tester import make_tester_node
from agents.executor import executor_node
from config.settings import (
    LM_STUDIO_BASE_URL,
    LM_STUDIO_MODEL,
    LM_STUDIO_API_KEY,
    TEMPERATURE,
)

MAX_ITERATIONS = 3


def review_router(state: AgentState) -> str:
    """Décide si le code doit retourner au codeur ou passer au testeur.

    Retourne au codeur uniquement si :
    - Le reviewer a marqué le code comme "needs_fix"
    - Et le nombre maximum d'itérations n'a pas été atteint.
    """
    if state["status"] == "needs_fix" and state["iterations"] < MAX_ITERATIONS:
        return "coder"
    return "tester"


def execution_router(state: AgentState) -> str:
    """Décide si les tests ont réussi ou s'il faut renvoyer au codeur.

    Renvoie au codeur uniquement si :
    - Les tests ont échoué
    - Et le nombre maximum d'itérations n'a pas été atteint.
    """
    if not state["execution_passed"] and state["iterations"] < MAX_ITERATIONS:
        return "coder"
    return "end"


def build_graph():
    """Construit et compile le workflow LangGraph multi-agent.

    Flux :
        coder -> reviewer -> [needs_fix? -> coder] -> tester -> executor
        executor -> [failed? -> coder] -> END
    """
    llm = ChatOpenAI(
        model=LM_STUDIO_MODEL,
        base_url=LM_STUDIO_BASE_URL,
        api_key=LM_STUDIO_API_KEY,
        temperature=TEMPERATURE,
    )

    graph = StateGraph(AgentState)
    graph.add_node("coder", make_coder_node(llm))
    graph.add_node("reviewer", make_reviewer_node(llm))
    graph.add_node("tester", make_tester_node(llm))
    graph.add_node("executor", executor_node)

    graph.add_edge(START, "coder")
    graph.add_edge("coder", "reviewer")
    graph.add_conditional_edges(
        "reviewer",
        review_router,
        {"coder": "coder", "tester": "tester"},
    )
    graph.add_edge("tester", "executor")
    graph.add_conditional_edges(
        "executor",
        execution_router,
        {"coder": "coder", "end": END},
    )

    return graph.compile()
