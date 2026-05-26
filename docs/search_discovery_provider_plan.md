# Search Discovery Provider Plan

Last updated: 2026-05-26

Status: mock/static provider taxonomy implemented. RSS and GDELT are fixture providers only. No live search, RSS, GDELT, website, platform, or LLM API is called.

## Provider Taxonomy

| Provider type | Current status | Live fetch | Requires key | Returns | Next action |
| --- | --- | --- | --- | --- | --- |
| `mock_static` | `mock_only` | false | false | URL/title/snippet metadata from local fixtures | Use for Search Discovery UI demos and regression tests. |
| `rss_mock` | `mock_only` | false | false | RSS-style URL/title/snippet metadata from local fixtures | Review source-specific feed terms before any future live RSS pilot. |
| `gdelt_mock` | `mock_only` | false | false | GDELT/news-style URL/title/snippet metadata from local fixtures | Research GDELT/news API terms and quota before a real adapter. |
| `search_api_future` | `future_real_provider` | false | true | Planned URL/title/snippet metadata only | Choose an approved provider and add mocked contract fixtures before real calls. |
| `user_url_list` | `planned` | false | false | User-provided URL/title/snippet metadata | Route through Manual URL Evidence or CSV/Excel import. |
| `data_vendor_future` | `future_real_provider` | false | true | Licensed vendor metadata only | Wait for a vendor contract and mocked fixtures. |

## Safety Boundaries

- RSS/GDELT providers are currently static local fixtures.
- Candidate URLs are never fetched.
- RSS feeds are not polled.
- GDELT APIs are not called.
- Search engine APIs are not called.
- Candidate snippets are metadata leads, not full source content.
- Full content extraction requires an official API route, a reviewed public parser, licensed vendor data, or user-provided text.
- Accepted candidates remain unverified and review-needed until a human reviews them.
- MediaCrawler is not integrated.
- No cookies, login bypass, captcha bypass, anti-bot bypass, private data collection, real LLM calls, or secret exposure is allowed.

## API Surface

```http
GET /api/v1/search-discovery/status
GET /api/v1/search-discovery/providers
GET /api/v1/search-discovery/mock-candidates?query=Tesla
GET /api/v1/search-discovery/mock-candidates?query=Tesla&provider=rss_mock
GET /api/v1/search-discovery/mock-candidates?query=Tesla&provider=gdelt_mock
POST /api/v1/cases/{case_id}/search-discovery/candidates/attach
```

The no-provider candidate endpoint defaults to `provider=mock_static`.

## Future Real Provider Path

Any future RSS, GDELT, search API, or vendor adapter should start with mocked contract fixtures, no-network tests, quota/terms review, credential-present booleans only, and human review before attach. Real providers should still return URL/title/snippet metadata first; automatic page fetching and full-content extraction remain separate reviewed work.
