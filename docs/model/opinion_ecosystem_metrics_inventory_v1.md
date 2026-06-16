# Opinion Ecosystem Metrics Inventory v1

> Scope: this inventory documents metrics currently visible or derivable in the frontend-only Opinion Ecosystem Sandbox and C-end public event mock pages. It is not a backend contract, not a production scoring engine, and not evidence that any metric has been scientifically calibrated.

## 1. Boundary

Current implementation status:

- Frontend-only local prototype for Opinion Ecosystem visualization.
- Inputs are mock schema, synthetic evidence fixture mapping, and the selected Helldivers PSN public sample fixture.
- No real platform action is executed.
- No real platform API or real LLM is called by these metrics.
- The Helldivers PSN mode is a selected public sample, not full-web coverage, not full-platform coverage, not full-thread coverage, not official verification, and not causal proof.
- PeopleCluster balls represent anonymous groups or clusters, not real individual users.
- InfluenceCore nodes represent content, narrative, official, media, meme, or other influence cores, not people balls.

## 2. Inventory Summary

| Group | Current metrics inventoried |
| --- | ---: |
| Evidence confidence and provenance | 4 |
| InfluenceCore | 5 |
| EchoBox | 6 |
| PeopleCluster | 6 |
| Camp Dynamics | 6 |
| DeconstructionCore | 6 |
| ResponseTempo | 5 |
| ReputationMemory | 4 |
| C-end public event mock display | 3 |
| Helldivers timeline preset fields | 7 |

This document inventories 52 current metric fields or derived indicators. Many are closely related visual indicators rather than independent model variables.

Future candidate metrics documented here: 10.

## 3. Current Metric Inventory

### 3.1 Evidence Confidence And Provenance

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `evidence_confidence` | `frontend/src/data/opinionEcosystemMapper.js` | Conservative confidence used by fixture-to-ecosystem mapping. | Weighted blend of trust label, declared trust score, review status, provenance type, duplicate penalty, and risk flag penalty. | Local fixture mapper only. |
| `trust_weight` | mapper constants | Trust label base weight. | `high=0.9`, `medium=0.72`, `medium_low=0.52`, `low=0.32`, `unverified=0.18`. | Local heuristic. |
| `review_weight` | mapper constants | Review status base weight. | `approved=1`, `not_reviewed=0.72`, `review_needed=0.48`, `marked_weak=0.42`, `rejected=0`. | Local heuristic. |
| `provenance_weight` | mapper constants | Provenance base weight. | `mock_fixture=0.72`, `manual_url=0.58`, `user_upload=0.48`, `data_vendor=0.5`. | Local heuristic. |

Notes:

- Rejected evidence is excluded from active fixture mapping.
- Duplicate groups are folded by `duplicate_group_id`, `content_hash`, or `evidence_id`.
- The confidence score is a visualization input, not a truth score.

### 3.2 InfluenceCore

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `attention_weight` | mapper | Approximate attention from interaction metrics. | Uses log-scaled views and interactions. Interactions weight replies and shares above likes. | Local heuristic. |
| `evidence_strength` | mapper | Strength of an influence core from confidence and attention. | `confidence * 0.72 + attention_weight * 0.18`. | Local heuristic. |
| `gravitational_pull` | mapper and mock scenario | Visual pull of a core on clusters and EchoBox. | In fixture mapping, blend of attention, child count, and confidence. In mock scenarios, scenario preset controls pull. | Local visual proxy. |
| `source_credibility` | mapper | Credibility proxy for source evidence. | Uses evidence confidence. | Not external verification. |
| `bridge_power` | mapper and mock data | Whether a core can bridge camps. | Type and fixture dependent. Used for official, third-party, and deconstruction cores. | Local heuristic. |

Interpretation:

- InfluenceCore is a content or narrative node, not a person.
- A high `gravitational_pull` means the visualization gives that core more local influence in the prototype. It does not prove real-world causality.

### 3.3 EchoBox

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `echo_chamber_score` | mapper and mock schema | Internal reinforcement level of an EchoBox. | Mapper blends oppose signal ratio and opposition core pull. Mock scenario sets a preset value. | Local heuristic. |
| `saturation_ratio` | mapper and mock schema | How saturated or crowded the EchoBox is. | Mapper blends comment volume and oppose ratio. Mock scenario sets a preset value. | Local heuristic. |
| `permeability_score` | mapper and mock schema | How open the EchoBox is to neutralizing or bridging content. | Mapper blends neutral signal share and deconstruction bridge power. Mock scenario uses `1 - echo_chamber_score * 0.62`. | Local heuristic. |
| `internal_reinforcement` | mapper and mock schema | Reinforcing pressure inside EchoBox. | Mapper blends echo chamber score and oppose signal share. Mock scenario uses `echo_chamber_score * 0.78 + hardening_score * 0.22`. | Local heuristic. |
| `fatigue_rate` | mapper and mock schema | Cooling, fatigue, or withdrawal tendency. | Mapper uses fatigue-like wording count. Mock scenario uses preset value. | Local text heuristic. |
| `breakout_risk` | mapper and mock schema | Chance that the EchoBox pressure spills into broader visible conflict. | Mapper blends opposition breakout power and saturation. Mock scenario uses preset value. | Risk proxy, not prediction guarantee. |

### 3.4 PeopleCluster

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `population_weight` | mapper | Approximate cluster size share. | Count of grouped evidence items divided by active items. | Fixture-derived local proxy. |
| `activity_weight` | mapper | Relative activity level of a cluster. | Based on group count and bounded scaling. | Fixture-derived local proxy. |
| `emotion_load` | mapper | Approximate emotional load. | Derived from stance bucket and signal classification. | Local text heuristic. |
| `expression_intensity` | mock schema and summary | Visual intensity of expression. | Used with activity weight to calculate active intensity. | Local visual proxy. |
| `grievance_memory` | mapper and mock schema | Whether a cluster carries unresolved dissatisfaction. | Bucket and signal dependent. | Local heuristic. |
| `bridge_power` | mapper | Whether a cluster can bridge camps. | Higher for neutral or bridge buckets. | Local heuristic. |

Interpretation:

- PeopleCluster is anonymous and aggregated.
- The prototype must not be presented as individual profiling or targeting.

### 3.5 Camp Dynamics

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `camp_distribution` | mock schema and mapper | Count or share by stance-like visual state. | Counts support, neutral, oppose, uncertain, bridge, and withdrawn clusters or evidence groups. | Local aggregate. |
| `conversion_score` | mapper and mock schema | Whether neutralization or shift is plausible in the visual model. | Mapper blends official neutral acceptance and neutral share. Mock scenario blends neutralization and deconstruction window. | Scenario heuristic. |
| `neutralization_score` | mapper and mock schema | Whether pressure can be reduced through explanation or deconstruction. | Mapper blends official pull, deconstruction bridge power, and neutral share. | Scenario heuristic. |
| `withdrawal_score` | mapper and mock schema | Whether users are likely to exit or cool down in the visualization. | Mapper blends withdrawn share and fatigue rate. | Scenario heuristic. |
| `hardening_score` | mapper and mock schema | Whether opposition becomes more entrenched. | Mapper blends oppose share and internal reinforcement. | Scenario heuristic. |
| `backlash_score` | mapper and mock schema | Whether a response could reactivate or intensify conflict. | Mapper blends deconstruction backlash risk and EchoBox breakout risk. | Scenario heuristic. |

### 3.6 DeconstructionCore

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `threat_deflation` | mapper and mock schema | Ability of community explanation or meme framing to lower perceived threat. | Mapper uses confidence. Mock scenario uses deconstruction fit. | Local heuristic. |
| `humor_acceptance` | mapper and mock schema | Whether lighter framing can be accepted. | Mapper uses base plus confidence. Mock scenario uses deconstruction fit. | Local heuristic. |
| `neutralization_power` | mapper and mock schema | Ability to reduce conflict intensity. | Mapper uses deconstruction influence bridge power. Mock scenario uses deconstruction window. | Local heuristic. |
| `withdrawal_power` | mapper and mock schema | Ability to encourage cooling or exit. | Mapper uses base plus confidence. Mock scenario uses withdrawal score. | Local heuristic. |
| `backlash_risk` | mapper and mock schema | Risk that deconstruction causes backlash. | Mapper uses risk flags. Mock scenario uses preset backlash. | Local heuristic. |
| `meme_replicability` | mapper and mock schema | Whether a meme-like frame can spread in the prototype. | Mapper uses share count. Mock scenario uses deconstruction fit. | Local heuristic. |

### 3.7 ResponseTempo

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `deconstruction_window_score` | mapper and mock schema | Whether the current phase is suitable for deconstruction or explanation. | Mapper blends deconstruction fit, neutral share, and backlash. Mock scenario uses preset. | Local heuristic. |
| `clarification_priority` | mapper and mock schema | Priority of transparent official clarification. | Mapper and mock scenario both depend on official pull and neutralization. | Local heuristic. |
| `faq_priority` | mapper and mock schema | Priority of FAQ or long-form explanation. | Depends on third-party or explanation pull and neutralization. | Local heuristic. |
| `third_party_explanation_priority` | mapper and mock schema | Priority of third-party explanation. | Depends on third-party pull. | Local heuristic. |
| `wait_and_monitor_score` | mapper and mock schema | Whether waiting and monitoring may be safer. | In mock scenario, reduced by breakout risk. | Local heuristic. |

### 3.8 ReputationMemory

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `unresolved_grievance_score` | mapper and mock schema | Remaining unresolved dissatisfaction. | Mapper blends dormant cluster share and breakout risk. Mock scenario uses preset. | Local heuristic. |
| `stigma_persistence` | mapper and mock schema | Persistence of negative label or reputation trace. | Mapper blends unresolved grievance and internal reinforcement. | Local heuristic. |
| `meme_persistence` | mapper and mock schema | Persistence of meme or community memory. | Mapper uses deconstruction window. Mock scenario uses deconstruction fit and backlash. | Local heuristic. |
| `trust_recovery` | mapper and mock schema | Possibility of trust recovery in visualization. | Mapper uses unresolved grievance and clarification priority. Mock scenario uses unresolved grievance and neutralization. | Local heuristic. |

### 3.9 C-End Public Event Mock Display

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `heat_score_mock` | `frontend/src/data/publicEventSamples.js` | Display heat for public event cards. | Static local sample field. | Mock display only. |
| `controversy_score_mock` | public event sample | Display controversy level. | Static local sample field. | Mock display only. |
| `breakout_risk_mock` | public event sample | Display breakout risk level. | Static local sample field. | Mock display only. |

These fields are public-event mock fields. They should not be described as real heat, natural public-opinion volume, or platform-wide measurement.

### 3.10 Helldivers Timeline Preset Metrics

| Metric | Current source | Meaning | Current calculation | Status |
| --- | --- | --- | --- | --- |
| `phase` | Helldivers timeline preset | Local T0 to T6 timeline stage. | Static preset stage. | Local narrative preset. |
| `echo_box_effects` | timeline preset | Stage-specific EchoBox visual changes. | Static preset fields mapped into scenario state. | Local narrative preset. |
| `camp_effects` | timeline preset | Stage-specific camp visual changes. | Static preset fields. | Local narrative preset. |
| `v2_metrics` | timeline preset | Stage-specific V2 metric snapshot. | Static preset fields. | Local narrative preset. |
| `visual_effects` | timeline preset | Aura, saturation, or pulse effects. | Static preset fields. | Local visual preset. |
| `response_recommendation` | timeline preset and scenario state | Stage-specific response label. | Static or mapped from response tempo. | Local narrative preset. |
| `sample_boundary_note` | sandbox copy | Limitations shown to viewer. | Static safety copy. | Required boundary copy. |

## 4. Future Candidate Metrics

These are not implemented as production metrics. They are candidate directions only.

| Candidate metric | Purpose | Possible basis | Status |
| --- | --- | --- | --- |
| Camp polarization index | Measure distance between stance camps. | Social influence and polarization modeling. | Literature/reference TBD. |
| Stance entropy | Measure diversity or concentration of stances. | Information theory and distribution diversity. | Literature/reference TBD. |
| Narrative dominance share | Measure which narrative core dominates attention. | Agenda-setting and attention allocation concepts. | Literature/reference TBD. |
| Bridge cluster centrality | Identify clusters that connect camps. | Network centrality and bridge-node concepts. | Candidate theory basis. |
| Echo chamber modularity | Estimate insulation of clusters. | Network modularity and homophily concepts. | Candidate theory basis. |
| Temporal burst score | Capture sudden attention spikes. | Event burst and self-excitation models. | Literature/reference TBD. |
| Source coverage completeness | Show how incomplete the evidence set may be. | Sampling and coverage reporting. | Candidate governance basis. |
| Confidence interval or uncertainty band | Avoid over-precision in visual scores. | Model card and uncertainty reporting practice. | Literature/reference TBD. |
| Review-adjusted influence score | Lower influence of weak or rejected evidence. | Sentigraph trust and review workflow. | Candidate internal basis. |
| Cross-source corroboration score | Reward independently observed evidence. | Evidence triangulation and provenance checks. | Candidate governance basis. |

## 5. Current Mock Or Local Fixture Metrics

Clearly mock or local fixture only:

- `heat_score_mock`
- `controversy_score_mock`
- `breakout_risk_mock`
- Helldivers T0 to T6 timeline preset fields
- mock schema scenario outputs from `PARAMETER_SOURCE = frontend_mock_schema_v1`
- fixture mapper outputs from `PARAMETER_SOURCE = frontend_evidence_fixture_mapper_v1`

## 6. Metrics With Candidate Theory Basis

The following have a plausible candidate theory basis, but are not yet calibrated or validated:

- `echo_chamber_score`: homophily, repeated exposure, and echo chamber concepts.
- `permeability_score`: bridge and cross-camp exposure concepts.
- `bridge_power`: network bridge or boundary-spanning concepts.
- `gravitational_pull`: attention, source salience, and narrative pull concepts.
- `deconstruction_window_score`: response timing and intervention-window concepts.
- `stigma_persistence`, `meme_persistence`, `reactivation_risk`: reputation memory and long-tail issue recurrence concepts.

The local research references are:

- `docs/research/opinion_ecosystem_model_v1.md`
- `docs/research/opinion_ecosystem_weight_calculation_v1.md`
- `docs/research/evidence_to_opinion_ecosystem_mapping_v1.md`
- `docs/research/evidence_to_opinion_ecosystem_mapping_contract_v1.md`
- `docs/research/opinion_ecosystem_sandbox_v2_visual_interaction_spec.md`
- `docs/research/sentigraph_ethical_public_opinion_simulation_research_report.md`

## 7. Literature Or Reference TBD

The following currently need explicit literature reference, benchmark, or calibration design before being treated as more than prototype heuristics:

- exact numeric weights in `computeEvidenceConfidence`
- exact numeric weights in `buildEchoBoxes`
- exact numeric weights in `buildCampDynamics`
- exact numeric weights in `buildResponseTempo`
- exact numeric weights in `buildReputationMemory`
- threshold values used to choose recommendation labels
- T0 to T6 Helldivers timeline preset values
- public-event display scores such as `heat_score_mock`

## 8. Do-Not-Claim List

Do not claim:

- full-web coverage
- full-platform coverage
- full-thread coverage
- official verification of the selected sample
- causal proof
- individual-level profiling
- real platform action
- real platform API or LLM execution
- production-grade simulation
- guaranteed forecasts or moderation outcomes

