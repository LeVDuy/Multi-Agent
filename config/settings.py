import os
from dotenv import load_dotenv

load_dotenv()

LM_STUDIO_BASE_URL: str = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
LM_STUDIO_MODEL: str = os.getenv("LM_STUDIO_MODEL", "local-model")
LM_STUDIO_API_KEY: str = os.getenv("LM_STUDIO_API_KEY", "not-needed")
TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.3"))
