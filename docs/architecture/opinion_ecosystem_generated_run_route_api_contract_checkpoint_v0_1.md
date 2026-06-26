# Opinion Ecosystem Generated-run Route/API Contract Checkpoint v0.1

## A. Purpose

This checkpoint defines what must be true before a future API route exposes generated run output from the Opinion Ecosystem minimum real-run wrapper.

The checkpoint is a planning boundary. It does not implement an API route.

## B. Current Decision

No API route is approved in 8S-3.

8S-3 only plans the contract.

API implementation requires a later explicit backend route implementation phase.

The existing 8S-2 backend wrapper is service-level only. It produces `sentigraph_opinion_ecosystem_run_v0_1` from an in-memory safe fixture, but it is not reachable through HTTP.

## C. Future Route Candidate

Candidate routes for a later implementation phase:

```text
GET /api/v1/opinion-ecosystem/generated-runs/{run_id}
POST /api/v1/opinion-ecosystem/generated-runs/local-fixture
```

These are candidates, not implemented routes.

Route naming may change after backend route inspection, but any final route must preserve the same safety boundaries:

- local fixture or selected sample only
- no real API
- no real LLM
- no collector
- no exchange dir read
- no URL fetch
- no scraping
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no response execution

## D. Future Request Boundaries

Future POST must only accept safe local fixture or selected sample references.

It must not accept:

- raw author identifiers
- raw author names
- profile URLs
- cookies
- tokens
- sessions
- browser profiles
- raw evidence rows
- private messages
- real exchange dir paths
- absolute private filesystem paths
- direct `evidence_items.jsonl` paths
- direct `evidence_items.csv` paths
- publish/send/post/execute requests

Recommended first request shape for a future route:

```json
{
  "input_source_kind": "in_memory_safe_fixture",
  "sample_id": "fixture_8s2_full",
  "requested_by": "local_operator",
  "dry_run": true
}
```

This sample request is illustrative only. It is not an implemented schema.

## E. Future Response Contract

Future response must wrap `sentigraph_opinion_ecosystem_run_v0_1` output.

It must include:

- `run_id`
- `run_schema`
- `run_status`
- model metadata
- `boundary_flags`
- `warnings`
- `blockers`
- `module_outputs`
- `runtime_side_effects`

It must not expose:

- absolute filesystem paths
- secrets
- raw author identifiers
- raw author names
- profile URLs
- cookies
- tokens
- sessions
- browser profile paths
- raw evidence rows
- private messages

The response must preserve all boundary flags and false runtime side-effect flags from the backend wrapper.

## F. Future Route Safety Gates

Before API implementation, require:

- backend generated-run wrapper tests passing
- no real API
- no real LLM
- no collector
- no file IO for first route slice unless separately approved
- no Evidence Layer write
- no production case
- no production `analysis_run`
- no runtime persistence unless separately approved
- no response text generation
- no publish/send/post/execute behavior
- no private collector access
- no real exchange dir read
- no `evidence_items` parsing unless separately approved

The first route slice should prefer an in-memory fixture registry or explicit test fixture factory over path-based input.

## G. Future Frontend Integration Gate

Frontend integration is allowed only after:

- route/API contract implementation is complete
- generated run response has model metadata and boundary flags
- blocked/manual-review states are tested
- default Opinion Ecosystem route smoke passes
- Dong/Sun route smoke passes
- no visible `undefined`
- no visible `NaN`
- no visible `[object Object]`
- no visible 500
- no publish/send/post/execute CTA
- no generated response text field
- no production-score wording

Frontend integration should remain behind generated-run labels until browser smoke confirms the UI distinguishes static fallback from generated backend output.

## H. Explicitly Deferred

The following remain deferred:

- real package row parsing
- real exchange dir read
- private collector access
- production Evidence import
- production case / `analysis_run`
- B-end report runtime
- Sandbox/public event runtime generation
- generated response text
- Strategy Lab runtime
- calibration
- manual playtest / recording

Deferred means not implemented, not implied, and not available through hidden UI or API behavior.
