# Dedup Group Completion To Promotion Gate v1

## Purpose

This document defines how Dedup Group Review Completion Gate relates to the later analysis-ready promotion gate.

Completion gate does not promote.

Completion gate only allows future analysis-ready promotion gate design or runtime to be considered.

## Relationship To Future Promotion Gate

The future promotion gate must check:

- Review Queue Completion Gate passed
- Dedup Preview status is `preview_ready`
- Dedup Group Review Completion Gate passed
- no `privacy_hold`
- rejected groups and rejected items excluded
- weak groups and weak items warning-marked
- duplicate groups confirmed or resolved
- split groups resolved or blocked
- coverage limitations acknowledged
- audit timeline complete
- no production side-effect flags in prior gates
- human promotion decision exists

The promotion gate still does not automatically run analysis.

Manual Analysis Trigger from Review-only Case must be a later separate phase.

## What Completion Allows

If the gate status is `complete_enough_for_future_promotion_gate_design`, Sentigraph may consider designing or running a future promotion gate.

That future gate may decide whether a safe, review-only, dedup-aware input set can be prepared for manual analysis trigger.

## What Completion Does Not Allow

Completion does not allow:

- production dedup
- Evidence Layer write
- production case creation
- production Evidence Review Queue creation
- automatic analysis
- report generation
- Sandbox fixture generation
- public event page generation
- B-end report generation
- official verification claims
- full-web coverage claims
- full-platform coverage claims
- risk score updates

## Promotion Gate Carry-Forward Requirements

A future promotion gate must carry forward:

- rejected excluded status
- weak warning status
- duplicate group status
- audit ids and latest audit status
- coverage limitations
- selected public sample limitations
- provider output is evidence, not truth boundary
- no official verification boundary
- no causal proof boundary

## Human Promotion Decision

A future promotion gate must require an explicit human promotion decision.

The decision should acknowledge:

- the input remains review-derived evidence
- duplicates are governed but not production merged by this phase
- weak evidence remains weak
- rejected evidence remains excluded
- coverage is not full-web or full-platform
- analysis, reports, Sandbox output, and public event pages still require later gates

## Suggested Future Phases

- 7A: Analysis-ready Promotion Gate Design
- 7B: Analysis-ready Promotion Gate Runtime
- 7C: Manual Analysis Trigger Design
- 7D: Manual Analysis Trigger Runtime
- 7E: Report/Sandbox Generation Gate Design

## Boundary Wording

Use:

- dedup group review completion gate
- future promotion gate consideration
- confirmed group is still review-only
- duplicate evidence must not amplify risk
- `analysis_included=false`
- audit-visible
- weak warning
- rejected excluded
- provider output is evidence, not truth

Avoid:

- production dedup completed
- Evidence Layer merged
- evidence verified
- analysis-ready
- report-ready
- official verified
- risk score updated
- full-web coverage

