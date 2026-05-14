from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, ClassVar, Literal, Mapping

from app.schemas.comment import RawComment, RawPost


AdapterMode = Literal["mock", "real"]


class PlatformAdapterError(RuntimeError):
    """Raised when a platform adapter cannot complete a requested operation."""


@dataclass(frozen=True)
class RetryPolicy:
    max_attempts: int = 2
    backoff_seconds: float = 0.25


@dataclass(frozen=True)
class RateLimitPolicy:
    requests_per_minute: int = 60


class BasePlatformAdapter(ABC):
    """Common interface for safe public platform adapters.

    Adapters must normalize all public source data into Sentigraph RawPost and
    RawComment schemas. They must not implement login bypass, captcha bypass,
    anti-bot evasion, paywall bypass, or private data collection.
    """

    platform_id: ClassVar[str]
    display_name: ClassVar[str]

    def __init__(
        self,
        *,
        mode: AdapterMode = "mock",
        retry_policy: RetryPolicy | None = None,
        rate_limit_policy: RateLimitPolicy | None = None,
    ) -> None:
        self.mode: AdapterMode = mode
        self.retry_policy = retry_policy or RetryPolicy()
        self.rate_limit_policy = rate_limit_policy or RateLimitPolicy()

    @abstractmethod
    def search_posts(
        self,
        keyword: str,
        limit: int = 20,
        sort: str = "relevance",
        date_range: dict[str, str] | None = None,
    ) -> list[RawPost]:
        """Search public posts and return normalized RawPost objects."""

    @abstractmethod
    def fetch_comments(self, post_id: str, limit: int = 100) -> list[RawComment]:
        """Fetch public comments for a post and return normalized RawComment objects."""

    @abstractmethod
    def normalize_post(self, raw: Mapping[str, Any]) -> RawPost:
        """Normalize a platform-native post payload into RawPost."""

    @abstractmethod
    def normalize_comment(self, raw: Mapping[str, Any]) -> RawComment:
        """Normalize a platform-native comment payload into RawComment."""

    def clamp_limit(self, limit: int, *, default: int, maximum: int) -> int:
        if not isinstance(limit, int) or limit <= 0:
            return default
        return min(limit, maximum)

    def to_utc_iso(self, value: Any) -> str:
        if isinstance(value, (int, float)):
            return datetime.fromtimestamp(value, tz=timezone.utc).isoformat().replace("+00:00", "Z")
        if isinstance(value, str) and value:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=timezone.utc)
                return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
            except ValueError:
                return value
        return "1970-01-01T00:00:00Z"

    def coerce_int(self, value: Any, default: int = 0) -> int:
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def safe_text(self, value: Any, default: str = "") -> str:
        if value is None:
            return default
        text = str(value).strip()
        return text if text else default

    def sanitize_raw_data(self, raw: Mapping[str, Any]) -> dict[str, Any]:
        """Return a MongoDB-safe raw payload with string dictionary keys."""

        return _string_keyed_dict(raw)


def _string_keyed_dict(raw: Mapping[str, Any]) -> dict[str, Any]:
    safe: dict[str, Any] = {}
    for key, value in raw.items():
        safe[str(key)] = _string_keyed_value(value)
    return safe


def _string_keyed_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return _string_keyed_dict(value)
    if isinstance(value, list):
        return [_string_keyed_value(item) for item in value]
    return value
