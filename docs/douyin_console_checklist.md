# Douyin Console Verification Checklist

Last updated: 2026-05-19

Use this checklist before any real Douyin OAuth or `item.comment` implementation. This is an operator checklist only; Sentigraph must keep Douyin mock fallback active until these items are verified and sanitized fixture payloads are captured.

## App Identity

- Confirm the app type is Web App.
- Confirm the Client Key exists.
- Confirm the Client Secret exists.
- Confirm no credential value is copied into docs, screenshots, tickets, logs, or API responses.
- Confirm whether the app is in test, preview, or production status.

## Redirect URI

- Confirm the redirect URI is configured in the Douyin console.
- Confirm the redirect URI is HTTPS.
- Confirm the redirect URI includes the full callback path.
- Confirm the redirect URI has no query string or fragment.
- Confirm Sentigraph stores any business context in OAuth `state`, not in the redirect URI.

## Test Authorization

- Confirm preview whitelist / test Douyin account configuration.
- Confirm whether `trial.whitelist` or another test-mode scope is required.
- Confirm `user_info` is available for the test account.
- Confirm the authorization callback returns `code`, `state`, and granted scope metadata.
- Confirm daily testing quota limits and any per-endpoint test restrictions.

## Comment Permission

- Confirm `item.comment` is approved or pending.
- Confirm whether `item.comment` is the current official Web App route for comment list and reply list.
- Confirm `video.comment` status; keep it `not_recommended_for_mvp` unless the console says it is the right route.
- Confirm whether access is only for authorized account videos, owned videos, or broader approved content.
- Confirm whether keyword video comment APIs are available. Treat keyword/discovery APIs as separate from the MVP unless explicitly approved.

## Item ID Source

- Confirm whether `video.list.bind` is available or pending.
- Confirm whether `video.data.bind` is available or pending.
- Confirm whether posting/share callbacks can provide lawful `item_id` values.
- Confirm whether manual verified item IDs are acceptable for the first smoke test.
- Do not request comments for unverified item IDs.

## API Behavior to Capture as Sanitized Fixtures

- Successful video/item metadata response.
- Successful top-level comment list response.
- Successful reply list response if replies are approved.
- Comments-disabled response.
- Permission-denied response.
- Quota/rate-limit response.
- Expired-token response.
- Malformed or partial payload response.

## Non-Negotiable Boundaries

- No scraping.
- No cookies.
- No login bypass.
- No captcha bypass.
- No anti-bot evasion.
- No real API call from automated tests.
- No credential printing.
- No real LLM calls.
