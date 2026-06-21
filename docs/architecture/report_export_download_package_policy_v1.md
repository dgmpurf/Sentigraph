# Report Export Download / Package Policy v1

## Purpose

This policy defines the human review rules for future Report Export Download / Package Gate decisions.

The gate sits after local `FinalSummaryReportExportArtifact` creation and before any future controlled download/package runtime. It is a governance decision only.

## Human Review Requirement

Human review is required before any future download/package runtime can be considered.

The reviewer must confirm:

- the export artifact exists
- the export artifact is local runtime-only
- export artifact metadata exists
- export artifact audit exists
- upstream export gate exists and was ready
- upstream final summary report exists
- upstream final report review gate exists
- required audit references exist
- boundary block is preserved
- warnings are preserved
- no rejected evidence is included
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- provider output is evidence, not truth
- not official verification remains visible
- not full-web coverage remains visible
- not full-platform coverage remains visible
- not full-thread coverage remains visible
- no raw, private, or secret-like fields appear in the metadata
- no public URL is created at gate stage
- no signed URL is created at gate stage
- no download route is created at gate stage
- no package file is created at gate stage

## Possible Decisions

### `approve_for_future_download_package_runtime`

Records that a future controlled delivery runtime may be considered.

Approval does not:

- create a download route
- create a local download file
- create a ZIP or package file
- create a public URL
- create a signed URL
- create a B-end report
- create a Sandbox fixture
- create a public event page
- write Evidence Layer
- create a production case
- run analysis

### `request_revision`

Records that the artifact or its metadata needs revision before future delivery consideration.

Typical reasons include:

- missing boundary block
- missing warning section
- unclear evidence scope
- unclear audit references
- unclear runtime path metadata
- wording that implies official verification
- wording that implies full-web, full-platform, or full-thread coverage
- wording that implies causal proof

### `block`

Records that the artifact is not eligible for future download/package runtime.

Typical reasons include:

- rejected evidence appears in the artifact metadata
- duplicate evidence appears to amplify conclusions
- boundary block was removed
- audit trace is missing
- unsafe downstream flags are true
- public URL or signed URL is attempted at gate stage
- B-end, Sandbox, or public-event generation is attempted at gate stage

### `privacy_hold`

Blocks all future delivery until the issue is resolved and separately reviewed.

Typical reasons include:

- raw author identifiers
- profile URLs
- private messages
- email addresses
- phone numbers
- passwords
- cookies
- tokens
- sessions
- API key values
- `.env` values
- other secret-like or private fields

## Required Boundary Preservation

The reviewer must ensure the following statements survive into future download/package runtime:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- selected, imported, or available evidence coverage only
- weak evidence remains warning-marked
- rejected evidence remains excluded
- duplicate evidence does not amplify risk, sentiment, coverage, or conclusions
- audit trace is required

Formatting, compression, packaging, and future delivery UI must not hide or weaken these statements.

## Public URL and Signed URL Policy

This gate must not create:

- public URL
- signed URL
- temporary access URL
- share link
- public object storage path
- externally reachable route

If a later phase introduces signed delivery, it must define a separate policy for:

- expiration
- recipient scope
- audit logging
- revocation
- boundary preservation
- privacy scan
- no external disclosure of secrets

Until that exists, `signed_url_candidate` and `public_url_candidate` must remain false.

## Approval Is Not Delivery

`approve_for_future_download_package_runtime` means only that a later runtime may be considered. It is not:

- artifact delivery
- customer delivery
- public release
- legal approval
- official verification
- full-web result
- full-platform result
- B-end report generation
- Sandbox generation
- public event generation

## Stop Conditions

The gate must stop with `privacy_hold` or `blocked` if it detects:

- private data
- secret-like data
- raw author identifiers
- missing audit references
- missing boundary notes
- rejected evidence leakage
- duplicate amplification
- trust upgrade
- verification upgrade
- official verification claim
- full-web or full-platform claim
- attempted public URL
- attempted signed URL
- attempted download route
- attempted package generation

