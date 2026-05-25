# CSV / Excel Evidence Import Guide

Status: implemented for local/offline evidence normalization.

This feature lets a user upload a lawful CSV or Excel dataset and map rows into Sentigraph `EvidenceItem` records. It is designed for all-web public-opinion monitoring when platform APIs are unavailable, pending, or intentionally not used.

Import commit now records a lightweight local `EvidenceIngestionJob` summary on the case. The job tracks total rows, accepted rows, rejected/skipped rows, duplicate rows, warning count, review-needed count, input type (`csv` / `xlsx`), source type, acquisition mode, and safe metadata. It is a local audit/progress record only: it does not persist the raw uploaded file, start a crawler, fetch URLs, call real APIs, or claim full-platform coverage.

## Manual URL / Manual Evidence

The Cases page also includes `手动添加证据` for one-off public evidence entry. This is for a user who already has lawful public material and wants to attach a single article, video, post, comment, reply, or interaction-metric record without preparing a spreadsheet.

Important boundary:

- Sentigraph does not fetch the URL.
- Sentigraph does not follow links.
- Sentigraph does not scrape the page.
- Sentigraph does not use cookies, login sessions, captcha handling, proxy evasion, or anti-bot bypasses.
- Sentigraph stores only normalized `EvidenceItem` records, not credentials, cookies, API keys, or raw secret values.

Recommended manual fields:

- `URL`: optional review context. It is stored as plain text and is never fetched.
- `平台`: a display/source label such as `manual_url`, `youtube`, `news_site`, or `public_web`.
- `来源类型`: usually `public_web`; use `news_site`, `forum`, `youtube`, or `uploaded_dataset` when that better describes the evidence.
- `证据类型`: `article`, `video`, `post`, `comment`, `reply`, or `interaction_metric`.
- `标题`, `正文 / 摘要`, `评论内容`: at least one of these text fields is required so the evidence is human-reviewable and analyzable.
- `作者`, `发布时间`, and metric fields: optional public context.
- `source_capture_method`: optional provenance context such as `manual_entry`, `manual_copy_from_public_page`, or `screenshot_transcription`.
- user attestation checkbox: confirms the user has the right to submit the public-opinion evidence for analysis. If missing, the item is still stored when allowed but marked `needs_review` / `user_attestation_missing`.

Manual URL evidence always uses `acquisition_mode=manual_url`. If a user accidentally pastes `api_key`, `access_token`, `refresh_token`, `client_secret`, `password`, or `cookie` style values into text fields, the backend redacts them before storage/output and returns a warning. Invalid numeric metrics are coerced to `0` with a warning instead of crashing.

Manual URL trust behavior:

- source URL + attestation: medium trust, `source_url_provided_unverified`
- no source URL: lower trust and `source_url_missing`
- screenshot transcription: always `screenshot_unverified`
- raw HTML/script-like text: stored as plain text and flagged, never executed
- duplicate text/URL: collapsed into a duplicate group with `duplicate_count`

Example article entry:

```text
URL: https://example.test/news/tesla-quality-update
平台: news_site
证据类型: article
标题: Tesla quality discussion
正文 / 摘要: A public article says users want a clearer repair timeline.
```

Example comment entry:

```text
URL: https://example.test/public-thread/1
平台: public_web
证据类型: comment
评论内容: 用户认为官方回应太慢，希望看到明确进展。
```

After clicking `添加到案例`, the UI shows evidence count, type/source distribution, `acquisition_mode=manual_url`, and the latest evidence preview. Click `添加后运行分析` to run the deterministic offline case analysis; when no attached raw comments exist, the case should report `analysis_input_source=case_evidence_items`.

## Accepted Formats

- `.csv`
- UTF-8 CSV
- UTF-8-BOM CSV
- GB18030 / GBK CSV fallback
- macro-free `.xlsx`

Unsupported:

- `.xls`
- `.xlsm`
- `.xlsb`
- macros
- executable content
- unknown binary files
- external links as active fetch instructions

Sentigraph does not execute formulas. Cells beginning with `=`, `+`, `-`, or `@` are treated as plain text.

## Download Template

The Cases page Evidence Import panel includes `下载 CSV 模板`. The same template is available from:

```http
GET /api/v1/evidence/import/template.csv
```

The response is a UTF-8 CSV attachment named `sentigraph_evidence_import_template.csv`. It contains the full recommended header and three safe sample rows:

- article evidence from a public news/media source
- video evidence from a public YouTube-style source
- comment evidence from a user-uploaded dataset

No credentials, cookies, API keys, tokens, or private data are included in the template. The template is a starting point only; users are still responsible for ensuring uploaded datasets come from lawful sources.

## Recommended Columns

Recommended CSV header:

```csv
platform,title,comment_text,author_name,url,created_at,like_count,reply_count
uploaded_dataset,Tesla delivery delay,用户说官方回应太慢 😟,用户A,https://example.test/post/1,2026-05-25T09:00:00Z,12,3
uploaded_dataset,Tesla quality discussion,The product quality concern needs a transparent update.,User B,https://example.test/post/2,2026-05-25T09:05:00Z,8,1
```

Supported mapping fields:

- `platform`
- `source_type`
- `acquisition_mode`
- `evidence_type`
- `title`
- `body_text`
- `comment_text`
- `parent_id`
- `root_id`
- `author_id`
- `author_name`
- `url`
- `created_at`
- `like_count`
- `reply_count`
- `share_count`
- `view_count`
- `language`
- `provenance_type`
- `verification_status`
- `source_capture_method`
- `user_attestation`

Column notes:

- `platform`: display/source label such as `youtube`, `news_site`, or `uploaded_dataset`.
- `source_type`: normalized source bucket such as `youtube`, `news_site`, `public_web`, or `uploaded_dataset`.
- `acquisition_mode`: usually `user_upload` for imported files.
- `evidence_type`: `article`, `video`, `post`, `comment`, `reply`, `title`, `body_text`, or `interaction_metric`.
- `title`, `body_text`, `comment_text`: public text that can be analyzed.
- `parent_id` and `root_id`: optional relationship IDs for replies, threads, videos, articles, or posts.
- `author_id` and `author_name`: optional public labels from the uploaded dataset.
- `url`: optional public source URL for review context; Sentigraph does not fetch it during import.
- metric columns: optional non-negative counts parsed safely.
- `language`: optional language hint such as `zh-CN` or `en-US`.
- `provenance_type`: optional value such as `user_upload`, `manual_url`, `screenshot_transcription`, or `data_vendor`.
- `verification_status`: optional initial status. Sentigraph may conservatively override it based on provenance and attestation.
- `source_capture_method`: optional capture label such as `csv_export`, `manual_entry`, or `screenshot_transcription`.
- `user_attestation`: optional boolean-like value (`true`, `yes`, `1`, `confirmed`) indicating lawful-source/right-to-submit attestation.

Defaults:

- `acquisition_mode=user_upload`
- `source_type=uploaded_dataset`
- `platform=uploaded_dataset`
- `evidence_type=comment` when `comment_text` is present
- `evidence_type=article` when `title` and `body_text` are present
- `evidence_type=video` when video-like fields or URLs are present
- `evidence_type=post` when only body text is present
- standalone metrics can use `interaction_metric`

## Safety and Privacy

- The uploaded raw file is not persisted by default.
- Only normalized `EvidenceItem` records and safe import metadata are stored.
- Case evidence summary endpoints can show the latest import job and coverage note: imported/available evidence is not full-platform or all-web coverage.
- Secret-like columns and values are redacted or omitted, including `api_key`, `access_token`, `refresh_token`, `client_secret`, `password`, and `cookie`.
- Screenshots and transcriptions are never automatically verified.
- Source URLs improve review context but do not guarantee truth.
- Duplicate rows/submissions are collapsed so repeated uploads do not directly inflate sentiment or risk counts.
- No crawler is started.
- MediaCrawler is not integrated.
- No login-cookie crawling, captcha bypass, proxy evasion, anti-bot bypass, or private-data collection is supported.
- No real platform API or real LLM API is called by import preview or commit.
- Users are responsible for ensuring uploaded datasets come from lawful sources and are appropriate for analysis.

## Local UI Flow

1. Open `Cases`.
2. Select or create a case.
3. Use `导入证据数据`.
4. Click `下载 CSV 模板` if you need a starter file.
5. Fill the template with lawful public/user-provided evidence.
6. Click `上传 CSV / Excel`.
7. Confirm or adjust `字段映射`.
8. Click `预览导入结果`.
9. Review warnings, duplicates, and normalized rows.
10. Click `确认导入`.
11. Click `导入后运行分析`.

Expected success signs:

- `acquisition_mode=user_upload`
- `source_type=uploaded_dataset`
- `evidence_item_count` increases on the case
- trust/provenance tags appear for imported/manual evidence
- duplicate submissions are shown as collapsed repetition signals
- `analysis_input_source=case_evidence_items` when the case has no attached raw comments
- `case_raw_data` still takes priority when raw comments exist

## API Flow

Preview:

```powershell
$template = "sentigraph_evidence_import_template.csv"
Invoke-WebRequest "http://127.0.0.1:8000/api/v1/evidence/import/template.csv" -OutFile $template
$bytes = [Convert]::ToBase64String([IO.File]::ReadAllBytes($template))
$body = @{
  filename = $template
  content_base64 = $bytes
} | ConvertTo-Json -Depth 8
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/api/v1/cases/case_001/evidence/import/preview" -ContentType "application/json" -Body $body
```

Commit:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/api/v1/cases/case_001/evidence/import/commit" -ContentType "application/json" -Body $body
```

Run analysis:

```powershell
Invoke-RestMethod -Method Post "http://127.0.0.1:8000/api/v1/cases/case_001/run"
```

## Analysis Path

Case run priority remains:

1. `case_raw_data` when attached raw comments exist.
2. `case_evidence_items` when imported/attached evidence exists and raw comments are absent.
3. `mock_data_fallback` when neither raw comments nor evidence exist.

Imported evidence feeds the same deterministic offline analysis, report, monitoring, forecast, and Simulation Lab initializer path as other normalized evidence. It is not a live crawler and not a prediction guarantee.
