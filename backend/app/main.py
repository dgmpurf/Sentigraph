from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.api.v1.routes.health import health_check
from app.services.storage.base_store import CaseRevisionConflict


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

    app.get("/health", tags=["health"])(health_check)

    return app


app = create_app()
