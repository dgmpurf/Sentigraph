from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping
from urllib.parse import parse_qsl, urlencode, urlparse


DOUYIN_AUTHORIZE_URL = "https://open.douyin.com/platform/oauth/connect/"
DEFAULT_DOUYIN_SCOPES = ("user_info", "item.comment")


class DouyinOAuthConfigError(ValueError):
    """Raised when the OAuth scaffold receives unsafe local configuration."""


class DouyinOAuthNotImplementedError(RuntimeError):
    """Raised by placeholder token flows that must not make network calls yet."""


@dataclass(frozen=True)
class DouyinOAuthCallback:
    code: str | None
    state: str | None
    scopes: tuple[str, ...]
    error: str | None = None
    error_description: str | None = None


def validate_redirect_uri(redirect_uri: str) -> str:
    uri = str(redirect_uri or "").strip()
    parsed = urlparse(uri)
    if parsed.scheme != "https":
        raise DouyinOAuthConfigError("douyin_redirect_uri_must_use_https")
    if not parsed.netloc:
        raise DouyinOAuthConfigError("douyin_redirect_uri_missing_host")
    if parsed.query or parsed.fragment:
        raise DouyinOAuthConfigError("douyin_redirect_uri_must_be_exact_path_without_query")
    return uri


def build_authorization_url(
    *,
    client_key: str,
    redirect_uri: str,
    state: str,
    scopes: tuple[str, ...] | list[str] | None = None,
    optional_scopes: tuple[str, ...] | list[str] | None = None,
) -> str:
    safe_client_key = str(client_key or "").strip()
    if not safe_client_key:
        raise DouyinOAuthConfigError("douyin_client_key_required")
    safe_state = str(state or "").strip()
    if not safe_state:
        raise DouyinOAuthConfigError("douyin_oauth_state_required")

    requested_scopes = tuple(scopes or DEFAULT_DOUYIN_SCOPES)
    query = {
        "client_key": safe_client_key,
        "response_type": "code",
        "scope": ",".join(_normalize_scopes(requested_scopes)),
        "redirect_uri": validate_redirect_uri(redirect_uri),
        "state": safe_state,
    }
    normalized_optional = _normalize_scopes(tuple(optional_scopes or ()))
    if normalized_optional:
        query["optionalScope"] = ",".join(normalized_optional)
    return f"{DOUYIN_AUTHORIZE_URL}?{urlencode(query)}"


def parse_callback_params(params: Mapping[str, object] | str) -> DouyinOAuthCallback:
    if isinstance(params, str):
        parsed_params = dict(parse_qsl(params.lstrip("?"), keep_blank_values=True))
    else:
        parsed_params = {str(key): str(value) for key, value in params.items()}
    scope_text = parsed_params.get("scopes") or parsed_params.get("scope") or ""
    return DouyinOAuthCallback(
        code=_non_empty(parsed_params.get("code")),
        state=_non_empty(parsed_params.get("state")),
        scopes=_normalize_scope_text(scope_text),
        error=_non_empty(parsed_params.get("error")),
        error_description=_non_empty(parsed_params.get("error_description")),
    )


def exchange_code_for_token(*_: object, **__: object) -> None:
    raise DouyinOAuthNotImplementedError("douyin_oauth_token_exchange_placeholder_no_network_call")


def refresh_access_token(*_: object, **__: object) -> None:
    raise DouyinOAuthNotImplementedError("douyin_oauth_refresh_token_placeholder_no_network_call")


def _normalize_scopes(scopes: tuple[str, ...]) -> tuple[str, ...]:
    cleaned: list[str] = []
    for scope in scopes:
        safe_scope = str(scope or "").strip()
        if safe_scope and safe_scope not in cleaned:
            cleaned.append(safe_scope)
    return tuple(cleaned)


def _normalize_scope_text(scope_text: str) -> tuple[str, ...]:
    normalized = str(scope_text or "").replace(",", " ")
    return _normalize_scopes(tuple(part for part in normalized.split(" ") if part))


def _non_empty(value: object) -> str | None:
    text = str(value or "").strip()
    return text or None
