# Sentigraph Production Analysis Run Candidate to Actual Analysis Execution Gate Contract v0.1

## A. Contract Purpose

This contract defines how a controlled production analysis run candidate may hand off into a future Actual Analysis Execution Gate Decision. It exists to prevent a candidate-shaped local object from being mistaken for a production analysis_run, an executed analysis, an analysis result, a report, or public/customer-ready output.

## B. Source Object Allowed from 8W-34

The only allowed upstream source for the next docs-only gate is the 8W-34 controlled production analysis run candidate set:

- candidate set schema: `sentigraph_controlled_production_analysis_run_candidate_set_v0_1`
- candidate schema: `sentigraph_controlled_production_analysis_run_candidate_v0_1`
- candidate set status: `production_analysis_run_candidate_set_warn_manual_review_required`
- candidate count: 1
- source production case candidate count: 1
- source controlled evidence item count: 5
- warning count: 1
- human review required: yes

No original package rows, private collector files, real exchange directories, raw comments, raw identities, or external sources are part of the 8W-35 or 8W-36 input scope.

## C. Production Analysis Run Candidate Completion Definition

Production analysis run candidate completion means:

- a controlled local candidate-shaped object exists
- the expected schemas are present
- upstream counts and warnings are preserved
- runtime side effects remain negative
- no production analysis_run has been created
- no actual analysis execution has occurred
- no analysis result has been generated

It does not mean analysis-ready, production-ready, report-ready, public-ready, customer-ready, or externally deliverable.

## D. Actual Analysis Execution Gate Definition

An Actual Analysis Execution Gate is a future governance decision point. Its job is to decide whether a later phase may design or implement a tightly controlled execution path.

The gate must define:

- accepted upstream candidate set schema
- warning/manual-review carry-forward
- blocker categories
- non-approval flags
- privacy and minimization requirements
- allowed future execution scope if a later phase is approved
- validation expectations

The gate itself does not execute analysis.

## E. Actual Analysis Execution Implementation Separation

The docs-only gate and runtime implementation must remain separate phases.

The 8W-35 decision only permits considering a future 8W-36 docs-only gate. It does not permit any implementation phase to start. A later implementation phase must require its own explicit approval and must restate all forbidden side effects.

## F. Controlled Production Analysis Run Candidate Is Not Production analysis_run

A controlled production analysis run candidate must not be:

- persisted as a production analysis_run
- returned as a production analysis_run API object
- displayed as a production analysis_run in frontend UI
- counted as production execution history
- used as evidence of completed analysis
- used as an input to reporting or public event output without later gates

## G. Controlled Production Analysis Run Candidate Is Not Actual Analysis Execution

The candidate does not run analysis. It does not execute calculators, derive conclusions, create risk findings, generate user-facing results, or create report-ready content.

The candidate only proves that upstream governance metadata can be shaped for a later gate.

## H. Actual Analysis Execution Is Not Analysis Result Generation Unless Separately Approved

Actual analysis execution and analysis result generation are distinct boundaries.

A future execution phase, if ever approved, may produce internal execution traces or controlled intermediate output only if that future phase defines them. It must not generate an Analysis Result record, summary report, final report, export artifact, public URL, signed URL, or delivery package unless later gates explicitly approve those outputs.

## I. Actual Analysis Execution Is Not B-end Report Runtime

Actual analysis execution must not imply:

- B-end report generation
- report candidate creation
- final summary report creation
- report export packaging
- customer delivery
- downloadable file creation

Those remain separate downstream gates.

## J. Actual Analysis Execution Is Not Sandbox / Public Event Runtime

Actual analysis execution must not imply:

- Sandbox fixture generation
- public event page generation
- C-end event plaza publication
- public route creation
- generated response text
- community-facing recommendation text
- public action, post, send, or publish behavior

Those remain separate downstream gates.

## K. Actual Analysis Execution Is Not Review Queue Runtime

Actual analysis execution must not create Review Queue items, production review queue items, review actions, or audit records unless a later Review Queue runtime gate explicitly approves that behavior.

The 8W-34 and 8W-35 chain carries human-review-required metadata only. It does not operate a review queue.

## L. Warning / Manual-review Carry-forward

The 8W-34 warning state is mandatory input to the future 8W-36 gate.

The future gate must treat:

- `production_analysis_run_candidate_set_warn_manual_review_required`
- `warning_count = 1`
- `human_review_required = yes`

as active caution state. It must not silently downgrade, clear, or hide this state.

## M. Allowed Future 8W-36 Docs-only Inputs

Future 8W-36 may inspect safe metadata summaries already represented in committed local records and docs. It may inspect the 8W-34 health report and controlled helper/test files only as needed to verify boundary claims.

It must not inspect:

- `evidence_items.jsonl`
- `evidence_items.csv`
- `source_manifest.jsonl`
- `collection_log.jsonl`
- original package rows
- raw comments
- raw identities
- private collector source files
- real exchange directories
- environment real paths
- secrets

## N. Forbidden Current and Future Actions

8W-35 and the proposed 8W-36 docs-only gate forbid:

- actual analysis execution
- production analysis_run creation
- analysis result generation
- production case creation
- production EvidenceItem creation
- Review Queue runtime use
- production review queue item creation
- route/API creation
- frontend integration
- runtime persistence
- B-end report runtime
- Sandbox/public event runtime
- export/download/public access/external delivery/final delivery runtime
- provider or collector jobs
- real API or real LLM calls
- URL fetching or scraping
- private collector inspection
- real exchange dir reading
- original package row parsing
- generated public response text
- post, send, publish, upload, or external delivery
- MediaCrawler integration
- OpenClaw production ingestion
- Project Source changes

## O. Future Blocker Categories

Future 8W-36 must define blockers for:

- missing or wrong upstream schema
- missing warning carry-forward
- privacy risk
- raw identity exposure
- secret-like value exposure
- unresolved human-review-required state without explicit carry-forward
- any request to create a production analysis_run
- any request to execute analysis
- any request to generate an analysis result
- any request to generate reports, Sandbox, public events, exports, downloads, public URLs, signed URLs, or external delivery
- any request to parse original package rows or read private collector/real exchange data
- any request to call real APIs, real LLMs, providers, collectors, fetchers, or scrapers

## P. Future Redaction / Minimization Carry-forward Principles

Future phases must keep the minimum-safe metadata principle:

- carry counts, schema names, status labels, warning labels, and boundary flags
- avoid raw comments
- avoid raw author identifiers
- avoid private URLs or profile URLs
- avoid original package rows
- avoid secrets, tokens, cookies, sessions, salts, credentials, and environment values
- preserve audit-visible warning state

Provider output remains evidence material, not truth. A production analysis run candidate remains a candidate, not a finding.

## Q. Approval Protocol

8W-35 does not activate an implementation approval phrase.

Future 8W-36 may define an approval protocol for a later implementation phase, but that protocol must remain inactive in the docs-only gate. If a later implementation phase is approved, it must use a phase-specific exact approval phrase and must prove that wrong, missing, non-ASCII, or garbled approval text blocks before any execution-like behavior.

## R. Forbidden Interpretations

Do not interpret this contract as approval for:

- actual analysis execution
- production analysis_run creation
- analysis result generation
- production case creation
- production EvidenceItem creation
- review queue runtime
- route/API or frontend integration
- B-end report generation
- Sandbox/public event generation
- export/download/public access/external delivery/final delivery
- real API, real LLM, provider, collector, fetch, or scrape behavior
- full-web coverage
- full-platform coverage
- official verification
- causal proof
- production readiness
- customer readiness
