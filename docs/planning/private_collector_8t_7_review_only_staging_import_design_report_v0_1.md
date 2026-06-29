# Private Collector 8T-7 Review-only Staging Import Design Report v0.1

## A. Decision / Status

```text
phase = 8T-7
task = review_only_staging_import_design
privacy_issue_stop = no
code_changed = no
docs_only = yes
collector_run = no
live_crawl = no
real_api_called = no
real_llm_called = no
full_evidence_rows_read = no
evidence_layer_write = no
production_case_created = no
analysis_run_created = no
project_source_changed = no
api_route_added = no
frontend_changed = no
```

Decision: ready.

## B. What Previous 8T Phases Proved

8T-3 resolver:

- metadata-only package resolver exists.
- package name resolution and explicit relative package path resolution are defined.
- path traversal and path escape are blocked.
- required package files are checked by existence only.
- evidence rows are not parsed.

8T-4 provider result reader:

- provider result metadata can be validated.
- package references can be validated.
- package resolver results propagate safely.
- forbidden actual metadata fields block privacy issues.

8T-5 local exchange fixture smoke:

- provider result JSON fixture can flow through reader and resolver.
- safe metadata-only handoff summary can be produced.
- no Evidence Layer write, production case, or `analysis_run` occurs.

8T-6 Search-to-Case product contract:

- Search-to-Case is defined as `search query -> governed case workspace candidate`.
- Search does not directly create production cases.
- Search must pass through gated metadata, staging, review, dedup, promotion, and workspace gates.

## C. Staging Design Decisions

Review-only staging design decisions:

- metadata-only handoff can become a review-only staging candidate.
- review-only staging is not production import.
- review-only staging is not Evidence Layer.
- review-only staging is not production case.
- review-only staging is not `analysis_run`.
- review-only staging is not report/public output.
- review-only staging does not parse evidence rows.
- review-only staging does not expose raw comments, raw identities, secrets, or absolute private paths.

## D. Contract Objects

The design defines four future objects:

- `review_only_staging_import_request_v0_1`
- `review_only_staging_candidate_v0_1`
- `review_only_staging_gate_result_v0_1`
- `review_only_staging_audit_record_v0_1`

Together, these objects separate the request to stage, the staged candidate metadata, the gate result, and the append-only audit record.

## E. Allowed and Blocked Transitions

Allowed transitions:

```text
provider_result_metadata_received -> package_reference_ready
package_reference_ready -> metadata_validation_passed
metadata_validation_passed -> staging_request_drafted
staging_request_drafted -> staging_metadata_validating
staging_metadata_validating -> staging_candidate_created
staging_candidate_created -> ready_for_human_review
ready_for_human_review -> future evidence review gate
```

Blocked transitions:

- `staging_candidate_created -> Evidence Layer write`
- `staging_candidate_created -> production case`
- `staging_candidate_created -> analysis_run`
- `staging_candidate_created -> B-end report runtime`
- `staging_candidate_created -> Sandbox/public event runtime`
- `staging_candidate_created -> public response`
- `staging_candidate_created -> publish/send/post/execute`
- `ready_for_human_review -> production import` without future explicit gate
- `metadata_validation_warn -> staging_candidate_created` without manual review

## F. Operator Boundary

An operator may:

- continue review
- request more metadata
- mark `manual_review_required`
- reject package
- block privacy issue
- request future evidence preview gate
- request future dedup gate
- request future promotion gate

An operator may not:

- approve production evidence
- create production case
- start `analysis_run`
- generate report
- generate public event
- publish / send / post / execute
- generate response text
- target individuals
- treat metadata as verified truth
- claim official confirmation or causal proof

## G. Safety / Privacy Policy

Blockers:

- full evidence rows in metadata stage
- raw comment dumps
- raw author ids
- raw author names
- profile URLs as actual exported values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profile paths
- absolute private package paths exposed to UI/API
- generated public response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- live collection without authorization
- unsupported platform
- path escape
- missing package

## H. Recommended Next Step

Recommend Phase 8T-8 tiny review-only staging metadata helper + targeted tests.

The helper should use safe summaries from the 8T-5 smoke and create only an in-memory or `tmp_path` fixture staging candidate in tests.

Do not recommend production import.

Do not recommend UI yet.

## I. Source Update Policy

No immediate Project Source update.

Batch later after review-only staging helper implementation or milestone-level state change.

## J. Safety Confirmations

- docs-only
- no code changed
- no collector run
- no live crawl
- no browser automation
- no real API
- no real LLM
- no URL fetch/scrape
- no full evidence rows parsed
- no `evidence_items.jsonl` parsed
- no `evidence_items.csv` parsed
- no raw comments printed
- no raw author ids/names printed
- no cookies/tokens/sessions/profile paths read
- no Evidence Layer write
- no production case / analysis_run
- no B-end report runtime
- no Sandbox/public event runtime
- no frontend/API route added
- no Project Source change
- no GitHub Actions workflow recreated
