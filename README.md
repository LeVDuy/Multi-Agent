# Équipe IT Multi-Agent (Local Agentic Workflow)

Un système Multi-Agent d'Intelligence Artificielle entièrement local et autonome, capable de fonctionner comme une équipe de développement (Codeur, Reviewer, Testeur). Construit avec LangGraph et Streamlit, le système utilise l'approche "Execution-driven Self-Correction" pour garantir que le code passe des tests unitaires réels.

Conçu pour fonctionner hors ligne via LM Studio ou tout serveur compatible OpenAI.

## Fonctionnalités

- Workflow Agentique : Agents Codeur, Reviewer et Testeur orchestrés par LangGraph.
- Auto-Correction : Le système exécute le code et les tests générés via un bac à sable (Executor). Les journaux d'erreurs (tracebacks) sont renvoyés automatiquement au Codeur pour correction itérative.
- Support Bilingue (Français/Anglais) : Les docstrings et le code s'adaptent à la langue de la requête.
- Multi-Interfaces : Application Streamlit moderne et mode CLI inclus.
- Architecture Locale : Compatible avec n'importe quel LLM Open-Source local (ex: Qwen 7B, Llama 3).

## Architecture

Le système repose sur un flux de travail conditionnel (StateGraph) en 4 étapes :

1. **Le Codeur** : Reçoit la requête et génère le code source Python initial.
2. **Le Reviewer** : Analyse le code généré. S'il détecte des problèmes ou des oublis, il renvoie des instructions de correction au Codeur (avec une limite de 3 itérations). Si le code est satisfaisant, il est approuvé.
3. **Le Testeur** : Une fois le code approuvé, cet agent rédige des tests unitaires (Pytest) rigoureux pour vérifier son comportement.
4. **L'Executor (Exécution réelle)** : Exécute le code et les tests de manière autonome dans un environnement temporaire (bac à sable).
   - **En cas d'échec** (Tests échoués) : Les journaux d'erreurs (tracebacks) sont renvoyés directement au Codeur pour une auto-correction.
   - **En cas de succès** (Tests réussis) : Le workflow s'arrête et le code validé est présenté à l'utilisateur.

## Installation

Prérequis: Python 3.9+ et LM Studio ou environnement API équivalent.

1. Cloner et installer l'environnement :
```bash
git clone <url-du-repo>
cd Mutil-Agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configuration API :
Ouvrez LM Studio, chargez un modèle (ex: Qwen 2.5 7B) et lancez le "Local Server".
Copiez le fichier `.env.example` en `.env` :
```bash
cp .env.example .env
```
Assurez-vous que le fichier `.env` contienne le bon modèle :
```env
LM_STUDIO_BASE_URL=http://localhost:1234/v1
LM_STUDIO_MODEL=qwen2.5-7b-instruct
TEMPERATURE=0.3
```

## Utilisation

Mode web :
```bash
streamlit run app.py
```

Mode Console (CLI) :
```bash
python main.py
```

Lancer les tests du projet :
```bash
pytest tests/ -v
```

## Déploiement Docker

Le projet est conteneurisé.
```bash
docker-compose up --build
```
Le port 8501 sera exposé pour accéder à Streamlit.
