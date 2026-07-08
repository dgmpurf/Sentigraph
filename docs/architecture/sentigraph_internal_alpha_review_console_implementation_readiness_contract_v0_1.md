# Sentigraph Internal Alpha Review Console Implementation Readiness Contract v0.1

## Scope of Readiness

This contract defines readiness for discussing a future first implementation slice of the Internal Alpha review console/operator workflow. It does not implement that slice.

The readiness scope is limited to backend-only safe metadata projection. It excludes route/API/frontend implementation, runtime persistence, Review Queue runtime, actual Evidence Layer write, production EvidenceItem, production case, production analysis_run, actual analysis execution, production Analysis Result, Source 11 runtime, FinalSummaryReport runtime, B-end/Sandbox/export/public delivery, collector/provider jobs, real package reads, and production package row parsing.

## Relationship to Prior Phases

8Z-16 reached `evidence_layer_write_candidate_boundary` only. It proved a no-write backend governance chain.

8Z-17 defined review console/operator workflow planning, safe display fields, forbidden fields, forbidden actions, and future route/UI posture.

8Z-18 added safety contract tests only. It verified the 8Z-17 boundary and confirmed no active review console implementation or public/customer alias was introduced.

8W-69 pause remains preserved. 8W-70 reactivation remains not selected.

## Option Comparison Summary

| Option | Description | Risk | Readiness decision |
| --- | --- | --- | --- |
| A | pause_only | lowest | allowed fallback |
| B | backend-only safe metadata projection helper | low if separately approved | selected as future boundary |
| C | disabled-by-default internal read-only backend route skeleton | medium | not next |
| D | frontend static read-only review console mock | medium/high | not next |
| E | actual review console route + UI implementation | high | blocked |
| F | Review Queue runtime / Evidence write console | forbidden | blocked |

## Allowed Future First Slice

Only Option B is selected for possible future discussion:

`ready_for_8Z_20_internal_alpha_review_console_safe_metadata_projection_helper_smoke`

Allowed scope if separately approved:

- backend-only
- test-first
- local-only
- no route/API
- no frontend
- no runtime persistence
- no helper execution from the Evidence chain
- no actual Evidence Layer write
- no Review Queue runtime
- no production objects
- no Source 11 runtime
- no FinalSummaryReport runtime
- no public/export delivery
- no collector/provider jobs
- no real package reads
- no raw rows/comments/identities
- creates only a local safe projection object from safe fixtures or stage summaries
- label-only operator outcomes
- `human_review_required = true`
- `no_automatic_trust_upgrade = true`

## Forbidden Implementation Paths

Forbidden paths:

- route/API review console implementation
- frontend review console implementation
- runtime persistence
- Evidence chain helper execution
- row preview execution
- candidate creation beyond a local projection object
- actual Evidence Layer write
- persisted Evidence Layer record
- production EvidenceItem
- Review Queue runtime
- production Review Queue item
- production case
- production analysis_run
- actual analysis execution
- production Analysis Result authorization or creation
- Source 11 runtime
- FinalSummaryReport runtime
- B-end report runtime
- Sandbox/public event runtime
- export/download/public/final-delivery runtime
- collector/provider jobs
- private collector inspection
- real exchange/package directory reads
- production package row parsing
- raw rows/comments/identities exposure
- secrets access

## Safe Metadata Projection Object Sketch

Future object:

```text
schema = sentigraph_internal_alpha_review_console_safe_metadata_projection_v0_1
mode = backend_only_local_safe_metadata_projection
projection_created = true only in backend test path
source_chain_boundary = evidence_layer_write_candidate_boundary
safe_metadata_only = true
label_only_operator_outcomes = true
actual_write_enabled = false
production_object_enabled = false
route_ready = false
frontend_ready = false
runtime_ready = false
public_ready = false
production_ready = false
human_review_required = true
no_automatic_trust_upgrade = true
```

## Input Contract

Inputs must be already-safe summaries or fixtures:

- request_id
- provider_result_id
- opaque package_reference
- stage_id
- stage_schema
- stage_status
- stage_mode
- candidate_id / boundary_id opaque IDs
- evidence_count summary only
- source_count summary only
- warning_count
- blocker_count
- coverage_note_summary
- validation_summary
- safety_flags
- boundary_flags
- audit refs / health report refs

Inputs must not include raw row contents, file bytes, private paths, source URLs, author identifiers, secrets, real package row contents, or data that requires fresh file reads.

## Output Contract

Output must include only safe projection fields:

- schema
- mode
- projection_created
- source_chain_boundary
- safe_metadata_only
- label_only_operator_outcomes
- request_id
- provider_result_id
- opaque package_reference
- stage_summaries
- evidence_count_summary
- source_count_summary
- warning_count
- blocker_count
- coverage_note_summary
- validation_summary
- safety_flags
- boundary_flags
- allowed_actions labels
- blocked_actions labels
- inactive_next_gate_label
- human_review_required
- no_automatic_trust_upgrade

Output must keep active flags false:

- actual_write_enabled
- production_object_enabled
- route_ready
- frontend_ready
- runtime_ready
- public_ready
- production_ready

## Blockers

Block if:

- approval phrase is missing or ambiguous
- input includes raw rows/comments/identities
- input includes secrets or private paths
- input requires real package or exchange directory reads
- input requires production package row parsing
- projection would call Evidence chain helpers
- projection would create candidates beyond local projection
- projection would write Evidence Layer
- projection would create production objects
- projection would use Review Queue runtime
- projection would call Source 11 / FinalSummaryReport
- projection would expose route/API/frontend
- projection weakens human review or no automatic trust upgrade semantics

## Stop Rules

Stop and report before implementation if any future task requires:

- backend route/API
- frontend UI
- runtime persistence
- helper execution
- row preview execution
- actual Evidence Layer write
- production EvidenceItem
- Review Queue runtime
- production case
- production analysis_run
- actual analysis execution
- production Analysis Result
- Source 11 runtime
- FinalSummaryReport runtime
- public/export delivery
- collector/provider jobs
- private collector inspection
- real package/exchange reads
- production package row parsing
- raw identity exposure
- secrets access

## Future Validation Expectations

Future 8Z-20, if separately approved, should validate:

- new focused test
- helper tests if a helper is added
- 8Z-17 / 8Z-18 contract tests
- no route/API/frontend changes
- no runtime persistence
- `py_compile` if a service file is touched
- `git diff --check`
- static scans for forbidden fields/actions/readiness claims
- no browser smoke unless frontend/UI is changed
- no full pytest unless explicitly required by the checkpoint

## Future Approval Phrase

Inactive future phrase only:

`APPROVE_8Z_20_INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_METADATA_PROJECTION_HELPER_SMOKE`

This phrase does not authorize anything in 8Z-19. It does not authorize route/API/frontend, Review Queue runtime, actual Evidence Layer write, production objects, Source 11 runtime, FinalSummaryReport runtime, collector/provider jobs, real package reads, or public delivery.

## Non-goals

This readiness contract does not:

- implement a projection helper
- add route/API
- add frontend
- add tests
- call helpers
- create candidates
- write Evidence Layer
- create production objects
- update Source 11
- create report/export/delivery runtime
