# Source Catalog

Last updated: 2026-05-25

Sentigraph's source catalog describes possible public-opinion evidence sources
without enabling collection by itself. It is a planning and readiness layer for
all-web monitoring: every source must produce event-centered `EvidenceItem`
records before downstream sentiment, topic risk, report, monitoring, forecasting,
and Simulation Lab workflows consume it.

The catalog is static metadata. It does not call real APIs, fetch URLs, use
cookies, run crawlers, call LLMs, or read credentials.

## Universal Rules

- Default mode remains mock/offline unless a source-specific official path is
  explicitly implemented and configured.
- No login-cookie crawling.
- No captcha bypass.
- No proxy evasion.
- No anti-bot bypass.
- No hidden/private data collection.
- No real LLM calls for ingestion.
- User-provided datasets are allowed only when the user attests that the source
  and collection method are lawful.
- MediaCrawler is not integrated as a core data source. Third-party crawler
  exports may only enter Sentigraph as user-provided uploaded datasets with
  lawful-source attestation and secret/private-data screening.

## API Surface

```http
GET /api/v1/sources/catalog
```

The endpoint returns static source categories and per-source readiness metadata:

- `acquisition_modes`
- `allowed_data_types`
- `forbidden_data_types`
- `current_status`
- `compliance_notes`
- `next_action`
- `priority`
- `feasibility_status`

No secret values are returned. The response is static metadata only.

## Categories

### Video Platforms

Examples:

- YouTube
- Douyin
- Bilibili
- Kuaishou
- TikTok

Allowed acquisition modes:

- `official_api_public`
- `official_api_oauth`
- `user_upload`
- `data_vendor`
- `mock_fixture`

Allowed data types:

- `video`
- `title`
- `body_text`
- `comment`
- `reply`
- `interaction_metric`

Forbidden data types:

- private messages
- hidden account data
- cookie/session data
- login-only comments
- captcha/anti-bot bypass output

Current Sentigraph status:

- YouTube is green/real-capable when local real mode and key are configured.
- Douyin is yellow: Web App OAuth and `item.comment` are pending.
- Bilibili is yellow: official permission is pending.
- Kuaishou is red for direct crawling; official permission or user-provided data
  is required.
- TikTok is future official/vendor/user-upload only.

Next action:

- Keep YouTube tiny and cached.
- Verify Douyin and Bilibili official scopes before any real call.

Priority:

- High for YouTube, Douyin, and Bilibili.
- Medium/low for other video platforms until credentials and scope are clear.

### News / Media Sites

Examples:

- The Paper
- Jiemian
- 36Kr
- Huxiu
- Sina
- NetEase
- Tencent News
- Xinhua
- People
- Reuters
- BBC
- The Guardian

Allowed acquisition modes:

- `public_parser`
- `manual_url`
- `search_discovery`
- `user_upload`
- `data_vendor`
- `mock_fixture`

Allowed data types:

- `article`
- `title`
- `body_text`
- `search_result`
- `interaction_metric` when public metrics are available

Forbidden data types:

- paywalled text without permission
- login-only comments
- private subscriber data
- broad bulk copying beyond permitted use

Current Sentigraph status:

- The Paper and Jiemian have fixture-first public parser scaffolds.
- Other media sources are catalog/planning entries.

Next action:

- Prefer RSS, official feeds, manual URLs, or reviewed parser fixtures.

Priority:

- Medium to high depending on the event domain.

### Forums / Communities

Examples:

- Hupu
- Tieba
- NGA
- V2EX
- Reddit

Allowed acquisition modes:

- `public_parser`
- `official_api_public`
- `manual_url`
- `user_upload`
- `mock_fixture`

Allowed data types:

- `post`
- `title`
- `body_text`
- `comment`
- `reply`
- `interaction_metric`

Forbidden data types:

- login-only forum pages
- cookies/session data
- anti-bot bypass output
- private user profiles or messages

Current Sentigraph status:

- Hupu, Tieba, NGA, and Maimai have fixture-only public parser scaffolds.
- Reddit is mock/selectable but real API approval is pending.
- V2EX is a future parser candidate.

Next action:

- Keep fixture-first coverage; do not use scraping as an API approval bypass.

Priority:

- High for current fixture parsers, medium for Reddit, low for future candidates.

### Q&A Sites

Examples:

- Zhihu
- Stack Exchange
- Quora

Allowed acquisition modes:

- `official_api_public`
- `official_api_oauth`
- `public_parser`
- `manual_url`
- `user_upload`
- `mock_fixture`

Allowed data types:

- `post`
- `article`
- `title`
- `body_text`
- `comment`
- `reply`

Forbidden data types:

- private accounts/messages
- login-only content
- hidden API payloads

Current Sentigraph status:

- Zhihu is mock/scaffold only.
- Stack Exchange and Quora are catalog-only future sources.

Next action:

- Research official API and terms before any real path.

Priority:

- Low/medium.

### Complaint / Review Sites

Examples:

- Black Cat Complaint
- App Store Reviews
- Google Play Reviews
- Steam Reviews
- Trustpilot

Allowed acquisition modes:

- `official_api_public`
- `public_parser`
- `manual_url`
- `user_upload`
- `data_vendor`
- `mock_fixture`

Allowed data types:

- `post`
- `comment`
- `reply`
- `title`
- `body_text`
- `interaction_metric`

Forbidden data types:

- private order details
- private support tickets
- reviewer identity enrichment
- login-only/private account data

Current Sentigraph status:

- Catalog/planning only.

Next action:

- Add source-specific import only with official/API/user-provided lawful data.

Priority:

- Medium.

### Finance / Investor Forums

Examples:

- Xueqiu
- Eastmoney Guba
- StockTwits

Allowed acquisition modes:

- `official_api_public`
- `public_parser`
- `manual_url`
- `user_upload`
- `data_vendor`
- `mock_fixture`

Allowed data types:

- `post`
- `comment`
- `reply`
- `title`
- `body_text`
- `interaction_metric`

Forbidden data types:

- private account data
- trading-advice profiles
- account-level influenceability scoring
- scraping bypass output

Current Sentigraph status:

- Catalog/planning only.

Next action:

- Review licensing, API access, and financial-data disclaimers before use.

Priority:

- Low/medium.

### Social Platforms

Examples:

- Weibo
- X/Twitter
- Bluesky
- Mastodon

Allowed acquisition modes:

- `official_api_public`
- `official_api_oauth`
- `manual_url`
- `user_upload`
- `data_vendor`
- `mock_fixture`

Allowed data types:

- `post`
- `comment`
- `reply`
- `title`
- `body_text`
- `interaction_metric`

Forbidden data types:

- private messages
- cookie/session data
- login bypass output
- captcha or anti-bot bypass output

Current Sentigraph status:

- Weibo is mock/scaffold with company-age requirement pending.
- X/Twitter, Bluesky, and Mastodon are catalog-only future sources.

Next action:

- Use official APIs or user-provided datasets only.

Priority:

- Medium for Weibo; low for others until approved.

### Search Discovery

Examples:

- GDELT
- Google Custom Search / Programmable Search
- approved data vendor discovery indexes

Allowed acquisition modes:

- `search_discovery`
- `data_vendor`
- `manual_url`
- `mock_fixture`

Allowed data types:

- `search_result`
- `title`
- `body_text`

Forbidden data types:

- SERP scraping without permission
- proxy evasion output
- captcha bypass output

Current Sentigraph status:

- Schema/catalog only. No connector implemented.

Next action:

- Design provider-specific connectors after terms and quota review.

Priority:

- Medium.

### RSS

Examples:

- Public RSS/Atom feeds from news, blogs, and official channels.

Allowed acquisition modes:

- `public_parser`
- `manual_url`
- `user_upload`
- `mock_fixture`

Allowed data types:

- `search_result`
- `article`
- `title`
- `body_text`

Forbidden data types:

- private feeds
- paywalled content
- subscriber-only metadata

Current Sentigraph status:

- Low-risk future source category; no connector yet.

Next action:

- Add fixture/import pilot if needed.

Priority:

- Medium.

### User-Uploaded Datasets

Examples:

- CSV upload
- Excel upload
- JSON upload

Allowed acquisition modes:

- `user_upload`
- `mock_fixture`

Allowed data types:

- `uploaded_record`
- `article`
- `post`
- `comment`
- `reply`
- `title`
- `body_text`
- `interaction_metric`

Forbidden data types:

- credential values
- private data without permission
- cookies or tokens

Current Sentigraph status:

- Manual evidence payload is implemented.
- CSV/Excel/JSON UI import remains future work.

Next action:

- Add upload parser after manual evidence attach is browser-smoke tested.

Priority:

- High.

### Manual URL Evidence

Examples:

- A user manually enters a public article URL plus title/body.
- A user manually enters a public video URL plus title/description.

Allowed acquisition modes:

- `manual_url`
- `user_upload`
- `mock_fixture`

Allowed data types:

- `article`
- `video`
- `post`
- `comment`
- `title`
- `body_text`

Forbidden data types:

- automatic fetch without review
- private/login-only content
- credential values

Current Sentigraph status:

- Manual evidence attach supports URL/title/body/comment fields.

Next action:

- Add a small UI form only if demos need it.

Priority:

- High.

### Data Vendor Future Integration

Examples:

- Licensed social listening vendors
- Licensed news/media datasets
- Licensed search/discovery indexes

Allowed acquisition modes:

- `data_vendor`
- `user_upload`
- `mock_fixture`

Allowed data types:

- `uploaded_record`
- `article`
- `post`
- `comment`
- `reply`
- `search_result`
- `interaction_metric`

Forbidden data types:

- unlicensed payloads
- credential values
- private data outside contract

Current Sentigraph status:

- Future planning only.

Next action:

- Add mocked fixtures first, then contract-specific adapter and retention rules.

Priority:

- Low until a vendor is selected.

## Relationship To Evidence Ingestion

All usable source records should become `EvidenceItem` records:

```text
source-specific record
  -> source catalog / feasibility check
  -> EvidenceItem normalization
  -> case evidence store
  -> deterministic offline analysis
  -> report / monitoring / forecast / Simulation Lab
```

See also:

- `docs/evidence_ingestion_design.md`
- `docs/source_feasibility_matrix.md`
- `docs/platform_sources.md`
