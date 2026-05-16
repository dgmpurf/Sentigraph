from __future__ import annotations

from typing import TypeAlias

from app.services.crawling.base_adapter import AdapterMode, BasePlatformAdapter, PlatformAdapterError
from app.services.crawling.bilibili_adapter import BilibiliAdapter
from app.services.crawling.douyin_adapter import DouyinAdapter
from app.services.crawling.kuaishou_adapter import KuaishouAdapter
from app.services.crawling.public_parser.public_parser_adapter import (
    HupuPublicParserAdapter,
    JiemianPublicParserAdapter,
    MaimaiPublicParserAdapter,
    NgaPublicParserAdapter,
    ThePaperPublicParserAdapter,
    TiebaPublicParserAdapter,
)
from app.services.crawling.reddit_adapter import RedditAdapter
from app.services.crawling.weibo_adapter import WeiboAdapter
from app.services.crawling.xiaohongshu_adapter import XiaohongshuAdapter
from app.services.crawling.zhihu_adapter import ZhihuAdapter


AdapterClass: TypeAlias = type[BasePlatformAdapter]


ADAPTER_REGISTRY: dict[str, AdapterClass] = {
    BilibiliAdapter.platform_id: BilibiliAdapter,
    DouyinAdapter.platform_id: DouyinAdapter,
    HupuPublicParserAdapter.platform_id: HupuPublicParserAdapter,
    JiemianPublicParserAdapter.platform_id: JiemianPublicParserAdapter,
    KuaishouAdapter.platform_id: KuaishouAdapter,
    MaimaiPublicParserAdapter.platform_id: MaimaiPublicParserAdapter,
    NgaPublicParserAdapter.platform_id: NgaPublicParserAdapter,
    RedditAdapter.platform_id: RedditAdapter,
    ThePaperPublicParserAdapter.platform_id: ThePaperPublicParserAdapter,
    TiebaPublicParserAdapter.platform_id: TiebaPublicParserAdapter,
    WeiboAdapter.platform_id: WeiboAdapter,
    XiaohongshuAdapter.platform_id: XiaohongshuAdapter,
    ZhihuAdapter.platform_id: ZhihuAdapter,
}


def get_platform_adapter(platform_id: str, *, mode: AdapterMode | None = None) -> BasePlatformAdapter:
    key = platform_id.strip().lower()
    adapter_class = ADAPTER_REGISTRY.get(key)
    if adapter_class is None:
        raise PlatformAdapterError(f"No platform adapter is registered for '{platform_id}'.")
    if mode is None:
        return adapter_class()
    return adapter_class(mode=mode)


def get_adapter(platform_id: str, *, mode: AdapterMode | None = None) -> BasePlatformAdapter:
    return get_platform_adapter(platform_id, mode=mode)


def has_platform_adapter(platform_id: str) -> bool:
    return platform_id.strip().lower() in ADAPTER_REGISTRY


def get_supported_adapter_ids() -> list[str]:
    return sorted(ADAPTER_REGISTRY)
