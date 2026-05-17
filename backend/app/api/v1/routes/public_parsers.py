from fastapi import APIRouter, HTTPException

from app.schemas.public_parser import (
    PublicParserPreviewRequest,
    PublicParserPreviewResponse,
    PublicParserStatusResponse,
)
from app.schemas.selector_repair import (
    SelectorRepairPreviewApiRequest,
    SelectorRepairPreviewResult,
    SelectorRepairSuggestApiRequest,
    SelectorRepairSuggestion,
)
from app.services.crawling.public_parser.parser_status_service import (
    get_public_parser_status_response,
    preview_public_parser,
)
from app.services.crawling.public_parser.selector_repair.selector_repair_service import (
    build_repair_request,
    preview_suggestion,
    suggest_selectors,
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


@router.post("/selector-repair/suggest", response_model=SelectorRepairSuggestion)
def suggest_selector_repair(
    payload: SelectorRepairSuggestApiRequest,
) -> SelectorRepairSuggestion:
    try:
        request = build_repair_request(
            payload.platform_id,
            payload.html,
            profile=payload.profile,
            error_summary=payload.error_summary,
            extraction_targets=payload.extraction_targets,
        )
        return suggest_selectors(request)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/selector-repair/preview", response_model=SelectorRepairPreviewResult)
def preview_selector_repair(
    payload: SelectorRepairPreviewApiRequest,
) -> SelectorRepairPreviewResult:
    try:
        return preview_suggestion(
            payload.platform_id,
            payload.suggestion,
            payload.fixture_html,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
