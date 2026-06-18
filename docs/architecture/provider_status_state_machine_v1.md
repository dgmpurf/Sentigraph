# Provider Status State Machine v1

Status: architecture contract draft

Scope: evidence provider job status, safety status, and Sentigraph UI wording

This document defines a provider status state machine for future provider integration. It is docs-only. It does not add a job runner, backend API, provider API, collector integration, or frontend route.

## 1. Purpose

Sentigraph needs a clear state model for external evidence providers without running provider acquisition inside Sentigraph core.

The state machine helps:

- describe provider-side work,
- keep unsafe or incomplete packages out of analysis,
- show users that evidence packages are samples with coverage limits,
- avoid implying full-web capture or official verification,
- preserve human review and audit gates.

## 2. Provider Job States

| State | Meaning | Provider responsibility | Sentigraph UI wording | Can Sentigraph import? | Human review required? | Allowed next states |
| --- | --- | --- | --- | --- | --- | --- |
| `draft` | Request is being prepared but not issued. | None or draft validation only. | `分析请求草稿，尚未发送给外部 Provider。` | no | no | `queued`, `canceled`, `expired` |
| `queued` | Request is waiting for provider pickup. | Observe queue and accept or reject. | `等待外部 Provider 生成证据包。` | no | no | `accepted`, `canceled`, `expired` |
| `accepted` | Provider accepted the request. | Assign provider job ID and prepare planning. | `Provider 已接受请求，正在准备采样计划。` | no | no | `planning`, `canceled`, `expired` |
| `planning` | Provider is planning sample scope and source strategy. | Plan platforms, time range, safety budget, and skip rules. | `Provider 正在规划 selected public sample。` | no | no | `safety_check`, `needs_manual_snapshot`, `blocked_by_safety_gate`, `canceled` |
| `safety_check` | Provider is checking safety and feasibility. | Enforce source rules, rate limits, platform gates, and privacy policy. | `Provider 正在执行安全门控检查。` | no | no | `running_safe`, `needs_manual_snapshot`, `blocked_by_safety_gate`, `cooldown`, `canceled` |
| `blocked_by_safety_gate` | Provider refused or paused because the source is unsafe or disallowed. | Record block reason and skip unsafe source. | `安全门控暂停：Provider 未执行采样。` | no | yes, if user wants to revise scope | `planning`, `canceled`, `expired` |
| `needs_manual_snapshot` | Provider needs a lawful manual snapshot or user-provided export. | Request manual package or snapshot outside Sentigraph core. | `需要人工提供本地 snapshot，Sentigraph 不运行采集。` | no | yes | `planning`, `package_generated`, `canceled`, `expired` |
| `running_safe` | Provider is running an allowed acquisition or local snapshot process outside Sentigraph. | Keep within safety budget and log collection events. | `Provider 正在安全预算内生成证据包。` | no | no | `cooldown`, `partial_success`, `package_generated`, `blocked_by_safety_gate`, `canceled` |
| `cooldown` | Provider paused to respect safety/rate/health gates. | Wait, reduce load, or stop safely. | `Provider 处于 cooldown，未继续采样。` | no | maybe | `running_safe`, `partial_success`, `blocked_by_safety_gate`, `canceled`, `expired` |
| `partial_success` | Provider collected some evidence but did not meet target coverage. | Generate partial package and coverage note if safe. | `Provider 生成了部分样本，coverage 有限制。` | maybe, after validation | yes | `package_generated`, `validation_running`, `canceled` |
| `package_generated` | Provider wrote package files. | Write manifest, evidence files, coverage note, collection log, and validation report if available. | `证据包已生成，等待校验。` | no | no | `validation_running`, `validation_failed`, `expired` |
| `validation_running` | Structural validation is running. | Run package validator or provide validation output. | `正在校验证据包结构和安全边界。` | no | no | `validation_warn`, `validation_failed`, `package_ready` |
| `validation_warn` | Validation passed with warnings. | Record warnings and coverage limits. | `校验通过但有 warning，需要人工确认。` | yes, if policy allows | yes | `package_ready`, `validation_failed`, `canceled` |
| `validation_failed` | Package failed validation. | Preserve failure report and do not ask Sentigraph to import. | `证据包校验失败，禁止导入。` | no | yes, for troubleshooting | `planning`, `package_generated`, `canceled`, `expired` |
| `package_ready` | Package passed validation and is ready for Sentigraph decision. | Refresh package index and expose safe metadata. | `证据包已就绪，可进入 Sentigraph 校验/草稿流程。` | yes | maybe, based on trust and coverage | `expired`, `canceled` |
| `canceled` | Job was canceled by user, Sentigraph, or provider. | Stop safely and record cancellation reason. | `Provider 任务已取消。` | no | no | terminal |
| `expired` | Job result or package is too stale for intended use. | Mark stale and require new request if needed. | `Provider 结果已过期，需要重新确认样本范围。` | no | yes, if reuse is requested | terminal or `planning` by new request |

## 3. Safety States

Safety status is separate from job status. A job can be `planning` with safety `medium`, or `package_ready` with safety `safe`.

| Safety state | Meaning | Sentigraph behavior |
| --- | --- | --- |
| `safe` | Provider reports the current operation stayed within allowed policy. | Package may continue through validation and review. |
| `medium` | Provider reports caution, reduced scope, warnings, or uncertain coverage. | Show warning and require review before strong claims. |
| `hold` | Provider paused before execution due to unresolved safety or policy question. | Do not import; show hold reason. |
| `cooldown` | Provider paused for rate, host, profile, or operational health. | Do not imply live failure; show cooldown status. |
| `blocked` | Provider blocked the job due to policy, privacy, source, or platform boundary. | Do not import; show block reason and allow request revision only. |

## 4. Sentigraph Import Rules

Sentigraph can import only when all are true:

- package files are present,
- validation is `passed` or `warn` under current policy,
- privacy checks pass,
- package coverage is displayed honestly,
- trust and review metadata can be assigned,
- rejected privacy or coverage states are absent.

Sentigraph must not import when:

- provider state is `draft`, `queued`, `accepted`, `planning`, `safety_check`, `blocked_by_safety_gate`, `needs_manual_snapshot`, `running_safe`, or `cooldown`,
- validation failed,
- privacy removal failed,
- package coverage would be misleading for the intended demo or analysis claim,
- source identity or provenance is too unclear for the requested use.

Warnings are allowed only if visible:

- validation warnings,
- coverage limitations,
- selected public sample boundary,
- missing source or timestamp warnings,
- provider attestation limitations,
- review-needed state.

## 5. Review Rules

Human review is required or recommended when:

- state is `validation_warn`,
- package is `partial_success`,
- safety state is `medium`,
- coverage is selected sample only,
- package contains vendor-attested evidence,
- package contains manual snapshot evidence,
- source URL is missing,
- timestamp is missing,
- duplicate groups are high,
- evidence is screenshot/transcription based,
- privacy or author identifier removal needs confirmation.

Human review does not mean official verification. It records a human decision about whether evidence may be used in the current Sentigraph analysis context.

## 6. UI Wording Examples

Use conservative wording:

- `等待外部 Provider 生成证据包。`
- `安全门控暂停：Provider 未执行采样。`
- `证据包已生成，等待校验。`
- `校验通过但有 warning，需要人工确认。`
- `隐私或 coverage 问题，禁止导入。`
- `当前覆盖范围仅代表已导入/可用证据，不代表全平台全量覆盖。`
- `Provider 输出是 evidence，不是官方事实结论。`
- `该包为 selected public sample，需要结合来源和人工复核判断。`

Avoid wording that implies:

- crawling,
- full-web,
- real-time full-platform,
- official verified,
- hidden API,
- bypass,
- live scraping,
- automatic truth verification.

## 7. State Transition Notes

Recommended transition flow:

```text
draft
-> queued
-> accepted
-> planning
-> safety_check
-> running_safe
-> package_generated
-> validation_running
-> validation_warn
-> package_ready
```

Alternative safe flows:

```text
planning -> needs_manual_snapshot -> package_generated
safety_check -> blocked_by_safety_gate
running_safe -> cooldown -> partial_success -> package_generated
validation_running -> validation_failed
queued -> canceled
package_ready -> expired
```

Terminal states:

- `canceled`,
- `expired`.

Recoverable states:

- `blocked_by_safety_gate` may return to `planning` only after scope revision.
- `validation_failed` may return to `package_generated` only after provider produces a corrected package.
- `cooldown` may return to `running_safe` only if provider safety gates permit.

## 8. Future Implementation Phases

Phase 1: file-based status.

- Provider writes local job result JSON.
- Sentigraph reads package index and status.
- No provider runtime is executed by Sentigraph.

Phase 2: local bridge UI.

- Sentigraph displays provider package status and coverage notes.
- User can validate and create case drafts from local packages.

Phase 3: governed provider API.

- Optional HTTP provider endpoints may be introduced after security review.
- Provider still owns acquisition and safety gates.
- Sentigraph still consumes normalized evidence artifacts.

Phase 4: streaming evidence.

- Future Evidence Stream v1 may support chunked or streaming evidence.
- Trust, provenance, dedup, review, coverage, and audit remain required.

## 9. Non-Implementation Statement

This state machine does not implement:

- frontend UI changes,
- backend APIs,
- provider APIs,
- collector jobs,
- live collection,
- URL fetching,
- scraping,
- browser automation,
- account/session handling,
- hidden platform APIs,
- or automated official verification.

