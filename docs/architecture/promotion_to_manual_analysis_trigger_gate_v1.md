# Promotion To Manual Analysis Trigger Gate v1

## Purpose

This document defines the relationship between the Analysis-ready Promotion Gate and a later Manual Analysis Trigger phase.

Promotion gate completion does not automatically run analysis.

A later Manual Analysis Trigger Design and Runtime are required.

## Manual Analysis Trigger Requirements

A future Manual Analysis Trigger must check:

- promotion gate status is eligible
- human promotion decision exists
- analysis scope is selected
- coverage limitations are displayed
- rejected items and groups are excluded
- weak warning is included
- dedup preview and group review warnings are included
- privacy blockers are absent
- audit timeline is complete
- no side-effect flags were set by prior gates
- manual trigger operator acknowledges no full-web or official verification claim

## What Promotion Allows

Promotion eligibility allows a future manual analysis trigger to be considered.

It may provide a promoted safe input preview that a later manual trigger phase can inspect.

## What Promotion Does Not Allow

Promotion does not allow:

- automatic analysis
- production Evidence Layer write
- production case creation
- production review queue creation
- production dedup
- report generation
- Sandbox fixture generation
- public event generation
- B-end report generation
- official verification claims
- full-web coverage claims
- full-platform coverage claims
- risk score updates

## Report, Sandbox, And Public Event Boundaries

Report, Sandbox, and public event generation still require separate later gates.

Manual analysis output should not automatically become:

- Summary Report
- B-end report
- Sandbox fixture
- public event page
- public claim

Those outputs require separate review, boundary, and generation gates.

## Carry-Forward Requirements

The future manual analysis trigger must carry forward:

- rejected excluded list
- weak evidence warnings
- dedup group warnings
- duplicate evidence must not amplify risk warning
- coverage limitation acknowledgement
- selected sample limitation
- provider output is evidence, not truth
- no official verification
- no causal proof
- audit ids and decision ids

## Suggested Future Phases

- 7B: Analysis-ready Promotion Gate Runtime
- 7C: Manual Analysis Trigger Design
- 7D: Manual Analysis Trigger Runtime
- 7E: Analysis Result Boundary / Report Gate Design
- 7F: Sandbox / Public Event Generation Gate Design

## Boundary Wording

Use:

- analysis-ready promotion gate
- eligible for future manual analysis trigger
- `analysis_included=false` until manual trigger
- rejected excluded
- weak warning
- duplicate evidence must not amplify risk
- provider output is evidence, not truth
- audit-visible
- coverage limitation acknowledged

Avoid:

- analysis completed
- production Evidence imported
- production case created
- report generated
- official verified
- full-web coverage
- risk score updated
- auto analysis

