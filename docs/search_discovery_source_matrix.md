# Search Discovery Source Matrix

Status: planning and static mock metadata only.

This matrix classifies discovery providers that could later help users find candidate public-opinion evidence URLs. It does not authorize crawling or content extraction. Candidate discovery returns URL/title/snippet metadata first; evidence use requires human review and a compliant attach/import/parser path.

When a candidate is later attached as evidence, Sentigraph keeps conservative trust/provenance metadata. URL/title/snippet discovery is not verification; user attestation, reviewed parser rules, official APIs, or vendor contracts are still needed before evidence can be treated as higher trust.

| Provider class | Allowed use | Forbidden use | Data returned | Full content? | API key? | User review? | Current Sentigraph status | Next action |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Search engine APIs | Approved API use after terms/quota review. | SERP scraping, captcha bypass, proxy evasion, hidden endpoints. | URL, title, snippet, source name, optional published time. | No, metadata/snippet only. | Usually yes. | Required. | Planned only; not configured. | Pick provider and add mocked fixtures before real calls. |
| News discovery APIs | Approved news/discovery APIs for article metadata. | Paywall bypass, full-content copying without license, website scraping. | URL, title, snippet, source, published time. | Usually no unless licensed. | Usually yes. | Required. | Research pending. | Review GDELT/news APIs and retention rules. |
| RSS feeds | Public RSS/Atom feeds when terms permit. | Private feeds, subscriber-only metadata, paywalled content extraction. | URL, title, summary/snippet, source, published time. | Sometimes feed summary only; full content requires source review. | Usually no. | Required. | Pilot candidate only. | Add fixture-first RSS pilot if needed. |
| Site-specific public search pages | Only after site-specific policy and parser review. | Dynamic SERP scraping, cookies, login/captcha/anti-bot bypass. | URL, title, public snippet if allowed. | No. | No, but review required. | Required. | Not implemented. | Keep out of live product until parser rules allow it. |
| User-provided URL lists | Users may paste/upload lawful public URLs and text. | Treating URL lists as permission to fetch or scrape automatically. | URL plus user-provided title/snippet/text. | Only if user provides text. | No. | Required. | Supported through Manual URL Evidence and CSV/Excel import. | Route accepted URLs to manual evidence/import. |
| Data vendors | Licensed discovery indexes after contract review. | Unlicensed payloads, credential-bearing exports, private data outside contract. | URL, title, snippet, source, published time, vendor metadata. | Only if licensed. | Usually yes. | Required. | Future only. | Wait for vendor and mocked contract fixtures. |
| Mock fixtures | Contract/UI testing with deterministic fake candidates. | Presenting mock candidates as real search results. | URL, title, snippet, source, published time. | No. | No. | Required. | Implemented static mock endpoint. | Use for planning and tests only. |

## Boundary Notes

- Search Discovery is green only for metadata discovery, mock fixtures, RSS metadata after review, and user-reviewed URL lists.
- Full content extraction requires one of:
  - official API permission
  - user-provided text
  - licensed data vendor payload
  - public parser review and fixture tests
- Search Discovery must not fetch candidate URLs by itself.
- MediaCrawler is not integrated and should not become a core source.
- No login-cookie crawling, captcha bypass, proxy evasion, anti-bot bypass, or private data collection is allowed.

## Current Mock Endpoint

```http
GET /api/v1/search-discovery/status
GET /api/v1/search-discovery/mock-candidates?query=Tesla
```

The mock candidate endpoint returns deterministic `example.test` URLs with `status=pending_review` and `acquisition_mode=search_discovery`. It is safe for UI planning and regression tests because it does not call any real provider or fetch any URL.
