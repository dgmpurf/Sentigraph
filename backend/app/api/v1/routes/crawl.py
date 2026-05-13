from fastapi import APIRouter

from app.schemas.crawl import CrawlStartRequest, CrawlStartResponse
from app.services.mock_service import start_mock_crawl

router = APIRouter()


@router.post("/start", response_model=CrawlStartResponse)
def start_crawl(payload: CrawlStartRequest) -> CrawlStartResponse:
    return start_mock_crawl(payload)

