# Opinion Ecosystem 8U-2 Dense Graph Generated-run Attachment Report v0.1

## A. Decision / Status

phase = 8U-2

task = backend_only_dense_graph_generated_run_attachment

decision = ready

privacy_issue_stop = no

backend_only = yes

frontend_changed = no

route_changed = no

api_route_added = no

code_changed = yes

tests_changed = yes

dense_graph_adapter_implemented = yes

dense_graph_builder_reused = yes

generated_run_attachment_created = yes

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

- `backend/app/services/opinion_ecosystem_dense_graph_generated_run_adapter.py`
- `backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py`
- `docs/health/opinion_ecosystem_8u_2_dense_graph_generated_run_attachment_report_v0_1.md`

Added backend-only adapter functions:

- `build_dense_graph_generated_run_attachment`
- `build_dense_graph_generated_run_attachment_from_evidence_items`

The adapter reuses the 8U-1 dense graph builder and packages its output as a generated-run-compatible attachment object. It does not add a frontend surface, API route, file download, Evidence Layer write, production case, or production analysis run.

## C. Attachment Output Summary

Attachment contract:

- `attachment_schema = sentigraph_opinion_ecosystem_dense_graph_attachment_v0_1`
- `attachment_status = ready_for_backend_generated_run_surface | degraded_missing_boundary_flags | blocked`
- `source_run_id`
- `sample_id`
- `created_at`
- `graph_schema = sentigraph_opinion_ecosystem_dense_graph_run_v0_1`
- `graph_summary`
- `nodes_preview`
- `edges_preview`
- `timeline_buckets`
- `boundary_flags`
- `runtime_side_effects`
- `warnings`
- `blockers`
- `human_review_required = true`

Future-frontend metadata included:

- `people_cluster_proxy_count`
- `influence_core_proxy_count`
- `content_aggregate_proxy_count`
- `echobox_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode = dense_sandbox_proxy_graph`
- `suggested_max_render_nodes`
- `suggested_max_render_edges`
- `density_note`

The adapter only exposes safe node and edge preview fields. Unknown node metadata is not copied into previews.

## D. Safety Behavior

The attachment remains anonymous aggregate/proxy only.

It does not expose raw author identifiers, usernames, account IDs, profile URLs, browser profile paths, cookies, sessions, tokens, private messages, response text, generated public messages, target-user lists, persuasion scores, truth scores, official verification claims, prediction probabilities, psychological profiles, or personality diagnoses.

If forbidden fields appear in dense graph nodes, edges, metadata, or top-level payload, attachment creation returns a blocked attachment without exposing forbidden values.

Missing boundary flags create a degraded attachment with `missing_boundary_flags`, not a production-ready claim.

Runtime side-effect flags are preserved as false. If a required side-effect flag is true, the attachment is blocked.

The adapter does not represent a real social graph, official verification, causal proof, prediction, production score, generated response, or platform action.

## E. Validation Commands and Results

Red phase:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
result = failed as expected before implementation
reason = ImportError for missing opinion_ecosystem_dense_graph_generated_run_adapter service
```

Green / required validation:

```text
python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
result = passed, 9 passed

python -m pytest backend/app/tests/test_opinion_ecosystem_dense_graph_builder.py
result = passed, 11 passed

python -m pytest backend/app/tests/test_analysis_request_golden_contracts.py
result = passed, 7 passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_generated_run_adapter.py
result = passed

python -m py_compile backend/app/services/opinion_ecosystem_dense_graph_builder.py
result = passed

git diff --check
result = passed

git status --short
result = three expected untracked files:
- backend/app/services/opinion_ecosystem_dense_graph_generated_run_adapter.py
- backend/app/tests/test_opinion_ecosystem_dense_graph_generated_run_adapter.py
- docs/health/opinion_ecosystem_8u_2_dense_graph_generated_run_attachment_report_v0_1.md
```

## F. Not Run and Why

- Frontend build was not run because no frontend code changed.
- Browser smoke was not run because no UI or route changed.
- Collector was not run because 8U-2 is backend-only adapter work.
- Real APIs were not called.
- Real LLMs were not called.
- Full backend pytest was not run because the approved slice requires focused adapter, builder, and golden-contract validation.

## G. Issues

### P0 Privacy / Safety

No P0 issue identified.

### P1 Contract Blocker

No P1 blocker identified.

### P2 Non-blocking Limitation

- Attachment is backend-only and not wired to any route.
- Attachment previews are intentionally bounded and safe, not a full graph export contract.
- Dense graph values remain deterministic and mock-default, not empirically calibrated.
- Attachment status is for backend-generated-run surface readiness only, not frontend readiness.

### P3 Nice-to-have

- Consider a future backend dense graph route contract after this attachment contract stabilizes.
- Keep frontend frozen until backend output semantics are settled.

## H. Next Recommendation

Prefer 8U-3 backend dense graph route contract or generated-run integration decision.

Do not modify frontend until backend attachment/output contract is stable.
