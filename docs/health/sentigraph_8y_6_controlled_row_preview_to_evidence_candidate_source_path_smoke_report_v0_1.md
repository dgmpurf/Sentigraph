# Sentigraph 8Y-6 Controlled Row Preview to Evidence Candidate Source Path Smoke Report v0.1

## Decision

```text
phase = 8Y-6
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
source_path_step = row_preview_to_evidence_candidate
evidence_candidate_created = yes
evidence_candidate_schema = sentigraph_controlled_evidence_candidate_set_v0_1
evidence_candidate_mode = backend_only_local_preview_derived_evidence_candidate
source_preview_schema = sentigraph_controlled_row_preview_v0_1
import_candidate_created = no
evidence_layer_import_candidate_created = no
evidence_layer_write = no
production_evidence_item_created = no
production_case_created = no
production_analysis_run_created = no
review_queue_runtime_used = no
source11_runtime_called = no
actual_final_summary_report_created = no
b_end_report_runtime_generated = no
sandbox_public_event_runtime_generated = no
export_download_public_delivery_created = no
generated_response_text = no
route_changed = no
frontend_changed = no
runtime_changed = no
raw_rows_exposed = no
raw_comments_exposed = no
raw_identities_exposed = no
author_names_or_profile_urls_exposed = no
secrets_read = no
human_review_required = yes
no_automatic_trust_upgrade = yes
old_direct_import_phrase_accepted = no
future_next_boundary_recommendation = review_only_or_review_queue_candidate_gate_docs_only_not_implementation
```

## What Was Proven

8Y-6 adds a focused backend-only smoke test proving this source path:

```text
controlled row preview
-> controlled evidence candidate helper
-> local controlled evidence candidate object
```

The smoke uses the existing controlled row preview output and the existing controlled evidence candidate helper. It does not create an import candidate, Evidence Layer record, production EvidenceItem, production case, production analysis run, Review Queue item, route, frontend state, runtime artifact, report, Sandbox output, public event output, export output, download output, public access output, or final delivery output.

## Approval Phrase Checks

The 8Y-6 smoke requires this exact approval phrase before constructing the row preview source path:

```text
APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE
```

The old direct-import phrase is rejected and remains inactive:

```text
APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE
```

The downstream evidence candidate helper still requires its existing controlled helper phrase:

```text
批准 8W-10 Controlled Evidence Candidate Helper Implementation
```

The mojibake form is used only as a negative assertion in tests and is not accepted.

## Boundary Summary

This phase is source-path smoke only. It remains local-only, metadata/safe-preview only, and candidate-only. The candidate object keeps `human_review_required = yes` and `no_automatic_trust_upgrade = yes`.

The smoke asserts that unsafe source preview flags block before evidence candidate creation, including raw rows, raw comments, raw identities, profile URL exposure, Evidence Layer write, production EvidenceItem creation, production case creation, production analysis run creation, and row/runtime parsing side effects.

Provider output and preview-derived evidence candidates remain evidence inputs, not truth, not official verification, not causal proof, not prediction, and not a production score.

## Validation

```text
python -m pytest backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py -q
result = pass

python -m pytest backend/app/tests/test_controlled_row_preview.py backend/app/tests/test_controlled_evidence_candidate.py -q
result = pass

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py -q
result = pass
```

Service files were not changed, so service `py_compile` was not required.

## Not Run

Full backend pytest, frontend build, browser smoke, provider jobs, collector jobs, route/API smoke, and runtime checks were not run because this phase is a focused backend-only source-path smoke with no service, route, frontend, runtime, provider, or collector changes.

## Next Recommendation

The next step should remain conservative: a review-only or Review Queue candidate gate docs-only decision, not implementation and not Evidence Layer write.
