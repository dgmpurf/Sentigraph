# Report Export Download / Package Manifest Policy v1

## Purpose

This document defines the safe manifest policy for a future local report export download/package runtime.

The manifest is safe metadata only. It is not a download file, ZIP file, public URL, signed URL, external delivery record, B-end report, Sandbox fixture, public event page, Evidence Layer write, or production case.

## Manifest Role

The future manifest should help a human operator understand what a local package candidate contains without exposing file bytes or private source material.

It may record:

- manifest id
- source request id
- download/package gate id
- export artifact ids
- source final summary report ids
- export format labels
- artifact filenames or safe relative names if allowed
- content hashes if a future runtime supports safe local hashing
- file sizes if a future runtime supports safe local metadata inspection
- package boundary statements
- evidence scope and coverage limitations
- unsupported format notes
- audit references
- created/updated timestamps

## Prohibited Manifest Content

The manifest must not include:

- raw author identifiers
- raw author names
- profile URLs
- private messages
- cookies
- tokens
- sessions
- salts
- passwords
- API key values
- `.env` values
- raw original package rows
- `evidence_items.jsonl` rows
- `evidence_items.csv` rows
- artifact file content
- public URLs
- signed URLs
- real download links
- absolute runtime paths
- browser profile paths
- collector profile paths
- private collector project paths

## Safe Manifest Shape

```json
{
  "schema": "sentigraph_report_export_download_package_manifest_v1",
  "manifest_id": "download_package_manifest_...",
  "package_artifact_id": "download_package_artifact_...",
  "request_id": "req_...",
  "download_package_gate_id": "download_package_gate_...",
  "source_artifacts": [
    {
      "export_artifact_id": "export_artifact_...",
      "artifact_type": "analyst_markdown",
      "artifact_format": "markdown",
      "safe_relative_name": "final_summary_report.md",
      "content_hash": "",
      "file_size_bytes": null,
      "unsupported_format": false
    }
  ],
  "coverage_boundary": {
    "not_full_web_coverage": true,
    "not_full_platform_coverage": true,
    "not_full_thread_coverage": true
  },
  "trust_boundary": {
    "provider_output_is_evidence_not_truth": true,
    "not_official_verification": true,
    "weak_evidence_warning_preserved": true,
    "rejected_evidence_excluded": true,
    "duplicate_no_amplification": true
  },
  "access_boundary": {
    "public_url": false,
    "signed_url": false,
    "download_route": false,
    "external_delivery": false
  },
  "audit_refs": {}
}
```

## Hash and Size Policy

Future content hashes and file sizes are optional safe metadata.

If supported later:

- compute hashes only for files already produced by approved local export runtime
- do not hash original provider package rows
- do not hash private collector raw files
- do not expose absolute file paths
- do not expose file bytes
- keep hash/size values inside ignored runtime manifest metadata

If unsupported:

- leave hash fields empty
- leave size fields null
- record `unsupported_format_count` or equivalent safe summary

## Unsupported Formats

Unsupported formats must be recorded without trying to render or convert them.

Examples:

- PDF remains unsupported unless a safe repo-local renderer exists.
- PPTX binary remains unsupported unless a safe local deck renderer exists.
- Deck outline may be JSON metadata only.
- Unknown binary formats are blocked.

Unsupported format handling must not call real LLMs, real APIs, external converters, browsers, network renderers, or URL fetchers.

## Required Boundary Statements

Every manifest must carry boundary statements equivalent to:

- This package candidate is local metadata only until a future runtime implements controlled output.
- It is not a public URL or signed URL.
- It is not official verification.
- It is not full-web, full-platform, or full-thread coverage.
- Provider output is evidence, not truth.
- Weak evidence warnings remain visible.
- Rejected evidence remains excluded.
- Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.
- B-end report, Sandbox, public event, and external delivery require separate future gates.

