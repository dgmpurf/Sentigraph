from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.schemas.external_collector_bridge import (
    ExternalCollectorDiscoveryResponse,
    ExternalCollectorPackageDetail,
    ExternalCollectorPackageSummary,
    ExternalCollectorStatus,
    ExternalCollectorValidationResult,
)
from app.services.external_collector_bridge import (
    ExternalCollectorBridgeLookupError,
    discover_external_collector_packages,
    get_external_collector_package_detail,
    get_external_collector_status,
    list_external_collector_packages,
    validate_external_collector_package,
)

router = APIRouter()


@router.get("/discovery", response_model=ExternalCollectorDiscoveryResponse)
def external_collector_discovery(
    query: str = Query(min_length=1, max_length=120),
    max_results: int = Query(default=5, ge=1, le=5),
) -> ExternalCollectorDiscoveryResponse:
    try:
        return discover_external_collector_packages(query, max_results)
    except ExternalCollectorBridgeLookupError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.status) from exc


@router.get("/status", response_model=ExternalCollectorStatus)
def external_collector_status() -> ExternalCollectorStatus:
    return get_external_collector_status()


@router.get("/packages", response_model=list[ExternalCollectorPackageSummary])
def external_collector_packages() -> list[ExternalCollectorPackageSummary]:
    return list_external_collector_packages()


@router.get("/packages/{package_name:path}", response_model=ExternalCollectorPackageDetail)
def external_collector_package_detail(package_name: str) -> ExternalCollectorPackageDetail:
    try:
        return get_external_collector_package_detail(package_name)
    except ExternalCollectorBridgeLookupError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.status) from exc


@router.post("/packages/{package_name:path}/validate", response_model=ExternalCollectorValidationResult)
def external_collector_package_validate(package_name: str) -> ExternalCollectorValidationResult:
    try:
        return validate_external_collector_package(package_name)
    except ExternalCollectorBridgeLookupError as exc:
        raise HTTPException(status_code=exc.http_status, detail=exc.status) from exc
