from fastapi import APIRouter

from app.schemas.keyword import KeywordExpandRequest, KeywordExpandResponse
from app.services.keyword import build_keyword_expansion

router = APIRouter()


@router.post("/expand", response_model=KeywordExpandResponse)
def expand_keywords(payload: KeywordExpandRequest) -> KeywordExpandResponse:
    return build_keyword_expansion(payload)
