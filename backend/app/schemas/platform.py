from pydantic import BaseModel, Field


class PlatformSource(BaseModel):
    platform: str | None = None
    platform_id: str
    display_name: str
    category: str
    source_type: str
    integration_type: str = "mock_scaffold"
    status: str
    enabled_in_mvp: bool
    selectable_for_mock: bool
    mock_available: bool = False
    real_mode_available: bool = False
    real_mode_configured: bool = False
    api_approval_required: bool = False
    api_approval_status: str = "not_required"
    developer_access_status: str | None = None
    app_type: str | None = None
    comment_api_status: str | None = None
    recommended_comment_scope: str | None = None
    video_comment_scope_status: str | None = None
    required_credentials: list[str] = Field(default_factory=list)
    required_scopes: list[str] = Field(default_factory=list)
    scope_status: str = "not_required"
    oauth_required: bool = False
    oauth_status: str = "not_required"
    real_mode_blocker: str | None = None
    data_access_level: str = "mock_or_fixture_data"
    next_user_action: str = "Use mock/offline mode until official access is verified."
    quota_cache_protected: bool = False
    credentials_required: list[str] = Field(default_factory=list)
    credentials_present: dict[str, bool] = Field(default_factory=dict)
    credential_present: bool = False
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
