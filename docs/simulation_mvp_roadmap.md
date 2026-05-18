# Simulation Lab MVP Roadmap

Status: MVP backend scaffold, frontend bubble visualization, A/B intervention comparison, and deterministic content visibility backlash modeling are implemented. Richer animation, V2 dynamics, empirical calibration, and real-data replay remain roadmap items.

The roadmap is staged to keep the first version deterministic, offline, explainable, and hard to misuse.

## MVP: Deterministic Toy Simulator

Goal: build a small, auditable simulator that demonstrates aggregate scenario rehearsal without real data calls, real LLM calls, or manipulation tactics.

MVP scope:

- Deterministic toy simulator.
- Friedkin-Johnsen style opinion persistence.
- Bounded-confidence gate.
- Threshold-based public expression.
- Homophilous static network.
- Source credibility and framing.
- Attention decay.
- Transparent intervention packages.
- Simple lawful content-removal and visibility-intervention scenario comparison.
- Deterministic visibility backlash model for exposure reduction, trust loss, spillover, neutral-audience impact, and human-review recommendation.
- Simple 2D bubble visualization.

Suggested MVP work packages:

1. Schema and safety gate design
   - Add conceptual schemas as backend models.
   - Add allowed/forbidden intervention validation.
   - Ensure all outputs are aggregate.

2. Synthetic scenario fixtures
   - Create toy crisis scenarios.
   - Include baseline, clarification, apology, compensation, FAQ, progress update, third-party evidence, and correction variants.
   - Keep all data synthetic.

3. Opinion kernel
   - Implement Friedkin-Johnsen update.
   - Add DeGroot docking baseline for validation.
   - Add bounded-confidence neighbor gate.

4. Public expression rule
   - Implement threshold-based expression.
   - Include local social proof, fatigue, source credibility, and attention.
   - Do not model covert amplification.

5. Attention layer
   - Implement simple exponential decay.
   - Add shock and fatigue parameters.
   - Keep parameters visible to users.

6. Intervention layer
   - Implement transparent intervention packages only.
   - Include policy-based moderation actions only when lawful or platform-authorized.
   - Add safety warnings for unsupported, vague, or overclaiming interventions.
   - Block forbidden tactic categories.

7. Output metrics
   - Aggregate risk movement.
   - Topic risk movement.
   - Polarization.
   - Cross-cutting exposure.
   - Correction uptake.
   - Trust recovery.
   - Exposure reduction.
   - Backlash cost.
   - Trust loss.
   - Spillover risk.
   - Removal legitimacy score.
   - Ethical-risk warnings.

8. Frontend visualization
   - Simple 2D bubble visualization.
   - Scenario controls limited to backend-approved ethical intervention types.
   - Event/intervention cards and deterministic step timeline.
   - Aggregate metrics and explanation cards.
   - Scenario comparison cards.
   - Assumption and uncertainty panel.
   - No controls for real APIs, real LLMs, or covert tactics.

9. Benchmarks
   - Friedkin-Johnsen convergence and stubbornness cases.
   - Bounded-confidence fragmentation cases.
   - Threshold expression cases.
   - Intervention package comparison cases.
   - Content-removal tradeoff cases.
   - Ethics guardrail rejection cases.

MVP moderation scenario comparisons may include:

- remove high-reach negative video
- no response
- clarification
- removal plus transparent policy explanation
- labeling plus clarification

MVP acceptance:

- Runs offline.
- Deterministic benchmark output.
- No real API calls.
- No real LLM calls.
- No live public fetch.
- No individual targeting.
- No manipulation tactic output.
- Moderation scenarios must be lawful/platform-authorized, policy-based, transparent, and aggregate-level.
- Clear uncertainty and assumption labels.

## V2: Richer Dynamics After MVP Validation

V2 should begin only after the MVP has stable benchmarks, user-facing explanations, and an ethics review.

V2 scope:

- Deffuant micro-interaction.
- Watts cascade diagnostics.
- Complex contagion.
- Latent versus expressed opinion split.
- Platform-specific feed affordances.
- Hawkes-style burst modeling.

V2 acceptance:

- Each new module docks against simpler MVP baselines.
- Each module can be disabled independently.
- Outputs remain aggregate and explainable.
- Benchmarks include sensitivity and ablation tests.
- No real API or real LLM integration is implied by V2.

## Later Research

Hold these until the simulator is validated on historical or carefully reviewed synthetic events:

- Dynamic network rewiring.
- Cross-platform diffusion.
- Empirical calibration.
- Historical replay validation.
- Optional real LLM narrative generation only after safeguards.

Later-stage acceptance:

- Strong validation plan.
- Privacy and safety review.
- Real data approvals, if any.
- Redaction and audit controls.
- Explicit user approval before enabling any real external service.

## Stop Conditions

Pause implementation if:

- A feature requires real personal data before privacy review.
- A requested output ranks individual people or accounts.
- A scenario asks for fake consensus or bot amplification.
- A scenario asks for covert seeding or deceptive diversion.
- A scenario asks for illegal suppression, covert censorship, or evading platform governance.
- A scenario asks for individual accounts to be silenced or ranked for restriction.
- Model results are presented as certain predictions rather than scenario estimates.
- Benchmarks become flaky or impossible to explain.

## Recommended First Implementation Task

After the backend scaffold, frontend MVP page, A/B comparison mode, and visibility backlash model, the next implementation task should be:

QA-stabilize the visibility tradeoff UI and benchmark results, then add richer animation/replay controls or a safe aggregate assumption editor. Do not move to empirical calibration, real-data replay, or real LLM narrative generation until the deterministic MVP remains stable under benchmarks and manual demo checks.

## Implementation Checkpoint

As of 2026-05-18, the backend-only deterministic MVP scaffold has been implemented:

- `backend/app/services/simulation/` contains the synthetic agent, network, message, intervention, opinion update, attention, metrics, and engine modules.
- API endpoints are available under `/api/v1/simulation`.
- Forbidden intervention types are rejected before simulation.
- The offline benchmark runner includes a `simulation_lab` suite with synthetic scenarios.

The roadmap does not change for advanced work: richer ABM calibration, V2 dynamics, historical replay, and any optional real LLM narrative generation remain future work after QA and safety review.

## Frontend Visualization Checkpoint

As of 2026-05-18, the frontend Simulation Lab MVP page has been implemented and QA-stabilized:

- `frontend/src/pages/SimulationLab.jsx` renders a desktop-first bubble simulation page.
- The sidebar exposes `Simulation Lab / 舆情预演沙盘`.
- The page loads the deterministic demo scenario and ethics policy from existing backend endpoints.
- The page can run `POST /api/v1/simulation/run` with allowed interventions only.
- The bubble canvas displays synthetic agents by opinion color, centrality proxy size, attention opacity, and active influence glow.
- The UI includes event cards, aggregate metrics, explanation cards, timeline steps, and an A/B comparison mode.
- Forbidden intervention categories are not exposed as usable controls.
- Browser smoke with local backend/frontend servers confirmed route wiring, run/step controls, bubble rendering, event cards, aggregate metrics, explanation cards, and timeline updates.
- Frontend production build passed with the existing non-blocking Ant Design/ECharts chunk warning.

## Frontend A/B Comparison Checkpoint

As of 2026-05-18, the Simulation Lab page includes A/B intervention comparison:

- Users can switch between `single scenario` and `A/B strategy comparison` modes.
- A and B start from the same loaded demo scenario initial state.
- Each side can select only intervention types allowed by the backend ethics policy.
- The comparison reuses the existing local `POST /api/v1/simulation/run` endpoint twice instead of adding real APIs, crawlers, or real LLM calls.
- The frontend computes aggregate deltas for risk proxy, negative ratio, polarization, trust recovery, backlash-risk proxy, and ethical risk notes.
- The comparison output is explicitly human-review-oriented and does not automatically execute any strategy.
- Forbidden intervention categories remain absent from selectable controls.

## Frontend A/B Comparison QA Checkpoint

As of 2026-05-18, the A/B comparison UI has been QA-stabilized:

- Local browser smoke validated single-scenario mode and A/B strategy comparison mode.
- The requested A/B pairs were exercised: `no_response` vs `clarification`, `no_response` vs `apology`, `no_response` vs `third_party_evidence`, and `clarification` vs `misinformation_correction`.
- The summary shows both user-facing aggregate deltas and scalar field chips for `better_option`, `risk_delta`, `negative_ratio_delta`, `polarization_delta`, `trust_recovery_delta`, and `ethical_risk_notes`.
- The backend ethics policy still allows only transparent aggregate crisis-response interventions and rejects forbidden interventions.
- No `/simulation/compare` endpoint was added; the frontend still reuses the safe deterministic simulation run endpoint twice.
- Backend tests and offline benchmarks were not rerun for this QA pass because no backend simulation algorithm or benchmark code changed.

## Content Visibility Backlash Model Checkpoint

As of 2026-05-18, Simulation Lab includes deterministic content visibility backlash modeling:

- Backend schemas include `VisibilityIntervention`, `BacklashModel`, `AudienceImpactBreakdown`, and `VisibilityInterventionResult`.
- Allowed visibility intervention types include `content_removal`, `comment_closure`, `account_restriction`, `visibility_reduction`, `platform_labeling`, `policy_enforcement_notice`, and `content_removal_with_explanation`.
- The deterministic model estimates exposure reduction, backlash cost, trust loss, spillover risk, net risk change, removal legitimacy, neutral-audience impact, and hard-opposition impact.
- A high-reach negative video demo scenario is available through the backend scenario builder for benchmark and test use.
- The frontend A/B comparison page can show a content visibility tradeoff panel for allowed visibility actions such as `content_removal_with_explanation`, `visibility_reduction`, and `platform_labeling`.
- Outputs remain aggregate-level, human-review-oriented, and non-executing.

## Content Visibility QA Checkpoint

As of 2026-05-18, the content visibility backlash model and A/B tradeoff UI are QA-stabilized:

- Backend tests cover supported visibility type registration, high-reach exposure reduction sensitivity, low-legitimacy backlash and trust-loss increase, transparent-explanation backlash reduction, screenshot-driven spillover increase, reactance-driven hard-opposition impact, neutral-audience high concern, 0-100 score clamping, API visibility-result shape, and aggregate-only output.
- Offline `simulation_lab` benchmark cases include visibility intervention expectations for exposure reduction, backlash cost, and safe human-review-oriented recommendations.
- Browser smoke confirmed the `no_response` vs `透明说明后内容移除` A/B flow, the `内容可见性干预` tradeoff panel, and the absence of forbidden manipulation or illegal/covert suppression options from selectable controls.
- The model remains a scenario-review artifact only. It does not execute platform actions, name accounts, rank individuals, or produce suppression playbooks.

Remaining frontend roadmap items:

- Richer A/B replay controls and advanced comparison charts.
- Richer animation and replay controls.
- Assumption editor for safe aggregate parameters.
- Historical replay only after validation and data-approval review.

## Case-to-Simulation Initializer Checkpoint

As of 2026-05-18, Simulation Lab can initialize a synthetic scenario from completed Sentigraph cases:

- The backend converts aggregate case analysis outputs into EventFrame, SubIssue, AudienceSegment, PersonaCluster, FrameGapAnalysis, StrategyImplication, and SimulationScenario objects.
- The frontend Simulation Lab page includes `从案例初始化沙盘`, initialization preview, and a compact event-frame/audience/gap summary.
- The generated agents are synthetic audience bubbles only; they are not real accounts.
- The initializer does not call real APIs, real LLM APIs, crawlers, or live public fetchers.
- Outputs remain aggregate-level and human-review-oriented.

Next Simulation Lab task:

- QA-stabilize case initialization in the browser, then add a safe aggregate assumption editor or richer replay controls.
