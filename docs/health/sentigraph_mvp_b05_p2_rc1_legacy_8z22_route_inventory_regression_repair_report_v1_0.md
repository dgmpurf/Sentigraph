# Sentigraph MVP-B05-P2-RC1 Legacy 8Z22 Route Inventory Regression Repair Report v1.0

## Decision and privacy classification

- Decision: the directly coupled legacy 8Z22 regression is repaired and locally validated within the approved test-only boundary.
- Classification: conditional prompt; internal-only, read-only, human-review-only validation evidence.
- `B05-P2-RC1 status = ready_pending_independent_ChatGPT_acceptance`
- This report does not claim independent ChatGPT acceptance, production readiness, trust approval, or authorization for B05-P3.
- No real artifact, package, endpoint, provider, collector, network source, LLM, database, persistence layer, review decision, public export, or delivery action was accessed.

## Approval and fresh Goal

- Exact approval SHA-256: `730ef32b63f905b5a7f5f8114ce94927e4f8331372c54694b71a044349265433`.
- A single fresh Goal was activated for `MVP-B05-P2-RC1 Legacy 8Z22 Route Inventory Regression Repair`.
- No earlier B05-P2 Goal was resumed or replaced.
- Prompt accounting before activation, in engineering/fixed/conditional/risk order: consumed `6/2/3/1`; remaining fixed/conditional/risk `0/1/1`.
- Prompt accounting after activation: consumed `7/2/4/1`; remaining fixed/conditional/risk `0/0/1`.

## Repository and starting state

- Repository: `dgmpurf/Sentigraph`.
- Branch: `main`.
- Starting commit and starting `origin/main`: `65bd00ba38881899f776f90e3d704648e7cb43db`.
- Starting alignment: ahead/behind `0/0`; tracked and nonignored worktree clean.
- The B05-P2 implementation commit and its exact seven-file surface were present.
- The frozen legacy test blob matched `4a336f8247a53eafa1bc5a73f96485305237254b`.
- The default local-exchange sample registry remained empty and no approved real-sample mapping was present.
- No prior RC1 report, RC1 completion commit, or later superseding task was present.

## Why B05-P2 was not independently accepted

The committed B05-P2 surface added a second valid internal review-console GET route. The directly coupled legacy 8Z22 test still asserted an exact inventory containing only the original F10 route. The implementation therefore remained completed but not independently accepted until this legacy regression was forward-repaired without weakening the route, frontend, or safety contracts.

## Exact baseline failure

Command, run from the repository root without filtering or deselection:

```text
python -m pytest backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py -q
```

- Collected: `17`.
- Passed: `16`.
- Failed: `1`.
- Deselected: `0`.
- Failed test: `test_route_family_is_get_only_and_internal_only`.
- Safe cause: the actual route inventory contained the approved B05 sample-handle route in addition to the original F10 projection-id route; no unrelated test failed.

## Forward repair contract

The obsolete exact-one-route assertion was replaced by an exact two-route set:

```text
/api/v1/internal/alpha/review-console/projections/{projection_id}
/api/v1/internal/alpha/review-console/local-exchange-projections/{sample_handle}
```

Both entries must remain internal and include `GET`; neither may expose `POST`, `PUT`, `PATCH`, or `DELETE`. The exact-set assertion prevents count-only, prefix-only, or at-least matching.

The obsolete `test_no_frontend_hook_was_added` assertion was renamed and forward-repaired to verify the current bounded integration:

- F10 governed-record review remains the default selected view.
- B05 retains its distinct helper, normalizer, view identifier, state, and allowlisted safe handle.
- The B05 request remains inside the state-dependent effect and occurs only after explicit selection of the B05 view.
- All six required read-only and non-production boundary lines remain present.
- The two exact frontend files expose no filename, path, root, adapter, configuration, approval-write, rejection, persistence, promotion, publication, export, or decision-ledger controls.
- `result_file_name` is not rendered by the page.
- AST-based assertions require the B05 decorator exactly once, require the `sample_handle` parameter, permit only the B05 service call in that function, and forbid mutation decorators for the B05 route.
- The original F10 route remains exact, and its governed-record gate and governed projection service remain distinct from the B05 route authority.
- Existing 8Z22 disabled-route, safe-projection, safe-error, no-public-alias, no-delivery, and no-file-read assertions remain intact.

## Exact changed-file allowlist

Only these two files are permitted to differ from the starting commit:

1. `backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py`
2. `docs/health/sentigraph_mvp_b05_p2_rc1_legacy_8z22_route_inventory_regression_repair_report_v1_0.md`

No product route, service, API registration, frontend, configuration, manifest, lockfile, or Project Source file was changed.

## Validation evidence

Full repaired 8Z22 module, with no filter or deselection:

```text
python -m pytest backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py -q
```

- Collected/passed/failed/deselected: `17/17/0/0`.

Exact coupled regression bundle, with no filter or deselection:

```text
python -m pytest backend/app/tests/test_8z_22_internal_alpha_review_console_disabled_backend_route_skeleton_smoke.py backend/app/tests/test_8z_30_internal_alpha_review_console_disabled_backend_route_consumption_smoke.py backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py backend/app/tests/test_mvp_f10_p2_governed_nonproduction_review_console_projection.py -q
```

- Collected/passed/failed/deselected: `97/97/0/0`.
- No skip, xfail, dynamic deselection, failure hiding, `-k`, or marker substitution was introduced.
- Static allowlist, route, frontend-contract, Markdown-fence, forbidden-content, and Git diff checks are required to pass before finalization.

No frontend build, browser run, `py_compile`, or separate product/runtime invocation was performed. No backend was manually started. The only executable validation was the approved bounded pytest surface; there was no separate route, helper, writer, SQLite, target, payload, source-reader, or persistence action.

## No-side-effect statement

This repair changes assertions and documentation only. It does not add a real registry mapping, read a real sample, mutate a review object, write to an evidence layer, make a trust or production decision, persist data, or provide public/customer delivery capability.

## Git evidence and terminal receipt boundary

- Pre-finalization base: `65bd00ba38881899f776f90e3d704648e7cb43db` on `main`, initially aligned `0/0` with `origin/main` and clean.
- Ready-only finalization requires exactly the two allowlisted files, cached diff validation, commit message `Repair MVP-B05-P2 legacy 8Z22 regression`, ordinary push to `origin/main`, exact parent verification, final `0/0` alignment, and a clean tracked/nonignored worktree.
- The final commit SHA, the report blob SHA, exact commit file inventory, push result, final alignment, and clean-state evidence belong in the terminal receipt. They cannot be embedded as self-referential final hashes in this tracked report without changing those hashes.

## Next boundary

The only next boundary is independent ChatGPT acceptance of B05-P2-RC1. This repair does not authorize B05-P3, a real sample mapping, artifact/package/endpoint replay, runtime execution, productionization, or any public/export/delivery action.
