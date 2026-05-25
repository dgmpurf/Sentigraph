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
4. Click `上传 CSV / Excel`.
5. Confirm or adjust `字段映射`.
6. Click `预览导入结果`.
7. Review warnings, duplicates, and normalized rows.
8. Click `确认导入`.
9. Click `导入后运行分析`.

Expected success signs:

- `acquisition_mode=user_upload`
- `source_type=uploaded_dataset`
- `evidence_item_count` increases on the case
- `analysis_input_source=case_evidence_items` when the case has no attached raw comments
- `case_raw_data` still takes priority when raw comments exist

## API Flow

Preview:

```powershell
$bytes = [Convert]::ToBase64String([IO.File]::ReadAllBytes("sample_evidence_import.csv"))
$body = @{
  filename = "sample_evidence_import.csv"
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
