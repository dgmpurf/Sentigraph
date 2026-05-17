from __future__ import annotations

import re


DEFAULT_MAX_HTML_CHARS = 20_000

_SCRIPT_RE = re.compile(r"<script\b[^>]*>.*?</script\s*>", re.IGNORECASE | re.DOTALL)
_STYLE_RE = re.compile(r"<style\b[^>]*>.*?</style\s*>", re.IGNORECASE | re.DOTALL)
_EVENT_HANDLER_RE = re.compile(
    r"\s+on[a-zA-Z]+\s*=\s*(\"[^\"]*\"|'[^']*'|[^\s>]+)",
    re.IGNORECASE,
)
_SECRET_PAIR_RE = re.compile(
    r"(?i)\b(cookie|token|access_token|auth|authorization|sessionid|session_id|csrf|client_secret|password)"
    r"\s*[:=]\s*"
    r"(\"[^\"]*\"|'[^']*'|Bearer\s+[^\s\"'<>;]+|[^\s\"'<>;]+)"
)
_COOKIE_META_RE = re.compile(
    r"<meta\b[^>]*(?:cookie|token|csrf|authorization|client_secret)[^>]*>",
    re.IGNORECASE,
)


def sanitize_html(html: str, *, max_chars: int = DEFAULT_MAX_HTML_CHARS) -> str:
    """Return structural public HTML suitable for offline selector analysis."""

    safe_max = _safe_max_chars(max_chars)
    sanitized = str(html or "")
    sanitized = _SCRIPT_RE.sub("", sanitized)
    sanitized = _STYLE_RE.sub("", sanitized)
    sanitized = _COOKIE_META_RE.sub("", sanitized)
    sanitized = _EVENT_HANDLER_RE.sub("", sanitized)
    sanitized = _SECRET_PAIR_RE.sub(lambda match: f"{match.group(1)}=[REDACTED]", sanitized)
    return sanitized[:safe_max]


def _safe_max_chars(value: int) -> int:
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return DEFAULT_MAX_HTML_CHARS
    if parsed <= 0:
        return DEFAULT_MAX_HTML_CHARS
    return min(parsed, DEFAULT_MAX_HTML_CHARS)
