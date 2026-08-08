# Sentigraph Post-ClassC P01 Governed Human-Review Decision UI Integration

## Milestone and baseline

- Milestone: `POST_CLASSC_P01_GOVERNED_HUMAN_REVIEW_DECISION_UI_INTEGRATION`
- Repository: `dgmpurf/Sentigraph`
- Branch: `main`
- Baseline HEAD: `8598f786cb1b876d16f8d5266e37aec9385ee312`
- Baseline tree: `2a824e9dbe0aff3ae621a3f88ebd4b1101de8719`
- Lifecycle: implementation and synthetic validation only; no live governed-decision runtime was exercised.

## Exact changed paths

1. `frontend/src/api/sentigraphApi.js`
2. `frontend/src/pages/InternalAlphaReviewConsole.jsx`
3. `frontend/src/pages/InternalAlphaReviewConsole.test.jsx`
4. `docs/health/sentigraph_post_classc_p01_governed_human_review_decision_ui_integration_report_v0_1.md`

Backend decision route and all backend product code remain unchanged.

## Implemented bounded contract

- The frontend exposes exactly two decision types:
  - `keep_pending_human_review`
  - `request_more_governance_review`
- Request construction is strict and contains only `request_schema`, `request_version`, and `decision_type`.
- Response normalization requires the exact ordered 13-field outer response contract and validates the bounded success invariants before returning only a UI-safe subset.
- Expected non-success responses map to fixed bounded frontend states; raw Axios errors, backend exceptions, nested decision objects, and nested receipts are not returned to the UI.
- The decision control is available only on a ready governed-record review projection when the selected decision is also present in server-owned `allowed_actions`.
- The Local-exchange review surface has no governed-decision control.
- Selection alone performs no POST. Confirmation is explicit.
- A ref latch limits the page mount to at most one POST attempt, regardless of success or failure.
- Automatic retry, polling, and GET-after-POST verification are absent.

The UI describes the ledger as internal, nonproduction, append-only, and human-review-only. It grants no trust approval, automatic trust upgrade, governed evidence mutation, analysis/report start, production/public/export/delivery action, correction/revocation, deletion, or reset authority. The backend route remains disabled by default and requires separate runtime authorization before any real use.

## Synthetic validation

- Component command: `npm.cmd --prefix frontend run test:component -- src/pages/InternalAlphaReviewConsole.test.jsx`
- First run: 23 passed, 1 failed because the new Local-exchange isolation test omitted the existing projection helper mock.
- Evidence-based correction: added the missing synthetic projection mock only; no product behavior or scope was broadened.
- Independent diff review tightened the control-wide eligibility rule so a missing/non-array server `allowed_actions` value, a missing human-review invariant, or an automatic-trust invariant mismatch disables the entire control rather than only the confirmation action.
- Final component result: 29 passed, 0 failed, 0 skipped, including the HTTP 200 idempotent-success and bounded expected-failure response paths.
- Frontend build command: `npm.cmd --prefix frontend run build`
- Frontend build result: PASS; 4028 modules transformed. The existing chunk-size advisory remained non-blocking.
- Validation type: local static/synthetic only.

## Hard-zero and preserved boundaries

- Backend/frontend live servers: `0 / 0`
- Live governed-decision POST: `0`
- Formal target / SQLite access: `0 / 0`
- Formal decision-ledger mutation: `0`
- Second formal decision: `0`
- Browser runtime / navigation / screenshot: `0 / 0 / 0`
- HTTP / B05: `0 / 0`
- Project Source access / change: `0 / 0`
- Trust / production / analysis / report / public / export / delivery authority: `0 / 0 / 0 / 0 / 0 / 0 / 0`
- Backend product-code changes: `0`

Historical Class C and browser-visible acceptance remain established. Screenshot acceptance remains not established and the screenshot route remains deferred. Collector G4 remains a separate, unselected backlog candidate.

This report does not claim live decision runtime acceptance, a second formal decision, operator-runtime readiness, trust approval, analysis acceptance, or production readiness.
