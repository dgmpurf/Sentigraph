# Internal Operator Future Runtime Slice Candidates v0.1

## A. Purpose

This document compares possible future internal-operator runtime slices after 8T-23 tests.

It is docs-only. It does not approve implementation, does not modify route behavior, does not add UI, and does not permit runtime expansion.

## B. Candidate A: Pause

State: allowed.

Pause is the lowest-risk option. It is recommended if there is no immediate operator route need.

Pause preserves:

- disabled-by-default route behavior
- synthetic/test-only enabled mode
- no frontend UI
- no auth/session/cookie/token runtime
- no storage
- no evidence row preview
- no production import
- no collector bridge

## C. Candidate B: No-behavior-change Route Guard Design Docs-only

State: allowed.

This is recommended if continuing. It would design future guard/helper extraction or hardening without code.

Possible design topics:

- route guard helper concept
- safe error helper concept
- env gate helper concept
- response serialization safety concept
- static scan maintenance design
- no public alias regression mapping

This candidate must not implement helpers.

## D. Candidate C: No-behavior-change Route Guard Implementation

State: not approved now.

This would require:

- accepted design
- explicit user approval
- test-first implementation
- no route behavior change
- targeted tests
- full relevant validation
- rollback plan

Until those prerequisites exist, implementation remains blocked.

## E. Candidate D: Auth/local-only Runtime

State: not approved now.

This is higher risk than guard design. It requires separate design, test plan, explicit approval, and safe denial behavior.

It must not add sessions, tokens, cookies, accounts, browser profile state, or hidden authorization behavior unless separately approved in a later gate.

## F. Candidate E: Internal Operator UI

State: not approved now.

This requires separate implementation approval, frontend safety tests, browser smoke, internal-only routing, and no active actions.

Any future UI must clearly state:

- internal operator only
- metadata-only
- review-only
- no production import
- no Evidence Layer write
- no collector run
- no real API / LLM
- no evidence row preview unless separately approved

## G. Candidate F: Storage / Evidence Row Preview / Production Import

State: blocked.

These are not near-term runtime candidates.

Storage requires a retention/deletion and privacy threat model.
Evidence row preview requires a bounded reader, redaction, privacy scan, and explicit approval.
Production import requires review completion, dedup/promotion gates, Evidence Layer policy, and human authorization.

## H. Recommendation

Recommended if continuing:

8T-25 no-behavior-change route guard design docs-only.

Recommended alternative:

Pause.

Do not implement:

- UI
- auth/local-only runtime
- storage
- evidence row preview
- production import
- collector runtime/API bridge
- public/C-end/B-end/customer exposure
