from pydantic import BaseModel, Field

from app.schemas.evidence import EvidenceAcquisitionMode, EvidenceType


class SourceCatalogEntry(BaseModel):
    source_id: str
    display_name: str
    category: str
    feasibility_status: str
    acquisition_modes: list[EvidenceAcquisitionMode] = Field(default_factory=list)
    allowed_data_types: list[EvidenceType] = Field(default_factory=list)
    forbidden_data_types: list[str] = Field(default_factory=list)
    current_status: str
    compliance_notes: str
    next_action: str
    priority: str = "medium"


class SourceCatalogCategory(BaseModel):
    category_id: str
    display_name: str
    description: str
    sources: list[SourceCatalogEntry] = Field(default_factory=list)


class SourceCatalogResponse(BaseModel):
    categories: list[SourceCatalogCategory]
    total_categories: int
    total_sources: int
    safe_mode: dict[str, bool] = Field(
        default_factory=lambda: {
            "static_metadata_only": True,
            "real_api_calls": False,
            "real_llm_calls": False,
            "live_fetch_enabled": False,
            "cookies_used": False,
            "scraping_bypass": False,
            "secrets_exposed": False,
            "third_party_crawler_integrated": False,
        }
    )
