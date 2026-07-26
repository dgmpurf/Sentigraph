from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.schemas.external_collector_bridge import (
    ExternalCollectorPackageDetail,
    ExternalCollectorPackageSummary,
    ExternalCollectorStatus,
    ExternalCollectorValidationResult,
)
from app.services.external_collector_bridge import (
    ExternalCollectorBridgeLookupError,
    get_external_collector_package_detail,
    get_external_collector_status,
    list_external_collector_packages,
    validate_external_collector_package,
)

router = APIRouter()


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
