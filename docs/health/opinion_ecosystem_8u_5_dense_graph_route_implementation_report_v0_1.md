# Opinion Ecosystem 8U-5 Dense Graph Route Implementation Report v0.1

## A. Decision / Status

phase = 8U-5

task = backend_dense_graph_route_implementation

decision = ready

privacy_issue_stop = no

backend_only = yes

frontend_changed = no

route_changed = yes

api_route_added = yes

code_changed = yes

tests_changed = yes

route_implemented = yes

route_disabled_by_default = yes

route_get_only = yes

route_internal_local_only = yes

sample_allowlist_enforced = yes

arbitrary_path_input_allowed = no

private_collector_path_allowed = no

url_fetch_allowed = no

dense_graph_service_called_when_disabled = no

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

## B. What Changed

Changed files:

- `backend/app/api/v1/routes/opinion_ecosystem_dense_graph.py`
- `backend/app/api/v1/api.py`
- `backend/app/tests/test_opinion_ecosystem_dense_graph_route.py`
- `docs/health/opinion_ecosystem_8u_5_dense_graph_route_implementation_report_v0_1.md`

The new route module implements the approved internal dense graph route and registers it under the existing API v1 router.

## C. Route Behavior Summary

Route path:

```text
GET /api/v1/internal/opinion-ecosystem/dense-graph/generated-runs/{sample_id}
```

Environment gate:

```text
SENTIGRAPH_OPINION_ECOSYSTEM_DENSE_GRAPH_ROUTE_ENABLED
```

Allowed true values after normalization:

- `1`
- `true`
- `yes`

All other values return a safe disabled response:

- `error_schema = sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1`
- `route_status = disabled`
- `error_code = route_disabled`
- `path_exposed = false`
- `raw_metadata_exposed = false`
- `private_collector_path_exposed = false`
- `evidence_rows_exposed = false`

Allowed sample IDs:

- `donglu-sunjihai-youth-football`
- `helldivers-psn`

The route uses a hardcoded allowlist to controlled repo sample JSONL paths under `docs/samples`. Request input never supplies a file path, package path, private collector root, URL, or search query.

Unsupported sample response:

- `route_status = unsupported_sample`
- `error_code = unsupported_sample`
- no path exposure
- no raw row exposure
- no default-sample fallback

Bounded params implemented:

- `node_limit`: min 20, max 240
- `edge_limit`: min 50, max 800
- `include_previews`: boolean, default true

Unsupported query params return `unsupported_query_parameter` without path exposure.

Success response:

- `response_schema = sentigraph_opinion_ecosystem_dense_graph_route_response_v0_1`
- `route_status = ready | degraded | blocked`
- `sample_id`
- `generated_run_integration`
- `graph_summary`
- `preview_limits`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`
- `human_review_required = true`

## D. Dense Graph Output Summary

Enabled Dong/Sun aggregate route smoke:

```text
route_status = ready
people_cluster_proxy_count = 240
edge_count = 800
timeline_bucket_count = 7
frontend_ready = false
production_ready = false
```

Only aggregate counts were printed. Raw evidence rows and raw comments were not printed.

## E. Safety Behavior

- no raw author identifiers
- no arbitrary path input
- no private collector path input
- no URL fetch
- no search query execution
- no generated response text
- no auto-execute
- no Evidence Layer write
- no production case
- no production analysis run
- no frontend exposure
- no public/C-end/B-end/customer route
- no default sample fallback for unknown samples

Controlled JSONL rows are loaded only through the existing repo-relative `docs/samples` loader and are mapped into allowlisted safe evidence fields before entering the integration service. Original rows are not returned.

## F. Validation Commands and Results

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_route.py
result = passed, 13 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
result = passed, 10 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
result = passed, 9 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
result = passed, 11 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
result = passed, 7 passed

python -m py_compile backend/app/api/v1/routes/opinion_ecosystem_dense_graph.py
result = passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py
result = passed

python -m py_compile backend/app/api/v1/api.py
result = passed

git diff --check
result = passed with a line-ending warning for backend/app/api/v1/api.py
```

Final `git status --short` is recorded in the turn summary.

## G. Not Run and Why

- Frontend build not run because no frontend code changed.
- Browser smoke not run because this phase adds backend route only.
- Collector not run.
- Real APIs not called.
- Real LLMs not called.
- Full backend pytest not run because focused route, integration, adapter, builder, and golden-contract validation passed.

## H. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Contract Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- Route remains internal and disabled by default.
- Frontend still does not consume the route.
- Dense graph values remain deterministic and uncalibrated.
- The response intentionally keeps frontend and production readiness false.

### P3 Nice-to-have

- Add 8U-6 post-implementation route smoke and stabilization.
- Consider a small backend contract snapshot once route shape stops moving.

## I. Next Recommendation

Prefer 8U-6 backend route post-implementation validation / route contract smoke, or route stabilization.

Do not modify frontend until backend route is stable.
