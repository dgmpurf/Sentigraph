from __future__ import annotations

import os
from dataclasses import dataclass

from app.core.environment import load_project_env
from app.schemas.platform import PlatformSource, PlatformStatusResponse, PlatformStatusSummary
from app.services.crawling.bilibili_adapter import (
    BILIBILI_API_APPROVAL_STATUS,
    BILIBILI_REQUIRED_CREDENTIALS,
)
from app.services.crawling.douban_adapter import (
    DOUBAN_API_APPROVAL_STATUS,
    DOUBAN_REQUIRED_CREDENTIALS,
)
from app.services.crawling.douyin_adapter import (
    DOUYIN_API_APPROVAL_STATUS,
    DOUYIN_COMMENT_API_STATUS,
    DOUYIN_DEVELOPER_ACCESS_STATUS,
    DOUYIN_REAL_MODE_BLOCKER,
    DOUYIN_REQUIRED_CREDENTIALS,
)
from app.services.crawling.kuaishou_adapter import (
    KUAISHOU_API_APPROVAL_STATUS,
    KUAISHOU_REQUIRED_CREDENTIALS,
)
from app.services.crawling.reddit_adapter import REDDIT_API_APPROVAL_STATUS, REDDIT_REQUIRED_CREDENTIALS
from app.services.crawling.toutiao_adapter import (
    TOUTIAO_API_APPROVAL_STATUS,
    TOUTIAO_REQUIRED_CREDENTIALS,
)
from app.services.crawling.weibo_adapter import WEIBO_API_APPROVAL_STATUS, WEIBO_REQUIRED_CREDENTIALS
from app.services.crawling.xiaohongshu_adapter import (
    XIAOHONGSHU_API_APPROVAL_STATUS,
    XIAOHONGSHU_COMMENT_API_STATUS,
    XIAOHONGSHU_DEVELOPER_ACCESS_STATUS,
    XIAOHONGSHU_REAL_MODE_BLOCKER,
    XIAOHONGSHU_REQUIRED_CREDENTIALS,
)
from app.services.crawling.zhihu_adapter import ZHIHU_API_APPROVAL_STATUS, ZHIHU_REQUIRED_CREDENTIALS


OFFICIAL_API_PLANNED = "official_api_planned"
FUTURE_REAL_ADAPTER_CANDIDATE = "future_real_adapter_candidate"
CRAWLER_LATER = "crawler_later"
DISABLED_OR_OPTIONAL_FUTURE = "disabled_or_optional_future"
API_APPROVAL_NOT_REQUIRED = "not_required"
API_APPROVAL_NOT_APPLICABLE = "not_applicable"
REAL_MODE_DISABLED_API_PENDING = "api_pending"


@dataclass(frozen=True)
class PlatformRegistryItem:
    platform_id: str
    display_name: str
    category: str
    source_type: str
    status: str
    enabled_in_mvp: bool
    selectable_for_mock: bool
    mock_available: bool
    api_pending: bool
    real_mode_disabled: bool
    official_platform_url: str | None
    notes: str
    real_mode_available: bool = False
    api_approval_required: bool = False
    api_approval_status: str = API_APPROVAL_NOT_REQUIRED
    developer_access_status: str | None = None
    comment_api_status: str | None = None
    real_mode_blocker: str | None = None
    credentials_required: tuple[str, ...] = ()
    selectable_for_real: bool = False

    def to_schema(self) -> PlatformSource:
        credentials_present = _credential_presence(self.credentials_required)
        return PlatformSource(
            platform_id=self.platform_id,
            display_name=self.display_name,
            category=self.category,
            source_type=self.source_type,
            status=self.status,
            enabled_in_mvp=self.enabled_in_mvp,
            selectable_for_mock=self.selectable_for_mock,
            mock_available=self.mock_available,
            real_mode_available=self.real_mode_available,
            api_approval_required=self.api_approval_required,
            api_approval_status=self.api_approval_status,
            developer_access_status=self.developer_access_status,
            comment_api_status=self.comment_api_status,
            real_mode_blocker=self.real_mode_blocker,
            credentials_required=list(self.credentials_required),
            credentials_present=credentials_present,
            api_pending=self.api_pending,
            real_mode_disabled=self.real_mode_disabled,
            selectable_for_real=self.selectable_for_real,
            official_platform_url=self.official_platform_url,
            notes=self.notes,
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
        mock_available=False,
        api_pending=False,
        real_mode_disabled=True,
        official_platform_url=None,
        notes="Future crawler integration. No crawler is implemented yet.",
        api_approval_status=API_APPROVAL_NOT_APPLICABLE,
    )


def _public_parser_scaffold_platform(platform_id: str, display_name: str) -> PlatformRegistryItem:
    return PlatformRegistryItem(
        platform_id=platform_id,
        display_name=display_name,
        category=CRAWLER_LATER,
        source_type="public_page_parser",
        status="fixture_only",
        enabled_in_mvp=False,
        selectable_for_mock=False,
        mock_available=True,
        api_pending=False,
        real_mode_disabled=True,
        official_platform_url=None,
        notes=(
            "Public-page parser scaffold is available in fixture/mock fallback mode only. "
            "Live fetch is disabled by default and must not bypass login, captcha, paywalls, "
            "anti-bot systems, or private data access."
        ),
        api_approval_status=API_APPROVAL_NOT_APPLICABLE,
    )


PLATFORM_REGISTRY: tuple[PlatformRegistryItem, ...] = (
    PlatformRegistryItem(
        platform_id="reddit",
        display_name="Reddit",
        category=FUTURE_REAL_ADAPTER_CANDIDATE,
        source_type="mock_data_future_adapter_placeholder",
        status="api_pending",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url=None,
        notes=(
            "Selectable for offline mock analysis. Reddit API approval is pending, "
            "so real API mode is disabled and public-page scraping is not used as a bypass."
        ),
        api_approval_required=True,
        api_approval_status=REDDIT_API_APPROVAL_STATUS,
        credentials_required=REDDIT_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="weibo",
        display_name="Weibo",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://open.weibo.com",
        notes=(
            "Selectable for offline Weibo-style mock microblog/comment analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=WEIBO_API_APPROVAL_STATUS,
        credentials_required=WEIBO_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="bilibili",
        display_name="Bilibili",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://openhome.bilibili.com",
        notes=(
            "Selectable for offline Bilibili-style mock video/comment analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=BILIBILI_API_APPROVAL_STATUS,
        credentials_required=BILIBILI_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="douyin",
        display_name="Douyin",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://developer.open-douyin.com",
        notes=(
            "Selectable for offline Douyin-style mock short-video/comment analysis. "
            "Developer access is reported as obtained, but official comment permission is "
            "not yet verified. Real official API mode is disabled until the comment scope "
            "and compliant API implementation are confirmed. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=DOUYIN_API_APPROVAL_STATUS,
        developer_access_status=DOUYIN_DEVELOPER_ACCESS_STATUS,
        comment_api_status=DOUYIN_COMMENT_API_STATUS,
        real_mode_blocker=DOUYIN_REAL_MODE_BLOCKER,
        credentials_required=DOUYIN_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="kuaishou",
        display_name="Kuaishou",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://open.kuaishou.com",
        notes=(
            "Selectable for offline Kuaishou-style mock short-video/comment analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=KUAISHOU_API_APPROVAL_STATUS,
        credentials_required=KUAISHOU_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="xiaohongshu",
        display_name="Xiaohongshu",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://open.xiaohongshu.com",
        notes=(
            "Selectable for offline Xiaohongshu-style mock lifestyle/community note analysis. "
            "Developer access is reported as obtained, but note/comment API availability "
            "and permission are not yet verified. Real official API mode is disabled until "
            "the official data product and compliant API implementation are confirmed. "
            "No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=XIAOHONGSHU_API_APPROVAL_STATUS,
        developer_access_status=XIAOHONGSHU_DEVELOPER_ACCESS_STATUS,
        comment_api_status=XIAOHONGSHU_COMMENT_API_STATUS,
        real_mode_blocker=XIAOHONGSHU_REAL_MODE_BLOCKER,
        credentials_required=XIAOHONGSHU_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="zhihu",
        display_name="Zhihu",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://open.zhihu.com",
        notes=(
            "Selectable for offline Zhihu-style mock Q&A/article/comment analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=ZHIHU_API_APPROVAL_STATUS,
        credentials_required=ZHIHU_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="douban",
        display_name="Douban",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://developers.douban.com",
        notes=(
            "Selectable for offline Douban-style mock review/group/topic analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=DOUBAN_API_APPROVAL_STATUS,
        credentials_required=DOUBAN_REQUIRED_CREDENTIALS,
    ),
    PlatformRegistryItem(
        platform_id="toutiao",
        display_name="Toutiao",
        category=OFFICIAL_API_PLANNED,
        source_type="official_api_adapter_scaffold",
        status="official_api_planned",
        enabled_in_mvp=True,
        selectable_for_mock=True,
        mock_available=True,
        api_pending=True,
        real_mode_disabled=True,
        official_platform_url="https://open.toutiao.com",
        notes=(
            "Selectable for offline Toutiao-style mock article/micro-headline/comment analysis. "
            "Real official API mode is disabled until credentials, approval, and "
            "the compliant API implementation are added. No page scraping is implemented."
        ),
        api_approval_required=True,
        api_approval_status=TOUTIAO_API_APPROVAL_STATUS,
        credentials_required=TOUTIAO_REQUIRED_CREDENTIALS,
    ),
    _public_parser_scaffold_platform("hupu", "Hupu / 虎扑"),
    _public_parser_scaffold_platform("tieba", "Baidu Tieba / 百度贴吧"),
    _crawler_later_platform("tianya", "Tianya"),
    _public_parser_scaffold_platform("nga", "NGA"),
    _public_parser_scaffold_platform("maimai", "Maimai / 脉脉"),
    _public_parser_scaffold_platform("the_paper", "The Paper / Pengpai News"),
    _public_parser_scaffold_platform("jiemian", "Jiemian News / 界面新闻"),
    PlatformRegistryItem(
        platform_id="youtube",
        display_name="YouTube",
        category=DISABLED_OR_OPTIONAL_FUTURE,
        source_type="optional_future_api_or_export_source",
        status="disabled_optional_future",
        enabled_in_mvp=False,
        selectable_for_mock=False,
        mock_available=False,
        api_pending=False,
        real_mode_disabled=True,
        official_platform_url=None,
        notes="Removed from active MVP platform choices. Keep only as an optional future source.",
        api_approval_status=API_APPROVAL_NOT_APPLICABLE,
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


def get_platform_status_response() -> PlatformStatusResponse:
    platforms = get_platform_registry()
    mock_selectable_platforms = [
        platform.platform_id
        for platform in platforms
        if platform.selectable_for_mock and platform.mock_available
    ]
    real_selectable_platforms = [
        platform.platform_id
        for platform in platforms
        if platform.selectable_for_real and platform.real_mode_available
    ]
    summary = PlatformStatusSummary(
        total_platforms=len(platforms),
        mock_selectable_count=len(mock_selectable_platforms),
        real_selectable_count=len(real_selectable_platforms),
        api_pending_count=sum(1 for platform in platforms if platform.api_pending),
        disabled_count=sum(1 for platform in platforms if platform.real_mode_disabled and not platform.selectable_for_mock),
        crawler_later_count=sum(1 for platform in platforms if platform.category == CRAWLER_LATER),
    )
    return PlatformStatusResponse(
        platforms=platforms,
        active_mvp_platforms=get_active_mvp_platform_ids(),
        mock_selectable_platforms=mock_selectable_platforms,
        real_selectable_platforms=real_selectable_platforms,
        summary=summary,
    )


def _credential_presence(credentials_required: tuple[str, ...]) -> dict[str, bool]:
    if not credentials_required:
        return {}
    load_project_env()
    return {
        credential_name: bool(os.getenv(credential_name, "").strip())
        for credential_name in credentials_required
    }
