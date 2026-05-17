import os

from pydantic import BaseModel

from app.core.environment import load_project_env


load_project_env()


def _env_bool(name: str, default: bool = False) -> bool:
    raw = os.getenv(name)
    if raw is None:
        return default
    return raw.strip().lower() in {"1", "true", "yes", "on"}


def _env_int(name: str, default: int) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


class Settings(BaseModel):
    app_name: str = "Sentigraph"
    app_version: str = "0.1.0"
    app_env: str = os.getenv("APP_ENV", "development")
    api_v1_prefix: str = "/api/v1"
    llm_provider: str = os.getenv("LLM_PROVIDER", "mock")
    llm_enable_real_calls: bool = _env_bool("LLM_ENABLE_REAL_CALLS", False)
    llm_usage_tracking_enabled: bool = _env_bool("LLM_USAGE_TRACKING_ENABLED", True)
    llm_daily_call_limit: int = _env_int("LLM_DAILY_CALL_LIMIT", 100)
    llm_daily_token_limit: int = _env_int("LLM_DAILY_TOKEN_LIMIT", 100000)
    llm_max_input_chars: int = _env_int("LLM_MAX_INPUT_CHARS", 20000)
    llm_fail_closed_on_limit: bool = _env_bool("LLM_FAIL_CLOSED_ON_LIMIT", True)
    llm_cost_guardrail_mode: str = os.getenv("LLM_COST_GUARDRAIL_MODE", "mock")
    sentiment_analyzer_mode: str = os.getenv("SENTIMENT_ANALYZER_MODE", "rule_based")
    topic_summary_mode: str = os.getenv("TOPIC_SUMMARY_MODE", "template")
    selector_repair_mode: str = os.getenv("SELECTOR_REPAIR_MODE", "mock")
    selector_repair_enable_real_llm: bool = _env_bool("SELECTOR_REPAIR_ENABLE_REAL_LLM", False)
    selector_repair_max_html_chars: int = _env_int("SELECTOR_REPAIR_MAX_HTML_CHARS", 20000)
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:4173",
        "http://127.0.0.1:4173",
    ]


settings = Settings()
