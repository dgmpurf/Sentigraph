# Manual Analysis Trigger Design v1

## Purpose

Manual Analysis Trigger defines a future manual-only trigger that may start analysis from an eligible review-only case after Analysis-ready Promotion Gate approval.

The trigger exists to ensure that a human explicitly decides when a promoted review-only evidence set is ready to become analysis input.

This document is design only. It does not implement runtime, run analysis, write Evidence Layer records, create production cases, or generate reports, Sandbox fixtures, or public event pages.

## Core Principle

Manual Analysis Trigger is the first point where analysis may be requested, but this document does not implement that request.

The trigger must be:

- explicit
- human-initiated
- auditable
- coverage-aware
- privacy-bounded
- warning-preserving
- side-effect-free until a future runtime exists

Promotion gate eligibility is necessary but not sufficient for automatic analysis. Eligibility means only that a future manual trigger can be considered.

Provider output remains evidence, not truth.

## Required Prior Chain

Manual Analysis Trigger can be considered only after:

- Review-only Case exists.
- Analysis-ready Promotion Gate exists.
- Promotion gate status is `eligible_for_future_manual_analysis_trigger`.
- Promotion decision audit exists.
- Review Queue Completion Gate passed.
- Dedup Preview is ready.
- Dedup Group Review is safe enough or completion criteria are satisfied.
- No `privacy_hold` blockers exist.
- No unresolved `needs_more_source` blockers exist.
- Rejected items and rejected groups are excluded.
- Weak items and weak groups are warning-marked.
- Coverage limitations are acknowledged.
- Provider output is acknowledged as evidence, not truth.
- All included candidates remain future-runtime-only and must not be treated as already analyzed.

If any required prior gate is missing, unsafe, incomplete, or inconsistent, the trigger state must be `incomplete`, `blocked`, or `privacy_hold`.

## Non-Goals

This design does not implement:

- runtime code
- automatic analysis
- production Evidence Layer write
- production case creation
- production review queue creation
- report generation
- Sandbox fixture generation
- public event page generation
- official verification upgrade
- trust upgrade
- provider execution
- collector execution
- live collection
- URL fetching
- scraping
- real API integration
- real LLM integration

## Output Statuses For Future Runtime

### `trigger_ready_for_future_runtime`

All prior governance gates and acknowledgements are complete enough for a future manual trigger runtime to be implemented or invoked.

This status still does not run analysis and does not change production evidence state.

### `incomplete`

Required promotion, audit, dedup review, coverage acknowledgement, or warning propagation data is missing.

### `blocked`

The input set has unresolved governance blockers, side-effect attempts, trust upgrade attempts, rejected evidence leakage, or duplicate amplification risk.

### `privacy_hold`

Privacy, private-content, raw-identifier, or secret-like risk is present. Downstream analysis must stop until a separate privacy review resolves the issue.

## Design Requirements

Future runtime must preserve:

- rejected item and group exclusion
- weak evidence warnings
- dedup warnings
- duplicate evidence non-amplification
- coverage limitation notes
- provider-output-is-evidence-not-truth notes
- no official verification claim
- no full-web or full-platform coverage claim
- append-only audit traceability

Future runtime must not silently convert promotion eligibility into analysis execution.

## Boundary Language

Use:

- manual analysis trigger
- human-initiated
- explicit audit
- future runtime only
- promotion gate eligibility is not automatic analysis
- rejected excluded
- weak warning
- duplicate evidence must not amplify risk
- provider output is evidence, not truth
- coverage limitation

Avoid:

- analysis completed
- report generated
- official verified
- full-web coverage
- risk score updated
- auto analysis
- production evidence imported

