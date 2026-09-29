from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.api.v1.routes.health import health_check
from app.services.storage.base_store import CaseRevisionConflict
from app.services.monitoring.analysis_lineage_currentness import (
    AuxiliaryGuardUnavailable,
    AuxiliaryIdentityConflict,
    AuxiliaryLineageStale,
)


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="Mock-first public opinion analysis API for Sentigraph.",
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(api_router, prefix=settings.api_v1_prefix)

    @app.exception_handler(CaseRevisionConflict)
    async def case_revision_conflict_handler(request: Request, exc: CaseRevisionConflict) -> JSONResponse:
        return JSONResponse(
            status_code=409,
            content={"detail": {
                "error": "case_revision_conflict",
                "case_id": exc.case_id,
                "expected_revision": exc.expected_revision,
                "current_revision": exc.current_revision,
            }},
        )

    @app.exception_handler(AuxiliaryLineageStale)
    async def auxiliary_lineage_stale_handler(request: Request, exc: AuxiliaryLineageStale) -> JSONResponse:
        detail = {
            "error": "case_auxiliary_lineage_stale",
            "case_id": exc.case_id,
            "artifact_type": exc.artifact_type,
        }
        if exc.artifact_id is not None:
            detail["artifact_id"] = exc.artifact_id
        return JSONResponse(status_code=409, content={"detail": detail})

    @app.exception_handler(AuxiliaryIdentityConflict)
    async def auxiliary_identity_conflict_handler(request: Request, exc: AuxiliaryIdentityConflict) -> JSONResponse:
        detail = {
            "error": "case_auxiliary_identity_conflict",
            "case_id": exc.case_id,
            "artifact_type": exc.artifact_type,
        }
        if exc.artifact_id is not None:
            detail["artifact_id"] = exc.artifact_id
        return JSONResponse(status_code=409, content={"detail": detail})

    @app.exception_handler(AuxiliaryGuardUnavailable)
    async def auxiliary_guard_unavailable_handler(request: Request, exc: AuxiliaryGuardUnavailable) -> JSONResponse:
        return JSONResponse(status_code=503, content={"detail": {"error": "case_auxiliary_guard_unavailable"}})

    app.get("/health", tags=["health"])(health_check)

    return app


app = create_app()
