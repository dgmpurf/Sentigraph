# Report Export Public Access / External Delivery Gate Design v1

## Purpose

This document designs a future Report Export Public Access / External Delivery Gate.

The gate sits after the local manifest-only report export package runtime:

`FinalSummaryReport -> FinalSummaryReportExportGate -> FinalSummaryReportExportArtifact -> ReportExportDownloadPackageGate -> ReportExportDownloadPackageArtifact -> future ReportExportPublicAccessExternalDeliveryGate`

The gate decides only whether a local manifest-only package artifact may be considered by a later public access or external delivery runtime.

This phase is docs-only. It does not implement public access, external delivery, a download route, a file-byte response, a public URL, a signed URL, object storage publication, portal access, B-end report generation, Sandbox generation, public event generation, Evidence Layer writes, production case creation, real provider execution, real API calls, real LLM calls, URL fetching, or scraping.

## Gate Position

This gate is downstream of:

- `FinalSummaryReport`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportArtifact`
- `ReportExportDownloadPackageGate`
- `ReportExportDownloadPackageArtifact`
- local manifest-only package runtime metadata

It is upstream of any future:

- public download route
- file-byte response
- public URL
- signed URL
- external delivery
- object storage publication
- restricted portal access
- B-end report generation
- Sandbox generation
- public event generation

Gate readiness means only that a future runtime may be considered. It does not mean any public access or delivery has happened.

## Core Principle

The public access / external delivery gate is a governance decision boundary, not a delivery runtime.

The gate must preserve these statements:

- provider output is evidence, not truth
- package artifacts are not official verification
- package artifacts are not full-web coverage
- package artifacts are not full-platform coverage
- package artifacts are not full-thread coverage
- evidence scope remains limited to imported or available evidence
- low-trust and weak-evidence warnings remain visible
- rejected evidence exclusion remains visible
- duplicate evidence must not amplify risk, sentiment, coverage, or conclusions
- local manifest-only package metadata does not equal a public download
- public access and external delivery are future gated steps
- B-end, Sandbox, and public-event surfaces require separate gates

## Non-Goals

Phase 7X does not authorize:

- runtime implementation
- backend route creation
- frontend UI creation
- public download route creation
- file-byte response route creation
- public URL generation
- signed URL generation
- external delivery
- email delivery
- object storage upload
- portal publication
- download link creation
- ZIP generation
- binary archive generation
- runtime file exposure
- absolute filesystem path exposure
- runtime manifest content exposure
- export artifact file content reading
- export artifact file content parsing
- export artifact file content copying
- B-end report generation
- Sandbox fixture generation
- public event page generation
- Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- analysis engine execution
- real LLM calls
- real platform, search, RSS, GDELT, vendor, or provider API calls
- provider or collector execution
- URL fetching
- scraping
- original package row parsing
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- trust upgrade
- verification upgrade

## Required Upstream Eligibility

The future gate may only be considered when:

- upstream `ReportExportDownloadPackageArtifact` exists
- upstream package artifact status is `local_manifest_ready` or an equivalent safe status
- upstream package artifact has append-only audit
- upstream `ReportExportDownloadPackageGate` exists
- upstream download/package gate audit exists
- upstream `FinalSummaryReportExportArtifact` exists
- upstream final summary report export artifact audit exists
- upstream final summary report exists
- package manifest summary contains only safe metadata
- no public URL exists
- no signed URL exists
- no download URL exists
- no ZIP or binary archive exists
- no absolute filesystem path is exposed
- no raw author identifiers are present
- no secrets, tokens, cookies, sessions, salts, or API key values are present
- no file bytes are exposed
- no artifact content is exposed
- no original package rows are inspected
- all boundary flags remain safe
- downstream B-end, Sandbox, and public event gates remain separate

If any of these requirements fail, the future gate must fail closed as `blocked` or `privacy_hold`.

## Decision And Status Design

Suggested decision values:

- `approve_for_future_public_access_external_delivery_runtime`
- `request_revision`
- `block`
- `privacy_hold`

Suggested status mapping:

- `ready_for_future_public_access_external_delivery_runtime`
- `needs_revision`
- `blocked`
- `privacy_hold`

`ready_for_future_public_access_external_delivery_runtime` means only that a future public access or external delivery runtime may be considered after separate approval. It must not create public access or delivery.

## Future Access And Delivery Mode Labels

The following labels are design labels only. They must not be treated as implemented runtime behavior:

- `public_download_route_future_candidate`
- `file_byte_response_future_candidate`
- `signed_url_future_candidate`
- `public_url_future_candidate`
- `restricted_portal_access_future_candidate`
- `object_storage_publication_future_candidate`
- `external_delivery_future_candidate`
- `internal_handoff_future_candidate`

Each label remains blocked until a separate future runtime is explicitly approved, implemented, reviewed, and validated.

## Required Boundary Block

Any future gate object must include a boundary block with the following current flags:

```json
{
  "creates_public_download_route_now": false,
  "creates_file_byte_response_now": false,
  "generates_public_url_now": false,
  "generates_signed_url_now": false,
  "performs_external_delivery_now": false,
  "sends_email_now": false,
  "uploads_to_object_storage_now": false,
  "publishes_to_portal_now": false,
  "exposes_runtime_file_now": false,
  "exposes_absolute_path_now": false,
  "exposes_manifest_file_content_now": false,
  "exposes_export_artifact_content_now": false,
  "reads_export_artifact_file_content_now": false,
  "copies_export_artifact_content_now": false,
  "generates_zip_now": false,
  "generates_binary_archive_now": false,
  "generates_b_end_report_now": false,
  "generates_sandbox_now": false,
  "generates_public_event_now": false,
  "writes_evidence_layer_now": false,
  "creates_production_case_now": false,
  "calls_real_api_now": false,
  "calls_real_llm_now": false,
  "fetches_url_now": false,
  "scrapes_now": false,
  "reads_original_package_rows_now": false
}
```

If any flag is true, the gate must not report readiness.

## Public Access And External Delivery Separation

The future chain must keep these concepts separate:

- local package artifact generation
- public access gate
- public access runtime
- external delivery gate
- external delivery runtime
- B-end report gate and runtime
- Sandbox generation gate and runtime
- public event generation gate and runtime

This gate readiness does not authorize B-end report generation, Sandbox generation, public event generation, real provider execution, Evidence Layer writes, production case creation, or production review/dedup workflows.

## First Runtime Recommendation

Future Phase 7Y should implement only a gate runtime if explicitly approved.

The first safe runtime should:

1. read only safe upstream metadata records
2. verify local manifest-only package artifact readiness
3. verify append-only audit references
4. preserve boundary flags as false
5. record requested future access and delivery mode labels
6. append a gate audit record
7. not create public access, delivery, routes, links, file bytes, object storage, portal access, B-end reports, Sandbox artifacts, public events, Evidence Layer writes, production cases, real API calls, real LLM calls, URL fetches, or scraping

## Boundary Copy

Future UI, CLI, or API output should include equivalent copy:

- This is a public access / external delivery gate, not public access or delivery.
- It does not create a download route, file-byte response, public URL, signed URL, portal access, object storage publication, or external delivery.
- Local manifest-only package metadata does not equal a public download.
- Provider output is evidence, not truth.
- This is not official verification.
- This is not full-web, full-platform, or full-thread coverage.
- Weak evidence warnings, rejected-evidence exclusion, duplicate no-amplification, and audit trace must remain visible.
- B-end report, Sandbox, and public event generation require separate gates.

