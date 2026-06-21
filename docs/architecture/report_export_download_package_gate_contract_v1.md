# Report Export Download / Package Gate Contract v1

## Purpose

This contract defines the future `sentigraph_report_export_download_package_gate_v1` object.

The object records a human delivery-readiness decision for a local `FinalSummaryReportExportArtifact`. It is not a download route, ZIP package, public URL, signed URL, B-end report, Sandbox fixture, public event page, Evidence Layer write, production case, official verification, or full-web analysis.

## Future Object

```json
{
  "schema": "sentigraph_report_export_download_package_gate_v1",
  "download_package_gate_id": "...",
  "request_id": "...",
  "review_case_id": "...",
  "export_artifact_id": "...",
  "export_artifact_audit_id": "...",
  "final_summary_report_id": "...",
  "export_gate_id": "...",
  "created_at": "...",
  "created_by": "...",
  "status": "ready_for_future_download_package_runtime|needs_revision|blocked|privacy_hold",
  "delivery_decision": "approve_for_future_download_package_runtime|request_revision|block|privacy_hold",
  "allowed_future_delivery": {
    "local_metadata_download_candidate": true,
    "local_file_download_candidate": true,
    "zip_package_candidate": true,
    "signed_url_candidate": false,
    "public_url_candidate": false
  },
  "not_allowed_now": {
    "download_route_now": true,
    "zip_package_now": true,
    "public_url_now": true,
    "signed_url_now": true,
    "b_end_report_now": true,
    "sandbox_now": true,
    "public_event_now": true
  },
  "input_boundary": {
    "source": "final_summary_report_export_artifact",
    "read_runtime_file_content_now": false,
    "read_original_package_rows_now": false,
    "call_llm_now": false,
    "call_external_api_now": false,
    "write_evidence_layer_now": false,
    "create_production_case_now": false
  },
  "delivery_boundary": {
    "runtime_path_only": true,
    "public_url": false,
    "download_requires_future_runtime": true,
    "package_requires_future_runtime": true,
    "human_review_required": true
  },
  "downstream_readiness": {
    "can_run_future_download_package_runtime": true,
    "can_generate_download_now": false,
    "can_generate_package_now": false,
    "can_generate_b_end_report_now": false,
    "can_generate_sandbox_now": false,
    "can_generate_public_event_now": false,
    "requires_b_end_report_gate": true,
    "requires_sandbox_gate": true,
    "requires_public_event_gate": true
  },
  "blocked_reasons": [],
  "required_revisions": [],
  "warnings": [],
  "boundary_notes": [],
  "audit_refs": {}
}
```

## Field Definitions

### `schema`

Constant value: `sentigraph_report_export_download_package_gate_v1`.

### `download_package_gate_id`

Unique local identifier for the gate object. It must not be treated as a download id, package id, public URL id, signed URL id, B-end report id, Sandbox id, public event id, production case id, or Evidence Layer id.

### `request_id`

Local file-based Analysis Request id.

### `review_case_id`

Review-only case id. The gate does not create or promote a production case.

### `export_artifact_id`

The local `FinalSummaryReportExportArtifact` being reviewed for future controlled delivery runtime eligibility.

### `export_artifact_audit_id`

Audit record proving that the local export artifact was created through the approved final summary report export runtime path.

### `final_summary_report_id`

The local final summary report that was the source for the export artifact.

### `export_gate_id`

The upstream `FinalSummaryReportExportGate` that allowed the final summary report export runtime to create the local artifact.

### `created_at`

UTC timestamp for local gate creation.

### `created_by`

Local reviewer or runtime label. It must not include cookies, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, raw author identifiers, profile URLs, private messages, or private account identifiers.

### `status`

One of:

- `ready_for_future_download_package_runtime`
- `needs_revision`
- `blocked`
- `privacy_hold`

Ready means only that a future controlled download/package runtime may be considered. It does not create a route, file package, public URL, signed URL, or downstream product surface.

### `delivery_decision`

One of:

- `approve_for_future_download_package_runtime`
- `request_revision`
- `block`
- `privacy_hold`

The decision records a human review outcome. It does not rewrite the artifact automatically and does not expose the artifact.

### `allowed_future_delivery`

Candidate delivery modes that may be considered by future dedicated runtimes. These are candidates only:

- `local_metadata_download_candidate`: future metadata-only local download can be considered
- `local_file_download_candidate`: future local file download can be considered
- `zip_package_candidate`: future ZIP/package runtime can be considered
- `signed_url_candidate`: false until an explicit signed delivery policy exists
- `public_url_candidate`: false until an explicit public release policy exists

### `not_allowed_now`

Explicit no-side-effect flags. `true` means the action is not allowed during this gate phase.

### `input_boundary`

Machine-readable input restrictions. The source is the local export artifact metadata record. The gate does not read runtime file contents, original rows, external APIs, LLMs, Evidence Layer, or production case storage.

### `delivery_boundary`

Delivery limits for this gate:

- artifact remains runtime-path-only
- public URL remains false
- download requires a future runtime
- package requires a future runtime
- human review is required

### `downstream_readiness`

Future-runtime readiness booleans. `can_run_future_download_package_runtime` only authorizes a later runtime to be considered. All `can_generate_*_now` values must remain false.

### `blocked_reasons`

Human-readable reasons for `blocked` or `privacy_hold`, such as unsafe claims, missing boundary block, rejected evidence leakage, duplicate amplification risk, missing audit trace, missing artifact audit, public URL attempt, signed URL attempt, or privacy risk.

### `required_revisions`

Specific revisions required before the artifact can be reconsidered for future delivery runtime.

### `warnings`

Warnings that must remain visible to reviewers and future download/package runtime.

### `boundary_notes`

Boundary statements preserved from upstream gates and the local export artifact.

### `audit_refs`

References to upstream audit records. At minimum, this should include:

- `FinalSummaryReportExportArtifact`
- `FinalSummaryReportExportArtifactAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportReviewGate`
- `SummaryReportCandidate`
- `ReportGenerationGate`
- `ManualAnalysisExecution`
- `AnalysisResultBoundaryGate`

## Required Invariants

- The input source is `FinalSummaryReportExportArtifact` metadata only.
- The export artifact audit must exist.
- Required upstream gates and audits must exist.
- Runtime file content is not read during this gate.
- Original package rows are not read.
- `evidence_items.jsonl` and `evidence_items.csv` are not parsed.
- URLs are not fetched.
- Providers and collectors are not called.
- Real LLMs are not called.
- Evidence Layer is not written.
- Production case is not created.
- Trust and verification are not upgraded.
- Warnings are not removed.
- Rejected evidence remains excluded.
- Duplicate evidence does not amplify risk, sentiment, coverage, or conclusions.
- No official verification or full-web/full-platform/full-thread claim is introduced.
- No download route, ZIP package, public URL, signed URL, B-end report, Sandbox, or public-event artifact is generated.

## Suggested Audit Companion

A future runtime should append `sentigraph_report_export_download_package_gate_audit_v1`, recording:

- download/package gate id
- export artifact id
- reviewer label
- delivery decision
- previous and new gate status
- blocked reasons or required revisions
- boundary preservation checklist
- delivery boundary checklist
- audit references
- downstream side-effect flags, all false
- safe-mode flags, including no download route now, no package now, no public URL now, no signed URL now, no B-end report, no Sandbox, no public event, no Evidence Layer write, no production case, no URL fetch, no real API, and no real LLM

