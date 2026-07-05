# Sentigraph 8Y-3 Review-only Row Preview Existing-surface Audit Gate Decision v0.1

## Decision

- phase: 8Y-3
- decision: blocked
- privacy_issue_stop: no
- docs_only: yes
- audit_only: yes
- backend_code_changed: no
- tests_changed: no
- route_changed: no
- frontend_changed: no
- runtime_changed: no
- row_preview_implemented: no
- evidence_rows_parsed: no
- real_exchange_dir_read: no
- real_package_rows_read: no
- evidence_layer_write: no
- production_evidence_item_created: no
- production_case_created: no
- production_analysis_run_created: no
- production_analysis_result_creation_authorized: no
- source11_runtime_called: no
- actual_final_summary_report_created: no
- b_end_report_runtime_generated: no
- sandbox_public_event_runtime_generated: no
- export_download_public_delivery_created: no
- source_files_created: no
- docs_project_sources_created: no
- selected_next_boundary_option: pause_or_blocked_before_controlled_redacted_review_only_row_preview_smoke
- future_8y4_exact_approval_phrase_required: no
- future_8y4_exact_approval_phrase_active: no
- source_update_recommended_after_commit: no
- source11_update_recommended: no
- recommended_tag: no

## Route C State

8Y-2 selected Route C as the preferred backend mainline: real data chain / Evidence Layer / production case / analysis_run pre-governance.

8Y-3 is C1: a docs-only review-only row preview existing-surface audit and gate decision.

C2 / future 8Y-4 is not active. This decision does not authorize row parsing, real exchange directory reads, real package row reads, Evidence Layer write, production EvidenceItem creation, production case creation, production analysis_run creation, Source 11 runtime, or actual FinalSummaryReport runtime output.

## Existing Surface Audit Summary

The repository has multiple relevant governance surfaces:

| Surface | Classification | Row interaction | Side effects | Audit note |
| --- | --- | --- | --- | --- |
| `docs/architecture/real_package_row_preview_design_v1.md` and related row-preview contracts | docs_only | redacted_preview_only as design | no_persistence | Defines row-preview boundaries and redaction intent. |
| `docs/planning/sentigraph_8w_5_review_only_staging_boundary_completion_row_preview_gate_decision_v0_1.md` | docs_only | no_row_read | no_persistence | Allows only a docs gate after 8W-4. |
| `docs/planning/sentigraph_8w_6_controlled_row_preview_gate_decision_v0_1.md` | docs_only | no_row_read | no_persistence | Defines controlled row-preview implementation prerequisites. |
| `docs/health/sentigraph_8w_7_controlled_row_preview_implementation_report_v0_1.md` | docs_only health report | redacted_preview_only as reported | runtime_local_only as reported | Health report should be treated as stale until approval phrase encoding is repaired and revalidated. |
| `backend/app/services/metadata_smoke_review_only_staging_boundary.py` | backend_helper | no_row_read | no_persistence | Builds metadata-only 8W-4 boundary and blocks row preview, Evidence Layer write, production case, production analysis_run, route/frontend, and delivery actions. |
| `backend/app/services/private_collector_review_only_staging.py` | backend_helper | no_row_read | no_persistence | Creates in-memory review-only staging candidates from metadata handoff; rejects forbidden actual fields. |
| `backend/app/api/v1/routes/internal_operator_review_only_staging.py` | route | synthetic_fixture_only | no_persistence | Disabled by default; enabled mode returns synthetic safe fixture summaries only. |
| `backend/app/tests/test_internal_operator_review_only_staging_routes.py` | test_only | synthetic_fixture_only | no_persistence | Tests disabled default, safe synthetic response, no file stream/ZIP/delivery behavior, and no row file opening in disabled mode. |
| `backend/app/services/controlled_row_preview.py` | backend_helper | real_row_read_possible in approved controlled path | runtime_local_only | Existing helper reads one approved local row source and emits redacted preview rows, but the current approval phrase is encoded incorrectly. |
| `backend/app/tests/test_controlled_row_preview.py` | test_only | real_row_read_possible in approved controlled path | runtime_local_only | Tests bounded preview, redaction, row source guard, and side-effect blockers, but currently treats the mojibake phrase as the expected phrase. |
| `backend/app/services/controlled_evidence_candidate.py` and downstream 8W helpers | backend_helper | consumes controlled row preview output | runtime_local_only | These are downstream candidate helpers; they depend on a safe row-preview source. They do not make 8Y-4 safe while the row-preview gate phrase is wrong. |
| 8X handoff health/docs chain | docs_only/test_only/backend_helper | metadata/synthetic fixture only | runtime_local_only | Proves controlled handoff patterns, but does not override the row-preview approval issue. |

## Key Finding

The audit found enough design and helper surface to describe a future controlled redacted review-only row preview smoke, but not enough to proceed now.

The blocking issue is in the existing 8W-7 row-preview surface:

- `backend/app/services/controlled_row_preview.py` currently defines `APPROVAL_PHRASE` with mojibake text: `鎵瑰噯 8W-7 Controlled Row Preview Implementation`.
- `backend/app/tests/test_controlled_row_preview.py` currently sets the same mojibake text as the expected phrase.
- This means the existing exact-phrase safety gate is not trustworthy enough to use as a precedent for 8Y-4.

This is not marked as a privacy issue in 8Y-3 because the audit did not execute row preview, did not read package rows, and did not expose raw values. It is a governance blocker for any future controlled row-preview smoke.

## Gaps And Blockers

Blocking before 8Y-4:

- repair the committed 8W-7 approval phrase encoding
- make tests accept only the intended non-mojibake phrase for 8W-7
- make tests reject the mojibake phrase before opening any row source
- revalidate the 8W-7 health report wording

Still missing or needs reconfirmation before any future row-preview smoke:

- explicit preview boundary for the Route C / 8Y chain
- redaction contract scoped to 8Y-4
- allowed output field contract scoped to 8Y-4
- row count and sample-size limit scoped to 8Y-4
- privacy guard scoped to 8Y-4
- no-production-write guard scoped to 8Y-4
- focused test coverage for the future 8Y-4 phrase and no-open-before-approval behavior

## Selected Next Boundary Option

Selected:

`pause_or_blocked_before_controlled_redacted_review_only_row_preview_smoke`

Reason:

The repo has relevant controlled surfaces, but 8Y-3 found a committed approval-phrase encoding blocker in the existing row-preview helper/test pair. A future 8Y-4 should not be proposed as ready until that blocker is repaired or a fresh docs-only gate explicitly chooses a different safe path.

## Future 8Y-4 Placeholder Status

Future 8Y-4 is inactive in 8Y-3.

Inactive placeholder phrase:

`APPROVE_8Y_4_CONTROLLED_REDACTED_REVIEW_ONLY_ROW_PREVIEW_SMOKE`

This phrase appears here only as an inactive future gate marker. It does not authorize implementation in 8Y-3. It does not authorize Evidence Layer write, production EvidenceItem creation, production case creation, production analysis_run creation, Review Queue runtime creation, Source 11 runtime, actual FinalSummaryReport runtime, route/frontend/runtime persistence, provider/collector jobs, real API/LLM behavior, URL fetching, or scraping.

## Future 8Y-4 Minimum Constraints If Unblocked Later

A later 8Y-4 may be considered only after a new exact approval phrase and only if the 8W-7 encoding blocker has been resolved or superseded by a separately reviewed safe contract.

Minimum future constraints:

- backend-only
- test-first
- controlled smoke only
- review-only
- redacted preview only
- bounded row count
- no raw author identity exposure
- no actual profile URL exposure
- no raw comment dump
- no secret/cookie/token/session/browser-profile exposure
- no private collector source inspection
- no arbitrary real exchange directory read
- no arbitrary real package directory read
- no Evidence Layer write
- no production EvidenceItem creation
- no production case creation
- no production analysis_run creation
- no Review Queue runtime creation
- no Source 11 runtime
- no actual FinalSummaryReport runtime
- no route/frontend/runtime persistence unless separately gated later
- human_review_required: true
- no_automatic_trust_upgrade: true

Minimum future output flags:

- row_preview_created may be true only inside a controlled backend test path
- preview_mode: review_only_redacted_preview or safe equivalent
- evidence_rows_parsed may be true only if explicitly approved by the future 8Y-4 phrase and only inside the bounded controlled preview path
- raw_rows_exposed: false
- raw_comments_exposed: false
- raw_identities_exposed: false
- author_names_or_profile_urls_exposed: false
- secrets_read: false
- evidence_layer_write: false
- production_evidence_item_created: false
- production_case_created: false
- production_analysis_run_created: false
- review_queue_runtime_used: false
- generated_response_text: false
- source11_runtime_called: false
- actual_final_summary_report_created: false
- b_end_report_runtime_generated: false
- sandbox_public_event_runtime_generated: false
- export_download_public_delivery_created: false
- route_ready: false
- frontend_ready: false
- production_ready: false
- customer_ready: false
- public_ready: false

## Hard Blockers For Future 8Y-4

Future 8Y-4 must stop if it needs:

- the mojibake 8W-7 phrase to remain accepted
- private collector source inspection
- collector job execution
- arbitrary real exchange directory read
- arbitrary real package directory read
- raw row/comment/identity exposure
- actual author names or profile URLs in output
- secrets, cookies, sessions, tokens, browser profiles, or private paths
- Evidence Layer write
- production EvidenceItem creation
- production case creation
- production analysis_run creation
- Review Queue runtime creation
- route/API/frontend changes
- Source 11 runtime
- actual FinalSummaryReport runtime
- B-end/Sandbox/export/public delivery
- real API/LLM/network/fetch/scrape behavior
- automatic trust upgrade
- readiness claims for customers, public distribution, production use, final delivery, export, or Source 11 runtime

## Source Recommendation

source_update_recommended_after_commit: no

Source 11 update is not recommended because this docs-only audit did not change Analysis Request, Provider, Import Governance, Source 11 runtime, or actual FinalSummaryReport runtime behavior.

Do not create Project Source files inside this repository for 8Y-3.

## Recommended Next Task

Do not proceed directly to 8Y-4.

Recommended next task:

Repair and verify the existing 8W-7 approval phrase encoding in the committed row-preview helper/test/health-report surface, then rerun a docs-only 8Y-3 or 8Y-4 gate decision as appropriate.

