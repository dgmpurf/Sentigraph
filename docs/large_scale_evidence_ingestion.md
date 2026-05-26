# Large-Scale Evidence Ingestion Roadmap

Last updated: 2026-05-26

Sentigraph now has a source-neutral Evidence Layer, CSV/Excel import, Manual URL Evidence, trust/provenance, deduplication, human review, and audit timeline controls. The next scale step is batch-oriented ingestion and coverage reporting without adding non-compliant crawlers or overclaiming full-platform capture.

## What Scale Means

All-web public-opinion monitoring cannot be solved by a single crawler. Evidence can arrive through official APIs, OAuth-authorized account data, reviewed public parsers, search/RSS discovery metadata, user-uploaded datasets, manual URL/text evidence, or licensed vendors.

Three different scopes must stay separate:

- Single-source full capture: complete evidence for one approved source or account scope. This requires official access, user authorization, a vendor contract, or a reviewed parser that is allowed for that source.
- Event-scope large sample: a bounded sample for one event or keyword across available sources. This is the realistic near-term Sentigraph target.
- Platform-wide full capture: broad platform-level collection. This requires official platform access, user-provided lawful data, or data vendors. Sentigraph should not imply it has this today.

Sentigraph intentionally avoids scraping bypass, login-cookie crawling, captcha bypass, proxy evasion, anti-bot bypass, private data collection, and MediaCrawler integration as a core source.

## Acquisition Tiers

| Tier | Mode | Example | Current use |
| --- | --- | --- | --- |
| Tier 1 | Official API public data | YouTube Data API public video/comment data | Real-capable when locally configured, mocked in tests |
| Tier 2 | Official OAuth authorized data | Douyin/Bilibili after scopes and tokens are approved | Future pending console verification |
| Tier 3 | Reviewed public parser | Allowed public article pages after parser review | Fixture-first / planning |
| Tier 4 | Search discovery / RSS / GDELT / Common Crawl planning | URL/title/snippet discovery, RSS items, news discovery metadata | Static/mock only, including `rss_mock` and `gdelt_mock` fixture providers |
| Tier 5 | User-uploaded CSV/Excel/JSON | Lawful exported comments/articles/videos | Implemented for CSV/XLSX; JSON future |
| Tier 6 | Data vendor integration | Contracted datasets | Future |

## Scale Targets

- MVP: hundreds to thousands of evidence items per case using local JSON and deterministic summaries.
- V1: tens of thousands of items per case with chunked import, stricter idempotency, and stronger UI progress states.
- V2: hundreds of thousands per event with batch jobs, durable storage, worker queues, and coverage dashboards.
- Later: vendor-backed or official-platform large-scale ingestion with explicit quotas, terms, audit logs, and operational controls.

## Batch Principles

- Async/job-shaped ingestion even when the current MVP records only local completed jobs.
- Chunked upload for larger files in future.
- Row-level validation with warnings instead of hard crashes.
- Deterministic deduplication and idempotent commit.
- Resumable import once a worker/storage backend exists.
- Safe progress and error reporting with no raw secret persistence.
- Source coverage reporting that says what is available/imported, not what exists on the whole platform.
- Trust/dedup/review/audit integration for low-trust, duplicated, screenshot/transcribed, missing-source, or user-attested evidence.
- Rejected evidence excluded from default analysis, weak/unverified evidence flagged, and duplicate submissions collapsed by default.

## Current Scaffold

The current MVP adds lightweight local job and coverage summaries:

- `EvidenceIngestionJob`
- `EvidenceIngestionProgress`
- `EvidenceBatchSummary`
- `EvidenceCoverageSummary`
- `EvidenceSourceCoverage`

Read-only endpoints:

```http
GET /api/v1/cases/{case_id}/evidence/summary
GET /api/v1/cases/{case_id}/evidence/jobs
GET /api/v1/cases/{case_id}/evidence/coverage
```

CSV/XLSX import commit records a completed local job. Manual evidence attach records a lightweight manual job. Preview remains stateless. No raw file is persisted by default.

The Cases page shows:

- total and unique evidence counts
- duplicate count
- source/type/acquisition/trust/review distributions
- latest ingestion jobs
- source coverage and time range
- coverage limitation warning

## Coverage Boundary

The coverage note must remain visible:

```text
This is coverage of imported/available evidence, not full platform coverage.
```

The Chinese UI note says:

```text
当前覆盖范围仅代表已导入/可用证据，不代表全平台全量覆盖。
```

This prevents demos from implying that Sentigraph has complete all-web or platform-wide capture. Current summaries describe only what is already attached, imported, or normalized for the case.

## Future Work

- Chunked CSV/Excel/JSON upload.
- Resumable import sessions.
- Durable worker queue and storage backend for tens of thousands of rows.
- Search Discovery candidate review UI, still no automatic fetching.
- RSS/GDELT/news discovery research; current `rss_mock` and `gdelt_mock` providers are fixture-only UX scaffolds.
- Vendor dataset contract model.
- Official Douyin/Bilibili real modes only after OAuth/scope/item-id/permission gates are verified.
- Quota/rate-limit dashboards for real official APIs.

## Safety Boundaries

- No real APIs are called in automated tests.
- No URL fetching or website scraping is implemented by this scaffold.
- No cookies, login bypass, captcha bypass, proxy evasion, anti-bot bypass, or private data collection.
- No MediaCrawler core integration.
- No real LLM calls or real AI authenticity review.
- No credentials, tokens, cookies, or `.env` values are stored or exposed.
- No full-platform coverage, guaranteed prediction, automatic content moderation, real-world action execution, or individual targeting claims.
