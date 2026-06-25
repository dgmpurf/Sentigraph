# Opinion Ecosystem Weight Model Card v0.1

Status: docs-only / design-stage / deterministic heuristic / sample-scoped / uncalibrated.

## 1. Model Identity

- Name: Sentigraph Opinion Ecosystem Weight Model v0.1
- Status: design-stage, not implemented
- Type: deterministic heuristic
- Scope: selected sample / imported evidence / local fixture only
- `coefficient_source = mock_default`
- `calibration_status = uncalibrated`
- `empirical_validation = not_started`

## 2. Intended Use

- Explain selected sample discussion structure.
- Support Sandbox V2 visual parameters.
- Support B-end report explanation.
- Compare transparent response options for human review.

## 3. Forbidden Use

- Full-web or full-platform coverage claims.
- Official verification claims.
- Causal proof claims.
- Future prediction claims.
- Personality diagnosis or psychological profiling.
- Individual persuasion scoring.
- Public-opinion control.
- Automatic response strategy execution.
- Harassment, targeting, fake consensus, covert manipulation, or astroturfing.

## 4. Input Contract

Allowed future inputs:

- reviewed or staged EvidenceItem metadata
- dedup-reviewed aggregate counts
- review status distributions
- trust / provenance / verification labels
- sample-scoped ContentAggregate fields
- anonymous aggregate PeopleCluster inputs
- InfluenceCore candidates from reviewed sample metadata

Disallowed inputs:

- raw author identifiers
- private messages
- cookies, tokens, sessions, browser profiles, localStorage, or secrets
- unreviewed personal sensitive data
- live crawler output treated as truth
- real LLM authenticity judgment

## 5. Output Contract

Every module output must include:

- model name and version
- sample scope
- model status
- coefficient source
- calibration status
- empirical validation status
- boundary flags
- confidence / uncertainty notes
- human review requirement where strategy is involved

## 6. Data vs Assumption

Data:

- imported or selected evidence metadata
- trust labels
- review decisions
- dedup groups
- source coverage summaries
- sample counts

Assumptions:

- coefficients
- behavioral proxies
- bridge / openness / fatigue proxies
- stage weights
- response-strategy benefit and cost weights

Assumptions must be labeled as uncalibrated.

## 7. Confidence / Uncertainty Rules

- Low evidence confidence downgrades conclusions.
- Low-trust evidence can raise review risk but must not be treated as fact.
- Duplicate evidence can become repetition signal but must not infinitely amplify risk or heat.
- Missing source URLs increase review risk.
- Rejected evidence must not contribute to analysis-ready outputs.

## 8. Human Review Gate Rules

Human review is required before:

- strategy recommendation use
- report inclusion as a conclusion
- sensitive material use
- third-party / beneficiary / parent / adult student material use
- any public-facing phrasing that could imply truth, causality, or platform coverage

## 9. Calibration Status Rules

- v0.1 is uncalibrated.
- Do not present scores as measured truth.
- Do not compare across events as if normalized.
- Do not rank public events as a real hotlist.
- Calibration can only begin after reviewed historical replay datasets and human-review comparison are available.

## 10. Module-Specific Model Cards

### ContentAggregate

- Intended use: sample heat, controversy, risk, confidence.
- Forbidden use: real hotlist, fact judgment, legal risk conclusion.
- Boundary: selected sample only.

### PeopleCluster

- Intended use: anonymous aggregate behavior proxy.
- Forbidden use: real person, account, psychological profile, persuasion target.
- Boundary: not individual diagnosis.

### InfluenceCore

- Intended use: content / narrative / official / media / KOL / meme core weight.
- Forbidden use: person ball, fact verifier, causal root proof.
- Boundary: evidence, not truth.

### EchoBox

- Intended use: sample-scoped discussion container proxy.
- Forbidden use: real community map, full social graph, target pool.
- Boundary: not full-platform coverage.

### ResponseStrategy

- Intended use: compare transparent response options for human review.
- Forbidden use: auto execution, covert manipulation, fake consensus, harassment.
- Boundary: human review required.

## 11. Anti-Overclaim Checklist

Coverage:

- No full-web claim.
- No full-platform claim.
- No full-thread claim unless explicitly reviewed for a specific package.

Truth:

- Provider output and Evidence are evidence, not truth.
- Screenshot or transcription is not automatically verified.

Causality:

- No causal proof claim.
- No causal root claim.

Prediction:

- No future prediction claim.
- Reactivation proxy is not prediction.

People:

- PeopleCluster is anonymous aggregate group / behavioral proxy.
- InfluenceCore is not a person ball.
- No personality diagnosis.
- No individual persuasion scoring.

Strategy:

- No public-opinion control.
- No auto-executed response strategy.
- Human review required.

Implementation:

- No backend runtime in v0.1.
- No frontend UI in v0.1.
- No real API.
- No real LLM.
- No crawler.

## 12. Red Flag Phrases

Avoid:

- 全网
- 全平台
- 全量
- 精准预测
- 真实心理
- 人格分析
- 心理画像
- 最容易被说服
- 说服概率
- 控评
- 洗白
- 带节奏
- 水军
- 压制
- 删帖
- 投放
- 暗中种草
- 真实热榜
- 实锤
- 官方验证
- 因果证明
- 保证平息
- 自动决策

## 13. Approved Replacement Phrases

Use:

- selected sample
- 当前样本
- 样本内结构
- 公开表达代理
- 匿名人群簇
- 透明沟通
- 复核线索
- 讨论管理风险
- 可能方向
- 人审候选
- 未校准模型

## 14. Codex Implementation Guardrails

Future Codex work must:

- start with tests
- use local fixtures only unless explicitly approved otherwise
- avoid real APIs
- avoid real LLMs
- avoid crawler or scraping behavior
- preserve all boundary flags
- include counterexample tests
- keep response strategy behind human review
- never output `auto_execute`

## 15. Validation / Counterexample Matrix

| Module | Required counterexample |
| --- | --- |
| ContentAggregate | Duplicate comments do not infinitely amplify heat. |
| PeopleCluster | Low-trust screenshot does not force massive stance change. |
| InfluenceCore | Viral meme may amplify without high credibility. |
| EchoBox | Strong echo does not imply breakout. |
| ResponseStrategy | Minors/family material without consent is blocked pending review. |
