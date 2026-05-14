from __future__ import annotations

from typing import TypeAlias

from app.services.crawling.base_adapter import AdapterMode, BasePlatformAdapter, PlatformAdapterError
from app.services.crawling.reddit_adapter import RedditAdapter


AdapterClass: TypeAlias = type[BasePlatformAdapter]


ADAPTER_REGISTRY: dict[str, AdapterClass] = {
    RedditAdapter.platform_id: RedditAdapter,
}


def get_platform_adapter(platform_id: str, *, mode: AdapterMode = "mock") -> BasePlatformAdapter:
    key = platform_id.strip().lower()
    adapter_class = ADAPTER_REGISTRY.get(key)
    if adapter_class is None:
        raise PlatformAdapterError(f"No platform adapter is registered for '{platform_id}'.")
    return adapter_class(mode=mode)


def has_platform_adapter(platform_id: str) -> bool:
    return platform_id.strip().lower() in ADAPTER_REGISTRY


def get_supported_adapter_ids() -> list[str]:
    return sorted(ADAPTER_REGISTRY)
