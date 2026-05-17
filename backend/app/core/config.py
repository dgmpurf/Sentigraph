import os

from pydantic import BaseModel

from app.core.environment import load_project_env


load_project_env()


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


class Settings(BaseModel):
    app_name: str = "Sentigraph"
    app_version: str = "0.1.0"
    app_env: str = os.getenv("APP_ENV", "development")
    api_v1_prefix: str = "/api/v1"
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_enable_real_calls: bool = _env_bool("LLM_ENABLE_REAL_CALLS", False)
    sentiment_analyzer_mode: str = os.getenv("SENTIMENT_ANALYZER_MODE", "rule_based")
    topic_summary_mode: str = os.getenv("TOPIC_SUMMARY_MODE", "template")
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


settings = Settings()
