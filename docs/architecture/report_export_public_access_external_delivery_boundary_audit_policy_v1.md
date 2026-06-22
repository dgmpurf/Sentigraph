# Report Export Public Access / External Delivery Boundary and Audit Policy v1

## Purpose

This policy defines boundary preservation and append-only audit expectations for a future Report Export Public Access / External Delivery Gate.

It is docs-only. It does not implement a runtime, backend routes, frontend UI, public access, external delivery, public URLs, signed URLs, file-byte responses, object storage publication, portal access, B-end reports, Sandbox artifacts, public event pages, Evidence Layer writes, production cases, real APIs, real LLM calls, URL fetching, or scraping.

## Boundary Snapshot

Every future gate audit must capture a boundary snapshot with these flags:

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

If any flag is true, the audit must record a blocker and the gate must not become ready.

## Audit Event Labels

Expected append-only audit event labels:

- `public_access_delivery_gate_created`
- `public_access_delivery_gate_blocked`
- `public_access_delivery_gate_revision_requested`
- `privacy_hold`
- `unsafe_public_url_blocked`
- `unsafe_signed_url_blocked`
- `unsafe_file_byte_route_blocked`
- `unsafe_external_delivery_blocked`
- `unsafe_runtime_file_exposure_blocked`
- `unsafe_absolute_path_exposure_blocked`
- `unsafe_manifest_content_exposure_blocked`
- `unsafe_export_artifact_content_exposure_blocked`
- `unsafe_zip_or_binary_archive_blocked`
- `unsupported_delivery_mode_blocked`
- `unsupported_access_mode_blocked`
- `downstream_gate_required`

## Required Audit Fields

Each future audit entry should include:

- audit id
- `public_access_delivery_gate_id`
- `request_id`
- `package_artifact_id`
- `download_package_gate_id`
- final summary report id
- final summary report export artifact ids
- previous status
- new status
- decision
- event label
- requested future access modes
- requested future delivery modes
- reviewer/operator label
- reason or note
- upstream package artifact refs
- upstream audit refs
- boundary snapshot
- warnings snapshot
- blockers snapshot
- created_at

Audit records must not include secrets, cookies, tokens, sessions, salts, API key values, raw author identifiers, profile URLs, private messages, original package rows, manifest file content, export artifact content, absolute filesystem paths, or file bytes.

## Append-Only Requirement

Future gate audits must be append-only:

- create a new audit record for every decision
- never overwrite prior audit events
- never delete prior audit events as part of normal decision flow
- preserve blocked and privacy-hold events
- preserve unsupported mode decisions
- preserve downstream-gate-required decisions

## Boundary Enforcement

The future gate must block:

- public URL generation
- signed URL generation
- public download route creation
- file-byte response creation
- object storage publication
- portal publication
- external delivery
- email sending
- runtime file exposure
- absolute path exposure
- manifest file content exposure
- export artifact content exposure
- export artifact file content read/parse/copy
- ZIP or binary archive generation
- B-end report generation
- Sandbox generation
- public event generation
- Evidence Layer write
- production case/review queue/dedup creation
- real API or real LLM calls
- URL fetching or scraping
- original package row reads

## Reviewer And Operator Labels

Reviewer/operator labels should be safe local labels only.

They must not include:

- real personal contact information
- email addresses
- phone numbers
- account handles
- cookies
- sessions
- API keys
- tokens
- salts
- passwords
- absolute filesystem paths

## Audit Boundary Copy

Future audit timelines should show equivalent copy:

- Gate audit only; no public access or external delivery was performed.
- Future public access or external delivery requires separate runtime approval.
- Public URL, signed URL, download route, file-byte response, object storage publication, portal access, email delivery, B-end report, Sandbox, and public event flags remain false.
- Provider output is evidence, not truth.
- This is not official verification, full-web coverage, full-platform coverage, full-thread coverage, or causal proof.

