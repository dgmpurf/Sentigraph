# Final Summary Report Export Boundary and Audit Policy v1

## Purpose

This document defines the input boundary, output boundary, and audit requirements for future Final Summary Report Export Gate runtime and any later export runtime.

## Future Export Runtime Input Boundary

Future export runtime can only read:

- `FinalSummaryReport`
- `FinalSummaryReportAudit`
- `FinalSummaryReportExportGate`
- `FinalSummaryReportExportGateAudit`
- upstream audit records referenced by the final report and export gate

It must not read:

- original package rows
- `evidence_items.jsonl`
- `evidence_items.csv`
- external collector output rows
- private collector project files
- provider job folders
- browser profile data
- cookies, tokens, sessions, salts, passwords, API key values, or `.env` values
- raw author identifiers
- private messages
- URLs through network fetch

## Runtime Prohibitions

Future export runtime must not:

- fetch URLs
- call provider or collector
- call real LLM
- call external APIs
- write Evidence Layer
- create production case
- create production review queue
- run production dedup
- upgrade trust
- upgrade verification
- remove warnings
- include rejected evidence
- amplify duplicate evidence
- claim official verification
- claim full-web coverage
- claim full-platform coverage
- claim full-thread coverage
- claim causal proof
- create B-end report
- create Sandbox fixture
- create public event page

## Warning Preservation

The following warning classes must survive into future export runtime and exported output:

- coverage limitation
- weak evidence warning
- rejected evidence exclusion
- duplicate evidence no-amplification
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- uncertainty and causality caveats

Removing, hiding, or softening these warnings for readability is not allowed.

## Boundary Block Requirement

Every future exported output must include a boundary block stating:

- source is a local final Summary Report
- export is based on available reviewed evidence only
- provider output is evidence, not truth
- not official verification
- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- rejected evidence was excluded
- weak evidence remains warning-marked
- duplicate evidence does not amplify risk or conclusions
- audit trace is available

## Export Metadata Requirement

Every future export artifact should carry safe metadata:

- `schema`
- `export_gate_id`
- `final_summary_report_id`
- `request_id`
- `review_case_id`
- `created_at`
- `created_by`
- `export_format`
- `boundary_gate_id`
- `final_report_review_gate_id`
- `report_gate_id`
- `manual_analysis_execution_id`
- `result_candidate_id`
- audit refs

Metadata must not include raw author identifiers, private content, cookie values, token values, session identifiers, API key values, `.env` values, password values, email addresses, phone numbers, or profile URLs.

## Audit Policy

Final Summary Report Export Gate decisions must append audit entries.

Each audit entry should include:

- audit id
- export gate id
- final Summary Report id
- previous status if any
- new status
- export decision
- reviewer label
- reviewed at timestamp
- reason code
- note
- required revisions
- blocked reasons
- boundary checklist
- privacy scan result
- downstream side-effect flags
- safe-mode flags

Audit entries must be append-only. They must not overwrite previous decisions.

## Safe-Mode Flags

Every audit should explicitly record:

- `markdown_file_generated_now=false`
- `pdf_file_generated_now=false`
- `pptx_file_generated_now=false`
- `b_end_report_generated_now=false`
- `sandbox_generated_now=false`
- `public_event_generated_now=false`
- `evidence_layer_written_now=false`
- `production_case_created_now=false`
- `provider_or_collector_called_now=false`
- `real_llm_called_now=false`
- `url_fetched_now=false`

## Privacy Stop Policy

The gate or future runtime must stop with `privacy_hold` if any of the following are detected:

- raw author identifiers
- private messages
- cookie values
- token values
- session identifiers
- API key values
- `.env` values
- password values
- email addresses
- phone numbers
- profile URLs
- private account identifiers
- private or sensitive personal content not cleared for export

`privacy_hold` blocks export, B-end, Sandbox, and public-event downstream use.

## No Trust Upgrade

Export review and export formatting must not upgrade:

- trust label
- verification status
- coverage status
- source authenticity
- causality confidence
- official verification status

Formatting is not verification.

