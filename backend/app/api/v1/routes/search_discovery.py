from fastapi import APIRouter, HTTPException, Query

from app.schemas.search_discovery import (
    SearchDiscoveryBatch,
    SearchDiscoveryProviderStatus,
    SearchDiscoveryStatusResponse,
)
from app.services.search_discovery import (
    YouTubeLiveSearchDiscoveryCredentialMissingError,
    YouTubeLiveSearchDiscoveryRouteDisabledError,
    get_mock_search_discovery_candidates,
    get_search_discovery_providers,
    get_search_discovery_status,
    get_youtube_official_api_mock_candidates,
    get_youtube_official_api_live_route_candidates,
)
from app.services.crawling.youtube_adapter import (
    YouTubeAuthError,
    YouTubeNetworkError,
    YouTubeParsingError,
    YouTubeQuotaError,
    YouTubeRealModeError,
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


@router.get(
    "/youtube-official-api/mock-candidates",
    response_model=SearchDiscoveryBatch,
)
def search_discovery_youtube_official_api_mock_candidates(
    query: str = Query(default="Tesla", min_length=1, max_length=120),
    max_candidates: int = Query(default=5, ge=1, le=10),
) -> SearchDiscoveryBatch:
    return get_youtube_official_api_mock_candidates(query, max_candidates)


@router.get(
    "/youtube-official-api/live-candidates",
    response_model=SearchDiscoveryBatch,
    include_in_schema=False,
)
def search_discovery_youtube_official_api_live_candidates(
    query: str = Query(default="Tesla", min_length=1, max_length=120),
    max_candidates: int = Query(default=5, ge=1, le=5),
) -> SearchDiscoveryBatch:
    try:
        return get_youtube_official_api_live_route_candidates(
            query,
            max_candidates=max_candidates,
        )
    except YouTubeLiveSearchDiscoveryRouteDisabledError as exc:
        raise HTTPException(
            status_code=404,
            detail="youtube_live_search_discovery_route_disabled",
        ) from exc
    except YouTubeLiveSearchDiscoveryCredentialMissingError as exc:
        raise HTTPException(
            status_code=503,
            detail="youtube_live_search_discovery_credential_missing",
        ) from exc
    except YouTubeAuthError as exc:
        raise HTTPException(
            status_code=502,
            detail="youtube_live_search_discovery_auth_error",
        ) from exc
    except YouTubeQuotaError as exc:
        raise HTTPException(
            status_code=429,
            detail="youtube_live_search_discovery_quota_error",
        ) from exc
    except YouTubeNetworkError as exc:
        raise HTTPException(
            status_code=502,
            detail="youtube_live_search_discovery_network_error",
        ) from exc
    except YouTubeParsingError as exc:
        raise HTTPException(
            status_code=502,
            detail="youtube_live_search_discovery_parsing_error",
        ) from exc
    except YouTubeRealModeError as exc:
        raise HTTPException(
            status_code=502,
            detail="youtube_live_search_discovery_provider_error",
        ) from exc
