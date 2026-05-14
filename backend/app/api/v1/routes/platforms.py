from fastapi import APIRouter

from app.schemas.platform import PlatformRegistryResponse
from app.services.crawling.platform_registry import get_active_mvp_platform_ids, get_platform_registry

router = APIRouter()


@router.get("", response_model=PlatformRegistryResponse)
def list_platforms() -> PlatformRegistryResponse:
    return PlatformRegistryResponse(
        platforms=get_platform_registry(),
        active_mvp_platforms=get_active_mvp_platform_ids(),
    )
