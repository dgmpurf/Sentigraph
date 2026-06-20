# Summary Report Candidate Boundary and Audit Policy v1

## Purpose

This policy defines how future Summary Report Candidate Runtime must preserve boundaries and audit traceability.

The runtime may organize safe local candidate records into a reader-facing draft, but it must not remove warnings, upgrade trust, upgrade verification, or create downstream artifacts.

## Boundary Preservation

The candidate must preserve the `boundary_block` from `ManualAnalysisResultCandidate`.

At minimum, the boundary block must preserve:

- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- rejected evidence excluded
- weak evidence warning
- duplicate evidence does not amplify risk
- candidate-only status

The candidate must also preserve Report Generation Gate boundary notes.

If the upstream candidate or gate lacks boundary notes, future runtime must return `blocked` or `incomplete`.

## Audit Requirements

Future runtime must include audit references to:

- `ManualAnalysisExecutionAudit`
- `AnalysisResultBoundaryGateAudit`
- `ReportGenerationGateAudit`

The candidate should also preserve references to upstream review, dedup, promotion, and trigger audits when available through safe local records.

Every candidate should make the audit relationship explicit:

- what was reviewed
- what was excluded
- what remained weak
- what was dedup-governed
- which gates were passed
- which downstream outputs remain blocked

## No Warning Removal

The future runtime must not remove:

- weak evidence warnings
- rejected evidence exclusion
- duplicate non-amplification warning
- coverage limitation
- provider evidence-not-truth statement
- no official verification statement
- privacy/needs-more-source exclusion
- candidate-only status

If a user or caller requests warning removal, the runtime must block.

## Rejected Evidence

Rejected evidence must not appear in:

- executive summary candidate
- representative evidence section
- topic summary
- sentiment summary
- risk drivers
- narrative conclusions
- public-facing simplified language

Rejected evidence may appear only as audit-visible exclusion count or exclusion note.

## Duplicate Evidence

Duplicate evidence must not amplify:

- risk level
- sentiment count
- coverage count
- topic weight
- conclusion strength
- confidence level

Duplicate group size may be shown only as density, repetition, or traceability context.

## Trust and Verification

The candidate must not:

- upgrade trust labels
- upgrade verification status
- treat user-uploaded, manual, vendor, screenshot, or search-discovery evidence as official verification
- call screenshots or transcriptions verified
- claim official platform confirmation unless that is already proven by allowed official-source metadata

Provider output remains evidence, not truth.

## Privacy and Secret Safety

The candidate must not expose:

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
- email addresses
- phone numbers
- secret-like fields

If any of these appear in safe local inputs, the runtime must stop with `privacy_hold`.

## Input Restrictions

Future runtime may inspect only safe local candidate/gate/audit records.

It must not:

- parse `evidence_items.jsonl`
- parse `evidence_items.csv`
- re-read original package rows
- inspect private collector project files
- call provider jobs
- call collector jobs
- fetch URLs
- scrape websites
- call real platform, search, vendor, or LLM APIs

## Candidate Status Language

The candidate must explicitly state:

- local
- draft
- candidate only
- not final report
- no real platform action
- no real LLM call
- no external API call
- no export generated

## Blocking Conditions

Future runtime must block if:

- report gate is missing
- report gate is not ready
- report gate audit is missing
- boundary gate audit is missing
- manual execution audit is missing
- boundary block is missing
- warnings are missing
- rejected evidence appears in included sections
- duplicate amplification is requested
- trust or verification upgrade is requested
- privacy risk is detected
- secret-like value is detected
- original rows must be re-read to continue
- external API or LLM call is requested
- downstream output generation is requested
