from fastapi import APIRouter, Query

from app.schemas.search_discovery import (
    SearchDiscoveryBatch,
    SearchDiscoveryProviderStatus,
    SearchDiscoveryStatusResponse,
)
from app.services.search_discovery import (
    get_mock_search_discovery_candidates,
    get_search_discovery_providers,
    get_search_discovery_status,
)

router = APIRouter()


@router.get("/status", response_model=SearchDiscoveryStatusResponse)
def search_discovery_status() -> SearchDiscoveryStatusResponse:
    return get_search_discovery_status()


@router.get("/providers", response_model=list[SearchDiscoveryProviderStatus])
def search_discovery_providers() -> list[SearchDiscoveryProviderStatus]:
    return get_search_discovery_providers()


@router.get("/mock-candidates", response_model=SearchDiscoveryBatch)
def search_discovery_mock_candidates(
    query: str = Query(default="Tesla", min_length=1, max_length=120),
    provider: str = Query(default="mock_static", min_length=1, max_length=64),
) -> SearchDiscoveryBatch:
    return get_mock_search_discovery_candidates(query, provider)
