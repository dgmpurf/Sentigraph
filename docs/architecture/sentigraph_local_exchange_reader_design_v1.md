# Sentigraph Local Exchange Reader Design v1

Status: design for a future disabled-by-default metadata-only scaffold. This is not production ingestion.

## 1. Purpose

The Sentigraph local exchange reader is a future bridge for reading private collector provider result metadata after an explicit local-file handoff. It keeps Sentigraph and the private collector independent.

The reader is allowed to read metadata records only. It is not allowed to execute the collector, call HTTP/HTTPS, import evidence rows, create production cases, or generate analysis/report/Sandbox/public-event runtime artifacts.

## 2. Disabled-by-default configuration

The default configuration must be safe:

```json
{
  "exchange_enabled": false,
  "requestsDir": "",
  "resultsDir": "",
  "packageIndexPath": "",
  "packageRoot": "",
  "exchangeLogPath": "",
  "request_schema": "sentigraph_analysis_request_v1",
  "result_schema": "sentigraph_provider_job_result_v1",
  "contract_version": "1.0",
  "adapter_id": ""
}
```

Rules:

- `exchange_enabled=false` means no file reads.
- Paths must be configured explicitly.
- Runtime paths should remain under ignored runtime directories.
- Private collector paths must not be hardcoded.
- The scaffold should not read `.env`, tokens, cookies, sessions, browser profiles, or collector internals.

## 3. Reader responsibilities

The Sentigraph-side reader may:

- Read one configured provider result metadata JSON file.
- Validate `result_schema`, `contract_version`, `adapter_id`, `compatibility_status`, and `status`.
- Surface a safe metadata summary for a future governance UI.
- Preserve the boundary that provider output is evidence, not truth.

The reader must not:

- Execute collector jobs.
- Call HTTP or HTTPS.
- Import collector code.
- Read full package rows.
- Parse `evidence_items.jsonl` or `evidence_items.csv`.
- Write the production Evidence Layer.
- Create a production case, review queue, dedup run, analysis result, B-end report, Sandbox fixture, or public event page.

## 4. Accepted provider result statuses

Accepted status values are:

- `package_ready`
- `needs_manual_snapshot`
- `blocked`
- `invalid_schema`
- `unsupported_contract`
- `failed`
- `manual_review_required`

Runtime handling:

- `package_ready` and `needs_manual_snapshot` may be metadata-ready if the schema and compatibility checks pass.
- `blocked`, `failed`, `invalid_schema`, `unsupported_contract`, and `manual_review_required` must remain governance statuses only.
- Unknown statuses must be treated as safe manual review or blocked, never runnable.

## 5. Compatibility handling

Supported:

- `request_schema=sentigraph_analysis_request_v1`
- `result_schema=sentigraph_provider_job_result_v1`
- `contract_version=1.0`

Compatibility statuses:

- `compatible`: metadata may be read.
- `deprecated_compatible`: metadata may be read with warning in future UI.
- `unsupported_contract`: stop as unsupported.
- `invalid_schema`: stop as invalid.
- `manual_review_required`: stop as manual review.
- Unknown compatibility status: safe blocked/manual review.

If `adapter_id` is configured, metadata must match it or move to manual review. Empty adapter config means the reader can accept metadata from the configured result path without claiming production trust.

## 6. Safe package metadata fields

Provider result metadata may include:

- `package_id`
- `package_contract`
- `package_role`
- `package_index_ref`
- `package_root_ref`
- `package_relative_path`
- summary counts
- validation summary
- `coverage_note`
- `warnings`
- `errors`
- `nextAction`

This metadata is a pointer and summary only. It must not copy package evidence content.

## 7. Forbidden fields

Provider result metadata must not include:

- cookies
- tokens
- sessions
- browser profile paths
- raw author identifiers
- raw author names
- profile URLs
- private messages
- raw evidence rows
- evidence item content
- collector internals
- proxy, evasion, or bypass details

If forbidden fields are present, the reader returns `blocked`.

## 8. Future phase boundary

This phase adds a disabled scaffold only. Later phases may add:

- metadata status UI in AnalysisRequests
- review-ready case snapshot gate
- analysis_run gate
- Sandbox candidate gate
- B-end report candidate gate

Those remain future-gated. This reader does not make any package analysis-ready by itself.

## 9. Recommended scaffold behavior

A future backend scaffold should:

- Defaults to disabled.
- Does not read any file while disabled.
- Reads only a specific provider result metadata JSON file when enabled.
- Rejects forbidden fields.
- Rejects unknown schemas and contract versions.
- Moves unknown future platform metadata to manual review.
- Does not read package index or evidence item files yet.
- Not add any API route unless a later phase explicitly gates it.

This is intentionally smaller than a production integration.
