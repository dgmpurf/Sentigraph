# Sentigraph API Application Plan

Last updated: 2026-05-17

## Purpose

This plan lists the external platform application state and the exact information needed before any real-mode implementation. It does not authorize real API calls. It is a checklist for console verification, screenshots, permission review, and fixture preparation.

## Current Platform Status

| Platform | Current Status | Real Mode Decision |
| --- | --- | --- |
| Douyin | Developer access obtained; comment permission unknown | Blocked until comment scope and payloads are verified |
| Xiaohongshu | Developer access obtained; note/comment API availability unknown | Blocked until official note/comment capability is verified |
| Reddit | API approval pending | Blocked until approval is granted |
| Weibo | Company-age requirement blocks current application | Blocked until application eligibility is resolved |
| Bilibili | Pending | Apply later |
| Kuaishou | Not applied yet | Later |
| Zhihu | Not applied yet | Later |
| Douban | Not applied yet | Later |
| Toutiao | Not applied yet | Later |

## Universal Requirements Before Real Mode

For every platform, collect these before implementation:

- Developer console product name.
- App id/client id/client key naming.
- Secret naming, without storing values in docs or git.
- Required scopes/permissions.
- Whether comments are available.
- Whether replies are available.
- Whether access is public, own-account only, merchant-only, creator-only, or requires user OAuth.
- Endpoint names and official documentation links.
- Rate limits and quota limits.
- Data retention and storage restrictions.
- Moderation/compliance obligations.
- Screenshots proving approval status and scope availability.
- Sanitized sample payloads or mocked fixtures based on official payload shape.

## Douyin

Current status:

- Developer access obtained by user.
- Comment API permission is unknown.
- Local adapter remains mock-only.

Console checks needed:

- Is interaction/comment management enabled for the app?
- Is `item.comment` or a current equivalent comment-list permission available and approved?
- Is keyword video comment management available and applicable?
- Are comment replies available through an official API?
- Does access require user authorization?
- Is access limited to authorized users' own videos/items?
- What are the rate limits and review requirements?

Screenshots/records needed:

- App overview showing developer access and app status.
- Permission/scope page showing comment permission status.
- Any `item.comment` or equivalent scope approval state.
- Product page for keyword video comment management if available.
- OAuth/token flow page if user authorization is required.
- Rate-limit/quota page.

Credentials needed later:

- `DOUYIN_CLIENT_KEY`
- `DOUYIN_CLIENT_SECRET`
- `DOUYIN_ACCESS_TOKEN`

Implementation gate:

- Do not implement real Douyin mode until comment permission and official payload shapes are confirmed.

## Xiaohongshu

Current status:

- Developer access obtained by user.
- Exact API product/scope is unknown.
- Publicly visible official materials may be commerce/Ark oriented.
- Local adapter remains mock-only.

Console checks needed:

- Is there an official note/content data API for the user's app type?
- Is there an official comment or interaction API?
- Are comments available for public notes, own account notes, merchant content, Ark/ad content, or approved creators only?
- Are replies available?
- Are credentials named app-key/app-secret or client ID/client secret?
- Is OAuth/token exchange required?
- Are public opinion analysis use cases allowed by product terms?
- What are rate limits, storage limits, and audit obligations?

Screenshots/records needed:

- App overview showing developer access and app/product type.
- API product list showing available note/content/comment/interaction products.
- Scope/permission page showing comment API availability or absence.
- Credential naming page, with values redacted.
- Rate-limit/quota page.
- Product terms or usage restrictions relevant to comment data.

Credentials needed later:

- `XIAOHONGSHU_CLIENT_ID` or app-key.
- `XIAOHONGSHU_CLIENT_SECRET` or app-secret.
- `XIAOHONGSHU_ACCESS_TOKEN` if applicable.

Implementation gate:

- Do not implement real Xiaohongshu mode until an official note/comment API is confirmed and access limits are understood.

## Reddit

Current status:

- API approval pending.
- Mock mode is available.
- Scraping must not be used to bypass approval.

Checks needed:

- Confirm app approval status.
- Confirm allowed use case and rate limits.
- Confirm credentials outside the repository:
  - `REDDIT_CLIENT_ID`
  - `REDDIT_CLIENT_SECRET`
  - `REDDIT_USER_AGENT`
- Confirm PRAW-based implementation remains acceptable.

Implementation gate:

- Do not enable Reddit real mode until approval is granted.

## Weibo

Current status:

- Application is currently blocked by a company-age requirement.
- Mock adapter scaffold exists.

Checks needed:

- Confirm company eligibility requirement and date when eligible.
- Confirm comment/read permissions needed for public-opinion use.
- Confirm whether access is public-search capable or account-owned only.
- Capture screenshots of eligibility block and required materials.

Implementation gate:

- Do not implement real Weibo mode until application eligibility and relevant permissions are approved.

## Bilibili

Current status:

- Pending.
- Mock adapter scaffold exists.

Checks needed:

- Confirm official API product for video metadata and comments.
- Confirm required scopes and whether public video comments are available.
- Confirm owner/user authorization limits.
- Capture app status, permission list, and rate limits.

Implementation gate:

- Apply later after Douyin/Xiaohongshu/Reddit priorities are clarified.

## Other Platforms

Kuaishou, Zhihu, Douban, and Toutiao are not applied yet. They should remain mock-only until there is a specific business need, official application path, and permission review.

For each, collect:

- Official developer program URL.
- Application eligibility.
- Comment API availability.
- Public vs own-account access limits.
- Credentials and scopes.
- Rate limits.
- Approved payload fixtures.

## Real-Mode Implementation Sequence

1. Confirm permission and scope in the platform console.
2. Add sanitized official payload fixtures.
3. Add mocked HTTP client tests.
4. Add timeout, retry, rate-limit, and redacted diagnostics.
5. Keep real mode opt-in and disabled by default.
6. Run backend tests and offline benchmarks.
7. Only then allow a tiny controlled live smoke test.
