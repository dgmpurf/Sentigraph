# Opinion Ecosystem 8U-3 Dense Graph Generated-run Service Integration Report v0.1

## A. Decision / Status

phase = 8U-3

task = backend_only_generated_run_dense_graph_service_integration

decision = ready

privacy_issue_stop = no

backend_only = yes

frontend_changed = no

route_changed = no

api_route_added = no

code_changed = yes

tests_changed = yes

dense_graph_service_integration_implemented = yes

dense_graph_adapter_reused = yes

dense_graph_builder_reused = yes

minimum_real_run_service_reused = yes

generated_run_dense_graph_attachment_integrated = yes

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

- `backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py`
- `backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py`
- `docs/health/opinion_ecosystem_8u_3_dense_graph_generated_run_service_integration_report_v0_1.md`

Added backend-only integration function:

- `generate_opinion_ecosystem_run_with_dense_graph_attachment`

The function creates a base minimum real run through the existing backend service, produces a dense graph attachment through the 8U-2 adapter, and returns one JSON-serializable backend-only integration object.

No API route or frontend surface was added.

## C. Integrated Output Summary

Integration contract:

- `integration_schema = sentigraph_opinion_ecosystem_generated_run_dense_graph_integration_v0_1`
- `integration_status = ready_for_backend_service_surface | degraded_dense_graph_attachment | blocked`
- `sample_id`
- `source_run_id`
- `created_at`
- `base_generated_run`
- `dense_graph_attachment`
- `integration_summary`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`
- `human_review_required = true`

Integration summary includes:

- `dense_graph_attached`
- `people_cluster_proxy_count`
- `influence_core_proxy_count`
- `content_aggregate_proxy_count`
- `echobox_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode = dense_sandbox_proxy_graph`
- `frontend_ready = false`
- `route_ready = false`
- `production_ready = false`

If dense graph attachment is blocked, the integrated object is blocked and does not include the unsafe base or attachment payload.

If dense graph attachment is degraded, the integrated object is degraded and carries warnings while keeping frontend, route, and production readiness false.

## D. Safety Behavior

- anonymous aggregate/proxy only
- no raw author identifiers
- no real social graph claim
- no official verification
- no prediction
- no production score
- no generated response text
- no auto-execute
- no frontend exposure
- no API route
- no Evidence Layer write
- no production case
- no production analysis run
- no collector or private collector access

Forbidden active fields are scanned before base run generation and again before returning integrated output. Blocked objects avoid exposing forbidden field names or values in returned payloads.

## E. Validation Commands and Results

Red phase:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
result = failed as expected before implementation
reason = ImportError for missing opinion_ecosystem_dense_graph_generated_run_integration service
```

Green / required validation:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_integration.py
result = passed, 10 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
result = passed, 9 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
result = passed, 11 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_minimum_real_run.py
result = passed, 8 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
result = passed, 7 passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_generated_run_integration.py
result = passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_generated_run_adapter.py
result = passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_builder.py
result = passed

git diff --check
result = passed
```

Final `git status --short` is recorded in the turn summary.

## F. Not Run and Why

- Frontend build not run because no frontend code changed.
- Browser smoke not run because no UI or route changed.
- Collector not run because this is backend-only integration work.
- Real APIs not called.
- Real LLMs not called.
- Full backend pytest not run because focused validation covered the new integration, adapter, builder, minimum real run, and golden contracts.
- Optional controlled sample smoke not run to avoid expanding this phase beyond the required backend-only contract tests.

## G. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Contract Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- No route exposes the integrated object yet.
- No frontend consumes the dense graph attachment yet.
- Dense graph output remains deterministic and uncalibrated.
- The integrated object is not production-ready and explicitly marks frontend, route, and production readiness false.

### P3 Nice-to-have

- Consider 8U-4 backend dense graph route contract docs-only.
- Alternatively stabilize backend integration object shape with additional controlled fixture tests before route design.

## H. Next Recommendation

Prefer 8U-4 backend dense graph route contract docs-only or backend service stabilization.

Do not modify frontend until backend integration output contract is stable.
