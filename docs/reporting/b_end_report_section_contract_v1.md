# B-End Report Section Contract v1

Last updated: 2026-06-17

## Purpose

This document defines the report-section contract for future B-end Sentigraph exports. It is a docs-only handoff for future PDF, Markdown, briefing deck, and evidence appendix work.

It does not implement export generation, file downloads, backend jobs, PDF rendering, PowerPoint generation, Markdown generation, real LLM integration, or client report delivery.

## Section Matrix

| section_key | display_name_cn | display_name_en | required | appears_in_pdf | appears_in_markdown | appears_in_deck | data_inputs | review_required | boundary_required | current_status | notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `cover` | 封面 / 报告身份 | Cover / Report identity | yes | yes | yes | yes | report metadata, case metadata | yes | yes | planned | Must show sample/client/draft status. |
| `executive_summary` | 管理层摘要 | Executive Summary | yes | yes | yes | yes | analysis result, key findings, risk summary | yes | yes | planned | High-impact claims must be reviewed. |
| `case_context` | 事件背景 | Case Context | yes | yes | yes | yes | case title, keyword, time window, source labels | yes | yes | planned | Do not imply full historical reconstruction. |
| `evidence_coverage` | 证据覆盖与置信度 | Evidence Coverage | yes | yes | yes | yes | evidence summary, validation report, trust/dedup/review summaries | yes | yes | planned | Must state available/imported evidence only. |
| `source_provenance` | 来源与出处 | Source and Provenance | yes | yes | yes | optional | provenance, acquisition mode, verification status | yes | yes | planned | Selected public sample is not official verification. |
| `risk_taxonomy` | 风险分类 | Risk Taxonomy | yes | yes | yes | yes | base risk, monitor risk, forecast risk, report risk | yes | yes | planned | Risk types must not be merged. |
| `key_findings` | 核心发现 | Key Findings | yes | yes | yes | yes | analysis observations, evidence basis | yes | yes | planned | Findings are decision support, not absolute truth. |
| `opinion_ecosystem_summary` | 舆论生态摘要 | Opinion Ecosystem Summary | yes | yes | yes | yes | InfluenceCore, EchoBox, PeopleCluster, Camp Dynamics, Response Tempo | yes | yes | planned | Not causal proof or calibrated simulation unless validated. |
| `historical_replay` | 历史回放 | Historical Replay | yes | yes | yes | yes | timeline stages, event tokens, scenario state | yes | yes | planned | Not full historical reconstruction. |
| `response_tempo` | 响应节奏 | Response Tempo | yes | yes | yes | yes | response timing, escalation/cooling notes | yes | yes | planned | Not guaranteed effect prediction. |
| `risk_opportunity` | 风险与机会 | Risk and Opportunity | yes | yes | yes | yes | risk cards, opportunity cards, uncertainty | yes | yes | planned | Avoid manipulation or individual targeting. |
| `suggested_actions` | 建议动作 | Suggested Actions | yes | yes | yes | yes | action cards, rationale, evidence basis | yes | yes | planned | Decision support only; no guaranteed outcome. |
| `uncertainty_limitations` | 不确定性与限制 | Uncertainty and Limitations | yes | yes | yes | yes | boundary block, sample limitation, model caveats | yes | yes | planned | Mandatory for client-facing exports. |
| `human_review_audit` | 人工复核与审计 | Human Review and Audit | yes | yes | yes | optional | review queue, audit timeline, exclusion notes | yes | yes | planned | AI authenticity review is not active. |
| `evidence_appendix` | 证据附录 | Evidence Appendix | yes | yes | yes | no | safe evidence IDs, excerpts, provenance, review status | yes | yes | planned | No raw dump by default. |
| `methodology_appendix` | 方法说明 | Methodology Appendix | yes | yes | yes | optional | model card, metric versions, template versions | yes | yes | planned | Research candidates must be labeled. |
| `export_metadata` | 导出元数据 | Export Metadata | yes | yes | yes | no | export format, generated at, data cutoff, template version | no | yes | planned | Must not expose secrets or private runtime paths. |

## Minimal JSON-Like Report Contract

This shape is illustrative only. It is not a backend schema and is not implemented.

```json
{
  "report_metadata": {
    "report_id": "report_demo_001",
    "case_id": "case_demo_001",
    "case_title": "Helldivers PSN selected public sample",
    "report_type": "executive_pdf",
    "report_status": "draft",
    "report_version": "v1",
    "generated_at": "local-demo-time",
    "generated_by": "sentigraph_local_demo",
    "data_cutoff": "sample_defined",
    "analysis_input_source": "case_evidence_items",
    "sample_scope_label": "selected_public_sample",
    "coverage_level": "selected_public_sample_only",
    "confidence_level": "limited_sample",
    "metric_model_card_version": "metrics_model_card_v1",
    "export_format": "pdf",
    "confidentiality_label": "local_demo_sample"
  },
  "case_context": {},
  "evidence_coverage": {},
  "risk_taxonomy": {},
  "opinion_ecosystem": {},
  "historical_replay": {},
  "response_tempo": {},
  "risk_opportunity": [],
  "suggested_actions": [],
  "limitations": [],
  "human_review": {},
  "appendices": {}
}
```

## Sample Helldivers Report Mapping

The current Helldivers report sample should map to the contract as a selected public sample:

| Contract field | Example value |
| --- | --- |
| `sample_scope_label` | selected public sample |
| `evidence_count` | 34 |
| `source_count` | 7 |
| `comment_count` | 28 comment samples |
| `root_count` | 6 roots / InfluenceCore candidates |
| `validation_status` | warn |
| `coverage_level` | selected public sample only |
| `errors_count` | 0 |
| `warnings_count` | 2 |
| `official_verification` | no |
| `causal_proof` | no |
| `full_web_coverage` | no |
| `full_platform_coverage` | no |

These values are examples for the current local demo package. They are not complete, not production, not full-web, not full-platform, not full-thread, not official verification, and not causal proof.

## Export Format Matrix

| Format | Primary use | Included sections | Excluded by default | Current status |
| --- | --- | --- | --- | --- |
| PDF | Full client-facing report. | Cover, executive summary, context, evidence coverage, key findings, ecosystem, timeline, risk/opportunity, suggested actions, limitations, review/audit, appendices, metadata. | Full raw comment dump, raw identifiers, private data. | planned only |
| Markdown | Analyst-editable draft. | All sections, with stronger audit and methodology detail. | Production styling, private runtime details, secrets. | planned only |
| Deck | Meeting briefing outline. | Cover, summary, context, evidence coverage, key findings, ecosystem snapshot, risk/opportunity, suggested actions, limitations. | Full evidence appendix and methodology detail. | planned only |
| Appendix package | Evidence and audit supplement. | Evidence IDs, safe excerpts, source labels, provenance, trust/dedup/review status, exclusion notes, methodology metadata. | Raw identifiers, secret values, private messages, full raw dumps by default. | planned only |

## Copy Rules

Allowed wording:

- 样本显示
- 当前证据包显示
- 本地演示报告样例
- selected public sample
- evidence coverage limitation
- confidence / uncertainty
- response tempo
- risk/opportunity
- suggested actions sample
- imported / available evidence
- human review required

Avoid wording:

- 全网证明
- 官方确认
- 因果证明
- 自动最佳策略
- 保证降温
- 控评
- 洗白
- 带节奏
- 操控
- 精准影响用户
- 最容易被说服的人
- full-web truth
- full-platform capture
- official verification
- causal proof
- guaranteed forecast
- real-time platform action

## Boundary Copy Library

Use these lines in exports when relevant:

```text
本报告基于当前可用 / 已导入证据，不代表全网覆盖、全平台覆盖或官方验证。
当前 Helldivers 样例是 selected public sample，不代表完整事件全量数据。
Opinion Ecosystem 输出用于结构化理解，不构成因果证明。
PeopleCluster 表示匿名人群簇，不代表真实个人。
InfluenceCore 表示内容 / 叙事 / 官方 / 媒体 / meme 核心，不是个人节点。
建议动作仅用于决策辅助，需要人工、法务、政策或客户侧复核。
```

## Safety Notes For Future Implementers

- Do not add export runtime code from this document alone.
- Do not add backend APIs without a separate implementation task and review.
- Do not add PDF, Markdown, deck, or download behavior until privacy, evidence, and review gates are agreed.
- Do not treat vendor-attested, manually entered, screenshot, or selected sample evidence as official verification.
- Do not include raw identity fields, profile links, cookies, tokens, secret keys, private messages, or non-public personal data.
- Do not use suggested actions for covert persuasion, suppression, harassment, astroturfing, bot campaigns, or individual targeting.
