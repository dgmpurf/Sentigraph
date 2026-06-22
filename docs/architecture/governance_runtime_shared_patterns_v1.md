# Governance Runtime Shared Patterns v1

Status: design only. This document defines reusable patterns and does not implement shared code.

## Purpose

The Analysis Requests chain repeats a small set of governance runtime patterns: request schema, record schema, audit schema, decision-to-status mapping, eligibility validation, boundary flags, no-side-effect audit fields, and downstream gate separation. Future refactors should extract these patterns without changing behavior.

## Gate Request Schema Pattern

A gate request should generally include:

- upstream record IDs
- human decision
- reviewer label
- optional note
- acknowledgement booleans
- explicit `*_now=false` side-effect flags when the phase has dangerous future capabilities
- optional revisions or blockers

The request schema should reject unsafe extra fields for phases that could otherwise be confused with delivery, download, promotion, or evidence write behavior.

## Gate Record Schema Pattern

A gate record should generally include:

- stable schema name
- gate ID
- request ID
- upstream IDs
- decision
- status
- created timestamp
- reviewer label
- eligibility summary
- boundary block
- warnings
- downstream gate policy
- safe metadata only

Gate records are local governance records. They are not proof of truth, not official verification, not analysis output, and not public delivery.

## Audit Record Schema Pattern

An audit record should generally include:

- stable schema name
- audit ID
- request ID
- related gate or artifact ID
- decision
- status at creation time
- reviewer label
- note
- analysis effect
- now flags
- safe mode flags
- created timestamp

Audit records are append-only. Existing audit records must not be overwritten to make a later state look cleaner.

## Status Mapping Pattern

Status mapping should be deterministic and conservative. Example categories:

- approved future gate candidate -> ready for the next explicitly named future phase
- request revision -> needs revision
- block -> blocked
- privacy hold -> privacy hold

Status names should say what is ready in the future, not what has already happened. For example, use gate-ready wording instead of language that implies public delivery, production evidence write, or official verification.

## Decision Mapping Pattern

Decision values should be explicit and human-review oriented:

- approve for a future phase
- request revision
- block
- privacy hold
- mark weak where supported
- reject where supported

Decision values must not imply automatic analysis, report generation, export delivery, URL publication, or real-world action.

## Eligibility Policy Pattern

Eligibility functions should inspect only allowed metadata records. They should check:

- required upstream record exists
- upstream record has a ready status
- upstream audit exists where required
- privacy blockers are absent
- rejected items are excluded
- weak items remain warning-marked
- coverage limitations are acknowledged
- no unsafe fields are present in safe metadata

Eligibility should fail closed. Missing or ambiguous upstream state should produce `blocked`, `needs_revision`, or equivalent conservative status.

## Boundary Block Pattern

Boundary blocks should be explicit dictionaries of booleans. They should include all dangerous capabilities relevant to the phase and keep them false unless a separately approved runtime implements the capability.

Examples:

- run_analysis_now: false
- generate_report_now: false
- write_evidence_layer_now: false
- create_production_case_now: false
- return_file_bytes_now: false
- create_download_route_now: false
- generate_public_url_now: false
- generate_signed_url_now: false
- external_delivery_now: false
- upload_object_storage_now: false
- publish_portal_now: false
- call_real_api_now: false
- call_real_llm_now: false

## No-Side-Effect Flags

Every gate that precedes a potentially side-effecting future runtime should write audit-visible no-side-effect flags. This makes the absence of side effects inspectable later.

The no-side-effect flags should be recorded in both the gate record and audit record when useful.

## Append-Only Audit Behavior

Audit creation should happen in the same local transaction pattern as record creation where possible:

1. validate payload
2. validate upstream records
3. build gate record
4. build audit record
5. write gate record
6. write audit record

If a future phase needs stronger atomicity, it should use a local temp-file-then-rename pattern, not a remote service.

## Runtime Ignored Path Policy

Runtime records should remain under ignored local runtime folders. Refactoring should not expose absolute filesystem paths in API responses or UI.

Use safe labels:

- request ID
- record ID
- runtime-relative category
- safe root label

Avoid:

- absolute paths
- drive names
- user profile paths
- browser profile paths
- collector profile paths

## Redacted Metadata Policy

Safe metadata may include IDs, statuses, counts, source names, safe timestamps, and validation summaries.

Safe metadata must not include:

- secret values
- token values
- cookie values
- session values
- salts
- password-like values
- raw author identifiers
- profile URLs
- private messages
- original package rows
- export artifact file content
- file bytes

## Provider Output Is Evidence, Not Truth

Provider output, collector output, vendor output, and manually imported output are evidence inputs. They are not official truth. Trust, review, dedup, audit, and coverage limitations must remain visible through all downstream gates.

## Downstream Gate Separation

Each downstream capability needs its own explicit gate. Passing one gate does not imply the next action has occurred.

Examples:

- Dedup preview does not mean analysis-ready.
- Promotion gate does not run analysis.
- Manual analysis trigger does not create final reports.
- Summary report candidate does not mean final report.
- Export artifact does not mean public delivery.
- Public-access / external-delivery gate does not create public access or external delivery.

## Forbidden Shared Abstraction Shortcut

Do not create a generic helper that silently relaxes phase-specific boundaries. Shared helpers should make phase-specific validators easier to call, not replace them with broad permissive defaults.

