from __future__ import annotations

from app.services.crawling.public_parser.public_parser_adapter import (
    JiemianPublicParserAdapter,
    PublicParserPlatformAdapter,
    ThePaperPublicParserAdapter,
)
from app.services.crawling.public_parser.selector_profile import get_profile_ids, load_selector_profile


PUBLIC_PARSER_ADAPTERS = {
    JiemianPublicParserAdapter.platform_id: JiemianPublicParserAdapter,
    ThePaperPublicParserAdapter.platform_id: ThePaperPublicParserAdapter,
}


def get_public_parser_platform_ids() -> list[str]:
    return sorted(PUBLIC_PARSER_ADAPTERS)


def has_public_parser(platform_id: str) -> bool:
    return platform_id.strip().lower() in PUBLIC_PARSER_ADAPTERS


def get_public_parser_adapter_class(platform_id: str) -> type[PublicParserPlatformAdapter]:
    return PUBLIC_PARSER_ADAPTERS[platform_id.strip().lower()]


__all__ = [
    "PUBLIC_PARSER_ADAPTERS",
    "get_profile_ids",
    "get_public_parser_adapter_class",
    "get_public_parser_platform_ids",
    "has_public_parser",
    "load_selector_profile",
]
