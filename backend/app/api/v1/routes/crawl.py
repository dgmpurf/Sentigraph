from fastapi import APIRouter

from app.schemas.crawl import CrawlStartRequest, CrawlStartResponse
from app.services.crawling.crawl_service import start_crawl_with_adapters

router = APIRouter()


@router.post("/start", response_model=CrawlStartResponse)
def start_crawl(payload: CrawlStartRequest) -> CrawlStartResponse:
    return start_crawl_with_adapters(payload)
