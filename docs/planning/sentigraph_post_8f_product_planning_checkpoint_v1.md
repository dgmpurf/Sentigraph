# Sentigraph Post 8F Product Planning Checkpoint v1

Status: docs-only product planning checkpoint.

This document does not implement code, continue backend helper extraction, refactor backend or frontend files, modify runtime records, change Project Source files, run provider or collector jobs, write the Evidence Layer, create production cases, generate reports, create public access, or enable external delivery.

## 1. Executive Decision

Decision: pause broad AnalysisRequests refactor now.

Recommended approach: mixed approach with product-first priority.

- Primary path: pause further helper extraction and shift to product, demo, feedback, and business-readiness work.
- Allowed technical path: only small, no-behavior-change helper extractions when a concrete product/demo task is blocked by maintainability risk.
- Disallowed path: continuing broad store, schema, route, frontend, public-access, delivery, or report-runtime refactors by momentum alone.

## 2. Recommended Answer

Sentigraph should pause additional AnalysisRequests helper refactor after 8A-8F and move to product/demo/business priorities.

The best next task is a second-round C-end and B-end guided playtest preparation pass, using the current public event, Opinion Ecosystem Sandbox, B-end report sample, evidence governance, and safety-boundary surfaces.

The technical refactor can remain on standby. The golden-contract tests and tiny helper extraction have reduced enough immediate risk that the next decision should be market and demo validation, not more internal cleanup.

## 3. Why

### Technical Risk

8A-8F reduced the immediate danger of changing the AnalysisRequests governance spine:

- 8A documented the modularization strategy and no-behavior-change rules.
- 8B created a backend golden-contract inventory and test harness.
- 8C identified timestamp / ID helpers as the safest first extraction target.
- 8D added the first tiny shared helper.
- 8E selected one adjacent next helper candidate.
- 8F extended usage to a small adjacent ID helper family and then stopped.
- 8F checkpoint smoke passed with no file changes and no commit needed.

That is enough technical risk reduction for the current checkpoint. More refactor now has diminishing returns because the core product questions are no longer blocked by missing helper abstraction.

### Product Value

The highest-value unknowns are now product-facing:

- Do C-end users understand what the public event platform is for?
- Do users trust the sample, coverage, and safety boundaries?
- Can users distinguish PeopleCluster from InfluenceCore?
- Do B-end reviewers see decision-support value in the report sample?
- Do demo viewers understand that Sentigraph is not a full-web crawler, official truth source, or automatic action system?
- Are the current screenshots, recording scripts, and guixutech.com materials strong enough for external review?

These questions cannot be answered by further backend helper extraction.

### Demo Readiness

The current product surface is demo-rich:

- C-end public event platform prototype.
- Event Plaza and public event detail pages.
- Opinion Ecosystem Sandbox V2 with local timeline presets.
- Helldivers and Chinese-event demo assets.
- B-end report sample pages.
- Analysis Requests governance chain.
- Evidence trust, dedup, review, audit, import, staging, promotion, analysis, report, export, package, and public-access gate records.
- Static website and formal copy under `website/` and docs.

The demo now needs packaging, smoke, and feedback, not another internal refactor phase.

### Business And Compliance Readiness

Business readiness depends on clearer external-facing materials:

- C-end feedback scripts and scoring.
- B-end professional feedback questions.
- Demo screenshot and recording package.
- Website / ICP / platform-review copy.
- Vendor sample POC checklist and scorecard.
- Platform permission tracking.

These are safer and more valuable near-term than expanding live integrations, report delivery, or large backend modularization.

## 4. Current State After 8A-8F

### Technical State

- AnalysisRequests remains the local governance spine for the provider result, import, review, dedup, promotion, manual analysis, report, export, package, and public-access / external-delivery chain.
- `analysis_request_store.py` remains the compatibility facade.
- Route URLs and response contracts remain stable.
- Runtime records remain under ignored local runtime folders.
- Golden-contract tests protect key route families, schema availability, ignored paths, and latest public-access / external-delivery non-capabilities.
- The shared helper module exists for compact UTC timestamps and prefixed runtime IDs.
- Helper usage is intentionally narrow and low-risk.

### Product State

- The public event and demo surfaces are strong enough for structured feedback.
- Current evidence and report flows remain governance-heavy and clearly bounded.
- LLM semantic annotation, B-end export packaging, Response Strategy Lab, and backend Opinion Ecosystem schemas remain future or docs-only work.
- Search/RSS/GDELT, vendor, and collector integrations remain bounded by mock, fixture, local file, or offline handoff rules.

## 5. Refactor Risk Assessment

### Risk Reduced

The following risks have been reduced:

- Accidental route-family drift during future refactor.
- Missing latest-chain schema classes.
- Runtime/build/benchmark ignore regressions.
- Dangerous public-access or external-delivery primitives appearing in the router.
- Latest public-access / external-delivery functions reading export artifact content or generating delivery behavior.
- Repeated timestamp / ID generation drift in the selected helper area.

### Risk That Remains

The following risks still remain if refactoring continues:

- Large store/schema/route/frontend files still have many phase-specific policies interleaved.
- Generic helpers could weaken conservative phase-specific blockers.
- Runtime path helper extraction could break persisted local record discovery.
- Audit helper extraction could alter append-only ordering or audit shape.
- Boundary flag helper extraction could hide explicit false flags behind a too-broad abstraction.
- Frontend section extraction could remove visible boundary copy or change form payloads.
- API helper splitting could duplicate base URL handling or produce raw object rendering regressions.

### Stop Rule For Further Large Refactor

Do not continue broad refactor unless at least one of these is true:

- A product task is blocked by maintainability in AnalysisRequests.
- A bug or regression requires isolating a shared helper.
- A new governance phase would otherwise duplicate high-risk code.
- The team explicitly approves a small refactor plan with named files, no behavior change, and fresh validation commands.

Even then, only one tiny family should move per task.

## 6. Product Priority Assessment

### Priority 1: C-End And B-End Second-Round Playtest

Value: highest.

Reason: the product now needs evidence from real viewers about clarity, trust, usefulness, and commercial interest.

Why now:

- The C-end public event platform exists.
- Sandbox V2 and event timeline presets are visible.
- Request/vote mock flow is available.
- B-end report samples and professional risk/report docs exist.
- Feedback can identify whether more product polish or model/schema work is needed.

### Priority 2: Demo Screenshot / Recording Package Refresh

Value: high.

Reason: a clean asset package makes the project understandable to collaborators, customers, platform reviewers, and partners.

Why now:

- The UI has evolved beyond older v6.x screenshots.
- Current demo should show C-end flow, B-end report sample, Sandbox V2, safety copy, and boundaries.
- Screenshots help catch misleading labels before external sharing.

### Priority 3: Business / Compliance Packaging Checkpoint

Value: high.

Reason: guixutech.com, ICP materials, platform-review wording, vendor POC policy, and evidence-provider boundaries shape whether the product can be explained safely.

Why now:

- Website copy and static site exist.
- Vendor POC docs and mapper exist.
- Platform permission boundaries are still pending.
- External reviewers need conservative, consistent language.

### Priority 4: Response Strategy Lab Docs-Only Spec

Value: medium.

Reason: it could clarify safe response recommendations, but it should follow feedback so it does not optimize the wrong workflow.

### Priority 5: LLM Semantic Annotation Mock Fixture / Validator Scaffold

Value: medium.

Reason: it is useful for future interpretation, but real LLM remains mock-only and should not precede user validation.

### Priority 6: Backend Opinion Ecosystem Schema-Only Design

Value: medium.

Reason: it can prepare future backend authority for frontend-only concepts, but should not be implemented until the current visual model receives feedback.

## 7. Recommended Next 3 Tasks

### Task 1: Second-Round C-End And B-End Playtest Preparation

Goal: prepare a guided feedback round that tests clarity, trust, usefulness, and commercial interest.

Scope:

- Refresh demo path checklist for Event Plaza, public event detail, Sandbox V2, request/vote mock, B-end consultation mock, and B-end report sample.
- Add a feedback capture sheet or doc.
- Define red-flag observations and success signals.
- Keep all search, vote, request, and report actions clearly labeled as local/mock/demo where applicable.

Validation / QA:

- `git status --short`
- If docs-only: `git diff --check`
- If UI copy changes are explicitly approved later: `npm --prefix frontend run build` and browser smoke for demo pages.

Suggested Codex mode: gpt-5.5 high.

Suggested ChatGPT mode: Thinking.

### Task 2: Demo Screenshot / Recording Package Refresh

Goal: produce a current asset checklist and capture plan for C-end, B-end, and governance-chain demos.

Scope:

- Update screenshot list for public events, Sandbox V2, B-end reports, Analysis Requests governance panels, and safety boundaries.
- Capture or plan captures only after the user approves browser screenshot work.
- Avoid recording secrets, terminals with environment values, private browser state, or local collector internals.

Validation / QA:

- Docs-only package refresh: `git diff --check`.
- Screenshot capture: browser visual QA, console scan, no `[object Object]`, no `undefined`, no `NaN`, no 500 prompt.
- Build only if frontend code changes, which should not be needed for screenshot capture.

Suggested Codex mode: current Codex GPT-5.5 with low/medium reasoning effort for mechanical screenshot capture if the task is purely capture/checklist; use gpt-5.5 high for visual QA or if screenshots need interpretation.

Suggested ChatGPT mode: Thinking.

### Task 3: Business / Compliance Packaging Checkpoint

Goal: align website, ICP/platform-review materials, vendor POC gates, and real-vs-mock boundaries before broader external review.

Scope:

- Check guixutech.com static pages and docs for stale wording.
- Confirm no claim of full-web coverage, full-platform capture, live RSS/GDELT/search provider, live vendor adapter, MediaCrawler integration, OpenClaw production ingestion, or real LLM.
- Refresh platform permission tracking and vendor POC next-action notes.

Validation / QA:

- `git diff --check`
- Static wording scan for overclaims.
- No backend tests or frontend build unless code changes unexpectedly.

Suggested Codex mode: gpt-5.5 high.

Suggested ChatGPT mode: Thinking; use Pro only if making major business, compliance, ICP, platform-permission, or legal-positioning decisions.

## 8. Tasks To Defer

Defer the following until after playtest or business-review evidence:

- Broad AnalysisRequests store, schema, route, frontend, or API helper splitting.
- Runtime path helper extraction.
- Append-only audit helper extraction.
- Boundary flag builder extraction.
- Safe metadata projection helper extraction.
- Eligibility blocker/warning helper extraction.
- Real public access or external delivery runtime.
- Public download route.
- File-byte response route.
- ZIP or binary archive generation.
- Public URL or signed URL generation.
- Email sending.
- Object storage upload.
- Portal publication.
- B-end report generation runtime.
- Sandbox/public event generation runtime.
- Production Evidence Layer write.
- Production case, review queue, or dedup creation from the governance chain.
- Real platform APIs beyond explicitly configured optional local YouTube demo.
- Real search, RSS, GDELT, vendor, or LLM integrations.
- MediaCrawler integration.
- OpenClaw production ingestion.

## 9. Safety And Compliance Boundaries

The next phase must preserve these boundaries:

- Sentigraph is not a full-web crawler.
- Evidence Scale / Coverage does not mean full-web or full-platform coverage.
- Search Discovery, RSS, and GDELT remain mock/static unless future provider gates are approved.
- Vendor POC remains offline sample mapping, not a live vendor adapter.
- Vendor evidence is vendor-attested only when documented; it is not official verification.
- LLM provider remains mock unless a separate reviewed real-provider gate is approved.
- MediaCrawler is not integrated.
- OpenClaw / external agents are not production ingestion.
- Public event request/vote flows are mock unless a future product decision changes them with explicit labeling.
- PeopleCluster represents anonymous groups or clusters, not real individuals.
- InfluenceCore represents content, narrative, official, media, meme, or similar cores, not people balls.
- Reports and simulations are decision support, not causal proof, guaranteed prediction, or real-world platform action.

## 10. Validation / QA Needed Per Recommended Task

| Recommended task | Minimum validation | Browser QA | Backend tests | Frontend build |
| --- | --- | --- | --- | --- |
| Second-round playtest prep | `git diff --check`, static wording scan | only if UI/copy changes | not needed for docs-only | only if frontend changes |
| Demo screenshot / recording refresh | `git status --short`, screenshot list completeness | yes for captures | not needed | not needed unless frontend changes |
| Business / compliance packaging checkpoint | `git diff --check`, overclaim scan | optional static website visual check | not needed for docs-only | not needed unless frontend changes |

## 11. Source Update Recommendation

Do not modify Project Source files in this checkpoint.

After user approval, Source 00 and Source 11 may need a small update only if they currently present Phase 8 as an active refactor chain rather than a completed guardrail checkpoint followed by product planning.

Recommended update wording if approved later:

- Phase 8A-8F established AnalysisRequests refactor guardrails, golden contracts, and two tiny no-behavior-change helper extractions.
- Current recommended direction is product/demo/business validation before further refactor.
- Further helper extraction should remain tiny, justified, and validated.

## 12. Suggested Modes For Next Tasks

| Next task | Codex mode | ChatGPT mode |
| --- | --- | --- |
| Second-round C-end/B-end playtest preparation | gpt-5.5 high | Thinking |
| Demo screenshot / recording package refresh | current Codex GPT-5.5 with low/medium reasoning effort for mechanical screenshot capture if the task is purely capture/checklist; use gpt-5.5 high for visual QA or if screenshots need interpretation | Thinking |
| Business / compliance packaging checkpoint | gpt-5.5 high | Thinking; Pro only for major business/compliance decisions |
| Response Strategy Lab docs-only spec | gpt-5.5 high | Thinking |
| LLM semantic annotation mock fixture / validator scaffold | gpt-5.5 high | Thinking |
| Backend Opinion Ecosystem schema-only design | gpt-5.5 high | Thinking; Pro only if schema becomes a business-critical architecture decision |

## 13. What Should Not Be Built Yet

Do not build these in the next step:

- live platform integrations
- live search provider
- live RSS or GDELT provider
- live vendor adapter
- real LLM provider
- MediaCrawler integration
- OpenClaw production ingestion
- public download route
- file-byte response route
- public URL or signed URL generator
- external delivery
- email delivery
- object storage publishing
- portal publishing
- production B-end report delivery runtime
- production Evidence Layer write from AnalysisRequests governance records
- production case/review queue/dedup from review-only chain
- automatic public event generation from report or Sandbox outputs

## 14. Final Planning Recommendation

Final recommendation: pause refactor.

Use the next work cycle to test whether the current product story is understandable, trusted, and commercially interesting. Keep AnalysisRequests refactor guardrails in place, but do not spend the next phase on more helper extraction unless a concrete product/demo task exposes a blocker.

The next recommended task is second-round C-end and B-end playtest preparation.
