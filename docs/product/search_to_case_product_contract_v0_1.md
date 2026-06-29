# Search-to-Case Product Contract v0.1

Status: product contract only. This document does not implement search UI, backend routes, case creation, Evidence import, analysis runs, collector execution, API bridges, reports, Sandbox/public event runtime, or generated public response behavior.

## A. Product Definition

Search-to-Case means:

```text
search query -> governed case workspace candidate
```

It is not just a search result list.

It is not live crawling by default.

It is not production case creation by default.

A future Search-to-Case workflow should turn a user search for a person, event, brand, company, product, public topic, or controversy into a governed candidate workspace only after metadata, package, review, dedup, and promotion gates are satisfied.

## B. Supported Future Search Categories

Future Search-to-Case may support these search categories:

- event / controversy
- public person
- company / brand / product
- media topic
- policy / public issue
- platform-native sample event
- manual package-driven event

These categories describe product intent only. They do not authorize live collection, crawling, scraping, official platform API calls, or production Evidence import.

## C. Future Workflow

Canonical future chain:

```text
user_search_context
-> analysis_request
-> provider_request
-> provider_job_result metadata
-> package_reference
-> metadata_only_validation
-> review_only_staging_candidate
-> evidence_review_and_dedup
-> case_workspace_candidate
-> future explicit promotion gates
-> future analysis/report/sandbox gates
```

Every transition must preserve the principle that provider output is evidence, not truth.

## D. Workspace Concept

A case workspace is a governed container, not automatic production evidence and not public output.

Future case workspace fields may include:

- `case_id`
- `case_title`
- query context
- source scope
- provider result references
- package references
- evidence review state
- analysis request state
- allowed modules
- blocked modules
- audit trail
- safety flags

Important boundaries:

- Case workspace is not an endpoint.
- Case workspace is not automatically production evidence.
- Case workspace is not public output.
- Case workspace does not imply full-web coverage.
- Case workspace does not imply official verification.
- Case workspace does not imply causal proof.

## E. Permission Model, Future Only

Future roles may include:

- ordinary user
- VIP / pro user
- enterprise user
- internal admin / operator

This role split is future-only. This phase does not implement roles, permissions, billing, quotas, routing, UI, or backend authorization.

During internal development, the team may use a highest-permission internal workflow for testing after gates, but that does not create public permissions, public delivery, or production import rights.

## F. User-Facing Promise

Future product language may say:

- "We found a candidate case workspace."
- "Metadata package is ready for review."
- "Evidence import is blocked until review."
- "This case is review-only."
- "This is not verified truth."
- "This is not an official conclusion."

Future product language must not promise:

- full web coverage
- full platform coverage
- truth verification
- causal proof
- official confirmation
- real-time monitoring
- production PR automation
- persuasion targeting
- public response generation

## G. Forbidden Product Behavior

Search-to-Case must explicitly forbid:

- covert persuasion
- astroturfing
- fake consensus
- bot / sockpuppet / brigading behavior
- individual targeting
- `target_user_list`
- psychological profile
- personality diagnosis
- automatic public response text
- send / post / publish / execute behavior
- `truth_score` as a truth claim
- `official_verified` as an official confirmation claim
- `prediction_probability` as a guaranteed outcome claim

The product may support governance, evidence review, coverage limitation disclosure, and decision-support summaries. It must not become a covert influence system or an automatic public-action system.
