from typing import TypedDict


class AgentState(TypedDict):
    """État partagé entre les agents du graph."""

    task: str              # La demande initiale de l'utilisateur
    code: str              # Code Python produit (et éventuellement amélioré) par les agents
    review: str            # Analyse et suggestions du reviewer
    tests: str             # Tests unitaires rédigés par le testeur
    status: str            # Décision du reviewer : "approved" ou "needs_fix"
    iterations: int        # Nombre de fois que le codeur a été exécuté (limite les boucles)
    execution_result: str  # Sortie de l'exécution des tests (stdout + stderr)
    execution_passed: bool # True si tous les tests passent

