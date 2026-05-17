from __future__ import annotations

import hashlib
import os
from typing import Any

from app.schemas.selector_repair import (
    SelectorRepairPreviewResult,
    SelectorRepairRequest,
    SelectorRepairSuggestion,
)
from app.services.crawling.public_parser.html_cleaner import select_nodes
from app.services.crawling.public_parser.errors import SelectorProfileError
from app.services.crawling.public_parser.parser_registry import has_public_parser
from app.services.crawling.public_parser.selector_profile import SelectorProfile, load_selector_profile
from app.services.crawling.public_parser.selector_repair.html_sanitizer import (
    DEFAULT_MAX_HTML_CHARS,
    sanitize_html,
)
from app.services.llm.errors import LLMProviderError
from app.services.llm.mock_provider import MockProvider
from app.services.llm.provider_factory import get_llm_provider


SELECTOR_REPAIR_MODE_MOCK = "mock"
SELECTOR_REPAIR_MODE_FUTURE_REAL_LLM = "future_real_llm"


def build_repair_request(
    platform_id: str,
    html: str,
    profile: dict[str, Any] | None = None,
    error_summary: str = "",
    extraction_targets: list[str] | None = None,
) -> SelectorRepairRequest:
    normalized_platform = platform_id.strip().lower()
    if not has_public_parser(normalized_platform):
        raise ValueError(f"Public parser platform is not registered for '{platform_id}'.")

    try:
        loaded_profile = load_selector_profile(normalized_platform)
    except SelectorProfileError as exc:
        raise ValueError(f"Selector profile is unavailable for '{platform_id}'.") from exc
    current_profile = profile or loaded_profile.model_dump(mode="json")
    max_chars = _selector_repair_max_html_chars()
    targets = extraction_targets or _targets_from_profile(loaded_profile)

    return SelectorRepairRequest(
        platform_id=normalized_platform,
        sanitized_html=sanitize_html(html, max_chars=max_chars),
        current_profile=current_profile,
        extraction_targets=_dedupe(targets),
        parser_error_summary=error_summary,
        mode=_selector_repair_mode(),
        max_html_chars=max_chars,
    )


def suggest_selectors(request: SelectorRepairRequest) -> SelectorRepairSuggestion:
    mode = _selector_repair_mode()
    if mode != SELECTOR_REPAIR_MODE_MOCK:
        return SelectorRepairSuggestion(
            platform_id=request.platform_id,
            status="provider_not_enabled",
            candidates=[],
            warnings=["selector_repair_real_llm_disabled"],
            provider="mock",
            generated_by_mock=True,
            applied=False,
            review_required=True,
        )

    warnings: list[str] = []
    provider = MockProvider()
    try:
        configured_provider = get_llm_provider()
        if isinstance(configured_provider, MockProvider):
            provider = configured_provider
        else:
            warnings.append("configured_real_provider_not_used")
    except LLMProviderError:
        warnings.append("configured_provider_unavailable_mock_used")

    suggestion = provider.suggest_selector_repair(request)
    if warnings:
        suggestion = suggestion.model_copy(update={"warnings": _dedupe([*suggestion.warnings, *warnings])})
    return suggestion


def preview_suggestion(
    platform_id: str,
    suggestion: SelectorRepairSuggestion,
    fixture_html: str,
) -> SelectorRepairPreviewResult:
    normalized_platform = platform_id.strip().lower()
    if not has_public_parser(normalized_platform):
        raise ValueError(f"Public parser platform is not registered for '{platform_id}'.")

    sanitized = sanitize_html(fixture_html, max_chars=_selector_repair_max_html_chars())
    matched_targets: dict[str, bool] = {}
    sample_values: dict[str, str] = {}
    warnings: list[str] = []

    for candidate in suggestion.candidates:
        if candidate.selector_type != "css":
            warnings.append(f"unsupported_selector_type:{candidate.target}")
            matched_targets.setdefault(candidate.target, False)
            continue
        nodes = select_nodes(sanitized, candidate.selector)
        matched = bool(nodes)
        matched_targets[candidate.target] = matched_targets.get(candidate.target, False) or matched
        if matched and candidate.target not in sample_values:
            sample_values[candidate.target] = nodes[0].text_content()[:500]

    if not matched_targets:
        warnings.append("no_selector_candidates")
    elif not all(matched_targets.values()):
        warnings.append("some_selector_candidates_unmatched")

    status = "preview_ok" if matched_targets and all(matched_targets.values()) else "preview_failed"
    return SelectorRepairPreviewResult(
        platform_id=normalized_platform,
        status=status,
        matched_targets=matched_targets,
        sample_values=sample_values,
        warnings=_dedupe(warnings),
        suggestion=suggestion,
        profile_modified=False,
    )


def save_suggestion_as_draft(suggestion: SelectorRepairSuggestion) -> SelectorRepairSuggestion:
    """Return a draft marker without writing or modifying active profile files."""

    digest = hashlib.sha1(suggestion.model_dump_json().encode("utf-8")).hexdigest()[:12]
    return suggestion.model_copy(
        update={
            "status": "draft",
            "draft_id": f"{suggestion.platform_id}_selector_draft_{digest}",
            "applied": False,
            "review_required": True,
        }
    )


def _targets_from_profile(profile: SelectorProfile) -> list[str]:
    profile_data = profile.model_dump(mode="json")
    targets: list[str] = []
    for key, value in profile_data.items():
        if not key.endswith("_selector") or not value:
            continue
        targets.append(key.removesuffix("_selector"))
    if not targets:
        return ["title", "content"]
    return targets


def _selector_repair_mode() -> str:
    value = os.getenv("SELECTOR_REPAIR_MODE", SELECTOR_REPAIR_MODE_MOCK).strip().lower()
    if value in {SELECTOR_REPAIR_MODE_MOCK, SELECTOR_REPAIR_MODE_FUTURE_REAL_LLM}:
        return value
    return SELECTOR_REPAIR_MODE_MOCK


def _selector_repair_max_html_chars() -> int:
    raw = os.getenv("SELECTOR_REPAIR_MAX_HTML_CHARS", str(DEFAULT_MAX_HTML_CHARS))
    try:
        parsed = int(raw)
    except (TypeError, ValueError):
        return DEFAULT_MAX_HTML_CHARS
    if parsed <= 0:
        return DEFAULT_MAX_HTML_CHARS
    return min(parsed, DEFAULT_MAX_HTML_CHARS)


def _dedupe(values: list[str]) -> list[str]:
    return list(dict.fromkeys(value for value in values if value))
