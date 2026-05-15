from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]
PROJECT_ENV_PATH = REPOSITORY_ROOT / ".env"

_ENV_LOAD_ATTEMPTED = False


def load_project_env() -> bool:
    """Load the repository-root .env once without overriding existing env vars."""
    global _ENV_LOAD_ATTEMPTED
    if _ENV_LOAD_ATTEMPTED:
        return PROJECT_ENV_PATH.exists()

    _ENV_LOAD_ATTEMPTED = True
    if not PROJECT_ENV_PATH.exists():
        return False
    return bool(load_dotenv(dotenv_path=PROJECT_ENV_PATH, override=False))


def reddit_env_diagnostics() -> dict[str, str]:
    return {
        "REDDIT_ADAPTER_MODE": os.getenv("REDDIT_ADAPTER_MODE", "mock"),
        "REDDIT_CLIENT_ID": _presence("REDDIT_CLIENT_ID"),
        "REDDIT_CLIENT_SECRET": _presence("REDDIT_CLIENT_SECRET"),
        "REDDIT_USER_AGENT": _presence("REDDIT_USER_AGENT"),
    }


def _presence(name: str) -> str:
    return "present" if os.getenv(name, "").strip() else "missing"


load_project_env()
