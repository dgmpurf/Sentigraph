# Universal Evidence Ingestion Layer

Status: implemented as a thin normalization layer for local/offline analysis.

The Universal Evidence Ingestion Layer generalizes Sentigraph from platform-specific crawl outputs into event-centered evidence records. It does not fetch data by itself. It normalizes already available public or user-provided inputs so the case pipeline can support all-web public-opinion monitoring over official APIs, authorized OAuth sources, public-parser fixtures, search-discovery outputs, user uploads, data vendors, and mock fixtures.

## Safety Boundary

- No real platform API call is made by evidence attachment.
- No real Douyin or Bilibili API call is made.
- No scraping bypass, login bypass, captcha bypass, anti-bot evasion, browser-cookie use, or private-data access is implemented.
- No real LLM API call is made.
- Secrets are removed from `raw_data_safe`; API keys, tokens, cookies, authorization headers, passwords, client secrets, and `.env` values must not be stored or returned.
- Evidence remains case-level and aggregate-analysis-oriented. It must not create named-user targeting, account-level influenceability scores, or manipulation guidance.

## Core Schemas

Implemented in `backend/app/schemas/evidence.py`:

- `EvidenceItem`
- `EvidenceSource`
- `EvidenceType`
- `EvidenceIngestionBatch`
- `EvidenceIngestionResult`
- `EvidenceNormalizationMetadata`

`EvidenceItem` supports:

- identifiers: `evidence_id`, `case_id`, `parent_id`, `root_id`
- source metadata: `platform`, `source_type`, `acquisition_mode`, `access_scope`, `content_visibility`
- content: `title`, `body_text`, `comment_text`
- public author/source labels: `author_id`, `author_name`, `url`, `created_at`
- interaction metrics: `like_count`, `reply_count`, `share_count`, `view_count`
- safe raw metadata: `raw_data_safe`
- normalization metadata: `language`, `confidence`, `ingestion_metadata`
- trust/provenance metadata: `provenance_type`, `verification_status`, `trust_score`, `trust_label`, `source_url_present`, `source_url`, `source_platform_claim`, `source_capture_method`, `submitted_at`, `user_attestation_required`, `user_attestation_text`, `verification_notes`, and `risk_flags`
- deduplication metadata: `content_hash`, `normalized_content_hash`, `canonical_url_hash`, `duplicate_group_id`, `duplicate_count`, and `duplicate_group_size`

## Enumerations

`acquisition_mode`:

- `official_api_public`
- `official_api_oauth`
- `public_parser`
- `search_discovery`
- `user_upload`
- `manual_url`
- `data_vendor`
- `mock_fixture`

`source_type`:

- `youtube`
- `douyin`
- `bilibili`
- `weibo`
- `xiaohongshu`
- `reddit`
- `news_site`
- `forum`
- `public_web`
- `uploaded_dataset`
- `mock`

`evidence_type`:

- `video`
- `article`
- `post`
- `comment`
- `reply`
- `title`
- `body_text`
- `metadata`
- `interaction_metric`
- `interaction_metrics` (legacy alias kept for backward compatibility)
- `search_result`
- `uploaded_record`

## Converters

Implemented in `backend/app/services/evidence_ingestion.py`:

- YouTube `RawPost` / `RawComment` to `EvidenceItem`
- Public parser article/forum `RawPost` / `RawComment` to `EvidenceItem`
- Manual/user-upload payload to sanitized `EvidenceItem`
- `EvidenceItem` back to analysis-compatible `RawPost` / `RawComment`

Planned evidence sources include manual URL evidence, uploaded CSV/Excel/JSON records, RSS/search-discovery records, and future data-vendor payloads. These should normalize to the same `EvidenceItem` shape before any downstream analysis.

The case-specific crawl endpoint still preserves `raw_posts` and `raw_comments` for backward compatibility. It also stores normalized `evidence_items` so future source types can share one evidence surface.

Search Discovery is a lead-generation layer, not an evidence collector. `SearchDiscoveryCandidate` records contain URL/title/snippet metadata with `acquisition_mode=search_discovery` and `status=pending_review`. They become `EvidenceItem` records only after user review and one of these routes:

- Manual URL Evidence with user-provided title/body/comment text.
- CSV/Excel import with user-provided rows.
- A separately reviewed public parser path that explicitly allows fetching for that source.

The current Search Discovery endpoints are static/mock only and do not fetch URLs.

## Trust, Provenance, And Deduplication

Evidence is conservatively labeled before it enters analysis:

- Official API evidence is high trust for source provenance and `verified_by_official_api`.
- Public-parser evidence is medium/high trust when a parser path is reviewed.
- Manual URL evidence is `source_url_provided_unverified` when a source URL exists, and still requires human review.
- CSV/Excel evidence is user-uploaded and needs source/attestation review.
- Screenshot/transcribed evidence is always `screenshot_unverified`.
- Search Discovery candidates stay pending-review leads until accepted through a safe evidence path.

Within each case, Sentigraph computes deterministic content and URL hashes, removes common tracking URL parameters, collapses exact duplicate text/URL submissions, and preserves `duplicate_count` as a repetition signal. Analysis uses unique evidence by default so repeated malicious or accidental uploads do not directly inflate sentiment, topic, or risk counts.

## Case Pipeline Priority

`POST /api/v1/cases/{case_id}/run` uses:

1. Attached `raw_comments` when present, preserving the existing YouTube `analysis_input_source=case_raw_data` flow.
2. Attached `evidence_items` when no raw comments exist, using `analysis_input_source=case_evidence_items`.
3. The existing mock dataset when neither raw comments nor evidence items exist, using `analysis_input_source=mock_data_fallback`.

This preserves the current YouTube real-data demo while enabling manual article/video/comment evidence to feed the deterministic offline analysis path.

## API Surface

- `GET /api/v1/cases/{case_id}/evidence`
- `POST /api/v1/cases/{case_id}/evidence/attach`
- `GET /api/v1/cases/{case_id}/evidence/trust-summary`
- `GET /api/v1/cases/{case_id}/evidence/dedup-summary`
- `POST /api/v1/cases/{case_id}/evidence/import/preview`
- `POST /api/v1/cases/{case_id}/evidence/import/commit`

The attach endpoint accepts safe manual evidence payloads such as article title/body, video title/description, comments, and replies. It does not accept or expose credentials.

The CSV / Excel import endpoints add a user-upload path for evidence datasets when official APIs are unavailable or pending. The frontend reads the selected CSV/XLSX file locally and sends base64 bytes to the backend for in-memory parsing. Preview returns detected columns, inferred mapping, normalized row samples, duplicates, skipped-row counts, and validation warnings. Commit stores only normalized `EvidenceItem` records on the case; uploaded raw files are not persisted by default.

Import safety rules:

- Supported formats: CSV, UTF-8/UTF-8-BOM CSV, GB18030/GBK CSV fallback, and macro-free `.xlsx`.
- Unsupported formats: `.xls`, `.xlsm`, `.xlsb`, unknown binaries, macros, executable content, external crawler exports without lawful-source attestation, and oversized files.
- Formulas are not executed; formula-like cells are treated as plain text.
- Secret-like columns or values such as API keys, access tokens, refresh tokens, client secrets, passwords, and cookies are redacted or omitted.
- Duplicate rows are deduped by deterministic content hash.
- Default import metadata is `source_type=uploaded_dataset` and `acquisition_mode=user_upload`.

## Frontend Surface

The Cases and Analysis Result pages now display a small Evidence summary:

- source distribution
- evidence type counts
- top titles
- representative public text
- acquisition mode/source labels through normalized evidence records

The UI avoids rendering raw objects and does not expose secrets or `.env` values.

## All-Web Monitoring Implication

The evidence layer gives Sentigraph a source-neutral ingestion contract. Future official APIs, OAuth-authorized account data, public parser outputs, CSV/Excel uploads, search-discovery records, and vendor data can all be normalized into the same event evidence model before analysis. This keeps platform-specific collection logic separate from the downstream sentiment, risk, report, monitoring, forecast, and Simulation Lab systems.

See `docs/source_feasibility_matrix.md` for the green/yellow/red acquisition matrix. That matrix explicitly keeps MediaCrawler out of the core product and treats third-party crawler exports only as user-provided datasets with lawful-source attestation.
