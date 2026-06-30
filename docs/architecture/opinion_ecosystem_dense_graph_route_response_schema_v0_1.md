# Opinion Ecosystem Dense Graph Route Response Schema v0.1

## A. Purpose

This document defines the future response envelope for a dense graph backend route.

It is a contract reference only. No backend route, frontend integration, runtime file, collector job, or production data write is implemented in 8U-4.

## B. Success Response Schema

Future success response:

```json
{
  "response_schema": "sentigraph_opinion_ecosystem_dense_graph_route_response_v0_1",
  "route_status": "ready",
  "sample_id": "donglu-sunjihai-youth-football",
  "generated_run_integration": {},
  "graph_summary": {},
  "preview_limits": {
    "node_limit": 240,
    "edge_limit": 800,
    "include_previews": true
  },
  "boundary_flags": {},
  "runtime_side_effects": {},
  "warnings": [],
  "blockers": [],
  "human_review_required": true
}
```

Allowed `route_status` values:

- `ready`
- `degraded`
- `blocked`

Success response must not imply frontend readiness, route approval for public use, production readiness, official verification, causal proof, prediction, or complete coverage.

## C. Disabled Response Schema

Future disabled response:

```json
{
  "error_schema": "sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1",
  "route_status": "disabled",
  "error_code": "route_disabled",
  "message": "Dense graph route is disabled.",
  "path_exposed": false,
  "raw_metadata_exposed": false,
  "private_collector_path_exposed": false,
  "evidence_rows_exposed": false
}
```

Disabled response must not expose local file paths, private collector paths, runtime paths, package paths, raw rows, raw comments, or private metadata.

## D. Unsupported Sample Response Schema

Future unsupported sample response:

```json
{
  "error_schema": "sentigraph_opinion_ecosystem_dense_graph_route_error_v0_1",
  "route_status": "unsupported_sample",
  "error_code": "unsupported_sample",
  "sample_id": "requested-sample",
  "message": "Sample is not supported for dense graph route.",
  "path_exposed": false,
  "raw_metadata_exposed": false,
  "private_collector_path_exposed": false,
  "evidence_rows_exposed": false
}
```

`route_status = not_found` is also acceptable if that matches future route conventions.

Unsupported sample response must not reveal sample search paths, filesystem structure, private collector roots, or raw evidence rows.

## E. Preview Policy

Future route response may include safe previews only:

- `nodes_preview`
- `edges_preview`
- `timeline_buckets`
- `graph_summary`

Future route response must preserve:

- `people_cluster_proxy_count`
- `edge_count`
- `timeline_bucket_count`
- `recommended_visualization_mode = dense_sandbox_proxy_graph`
- `frontend_ready = false` until frontend is explicitly approved
- `production_ready = false`

Preview policy must exclude raw evidence rows, raw comments, raw author identifiers, private fields, and generated response text.

## F. Boundary Flags

Required boundary flags:

- `selected_sample_only`
- `not_full_web`
- `not_full_platform`
- `not_full_thread`
- `not_official_verification`
- `not_causal_proof`
- `not_prediction`
- `not_production_score`
- `no_auto_execute`
- `no_generated_public_response`
- `anonymous_aggregate_only`
- `human_review_required`

All boundary flags above must be present in future route response.

## G. Runtime Side-effect Flags

All runtime side-effect flags must be present and false:

- `called_real_api`
- `called_real_llm`
- `ran_collector`
- `accessed_private_collector`
- `read_real_exchange_dir`
- `fetched_url`
- `scraped_page`
- `wrote_evidence_layer`
- `created_production_case`
- `created_analysis_run`
- `generated_b_end_report_runtime`
- `generated_sandbox_runtime`
- `generated_public_event_runtime`
- `generated_response_text`
- `published_or_sent`
- `auto_executed`

If any side-effect flag would be true, future route response must be blocked.

## H. Error / Blocker Policy

Blocked response must avoid returning unsafe payload.

Warnings must not include forbidden values.

Errors and blockers must not include raw forbidden field values.

Error responses must not reveal:

- private collector paths
- local absolute private paths
- runtime file paths
- raw evidence row content
- raw comments
- raw author identifiers
- tokens, sessions, cookies, or browser profile paths
