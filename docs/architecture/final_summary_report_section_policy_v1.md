# Final Summary Report Section Policy v1

## Purpose

This policy defines the required sections and forbidden claims for any future local Final Summary Report Runtime.

The purpose is to make a final local report clearer for readers while preserving every evidence, review, dedup, coverage, privacy, and audit boundary.

## Required Sections

### Executive Summary

Must summarize the event, key findings, confidence limitations, and report scope in plain language.

It must state that the report is based on reviewed local evidence scope and is not full-web, full-platform, or full-thread coverage.

### Evidence Scope

Must describe:

- source scope
- reviewed item count
- platform/source distribution if available in the candidate
- excluded evidence categories
- sample limitations
- review-only provenance

### Coverage Limitation

Must clearly state:

- not full-web coverage
- not full-platform coverage
- not full-thread coverage
- not complete public opinion
- not a guarantee that all relevant evidence was captured

### Source / Provider Statement

Must state where the local candidate came from and that provider output is evidence, not truth.

It must not describe provider output as official verification unless a separate official API verification path explicitly supports that status.

### Provider Output Is Evidence, Not Truth

Must remain visible as a standalone caveat or boundary note.

### Not Official Verification

Must state that the final Summary Report object does not verify authenticity through an official platform unless future official verification gates explicitly prove it.

### Not Full-Web / Full-Platform / Full-Thread Coverage

Must state all three boundaries explicitly:

- not full-web coverage
- not full-platform coverage
- not full-thread coverage

### Analysis Summary

Must summarize only the bounded local analysis result candidate.

It must not rerun the analysis engine, call real APIs, call real LLMs, or infer beyond available reviewed local evidence.

### Risk and Topic Summary

Must include:

- bounded risk signals
- topic clusters or summaries where available
- confidence limitations
- caveats that risk is not causal proof or guaranteed future outcome

### Representative Evidence

Must include safe representative evidence previews only.

It must not expose raw author identifiers, profile URLs, private messages, secret-like values, email addresses, or phone numbers.

### Weak Evidence Warning

Must preserve a warning that weak evidence remains warning-marked and should not be overstated.

### Rejected Evidence Excluded

Must preserve a note that rejected evidence is excluded from report conclusions.

### Duplicate Evidence No Amplification

Must state that duplicate evidence does not multiply risk, sentiment, coverage, or report conclusions.

Group size may be used as a density signal only when clearly labeled as such.

### Privacy / Needs-More-Source Exclusions

Must state that privacy-held, needs-more-source, or rejected records remain excluded from final report conclusions unless future governance rules explicitly allow otherwise.

### Audit Trace

Must include references to:

- `SummaryReportCandidate`
- `SummaryReportCandidateAudit`
- `FinalSummaryReportReviewGate`
- `FinalSummaryReportReviewGateAudit`
- `ReportGenerationGate`
- `ManualAnalysisExecution`
- `AnalysisResultBoundaryGate`

### Limitations and Confidence Notes

Must include limitations and confidence notes copied from the candidate and review gate.

These notes must remain visible and must not be softened into marketing language.

## Forbidden Claims

Future final Summary Reports must not claim:

- official verified
- full-web coverage
- all-platform coverage
- full-thread coverage
- complete public opinion
- causal proof
- PDF ready
- Markdown ready
- briefing deck ready
- B-end ready
- Sandbox ready
- public event ready
- legal guarantee
- PR outcome guarantee
- production evidence merged
- production case created
- real-world action executed
- screenshot or transcription authenticity verified by AI
- provider output is truth

## Required Reader Framing

Use wording like:

- bounded local final Summary Report
- reviewed local evidence scope
- evidence, not truth
- not official verification
- not full-web, not full-platform, and not full-thread coverage
- weak evidence remains warning-marked
- rejected evidence excluded
- duplicate evidence does not amplify risk
- downstream artifacts require separate gates

Avoid wording like:

- definitive truth
- official verified report
- complete event capture
- whole-network opinion
- all-platform conclusion
- guaranteed outcome
- production-ready export

