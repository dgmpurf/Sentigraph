# Report Export Download / Package Boundary and Audit Policy v1

## Purpose

This policy defines boundary and audit requirements for any future download/package runtime after the Report Export Download / Package Gate.

It is design-only. It does not implement download/package runtime, route exposure, package creation, or public delivery.

## Allowed Future Runtime Inputs

After a future gate is approved, a future download/package runtime may read only:

- `FinalSummaryReportExportArtifact` metadata
- `FinalSummaryReportExportArtifactAudit`
- `ReportExportDownloadPackageGate`
- `ReportExportDownloadPackageGateAudit`
- upstream audit references embedded in those records

The future runtime may read the local artifact file only after a separate future runtime approval explicitly allows it. This design phase does not read runtime file content.

## Forbidden Inputs

The future download/package runtime must not read:

- original provider package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- external collector raw row files
- private collector project files
- browser profiles
- cookies
- tokens
- sessions
- salts
- passwords
- API key values
- `.env` values
- raw author identifiers
- profile URLs
- private messages
- external URLs through network fetch

## Forbidden Actions

The future download/package runtime must not:

- fetch URLs
- scrape websites
- call provider jobs
- call collector jobs
- call real LLMs
- call real platform, search, vendor, or provider APIs
- write Evidence Layer
- create production case
- create production review queue
- run production dedup
- run analysis
- upgrade trust
- upgrade verification
- remove warnings
- include rejected evidence
- amplify duplicate evidence
- claim official verification
- claim full-web coverage
- claim full-platform coverage
- claim full-thread coverage
- create B-end report
- create Sandbox fixture
- create public event page

## Boundary Preservation Checklist

Every future runtime and audit must preserve:

- local export artifact source
- runtime path scope
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- coverage limitation
- weak evidence warning
- rejected evidence excluded
- duplicate evidence no amplification
- audit trace
- human review decision
- no public URL at this gate
- no signed URL at this gate

## Audit Requirements

Each future gate decision must append an audit record containing:

- gate id
- export artifact id
- previous gate status
- new gate status
- delivery decision
- reviewer label
- reviewed_at timestamp
- reason or note
- boundary preservation checklist
- privacy scan result
- blocked reasons
- required revisions
- audit references
- safe-mode flags
- downstream side-effect flags

The audit must be append-only. It must not overwrite prior artifact, export gate, final report, analysis, review, dedup, or promotion audits.

## Safe-Mode Flags

The audit should explicitly record:

```json
{
  "download_route_created": false,
  "zip_package_created": false,
  "public_url_created": false,
  "signed_url_created": false,
  "b_end_report_generated": false,
  "sandbox_generated": false,
  "public_event_generated": false,
  "evidence_layer_written": false,
  "production_case_created": false,
  "provider_or_collector_called": false,
  "real_api_called": false,
  "real_llm_called": false,
  "url_fetch_or_scrape_performed": false,
  "original_package_rows_read": false,
  "trust_upgraded": false,
  "verification_upgraded": false
}
```

## Privacy Hold

`privacy_hold` must block all future delivery runtimes.

Privacy hold is required if the gate or future runtime detects:

- raw author identifiers
- profile URLs
- private messages
- email addresses
- phone numbers
- passwords
- cookies
- tokens
- sessions
- salts
- API key values
- `.env` values
- other secret-like or private fields

The hold can be lifted only by a separate audited review action after the unsafe field is removed or proven to be a false positive.

## Boundary Copy

Future UI, CLI, or JSON output should say:

- The download/package gate records eligibility only.
- The local export artifact is not a public download.
- No download route, package, public URL, or signed URL is created now.
- Provider output is evidence, not truth.
- The artifact is not official verification.
- The artifact is not full-web, full-platform, or full-thread coverage.
- Warnings, exclusions, and duplicate no-amplification must remain visible.
- B-end, Sandbox, and public-event generation require separate gates.

