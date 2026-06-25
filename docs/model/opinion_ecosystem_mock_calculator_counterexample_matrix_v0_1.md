# Opinion Ecosystem Mock Calculator Counterexample Matrix v0.1

Status: docs-only / design-only / future deterministic local mock calculator counterexample plan. This is not implemented, not runtime, not backend schema, not frontend UI, not tests, not real API, not real LLM, not crawler, not full-web, not full-platform, not official verification, not causal proof, not prediction, not personality diagnosis, not individual persuasion scoring, and not auto-executed response strategy.

Scope is selected sample / local fixture / imported evidence only.

Required model metadata:

- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 1. Purpose

This document designs counterexample cases for a future deterministic local mock calculator. No tests are implemented in this phase.

Each future test should assert:

- expected outputs
- expected warnings/blockers
- anti-overclaim checks
- no real API / real LLM / crawler behavior
- no `auto_execute`
- human review required for response strategies

## 2. Counterexample Cases

### A. duplicate_comments_do_not_infinite_amplify

Fixture purpose: ensure duplicate evidence becomes folded repetition signal, not linear heat/risk amplification.

Minimum input shape:

- many evidence items in the same `duplicate_group_id`
- `duplicate_count > 1`
- same aggregate reference

Expected outputs:

- `repetition_signal` rises
- `sample_heat_score` does not grow linearly with raw duplicate count
- risk does not infinitely amplify

Expected warnings/blockers:

- `duplicate_folded_warnings` includes duplicate group summary

Anti-overclaim checks:

- no real hotlist claim
- no full-web or full-platform claim

Future test assertion ideas:

- unique group count drives main score more than raw item count
- duplicate warning visible in run summary

### B. low_trust_emotional_screenshot

Fixture purpose: ensure low-trust emotional evidence raises review risk but dampens confidence and stance movement.

Minimum input shape:

- `provenance_type = screenshot_transcription`
- `trust_label = low`
- high `emotion_intensity_hint`
- `review_status = review_needed`
- `source_url_present = false`

Expected outputs:

- review risk rises
- evidence confidence lowers
- PeopleCluster `stance_delta` damped
- no official verification
- no causal proof

Expected warnings/blockers:

- `low_trust_warnings`
- `review_needed_warnings`
- missing source URL warning

Anti-overclaim checks:

- screenshot is not verified
- evidence is evidence, not truth

Future test assertion ideas:

- damping factor reduces stance update
- confidence warning present

### C. rejected_evidence_excluded

Fixture purpose: ensure rejected evidence does not affect analysis-ready scores.

Minimum input shape:

- high emotion evidence with `review_status = rejected`
- optional `verification_status = human_rejected`

Expected outputs:

- excluded from analysis-ready score
- counted in `rejected_excluded_count`
- appears in warning only

Expected warnings/blockers:

- `rejected_excluded_warnings`

Anti-overclaim checks:

- no score contribution from rejected evidence

Future test assertion ideas:

- score unchanged when rejected evidence is added

### D. one_sided_high_heat_not_high_controversy

Fixture purpose: prevent high volume from inventing controversy.

Minimum input shape:

- high volume in one stance
- low or absent opposing stance
- low cross-stance interaction

Expected outputs:

- heat high
- controversy not automatically high
- no invented opposing cluster

Expected warnings/blockers:

- none unless confidence is low

Anti-overclaim checks:

- no fact judgment
- no causal proof

Future test assertion ideas:

- `sample_heat_score > sample_controversy_score`

### E. official_statement_credible_low_exposure

Fixture purpose: distinguish credibility from exposure.

Minimum input shape:

- InfluenceCore type `official_statement`
- high source identity weight
- low exposure metrics

Expected outputs:

- factual credibility high
- observed amplification low
- no claim it changed discourse

Expected warnings/blockers:

- no exposure-overclaim

Anti-overclaim checks:

- official statement is not proof of discourse effect

Future test assertion ideas:

- `factual_credibility > observed_amplification`

### F. viral_meme_low_credibility

Fixture purpose: distinguish amplification from truth.

Minimum input shape:

- core type `meme_deconstruction` or `ordinary_viral_content`
- high repetition
- high emotional charge
- low factual credibility

Expected outputs:

- observed amplification high
- factual credibility low
- stance effect damped

Expected warnings/blockers:

- `high_attention_low_credibility`

Anti-overclaim checks:

- no truth score
- evidence not truth

Future test assertion ideas:

- amplification can exceed credibility without upgrading truth

### G. strong_echo_no_breakout

Fixture purpose: prevent closed discussion from being treated as breakout.

Minimum input shape:

- high saturation
- high closure
- low cross-box exposure

Expected outputs:

- `sealed_echo_box` or high closure
- breakout low

Expected warnings/blockers:

- possible echo risk warning

Anti-overclaim checks:

- no full-platform claim

Future test assertion ideas:

- `risk_breakout < closure`

### H. bridgeable_controversy

Fixture purpose: ensure controversy with bridge capacity is not simply classified as dangerous echo.

Minimum input shape:

- controversy high
- bridge capacity high
- explanatory cores present

Expected outputs:

- constructive breakout candidate visible
- not simply classified as dangerous echo

Expected warnings/blockers:

- still include human review requirement

Anti-overclaim checks:

- no auto response strategy

Future test assertion ideas:

- bridge capacity moderates echo risk classification

### I. t4_long_faq_backlash

Fixture purpose: test long FAQ strategy during emotional peak.

Minimum input shape:

- stage `T4`
- high emotion / risk breakout
- `strategy_type = FAQ_or_longform_explanation`

Expected outputs:

- clarity benefit possible
- amplification/backlash risk high
- not auto-execute

Expected warnings/blockers:

- `response_strategy_blockers` or human-review warning

Anti-overclaim checks:

- no guaranteed calming claim

Future test assertion ideas:

- strategy level no higher than human-review candidate

### J. minors_family_material_without_consent

Fixture purpose: block sensitive material without consent and redaction.

Minimum input shape:

- strategy uses personal / family / minor material
- missing consent or redaction

Expected outputs:

- `blocked_pending_review` or `private_review_only`
- no public use

Expected warnings/blockers:

- privacy blocker
- human review blocker

Anti-overclaim checks:

- no public response generation

Future test assertion ideas:

- privacy blocker dominates benefit score

### K. response_strategy_auto_execute_forbidden

Fixture purpose: ensure `auto_execute` is invalid.

Minimum input shape:

- response strategy status or recommendation tries `auto_execute`

Expected outputs:

- forbidden / invalid
- human review required

Expected warnings/blockers:

- `response_strategy_blockers`

Anti-overclaim checks:

- no auto-executed response strategy

Future test assertion ideas:

- validator rejects fixture or output

### L. peoplecluster_not_real_person

Fixture purpose: prevent PeopleCluster from exposing real identities.

Minimum input shape:

- raw author identifier
- person label
- profile-like value

Expected outputs:

- blocked or warning
- PeopleCluster remains anonymous aggregate proxy

Expected warnings/blockers:

- privacy blocker
- forbidden field warning

Anti-overclaim checks:

- no personality diagnosis
- no individual persuasion scoring

Future test assertion ideas:

- `raw_author_id` blocks validation

### M. influencecore_not_person_ball

Fixture purpose: prevent InfluenceCore from becoming a people node.

Minimum input shape:

- InfluenceCore represented as person ball
- person-only label without content/narrative/source context

Expected outputs:

- invalid fixture or warning
- InfluenceCore remains content/narrative/source identity

Expected warnings/blockers:

- model card warning

Anti-overclaim checks:

- no person-ball output

Future test assertion ideas:

- output flag `not_person_ball = true`

### N. echobox_not_real_community_map

Fixture purpose: prevent EchoBox from claiming full graph truth.

Minimum input shape:

- output claims real community map or full graph

Expected outputs:

- overclaim blocker

Expected warnings/blockers:

- `overclaim_blockers`

Anti-overclaim checks:

- not real community map
- not full social graph

Future test assertion ideas:

- any `real_community_map = true` fails

### O. unknown_platform_or_future_platform

Fixture purpose: ensure unknown future platforms do not imply runnable provider support.

Minimum input shape:

- `platform = future_forum`
- or unknown platform metadata

Expected outputs:

- `manual_review_required`
- unsupported platform warning
- no runnable provider implication

Expected warnings/blockers:

- unsupported platform warning

Anti-overclaim checks:

- no real API
- no crawler
- no live platform monitor

Future test assertion ideas:

- unknown platform cannot become `metadata_ready` without review
