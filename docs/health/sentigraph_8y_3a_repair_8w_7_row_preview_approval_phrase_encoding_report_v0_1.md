# Sentigraph 8Y-3A Repair 8W-7 Row-preview Approval Phrase Encoding Report v0.1

## Decision

- phase: 8Y-3A
- decision: ready
- privacy_issue_stop: no
- backend_safety_repair: yes
- minimal_implementation: yes
- focused_tests_only: yes
- canonical_repaired_phrase: APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION
- mojibake_phrase_accepted: false
- mojibake_phrase_rejected_before_row_open: true
- missing_or_wrong_phrase_rejected_before_row_open: true
- row_preview_capability_expanded: no
- real_exchange_dir_read: no
- real_package_rows_read: no
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
- source_files_created: no
- docs_project_sources_created: no
- future_8Y_4_status: still_inactive / requires separate approval
- recommended_tag: no

## Repair Summary

8Y-3A repairs the 8W-7 controlled row-preview exact approval phrase.

Canonical repaired phrase:

`APPROVE_8W_7_CONTROLLED_ROW_PREVIEW_IMPLEMENTATION`

The old mojibake phrase is superseded and must be rejected:

`鎵瑰噯 8W-7 Controlled Row Preview Implementation`

The earlier Chinese phrase is also no longer accepted:

`批准 8W-7 Controlled Row Preview Implementation`

ASCII is used to avoid future Windows codepage or UTF-8 ambiguity.

## Files Changed

- `backend/app/services/controlled_row_preview.py`
- `backend/app/tests/test_controlled_row_preview.py`
- `docs/health/sentigraph_8w_7_controlled_row_preview_implementation_report_v0_1.md`
- `docs/health/sentigraph_8y_3a_repair_8w_7_row_preview_approval_phrase_encoding_report_v0_1.md`

## Scope

This repair does not add row-preview capability. It only changes the approval phrase and test expectations for the existing controlled helper.

The existing controlled row-preview helper remains:

- backend-only
- bounded
- redacted
- review-only
- local controlled path only
- no route/API
- no frontend
- no runtime persistence
- no Evidence Layer write
- no production EvidenceItem
- no production case
- no production analysis_run
- no Review Queue runtime
- no Source 11 runtime
- no actual FinalSummaryReport runtime

## Proof Requirements

The focused test file proves:

- canonical ASCII phrase is accepted in the existing bounded controlled preview path
- missing phrase is rejected before row source open
- wrong phrase is rejected before row source open
- old Chinese phrase is rejected before row source open
- old mojibake phrase is rejected before row source open
- rejection guards patch `Path.open` and `Path.read_text` so a row-source access would fail the test
- bounded row limit still applies
- redaction still applies
- raw rows are not exposed
- raw comments are not exposed
- raw identities are not exposed
- actual author names/profile URLs are not exposed
- Evidence Layer write remains false
- production EvidenceItem creation remains false
- production case creation remains false
- production analysis_run creation remains false
- Review Queue runtime remains false
- Source 11 runtime remains false
- actual FinalSummaryReport runtime remains false

## 8Y-4 Status

8Y-3A does not proceed to 8Y-4.

Future 8Y-4 remains inactive and requires a separate approval phrase and separate task. This repair only removes the encoding blocker identified by 8Y-3.

## Not Implemented

8Y-3A does not implement:

- new row-preview capability
- broader row access
- arbitrary package directory reads
- real exchange directory reads
- private collector source inspection
- collector jobs
- provider jobs
- real APIs
- real LLMs
- URL fetching
- scraping
- raw row/comment/identity exposure
- actual author name/profile URL exposure
- Evidence Layer write
- production EvidenceItem creation
- production case creation
- production analysis_run creation
- Review Queue runtime
- route/API/frontend changes
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime

## Validation Results

Focused row-preview tests:

- `python -m pytest backend/app/tests/test_controlled_row_preview.py -q`
- result: passed, 51 tests

Nearby tests:

- `python -m pytest backend/app/tests/test_controlled_evidence_candidate.py backend/app/tests/test_analysis_request_golden_contracts.py -q`
- result: passed, 66 tests

Compile:

- `python -m py_compile backend/app/services/controlled_row_preview.py`
- result: passed

Diff/status:

- `git diff --check`
- result: passed with Git line-ending warnings only
- `git status --short`
- result: allowed changed files only

Static phrase and scope scan:

- static phrase and scope scan on changed files
- result: canonical ASCII phrase appears in helper/tests/report; old mojibake appears only in superseded/rejected documentation context; old Chinese phrase appears only in negative-test or superseded documentation context

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

8Y-3A is a focused backend safety repair with focused tests only.
