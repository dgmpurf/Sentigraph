# Real API Capability Audit: Douyin and Xiaohongshu

Date: 2026-05-19

This audit records what Sentigraph must verify before enabling real official API mode for Douyin or Xiaohongshu public-comment ingestion. It is a planning and capability-mapping document only. No real platform APIs were called, no credentials were required, no cookies were used, and no scraping path is proposed.

Official documentation references reviewed:

- Douyin Open Platform: https://developer.open-douyin.com/
- Douyin comment data permission reference observed in official docs/search snippets: `item.comment`
- Xiaohongshu Open Platform: https://open.xiaohongshu.com/
- Xiaohongshu Ark/Open API documentation examples: https://school.xiaohongshu.com/en/open/quick-start/how-to-get-app-key.html and https://school.xiaohongshu.com/en/open/quick-start/system-parameter.html

## Summary

| Platform | Developer Access | Comment API Status | Current Sentigraph Mode | Real Mode Blocker |
| --- | --- | --- | --- | --- |
| Douyin | obtained by user | `item_comment_scope_not_verified` | mock adapter only | `oauth_and_scope_not_verified` |
| Xiaohongshu | obtained by user | `unknown_or_not_confirmed` | mock adapter only | `permission_not_verified` |

Both adapters remain `official_api_adapter_scaffold` implementations. Mock mode stays available. Real mode is disabled until official permission, scope, payload shape, rate limits, and compliance requirements are verified.

## Douyin

Current status:

- Developer access has been obtained by the user.
- App type is tracked as Web App, but redirect URI, OAuth callback/token exchange, approved scopes, and lawful `item_id` source are not yet verified in Sentigraph.
- The local Douyin adapter remains mock-only.
- `DOUYIN_ADAPTER_MODE=real` does not call a real API. With credentials present, it reports `api_pending:permission_not_verified`; without credentials, it reports a safe missing-credential configuration state.

Known required areas to check in the Douyin developer console:

- Whether interaction or comment management permissions are available for the app.
- Whether the app has `item.comment` or the current official equivalent comment permission.
- Whether the Web App redirect URI is configured and a test account can authorize the app.
- Whether OAuth callback and token exchange return the expected safe metadata and granted scopes.
- Whether any keyword video comment management capability is available and what its approval process requires.
- Whether user authorization is required and whether access is limited to authorized users' own videos/items.
- Whether comment reply lists are available through an official endpoint.
- Rate limits, moderation rules, data retention requirements, and audit requirements.

Required future credentials:

- `DOUYIN_CLIENT_KEY`
- `DOUYIN_CLIENT_SECRET`
- `DOUYIN_REDIRECT_URI`
- `DOUYIN_ACCESS_TOKEN`
- `DOUYIN_REFRESH_TOKEN`

Required future scopes:

- `item.comment` or the current official equivalent comment-list permission.
- A reply-list permission if Douyin exposes nested replies through a separate scope.

Future data target:

- Video/post metadata.
- Comment list.
- Comment reply list if available through official APIs.

Minimum integration gate before code can make real calls:

1. Confirm the exact official endpoint names, scopes, and payloads in the Douyin console.
2. Confirm that the Web App redirect URI, test-account authorization, OAuth callback, and token exchange are configured.
3. Confirm that the app is approved for comment access on the intended content class.
4. Confirm the lawful source of `item_id` values.
5. Add response fixtures based on approved official payloads.
6. Implement a reviewed API client behind explicit config gates.
7. Keep tests proving missing credentials, disabled real calls, and network-blocked paths stay safe.

## Xiaohongshu

Current status:

- Developer access has been obtained by the user.
- The exact API product and scope set are unknown.
- Publicly reachable official documentation appears to include commerce/Ark-oriented materials; Sentigraph has not verified an official public note/comment data API.
- The local Xiaohongshu adapter remains mock-only.
- `XIAOHONGSHU_ADAPTER_MODE=real` does not call a real API. With credentials present, it reports `api_pending:permission_not_verified`; without credentials, it reports a safe missing-credential configuration state.

Required console checks:

- Whether an official note/content data API exists for the user's app type.
- Whether official APIs expose note comments or interaction/comment lists.
- Whether comment access is limited to the user's own account, merchant content, advertising/Ark assets, or approved creator content.
- Whether public opinion use cases are allowed under the selected API product terms.
- Whether credentials are named app-key/app-secret or client ID/client secret for the approved product.
- Whether OAuth or token exchange is required before comment access.
- Rate limits, data retention requirements, audit requirements, and allowed storage duration.

Required future credentials:

- `XIAOHONGSHU_CLIENT_ID` or official app-key.
- `XIAOHONGSHU_CLIENT_SECRET` or official app-secret.
- `XIAOHONGSHU_ACCESS_TOKEN` if applicable.

Future data target:

- Note/post metadata if officially available.
- Comment list if officially available.
- Reply list if officially available.

Minimum integration gate before code can make real calls:

1. Confirm that an official note/content/comment API is available for the user's developer account.
2. Confirm whether the API permits reading public comments or only own-account/merchant/Ark content.
3. Map official app-key/app-secret terminology to Sentigraph env placeholders.
4. Add response fixtures based on approved official payloads.
5. Implement a reviewed API client behind explicit config gates.

## Explicit Non-Goals

- No page scraping.
- No login bypass.
- No captcha bypass.
- No anti-bot evasion.
- No browser cookies.
- No proxy rotation.
- No private data collection.
- No real API calls before explicit credential, scope, and compliance approval.
