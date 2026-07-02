# Sentigraph 8W-6 Controlled Row Preview Gate Decision v0.1

## A. Decision / Status

phase = 8W-6

task = controlled_row_preview_gate_decision

decision = ready

selected_next_boundary_option = ready_for_8W_7_controlled_row_preview_implementation_after_explicit_approval

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_code_changed = no

tests_changed = no

route_changed = no

api_route_added = no

runtime_changed = no

row_preview_gate_decision_created = yes

row_preview_implementation_approved = no

row_preview_executed = no

future_8w7_implementation_candidate_selected = yes

future_8w7_exact_approval_phrase_required = yes

future_row_source_policy_defined = yes

future_row_count_limit_defined = yes

future_redaction_policy_defined = yes

evidence_items_jsonl_parsed = no

evidence_items_csv_parsed = no

source_manifest_rows_parsed = no

collection_log_rows_parsed = no

original_package_rows_read = no

raw_comments_read = no

raw_identities_read = no

private_collector_inspected = no

private_collector_source_inspected = no

real_exchange_dir_read = no

review_queue_item_created = no

production_review_queue_item_created = no

evidence_items_created = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

b_end_report_runtime_generated = no

sandbox_public_event_generated = no

generated_response_text = no

public_route_created = no

frontend_integration_approved = no

download_package_runtime_used = no

public_access_runtime_used = no

external_delivery_runtime_used = no

final_delivery_runtime_used = no

source_files_created = no

docs_project_sources_created = no

approved_package_name = donglu-sunjihai-youth-football-202606-v2_20260617_121016

approved_package_role = candidate_demo_sample

approved_case_id_hint = donglu_sunjihai_youth_football_202606

8w4_boundary_status = review_only_staging_boundary_ready_for_manual_review

8w4_warning_count = 1

human_review_required = yes

source24_patch_recommended = consider_after_8W_6_commit

source11_update_recommended = no

8W-6 decision:

`eligible_for_future_controlled_row_preview_implementation_after_exact_approval`

This eligibility is narrow. It does not approve row preview now. It only means a future 8W-7 implementation can be considered if the user provides the exact 8W-7 approval phrase and if the implementation follows the contract below.

## B. Current 8W Source Boundary

The current chain is:

8W-2 safe metadata-smoke object -> 8W-4 local review-only staging boundary marker -> 8W-5 docs-only row preview gate decision -> 8W-6 controlled row preview gate decision.

The approved package identity remains:

- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`

8W-6 does not broaden the package target, add a selector, read row files, inspect private collector source, or read real exchange directories.

## C. 8W-4 Boundary Marker Eligibility Assessment

Eligibility assessment:

`eligible_for_future_controlled_row_preview_implementation_after_exact_approval`

The 8W-4 boundary marker is eligible as a future 8W-7 source because:

- it has schema `sentigraph_metadata_smoke_review_only_staging_boundary_v0_1`
- it has boundary status `review_only_staging_boundary_ready_for_manual_review`
- it preserves the exact approved package identity
- it preserves `metadata_only = true`
- it preserves `warning_count = 1`
- it preserves `human_review_required = true`
- it preserves `warning_manual_review_preserved = true`
- it keeps `row_preview_approved = false`
- it keeps Evidence Layer write, production case, and production `analysis_run` false
- it keeps frontend/route/API false
- it records that no row files were parsed and no private collector source was inspected

Eligibility does not mean rows can be opened now. It means a later exact approval could authorize a tightly bounded implementation.

## D. Warning/manual-review Preservation

The warning/manual-review state remains active:

- `warning_count = 1`
- `human_review_required = true`
- `warning_manual_review_preserved = true`

Future 8W-7 must carry those fields forward into any preview output. The warning must not be treated as evidence verification, trust upgrade, production readiness, analysis readiness, report readiness, public readiness, or customer delivery readiness.

## E. Selected Next Boundary Option

Selected option:

`ready_for_8W_7_controlled_row_preview_implementation_after_explicit_approval`

Rationale:

The contract below defines strict row minimization, redaction, blocker categories, exact target identity, row count limits, and no-production side-effect boundaries. Therefore, future 8W-7 may implement a controlled backend-only redacted row preview helper only after exact approval.

Options not selected:

- `warning_review_required_before_8W_7`: not selected because warning/manual-review state is already explicitly preserved and must remain active in 8W-7.
- `keep_as_metadata_review_only_boundary_checkpoint_no_row_preview_implementation`: not selected because a minimal redacted future preview can be considered under a strict gate.
- `pause`: not selected because 8W-6 remains docs-only and no row content is opened.

## F. Row Preview Gate vs Row Preview Implementation

8W-6 is a row preview gate decision. It defines a possible future implementation boundary.

8W-6 does not:

- implement row preview
- open `evidence_items.jsonl`
- open `evidence_items.csv`
- parse any evidence row
- create preview rows
- create tests
- create backend helpers
- write Evidence Layer
- create production case
- create production `analysis_run`
- add route/frontend/API

Future 8W-7 implementation would be the first phase where a controlled helper may open one explicitly approved row source and emit a small redacted preview. That is not approved until the exact 8W-7 approval phrase is provided.

## G. Future 8W-7 Exact Approval Phrase

Future row preview implementation must require exactly:

`批准 8W-7 Controlled Row Preview Implementation`

Without this exact phrase:

- do not implement row preview
- do not open `evidence_items.jsonl` or `evidence_items.csv`
- do not parse rows
- do not create preview rows
- do not add tests
- do not create backend helper
- do not write Evidence Layer
- do not create production case
- do not create production `analysis_run`
- do not touch frontend/routes

## H. Future 8W-7 Source Object Contract

Future 8W-7 source must be only the 8W-4 safe local review-only staging boundary marker.

Required source fields:

- schema: `sentigraph_metadata_smoke_review_only_staging_boundary_v0_1`
- phase: `8W-4`
- boundary_status: `review_only_staging_boundary_ready_for_manual_review`
- package_name: `donglu-sunjihai-youth-football-202606-v2_20260617_121016`
- package_role: `candidate_demo_sample`
- case_id_hint: `donglu_sunjihai_youth_football_202606`
- metadata_only: `true`
- warning_count: `1`
- human_review_required: `true`
- warning_manual_review_preserved: `true`
- row_preview_approved: `false` before implementation starts
- Evidence Layer write: `false`
- production case: `false`
- production `analysis_run`: `false`

Future 8W-7 must not accept arbitrary path, package name, directory, file path, URL, env root, collector output root, or user-provided filesystem path.

## I. Future Row Source Policy

Future 8W-7 may use only one explicitly approved row source under the already approved package target.

Recommended first-slice source:

`evidence_items.jsonl`

Alternative source:

`evidence_items.csv`, only if the future approval explicitly names CSV.

Future 8W-7 must not parse both row files unless a later gate explicitly approves dual-source comparison.

Future 8W-7 must not parse:

- `source_manifest.jsonl` rows
- `collection_log.jsonl` rows
- original raw package rows outside the approved evidence row file
- private collector raw output

## J. Future Row Count Limit

Recommended future first-slice limit:

`max_preview_rows = 5`

Hard upper bound unless a later gate changes it:

`max_preview_rows <= 10`

The limit must be enforced before preview output is emitted. If implementation cannot prove the bound, it must block.

## K. Future Redacted Preview Field Policy

Future redacted preview rows may include only minimized safe fields:

- `preview_row_id`, generated local safe ID
- `row_index`, bounded integer
- `evidence_id` or `evidence_id_hash` if safe
- `evidence_type`
- `platform`
- `created_at_date` or coarse `created_at` if safe
- `trust_label`
- `verification_status`
- `review_status`
- `language`
- `content_visibility` or `access_scope` if safe
- `text_snippet_redacted`, capped length
- `redaction_status`
- `redaction_warnings`
- `row_boundary_flags`

Future preview rows must not include:

- `raw_author_id`
- `author_id`
- `author_name`
- `username`
- `display_name`
- actual `profile_url` value
- raw profile URL
- private messages
- email, phone, address, or identity fields
- cookies, tokens, sessions, passwords, API keys, or secrets
- browser profile paths
- absolute filesystem paths
- package paths
- raw collector paths
- unbounded raw comments
- generated response text
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`

## L. Future Text Snippet Policy

Future snippets must be:

- redacted
- capped, recommended maximum `160` characters
- preview-only
- human-review-only
- not used for production scoring
- not used for public output
- not used for B-end report runtime
- not used for Sandbox/public event runtime

If a row contains private messages, minors/family sensitive details, secrets, raw identifiers, actual profile URLs, doxxing risks, or harassment risks, the row must be skipped or blocked, not emitted.

## M. Future Blocker Categories

Future 8W-7 must block if:

- exact approval phrase is missing
- package identity mismatches
- row source is not explicitly approved
- row file is missing
- row file path would require directory traversal
- evidence row file parse is broader than the max row limit
- redaction policy is missing
- raw author ID exposure risk exists
- author name exposure risk exists
- actual profile URL exposure risk exists
- raw comment overexposure risk exists
- private message risk exists
- minors/family sensitive personal detail risk exists
- cookie/session/token/API key/password/secret risk exists
- browser profile path risk exists
- absolute path or package path exposure risk exists
- private collector source inspection is requested
- real exchange directory traversal is requested
- Evidence Layer write is requested
- production case or production `analysis_run` is requested
- review queue runtime is requested
- frontend/route/API is requested
- B-end report or Sandbox/public event is requested
- report/export/download/public/final-delivery runtime is requested
- public/customer output is requested
- generated response text is requested
- publish/send/post/execute/auto-execute is requested
- real API, real LLM, provider, or collector execution is requested
- URL fetch or scrape is requested

Blocked output must use safe reason codes only and must not echo forbidden values.

## N. Future Test Requirements

Future 8W-7 tests should include:

- exact package identity accepted
- wrong package blocks
- missing exact approval context blocks
- row file opening limited to the explicitly approved file
- `max_preview_rows` enforced
- `evidence_items.csv` not opened if JSONL is selected
- `source_manifest.jsonl` not parsed
- `collection_log.jsonl` not parsed
- private collector source not accessed
- real exchange directory not traversed
- raw author ID/name/profile URL sentinels redacted or blocked
- secret/token/cookie sentinels blocked
- absolute path/package path not emitted
- text snippets capped
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no route/frontend
- no B-end/Sandbox/public output
- no generated response text
- all runtime side-effect flags false

## O. Explicit Non-approvals

8W-6 explicitly does not approve:

- row preview implementation now
- row file opening now
- evidence row parsing now
- preview row creation now
- backend helper creation now
- test creation now
- route/API additions
- frontend code changes
- review queue runtime
- production review queue item creation
- EvidenceItem creation
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- B-end report runtime
- Sandbox/public event runtime
- report/export/download/public/final-delivery runtime
- public URL creation
- signed URL creation
- file-byte route
- object storage upload
- email sending
- portal publication
- generated response text
- publish, send, post, execute, or auto-execute behavior
- real API calls
- real LLM calls
- provider jobs
- collector jobs
- URL fetch
- scrape
- private collector source inspection
- real exchange directory read
- Project Source file creation
- `docs/project_sources/` creation

## P. Relationship to Source 11 / Evidence Layer

8W-6 does not change Source 11 behavior.

8W-6 does not write Evidence Layer, create EvidenceItems, create production review queue items, create a production case, create a production `analysis_run`, run production dedup, run analysis, generate reports, generate Sandbox fixtures, or generate public event pages.

Source 11 should remain unchanged because Analysis Request / Provider / Import Governance runtime behavior did not change in this docs-only checkpoint.

## Q. Relationship to Private Collector / Exchange Dirs

8W-6 does not change private collector behavior.

Sentigraph must not:

- inspect private collector source
- run collector jobs
- run provider jobs
- access collector sessions, cookies, tokens, profiles, browser state, or secrets
- read real exchange directories
- access external collector export roots
- parse exported row files
- use env-provided real paths

Future 8W-7, if approved, must not accept arbitrary private collector paths, external export roots, env roots, or user-provided filesystem paths.

## R. Validation / Not Run

Validation for this docs-only phase:

- `git status --short`
- `git branch --show-current`
- `git rev-parse HEAD`
- `git diff --check`
- static safety scan of the two new docs

Not run:

- pytest
- frontend build
- browser smoke
- collector
- real APIs
- real LLMs
- provider jobs
- URL fetch
- scrape
- private collector source inspection
- real exchange directory read
- evidence row parsing
- row preview
- Evidence Layer write
- production case / production `analysis_run`
- B-end report / Sandbox/public event / report/export/download/public/final-delivery runtime smoke
- route/frontend smoke

Reason:

8W-6 is docs-only and explicitly forbids runtime behavior.

## S. Issues P0/P1/P2/P3

- P0: none.
- P1: none.
- P2: future 8W-7 must require the exact approval phrase and must remain backend-only, bounded, redacted, and preview-only.
- P3: consider ChatGPT-side Source 24 patch after commit.

## T. Recommended Next Step

Recommended next task:

Phase 8W-7 Controlled Row Preview Implementation, only after the exact approval phrase:

`批准 8W-7 Controlled Row Preview Implementation`

Do not proceed to row preview implementation without that phrase.

## U. Source Maintenance Recommendation

After commit:

- consider ChatGPT-side Source 24 or equivalent project-context patch for 8W-6
- do not update Source 11
- do not create Project Source files inside this repository
- do not create `docs/project_sources/`
