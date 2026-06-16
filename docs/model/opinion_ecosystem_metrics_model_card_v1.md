# Opinion Ecosystem Metrics Model Card v1

> This model card describes the current frontend-only Opinion Ecosystem metrics used in Sentigraph demos. It is a transparency document, not a claim of scientific validation, production readiness, official platform verification, or causal proof.

## 1. Model Name

Opinion Ecosystem Sandbox Metrics v1

Related frontend modes:

- Mock schema mode
- Synthetic evidence fixture mapping mode
- Helldivers PSN selected public sample mode
- Sandbox V2 ecology view
- C-end public event prototype display cards

## 2. Intended Use

The metrics are intended to help explain, in a local demo:

- how public-opinion evidence may be grouped into anonymous PeopleCluster visuals;
- how content, official statements, media, narrative, or meme nodes can be shown as InfluenceCore nodes;
- how EchoBox pressure, saturation, and breakout risk can be visualized;
- how transparent clarification, FAQ, third-party explanation, community deconstruction, delayed response, or no response can be compared in a sandbox;
- how selected sample limitations and review boundaries should be shown to users.

The current model is useful for product explanation, demo walkthroughs, UI research, and future model-design discussion.

## 3. Out Of Scope

The current metrics must not be used as:

- a real-world prediction engine;
- a moderation execution engine;
- a causal proof tool;
- a full-web or full-platform measurement system;
- an official verification system;
- a system for identifying or targeting individual people;
- a replacement for human review, legal review, or platform-approved data access.

## 4. Data Sources

Current data sources for the Opinion Ecosystem Sandbox:

| Source | Status | Notes |
| --- | --- | --- |
| Mock schema | Frontend local mock | Used for baseline visual states and scenario examples. |
| Synthetic evidence fixture | Frontend local fixture | Used to test evidence-to-ecosystem mapping. |
| Helldivers PSN selected public sample | Frontend local fixture | Small selected public sample, not full coverage. |
| C-end public event sample | Frontend local mock | Used for event plaza and detail page display. |

Current boundaries:

- No live search provider is used for these metrics.
- No RSS or GDELT live provider is used for these metrics.
- No real LLM is used.
- No real platform action is executed.
- The selected public sample is not full-web coverage, not full-platform coverage, not full-thread coverage, not official verification, and not causal proof.

## 5. Main Output Families

### 5.1 Evidence Confidence

Evidence confidence is a conservative local fixture score. It blends:

- trust label;
- declared trust score when available;
- review status;
- provenance type;
- duplicate penalty;
- risk flag penalty.

Rejected evidence is excluded from active mapping. Duplicate evidence is folded before mapping.

This score is not a truth score and not official verification.

### 5.2 InfluenceCore

InfluenceCore nodes represent content, narrative, official, media, meme, or similar cores.

Main metrics:

- `attention_weight`
- `evidence_strength`
- `gravitational_pull`
- `source_credibility`
- `bridge_power`

Important boundary:

- InfluenceCore nodes are not PeopleCluster balls.
- InfluenceCore nodes are not individual users.
- Higher pull means stronger visual influence in the local prototype, not proven real-world causality.

### 5.3 EchoBox

EchoBox represents local visualization of repeated exposure, pressure, and reinforcement.

Main metrics:

- `echo_chamber_score`
- `saturation_ratio`
- `permeability_score`
- `internal_reinforcement`
- `fatigue_rate`
- `breakout_risk`

Important boundary:

- These are local visual proxies.
- `breakout_risk` is not a guaranteed forecast.
- Saturation does not mean full platform volume.

### 5.4 PeopleCluster

PeopleCluster balls represent anonymous groups or clusters.

Main metrics:

- `population_weight`
- `activity_weight`
- `emotion_load`
- `expression_intensity`
- `grievance_memory`
- `bridge_power`

Important boundary:

- PeopleCluster balls do not represent real individual users.
- The system must not infer individual-level persuasion profiles.
- The current fixture does not expose raw personal identity fields.

### 5.5 Camp Dynamics

Camp Dynamics describes local visual changes across stance-like groups.

Main metrics:

- `camp_distribution`
- `conversion_score`
- `neutralization_score`
- `withdrawal_score`
- `hardening_score`
- `backlash_score`

Important boundary:

- These are scenario comparison signals, not manipulation instructions.
- Use language such as transparent clarification, FAQ, third-party explanation, community deconstruction, cooling, neutralization, exit, backlash risk, and reactivation risk.

### 5.6 DeconstructionCore

DeconstructionCore represents community explanation, meme framing, or narrative de-escalation cores.

Main metrics:

- `threat_deflation`
- `humor_acceptance`
- `neutralization_power`
- `withdrawal_power`
- `backlash_risk`
- `meme_replicability`

Important boundary:

- The demo does not claim that community deconstruction always reduces risk.
- Backlash and long-tail reputation risks remain visible.

### 5.7 ResponseTempo

ResponseTempo visualizes local timing suggestions.

Main metrics:

- `deconstruction_window_score`
- `clarification_priority`
- `faq_priority`
- `third_party_explanation_priority`
- `wait_and_monitor_score`

Important boundary:

- ResponseTempo is not an automated action plan.
- It does not execute real platform communication or moderation.

### 5.8 ReputationMemory

ReputationMemory visualizes unresolved grievance and long-tail memory.

Main metrics:

- `unresolved_grievance_score`
- `stigma_persistence`
- `meme_persistence`
- `trust_recovery`
- `reactivation_risk`

Important boundary:

- ReputationMemory is a local prototype concept.
- It does not prove long-term causal effects.

## 6. Helldivers PSN Sample Model Card

Current Helldivers sample facts:

- Event: Helldivers 2 PSN account linking controversy.
- Evidence count: 34 evidence items.
- Sources: 7.
- Comment samples: 28.
- Root or InfluenceCore candidates: 6.
- Mode: selected public sample fixture.

Limitations:

- not full-web coverage;
- not full-platform coverage;
- not full-thread coverage;
- not official verification;
- not causal proof;
- not production data;
- no real platform action;
- no real API or LLM call.

T0 to T6 timeline phases are local preset stages:

| Phase | Local meaning |
| --- | --- |
| T0 | Account linking announcement |
| T1 | Community backlash |
| T2 | Official rollback or response |
| T3 | Media or third-party explanation |
| T4 | Review bomb cape or community deconstruction |
| T5 | Fatigue and cooling |
| T6 | Reputation memory |

The phase values are visual presets. They are not calibrated event reconstruction.

## 7. Current Calibration Status

| Area | Calibration status |
| --- | --- |
| Evidence confidence weights | Local heuristic only |
| EchoBox score weights | Local heuristic only |
| Camp Dynamics weights | Local heuristic only |
| ResponseTempo recommendation labels | Local heuristic only |
| ReputationMemory values | Local heuristic only |
| Helldivers timeline values | Local selected-sample preset |
| C-end public event heat and controversy | Mock display values |

No claim should be made that these weights have been validated against historical event outcomes.

## 8. Candidate Theory Basis

The current metrics are inspired by product and research concepts documented in local Sentigraph notes:

- opinion ecosystem layers;
- evidence-to-ecosystem mapping;
- trust, provenance, and deduplication;
- human review and audit workflow;
- ethical public-opinion simulation boundaries;
- visual interaction design for Sandbox V2.

Candidate theory families:

- social influence and bounded confidence;
- echo chamber and homophily;
- network bridge and centrality;
- attention and salience;
- agenda-setting and narrative competition;
- temporal burst and event memory;
- model-card and uncertainty-reporting practice.

These theory families are candidate framing only. Exact citations, benchmarks, and validation protocols remain to be completed before production claims.

## 9. Known Limitations

- The current metrics are frontend-local and not backend-authoritative.
- Values are based on fixtures, presets, and heuristic mapping.
- Small samples can be misleading.
- Evidence coverage is incomplete unless otherwise documented.
- Review status and trust label affect display but do not create official verification.
- Screenshots and transcriptions are not automatically verified.
- The system does not perform individual-level profiling.
- Scenario playback is a visual sandbox, not real-world intervention.

## 10. Recommended Future Validation Work

Before treating these metrics as production-grade, Sentigraph should add:

- explicit literature references for each metric family;
- ablation tests for weights;
- sensitivity analysis for scenario values;
- uncertainty or confidence bands;
- benchmark cases with documented evidence coverage;
- calibration against historical outcomes where legally and ethically appropriate;
- review by product, legal, and domain experts;
- clear user-facing model cards in the UI.

## 11. Safe Demo Language

Recommended:

- "This is a frontend-only local demo."
- "This uses a selected public sample."
- "This helps visualize possible public-opinion structure."
- "The metrics are local heuristic indicators."
- "PeopleCluster balls are anonymous groups or clusters."
- "InfluenceCore nodes are content, narrative, official, media, or meme cores."
- "Rejected and weak evidence should be treated carefully."
- "This is not official verification or causal proof."

Avoid:

- "full-web coverage"
- "full-platform coverage"
- "officially verified"
- "causal proof"
- "real full simulation"
- "automatic authenticity verification"
- "automatic platform action"
- "individual user profiling"

## 12. Related Local Documents

- `docs/model/opinion_ecosystem_metrics_inventory_v1.md`
- `docs/research/opinion_ecosystem_model_v1.md`
- `docs/research/opinion_ecosystem_weight_calculation_v1.md`
- `docs/research/evidence_to_opinion_ecosystem_mapping_v1.md`
- `docs/research/evidence_to_opinion_ecosystem_mapping_contract_v1.md`
- `docs/research/opinion_ecosystem_sandbox_v2_visual_interaction_spec.md`
- `docs/research/sentigraph_ethical_public_opinion_simulation_research_report.md`
- `docs/evidence_trust_and_deduplication.md`
- `docs/evidence_review_workflow.md`

