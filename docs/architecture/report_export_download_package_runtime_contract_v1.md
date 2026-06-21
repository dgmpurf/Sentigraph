# Report Export Download / Package Runtime Contract v1

## Purpose

This document defines the future contract for a local report export download/package artifact.

The contract is for architecture handoff only. It does not mean runtime exists, and Phase 7V does not create files, ZIPs, download routes, public URLs, signed URLs, or external delivery.

## Future Object

```json
{
  "schema": "sentigraph_report_export_download_package_artifact_v1",
  "package_artifact_id": "download_package_artifact_...",
  "request_id": "req_...",
  "download_package_gate_id": "download_package_gate_...",
  "final_summary_report_export_artifact_ids": ["export_artifact_..."],
  "final_summary_report_id": "final_summary_report_...",
  "final_summary_report_export_gate_id": "export_gate_...",
  "package_mode": "local_manifest_only",
  "package_status": "manifest_ready|bundle_candidate_ready|blocked|privacy_hold|unsupported",
  "manifest_id": "download_package_manifest_...",
  "manifest_summary": {
    "artifact_count": 0,
    "safe_file_name_count": 0,
    "unsupported_format_count": 0,
    "contains_public_url": false,
    "contains_signed_url": false,
    "contains_download_route": false,
    "contains_raw_author_identifier": false,
    "contains_secret_like_value": false
  },
  "file_inventory_summary": {
    "runtime_relative_names": [],
    "content_hashes_available": false,
    "file_sizes_available": false,
    "absolute_paths_exposed": false,
    "file_bytes_exposed": false
  },
  "boundary_block": {
    "provider_output_is_evidence_not_truth": true,
    "not_official_verification": true,
    "not_full_web_coverage": true,
    "not_full_platform_coverage": true,
    "not_full_thread_coverage": true,
    "weak_evidence_warning_preserved": true,
    "rejected_evidence_excluded": true,
    "duplicate_no_amplification": true,
    "audit_trace_preserved": true
  },
  "audit_trace": {
    "export_artifact_audit_ids": [],
    "download_package_gate_audit_ids": [],
    "package_artifact_audit_ids": []
  },
  "created_at": "2026-06-21T00:00:00Z",
  "updated_at": "2026-06-21T00:00:00Z"
}
```

## Field Definitions

- `schema`: constant value `sentigraph_report_export_download_package_artifact_v1`.
- `package_artifact_id`: local metadata record id. It is not a URL, download id, signed URL id, public release id, B-end report id, Sandbox id, public event id, production case id, or Evidence Layer id.
- `request_id`: source file-based Analysis Request id.
- `download_package_gate_id`: upstream `ReportExportDownloadPackageGate` id.
- `final_summary_report_export_artifact_ids`: local export artifact ids included by metadata reference.
- `final_summary_report_id`: source final summary report id.
- `final_summary_report_export_gate_id`: upstream final summary report export gate id.
- `package_mode`: one of `local_manifest_only`, `local_controlled_bundle`, `local_zip_candidate`, or `local_download_candidate`. These are policy labels, not proof of generated files.
- `package_status`: safe status for the future runtime.
- `manifest_id`: local manifest metadata id.
- `manifest_summary`: safe aggregate metadata only.
- `file_inventory_summary`: safe inventory summary only; no absolute paths or file bytes.
- `boundary_block`: machine-readable boundary statements that must remain true.
- `audit_trace`: append-only audit ids used to reconstruct governance history.
- `created_at`: local UTC creation timestamp.
- `updated_at`: local UTC update timestamp.

## Package Status Semantics

- `manifest_ready`: safe manifest metadata exists under ignored runtime storage.
- `bundle_candidate_ready`: local controlled bundle candidate metadata exists, but no public access is implied.
- `blocked`: unsafe metadata, missing gates, missing audit trace, path traversal risk, or side-effect attempt blocked the runtime.
- `privacy_hold`: privacy risk stops runtime consideration.
- `unsupported`: requested format or mode is not supported by the local runtime policy.

## Required Safe Defaults

All future runtime records must keep these flags false:

- public URL generated
- signed URL generated
- download route created
- external delivery triggered
- B-end report generated
- Sandbox fixture generated
- public event generated
- Evidence Layer written
- production case created
- production review queue created
- production dedup run
- analysis engine called again
- real LLM called
- real API called
- URL fetched
- scraping performed
- artifact file bytes exposed in API response
- raw author identifiers exposed
- secrets exposed

## Contract Boundaries

This object must not be used to claim:

- official verification
- full-web coverage
- full-platform coverage
- full-thread coverage
- causal proof
- public release
- customer delivery
- external delivery
- production case promotion
- B-end report availability
- Sandbox or public event availability

