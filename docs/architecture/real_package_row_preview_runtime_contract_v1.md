# Real Package Row Preview Runtime Contract v1

Status: future runtime contract draft

Scope: future Phase 6N/6O real package row preview output object

This document is design-only. It does not implement runtime code, row reading, row parsing, evidence import, Evidence Layer writes, production case creation, review queue creation, dedup, analysis, Sandbox fixture generation, public event page generation, B-end report generation, provider execution, collector jobs, real API calls, URL fetching, scraping, browser automation, MediaCrawler integration, OpenClaw production ingestion, official API providers, vendor API providers, or real LLM integration.

## 1. Contract Purpose

This contract defines the shape and boundaries for a future append-only real package row preview result.

The object is for reviewer safety inspection only. It must never authorize import, write Evidence Layer records, create production cases, create review queues, run dedup, run analysis, generate Sandbox fixtures, generate public event pages, or generate reports.

## 2. Suggested Object Shape

```json
{
  "schema": "sentigraph_real_package_row_preview_v1",
  "preview_run_id": "...",
  "preflight_id": "...",
  "import_job_id": "...",
  "request_id": "...",
  "created_at": "...",
  "created_by": "...",
  "execution_mode": "real_package_row_preview_only",
  "status": "passed|warn|blocked|privacy_stop",
  "package_reference": {
    "package_name": "...",
    "package_role": "...",
    "package_path": "...",
    "package_hash": "...",
    "manifest_hash": "..."
  },
  "limits": {
    "max_rows": 10,
    "full_scan": false,
    "import_rows": false,
    "analysis": false,
    "report": false
  },
  "rows": {
    "rows_seen": 0,
    "accepted_for_preview": 0,
    "quarantined": 0,
    "rejected": 0,
    "privacy_stop_at_row": null
  },
  "redacted_preview_rows": [],
  "quarantine_summary": [],
  "rejection_summary": [],
  "privacy_scan": {
    "raw_author_id_detected": 0,
    "raw_author_name_detected": 0,
    "profile_url_detected": 0,
    "private_message_detected": 0,
    "secret_like_value_detected": 0,
    "privacy_stop_triggered": false
  },
  "governance_defaults": {
    "review_status": "review_needed",
    "verification_status": "source_url_provided_unverified",
    "trust_label": "medium_low",
    "analysis_included": false
  },
  "now_flags": {
    "import_evidence_rows_now": false,
    "write_evidence_layer_now": false,
    "create_case_now": false,
    "create_review_queue_now": false,
    "run_dedup_now": false,
    "run_analysis_now": false,
    "generate_sandbox_now": false,
    "generate_report_now": false
  },
  "readiness": {
    "state": "ready_for_future_staging_import_design|blocked|privacy_stop",
    "can_import_now": false,
    "requires_future_phase": true
  },
  "boundary_notes": [],
  "recommended_next_steps": []
}
```

## 3. Required Invariants

The object must always satisfy:

- `schema=sentigraph_real_package_row_preview_v1`.
- `execution_mode=real_package_row_preview_only`.
- `limits.full_scan=false`.
- `limits.import_rows=false`.
- `limits.analysis=false`.
- `limits.report=false`.
- `limits.max_rows <= 20`.
- all `now_flags` are false.
- `readiness.can_import_now=false`.
- `readiness.requires_future_phase=true`.
- `governance_defaults.analysis_included=false`.
- preview result is append-only.
- preview result does not authorize import.
- future staging import still needs a separate design and decision.

## 4. Forbidden Values

The object must never include raw forbidden values:

- raw author id,
- raw author name,
- profile URL,
- avatar URL,
- private message,
- cookie,
- token,
- session,
- browser profile path,
- password,
- email address if detected,
- phone number if detected,
- precise personal address,
- minors' personal details,
- direct personal identifiers,
- full raw row.

Field names may appear as blocker categories or privacy scan counters. Values must not appear.

## 5. Package Reference Rules

`package_reference` may include safe identifiers:

- package name,
- package role,
- local package path if not secret and if already approved,
- package hash,
- manifest hash.

The package reference must not include:

- live account path,
- browser profile path,
- credential path,
- cookie/session path,
- private collector runtime details beyond safe package identity,
- raw source rows.

## 6. Limits Rules

The runtime must set:

- default `max_rows=10`,
- hard maximum `max_rows=20`,
- `full_scan=false`,
- `import_rows=false`,
- `analysis=false`,
- `report=false`.

The runtime must not scan the whole package to compute totals or summaries. Counts must describe only rows seen during the capped preview.

## 7. Status Rules

Allowed statuses:

- `passed`: preview completed within limits and no blockers.
- `warn`: preview completed but quarantine/rejection/coverage warnings exist.
- `blocked`: preview did not run because a gate failed.
- `privacy_stop`: preview stopped immediately due to privacy/security violation.

`privacy_stop` must block future import until privacy/security review.

## 8. Redacted Preview Rows

`redacted_preview_rows` may include only safe fields defined in the redaction policy:

- row index,
- evidence type,
- platform,
- safe source URL,
- title preview,
- body text preview,
- created time,
- language,
- non-sensitive counts,
- governance defaults,
- privacy check category.

It must not contain raw forbidden values.

## 9. Quarantine and Rejection Summaries

Quarantine summary may include:

- row index,
- reason code,
- forbidden field names,
- safe category.

Rejection summary may include:

- row index,
- reason code,
- parser category,
- safe explanation.

Neither summary may include raw row text or forbidden values.

## 10. Privacy Scan

Privacy scan counters may record detections:

- `raw_author_id_detected`,
- `raw_author_name_detected`,
- `profile_url_detected`,
- `private_message_detected`,
- `secret_like_value_detected`,
- `privacy_stop_triggered`.

Counters are safe because they do not expose the values.

## 11. Boundary Notes

Every preview result should include notes such as:

- Preview rows were not imported.
- Preview rows are not representative.
- Preview rows do not prove full coverage.
- Preview rows are redacted.
- Preview rows are for reviewer safety inspection only.
- Provider output is evidence, not truth.
- Future staging import requires a separate phase.

## 12. Storage Rule

Future preview results should be stored append-only, for example:

- `runtime/analysis_requests/real_package_row_previews/`

The runtime must not overwrite prior preview results. It must not delete prior preview results as part of creation.

Runtime files remain ignored and should not be committed.

## 13. Future Endpoint Guidance

Potential future endpoint group:

- `GET /api/v1/analysis-requests/real-package-row-previews`
- `GET /api/v1/analysis-requests/{request_id}/real-package-row-previews`
- `POST /api/v1/analysis-requests/{request_id}/real-package-row-previews`
- `GET /api/v1/analysis-requests/{request_id}/real-package-row-previews/{preview_run_id}`

The POST endpoint must require explicit human row preview approval and must remain preview-only.

## 14. Future Phase Boundary

This contract supports a future limited runtime only.

It does not authorize:

- staging import,
- Evidence Layer writes,
- review queue creation,
- dedup,
- analysis,
- Sandbox generation,
- public event generation,
- report generation.

Those must remain separate phases with separate human decisions.
