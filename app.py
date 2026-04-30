"""Streamlit web UI for the Multi-Agent IT Team."""
import streamlit as st

from graph.workflow import build_graph

st.set_page_config(page_title="Équipe IT Multi-Agent", layout="wide")

st.title("Équipe IT Multi-Agent")
st.caption("Codeur · Reviewer · Testeur — propulsé par LM Studio (local)")

if "result" not in st.session_state:
    st.session_state.result = None

task = st.text_area(
    label="Décrivez la fonction ou le module Python que vous souhaitez",
    height=120,
    placeholder="Exemple : Écris une fonction qui parse un fichier CSV et retourne une liste de dictionnaires.",
)

col_run, col_reset = st.columns([1, 5])

with col_run:
    run = st.button("Lancer", disabled=not task.strip())

with col_reset:
    if st.button("Réinitialiser"):
        st.session_state.result = None
        st.rerun()

if run and task.strip():
    graph = build_graph()
    with st.spinner("Agents en cours d'exécution..."):
        st.session_state.result = graph.invoke({
            "task": task, "code": "", "review": "", "tests": "",
            "status": "", "iterations": 0,
            "execution_result": "", "execution_passed": False,
        })

if st.session_state.result:
    result = st.session_state.result
    tab_code, tab_review, tab_tests, tab_exec = st.tabs(
        ["Code", "Revue", "Tests unitaires", "Execution"]
    )

    with tab_code:
        st.code(result["code"], language="python")

    with tab_review:
        st.markdown(result["review"])

    with tab_tests:
        st.code(result["tests"], language="python")

    with tab_exec:
        if result["execution_passed"]:
            st.success(f"Tous les tests passent. (iterations: {result['iterations']})")
        else:
            st.error(f"Des tests ont echoue. (iterations: {result['iterations']})")
        st.code(result["execution_result"], language="text")
