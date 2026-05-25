# CSV / Excel Evidence Import Guide

Status: implemented for local/offline evidence normalization.

This feature lets a user upload a lawful CSV or Excel dataset and map rows into Sentigraph `EvidenceItem` records. It is designed for all-web public-opinion monitoring when platform APIs are unavailable, pending, or intentionally not used.

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
- Secret-like columns and values are redacted or omitted, including `api_key`, `access_token`, `refresh_token`, `client_secret`, `password`, and `cookie`.
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
