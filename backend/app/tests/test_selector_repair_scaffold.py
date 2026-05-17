from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.selector_repair import (
    SelectorCandidate,
    SelectorRepairRequest,
    SelectorRepairSuggestion,
)
from app.services.crawling.public_parser.selector_repair.html_sanitizer import sanitize_html
import app.services.crawling.public_parser.selector_repair.selector_repair_service as repair_service
from app.services.llm.mock_provider import MockProvider


client = TestClient(app)

FIXTURE_HTML = """
<html>
  <head>
    <style>.secret{display:none}</style>
    <script>window.token = "secret";</script>
  </head>
  <body>
    <article class="thread" onclick="steal()">
      <h1 class="thread-title">Fixture title</h1>
      <div class="thread-author">public_author</div>
      <div class="thread-created-at">2026-05-15T00:00:00Z</div>
      <div class="thread-content">Fixture public thread content.</div>
      <div class="reply-item">
        <div class="reply-author">commenter</div>
        <div class="reply-content">Visible public reply.</div>
      </div>
    </article>
  </body>
</html>
"""


def test_html_sanitizer_removes_scripts_styles_events_and_obvious_tokens() -> None:
    html = """
    <div onclick="alert(1)" data-safe="ok">public</div>
    <script>token=abc123</script>
    <style>body{color:red}</style>
    <meta name="csrf-token" content="secret">
    token=abc123; session_id="secret"; client_secret='secret'
    """

    sanitized = sanitize_html(html)

    assert "<script" not in sanitized.lower()
    assert "<style" not in sanitized.lower()
    assert "onclick" not in sanitized.lower()
    assert "csrf-token" not in sanitized.lower()
    assert "abc123" not in sanitized
    assert "client_secret=[REDACTED]" in sanitized
    assert "data-safe" in sanitized


def test_html_sanitizer_limits_length() -> None:
    sanitized = sanitize_html("x" * 100, max_chars=12)

    assert sanitized == "x" * 12


def test_env_example_documents_selector_repair_defaults() -> None:
    env_example = (Path(__file__).resolve().parents[3] / ".env.example").read_text(encoding="utf-8")

    assert "SELECTOR_REPAIR_MODE=mock" in env_example
    assert "SELECTOR_REPAIR_ENABLE_REAL_LLM=false" in env_example
    assert "SELECTOR_REPAIR_MAX_HTML_CHARS=20000" in env_example


def test_repair_request_builds_safely(monkeypatch) -> None:
    monkeypatch.setenv("SELECTOR_REPAIR_MODE", "mock")
    monkeypatch.setenv("SELECTOR_REPAIR_MAX_HTML_CHARS", "200")

    request = repair_service.build_repair_request(
        "hupu",
        FIXTURE_HTML,
        profile={"title_selector": ".old-title"},
        error_summary="title selector missing",
        extraction_targets=["title", "content"],
    )

    assert request.platform_id == "hupu"
    assert request.mode == "mock"
    assert request.max_html_chars == 200
    assert request.current_profile == {"title_selector": ".old-title"}
    assert request.extraction_targets == ["title", "content"]
    assert "<script" not in request.sanitized_html.lower()
    assert "onclick" not in request.sanitized_html.lower()


def test_mock_provider_returns_deterministic_selector_suggestions() -> None:
    request = SelectorRepairRequest(
        platform_id="hupu",
        sanitized_html=sanitize_html(FIXTURE_HTML),
        current_profile={"title_selector": ".old-title"},
        extraction_targets=["title", "content", "comment_content"],
        parser_error_summary="selectors missing",
    )

    first = MockProvider().suggest_selector_repair(request)
    second = MockProvider().suggest_selector_repair(request)

    assert first.model_dump() == second.model_dump()
    assert first.platform_id == "hupu"
    assert first.generated_by_mock is True
    assert first.applied is False
    assert first.review_required is True
    assert "active_profiles_not_modified" in first.warnings
    assert {candidate.target for candidate in first.candidates} == {
        "title",
        "content",
        "comment_content",
    }


def test_selector_repair_service_never_uses_real_provider(monkeypatch) -> None:
    class RealishProvider:
        provider_id = "openai"

        def suggest_selector_repair(self, request):
            pytest.fail("real provider must not be used")

    monkeypatch.setenv("SELECTOR_REPAIR_MODE", "mock")
    monkeypatch.setattr(repair_service, "get_llm_provider", lambda: RealishProvider())
    request = repair_service.build_repair_request(
        "hupu",
        FIXTURE_HTML,
        error_summary="selectors missing",
        extraction_targets=["title"],
    )

    suggestion = repair_service.suggest_selectors(request)

    assert suggestion.generated_by_mock is True
    assert "configured_real_provider_not_used" in suggestion.warnings
    assert suggestion.candidates[0].selector == "h1"


def test_future_real_selector_repair_mode_is_disabled(monkeypatch) -> None:
    monkeypatch.setenv("SELECTOR_REPAIR_MODE", "future_real_llm")
    request = repair_service.build_repair_request(
        "hupu",
        FIXTURE_HTML,
        error_summary="selectors missing",
        extraction_targets=["title"],
    )

    suggestion = repair_service.suggest_selectors(request)

    assert suggestion.status == "provider_not_enabled"
    assert suggestion.candidates == []
    assert "selector_repair_real_llm_disabled" in suggestion.warnings


def test_preview_suggestion_works_against_fixture_html() -> None:
    suggestion = SelectorRepairSuggestion(
        platform_id="hupu",
        candidates=[
            SelectorCandidate(target="title", selector="h1.thread-title", confidence=0.9),
            SelectorCandidate(target="content", selector=".thread-content", confidence=0.9),
            SelectorCandidate(target="comment_content", selector=".reply-content", confidence=0.9),
        ],
    )

    preview = repair_service.preview_suggestion("hupu", suggestion, FIXTURE_HTML)

    assert preview.status == "preview_ok"
    assert preview.profile_modified is False
    assert preview.matched_targets == {
        "title": True,
        "content": True,
        "comment_content": True,
    }
    assert preview.sample_values["title"] == "Fixture title"
    assert preview.sample_values["comment_content"] == "Visible public reply."


def test_invalid_platform_fails_safely() -> None:
    with pytest.raises(ValueError, match="not registered"):
        repair_service.build_repair_request("unknown_source", FIXTURE_HTML)

    response = client.post(
        "/api/v1/public-parsers/selector-repair/suggest",
        json={"platform_id": "unknown_source", "html": FIXTURE_HTML},
    )

    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_selector_repair_api_suggest_and_preview() -> None:
    suggest_response = client.post(
        "/api/v1/public-parsers/selector-repair/suggest",
        json={
            "platform_id": "hupu",
            "html": FIXTURE_HTML,
            "profile": {"title_selector": ".old-title"},
            "extraction_targets": ["title", "content"],
            "error_summary": "selectors missing",
        },
    )

    assert suggest_response.status_code == 200
    suggestion = suggest_response.json()
    assert suggestion["platform_id"] == "hupu"
    assert suggestion["generated_by_mock"] is True
    assert suggestion["applied"] is False
    assert suggestion["review_required"] is True

    preview_response = client.post(
        "/api/v1/public-parsers/selector-repair/preview",
        json={
            "platform_id": "hupu",
            "suggestion": suggestion,
            "fixture_html": FIXTURE_HTML,
        },
    )

    assert preview_response.status_code == 200
    preview = preview_response.json()
    assert preview["profile_modified"] is False
    assert preview["matched_targets"]["title"] is True
    assert preview["matched_targets"]["content"] is True


def test_selector_repair_does_not_modify_active_profiles() -> None:
    profile_path = (
        Path(__file__).resolve().parents[1]
        / "services"
        / "crawling"
        / "public_parser"
        / "profiles"
        / "hupu.json"
    )
    before = profile_path.read_text(encoding="utf-8")
    request = repair_service.build_repair_request(
        "hupu",
        FIXTURE_HTML,
        error_summary="selectors missing",
        extraction_targets=["title"],
    )
    suggestion = repair_service.suggest_selectors(request)
    draft = repair_service.save_suggestion_as_draft(suggestion)
    repair_service.preview_suggestion("hupu", draft, FIXTURE_HTML)
    after = profile_path.read_text(encoding="utf-8")

    assert draft.status == "draft"
    assert draft.applied is False
    assert draft.review_required is True
    assert before == after
