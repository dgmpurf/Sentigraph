from fastapi import APIRouter

from app.schemas.source_catalog import SourceCatalogResponse
from app.services.source_catalog import get_source_catalog

router = APIRouter()


@router.get("/catalog", response_model=SourceCatalogResponse)
def get_sources_catalog() -> SourceCatalogResponse:
    return get_source_catalog()
