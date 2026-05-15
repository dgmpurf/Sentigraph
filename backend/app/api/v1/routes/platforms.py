from fastapi import APIRouter

from app.schemas.platform import PlatformRegistryResponse, PlatformStatusResponse
from app.services.crawling.platform_registry import (
    get_active_mvp_platform_ids,
    get_platform_registry,
    get_platform_status_response,
)

router = APIRouter()


@router.get("", response_model=PlatformRegistryResponse)
def list_platforms() -> PlatformRegistryResponse:
    return PlatformRegistryResponse(
        platforms=get_platform_registry(),
        active_mvp_platforms=get_active_mvp_platform_ids(),
    )


@router.get("/status", response_model=PlatformStatusResponse)
def list_platform_status() -> PlatformStatusResponse:
    return get_platform_status_response()
