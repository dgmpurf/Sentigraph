# Post-P04 B05 identity-ready versioned backend service slice

## Lifecycle

- Goal: `SENTIGRAPH_POST_P04_VERSIONED_B05_IDENTITY_READY_BACKEND_SERVICE_SLICE_IMPLEMENTATION_V0_1R2`
- Terminal target: `IMPLEMENTATION_V0_1R2_STATUS_PROPAGATION_CORRECTED_CANDIDATE_COMPLETE_READY_FOR_MAINLINE_INDEPENDENT_REVIEW`
- Lifecycle: local uncommitted candidate; not staged, committed, or pushed
- Base branch: `main`
- Base HEAD and `origin/main`: `c6f12e5321d0b7efdfac41aa1453744e3bf3fa69`
- Base tree: `73ff05fe7129c8399845ecc1ac4adbfedb6f9e8a`
- Authority: fresh V0.1R2 `1/0/1` before the exact regression-test mutation, then `1/1/0 CONSUMED_NONREUSABLE`

The predecessor V0.1 implementation remains terminal as `STOP_WITH_EXACT_FAILURE_STAGE` at `combined_legacy_regression_validation`. V0.1R1 remains a completed local candidate whose exact transfer archive passed Mainline integrity review but whose code review remained `NEEDS_FIX` under `B05-V02-STATUS-PROP-001`. Both predecessor authorities remain consumed and nonreusable; V0.1R2 is a distinct successor and does not retry or reclassify either result.

## Accepted successor input

Mainline bound the exact V0.1R1 eleven-path uncommitted candidate before V0.1R2 activation. Its eight tracked-file diff was 59,456 bytes with SHA-256 `d563f41b3ce4a35f64e89e22e7b2d14537c6293bb26fa49af3499b51753a9ea1`. The V0.1R2 pre-mutation guard reproduced all eleven statuses, byte counts, SHA-256 identities, raw working blobs, zero staged paths, base HEAD/tree, and the exact `0/8/3` staged/modified/untracked topology.

## Corrected design

The candidate-caused B03 purity failure was corrected without weakening the pure-module contract:

- the server-owned internal-alpha orchestrator now constructs the final bounded `review_subject_identity` using the versioned upstream material;
- the orchestrator strips `review_subject_identity_material` before calling the pure projection bridge;
- the projection bridge has no `app` import root and performs only local/stdlib structural, field-order, status, binding, and digest-shape validation;
- the projection bridge appends only an already-constructed safe mapping to the distinct v0.2 projection;
- no filesystem, environment, network, database, Provider Result, or package access was added to the projection bridge.

The two stale post-P04 frontend assertions were maintained in tests only. B05 negative assertions now inspect the exact structurally isolated Local-exchange branch, bounded by `if (selectedReviewView === LOCAL_EXCHANGE_PROJECTION_REVIEW_VIEW)` and `const projection = routeState.projection`, together with the Local-exchange API helper. The scoped surface continues to reject retry, polling, prefetch, filename/path/root/adapter/config inputs, button/form mutation controls, decision-ledger controls, and persist/promote/publish/export controls. Frontend product code was not changed.

Mainline finding `B05-V02-STATUS-PROP-001` identified that V0.1R1 dropped a structurally valid ready identity whenever the legacy 52-field prefix required manual review. V0.1R2 corrects only that propagation defect:

- ready identity package binding first uses a safe package name already present in the legacy projection and otherwise uses a safe bounded `staging_candidate.package_name` from the supplied versioned upstream mapping;
- the bridge still performs no Provider Result, package, filesystem, environment, database, or network access;
- after validation, the exact supplied ready identity is always appended as field 53, independent of the legacy prefix review status;
- a legacy `manual_review_required` / `upstream_manual_review_required` prefix is preserved while `review_subject_identity.identity_status` remains `ready`;
- blocked identity behavior and the v0.1 52-field callable remain unchanged.

## Contract preservation

- Current v0.1 schema remains `sentigraph_local_exchange_review_only_candidate_projection_v0_1`.
- Current v0.1 version remains `0.1`.
- Current v0.1 ordered field count remains 52.
- The service-only v0.2 schema remains `sentigraph_local_exchange_review_only_candidate_projection_v0_2` with the exact v0.1 semantic field order followed by `review_subject_identity`, for 53 fields total.
- No route, environment gate, or frontend exposure was added for v0.2.
- Historical B05 reviews and existing formal decisions were not retroactively rebound.

## Validation receipt

All three V0.1R2 pytest budgets were used exactly once with no retry.

1. RED, exact new regression only: 1 expected failure, proving the V0.1R1 52-field identity-drop behavior.
2. GREEN: 7 passed, 0 failed, 0 skipped, 0 errors.
   - complete `test_post_p04_b05_identity_ready_versioned_surfaces.py`
   - exact B03 pure-module test
3. Frozen five-file combined legacy regression: 160 passed, 0 failed, 0 skipped, 0 errors.

One changed-Python-file `py_compile` invocation and one `git diff --check` invocation remain to be performed after this report is created. Their results are returned in the terminal evidence and are not anticipated here.

## Candidate path identities after the V0.1R2 product/test correction and before this report update

| Status | Path | Bytes | SHA-256 | Working blob |
| --- | --- | ---: | --- | --- |
| M | `backend/app/schemas/local_exchange.py` | 4942 | `5eea2f12c2f41a8adaaa60c5da75ef0f4fd97b4852cd0852d54bb282339acbcd` | `5d28953a43fc6a5fbe9ac31e907f6c095f4f1ac5` |
| M | `backend/app/services/internal_alpha_local_exchange_review_projection.py` | 16721 | `c60708fb4703bc82c997bd064293a98a05a22c3efb3f01138491f94b80777077` | `a52099b8bd245ae6f9b1bd050e38ae52a4107ad7` |
| M | `backend/app/services/local_exchange_reader.py` | 19301 | `88878684640af86def872a2fb57b58746b68dc378f8300ae6a2d128d2b735a54` | `c14c6f57a009d6352d15b95e5241601414077970` |
| M | `backend/app/services/local_exchange_review_only_projection_bridge.py` | 26601 | `e9f66bfe2f880c2c09c17e71a800b104f1d5c0bfcb120b36354e0312c042a78a` | `e2787266a5b014a74feb9880931bd6649b288b51` |
| M | `backend/app/services/local_exchange_review_only_staging_bridge.py` | 26530 | `56d42e8e746f4bf56610d05b540cb696b6d3afa622a00db0f3c58b2293af9dea` | `39760e1b123cc32512052e2b94b19b2b52058bd6` |
| M | `backend/app/services/private_collector_package_resolver.py` | 26846 | `a2317ef73f313f9a43c7189d6bd32ab9a6a47bfa96268087fe00c2152c7a1c86` | `57835df7ab38a7ff938a0077f3759a4c458d4699` |
| M | `backend/app/services/private_collector_provider_result_reader.py` | 24604 | `2803549a22d267ddbab99dac3e501d5a23c35d01edccb3562813d63836ade3d4` | `a31c74346183435684c832eb7d3851b7fbc1120e` |
| M | `backend/app/tests/test_mvp_b05_p2_internal_alpha_local_exchange_review_projection.py` | 43147 | `aaf78fd3625766c3e092ce3a626d27486405bb25339e0f0da60044c0b113147d` | `2a3f4a3070c613d7dce172442c850c59cb39440b` |
| ?? | `backend/app/services/b05_review_subject_identity.py` | 9988 | `f84ad527acf5b0665a71f1f3b244ac9ce415878357633bde621734e6711a691b` | `8bb6c89cd957edee2027b8c1721edf97c284366c` |
| ?? | `backend/app/tests/test_post_p04_b05_identity_ready_versioned_surfaces.py` | 15783 | `a8186a66336ff23db7c6212e88b893c421cff8a6d5d96c7d14a4aba23d013455` | `7bdf06a679a8d5efd6242a4a41b2d51605d8a02b` |

This report is the eleventh and final allowed candidate path. Its own final bytes, SHA-256, and working blob are reported externally after creation to avoid a self-referential identity claim.

## Hard-zero ledger

- Real Provider Result/package/metadata reads: 0
- Provider/collector execution: 0
- Runtime/server/browser/HTTP/B05: 0
- SQLite/formal-decision access: 0
- Analysis/dense-graph/report execution: 0
- Evidence Layer/Review Queue/trust/production mutation: 0
- Project Source access/change: 0/0
- Frontend product mutation: 0
- Stage/commit/push: 0/0/0
- External network, screenshot, public/export/delivery: 0
