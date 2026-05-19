# Douyin Web App Integration Plan

Last updated: 2026-05-19

This document records the readiness scaffold for a future Douyin Web App integration. It is based on the two uploaded research reports in the parent project folder plus the current Sentigraph adapter/registry state. Any console-specific detail should still be rechecked against the latest Douyin Open Platform UI before implementation.

## 1. Current Status

Douyin remains mock-first in Sentigraph. No real Douyin API calls are made, no scraping is implemented, and `DOUYIN_ADAPTER_MODE=real` is intentionally blocked.

Current safe status values:

```text
developer_access_status=obtained
app_type=web_app
comment_api_status=item_comment_scope_not_verified
recommended_comment_scope=item.comment
video_comment_scope_status=not_recommended_for_mvp
real_mode_blocker=oauth_and_scope_not_verified
permission_status=permission_not_verified
oauth_status=scaffold_documented_not_implemented
token_exchange_status=placeholder_not_implemented
item_id_source_status=not_confirmed
scope_status=unverified
real_calls_enabled=false
```

Real Douyin mode must stay disabled until all of these are verified:

- `item.comment` or the current official equivalent comment scope is approved.
- The Web App redirect URI is configured in the Douyin developer console.
- A test account has completed authorization.
- Access and refresh tokens are obtained through the official OAuth flow.
- The lawful source of `item_id` values is confirmed.
- Approved payload fixtures are captured and normalized in tests without live network calls.

The research reports recommend `item.comment` as the MVP comment-access path rather than treating older or enterprise-account-oriented `video.comment` references as the main line.

## 2. Environment Placeholders

The repository only provides placeholders in `.env.example`; real values must stay in ignored local `.env` files or a future secret store.

```text
DOUYIN_ADAPTER_MODE=mock
DOUYIN_CLIENT_KEY=
DOUYIN_CLIENT_SECRET=
DOUYIN_REDIRECT_URI=
DOUYIN_ACCESS_TOKEN=
DOUYIN_REFRESH_TOKEN=
DOUYIN_CLIENT_TOKEN=
DOUYIN_STABLE_CLIENT_TOKEN=
DOUYIN_ENABLE_REAL_CALLS=false
DOUYIN_SCOPE_STATUS=unverified
```

Never print or commit `client_key`, `client_secret`, `access_token`, `refresh_token`, `client_token`, or `stable_client_token`. API responses and logs should expose only boolean credential presence.

Token meanings for the future implementation:

- `access_token`: user-authorized token used for user-scoped APIs after OAuth authorization.
- `refresh_token`: token used to refresh an expired user access token.
- `client_token`: app/client credential token for app-level APIs if Douyin grants a relevant product path.
- `stable_client_token`: longer-lived app/client token variant if the console exposes it for an approved product path.

The MVP `item.comment` route should be treated as user-authorized until the console proves otherwise. App/client tokens are placeholders only and are not sufficient to enable comment ingestion.

## 3. OAuth Scaffold Design

No OAuth endpoint is implemented in this scaffold. A non-network helper module exists for URL/callback validation only. The intended future API design is:

- `GET /api/v1/douyin/oauth/authorize-url`
  Returns a generated authorization URL using `client_key`, `redirect_uri`, requested scopes, and a one-time `state` value. The intended Douyin-side browser authorization concept is `/platform/oauth/connect/` with `response_type=code`. The MVP scope request should start with `user_info,item.comment`; in test mode, add `trial.whitelist` only if the console requires it. The response must not expose secrets.

- `GET /api/v1/douyin/oauth/callback`
  Receives `code`, `state`, and granted scopes. It validates the `state`, records only safe authorization metadata, and does not print the code.

- `POST /api/v1/douyin/oauth/token/exchange`
  Placeholder for exchanging an authorization code for tokens through the official Douyin OAuth endpoint, expected conceptually as `/oauth/access_token/`. This remains disabled until token storage and scope verification are reviewed.

- `POST /api/v1/douyin/oauth/token/refresh`
  Placeholder for refreshing tokens through the official refresh-token flow, expected conceptually as `/oauth/refresh_token/`; a later `renew_refresh_token` path may be needed if the account/app is approved for it. This remains disabled until encrypted or otherwise protected token storage is designed.

OAuth safety rules:

- Generate unpredictable `state` values and expire them quickly.
- Validate the configured redirect URI against an allowlist.
- Use a complete HTTPS redirect URI registered in the console.
- Reject non-HTTPS, malformed, query-string, or fragment-bearing redirect URIs in local validation.
- Do not attach business query parameters to `redirect_uri`; put opaque business context in `state`.
- Never log OAuth codes or token payloads.
- Store tokens only after storage/security review.
- Treat granted scopes as runtime metadata; do not assume `item.comment` until confirmed.
- Treat test-application quota and whitelist limits as product constraints; do not build bulk crawling behavior around test-mode credentials.

## 4. item.comment Readiness

The future item-comment flow should only use official Web App APIs. It must not use page scraping, cookies, browser automation, captcha bypass, anti-bot evasion, or private data access.

Readiness checks:

- Confirm the exact scope name and approval state for `item.comment`.
- Treat `video.comment` as not recommended for this MVP path unless the console proves it is the correct Web App product for the approved account type.
- Confirm whether comment access is limited to authorized-user videos, owned videos, or a broader approved data product.
- Confirm how `item_id` can be lawfully obtained for a case.
- Prefer authorized account video-list/detail sources such as `video.list.bind` / `video.data.bind`, a posting/share callback, or a manual verified seed as the first `item_id` source.
- Treat public keyword video search and search-comment products as separate future capabilities, not prerequisites for the MVP authorized-account comment path.
- Confirm comment pagination, reply availability, rate limits, and error codes.
- Capture approved mock fixtures for video metadata, `/item/comment/list/` top-level comments, `/item/comment/reply/list/` replies if allowed, comments-disabled results, permission-denied results, and quota/rate-limit results.

## 5. Planned Schemas

These are design placeholders, not implemented storage contracts yet.

### DouyinAccount

```json
{
  "open_id": "string",
  "nickname": "string",
  "avatar_url": "string|null",
  "authorized_scopes": ["item.comment"],
  "authorized_at": "datetime",
  "token_status": "missing|valid|expired|refresh_required",
  "safe_metadata_only": true
}
```

### DouyinVideo

```json
{
  "item_id": "string",
  "title": "string",
  "description": "string",
  "author_open_id": "string|null",
  "like_count": 0,
  "comment_count": 0,
  "share_count": 0,
  "published_at": "datetime|null",
  "url": "string|null",
  "raw_data": {"safe_metadata_only": true}
}
```

### DouyinComment

```json
{
  "comment_id": "string",
  "item_id": "string",
  "parent_id": "string|null",
  "author_open_id": "string|null",
  "author_name": "string|null",
  "content": "string",
  "like_count": 0,
  "reply_count": 0,
  "created_at": "datetime|null",
  "raw_data": {"safe_metadata_only": true}
}
```

### DouyinFetchJob

```json
{
  "job_id": "string",
  "case_id": "string|null",
  "item_ids": ["string"],
  "requested_limit": 20,
  "effective_limit": 20,
  "status": "planned|blocked|running|completed|failed",
  "blocked_reason": "oauth_and_scope_not_verified",
  "safe_counts": {
    "video_count": 0,
    "comment_count": 0
  }
}
```

### DouyinOAuthState

```json
{
  "state_id": "string",
  "state_hash": "string",
  "redirect_uri": "string",
  "requested_scopes": ["item.comment"],
  "created_at": "datetime",
  "expires_at": "datetime",
  "consumed_at": "datetime|null"
}
```

## 6. Sentigraph Mapping

Future Douyin `DouyinVideo` items should normalize into `RawPost` with `platform="douyin"`, `post_id=item_id`, public title/description/statistics, URL if available, and safe metadata only.

Future Douyin `DouyinComment` items should normalize into `RawComment` with `platform="douyin"`, `post_id=item_id`, `comment_id`, `parent_id`, author display metadata when allowed, public comment text, counts, timestamps, and safe metadata only.

Case analysis may use attached Douyin raw comments only after explicit case-scoped ingestion. Missing or blocked Douyin real data must fall back to existing deterministic mock behavior.

## 7. Test Plan

Required tests before real-mode code:

- Mock mode still returns deterministic `RawPost` and `RawComment` data.
- `DOUYIN_ADAPTER_MODE=real` without complete OAuth config returns `config_error` and mock data.
- `DOUYIN_ADAPTER_MODE=real` with placeholder credentials returns `permission_not_verified` and mock data.
- No real network calls are made in automated tests.
- Credential values never appear in API responses, logs, metadata, snapshots, or cache files.
- Platform registry exposes only readiness booleans and safe statuses.

Required tests before future live-mode enablement:

- Mocked official OAuth callback payloads validate `state`.
- Mocked token exchange/refresh responses are redacted before persistence.
- Mocked `item.comment` payloads normalize to existing Sentigraph schemas.
- Permission-denied, comments-disabled, quota/rate-limit, and malformed-payload cases fail safely.

## 8. Non-Goals

- No real Douyin API call in this readiness scaffold.
- No scraping or browser-cookie use.
- No login, captcha, or anti-bot bypass.
- No private data collection.
- No real LLM call.
- No automatic real-world moderation or outreach action.
