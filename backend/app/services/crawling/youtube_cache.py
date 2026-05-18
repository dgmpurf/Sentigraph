from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from threading import RLock
from typing import Any, Mapping


PROJECT_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_YOUTUBE_CACHE_PATH = PROJECT_ROOT / "backend" / "data" / "youtube_cache.json"


@dataclass(frozen=True)
class YouTubeAdapterConfig:
    cache_enabled: bool = True
    cache_ttl_seconds: int = 3600
    max_search_results: int = 5
    max_comments_per_video: int = 20
    max_replies_per_comment: int = 5
    max_total_comments: int = 50
    enable_deep_replies: bool = False

    @classmethod
    def from_env(cls) -> "YouTubeAdapterConfig":
        return cls(
            cache_enabled=_env_bool("YOUTUBE_CACHE_ENABLED", True),
            cache_ttl_seconds=_env_int("YOUTUBE_CACHE_TTL_SECONDS", 3600, minimum=0),
            max_search_results=_env_int("YOUTUBE_MAX_SEARCH_RESULTS", 5, minimum=1),
            max_comments_per_video=_env_int("YOUTUBE_MAX_COMMENTS_PER_VIDEO", 20, minimum=1),
            max_replies_per_comment=_env_int("YOUTUBE_MAX_REPLIES_PER_COMMENT", 5, minimum=0),
            max_total_comments=_env_int("YOUTUBE_MAX_TOTAL_COMMENTS", 50, minimum=1),
            enable_deep_replies=_env_bool("YOUTUBE_ENABLE_DEEP_REPLIES", False),
        )


@dataclass(frozen=True)
class YouTubeCacheLookup:
    hit: bool
    payload: dict[str, Any] | None = None
    cache_age_seconds: int | None = None
    expired: bool = False


class YouTubeResponseCache:
    """Small project-local JSON cache for quota-safe YouTube API demos.

    Cache keys are created only from safe query fields and the cache payload is
    normalized crawl data. Credentials are never accepted as key material.
    """

    def __init__(
        self,
        *,
        path: str | Path = DEFAULT_YOUTUBE_CACHE_PATH,
        enabled: bool = True,
        ttl_seconds: int = 3600,
    ) -> None:
        self.path = Path(path)
        self.enabled = enabled
        self.ttl_seconds = max(0, int(ttl_seconds))
        self._lock = RLock()

    @classmethod
    def from_config(cls, config: YouTubeAdapterConfig) -> "YouTubeResponseCache":
        return cls(
            path=DEFAULT_YOUTUBE_CACHE_PATH,
            enabled=config.cache_enabled,
            ttl_seconds=config.cache_ttl_seconds,
        )

    def build_key(self, namespace: str, params: Mapping[str, Any]) -> str:
        safe_payload = {
            "namespace": str(namespace),
            "params": _json_safe(params),
        }
        digest = hashlib.sha256(
            json.dumps(safe_payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        return f"{namespace}:{digest}"

    def get(self, key: str) -> YouTubeCacheLookup:
        if not self.enabled:
            return YouTubeCacheLookup(hit=False)
        now = _utcnow()
        with self._lock:
            data = self._read_data()
            entry = data.get("entries", {}).get(key)
        if not isinstance(entry, dict):
            return YouTubeCacheLookup(hit=False)

        cached_at = _parse_datetime(entry.get("cached_at"))
        expires_at = _parse_datetime(entry.get("expires_at"))
        if expires_at is None or expires_at <= now:
            return YouTubeCacheLookup(hit=False, expired=True)

        payload = entry.get("payload")
        if not isinstance(payload, dict):
            return YouTubeCacheLookup(hit=False)
        age = int(max(0.0, (now - (cached_at or now)).total_seconds()))
        return YouTubeCacheLookup(hit=True, payload=payload, cache_age_seconds=age)

    def set(
        self,
        key: str,
        *,
        safe_key: Mapping[str, Any],
        payload: Mapping[str, Any],
        source_type: str,
    ) -> None:
        if not self.enabled:
            return
        now = _utcnow()
        entry = {
            "source_type": source_type,
            "safe_key": _json_safe(safe_key),
            "cached_at": _format_datetime(now),
            "expires_at": _format_datetime(now + timedelta(seconds=self.ttl_seconds)),
            "payload": _json_safe(payload),
        }
        with self._lock:
            data = self._read_data()
            entries = data.setdefault("entries", {})
            if not isinstance(entries, dict):
                data["entries"] = {}
                entries = data["entries"]
            entries[key] = entry
            self._write_data(data)

    def status(self) -> dict[str, Any]:
        with self._lock:
            data = self._read_data()
        entries = data.get("entries", {})
        return {
            "enabled": self.enabled,
            "path": str(self.path),
            "ttl_seconds": self.ttl_seconds,
            "entry_count": len(entries) if isinstance(entries, dict) else 0,
        }

    def clear(self) -> None:
        with self._lock:
            if self.path.exists():
                self.path.unlink()

    def _read_data(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"version": 1, "entries": {}}
        try:
            with self.path.open("r", encoding="utf-8") as file:
                raw = json.load(file)
        except (OSError, json.JSONDecodeError):
            return {"version": 1, "entries": {}}
        if not isinstance(raw, dict):
            return {"version": 1, "entries": {}}
        entries = raw.get("entries")
        return {
            "version": 1,
            "entries": entries if isinstance(entries, dict) else {},
        }

    def _write_data(self, data: Mapping[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(f"{self.path.suffix}.tmp")
        with tmp_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=2, sort_keys=True)
            file.write("\n")
        tmp_path.replace(self.path)


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


def _env_int(name: str, default: int, *, minimum: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        parsed = int(value.strip())
    except ValueError:
        return default
    return max(minimum, parsed)


def _json_safe(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_json_safe(item) for item in value]
    if isinstance(value, tuple):
        return [_json_safe(item) for item in value]
    if isinstance(value, datetime):
        return _format_datetime(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _utcnow() -> datetime:
    return datetime.now(timezone.utc)


def _format_datetime(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _parse_datetime(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value.strip():
        return None
    text = value.strip()
    if text.endswith("Z"):
        text = f"{text[:-1]}+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
