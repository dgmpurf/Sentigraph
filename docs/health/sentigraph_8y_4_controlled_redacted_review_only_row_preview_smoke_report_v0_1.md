# Sentigraph 8Y-4 Controlled Redacted Review-only Row Preview Smoke Report v0.1

## Decision

- phase: 8Y-4
- decision: ready
- privacy_issue_stop: no
- backend_only: yes
- test_first: yes
- controlled_smoke: yes
- review_only: yes
- redacted_preview_only: yes
- row_preview_created: yes
- approved_row_source: evidence_items.jsonl
- evidence_items_jsonl_opened: yes only in approved controlled path
- evidence_items_jsonl_parsed: yes only in approved controlled path
- evidence_items_csv_opened: no
- evidence_items_csv_parsed: no
- source_manifest_rows_parsed: no
- collection_log_rows_parsed: no
- original_package_rows_read: no
- real_exchange_dir_read: no
- arbitrary_package_dir_read: no
- raw_rows_exposed: no
- raw_comments_exposed: no
- raw_identities_exposed: no
- author_names_or_profile_urls_exposed: no
- secrets_read: no
- evidence_layer_write: no
- production_evidence_item_created: no
- production_case_created: no
- production_analysis_run_created: no
- review_queue_runtime_used: no
- source11_runtime_called: no
- actual_final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- export_download_public_delivery_created: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- future_next_boundary_recommendation: Evidence Layer import gate docs-only, not implementation
- recommended_tag: no

## Scope

8Y-4 is a focused backend-only controlled smoke. It reuses the existing `controlled_row_preview` helper and does not change the helper implementation.

The approved helper phrase remains:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

The 8Y-4 task approval phrase was:

`APPROVE_8Y_4_CONTROLLED_REDACTED_REVIEW_ONLY_ROW_PREVIEW_SMOKE`

8Y-4 proves that the repaired helper can create a bounded, redacted, review-only row preview inside the controlled backend test path.

## Controlled Row Preview Proof

The new smoke test verifies:

- output schema is `sentigraph_controlled_row_preview_v0_1`
- `created_local_row_preview = true` only in the approved controlled path
- output is preview-only
- approved row source is `evidence_items.jsonl`
- row source policy is `single_approved_jsonl_source_only`
- `opened_approved_evidence_items_jsonl = true` only in the approved controlled path
- `parsed_evidence_items_jsonl = true` only in the approved controlled path
- `parsed_evidence_items_csv = false`
- `parsed_source_manifest_jsonl_rows = false`
- `parsed_collection_log_jsonl_rows = false`
- `read_original_package_rows = false`
- `read_real_exchange_dir = false`
- `accessed_private_collector = false`
- `inspected_private_collector_source = false`

## Bounded Preview Proof

The smoke verifies:

- `max_preview_rows_applied = 5`
- hard row bound remains `10`
- `preview_rows_count <= max_preview_rows_applied`
- `rows_inspected_count <= max_preview_rows_hard_bound`
- `row_limit_enforced = true`
- redaction policy version is explicit
- `human_review_required = true`
- warning/manual-review state is preserved

## Approval Phrase Safety Proof

The smoke verifies:

- canonical 8W-7 phrase is accepted
- missing phrase is rejected before row source open
- wrong phrase is rejected before row source open
- old Chinese phrase is rejected before row source open
- old garbled phrase is rejected before row source open
- wrong/missing/old phrase cases monkeypatch `Path.open` and `Path.read_text`, so any row-source access would fail the test
- blocked output keeps preview rows empty and row-source side-effect flags false

## Redaction And Minimization Proof

The smoke verifies preview rows expose only allowed minimized fields:

- preview row id
- row index
- evidence id hash
- evidence type
- platform
- coarse created date
- trust label
- verification status
- review status
- language
- content visibility
- access scope
- redacted text snippet
- redaction status and warnings
- row boundary flags

The smoke verifies no raw rows, raw comments, raw identities, raw author ids, raw author names, actual profile URLs, actual author names, source URLs, secrets, cookies, tokens, sessions, browser profile paths, or private paths appear in output.

## Production Side-effect Proof

The smoke verifies all production/public/action side effects remain false:

- Evidence Layer write
- EvidenceItem creation
- production EvidenceItem creation
- production case creation
- production analysis_run creation
- Review Queue runtime
- production review queue item creation
- generated response text
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- route/API/frontend readiness
- real API / real LLM / provider / collector execution
- URL fetching / scraping
- publish/send/post/execute/auto-execute behavior

## Validation Results

8Y-4 focused smoke:

- command: `python -m pytest backend/app/tests/test_8y_4_controlled_redacted_review_only_row_preview_smoke.py -q`
- result: passed, 6 tests

Existing row-preview tests:

- command: `python -m pytest backend/app/tests/test_controlled_row_preview.py -q`
- result: passed, 51 tests

Nearby safety tests:

- command: `python -m pytest backend/app/tests/test_controlled_evidence_candidate.py backend/app/tests/test_analysis_request_golden_contracts.py -q`
- result: passed, 66 tests

Compile:

- not run
- reason: `backend/app/services/controlled_row_preview.py` was not modified in 8Y-4

## Not Run

Not run:

- full pytest
- frontend build
- browser smoke
- collector
- real API/LLM/network
- URL fetching
- scraping

Reason:

8Y-4 is a focused backend-only controlled smoke with focused tests only.

## Next Boundary Recommendation

Recommended next task:

Evidence Layer import gate docs-only, not implementation.

Do not proceed directly to Evidence Layer write, production EvidenceItem creation, production case creation, production analysis_run creation, Review Queue runtime, route/API/frontend, Source 11 runtime, actual FinalSummaryReport runtime, B-end report runtime, Sandbox/public event runtime, export/download/public/final-delivery runtime, real API, real LLM, provider execution, or collector execution.

