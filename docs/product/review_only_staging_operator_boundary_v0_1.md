# Review-only Staging Operator Boundary v0.1

Status: product/operator boundary only. This document does not implement roles, permissions, backend routes, frontend UI, Evidence import, production case creation, analysis runs, report runtime, Sandbox/public event runtime, public response generation, or platform actions.

## A. Operator Purpose

Review-only staging exists for internal operator review of safe metadata handoff.

The operator boundary is designed to help a human decide whether a metadata-only package should continue toward future evidence preview, evidence review, dedup, promotion, or case workspace gates.

Review-only staging does not approve production evidence, does not create a production case, and does not start analysis.

## B. What an Operator May Decide

An operator may decide:

- continue review
- request more metadata
- mark `manual_review_required`
- reject package
- block privacy issue
- request future evidence preview gate
- request future dedup gate
- request future promotion gate

These decisions remain review-only and audit-visible.

## C. What an Operator May Not Do in This Stage

An operator may not:

- approve production evidence
- create production case
- start `analysis_run`
- generate report
- generate public event
- publish / send / post / execute
- generate response text
- target individuals
- treat metadata as verified truth
- claim official confirmation or causal proof

Any action that would affect production evidence, external delivery, public output, or platform behavior requires a later explicit gate.

## D. User-facing Wording, Future Only

Allowed wording:

- "A review-only staging candidate exists."
- "This package is metadata-ready for human review."
- "Evidence import is still blocked."
- "This is not verified truth."
- "This is not an official conclusion."

Forbidden wording:

- "Verified event."
- "Officially confirmed."
- "Full web coverage."
- "Causal proof."
- "Ready to publish."
- "Recommended public response."
- "Target these users."
- "Predicted outcome probability."

Future UI copy must keep the difference between metadata readiness and evidence truth visible.

## E. Human Review Checklist

Before moving beyond review-only staging, a human operator should confirm:

- package metadata complete
- validation passed or warning understood
- privacy markers safe
- path resolution safe
- no forbidden fields
- no raw identifiers
- no private messages
- no evidence rows parsed in metadata stage
- no production import
- no public output

If any checklist item fails, the candidate must remain blocked, rejected, or manual-review-required.

## F. Future Promotion Gates

Future gates:

- evidence preview gate
- evidence review gate
- dedup gate
- evidence promotion gate
- case workspace gate
- `analysis_run` gate
- report gate
- Sandbox/public event gate

Passing review-only staging does not pass any of those future gates automatically.
