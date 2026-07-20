import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

DEPARTMENTS: List[str] = ["hr", "it", "finance", "legal"]


@dataclass
class Settings:
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")

    orchestrator_model: str = os.getenv("ORCHESTRATOR_MODEL", "gpt-4o")
    rag_model: str = os.getenv("RAG_MODEL", "gpt-4o")
    evaluator_model: str = os.getenv("EVALUATOR_MODEL", "gpt-4o")

    embedding_model_name: str = os.getenv(
        "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
    )

    data_dir: Path = BASE_DIR / "data"
    chroma_persist_dir: Path = BASE_DIR / ".chroma"

    langfuse_public_key: str = os.getenv("LANGFUSE_PUBLIC_KEY", "")
    langfuse_secret_key: str = os.getenv("LANGFUSE_SECRET_KEY", "")
    langfuse_host: str = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")

    departments: List[str] = field(default_factory=lambda: list(DEPARTMENTS))


settings = Settings()
