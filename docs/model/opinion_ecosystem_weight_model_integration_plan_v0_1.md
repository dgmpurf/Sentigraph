# Opinion Ecosystem Weight Model Integration Plan v0.1

Status: docs-only / design-stage / no implementation.

This plan does not implement backend schema, frontend UI, calculator code, real LLM, real API, real platform provider, production Evidence import, production case, analysis run, B-end report runtime, Sandbox runtime, or public event runtime.

## 1. Current Status

- Model docs exist only as design references.
- No runtime calculator exists.
- No backend schema is added.
- No frontend UI is added.
- No tests are added in this phase.
- No real API or real LLM is used.
- No crawler or scraping behavior is added.

## 2. Recommended Future Phases

1. Phase 8N-h docs review and source update.
2. Phase 8O mock fixture calculator design only.
3. Phase 8P deterministic local calculator implementation, if approved.
4. Phase 8Q frontend explanatory UI, if approved.
5. Phase 8R model card QA / screenshot smoke.
6. Later: calibration only after historical replay dataset and human review comparison.

## 3. Do Not Implement Now

- backend schema
- frontend UI
- calculator code
- real LLM
- real API
- real platform provider
- production Evidence import
- production case
- analysis run
- B-end report runtime
- Sandbox/public event runtime

## 4. Future Implementation Rules

Future Codex implementation must:

- start with tests
- use no real APIs
- use no real LLMs
- use local fixtures only
- include `model_status`
- include `calibration_status`
- include `scope_note`
- include boundary flags
- include human-review gates
- keep response strategy non-executable

## 5. Required Future Tests

Future tests must cover:

- low-trust evidence damping
- duplicate evidence not infinitely amplifying heat or risk
- rejected evidence excluded
- forbidden personal fields blocked
- no auto-execute response strategy
- no full-web or full-platform claim in output
- no official verification claim in output
- no causal proof claim in output
- PeopleCluster not represented as real person
- InfluenceCore not represented as person ball
- EchoBox not represented as real community map

## 6. Output Metadata Requirements

All future outputs must include:

```json
{
  "model_status": "design_stage_or_runtime_versioned",
  "coefficient_source": "mock_default",
  "calibration_status": "uncalibrated",
  "empirical_validation": "not_started",
  "scope_note": "selected_sample_or_local_fixture_only",
  "human_review_required": true
}
```

## 7. Gate Placement

Suggested placement before any future public-facing use:

```text
Evidence governance
-> Review queue completion
-> Dedup group review completion
-> Analysis-ready promotion
-> Local calculator, if approved
-> Model card QA
-> Human review
-> Report or Sandbox explanation gate
```

## 8. Stop Conditions

Stop implementation if any future output:

- implies full-web coverage
- implies full-platform coverage
- implies official verification
- implies causal proof
- implies future prediction
- implies personality diagnosis
- implies individual persuasion scoring
- implies automatic response execution
- requires secrets, cookies, sessions, browser profiles, or hidden APIs
- requires crawler, scraping, or real platform collection

## 9. Source Update Recommendation

After these docs are reviewed and committed, update Project Source only after user approval:

- Source 00: current phase/status note.
- Source 08: model documentation inventory.
- Source 09: Sandbox / Opinion Ecosystem conceptual boundary.
- Source 10: playtest/demo boundary reference.

Do not update Project Source automatically in this phase.
