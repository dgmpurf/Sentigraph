# Report Export Download / Package Runtime To B-end / Sandbox / Public Gate v1

## Purpose

This document separates the future local Report Export Download / Package Runtime from downstream product surfaces.

A local package/download artifact does not authorize B-end report generation, Sandbox generation, public event generation, public URL creation, signed URL creation, or external delivery.

## Downstream Separation

The future chain must remain:

1. `FinalSummaryReportExportArtifact`
2. `ReportExportDownloadPackageGate`
3. future `ReportExportDownloadPackageRuntime`
4. future downstream gates, if separately approved

The downstream gates are separate:

- B-end report generation gate
- Sandbox generation gate
- public event generation gate
- external delivery / public access gate
- public URL gate
- signed URL gate

The package runtime cannot skip or replace any downstream gate.

## What A Future Package Artifact Means

A future package artifact means:

- local safe metadata has been prepared
- upstream gate refs are preserved
- boundary statements are preserved
- audit refs are available
- package mode is recorded
- unsafe delivery flags remain false

It does not mean:

- customer-facing B-end report exists
- Sandbox fixture exists
- public event page exists
- public download exists
- signed delivery exists
- external delivery occurred
- Evidence Layer was written
- production case was created
- production review queue was created
- production dedup ran
- analysis was rerun
- official verification occurred
- full-web, full-platform, or full-thread coverage exists

## Downstream Gate Requirements

Any future B-end report, Sandbox, or public event step must require:

- explicit human/operator decision
- package artifact id
- package manifest id
- upstream download/package gate id
- upstream final summary report id
- audit timeline completeness
- coverage limitations acknowledged
- weak evidence warnings preserved
- rejected evidence exclusion preserved
- duplicate no-amplification preserved
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- no privacy blockers
- no public URL or signed URL unless a separate public access gate allows it

## Public Access Gate Boundary

Public access is its own future gate.

The public access gate must separately decide:

- whether any artifact may be exposed outside local runtime storage
- whether a public URL is allowed
- whether a signed URL is allowed
- whether external delivery is allowed
- what privacy and redaction checks are required
- what expiration, access logging, and revocation policy is required

Until such a gate exists, all public URL, signed URL, direct download, and external delivery flags must remain false.

## Audit Policy

Future runtime and downstream gates must use append-only audit records.

Expected audit event labels:

- `package_artifact_created`
- `package_artifact_blocked`
- `manifest_created`
- `unsupported_format_blocked`
- `unsafe_boundary_blocked`
- `privacy_hold`
- `downstream_gate_required`
- `public_access_gate_required`

Each audit should include:

- package artifact id
- manifest id if present
- upstream gate refs
- reviewer or operator label
- boundary snapshot
- decision
- reason
- created_at
- downstream flags, all false unless that downstream gate specifically owns the flag

## Boundary Copy For Downstream Handoff

Future UI, CLI, and API responses should include equivalent copy:

- This package artifact is local and controlled.
- It is not a B-end report.
- It is not a Sandbox fixture.
- It is not a public event page.
- It is not a public URL or signed URL.
- It is not external delivery.
- Provider output is evidence, not truth.
- This is not official verification.
- This is not full-web, full-platform, or full-thread coverage.
- Weak evidence warnings, rejected-evidence exclusion, duplicate no-amplification, and audit trace must stay visible.

## Future Phase Recommendation

Recommended sequence:

- 7W: Report Export Download / Package Runtime
- 7X: Report Export Download / Package Runtime QA
- 7Y: B-end Report Package Gate Design
- 7Z: Sandbox/Public Event Package Gate Design
- 8A: Public Access / External Delivery Gate Design

Do not implement B-end report, Sandbox, public event, public URL, signed URL, or external delivery directly inside the package runtime.

