# Sentigraph Analysis Request / Provider Handoff / Import Governance Status Source 11

Update date: 2026-06-18

Nature: Status patch Source. This document records Phase 6A-L implementation status and does not replace Source 00-10.

## One-Sentence Conclusion

Sentigraph has added a local file-based Analysis Request and Evidence Provider handoff subsystem that can create analysis requests, receive provider job results, generate case draft handoff records, import plans, metadata-only previews, human review decisions, dry-run import job drafts, execution preflights, and synthetic fixture row-reader dry-runs without running collectors, importing evidence rows, creating production cases, or generating analysis/report outputs.

## Non-Changing Boundaries

- Sentigraph is still not a crawler.
- Sentigraph still does not run private collector jobs.
- Sentigraph still does not call real platform APIs.
- Sentigraph still does not fetch URLs or scrape websites.
- Sentigraph still does not store cookies, sessions, or browser profiles.
- Sentigraph still does not expose raw author identifiers.
- Sentigraph still does not import provider package evidence rows into the Evidence Layer.
- Sentigraph still does not create production cases from provider packages.
- Sentigraph still does not run analysis, Sandbox generation, public event generation, or B-end report generation from this chain.
- Private collector capabilities remain outside Sentigraph core.
- Provider output is evidence, not official truth.
- Evidence Scale / Coverage still does not represent full-web or full-platform coverage.

## Current Phase 6 Chain

Analysis Request -> Provider Result -> Case Draft Handoff -> Evidence Import Plan -> Import Preview -> Human Review Decision -> Dry-run Import Job -> Execution Preflight -> Synthetic Row Reader Dry-Run

| Stage | Status | Local storage path | Append-only | Reads rows | Imports rows | Creates case | Runs analysis | API endpoint group |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Analysis Request | Implemented | `runtime/analysis_requests/requests/` | Request records are file-based | No | No | No | No | `/api/v1/analysis-requests` |
| Provider Result | Implemented as local file handoff | `runtime/analysis_requests/results/` | Provider result files are read locally | No | No | No | No | request detail/provider result read path |
| Case Draft Handoff | Implemented | `runtime/analysis_requests/case_drafts/` | Yes | No | No | No | No | `/case-drafts` |
| Evidence Import Plan | Implemented | `runtime/analysis_requests/import_plans/` | Yes | No | No | No | No | `/import-plans` |
| Import Preview | Implemented, metadata-only | `runtime/analysis_requests/import_previews/` | Yes | No | No | No | No | `/import-previews` |
| Human Review Decision | Implemented | `runtime/analysis_requests/review_decisions/` | Yes | No | No | No | No | `/review-decisions` |
| Dry-run Import Job | Implemented as non-executing gate | `runtime/analysis_requests/import_jobs/` | Yes | No | No | No | No | `/import-jobs` |
| Execution Preflight | Implemented, metadata and file-name checks only | `runtime/analysis_requests/execution_preflights/` | Yes | No | No | No | No | `/execution-preflights` |
| Synthetic Row Reader Dry-Run | Implemented for synthetic fixtures only | `runtime/analysis_requests/row_reader_dry_runs/` | Yes | Synthetic fixtures only | No | No | No | `/row-reader-dry-runs` |

Runtime storage is ignored and should not be committed.

## Phase 6A: File-Based Analysis Request MVP

Frontend route:

- `/#/analysis-requests`

Primary schema:

- `sentigraph_analysis_request_v1`

Storage:

- `runtime/analysis_requests/requests/`
- `runtime/analysis_requests/results/`

API endpoints:

- `GET /api/v1/analysis-requests/config`
- `POST /api/v1/analysis-requests`
- `GET /api/v1/analysis-requests`
- `GET /api/v1/analysis-requests/{request_id}`
- `POST /api/v1/analysis-requests/{request_id}/cancel`

Conservative defaults:

- `allow_live_collection=false`
- `allow_saved_profile=false`
- `allow_manual_snapshot=true`
- `allow_official_api=true`
- `allow_vendor_api=true`
- `forbid_proxy_pool=true`
- `forbid_captcha_bypass=true`
- `forbid_private_content=true`
- raw author ids, raw author names, profile URLs, and private messages are required to be removed or excluded.

## Phase 6B: Private Collector Side File Adapter

Private collector project path:

- `G:\AICODING\网页端任务二`

Status:

- The private collector project was observed as not a Git repository during earlier audits.
- No `git init` should be performed by Sentigraph work.

Collector-side scripts:

- `sentigraph:request:validate`
- `sentigraph:request:result`
- `sentigraph:request:scan`

Behavior:

- Reads `sentigraph_analysis_request_v1`.
- Writes `sentigraph_provider_job_result_v1`.
- Supports attaching existing package metadata only.
- Does not execute collection.
- Does not call APIs.
- Does not fetch URLs.
- Does not run browser automation.
- Does not use login, profile, cookie, or session access.
- Does not read or print secrets.
- Does not expose raw author identifiers.

## Phase 6C / 6C-Fix: Cross-Project File Handshake

Handshake status:

- Sentigraph creates an analysis request.
- Collector validates the request.
- Collector writes a provider result.
- Collector can attach existing package metadata.
- Sentigraph reads the result.

Schema compatibility issue found and fixed:

- `counts.evidence_items` -> `counts.evidence`
- `counts.root_content` -> `counts.roots`
- `validation.errors_count` -> `validation.errors`
- `validation.warnings_count` -> `validation.warnings`
- `validation.status=not_run` is accepted.

Canonical result fields now work.

Dong Lu / Sun Jihai package metadata test:

- `evidence=581`
- `comments=546`
- `sources=37`
- `roots=35`
- `validation.status=warn`
- `errors=0`
- `warnings=1`

## Phase 6D: Case Draft Handoff

Storage:

- `runtime/analysis_requests/case_drafts/`

Schema:

- `sentigraph_case_draft_handoff_v1`

Allowed only when:

- package status is package-ready or validation-warn.
- validation errors equal 0.
- safety status is safe or medium.

Boundary:

- No evidence rows imported.
- No case created.
- No analysis generated.
- No Sandbox or report generated.

## Phase 6E: Evidence Import Plan

Storage:

- `runtime/analysis_requests/import_plans/`

Schema:

- `sentigraph_evidence_import_plan_v1`

Default policy:

- `review_status=review_needed`
- `verification_status=source_url_provided_unverified`
- `trust_label=medium_low`
- `dedup_required=true`
- `audit_required=true`

Boundary:

- No evidence import.
- No case creation.
- No analysis, report, or Sandbox generation.

## Phase 6F: Docs-Only Manual Evidence Import Execution Design

Documents:

- `docs/architecture/manual_evidence_import_execution_v1.md`
- `docs/architecture/evidence_import_preview_contract_v1.md`
- `docs/architecture/evidence_import_review_decision_record_v1.md`

Scope:

- Defines the future manual import chain.
- Does not implement import.

## Phase 6G: Metadata-Only Evidence Import Preview

Storage:

- `runtime/analysis_requests/import_previews/`

Schema:

- `sentigraph_evidence_import_preview_v1`

Behavior:

- Metadata-only preview.
- `read_rows_now=false`.
- No evidence row parsing.
- No import.
- No case.
- No analysis.
- No report.

## Phase 6H: Human Review Decision Record

Storage:

- `runtime/analysis_requests/review_decisions/`

Storage behavior:

- Append-only.

Schema:

- `sentigraph_evidence_import_review_decision_v1`

Decisions:

- `approve_import`
- `reject_import`
- `request_more_source`
- `mark_limited_sample`
- `hold_for_privacy_review`

Boundary:

- `approve_import` only allows a future manual import phase.
- `approve_import` does not immediately import evidence.
- Checklist is required for `approve_import`.

## Phase 6I: Manual Evidence Import Job Dry-Run Gate

Storage:

- `runtime/analysis_requests/import_jobs/`

Storage behavior:

- Append-only.

Schema:

- `sentigraph_manual_evidence_import_job_v1`

Execution mode:

- `execution_mode=dry_run_gate`
- `status=draft_not_executed`

Now flags:

- `import_evidence_rows_now=false`
- `create_case_now=false`
- `run_analysis_now=false`
- `generate_report_now=false`

Boundary:

- No Evidence Layer write.

## Phase 6J: Docs-Only Manual Evidence Import Execution Design

Documents:

- `docs/architecture/manual_evidence_import_job_execution_v1.md`
- `docs/architecture/evidence_row_staging_contract_v1.md`
- `docs/architecture/review_only_case_import_contract_v1.md`
- `docs/architecture/evidence_import_audit_and_rollback_v1.md`

Scope:

- Defines future row reader, staging, review-only case, audit, and rollback.
- No implementation yet in this phase.

## Phase 6K: Manual Evidence Import Execution Preflight

Storage:

- `runtime/analysis_requests/execution_preflights/`

Storage behavior:

- Append-only.

Schema:

- `sentigraph_manual_evidence_import_execution_preflight_v1`

Behavior:

- Metadata and file-name level checks only.
- Checks package path and required file names.
- `row_files_opened=false`.
- `row_files_parsed=false`.
- No row content in response.
- No Evidence Layer write.

## Phase 6L: Synthetic Fixture Row Reader Dry-Run

Storage:

- `runtime/analysis_requests/row_reader_dry_runs/`

Storage behavior:

- Append-only.

Schema:

- `sentigraph_evidence_row_reader_dry_run_v1`

Behavior:

- Reads only synthetic fixture JSONL under backend test fixtures.
- Does not read real provider package rows.
- Does not read Dong/Sun or Helldivers package rows.
- Safe fixture and mixed fixture exist.
- Mixed fixture quarantines forbidden fields and rejects invalid JSON.
- No raw author/private values are exposed.
- No import.

## Current Frontend Route

Route:

- `/#/analysis-requests`

UI sections currently include:

- create analysis request
- provider result
- case draft handoff
- evidence import plan
- metadata-only import preview
- human review decision
- dry-run import job
- execution preflight
- synthetic row reader dry-run

Required UI meaning:

- no live crawling
- no provider execution
- no evidence import
- provider output is evidence, not truth

## Current Backend Endpoint Groups

Primary route group:

- `/api/v1/analysis-requests`

Related groups:

- `/case-drafts`
- `/import-plans`
- `/import-previews`
- `/review-decisions`
- `/import-jobs`
- `/execution-preflights`
- `/row-reader-dry-runs`

Representative routes:

- `GET /api/v1/analysis-requests/config`
- `POST /api/v1/analysis-requests`
- `GET /api/v1/analysis-requests`
- `GET /api/v1/analysis-requests/{request_id}`
- `POST /api/v1/analysis-requests/{request_id}/cancel`
- `POST /api/v1/analysis-requests/{request_id}/case-drafts`
- `POST /api/v1/analysis-requests/{request_id}/import-plans`
- `POST /api/v1/analysis-requests/{request_id}/import-previews`
- `POST /api/v1/analysis-requests/{request_id}/review-decisions`
- `POST /api/v1/analysis-requests/{request_id}/import-jobs`
- `POST /api/v1/analysis-requests/{request_id}/execution-preflights`
- `POST /api/v1/analysis-requests/{request_id}/row-reader-dry-runs`

## Runtime Directories

- `runtime/analysis_requests/requests/`
- `runtime/analysis_requests/results/`
- `runtime/analysis_requests/case_drafts/`
- `runtime/analysis_requests/import_plans/`
- `runtime/analysis_requests/import_previews/`
- `runtime/analysis_requests/review_decisions/`
- `runtime/analysis_requests/import_jobs/`
- `runtime/analysis_requests/execution_preflights/`
- `runtime/analysis_requests/row_reader_dry_runs/`

Runtime is ignored and should not be committed.

## Current Validation Status

Latest known validation from Phase 6L:

- `python -m pytest`: 697 passed.
- offline benchmarks: 522 passed, 0 failed.
- frontend build: passed with existing Vite chunk-size warning.
- API smoke passed for synthetic row-reader route tests.
- Browser smoke for Phase 6L was not completed because the local Vite dev server hit port binding `EACCES`.
- There is no blocker from tests or build.

## What This Still Does Not Do

- no real platform provider
- no official API provider
- no vendor API provider
- no MediaCrawler
- no OpenClaw production integration
- no real LLM
- no live collection
- no URL fetching or scraping
- no evidence rows imported
- no Evidence Layer write
- no review queue created
- no dedup run
- no production case created
- no public event generation
- no Sandbox fixture generation
- no report generation
- no Strategy Lab runtime
- no full-web/full-platform coverage claim
- no official verification claim

## Current Ready State

Decision:

- `ready_for_phase_6M_real_package_row_preview_design`

Recommendation:

- Before any real package row preview runtime, do a docs-only design or risk-control update first.
- Real package row preview must require an explicit human decision.
- It must be limited, redacted, metadata-linked, and must never import rows.

## Phase 6M Recommendation

Recommended next task:

- Phase 6M real package row preview design, not runtime first.

The design should define:

- explicit opt-in to read a tiny redacted sample from a selected package
- `max_rows=20`
- read-only behavior
- no import
- redaction of author, profile, and private fields
- privacy stop
- quarantine
- no broad real package scan
- no full dataset read
- no Evidence Layer write
- no analysis

## Commit Guidance

Recommended commit message:

- `Add Source 11 analysis request provider handoff status`

Recommended tag:

- No tag needed.
