# Sentigraph Dual Read-only B05 Sample Registry and Frontend Selection Report v1.0

## Status and authority

- Milestone: `SENTIGRAPH_DUAL_READ_ONLY_B05_SAMPLE_REGISTRY_AND_FRONTEND_SELECTION_V0_1`
- Decision candidate: `ready`
- Starting repository: `dgmpurf/Sentigraph`
- Starting branch: `main`
- Starting HEAD: `93e68434a9ba6615bffb63cb1e310ec3a4f6e993`
- Approval scope: one bounded dual-sample read-only implementation, its tests, this health report, and exact-file commit and push.
- Fresh Goal activation: verified.
- Runtime or downstream authority created: none.

## Changed-file scope

Exactly these six repository files comprise the authorized change:

1. `backend/app/services/internal_alpha_local_exchange_review_projection.py`
2. `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py`
3. `frontend/src/api/sentigraphApi.js`
4. `frontend/src/pages/InternalAlphaReviewConsole.jsx`
5. `backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py`
6. `docs/health/sentigraph_dual_read_only_b05_sample_registry_and_frontend_selection_report_v1_0.md`

No route, B01/B03 bridge, application shell, package, lockfile, fixture, configuration, Project Source, or runtime-artifact file changed.

## Test-driven contract migration

The two authorized test files were changed first.

The genuine RED run used the bounded two-file pytest command and excluded the two route-runtime tests required by the approval. It produced six assertion failures, all attributable to the not-yet-implemented historical registry entry and frontend dual-sample selection/cache contract. There were no collection, import, or unrelated failures.

After implementation, the same bounded command passed:

```text
64 passed
```

The tests now establish:

- an immutable two-entry backend registry in exact order;
- exact handle-to-basename mapping for both entries;
- enabled, route-mode, and capability-label parity;
- one injected builder path per handle with no cross-handle basename use;
- an exact ordered two-handle frontend allowlist;
- preservation of the current sample as index-zero default;
- an explicit read-only sample selector with bounded human-facing labels;
- independent per-handle request state and one request at most per handle per page mount;
- no retry, prefetch, persistence, or mutation control.

## Backend registry

The default immutable registry contains exactly two ordered entries:

1. `helldivers2-psn-demo` maps to `provider_result_helldivers2-psn-demo_20260720_123627.json`.
2. `helldivers2-psn-demo-20260614` maps to `provider_result_helldivers2-psn-demo_20260614_055754.json`.

Both entries remain enabled and retain the existing read-only route mode and capability label. The existing current sample remains first and therefore remains the default. The registry builder, validation behavior, route, and projection contract were not changed.

## Frontend API and selection

The safe sample-handle allowlist contains exactly the same two handles in backend order. The existing GET helper, URL encoding, strict 52-field normalizer, and contract-mismatch behavior remain unchanged.

The Internal Alpha Review Console now provides an explicit selector only within the local-exchange projection review surface:

- `Current curated sample` selects the existing default handle.
- `Accepted historical sample` selects the newly registered historical handle.

State is keyed by safe sample handle. Entering or switching within the surface requests only a selected handle that has not already been requested during the current page mount. Returning to a previously requested handle reuses its retained in-memory state. No automatic retry, polling, prefetch, persistence, or write action was added.

## Validation

- Focused bounded pytest: pass, `64 passed`.
- Nearby frontend-safety and B03 regression pytest: pass, `35 passed`.
- Python syntax compilation for the changed backend service and two changed Python tests: pass, three files.
- Frontend production build: pass, 4,028 modules transformed.
- Build warnings: existing Vite chunk-size advisory only; no build failure.
- `git diff --check`: pass before finalization.
- Static changed-file and authority scan: pass.
- Frontend B05 helper call sites in the page: exactly one.
- Frontend normalizer field count: unchanged at 52.
- Route files and route behavior: unchanged.
- Dependency files and installed dependency set: unchanged.

## No-side-effect ledger

- Real B05 GET attempts / completed: `0 / 0`
- Route-runtime tests executed: `0`
- Backend or frontend server starts: `0 / 0`
- Browser contexts / navigation / screenshots: `0 / 0 / 0`
- Provider Result or collector data reads: `0`
- Environment / stable receipt / CIB / gate access: `0 / 0 / 0 / 0`
- Application-factory imports: `0`
- Database / persistence writes: `0 / 0`
- Production / public / export / delivery actions: `0 / 0 / 0 / 0`
- Project Source reads / changes: `0 / 0`
- Dependency installs or updates: `0`
- Product route changes: `0`

The frontend build and bounded static/unit tests were local validation only. They did not exercise protected runtime behavior.

## Directly established

- The backend exposes a deterministic immutable two-entry sample registry.
- The frontend exposes the same two handles in the same order.
- The existing current sample remains the default.
- The review surface provides bounded human-readable selection.
- Each handle has independent in-memory request state and at-most-once request behavior per page mount.
- Existing GET normalization and read-only boundaries remain intact.
- The authorized implementation and regression suite pass.

## Not established and next boundary

- No real historical Provider Result was read.
- No real B05 response was obtained.
- No browser-visible behavior was validated.
- No runtime configuration, CIB, gate, persistence, production, or delivery readiness was established.
- No follow-on execution authority exists.

The new handle is implemented as a read-only selectable capability but has not yet been independently validated through a real B05 GET or browser-visible review. Any such validation requires a separate fresh approval and Goal.
