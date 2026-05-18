# Simulation Lab MVP Roadmap

Status: roadmap only. No Simulation Lab product code has been implemented.

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
   - Add safety warnings for unsupported, vague, or overclaiming interventions.
   - Block forbidden tactic categories.

7. Output metrics
   - Aggregate risk movement.
   - Topic risk movement.
   - Polarization.
   - Cross-cutting exposure.
   - Correction uptake.
   - Trust recovery.
   - Ethical-risk warnings.

8. Frontend visualization
   - Simple 2D bubble visualization.
   - Scenario comparison cards.
   - Assumption and uncertainty panel.
   - No controls for real APIs, real LLMs, or covert tactics.

9. Benchmarks
   - Friedkin-Johnsen convergence and stubbornness cases.
   - Bounded-confidence fragmentation cases.
   - Threshold expression cases.
   - Intervention package comparison cases.
   - Ethics guardrail rejection cases.

MVP acceptance:

- Runs offline.
- Deterministic benchmark output.
- No real API calls.
- No real LLM calls.
- No live public fetch.
- No individual targeting.
- No manipulation tactic output.
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
- Model results are presented as certain predictions rather than scenario estimates.
- Benchmarks become flaky or impossible to explain.

## Recommended First Implementation Task

After this design is reviewed, the next implementation task should be:

Build a backend-only deterministic Simulation Lab toy service with synthetic fixtures, allowed/forbidden intervention validation, and offline benchmarks. Do not add frontend visualization until the toy service and guardrails pass.
