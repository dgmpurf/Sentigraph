# Report Export Download / Package File Boundary Policy v1

## Purpose

This document defines future file boundary rules for local report export download/package artifacts.

The policy is design-only. It does not create folders, files, ZIP archives, packages, download routes, public URLs, signed URLs, or external delivery.

## Runtime Storage Boundary

Future package metadata and local artifacts must stay under ignored runtime storage:

- `runtime/analysis_requests/report_export_download_packages/`
- `runtime/analysis_requests/report_export_download_package_artifacts/`
- `runtime/analysis_requests/report_export_download_package_artifact_audits/`

These paths are local runtime storage only. They must not be served publicly and must not be treated as production document storage.

## File Access Rules

The future runtime must enforce:

- no public serving of runtime files
- no direct file-byte response route
- no path traversal
- no absolute path exposure in API responses
- no public URL
- no signed URL
- no automatic external delivery
- no B-end report generation
- no Sandbox generation
- no public event generation
- no Evidence Layer write
- no production case creation
- no production review queue creation
- no production dedup
- no original package row read
- no artifact file content exposure through API responses

## Safe Relative Name Policy

If future runtime exposes file names, it may expose safe relative names only.

Allowed examples:

- `final_summary_report.md`
- `manifest.json`
- `evidence_appendix_metadata.json`

Forbidden examples:

- absolute paths
- parent traversal with `..`
- drive letters
- UNC paths
- browser profile paths
- private collector project paths
- names containing raw author identifiers
- names containing tokens, cookies, sessions, salts, passwords, API key values, email addresses, phone numbers, or private message fragments

## Package and ZIP Boundary

Future controlled bundle or ZIP candidate modes require separate implementation and review.

Even when a future local package exists:

- it is not a public download route
- it is not a public URL
- it is not a signed URL
- it is not external delivery
- it is not a B-end report
- it is not a Sandbox fixture
- it is not a public event page
- it must remain under ignored runtime storage until a separate gate allows a later step

## Download Route Boundary

Package artifact generation, download route creation, signed URL creation, public URL creation, and external delivery are separate concerns.

A future local package runtime does not automatically imply:

- browser download route
- API file-byte route
- public URL
- signed URL
- email or external transfer
- customer delivery
- public access

Each of those requires a separate future gate and explicit operator decision.

## Path Traversal and Metadata Checks

Future runtime must block:

- `..`
- absolute filesystem paths
- drive-letter paths
- UNC paths
- URL-like paths
- empty or ambiguous names
- names with secret-like values
- names with raw identity values
- metadata containing `public_url` or `signed_url` as active access values

Any blocked file boundary should produce an append-only audit with `unsafe_boundary_blocked` or `privacy_hold`.

## Response Boundary

API responses for future package runtime may return:

- package artifact id
- manifest id
- request id
- upstream gate ids
- status
- safe relative names
- counts
- warnings
- boundary statements
- audit ids

API responses must not return:

- file bytes
- absolute paths
- public URLs
- signed URLs
- direct download links
- raw author identifiers
- secrets
- original package row content
- artifact body content

