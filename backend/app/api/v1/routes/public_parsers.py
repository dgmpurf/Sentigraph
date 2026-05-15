from fastapi import APIRouter, HTTPException

from app.schemas.public_parser import (
    PublicParserPreviewRequest,
    PublicParserPreviewResponse,
    PublicParserStatusResponse,
)
from app.services.crawling.public_parser.parser_status_service import (
    get_public_parser_status_response,
    preview_public_parser,
)

router = APIRouter()


@router.get("/status", response_model=PublicParserStatusResponse)
def list_public_parser_status() -> PublicParserStatusResponse:
    return get_public_parser_status_response()


@router.post("/preview", response_model=PublicParserPreviewResponse)
def preview_public_parser_source(
    payload: PublicParserPreviewRequest,
) -> PublicParserPreviewResponse:
    try:
        return preview_public_parser(
            payload.platform,
            limit=payload.limit,
            use_live_fetch=payload.use_live_fetch,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
