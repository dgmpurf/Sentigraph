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
- Simulating lawful/platform-authorized content moderation effects.
- Simulating removal vs labeling vs clarification tradeoffs.
- Estimating backlash, perceived suppression, legitimacy, and spillover risk.
- Aggregate-level crisis-response comparison.

Examples:

- Compare whether a factual clarification plus FAQ may reduce confusion faster than a delayed statement.
- Compare an apology plus compensation package against a progress-update-only package.
- Test whether third-party verification improves correction uptake in an aggregate scenario.
- Compare policy labeling, content removal, and removal plus transparent explanation for a policy-violating high-reach post.
- Estimate whether closing comments may reduce immediate exposure but increase cross-platform spillover or trust loss.
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
- Illegal suppression.
- Covert censorship.
- Targeting individuals for silencing.
- Evading platform governance.
- Suppression or harassment tactics.

Examples of blocked requests:

- "Find the easiest users to convince."
- "Create a fake grassroots response."
- "Simulate how many bots are needed to drown out criticism."
- "Identify bridge users for covert seeding."
- "Distract attention with an unrelated controversy."
- "Find people to silence so the criticism disappears."
- "Model how to hide lawful criticism without platform review."
- "Bypass platform governance to reduce visibility."
- "Exploit fear, identity threat, or isolation anxiety."

## Content Moderation and Visibility Ethics

Allowed moderation simulations:

- Lawful or platform-authorized content removal based on explicit policy.
- Comment closure when a platform, owner, or moderator has legitimate authority.
- Account restriction modeled only as aggregate policy enforcement, not real account targeting.
- Visibility reduction or ranking changes modeled as platform governance variables.
- Platform labeling, fact-check labels, disputed-content labels, and policy-enforcement notices.
- Content removal with transparent explanation when policy clarity and legitimate authority are explicit.
- Removal versus labeling versus clarification tradeoff analysis.
- Backlash, trust-loss, legitimacy, spillover, neutral-audience, and hard-opposition impact estimates.

Required safeguards:

- The scenario must identify the policy basis or lawful authority for the moderation action.
- The simulator should compare exposure reduction against backlash, trust loss, and spillover risk.
- Outputs must remain aggregate and must not list real accounts, real posts, or targets.
- Any policy enforcement notice should be transparent, factual, and reviewable.
- The model must avoid implying that lawful criticism should be hidden merely because it is inconvenient.

Forbidden moderation uses:

- Illegal suppression or covert censorship.
- Silencing individuals or communities outside a lawful/platform-authorized process.
- Evading platform governance, appeals, moderation review, legal requirements, or audit trails.
- Pairing removal with fake consensus, bot amplification, fabricated support, or deceptive diversion.
- Harassment, doxxing, intimidation, or retaliation against speakers.
- Account-level influenceability scoring or target lists for restriction.

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
- Uses content removal without a clear policy basis.
- Uses content removal without transparent explanation when neutral-audience trust risk is high.
- Has high perceived-suppression, martyr-effect, or cross-platform-spillover risk.

## Output Restrictions

Allowed outputs:

- Aggregate risk movement.
- Topic-level scenario comparison.
- Uncertainty labels.
- Assumption logs.
- Intervention package summaries.
- Ethical-risk warnings.
- Monitoring recommendations.
- Lawful moderation tradeoff metrics such as exposure reduction, backlash cost, trust loss, spillover risk, and removal legitimacy.

Forbidden outputs:

- Account-level rankings.
- Influenceability scores.
- Microtargeting segments.
- Bot counts or bot scripts.
- Covert seeding plans.
- Harassment or suppression playbooks.
- Message variants designed to exploit vulnerabilities.
- Lists of individuals or accounts to silence.
- Instructions for evading platform governance.

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
