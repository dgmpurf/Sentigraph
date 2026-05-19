from __future__ import annotations

import urllib.request
from urllib.parse import parse_qs, urlparse

import pytest

from app.services.crawling.douyin_oauth import (
    DouyinOAuthConfigError,
    DouyinOAuthNotImplementedError,
    build_authorization_url,
    exchange_code_for_token,
    parse_callback_params,
    refresh_access_token,
    validate_redirect_uri,
)


def test_douyin_authorization_url_excludes_client_secret() -> None:
    url = build_authorization_url(
        client_key="client-key-safe-id",
        redirect_uri="https://example.com/oauth/douyin/callback",
        state="csrf-state-123",
        scopes=("user_info", "item.comment"),
        optional_scopes=("trial.whitelist",),
    )
    parsed = urlparse(url)
    query = parse_qs(parsed.query)

    assert parsed.scheme == "https"
    assert "client_secret" not in query
    assert "client-key-safe-id" in query["client_key"]
    assert query["redirect_uri"] == ["https://example.com/oauth/douyin/callback"]
    assert query["state"] == ["csrf-state-123"]
    assert query["scope"] == ["user_info,item.comment"]
    assert query["optionalScope"] == ["trial.whitelist"]


@pytest.mark.parametrize(
    "redirect_uri",
    [
        "http://example.com/oauth/douyin/callback",
        "https:///missing-host",
        "not a url",
        "https://example.com/oauth/douyin/callback?case_id=case_001",
        "https://example.com/oauth/douyin/callback#fragment",
    ],
)
def test_douyin_redirect_uri_validation_rejects_unsafe_values(redirect_uri: str) -> None:
    with pytest.raises(DouyinOAuthConfigError):
        validate_redirect_uri(redirect_uri)


def test_douyin_redirect_uri_validation_accepts_https_path() -> None:
    assert (
        validate_redirect_uri("https://example.com/oauth/douyin/callback")
        == "https://example.com/oauth/douyin/callback"
    )


def test_douyin_callback_parser_handles_code_state_and_scopes() -> None:
    callback = parse_callback_params(
        {
            "code": "callback-code",
            "state": "csrf-state-123",
            "scopes": "user_info,item.comment",
        }
    )

    assert callback.code == "callback-code"
    assert callback.state == "csrf-state-123"
    assert callback.scopes == ("user_info", "item.comment")
    assert callback.error is None


def test_douyin_callback_parser_handles_error_without_secret_fields() -> None:
    callback = parse_callback_params("error=access_denied&state=csrf-state-123")

    assert callback.code is None
    assert callback.state == "csrf-state-123"
    assert callback.error == "access_denied"
    assert callback.scopes == ()


def test_douyin_token_placeholders_do_not_call_network(monkeypatch: pytest.MonkeyPatch) -> None:
    def fail_urlopen(*args: object, **kwargs: object) -> object:
        del args, kwargs
        raise AssertionError("Douyin OAuth scaffold must not call network.")

    monkeypatch.setattr(urllib.request, "urlopen", fail_urlopen)

    with pytest.raises(DouyinOAuthNotImplementedError):
        exchange_code_for_token(code="code")
    with pytest.raises(DouyinOAuthNotImplementedError):
        refresh_access_token(refresh_token="refresh")
