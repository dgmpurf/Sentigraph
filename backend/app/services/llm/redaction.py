from __future__ import annotations

from collections.abc import Mapping
from typing import Any


SECRET_KEY_MARKERS = (
    "api_key",
    "access_token",
    "token",
    "secret",
    "password",
    "credential",
)


def redact_api_key(value: Any) -> str:
    """Return presence-only status for secret values.

    Readiness diagnostics should never include even partially masked keys. The
    UI/log-safe representation is only whether a value exists.
    """

    return "present" if str(value or "").strip() else "missing"


def redact_config_dict(config: Mapping[str, Any]) -> dict[str, Any]:
    """Redact secret-like config entries while preserving non-secret shape."""

    redacted: dict[str, Any] = {}
    for key, value in config.items():
        key_text = str(key)
        if _is_secret_key(key_text):
            redacted[key_text] = redact_api_key(value)
        elif isinstance(value, Mapping):
            redacted[key_text] = redact_config_dict(value)
        elif isinstance(value, list):
            redacted[key_text] = [
                redact_config_dict(item) if isinstance(item, Mapping) else item
                for item in value
            ]
        else:
            redacted[key_text] = value
    return redacted


def _is_secret_key(key: str) -> bool:
    normalized = key.lower()
    return any(marker in normalized for marker in SECRET_KEY_MARKERS)
