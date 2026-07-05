# Sentigraph 8Y-8 Controlled Evidence Candidate to Review Queue Candidate Smoke Report v0.1

## Decision

```text
phase = 8Y-8
decision = ready
privacy_issue_stop = no
backend_only = yes
test_first = yes
controlled_smoke = yes
source_path_step = evidence_candidate_to_review_queue_candidate
review_queue_candidate_created = yes
review_queue_candidate_schema = sentigraph_controlled_review_queue_candidate_set_v0_1
review_queue_candidate_mode = backend_only_local_review_queue_candidate_boundary
source_candidate_set_schema = sentigraph_controlled_evidence_candidate_set_v0_1
actual_review_queue_runtime_used = no
production_review_queue_item_created = no
review_queue_item_created = no
evidence_layer_import_candidate_created = no
import_candidate_created = no
evidence_layer_write = no
production_evidence_item_created = no
production_case_created = no
production_analysis_run_created = no
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
future_next_boundary_recommendation = Evidence Layer import candidate gate docs-only, not implementation
```

## What Was Proven

8Y-8 adds a focused backend-only smoke test proving this source path:

```text
existing controlled evidence candidate object
-> existing controlled review queue candidate helper
-> local controlled review-only / review queue candidate object
```

The smoke uses the existing controlled helper-shaped candidate path. It creates a review queue candidate object only inside the controlled backend test path.

## Source Path Proof

The smoke builds a safe upstream candidate source using existing local helpers:

```text
controlled row preview
-> controlled evidence candidate helper
-> controlled evidence candidate set
```

Then it feeds that controlled evidence candidate set into:

```text
backend/app/services/controlled_review_queue_candidate.py
```

The resulting object remains:

```text
review_queue_candidate_set_schema = sentigraph_controlled_review_queue_candidate_set_v0_1
review_queue_candidate_mode = backend_only_local_review_queue_candidate_boundary
source_candidate_set_schema = sentigraph_controlled_evidence_candidate_set_v0_1
```

## Approval Phrase Safety

8Y-8 requires this exact phrase before the review queue candidate smoke can run:

```text
APPROVE_8Y_8_CONTROLLED_EVIDENCE_CANDIDATE_TO_REVIEW_QUEUE_CANDIDATE_SMOKE
```

The following unrelated previous phrases are rejected before review queue candidate creation:

```text
APPROVE_8Y_6_CONTROLLED_ROW_PREVIEW_TO_EVIDENCE_CANDIDATE_SOURCE_PATH_SMOKE
APPROVE_8Y_6_CONTROLLED_REDACTED_ROW_PREVIEW_EVIDENCE_LAYER_IMPORT_CANDIDATE_SMOKE
```

The downstream review queue candidate helper keeps its own exact helper phrase gate:

```text
批准 8W-13 Controlled Review Queue Candidate Helper Implementation
```

The helper phrase was checked by codepoint in the smoke test. The first two characters are `0x6279` and `0x51c6`, matching the intended Chinese characters.

## Production Side-effect Proof

The smoke monkeypatches actual Review Queue runtime, Evidence Layer import candidate, Evidence Layer write, production EvidenceItem write, report/export/public delivery, and FinalSummaryReport-related entrypoints to fail if called.

The smoke asserts all of these remain false:

```text
actual_review_queue_runtime_used
production_review_queue_item_created
review_queue_item_created
evidence_layer_import_candidate_created
import_candidate_created
evidence_layer_write
production_evidence_item_created
production_case_created
production_analysis_run_created
source11_runtime_called
actual_final_summary_report_created
b_end_report_runtime_generated
sandbox_public_event_runtime_generated
export_download_public_delivery_created
generated_response_text
route_ready
frontend_ready
production_ready
customer_ready
public_ready
raw_rows_exposed
raw_comments_exposed
raw_identities_exposed
author_names_or_profile_urls_exposed
secrets_read
```

The smoke also asserts unsafe source candidate flags block before review queue candidate creation, including raw rows, raw comments, raw identities, profile URL/name exposure, Evidence Layer write, production EvidenceItem, production case, production analysis run, import candidate, actual review queue runtime, and unsafe runtime side effects.

## Validation

```text
python -m pytest backend/app/tests/test_8y_8_controlled_evidence_candidate_to_review_queue_candidate_smoke.py -q
result = pass

python -m pytest backend/app/tests/test_8y_6_controlled_row_preview_to_evidence_candidate_source_path_smoke.py backend/app/tests/test_controlled_evidence_candidate.py backend/app/tests/test_controlled_review_queue_candidate.py -q
result = pass

python -m pytest backend/app/tests/test_controlled_row_preview.py backend/app/tests/test_analysis_request_golden_contracts.py -q
result = pass
```

Service files were not changed, so service `py_compile` was not required.

## Not Run

Full backend pytest, frontend build, browser smoke, collector jobs, real API/LLM/network checks, URL fetching, and scraping were not run because this phase is a focused backend-only controlled smoke with no route, frontend, runtime, provider, collector, or service changes.

## Next Recommendation

The next step should remain conservative: an Evidence Layer import candidate gate docs-only decision, not implementation.
