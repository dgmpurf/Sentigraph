from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any


def parse_json_object(raw: str, fallback: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Parse a JSON object, returning a deterministic fallback on malformed input."""

    default = dict(fallback or {})
    try:
        parsed = json.loads(_strip_simple_markdown_fence(raw))
    except (TypeError, json.JSONDecodeError):
        return default
    if not isinstance(parsed, dict):
        return default
    return parsed


def parse_json_array(raw: str, fallback: list[Any] | None = None) -> list[Any]:
    """Parse a JSON array, returning a deterministic fallback on malformed input."""

    default = list(fallback or [])
    try:
        parsed = json.loads(_strip_simple_markdown_fence(raw))
    except (TypeError, json.JSONDecodeError):
        return default
    if not isinstance(parsed, list):
        return default
    return parsed


def _strip_simple_markdown_fence(raw: str) -> str:
    text = str(raw).strip()
    if not text.startswith("```"):
        return text
    lines = text.splitlines()
    if len(lines) >= 2 and lines[-1].strip() == "```":
        return "\n".join(lines[1:-1]).strip()
    return text
