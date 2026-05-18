# Simulation Lab Research Basis

Status: research-to-design summary. This document formalizes the uploaded DeepSearch Simulation Lab research report for Sentigraph planning. It does not introduce product code, real API calls, real LLM calls, or manipulation tactics.

Priority labels:

- MVP: suitable for the first deterministic toy simulator.
- V2: useful after the MVP is benchmarked and explained.
- Later: hold until validation data and safety controls are stronger.

## Theory Mapping

| Theory | Core idea | Model variables | Sentigraph mapping | Priority | Limitations | Ethical constraints |
| --- | --- | --- | --- | --- | --- | --- |
| DeGroot opinion updating | Agents repeatedly average neighbor opinions until consensus or local equilibrium. | Neighbor weights, network adjacency, current opinion. | Baseline opinion kernel for checking whether Sentigraph simulations behave like a simple consensus model. | MVP as docking baseline | Too simple for stubbornness, identity, and polarization. | Use as transparent baseline only; do not infer individual persuasion routes. |
| Friedkin-Johnsen | Agents update from neighbors while retaining part of their initial opinion. | `stubbornness`, initial opinion, neighbor weights. | Core MVP opinion persistence model; supports realistic non-consensus outcomes. | MVP | Requires assumptions about stubbornness and initial opinion. | Keep parameters aggregate and synthetic; no person-level stubbornness scoring. |
| Hegselmann-Krause | Agents only interact with opinions within a bounded-confidence radius. | `confidence_radius`, opinion distance, accepted-neighbor set. | Echo chamber and opinion bubble gate; explains fragmentation and cluster persistence. | MVP | Confidence radius is hard to estimate from limited data. | Do not use to isolate or target resistant groups. |
| Deffuant-Weisbuch | Pairwise micro-interactions move opinions when agents are close enough. | Pairwise confidence threshold, convergence rate, interaction schedule. | Optional V2 micro-interaction kernel for richer scenario dynamics. | V2 | More sensitive to simulation schedule and random seeds. | Use only for aggregate rehearsal; no account-level interaction plans. |
| Granovetter threshold model | Public action happens when perceived participation exceeds an individual threshold. | `action_threshold`, perceived local action, social proof. | MVP public-expression rule for comment, share, correction uptake, or escalation. | MVP | Thresholds are assumed without direct observation. | Never use thresholds for coercive mobilization or suppression. |
| Watts cascade model | Global cascades depend on network structure and vulnerable nodes with low thresholds. | Degree, threshold, vulnerable-node share, seed location. | V2 diagnostic for cascade risk from aggregate topic states. | V2 | Cascade predictions are fragile without network calibration. | Do not recommend seed placement, covert amplification, or influencer exploitation. |
| Complex contagion | Some behaviors require repeated reinforcement from multiple sources. | Reinforcement count, repeated exposure, tie diversity. | V2 correction uptake, de-escalation, or coordinated clarification acceptance. | V2 | Hard to separate reinforcement from homophily. | Model transparent correction and clarification only, not coordinated manipulation. |
| Homophily and echo chambers | Similar agents connect and expose each other to similar views. | `identity_vector`, homophily strength, modularity, cross-cutting exposure. | Network construction, bubble metrics, bridge exposure, polarization analysis. | MVP | Homophily and contagion are confounded in observational data. | Do not infer causal manipulation levers or target identity groups. |
| Source credibility | Messages from trusted sources have larger attitude effects. | `source_credibility`, `authority_trust`, source type. | Compare official statement, third-party evidence, expert update, and peer discussion packages. | MVP | Trust varies by audience and context. | Use credibility to compare transparent sources; do not fabricate sources. |
| Framing theory | How information is framed affects interpretation and salience. | `framing`, issue emphasis, emotional valence, responsibility attribution. | Compare factual clarification, apology, progress update, compensation, and evidence-first framing. | MVP | Frame effects can be culture- and context-specific. | Do not generate deceptive, inflammatory, or manipulative frames. |
| Agenda-setting and issue-attention cycle | Public attention rises, competes, decays, and can be renewed by events. | Attention budget, decay rate, shock size, novelty, topic competition. | Attention layer for risk persistence, topic fadeout, and event shocks. | MVP | Attention dynamics need historical calibration. | Do not design deceptive diversion or distraction events. |
| Situational Crisis Communication Theory | Response strategy should fit crisis type, responsibility, and stakeholder harm. | Responsibility admission, empathy, evidence strength, corrective action. | Intervention package templates for apology, clarification, compensation, and progress updates. | MVP | Needs human judgment about responsibility and harm. | Use to support accountable response, not liability evasion or blame shifting. |
| Image Repair Theory | Organizations use denial, correction, mortification, compensation, or corrective action to repair reputation. | Response type, apology strength, compensation, corrective action, evidence. | Intervention library and report explanation of response options. | MVP | Some strategies may be inappropriate or unethical in real crises. | Block denial/deflection when unsupported by facts; forbid deceptive reputation repair. |
| Inoculation, prebunking, and misinformation correction | Warning or correction can reduce misinformation impact when factual and timely. | Correction timing, evidence strength, repetition, backfire risk warning. | Transparent misinformation correction and FAQ scenario packages. | MVP for correction packages; V2 for reinforcement effects | Correction effects are context-dependent and should not be overstated. | Correct false claims with evidence; do not weaponize prebunking against legitimate criticism. |
| ODD, ODD+D, and ABM validation | Agent-based models need formal purpose, entities, processes, decision rules, data, and validation. | Purpose, entities, state variables, schedule, assumptions, inputs, outputs. | Required documentation and benchmark workflow before implementation. | MVP | Documentation does not guarantee empirical validity. | Require audit trails, assumption logs, uncertainty labels, and human review. |

## Additional Research Signals

The report also highlights several ideas that should remain carefully staged:

- Confirmation bias and motivated reasoning can be modeled as message-weight modifiers, but must not become tools for exploiting identity or vulnerability.
- Negativity weighting helps simulate crisis attention but should not be used to craft fear-based messaging.
- Spiral-of-silence and public-commitment ideas can motivate a latent-versus-expressed stance split, but this should wait until V2 and remain aggregate.
- Hawkes-style self-exciting processes may help describe attention bursts, but only after historical replay validation.
- Dynamic network rewiring and cross-platform diffusion are later-stage research items because they are harder to validate and easier to misuse.

## Design Implications

The first Simulation Lab implementation should:

- Prefer Friedkin-Johnsen persistence over pure consensus.
- Use bounded-confidence gates to represent bubble boundaries.
- Use threshold rules for public expression.
- Use source credibility and framing as transparent intervention variables.
- Use attention decay and shock variables conservatively.
- Keep intervention modules swappable.
- Produce aggregate, uncertainty-labeled metrics.
- Log assumptions and run benchmarks before any user-facing claims are trusted.
