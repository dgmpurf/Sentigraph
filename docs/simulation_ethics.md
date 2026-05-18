# Simulation Lab Ethics

Status: governance design only. This document defines allowed and forbidden uses for a future Simulation Lab module.

Simulation Lab must support ethical public-interest crisis response. It must not become a manipulation engine.

## Core Principles

- Aggregate only: outputs should describe topic, cohort, and scenario-level dynamics, not individual people.
- Transparent only: simulated interventions must be open, reviewable, and attributable.
- Defensive only: the module should compare clarification, correction, accountability, and harm-reduction options.
- Uncertainty-labeled: all simulated outcomes should state assumptions and limits.
- Human-reviewed: no automatic public response or operational action should be triggered by a simulation.
- Offline-first: MVP simulations should use synthetic or sanitized inputs and should not call real platform APIs or real LLM APIs.

## Allowed Uses

Simulation Lab may support:

- Clarification simulation.
- Apology simulation.
- Compensation simulation.
- FAQ simulation.
- Progress update simulation.
- Third-party evidence simulation.
- Misinformation correction simulation.
- Aggregate-level crisis-response comparison.

Examples:

- Compare whether a factual clarification plus FAQ may reduce confusion faster than a delayed statement.
- Compare an apology plus compensation package against a progress-update-only package.
- Test whether third-party verification improves correction uptake in an aggregate scenario.
- Identify whether the current history is too thin and monitoring should continue before making claims.

## Forbidden Uses

Simulation Lab must not support:

- Fake consensus.
- Bot amplification.
- Covert influencer seeding.
- Fake events.
- Deceptive attention diversion.
- Manipulation of vulnerable groups.
- Individual-level persuasion targeting.
- Account-level influenceability scoring.
- Suppression or harassment tactics.

Examples of blocked requests:

- "Find the easiest users to convince."
- "Create a fake grassroots response."
- "Simulate how many bots are needed to drown out criticism."
- "Identify bridge users for covert seeding."
- "Distract attention with an unrelated controversy."
- "Exploit fear, identity threat, or isolation anxiety."

## Ethical Boundary for Bridge Metrics

Bridge metrics can help estimate whether transparent corrections may cross cluster boundaries. They must not be used to identify real bridge accounts or assign covert outreach targets.

Allowed:

- Aggregate bridge exposure estimate.
- Public, disclosed channel planning.
- Scenario-level correction reach comparison.

Forbidden:

- Real account lists.
- Individual influencer targeting.
- Covert seeding recommendations.
- Harassment or suppression lists.

## Intervention Review Rules

Every intervention package should be reviewed for:

- Factual basis.
- Evidence strength.
- Transparency.
- Accountability.
- Non-deception.
- Non-harassment.
- Absence of fake consensus.
- Absence of vulnerable-group targeting.

The system should warn when an intervention:

- Uses unsupported claims.
- Overpromises future outcomes.
- Blames without evidence.
- Uses inflammatory or accusatory language.
- Attempts to divert attention from the core issue.
- Relies on fabricated or unverifiable sources.

## Output Restrictions

Allowed outputs:

- Aggregate risk movement.
- Topic-level scenario comparison.
- Uncertainty labels.
- Assumption logs.
- Intervention package summaries.
- Ethical-risk warnings.
- Monitoring recommendations.

Forbidden outputs:

- Account-level rankings.
- Influenceability scores.
- Microtargeting segments.
- Bot counts or bot scripts.
- Covert seeding plans.
- Harassment or suppression playbooks.
- Message variants designed to exploit vulnerabilities.

## Data Rules

MVP data:

- Synthetic agents.
- Synthetic networks.
- Sanitized fixtures.
- Aggregate monitoring snapshots.
- No private data.
- No real personal identifiers.

Future real-data use requires:

- Documented lawful basis.
- Data minimization.
- Redaction review.
- Privacy review.
- Updated validation plan.
- Explicit user approval.

## LLM Rules

MVP Simulation Lab must not call real LLM APIs.

Future optional LLM narrative generation may be considered only after:

- Real-provider safety gates are active.
- Usage guardrails are active.
- Prompt and output redaction are tested.
- JSON/schema validation exists.
- Human review is mandatory.
- The LLM cannot generate forbidden tactics.

## Abuse-Resistance Requirements

Before implementation, the project should add tests that verify:

- Forbidden tactic requests are rejected.
- No output contains bot amplification instructions.
- No output contains account-level targeting.
- No output contains API keys, secrets, or raw private data.
- Scenario reports include uncertainty and assumption labels.
- Simulation runs can be audited after the fact.

## Human Review Workflow

Recommended workflow:

1. User selects a legitimate scenario goal.
2. System checks the goal against allowed and forbidden uses.
3. User chooses transparent intervention packages.
4. Simulator runs deterministic aggregate scenarios.
5. System shows assumptions, uncertainty, and ethical warnings.
6. Human reviewer decides what, if anything, to do.
7. Any public action happens outside Simulation Lab with normal accountability.
