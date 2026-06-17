# B-End Report Export Specification v1

Last updated: 2026-06-17

## Purpose

This document defines the future export structure for Sentigraph B-end public-opinion reports. It covers planned shapes for:

- Executive PDF report
- Analyst Markdown report
- Briefing deck / slide outline
- Evidence appendix package

This is a specification only. It does not implement any exporter, renderer, download action, backend job, or production report delivery workflow.

## Current Status

- Current status: docs-only specification.
- No runtime export implementation.
- No PDF renderer.
- No PowerPoint or briefing deck generator.
- No production file generation.
- No real client report delivery.
- No real LLM integration.
- No real API calls.

The current B-end sample route, `/#/reports/helldivers-psn-sample`, is a frontend-only fixed report sample based on the Helldivers selected public sample. It is not a dynamic report generator and must not be presented as a real customer report system.

## Target Users

Future B-end report exports are intended for:

- Brand / public relations teams
- MCN / creator teams
- Game studios / community operations
- IP operations teams
- Internal crisis response teams
- Agencies / consultants

## Export Formats

### A. Executive PDF

Purpose: leadership, decision makers, clients, and cross-functional stakeholders who need a polished decision-support report.

Expected characteristics:

- Client-facing layout.
- Strong boundary block.
- Executive summary first.
- Evidence coverage and confidence visible.
- Human review status visible.
- Appendices included or linked as a separate evidence appendix package.

### B. Analyst Markdown

Purpose: internal analysts, audit-friendly report drafts, version control, reviewer edits, and reproducible report work.

Expected characteristics:

- Plain text and table-friendly.
- Section keys preserved.
- Evidence IDs and methodology notes visible.
- Easy to diff and review.
- Suitable for manual editing before client-facing publication.

### C. Briefing Deck Outline

Purpose: meeting slides, client presentation, internal decision briefings, and workshop discussion.

Expected characteristics:

- Shorter than the PDF.
- Focuses on decision questions, key findings, evidence coverage, risk/opportunity, and suggested actions.
- Must still include boundary language.
- Does not include full evidence appendices by default.

### D. Evidence Appendix Package

Purpose: evidence review, audit, traceability, reviewer handoff, and internal quality control.

Expected characteristics:

- Evidence IDs, source type labels, acquisition modes, trust labels, review status, duplicate grouping, and exclusion notes.
- No full raw comment dump by default.
- No raw identifiers, secrets, cookies, or non-public personal data.
- Designed as a supplement to the PDF, Markdown, or deck export.

## Required Report Metadata

Every export-ready report object should include:

| Field | Purpose |
| --- | --- |
| `report_id` | Stable report identifier. |
| `case_id` | Source case identifier. |
| `case_title` | Human-readable case title. |
| `report_type` | Executive PDF, analyst Markdown, briefing deck, or evidence appendix. |
| `report_status` | Draft, reviewed, approved, archived, or rejected. |
| `report_version` | Version of this report content. |
| `generated_at` | Local generation timestamp. |
| `generated_by` | System/user label; do not expose private account details. |
| `data_cutoff` | Latest evidence timestamp included in the report. |
| `analysis_input_source` | `case_raw_data`, `case_evidence_items`, `mock_data_fallback`, or another explicit source label. |
| `evidence_package_id` | Evidence export package ID when relevant. |
| `sample_scope_label` | Example: selected public sample, imported evidence, mock fixture. |
| `coverage_level` | Coverage scope label, not a full-web claim. |
| `confidence_level` | Conservative confidence label. |
| `model_version` | Offline deterministic model/version label. |
| `metric_model_card_version` | Metrics model card version. |
| `llm_annotation_version` | Future annotation schema/provider version, if used. |
| `reviewer_label` | Human reviewer label if reviewed. |
| `review_status` | Not reviewed, review needed, approved, rejected, marked weak, etc. |
| `export_format` | PDF, Markdown, deck outline, appendix package. |
| `confidentiality_label` | Internal, confidential, client draft, public sample, etc. |

## Mandatory Boundary Block

Every exported report must include a visible boundary block.

Required statements:

- This report is based on available / imported evidence, not full-web coverage.
- Selected public sample does not equal official verification.
- Metrics may be mock / local fixture / heuristic / research candidate unless calibrated.
- Forecast or replay is not guaranteed future prediction.
- Opinion Ecosystem output is not causal proof.
- PeopleCluster means anonymous group cluster, not real individual.
- InfluenceCore means content / narrative / official / media / meme core, not a person.
- LLM semantic annotation, if used in the future, is not fact verification and does not directly decide final weights.

Recommended Chinese wording:

```text
本报告基于当前可用 / 已导入证据生成，不代表全网覆盖、全平台覆盖或官方验证。
样本、指标、回放和建议均用于决策辅助与人工复核，不构成因果证明、保证性预测、法律意见或自动化平台行动。
PeopleCluster 表示匿名人群簇，不代表真实个人；InfluenceCore 表示内容 / 叙事 / 官方 / 媒体 / meme 核心，不是个人节点。
```

## Core Report Sections

| Section | Purpose | Required fields | Optional fields | User-facing wording | Boundary notes | PDF | Markdown | Deck | Human review |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Cover / Report identity | Identify report, case, scope, and version. | `report_id`, `case_title`, `report_version`, `data_cutoff`, `confidentiality_label` | client label, reviewer label | "Report identity / 报告身份" | Must not imply production delivery if sample. | yes | yes | yes | yes |
| Executive summary | Summarize key findings and decisions. | summary bullets, risk level, confidence, boundary note | decision questions, next review owner | "Executive summary / 管理层摘要" | High-impact claims require review. | yes | yes | yes | yes |
| Case context | Explain event, keyword, time window, stakeholder context. | case title, event description, time window, platform/source labels | business impact, audience map | "Case context / 事件背景" | Avoid full-history reconstruction claims. | yes | yes | yes | yes |
| Evidence coverage and confidence | Show what evidence is included and how reliable it is. | evidence count, source count, trust distribution, validation status | root count, warning details, exclusion notes | "Evidence coverage / 证据覆盖" | Coverage is imported/available only. | yes | yes | yes | yes |
| Data source and provenance | Explain acquisition modes and source provenance. | acquisition mode distribution, provenance distribution, verification status | evidence package ID, source policy notes | "Source and provenance / 来源与出处" | Selected sample is not official verification. | yes | yes | optional | yes |
| Key findings | Present main analytical observations. | findings, evidence basis, confidence, uncertainty | supporting excerpts, charts | "Key findings / 核心发现" | Findings are analysis outputs, not absolute truth. | yes | yes | yes | yes |
| Opinion Ecosystem summary | Summarize InfluenceCore, EchoBox, clusters, camps, and tempo. | ecosystem metrics, component summaries, boundary copy | visual snapshot, model card link | "Opinion Ecosystem / 舆论生态摘要" | Not calibrated simulation or causal proof unless validated. | yes | yes | yes | yes |
| Timeline / historical replay | Show event stages and response timing. | timeline stages, date labels, observed shifts | scenario notes, replay screenshots | "Timeline / 历史回放" | Not full historical reconstruction. | yes | yes | yes | yes |
| Risk taxonomy | Distinguish base, monitor, forecast, and report risk. | `base_analysis_risk`, `monitor_current_risk`, `forecast_risk`, `report_risk` | scoring notes, confidence | "Risk taxonomy / 风险分类" | Monitor/forecast do not rewrite report unless regenerated. | yes | yes | yes | yes |
| Response tempo analysis | Describe timing and response-window implications. | current tempo, delayed-response risk, fatigue/cooling state | recommended response window | "Response tempo / 响应节奏" | Tempo is decision support, not guaranteed effect. | yes | yes | yes | yes |
| Risk and opportunity cards | Translate findings into actionable risk/opportunity cards. | card title, impact, evidence basis, confidence, caveat | owner, time horizon | "Risk and opportunity / 风险与机会" | Must avoid manipulation or individual targeting. | yes | yes | yes | yes |
| Suggested actions | Provide safe response options and caveats. | action type, target audience, rationale, uncertainty, review requirement | rollout checklist, communication owner | "Suggested actions / 建议动作" | Not legal advice or guaranteed PR outcome. | yes | yes | yes | yes |
| Uncertainty and limitations | Make limitations explicit. | limitations, sample scope, model caveats, unresolved questions | reviewer questions | "Limitations / 不确定性" | Mandatory for every client-facing export. | yes | yes | yes | yes |
| Human review / audit status | Show review decisions and unresolved review needs. | reviewer label, reviewed at, review status, notes | change log | "Human review / 人工复核" | AI review is future only unless implemented and labeled. | yes | yes | optional | yes |
| Evidence appendix | Provide traceable evidence references. | evidence IDs, source type, acquisition mode, trust/review status | safe excerpts, redacted URL references | "Evidence appendix / 证据附录" | No raw dump by default; no private data. | yes | yes | no | yes |
| Methodology appendix | Explain metrics, model cards, and generation method. | model version, metric card, analysis method, boundary block | formula notes, validation notes | "Methodology / 方法说明" | Research candidates must be labeled. | yes | yes | optional | yes |
| Export metadata | Preserve reproducibility. | export format, template version, generated at, data cutoff | deterministic build metadata | "Export metadata / 导出元数据" | Must not expose secrets or private runtime paths. | yes | yes | no | no |

## Evidence Coverage Section

Required fields:

- `evidence_count`
- `source_count`
- `comment_count`, if available
- `root_count` / InfluenceCore candidates, if available
- `validation_status`
- `errors_count`
- `warnings_count`
- trust distribution
- verification distribution
- review status distribution
- acquisition mode distribution
- duplicate count / dedup note
- coverage note
- excluded evidence note
- sample limitation

Example for the current Helldivers selected public sample:

| Field | Sample value |
| --- | --- |
| evidence count | 34 |
| source count | 7 |
| comment samples | 28 |
| roots / InfluenceCore candidates | 6 |
| validation | warn |
| errors | 0 |
| warnings | 2 |

These are sample values only. They are not hardcoded report requirements and do not imply full-web, full-platform, full-thread, official, or production coverage.

## Risk Taxonomy Section

Reports must distinguish:

- `base_analysis_risk`
- `monitor_current_risk`
- `forecast_risk`
- `report_risk`

Definitions:

- Base analysis risk comes from Analysis Result / case summary.
- Monitor current risk comes from the latest local/offline monitoring check.
- Forecast risk comes from deterministic/local forecast.
- Report risk reflects the generated report snapshot.

Monitor or forecast results do not automatically rewrite the report unless a future regeneration flow exists and the report metadata records the new snapshot.

## Opinion Ecosystem Section

Required content:

- InfluenceCore summary
- EchoBox summary
- PeopleCluster summary
- Camp Dynamics
- Response Tempo
- Reputation Memory
- Deconstruction / cooling window, if present
- Bridge path / bridge cluster, if present

Boundary:

Do not present these as calibrated real simulation unless separately validated. The current sandbox and sample mapping are local/demo evidence interpretation tools, not official verification, causal proof, or real-world action execution.

## Timeline / Replay Section

Timeline exports should separate historical replay from forward simulation placeholders.

For current Helldivers sample documentation, the visible stages are:

- T0 announcement
- T1 community backlash
- T2 rollback / not moving forward
- T3 media / third-party explanation
- T4 community deconstruction
- T5 fatigue / cooling
- T6 reputation memory

Boundary:

- Historical replay is not full historical reconstruction.
- Forward simulation is planned, not active, unless implemented later.
- Scenario preview must not be described as a guaranteed prediction.

## Suggested Actions Section

Action recommendation format:

| Field | Meaning |
| --- | --- |
| `action_id` | Stable action identifier. |
| `action_type` | Transparent clarification, FAQ, third-party explanation, etc. |
| `target_audience` | Stakeholder group, not individual targeting. |
| `rationale` | Why this action is suggested. |
| `evidence_basis` | Evidence IDs or summarized evidence support. |
| `expected_effect_direction` | Expected direction, not guaranteed outcome. |
| `uncertainty` | Confidence and caveat. |
| `risk_of_backfire` | Possible negative reaction. |
| `required_review` | Legal, comms, policy, or human review requirement. |
| `caveat` | Boundary note. |

Safe action examples:

- Transparent clarification
- FAQ / long explanation
- Third-party explanation
- Community language translation
- Acknowledgement of communication gap
- Evidence correction
- Follow-up monitoring
- Avoid over-response

Boundary:

Suggested actions are report-format examples or decision support. They are not guaranteed PR outcomes, legal advice, automated moderation instructions, or manipulation instructions. Do not include covert seeding, astroturfing, bot campaigns, harassment, suppression, or individual persuasion targeting.

## Human Review and Audit

Human review is required for:

- Executive summary
- High-impact claims
- Suggested actions
- Risk severity escalation
- Source credibility claims
- Evidence exclusion
- Misinformation / harassment / doxxing flags
- Client-facing excerpts
- LLM semantic annotation, if a future provider is used

Audit fields:

- `reviewer_label`
- `reviewed_at`
- `review_status`
- `decision_notes`
- `evidence_exclusion_notes`
- `uncertainty_notes`
- `report_change_log`

## Export Safety Rules

Do not include:

- raw author identifiers
- raw display names
- profile links
- cookies
- tokens
- secret keys
- private messages
- unredacted secrets
- non-public personal data
- full raw comment dump by default

Allow:

- anonymized excerpts
- aggregated statistics
- evidence IDs
- source type labels
- redacted URL references only if needed and safe
- public source references only after policy review

## Versioning and Reproducibility

Required reproducibility fields:

- `report_version`
- `data_cutoff`
- `evidence_snapshot_id`
- `metric_model_card_version`
- `annotation_schema_version`
- `prompt_template_version`, if future LLM is used
- `export_template_version`
- `generated_at`
- deterministic build metadata
- changelog

The export should be reproducible from a stable evidence snapshot and documented model/template versions. Future LLM usage must record provider, schema, prompt-template version, and review state without exposing prompts that contain secrets or private data.

## Future Implementation Phases

| Phase | Scope | Gate |
| --- | --- | --- |
| Phase A | Docs-only export spec. | Current document reviewed. |
| Phase B | Static frontend report sample alignment. | Sample copy and boundaries approved. |
| Phase C | Markdown export draft from local fixed sample. | Evidence coverage/review/privacy wording confirmed. |
| Phase D | PDF export prototype from local fixed sample. | PDF template and redaction rules approved. |
| Phase E | Briefing deck outline. | Deck copy and client-facing claims reviewed. |
| Phase F | Backend report export job with audit metadata. | Access control, export logs, snapshot IDs, and retention reviewed. |
| Phase G | Production export with access control. | Legal, privacy, security, and client-delivery gates complete. |

No real export should be used for client delivery until evidence coverage, human review, privacy, legal wording, and access-control gates are confirmed.
