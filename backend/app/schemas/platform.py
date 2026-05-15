from pydantic import BaseModel, Field


class PlatformSource(BaseModel):
    platform_id: str
    display_name: str
    category: str
    source_type: str
    status: str
    enabled_in_mvp: bool
    selectable_for_mock: bool
    mock_available: bool = False
    real_mode_available: bool = False
    api_approval_required: bool = False
    api_approval_status: str = "not_required"
    credentials_required: list[str] = Field(default_factory=list)
    credentials_present: dict[str, bool] = Field(default_factory=dict)
    api_pending: bool = False
    real_mode_disabled: bool = False
    selectable_for_real: bool = False
    official_platform_url: str | None = None
    notes: str


class PlatformRegistryResponse(BaseModel):
    platforms: list[PlatformSource]
    active_mvp_platforms: list[str]


class PlatformStatusSummary(BaseModel):
    total_platforms: int
    mock_selectable_count: int
    real_selectable_count: int
    api_pending_count: int
    disabled_count: int
    crawler_later_count: int


class PlatformStatusResponse(BaseModel):
    platforms: list[PlatformSource]
    active_mvp_platforms: list[str]
    mock_selectable_platforms: list[str]
    real_selectable_platforms: list[str]
    summary: PlatformStatusSummary
