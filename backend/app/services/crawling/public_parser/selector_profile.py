from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, Field

from app.services.crawling.public_parser.errors import SelectorProfileError


PROFILE_DIR = Path(__file__).resolve().parent / "profiles"


class SelectorProfile(BaseModel):
    platform_id: str
    display_name: str
    base_url: str
    allowed_public_paths: list[str] = Field(default_factory=list)
    search_url_template: str | None = None
    article_selector: str
    title_selector: str
    content_selector: str
    author_selector: str | None = None
    created_at_selector: str | None = None
    comment_selector: str | None = None
    next_page_selector: str | None = None
    rate_limit_seconds: float = 3.0
    notes: str = ""
    status: str = "fixture_only"
    fixture_url: str | None = None


def load_selector_profile(platform_id: str, *, profiles_dir: Path | None = None) -> SelectorProfile:
    profile_dir = profiles_dir or PROFILE_DIR
    profile_path = profile_dir / f"{platform_id.strip().lower()}.json"
    if not profile_path.exists():
        raise SelectorProfileError(f"Selector profile is not registered for '{platform_id}'.")
    try:
        raw = json.loads(profile_path.read_text(encoding="utf-8"))
        return SelectorProfile.model_validate(raw)
    except json.JSONDecodeError as exc:
        raise SelectorProfileError(f"Selector profile JSON is invalid for '{platform_id}'.") from exc


def list_selector_profiles(*, profiles_dir: Path | None = None) -> list[SelectorProfile]:
    profile_dir = profiles_dir or PROFILE_DIR
    profiles: list[SelectorProfile] = []
    if not profile_dir.exists():
        return profiles
    for profile_path in sorted(profile_dir.glob("*.json")):
        profiles.append(load_selector_profile(profile_path.stem, profiles_dir=profile_dir))
    return profiles


def get_profile_ids(*, profiles_dir: Path | None = None) -> list[str]:
    return [profile.platform_id for profile in list_selector_profiles(profiles_dir=profiles_dir)]

