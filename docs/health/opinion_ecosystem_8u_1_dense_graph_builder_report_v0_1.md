# Opinion Ecosystem 8U-1 Dense Graph Builder Report v0.1

## A. Decision / Status

```text
phase = 8U-1
task = backend_only_controlled_evidence_package_to_dense_opinion_graph_builder
decision = ready
privacy_issue_stop = no
backend_only = yes
frontend_changed = no
code_changed = yes
tests_changed = yes
dense_graph_builder_implemented = yes
controlled_repo_sample_loader_implemented = yes
data_connected_scope = controlled_repo_sample_or_in_memory_fixture_only
real_api_called = no
real_llm_called = no
collector_run = no
private_collector_accessed = no
real_exchange_dir_read = no
evidence_layer_write = no
production_case_created = no
production_analysis_run_created = no
generated_response_text = no
publish_send_post_execute = no
```

## B. What Changed

Changed files:

- `backend/app/services/opinion_ecosystem_dense_graph_builder.py`
- `backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py`
- `docs/health/opinion_ecosystem_8u_1_dense_graph_builder_report_v0_1.md`

The new backend-only service provides:

- `build_dense_opinion_graph_from_evidence_items(...)`
- `load_controlled_repo_sample_evidence_items(...)`

The builder accepts in-memory evidence item dictionaries and returns a JSON-serializable dense graph run. The loader is separate, explicit, repo-relative, JSONL-only, and restricted to `docs/samples`.

## C. Graph Output Summary

Output contract:

```text
run_schema = sentigraph_opinion_ecosystem_dense_graph_run_v0_1
run_status = generated_local_dense_graph
coefficient_source = mock_default
calibration_status = uncalibrated
empirical_validation = not_started
human_review_required = true
```

Graph sections:

- `nodes`
- `edges`
- `timeline_buckets`
- `graph_summary`

Node types:

- `people_cluster_proxy`
- `influence_core_proxy`
- `content_aggregate_proxy`
- `echobox_proxy`

PeopleCluster proxy nodes are synthetic anonymous aggregate proxies such as `pc_0001`. They are not real users, not account nodes, not raw author IDs, and not psychological profiles.

Edge types:

- `same_platform_discussion`
- `same_time_bucket`
- `stance_affinity`
- `influence_core_exposure`
- `echobox_membership`
- `cross_platform_bridge_candidate`

Edges are safe synthetic visualization candidates. They are not a real social graph, not a reply/follower graph, and not causal proof.

## D. Controlled Sample Smoke

Controlled repo sample loaded:

```text
docs/samples/donglu_sunjihai_youth_football/donglu-sunjihai-youth-football-202606-v2_20260617_121016/evidence_items.jsonl
```

Summary only:

```text
run_status = generated_local_dense_graph
raw_evidence_count = 581
eligible_evidence_count = 581
people_cluster_proxy_count = 240
edge_count = 800
timeline_bucket_count = 7
blocked_field_count = 0
```

No raw evidence rows or author identifiers were printed in this report.

## E. Safety Behavior

Boundary flags are present and true:

- selected_sample_only
- not_full_web
- not_full_platform
- not_full_thread
- not_official_verification
- not_causal_proof
- not_prediction
- not_production_score
- no_auto_execute
- no_generated_public_response
- anonymous_aggregate_only

Runtime side-effect flags remain false:

- called_real_api
- called_real_llm
- ran_collector
- accessed_private_collector
- read_real_exchange_dir
- fetched_url
- scraped_page
- wrote_evidence_layer
- created_production_case
- created_analysis_run
- generated_b_end_report_runtime
- generated_sandbox_runtime
- generated_public_event_runtime
- generated_response_text
- published_or_sent
- auto_executed

Forbidden active fields block graph generation without exposing forbidden values:

- raw author identifiers
- profile URLs
- secret-like fields
- generated public response fields
- publish/send/post/execute fields
- target-user or persuasion fields
- truth/official verification/prediction fields
- psychological profile fields

## F. Validation Commands and Results

Red phase:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
result = failed as expected before implementation
reason = ImportError for missing opinion_ecosystem_dense_graph_builder service
```

Green / required validation:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
result = passed, 11 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
result = passed, 7 passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_builder.py
result = passed

git diff --check
result = passed
```

Current git status before final report validation:

```text
backend/app/services/opinion_ecosystem_dense_graph_builder.py = untracked
backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py = untracked
docs/health/opinion_ecosystem_8u_1_dense_graph_builder_report_v0_1.md = untracked
```

## G. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Contract Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- Graph density is deterministic and mock-default, not calibrated.
- Timeline buckets are deterministic buckets, not complete historical reconstruction.
- Edges are visualization candidates, not real social/causal edges.
- No frontend integration is included in this phase.

These limitations are intentional for 8U-1.

### P3 Nice-to-have

- Consider 8U-2 backend generated-run integration decision or backend-only route contract.
- Keep frontend frozen until dense graph output is stable.

## H. Not Run and Why

- frontend build not run because frontend was not changed
- browser smoke not run because no UI was changed
- collector not run because this phase is controlled repo sample / in-memory fixture only
- real APIs not called
- real LLMs not called
- full backend pytest not run because the approved slice is a focused backend-only service and required validations passed

## I. Safety Confirmations

- backend-only implementation
- no frontend code changed
- no UI changed
- no public route added
- no production import
- no private collector runtime integration
- no private collector access
- no real exchange dirs read
- no arbitrary absolute local paths read
- no real API called
- no real LLM called
- no URL fetching
- no scraping
- no cookies / sessions / tokens / browser profiles read
- no Evidence Layer write
- no production case created
- no production analysis_run created
- no B-end report runtime generated
- no Sandbox/public event runtime generated
- no response_text or generated_public_message generated
- no publish / send / post / execute behavior
- no target_user_list, persuasion_score, truth_score, official_verified, prediction_probability, psychological_profile, or personality_diagnosis exposed
- no GitHub Actions workflow recreated

## J. Next Recommendation

Prefer 8U-2 backend dense graph generated-run integration decision or backend-only route contract.

Do not modify frontend until backend graph output is stable.
