# Sentigraph 8Z-17 Internal Alpha Review Console and Operator Workflow Planning Decision v0.1

## Decision

- phase = 8Z-17
- decision = ready
- privacy_issue_stop = no
- docs_only = yes
- planning_only = yes
- architecture_contract_created = yes
- safety_test_plan_created = yes
- backend_code_changed = no
- tests_changed = no
- route_changed = no
- api_route_added = no
- frontend_changed = no
- runtime_changed = no
- helper_called = no
- actual_evidence_layer_write = no
- production_evidence_item_created = no
- review_queue_runtime_used = no
- production_case_created = no
- production_analysis_run_created = no
- actual_analysis_execution_started = no
- production_analysis_result_created = no
- source11_runtime_called = no
- finalsummaryreport_runtime_called = no
- public_delivery_created = no
- approval_phrase = APPROVE_8Z_17_INTERNAL_ALPHA_REVIEW_CONSOLE_AND_OPERATOR_WORKFLOW_PLANNING_DOCS_ONLY
- selected_next_boundary_option = ready_for_8Z_18_internal_alpha_review_console_safety_contract_tests_only
- recommended_tag = no

## Current State Summary

8Z-1 through 8Z-2 defined the on-demand collector workflow and request/result metadata contracts as docs-only planning.

8Z-3 through 8Z-5 proved controlled backend metadata fixture steps for request metadata, provider result metadata, and request/result correlation.

8Z-6 through 8Z-8C defined and repaired the review-only staging to Route C entry path, including the no-real-row adapter compatibility path.

8Z-9 proved a controlled Route C row-preview smoke with synthetic temp input only. It did not read real exchange directories, real package directories, production package rows, source manifests, collection logs, or private collector source.

8Z-10 through 8Z-11 repaired the controlled Evidence candidate helper phrase and proved a controlled Evidence candidate can be created in a backend test path only.

8Z-12 through 8Z-13 proved controlled Evidence candidate to controlled Review Queue candidate to controlled Evidence Layer import candidate.

8Z-14 through 8Z-15 proved controlled Evidence Layer import candidate to controlled Evidence Layer write-candidate boundary.

8Z-16 completed Internal Alpha v0.1 as a no-write backend governance chain:

`on-demand request metadata fixture -> provider_result/package metadata fixture -> request/result correlation -> review-only staging candidate -> no-real-row Route C row-preview entry adapter -> controlled redacted review-only row preview -> controlled Evidence candidate -> controlled Review Queue candidate -> controlled Evidence Layer import candidate -> controlled Evidence Layer write-candidate boundary`

8Z-16 reached `evidence_layer_write_candidate_boundary`. It did not perform actual Evidence Layer write, create a persisted Evidence Layer record, create a production EvidenceItem, use Review Queue runtime, create production case, create production analysis_run, start actual analysis execution, create production Analysis Result, call Source 11 runtime, call FinalSummaryReport runtime, generate B-end/Sandbox/public/export/final delivery runtime, run collector/provider jobs, read real package/exchange directories, or parse production package rows.

Internal Alpha v0.1 remains a no-write backend governance chain only. `human_review_required = true` remains central. `no_automatic_trust_upgrade = true` remains central. The default next state is pause.

## Review Console Purpose

A future Internal Alpha review console would be an internal operator planning surface and human review coordination surface. It would show safe metadata and boundary status for the controlled no-write chain.

The future console is not:

- public UI
- customer UI
- Review Queue runtime
- Evidence Layer write UI
- production approval UI
- Source 11 UI
- report UI
- export UI
- delivery UI

8Z-17 does not implement this console. It only defines what a safe future console would need to prove before any route/UI work is considered.

## Operator Workflow Draft

A future operator workflow may follow this read-only sequence:

1. Operator opens an Internal Alpha chain summary.
2. Operator sees request/result correlation summary.
3. Operator sees review-only staging candidate summary.
4. Operator sees no-real-row adapter status.
5. Operator sees redacted row-preview status.
6. Operator sees Evidence candidate status.
7. Operator sees Review Queue candidate status.
8. Operator sees Evidence Layer import candidate status.
9. Operator sees write-candidate boundary status.
10. Operator reviews blockers and warnings.
11. Operator acknowledges `human_review_required`.
12. Operator acknowledges `no_automatic_trust_upgrade`.
13. Operator may assign one label-only outcome.

Allowed label-only outcomes:

- keep_paused
- needs_more_review
- blocked_privacy_or_raw_identity_risk
- blocked_missing_authority
- candidate_ready_for_future_docs_only_write_gate_discussion

These labels must not execute downstream actions. They must not write the Evidence Layer, create production objects, trigger Review Queue runtime, call Source 11 or FinalSummaryReport runtime, generate public/customer artifacts, run collector/provider jobs, or change readiness state.

## Allowed Future Display Fields

Future display is limited to safe metadata:

- request_id
- provider_result_id
- package_reference opaque ID
- stage_id
- stage_schema
- stage_status
- stage_mode
- candidate_id or boundary_id opaque IDs
- evidence_count summary only
- source_count summary only
- warning_count
- blocker_count
- coverage_note_summary
- validation_summary
- safety_flags
- boundary_flags
- human_review_required
- no_automatic_trust_upgrade
- approval_phrase_status labels only, no secret values
- audit refs or health report refs
- allowed_actions labels
- blocked_actions labels
- next gate inactive phrase labels, if any

## Forbidden Future Display Fields

Future display must not include:

- raw evidence rows
- raw comments
- raw author IDs
- raw author names
- actual profile URLs
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- browser profiles
- absolute private paths
- `.env` values
- `evidence_items.jsonl` contents
- `evidence_items.csv` contents
- source_manifest row contents
- collection_log row contents
- original package row contents
- response_text
- generated_public_message
- target_user_list
- persuasion_score
- truth_score
- official_verified
- prediction_probability
- psychological_profile
- personality_diagnosis

## Forbidden Future Active Actions

Future active actions remain forbidden:

- approve actual Evidence Layer write
- perform actual Evidence Layer write
- create production EvidenceItem
- use Review Queue runtime
- create production Review Queue item
- create production case
- create production analysis_run
- start actual analysis execution
- authorize production Analysis Result
- create production Analysis Result
- call Source 11 runtime
- create FinalSummaryReport runtime output
- generate B-end report runtime
- generate Sandbox/public event runtime
- create export/download/public/final-delivery runtime
- run collector/provider job
- inspect private collector source
- read real exchange/package directory
- parse production package rows
- fetch URL
- scrape
- call real API
- call real LLM
- publish/send/post/execute any platform action

## Future Route/UI Posture

If a future implementation is considered, it must start with safety contract tests or a docs-only contract. A future route, if ever allowed, should be:

- internal-only
- local-only
- disabled-by-default
- GET/read-only first
- safe metadata only
- no raw rows
- no file bytes
- no FileResponse / StreamingResponse / ZIP
- no public / C-end / B-end / customer alias
- no direct write buttons
- no production approval actions
- no route readiness, frontend readiness, production readiness, customer readiness, public readiness, export readiness, or final delivery readiness claim

8Z-17 does not implement route/UI.

## Future 8Z-18 Safety-test Plan

Future 8Z-18, if explicitly approved later, should be safety-contract-tests-only. It should test:

- disabled/default behavior if a route is later introduced
- no public aliases
- safe metadata projection only
- forbidden field scan
- no file read and no row read
- no downstream helper call
- no Evidence Layer write
- no production object
- no Review Queue runtime
- no Source 11 runtime
- no FinalSummaryReport runtime
- no export/public delivery runtime
- no forbidden call-to-action
- browser smoke requirements if frontend/UI later changes and browser capability is available
- Codex self-validation first

Inactive future phrase only:

`APPROVE_8Z_18_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFETY_CONTRACT_TESTS_ONLY`

This phrase does not authorize anything in 8Z-17. It does not authorize route/API/frontend implementation, actual write, production objects, Review Queue runtime, Source 11 runtime, FinalSummaryReport runtime, or public/export delivery.

## Relationship to Actual Write

8Z-17 does not make actual Evidence Layer write safer by itself. It does not approve actual Evidence Layer write. Future actual write or production EvidenceItem gate remains separate and higher risk.

Any actual write path needs a fresh docs-only gate and exact approval phrase before discussion, and another explicit authorization before implementation. 8Z-17 is not that gate.

## Relationship to 8W

8W-69 pause remains preserved. 8W-70 reactivation remains not selected.

Review console planning cannot satisfy production Analysis Result creation protocol requirements. It does not perform go/no-go authorization, final authorization, actual analysis execution, or production Analysis Result creation.

## Relationship to Source 11 / Report / Export

8Z-17 does not call Source 11 runtime. It does not call FinalSummaryReport runtime. It does not generate B-end report runtime, Sandbox/public event runtime, export/download/public delivery, or final delivery.

Source 11 update is not recommended because runtime behavior did not change.

## Relationship to Recording / Video

Recording/video is not the next architecture step. Review console planning is not recording. Recording remains a final presentation asset after product and governance boundaries are clearer.

## Acceptance Criteria

- planning decision doc created
- architecture/operator workflow contract created
- safety test plan created
- no backend code changed
- no tests changed
- no route/API/frontend/runtime changes
- no helpers called
- no Project Source files changed
- validation passes

## Source Recommendation

No immediate Project Source update unless this becomes part of a larger checkpoint.

Source 11 update: no.

## Next Recommended Task

Next recommended task: Phase 8Z-18 Internal Alpha Review Console Safety Contract Tests Only, docs/test-only if explicitly approved; otherwise pause. It must not implement route/API/frontend or actual Evidence Layer write.
