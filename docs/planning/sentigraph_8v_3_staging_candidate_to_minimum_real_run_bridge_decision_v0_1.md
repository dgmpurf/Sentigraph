# Sentigraph 8V-3 Staging Candidate to Minimum Real-run Bridge Decision v0.1

## A. Decision / Status

phase = 8V-3

task = staging_candidate_to_minimum_real_run_bridge_decision

decision = ready

privacy_issue_stop = no

docs_only = yes

backend_code_changed = no

frontend_code_changed = no

tests_changed = no

route_changed = no

api_route_added = no

runtime_changed = no

collector_run = no

real_api_called = no

real_llm_called = no

url_fetch_or_scrape = no

private_collector_inspected = no

real_exchange_dir_read = no

evidence_rows_parsed = no

evidence_layer_write = no

production_case_created = no

production_analysis_run_created = no

generated_response_text = no

public_route_created = no

source_files_created = no

docs_project_sources_created = no

Decision:

8V-3 approves only a future contract direction: a safe review-only staging candidate may later become a minimum real-run / generated-run input candidate if the bridge remains metadata-only, human-review-required, and side-effect-free.

8V-3 does not approve implementation.

## B. Current Proven Chain After 8V-2

8V-2 proved the following backend-only controlled metadata chain:

1. controlled provider result metadata
2. safe package resolver
3. local exchange metadata smoke
4. review-only staging candidate

8V-2 also proved:

- `evidence_items.jsonl` and `evidence_items.csv` are presence-only in the metadata smoke.
- Sentinel row values are not read or emitted.
- Path escape is blocked.
- Forbidden top-level secret-like provider metadata is blocked.
- No Evidence Layer write happens.
- No production case is created.
- No production `analysis_run` is created.
- No collector job runs.
- No real API or real LLM is called.
- No frontend, route, or runtime behavior is changed.

The resulting safe staging surface is a review-only metadata object, not evidence truth, not imported evidence, and not an analysis-ready case.

## C. Bridge Problem Statement

Sentigraph now needs a careful bridge design between two implemented but separate surfaces:

- upstream: provider package metadata -> review-only staging candidate
- downstream: backend-only minimum real-run / generated-run wrapper over safe local fixture inputs

The bridge problem is not "run analysis from a package." The bridge problem is narrower:

Define how safe, reviewed metadata from a review-only staging candidate can become a candidate request for a future minimum real-run wrapper while preserving all current boundaries.

The bridge must prevent accidental promotion from:

- package metadata to Evidence Layer
- review-only staging to production case
- staging candidate to production `analysis_run`
- metadata summary to raw evidence rows
- generated-run candidate to report/public/Sandbox output

## D. Allowed Future Bridge Input

Allowed input must come from safe review-only staging summaries and safe package/provider metadata already produced by existing helpers. It may include:

- `staging_candidate_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `package_name`
- `package_role`
- `case_id_hint`
- `case_title_hint`
- `validation_status`
- `evidence_count`
- `source_count`
- `warning_count`
- `error_count`
- safe coverage summary
- validation summary
- package file presence map
- missing metadata-file summary
- blocker summary
- warning summary
- audit refs
- source count summary if already safe metadata
- platform summary if already safe metadata
- selected-sample / controlled-package scope note
- `metadata_only=true`
- `path_exposed=false`
- side-effect flags already known false

Allowed input must not require reading original package rows. It should be passed as a dict/object already produced by the metadata smoke or staging helper.

## E. Forbidden Input / Forbidden Outputs

Forbidden input:

- full evidence rows
- raw comments
- raw author IDs
- raw author names
- profile URL values
- private messages
- cookies
- sessions
- tokens
- passwords
- API keys
- absolute private package paths
- browser profile paths
- collector runtime internals
- raw package row files
- external URL contents
- row-level identities

Forbidden output:

- `response_text`
- `generated_public_message`
- `target_user_list`
- `persuasion_score`
- `truth_score`
- `official_verified`
- `prediction_probability`
- `psychological_profile`
- `personality_diagnosis`
- `auto_execute`
- `publish_now`
- `send_now`
- `post_now`
- `execute_now`
- any public route or public URL
- any B-end report runtime output
- any Sandbox/public event runtime output
- any Evidence Layer write result
- any production case or production `analysis_run`

Safe negative boundary flags may name these concepts only to confirm they are false or blocked.

## F. Future Bridge Output Contract

Future bridge object name:

`sentigraph_staging_candidate_generated_run_bridge_v0_1`

Future bridge output should include:

- `bridge_id`
- `bridge_schema`
- `bridge_status`
- `staging_candidate_id`
- `provider_result_id`
- `provider_job_id`
- `request_id`
- `case_id_hint`
- `package_name`
- `input_source_kind = review_only_staging_candidate`
- `input_scope_note`
- `metadata_only = true`
- `evidence_rows_parsed = false`
- `evidence_layer_write = false`
- `production_case_created = false`
- `production_analysis_run_created = false`
- `human_review_required = true`
- `generated_run_requested = false` in bridge decision mode
- `minimum_real_run_input_candidate`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`
- `audit_refs`
- `downstream_allowed_actions`
- `downstream_blocked_actions`

Bridge status values should be conservative:

- `candidate_ready_for_future_minimum_real_run`
- `manual_review_required`
- `blocked_metadata_contract`
- `blocked_privacy_issue`
- `blocked_path_escape`
- `blocked_missing_validation`
- `blocked_count_inconsistency`
- `blocked_requested_side_effect`

The bridge must not call `generate_opinion_ecosystem_minimum_real_run` in the design phase. A later implementation may create a bridge object first, then separately decide whether a generated-run wrapper may be called against a safe in-memory input candidate.

## G. Minimum Real-run Input Candidate Mapping

The future bridge may map safe staging metadata into a minimum real-run input candidate with this shape:

- `candidate_id`: derived from bridge/staging identifiers
- `case_id`: from `case_id_hint` if safe, otherwise `missing_case_id`
- `sample_id`: safe controlled package/sample identifier, not a raw package path
- `input_package_id`: safe `package_name` or package ID
- `input_source_kind`: `review_only_staging_candidate`
- `input_scope_note`: selected sample / controlled package only
- `fixture_metadata`: safe metadata fields needed by the minimum real-run wrapper
- `evidence_items_safe`: empty or future-safe aggregate placeholders only; no raw rows in 8V-4 unless separately approved
- `module_seed_policy`: `metadata_only_seed_candidate`
- `human_review_required`: true
- `calibration_status`: `uncalibrated`
- `empirical_validation`: `not_started`

The candidate must remain:

- selected sample / controlled package only
- metadata-only
- human-review-required
- uncalibrated
- not prediction
- not causal proof
- not official verification
- not production score
- not full-web
- not full-platform
- not full-thread

If future implementation needs actual safe evidence item dicts, that must be a separate design checkpoint. 8V-3 does not approve row preview, row import, or package evidence parsing.

## H. Blockers / Warnings

Hard blockers:

- missing `package_name`
- package resolver status is not accepted metadata-only
- privacy issue
- forbidden metadata fields
- path escape
- missing validation report
- missing required package metadata files
- evidence count / source count inconsistency
- unknown or future platform requiring manual review
- requested row parsing
- requested Evidence Layer write
- requested production case
- requested production `analysis_run`
- requested public output
- requested generated response text
- requested auto-execute / publish / send / post
- requested real API / real LLM
- requested collector job
- requested private collector access
- requested real exchange directory read

Warnings:

- validation status is warn
- coverage note is missing or weak
- evidence count is low
- source count is low
- package role is not clearly review-ready
- unknown platform appears only in safe metadata and requires manual review
- selected sample limitations need visible downstream copy

Warnings do not upgrade trust. Warnings do not make the candidate analysis-ready.

## I. Relationship to Generated-run, Dense Graph, Report Runtime

This bridge is upstream of minimum real-run / generated-run.

It does not call dense graph directly.

Dense graph may later attach only after a safe generated-run object exists and only through its own boundary-preserving integration. Existing dense graph integration keeps `frontend_ready=false`, `route_ready=false`, and `production_ready=false` in its summary.

This design does not approve:

- dense graph frontend integration
- dense graph public route
- B-end route
- report runtime
- public event runtime
- Strategy Lab runtime
- generated response text
- public access or delivery

Generated-run is still a selected-sample, uncalibrated, human-review-only object. Provider output remains evidence, not truth.

## J. Next-slice Options

| Option | Description | Risk | Recommended |
| --- | --- | --- | --- |
| 8V-4 Bridge Contract Test Plan Docs-only | Write future tests before implementation | lowest | acceptable if more planning is desired |
| 8V-4 Controlled Staging Candidate to Minimum Real-run Bridge Smoke / Test-first Skeleton | Add backend-only tests and minimal bridge helper using controlled metadata only | low | recommended |
| Row preview gate | Read bounded package rows | medium/high | not now |
| Production Evidence import | Write Evidence Layer / production case | high | not approved |
| Dense graph frontend integration | UI/API display path | medium | not now |
| Algorithm or weight recalibration | Formula changes | medium | not now |
| Public route or report runtime | Public/customer output | high | not approved |

## K. Recommended Next Step

Recommended next task:

Phase 8V-4 Controlled Staging Candidate to Minimum Real-run Bridge Smoke / Test-first Skeleton.

Recommended scope:

- backend-only
- test-first
- no production code beyond a tiny pure helper if needed
- input is safe review-only staging summary from controlled metadata fixture
- output is bridge candidate only
- no call to dense graph
- no API route
- no frontend
- no runtime persistence
- no evidence row parsing
- no Evidence Layer write
- no production case or production `analysis_run`
- no collector/private project access
- no real APIs/LLMs

If the implementation looks larger than a tiny helper and test, stop and do `Phase 8V-4 Bridge Contract Test Plan Docs-only` instead.

## L. Explicit Non-approvals

8V-3 does not approve:

- backend runtime implementation
- frontend integration
- API route
- route change
- runtime persistence
- collector execution
- private collector inspection
- real exchange directory read
- evidence row parsing
- Evidence Layer write
- production case creation
- production `analysis_run` creation
- generated response text
- public route
- B-end report runtime
- Sandbox/public event runtime
- Strategy Lab runtime
- dense graph frontend integration
- real API
- real LLM
- URL fetching
- scraping
- MediaCrawler integration
- OpenClaw production integration

## M. Validation / Not Run

Validation for this docs-only phase:

```text
git status --short
git branch --show-current
git rev-parse HEAD
git diff --check
```

Optional static scan:

```text
rg -n "fetch\(|axios|http://|https://|API key|token|cookie|author_name|author_id|profile_url|evidence_items|production_case|analysis_run|auto_execute|publish_now|send_now|post_now|execute_now" docs/planning/sentigraph_8v_3_staging_candidate_to_minimum_real_run_bridge_decision_v0_1.md docs/architecture/sentigraph_staging_candidate_to_generated_run_bridge_contract_v0_1.md
```

Expected scan result:

- Matches are acceptable only in boundary, forbidden, blocker, or false-flag language.
- No runtime implementation should appear.

Not run:

- pytest: not run because no code/tests changed.
- frontend build: not run because no frontend changed.
- browser smoke: not run because no UI changed.
- collector: not run by boundary.
- real APIs/LLMs/network: not run by boundary.

## N. Source Maintenance Note

source_update_recommended = no immediate

Reason:

This is a docs-only bridge decision. It does not change runtime behavior, Analysis Request governance behavior, provider/package runtime behavior, or frontend behavior. Project Source files should not be created or updated in this task.

