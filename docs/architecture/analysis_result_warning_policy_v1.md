# Analysis Result Warning Policy v1

## Purpose

This document defines warning requirements for any future Analysis Result created from the review-only evidence governance chain.

The policy ensures that future result consumers can see the limits of source coverage, trust, review status, deduplication, exclusions, and audit traceability.

This document is design-only and does not generate Analysis Result output.

## Required Warnings

Future Analysis Result UI, API response, export metadata, Summary Report input, Sandbox input, public event input, and B-end report input must preserve these warnings when applicable.

### Coverage Limitation Warning

Analysis is based on reviewed available evidence scope, not all possible evidence.

The warning must state that the result is not full-web coverage, not full-platform coverage, and not full-thread coverage unless a separate future source-coverage gate proves otherwise.

### Provider Output Is Evidence, Not Truth

Provider output, external package output, vendor sample output, and collector output are evidence inputs.

They are not public truth, official verification, causal proof, or platform-certified conclusions.

### Not Official Verification

The result must not imply official verification by YouTube, Douyin, Bilibili, Reddit, Steam, a vendor, a collector, Sentigraph, or any platform unless a separate future official verification gate proves it.

### Not Full-Web Or Full-Platform Coverage

The result must state that the analysis uses a bounded reviewed evidence set and does not represent the whole web, whole platform, whole thread, or all public opinion.

### Weak Evidence Warning

Weak, low-trust, user-attested, screenshot-transcribed, externally assisted, or vendor-attested evidence may be included only with clear warning text.

Weak evidence must not be described as verified.

### Dedup Preview Warning

Deduplication and duplicate group review are governance aids.

Duplicate groups are not proof of truth and are not production evidence merges unless a later production gate allows it.

### Duplicate Evidence Must Not Amplify Risk

Duplicate evidence must not multiply primary risk, sentiment, coverage, or conclusion strength.

Duplicate count may be shown as context, evidence density, or repetition signal only when clearly labeled.

### Rejected Evidence Excluded

Rejected evidence and rejected groups must be excluded from result metrics, representative evidence, risk, sentiment, and conclusions.

The result must state that rejected evidence remains audit-visible but not analysis-included.

### Privacy-Excluded Evidence Not Used

Privacy-held, private-content, raw-identifier, or secret-like evidence must not be used in result metrics or representative evidence.

### Needs-More-Source Evidence Not Used

Evidence or groups marked `needs_more_source` must not be included until a later human review resolves the source requirement.

### Manual Trigger And Audit Trace Available

The result must link or reference the Manual Analysis Trigger audit, Promotion Gate audit, Review Action audit, Dedup Group Review audit, and exclusion decisions where available.

### Reviewed Scope Only

The result must state that it is based on reviewed evidence scope, not all possible evidence and not live platform state.

## Warning Placement

Warnings must appear:

- at the top of the Analysis Result
- near risk, sentiment, trend, and coverage metrics
- near representative evidence or quoted evidence previews
- in export and report downstream metadata
- in API response boundary blocks
- near Sandbox or public event generation controls when future gates use the result

Warnings must not be hidden only in footnotes when they materially affect interpretation.

## Required Boundary Block

A future Analysis Result should include a boundary block equivalent to:

- source scope
- coverage limitation
- weak evidence warning
- rejected evidence excluded
- duplicate evidence non-amplification
- provider output is evidence, not truth
- not official verification
- not full-web or full-platform coverage
- audit trace ids
- downstream report/Sandbox/public event gates required

## Forbidden Claims

Future Analysis Result wording must not claim:

- official verified
- full-web coverage
- all-platform coverage
- risk score updated from full corpus
- public truth conclusion
- production evidence merged
- report-ready
- Sandbox-ready
- public event-ready
- causal proof
- real-world action executed
- real LLM authenticity verification

## Warning Severity Guidance

### Blocking Warnings

These should block result presentation until resolved:

- privacy-held evidence included
- rejected evidence included
- duplicate evidence amplifies risk
- missing coverage limitation
- missing provider-output-is-evidence-not-truth note
- missing not-official-verification note
- raw author identifier exposure
- private content exposure
- secret-like value exposure

### Non-Blocking Warnings

These may allow result presentation only with visible warnings:

- weak evidence included
- selected sample limitation
- small sample limitation
- vendor-attested evidence
- external-agent-assisted evidence
- screenshot transcription
- manual URL evidence
- duplicate count shown as density only

## Carry-Forward Rules

Warnings must travel downstream into:

- Summary Report metadata
- Markdown export metadata
- B-end report generation gate input
- Sandbox generation gate input
- public event generation gate input
- audit timeline references

Warnings must not be removed because the result is visually summarized.
