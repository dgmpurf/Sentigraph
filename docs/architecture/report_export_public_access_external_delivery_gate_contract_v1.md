# Report Export Public Access / External Delivery Gate Contract v1

## Purpose

This document defines the future contract for a Report Export Public Access / External Delivery Gate.

The contract is for architecture handoff only. It does not implement runtime code, backend routes, frontend UI, public download routes, file-byte responses, public URLs, signed URLs, external delivery, object storage publication, portal access, B-end report generation, Sandbox generation, or public event generation.

## Future Object

```json
{
  "schema": "sentigraph_report_export_public_access_external_delivery_gate_v1",
  "public_access_delivery_gate_id": "public_access_delivery_gate_...",
  "request_id": "req_...",
  "package_artifact_id": "download_package_artifact_...",
  "download_package_gate_id": "download_package_gate_...",
  "final_summary_report_export_artifact_ids": ["export_artifact_..."],
  "final_summary_report_id": "final_summary_report_...",
  "gate_type": "report_export_public_access_external_delivery_gate",
  "gate_version": "v1",
  "gate_status": "ready_for_future_public_access_external_delivery_runtime|needs_revision|blocked|privacy_hold",
  "access_delivery_decision": "approve_for_future_public_access_external_delivery_runtime|request_revision|block|privacy_hold",
  "requested_future_access_modes": [],
  "requested_future_delivery_modes": [],
  "upstream_package_artifact_status": "local_manifest_ready",
  "package_manifest_summary": {
    "package_mode": "local_manifest_only",
    "safe_metadata_only": true,
    "manifest_file_content_exposed": false,
    "export_artifact_content_exposed": false,
    "absolute_paths_exposed": false,
    "public_url_present": false,
    "signed_url_present": false,
    "download_url_present": false,
    "zip_present": false,
    "binary_archive_present": false
  },
  "eligibility_summary": {
    "upstream_package_artifact_exists": true,
    "upstream_package_artifact_audit_exists": true,
    "download_package_gate_exists": true,
    "download_package_gate_audit_exists": true,
    "final_summary_report_export_artifact_exists": true,
    "final_summary_report_export_artifact_audit_exists": true,
    "safe_metadata_only": true,
    "no_privacy_hold": true,
    "no_public_access_or_delivery_side_effect": true
  },
  "boundary_block": {
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
  },
  "downstream_gate_policy": {
    "public_access_runtime_requires_separate_approval": true,
    "external_delivery_runtime_requires_separate_approval": true,
    "b_end_report_requires_separate_gate": true,
    "sandbox_generation_requires_separate_gate": true,
    "public_event_generation_requires_separate_gate": true
  },
  "audit_trace": {
    "package_artifact_audit_ids": [],
    "download_package_gate_audit_ids": [],
    "final_summary_report_export_artifact_audit_ids": [],
    "public_access_delivery_gate_audit_ids": []
  },
  "warnings": [],
  "blockers": [],
  "operator_label": "reviewer_or_operator",
  "reviewer_label": "reviewer_or_operator",
  "note": "Gate record only; no public access or external delivery performed.",
  "created_at": "2026-06-22T00:00:00Z",
  "updated_at": "2026-06-22T00:00:00Z"
}
```

## Field Definitions

- `schema`: constant value `sentigraph_report_export_public_access_external_delivery_gate_v1`.
- `public_access_delivery_gate_id`: local gate id. It is not a URL, signed URL id, public release id, object storage id, portal id, B-end report id, Sandbox id, public event id, production case id, or Evidence Layer id.
- `request_id`: source file-based Analysis Request id.
- `package_artifact_id`: upstream `ReportExportDownloadPackageArtifact` id.
- `download_package_gate_id`: upstream `ReportExportDownloadPackageGate` id.
- `final_summary_report_export_artifact_ids`: upstream export artifact ids referenced by metadata only.
- `final_summary_report_id`: source final summary report id.
- `gate_type`: constant value `report_export_public_access_external_delivery_gate`.
- `gate_version`: contract version.
- `gate_status`: safe status for this gate.
- `access_delivery_decision`: human or operator decision for this gate.
- `requested_future_access_modes`: future-only access mode labels.
- `requested_future_delivery_modes`: future-only delivery mode labels.
- `upstream_package_artifact_status`: upstream package artifact status observed from safe metadata.
- `package_manifest_summary`: safe metadata summary only. It must not include manifest file content, export artifact content, absolute paths, URLs, file bytes, or original package rows.
- `eligibility_summary`: machine-readable eligibility facts.
- `boundary_block`: required current-side-effect flags. All listed values must remain false for readiness.
- `downstream_gate_policy`: explicit separation between this gate and future downstream runtimes.
- `audit_trace`: append-only audit ids for upstream and this future gate.
- `warnings`: user-visible limitation and safety warnings.
- `blockers`: reasons that prevent readiness.
- `operator_label` / `reviewer_label`: non-secret human-readable label for the local reviewer/operator.
- `note`: optional review note. It must not contain secrets, raw author identifiers, private messages, cookies, tokens, sessions, salts, API key values, or absolute filesystem paths.
- `created_at`: UTC creation timestamp.
- `updated_at`: UTC update timestamp.

## Decision Values

- `approve_for_future_public_access_external_delivery_runtime`: permits a later runtime to be considered. It does not perform access or delivery.
- `request_revision`: upstream metadata, warnings, or boundary language require revision before a later runtime may be considered.
- `block`: unsafe or incomplete state prevents the gate from becoming ready.
- `privacy_hold`: privacy, secret, raw identifier, or exposure risk stops the gate.

## Status Values

- `ready_for_future_public_access_external_delivery_runtime`: a future runtime may be considered after separate approval.
- `needs_revision`: the package or metadata needs revision before readiness.
- `blocked`: required upstream records, audits, or boundary conditions are missing or unsafe.
- `privacy_hold`: privacy risk requires review and blocks readiness.

## Future Mode Labels

These labels are policy labels only:

- `public_download_route_future_candidate`
- `file_byte_response_future_candidate`
- `signed_url_future_candidate`
- `public_url_future_candidate`
- `restricted_portal_access_future_candidate`
- `object_storage_publication_future_candidate`
- `external_delivery_future_candidate`
- `internal_handoff_future_candidate`

No label creates a route, URL, file-byte response, object storage publication, portal access, delivery action, or public artifact.

## Required Safe Defaults

All future gate records must keep these statements true:

- no public download route exists
- no file-byte response exists
- no public URL exists
- no signed URL exists
- no external delivery occurred
- no object storage publication occurred
- no portal publication occurred
- no runtime file was exposed
- no absolute filesystem path was exposed
- no manifest file content was exposed
- no export artifact content was exposed
- no export artifact file content was read, parsed, or copied
- no ZIP or binary archive was generated
- no B-end report, Sandbox, or public event was generated
- no Evidence Layer write occurred
- no production case, review queue, or dedup was created
- no real API, real LLM, URL fetch, or scraping occurred
- no original package rows were read

