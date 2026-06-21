# Report Export Download / Package Runtime Design v1

## Purpose

This document designs the future controlled local Report Export Download / Package Runtime.

The runtime sits downstream of:

`FinalSummaryReportExportArtifact -> ReportExportDownloadPackageGate -> future ReportExportDownloadPackageRuntime`

It is upstream of any future B-end report, Sandbox, public event, external delivery, public access layer, public URL, signed URL, or direct file-byte response.

Phase 7V is design-only. It does not implement runtime code, create download routes, generate packages, generate ZIP files, expose runtime files, or read artifact file content.

## Runtime Position

The future runtime may only be considered after:

- `FinalSummaryReportExportArtifact` exists.
- `FinalSummaryReportExportArtifactAudit` exists.
- `ReportExportDownloadPackageGate` exists.
- `ReportExportDownloadPackageGate.status == ready_for_future_download_package_runtime`.
- upstream audit references are present.
- no privacy hold is active.
- no unresolved revision blocker remains.
- all download/package boundary acknowledgements are preserved.

Gate readiness means only that a future local runtime may be considered. It does not mean a package exists, a download route exists, a ZIP exists, a public URL exists, a signed URL exists, or external delivery is approved.

## Core Principle

The future runtime is a controlled local packaging boundary, not a publication boundary.

The runtime must preserve these statements:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- low-trust and weak-evidence warnings remain visible
- rejected evidence remains excluded
- duplicate evidence must not amplify risk, sentiment, coverage, or conclusions
- audit trace must remain append-only and visible
- no raw author identifiers
- no secrets
- no artifact content exposure through API responses

## Non-Goals

Phase 7V and the future runtime design do not authorize:

- runtime implementation in this phase
- download route creation
- direct file-byte response routes
- ZIP generation in this phase
- package generation in this phase
- public URL generation
- signed URL generation
- external delivery
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
- provider execution
- collector execution
- URL fetching
- scraping
- original package row parsing
- `evidence_items.jsonl` parsing
- `evidence_items.csv` parsing
- trust upgrade
- verification upgrade

## Future Package Modes

Future package modes are policy labels only:

- `local_manifest_only`: manifest metadata is prepared under ignored runtime storage.
- `local_controlled_bundle`: controlled local bundle candidate under ignored runtime storage.
- `local_zip_candidate`: ZIP candidate policy label only until a future implementation is separately approved.
- `local_download_candidate`: local download candidate policy label only until a future implementation is separately approved.

These labels are not implemented in Phase 7V. They must not be treated as generated files, exposed downloads, public links, signed links, or external delivery.

## Allowed Future Inputs

The future runtime may inspect safe metadata records only:

- `FinalSummaryReportExportArtifact`
- `FinalSummaryReportExportArtifactAudit`
- `ReportExportDownloadPackageGate`
- `ReportExportDownloadPackageGateAudit`
- upstream gate/report/audit identifiers referenced by those records
- safe artifact metadata such as type labels, format labels, safe relative runtime names, hashes, file sizes, and boundary statements if those are already present in safe metadata

The future runtime must not inspect:

- raw author identifiers
- raw author names
- profile URLs
- private messages
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- original provider package rows
- collector profiles
- browser profiles
- `evidence_items.jsonl`
- `evidence_items.csv`
- artifact file content unless a later file-content inspection gate explicitly allows a local safe read
- external URLs
- external APIs

## Future Output Category

The only future output category is a local package/download artifact metadata record.

Suggested schema name:

`sentigraph_report_export_download_package_artifact_v1`

The record is local metadata only. It does not itself authorize public access, signed access, external delivery, B-end delivery, Sandbox generation, public event generation, Evidence Layer write, or production case creation.

## First Runtime Recommendation

Future Phase 7W should design or implement only a local controlled runtime after verifying the 7U gate.

The first safe implementation should prefer `local_manifest_only` before any controlled bundle or ZIP candidate. It should:

1. read only safe metadata from the export artifact and download/package gate
2. validate the gate is ready
3. create a manifest record under ignored runtime storage
4. create append-only package artifact audit metadata
5. return safe relative names and summary counts only
6. keep public URL, signed URL, download route, B-end, Sandbox, public-event, Evidence Layer, production case, production dedup, provider, collector, and LLM flags false

## Boundary Copy

Future UI or CLI output should include equivalent copy:

- This is a local controlled package/download runtime candidate.
- It is not a public download route.
- It is not a public URL or signed URL.
- It is not external delivery.
- It is not official verification.
- It is not full-web, full-platform, or full-thread coverage.
- Provider output is evidence, not truth.
- Weak evidence warnings and rejected-evidence exclusion are preserved.
- Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions.
- B-end report, Sandbox, public event, and public access require separate gates.

