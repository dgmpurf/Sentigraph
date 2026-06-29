# Internal Operator Read-only Staging Route/UI Readiness v0.1

## A. Current Helper Chain

Current private collector metadata handoff chain:

- 8T-3 package resolver: resolves configured local package references by metadata and required-file presence.
- 8T-4 provider result reader: reads safe provider result metadata and resolves the referenced package through the metadata-only resolver.
- 8T-5 local exchange smoke: proves a synthetic metadata-only local exchange fixture can produce a safe handoff summary.
- 8T-8 review-only staging helper: creates in-memory review-only staging candidates and gate summaries from safe handoff metadata.
- 8T-9 integration smoke: proves the fixture chain from provider_result JSON to safe review-only staging summary.

This chain is local metadata-only governance support.

It is not a collector runtime.

It is not production Evidence import.

It is not production case creation.

It is not `analysis_run` creation.

It is not route/UI implementation.

## B. Readiness Matrix

| Area | Readiness | Notes |
| --- | --- | --- |
| package resolver | ready for internal helper use | Safe metadata-only package resolution is covered by targeted tests. |
| provider result reader | ready for internal helper use | Safe provider metadata reading and package handoff are covered by targeted tests. |
| local exchange fixture smoke | ready for fixture-level internal smoke | Uses synthetic `tmp_path` fixtures only. |
| review-only staging helper | ready for in-memory/test-fixture use | Produces safe candidate and gate summaries without persistence. |
| persistent staging storage | not ready | No storage contract or approval exists. |
| backend route | not ready for implementation yet | Needs route contract, auth/operator boundary, safe response schema, and audit behavior first. |
| frontend UI | not ready for implementation yet | Must wait for route contract and safe response schema. |
| production import | blocked | Review-only staging must not write production Evidence. |
| Evidence Layer write | blocked | No Evidence Layer write is approved. |
| production case | blocked | No production case creation is approved. |
| `analysis_run` | blocked | No analysis run creation is approved. |
| report/Sandbox/public event | blocked | No report, Sandbox, or public event generation is approved. |

## C. Route Readiness Decision

Recommended decision:

```text
not_ready_for_route_implementation_yet
ready_for_docs_only_internal_operator_read_only_route_contract
```

A route would expose an operator surface. That surface needs a separate route contract before implementation because it must define:

- internal operator access boundary
- disabled-by-default or local-only configuration behavior
- safe response schema
- audit behavior
- blocker/warning semantics
- explicit exclusion of production actions
- explicit exclusion of raw evidence rows, raw identifiers, secrets, and absolute paths

The current helper chain is enough to design the route contract, but not enough to implement the route safely.

## D. UI Readiness Decision

Recommended decision:

```text
not_ready_for_ui_implementation_yet
ready_for_docs_only_operator_review_screen_contract_later
```

UI should wait until a route contract and safe response schema are designed.

Future UI must display safe metadata summaries only. It must not show:

- raw evidence rows
- raw comments
- raw author identifiers
- profile URLs as actual values
- absolute private paths
- secrets
- generated response text
- production import actions
- analysis run triggers
- report generation triggers
- public event generation triggers
- publish/send/post/execute actions

## E. Safe Future Route Shape, Design Only

A future internal operator route may eventually expose:

- `staging_candidate_id`
- `package_name`
- `case_id_hint`
- `validation_status`
- evidence/source/warning/error counts
- `review_status`
- `promotion_status`
- `allowed_actions`
- `blocked_actions`
- `safety_flags`
- blocker summary
- warning summary
- audit refs

It must not expose:

- evidence rows
- raw comments
- raw author identifiers
- profile URLs as actual values
- secrets
- absolute private paths
- production import actions
- `analysis_run` trigger
- report generation trigger
- public event generation trigger
- publish/send/post/execute actions

## F. Required Future Preconditions Before Route Implementation

Before route implementation, Sentigraph needs:

- route contract docs
- safe response schema
- internal operator auth boundary
- local-only config or disabled-by-default setting
- tests proving no raw evidence exposure
- tests proving no raw identifiers, secrets, or absolute paths are exposed
- tests proving no production actions are available
- audit strategy
- explicit decision on whether any persistent storage is allowed
- confirmation that no persistent storage is added unless separately approved

## G. Required Future Preconditions Before UI Implementation

Before UI implementation, Sentigraph needs:

- safe route implementation
- route tests passing
- reviewed operator copy
- UI contract that displays only safe summary fields
- UI action list limited to review-only actions
- UI boundary copy stating metadata-only and not production import
- UI tests or smoke checks proving no public or production actions are exposed
- no raw evidence rows, raw identifiers, secrets, absolute paths, response text, or production actions in UI
