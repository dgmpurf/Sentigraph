# Sentigraph Internal Alpha Review Console Operator Workflow Contract v0.1

## Purpose

This contract defines a future Internal Alpha review console as a safe, internal, local, read-only operator planning surface for the 8Z no-write governance chain.

It is not an implementation contract for route/API/frontend work. It is not a production approval contract. It is not an Evidence Layer write contract.

## Actors / Personas

- internal_operator: reviews chain status, warnings, blockers, and safe metadata.
- human_reviewer: provides manual review judgment outside the system or in future label-only surfaces.
- project_owner: decides whether a future gate should remain paused, be documented further, or move into a safety-test-only phase.
- future_authorized_release_manager: placeholder only; not validated or granted authority in 8Z-17.

## Allowed Input Contract

A future console may consume only safe, already-produced, no-write chain summaries:

- Internal Alpha chain summary
- request/result correlation summary
- review-only staging candidate summary
- no-real-row adapter status
- redacted row-preview status
- Evidence candidate status
- Review Queue candidate status
- Evidence Layer import candidate status
- Evidence Layer write-candidate boundary status
- health report references
- audit reference IDs

Inputs must be metadata-only and safe-projected. They must not require helper execution, row preview execution, production row parsing, file bytes, real package directory reads, real exchange directory reads, private collector inspection, or any downstream runtime call.

## Safe Projection Contract

Allowed fields:

- request_id
- provider_result_id
- package_reference opaque ID
- stage_id
- stage_schema
- stage_status
- stage_mode
- candidate_id
- boundary_id
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
- approval_phrase_status label only
- audit_ref_id
- health_report_ref
- allowed_actions labels
- blocked_actions labels
- inactive_next_gate_label

Projection must preserve:

- selected sample limitations
- not full-web coverage
- not full-platform coverage
- not official verification
- not causal proof
- human review required
- no automatic trust upgrade
- no actual write
- no production object

## Blocked Field Matrix

Blocked fields include:

| Category | Blocked examples |
| --- | --- |
| raw evidence | raw evidence rows, raw comments, original package row contents |
| identity | raw author IDs, raw author names, actual profile URLs, private messages |
| secrets | cookies, sessions, tokens, passwords, API keys, `.env` values, browser profiles |
| paths/files | absolute private paths, `evidence_items.jsonl` contents, `evidence_items.csv` contents, source_manifest rows, collection_log rows |
| generated influence | response_text, generated_public_message, target_user_list, persuasion_score |
| unsupported truth claims | truth_score, official_verified, prediction_probability |
| sensitive profiling | psychological_profile, personality_diagnosis |

## Blocked Action Matrix

Blocked actions include:

| Action family | Blocked action |
| --- | --- |
| Evidence Layer | approve actual Evidence Layer write, perform actual Evidence Layer write |
| EvidenceItem | create production EvidenceItem, call EvidenceItem write runtime |
| Review Queue | use Review Queue runtime, create production Review Queue item |
| production case/run | create production case, create production analysis_run |
| analysis | start actual analysis execution, authorize or create production Analysis Result |
| Source/report | call Source 11 runtime, create FinalSummaryReport runtime output |
| product output | generate B-end report runtime, generate Sandbox/public event runtime |
| delivery | create export/download/public/final-delivery runtime |
| collection | run collector/provider job, inspect private collector source |
| data access | read real exchange/package directory, parse production package rows |
| network/action | fetch URL, scrape, call real API, call real LLM, publish/send/post/execute platform action |

## Future Route/UI Safety Posture

If future route/UI work is explicitly approved after a safety-test-only gate, it must be:

- internal-only
- local-only
- disabled-by-default
- GET/read-only first
- safe metadata only
- no raw rows or raw comments
- no file bytes
- no FileResponse / StreamingResponse / ZIP
- no public alias
- no C-end alias
- no B-end/customer alias
- no write button
- no production approval action
- no active downstream helper call
- no readiness claim for production/customer/public/export/final delivery

8Z-17 does not create or modify any route/UI.

## Future Audit Semantics

Future audit semantics may include:

- audit_ref_id
- actor_type
- review_label
- label_reason
- stage_refs
- health_report_refs
- created_at
- no_side_effect_confirmation

Audit labels are not runtime actions. Audit labels must not create production records, write the Evidence Layer, or trigger downstream processing.

## Future Manual Acknowledgement Semantics

Future manual acknowledgement may require explicit labels:

- acknowledged_human_review_required
- acknowledged_no_automatic_trust_upgrade
- acknowledged_selected_sample_limitations
- acknowledged_no_official_verification
- acknowledged_no_causal_proof
- acknowledged_no_actual_write
- acknowledged_no_production_object

Acknowledgement means only that a human saw the boundary. It does not clear blockers, grant authority, approve actual write, or authorize production objects.

## Future State Labels

Allowed label-only states:

- keep_paused
- needs_more_review
- blocked_privacy_or_raw_identity_risk
- blocked_missing_authority
- candidate_ready_for_future_docs_only_write_gate_discussion

Forbidden state labels:

- actual_write_approved
- production_evidence_item_approved
- review_queue_runtime_approved
- production_case_approved
- production_analysis_run_approved
- actual_analysis_execution_approved
- production_analysis_result_approved
- source11_runtime_ready
- finalsummaryreport_runtime_ready
- public_delivery_ready

## Future Stop Rules

Stop and report before implementation if any future task requires:

- backend route/API change without safety contract tests
- frontend UI change without safety contract tests
- helper execution
- row preview execution
- Evidence candidate creation
- Review Queue candidate creation
- Evidence Layer import candidate creation
- Evidence Layer write-candidate creation
- actual Evidence Layer write
- production EvidenceItem
- Review Queue runtime
- production case
- production analysis_run
- actual analysis execution
- production Analysis Result
- Source 11 runtime
- FinalSummaryReport runtime
- B-end/Sandbox/export/public/final delivery runtime
- collector/provider job
- real exchange/package directory read
- production package row parsing
- raw rows/comments/identities exposure
- secrets access

## Non-goals

This contract does not:

- implement review console
- add route/API
- add frontend
- add tests
- call helpers
- execute row preview
- create candidates
- create production records
- write Evidence Layer
- use Review Queue runtime
- approve actual write
- authorize production Analysis Result
- update Source 11
- create report/export/delivery runtime

## Future Test Matrix Summary

Future safety tests should cover:

- disabled-by-default route behavior if a route exists
- safe metadata projection only
- forbidden key scan
- forbidden value scan
- no file read
- no row read
- no helper call
- no actual write
- no production object
- no Review Queue runtime
- no Source 11 / FinalSummaryReport / export/public delivery runtime
- no public aliases
- no forbidden CTAs
- browser smoke only if UI later changes and browser tooling is available
