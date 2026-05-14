from __future__ import annotations

from dataclasses import dataclass

from app.schemas.platform import PlatformSource


OFFICIAL_API_PLANNED = "official_api_planned"
FUTURE_REAL_ADAPTER_CANDIDATE = "future_real_adapter_candidate"
CRAWLER_LATER = "crawler_later"
DISABLED_OR_OPTIONAL_FUTURE = "disabled_or_optional_future"


@dataclass(frozen=True)
class PlatformRegistryItem:
    platform_id: str
    display_name: str
    category: str
    source_type: str
    status: str
    enabled_in_mvp: bool
    selectable_for_mock: bool
    official_platform_url: str | None
    notes: str

    def to_schema(self) -> PlatformSource:
        return PlatformSource(
            platform_id=self.platform_id,
            display_name=self.display_name,
            category=self.category,
            source_type=self.source_type,
            status=self.status,
            enabled_in_mvp=self.enabled_in_mvp,
            selectable_for_mock=self.selectable_for_mock,
            official_platform_url=self.official_platform_url,
            notes=self.notes,
        )


def _official_mock_platform(
    platform_id: str,
    display_name: str,
    official_platform_url: str,
) -> PlatformRegistryItem:
    return PlatformRegistryItem(
        platform_id=platform_id,
        display_name=display_name,
        category=OFFICIAL_API_PLANNED,
        source_type="mock_data_official_api_placeholder",
        status="mock_selectable_official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        official_platform_url=official_platform_url,
        notes=(
            "Selectable for offline mock analysis only. Real access is planned through "
            "the official API after credentials, permissions, and compliance review."
        ),
    )


def _crawler_later_platform(platform_id: str, display_name: str) -> PlatformRegistryItem:
    return PlatformRegistryItem(
        platform_id=platform_id,
        display_name=display_name,
        category=CRAWLER_LATER,
        source_type="public_page_parser_later",
        status="future_crawler_integration",
        enabled_in_mvp=False,
        selectable_for_mock=False,
        official_platform_url=None,
        notes="Future crawler integration. No crawler is implemented yet.",
    )


PLATFORM_REGISTRY: tuple[PlatformRegistryItem, ...] = (
    PlatformRegistryItem(
        platform_id="reddit",
        display_name="Reddit",
        category=FUTURE_REAL_ADAPTER_CANDIDATE,
        source_type="mock_data_future_adapter_placeholder",
        status="mock_selectable_future_adapter_candidate",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        official_platform_url=None,
        notes=(
            "Selectable for offline mock analysis. Reddit stays in the project as a "
            "future real adapter candidate, but no real API call is implemented yet."
        ),
    ),
    _official_mock_platform("weibo", "Weibo", "https://open.weibo.com"),
    _official_mock_platform("bilibili", "Bilibili", "https://openhome.bilibili.com"),
    _official_mock_platform("douyin", "Douyin", "https://developer.open-douyin.com"),
    _official_mock_platform("kuaishou", "Kuaishou", "https://open.kuaishou.com"),
    _official_mock_platform("xiaohongshu", "Xiaohongshu", "https://open.xiaohongshu.com"),
    _official_mock_platform("zhihu", "Zhihu", "https://open.zhihu.com"),
    _official_mock_platform("douban", "Douban", "https://developers.douban.com"),
    _official_mock_platform("toutiao", "Toutiao", "https://open.toutiao.com"),
    _crawler_later_platform("hupu", "Hupu"),
    _crawler_later_platform("baidu_tieba", "Baidu Tieba"),
    _crawler_later_platform("tianya", "Tianya"),
    _crawler_later_platform("nga", "NGA"),
    _crawler_later_platform("maimai", "Maimai"),
    _crawler_later_platform("the_paper", "The Paper / Pengpai News"),
    _crawler_later_platform("jiemian", "Jiemian News"),
    PlatformRegistryItem(
        platform_id="youtube",
        display_name="YouTube",
        category=DISABLED_OR_OPTIONAL_FUTURE,
        source_type="optional_future_api_or_export_source",
        status="disabled_optional_future",
        enabled_in_mvp=False,
        selectable_for_mock=False,
        official_platform_url=None,
        notes="Removed from active MVP platform choices. Keep only as an optional future source.",
    ),
)


def get_platform_registry() -> list[PlatformSource]:
    return [item.to_schema() for item in PLATFORM_REGISTRY]


def get_active_mvp_platform_ids() -> list[str]:
    return [
        item.platform_id
        for item in PLATFORM_REGISTRY
        if item.enabled_in_mvp and item.selectable_for_mock
    ]
