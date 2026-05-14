from pydantic import BaseModel


class PlatformSource(BaseModel):
    platform_id: str
    display_name: str
    category: str
    source_type: str
    status: str
    enabled_in_mvp: bool
    selectable_for_mock: bool
    official_platform_url: str | None = None
    notes: str


class PlatformRegistryResponse(BaseModel):
    platforms: list[PlatformSource]
    active_mvp_platforms: list[str]
