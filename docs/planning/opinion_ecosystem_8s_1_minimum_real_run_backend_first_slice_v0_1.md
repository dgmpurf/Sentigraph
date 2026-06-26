# Phase 8S-1 Minimum Real-run Backend First Slice Plan v0.1

## A. Decision

```text
phase = 8S-1
decision = backend_contract_design_only
current_state = ready_for_minimum_real_run_backend_contract_design
next_state_if_ready = ready_for_8S_2_backend_minimum_real_run_contract_implementation
```

This phase creates the contract and test plan for the first minimum real-run backend slice. It does not create runtime behavior.

## B. Why Not API Yet

The 8R decision kept static UI as the demo default and did not approve API integration for the Opinion Ecosystem model-card and screenshot-smoke path.

The first minimum real-run step should therefore remain backend-only. Its purpose is to define and then produce a generated local run object that can be tested without frontend routing, browser state, API contracts, or user-visible runtime behavior.

API work should wait until a later checkpoint approves:

- endpoint shape
- persistence expectations
- frontend consumption behavior
- manual review wording
- public boundary labels
- failure and blocked-state UI behavior

## C. Why Not Manual Playtest Or Recording Yet

```text
manual_playtest_status = deferred_until_minimum_real_run
recording_status = deferred_until_minimum_real_run
```

Manual playtest and recording are deferred because the current product decision prioritizes a minimum backend real-run chain first. A recording before this step would still be based on static or mock UI behavior, which is not the next validation target.

The next credible playtest or recording checkpoint should happen only after the minimum real-run backend output exists and its boundaries are visible in the planned experience.

## D. Recommended 8S-2 Implementation Slice

Future 8S-2 should be:

```text
backend-only pure-local generated run wrapper around existing calculator
no API
no frontend
no runtime persistence
no file IO except in-memory fixture
test-first
```

Recommended future implementation shape:

- inspect `backend/app/services/opinion_ecosystem_mock_calculator.py`
- reuse the existing pure-local calculator entrypoint after confirming current function names
- create a small wrapper that emits `sentigraph_opinion_ecosystem_run_v0_1`
- map existing module outputs into the canonical contract module keys
- include required boundary flags
- include required false runtime side-effect flags
- block forbidden fields and overclaim language through tests
- keep `human_review_required = true`
- keep response generation blocked

Suggested future files, subject to inspection:

```text
backend/app/services/opinion_ecosystem_minimum_real_run.py
backend/app/tests/test_opinion_ecosystem_minimum_real_run.py
```

These files are not created in 8S-1.

## E. Acceptance Criteria For This Docs-only Phase

8S-1 is complete when:

- `docs/architecture/opinion_ecosystem_minimum_real_run_backend_contract_v0_1.md` exists
- `docs/architecture/opinion_ecosystem_minimum_real_run_backend_test_plan_v0_1.md` exists
- `docs/planning/opinion_ecosystem_8s_1_minimum_real_run_backend_first_slice_v0_1.md` exists
- no backend code changed
- no frontend code changed
- no tests changed
- no package files changed
- no runtime files changed
- no Project Source files changed
- no real API or real LLM was called
- no collector was run or accessed
- no real exchange dir was read
- no URL was fetched
- no website was scraped
- safety boundaries remain explicit
- `git diff --check` passes
- docs-only scans pass or show only acceptable boundary-language matches

## F. Source Recommendation

After commit:

- update Source 00
- update Source 08
- update Source 09
- update Source 10

Do not update Source 11 unless Analysis Request, Provider, or Import Governance behavior changes.
