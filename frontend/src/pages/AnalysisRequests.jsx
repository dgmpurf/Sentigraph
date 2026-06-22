import {
  Alert,
  App as AntApp,
  Button,
  Card,
  Checkbox,
  Col,
  Descriptions,
  Empty,
  Form,
  Input,
  InputNumber,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tag,
  Typography,
} from 'antd'
import { ClipboardCopy, FileJson, RefreshCw, ShieldCheck, XCircle } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import {
  cancelAnalysisRequest,
  createAnalysisRequestAnalysisReadyPromotionGate,
  createAnalysisRequestAnalysisResultBoundaryGate,
  createAnalysisRequestManualAnalysisExecution,
  createAnalysisRequestManualAnalysisTrigger,
  createAnalysisRequestReportGenerationGate,
  createAnalysisRequestFinalSummaryReport,
  createAnalysisRequestFinalSummaryReportExportArtifact,
  createAnalysisRequestFinalSummaryReportExportGate,
  createAnalysisRequestFinalSummaryReportReviewGate,
  createAnalysisRequestReportExportDownloadPackageGate,
  createAnalysisRequestReportExportDownloadPackageArtifact,
  createAnalysisRequestReportExportPublicAccessExternalDeliveryGate,
  createAnalysisRequestSummaryReportCandidate,
  createAnalysisRequest,
  createAnalysisRequestDedupGroupReviewAction,
  createAnalysisRequestCaseDraft,
  createAnalysisRequestDedupPreview,
  createAnalysisRequestImportJob,
  createAnalysisRequestImportPlan,
  createAnalysisRequestImportPreview,
  createAnalysisRequestReviewDecision,
  createAnalysisRequestExecutionPreflight,
  createAnalysisRequestRealPackageRowPreview,
  createAnalysisRequestReviewOnlyCase,
  createAnalysisRequestReviewQueueCompletionGate,
  createAnalysisRequestReviewQueueItemAction,
  createAnalysisRequestReviewQueueInitialization,
  createAnalysisRequestRowReaderDryRun,
  createAnalysisRequestStagingImport,
  getAnalysisRequestReviewQueueItems,
  getAnalysisRequestStagingImportCandidates,
  getAnalysisRequest,
  getAnalysisRequestCaseDraft,
  getAnalysisRequestConfig,
  getAnalysisRequestImportPlan,
  getAnalysisRequestImportPreview,
  listAnalysisRequestExecutionPreflights,
  listAnalysisRequestAnalysisReadyPromotionGates,
  listAnalysisRequestAnalysisResultBoundaryGateAudits,
  listAnalysisRequestAnalysisResultBoundaryGates,
  listAnalysisRequestDedupGroupReviewAudits,
  listAnalysisRequestDedupPreviews,
  listAnalysisRequestImportJobs,
  listAnalysisRequestManualAnalysisExecutionAudits,
  listAnalysisRequestManualAnalysisExecutions,
  listAnalysisRequestManualAnalysisResultCandidates,
  listAnalysisRequestManualAnalysisTriggerAudits,
  listAnalysisRequestManualAnalysisTriggers,
  listAnalysisRequestReportGenerationGateAudits,
  listAnalysisRequestReportGenerationGates,
  listAnalysisRequestFinalSummaryReportAudits,
  listAnalysisRequestFinalSummaryReportExportArtifactAudits,
  listAnalysisRequestFinalSummaryReportExportArtifacts,
  listAnalysisRequestFinalSummaryReportExportGateAudits,
  listAnalysisRequestFinalSummaryReportExportGates,
  listAnalysisRequestFinalSummaryReports,
  listAnalysisRequestFinalSummaryReportReviewGateAudits,
  listAnalysisRequestFinalSummaryReportReviewGates,
  listAnalysisRequestReportExportDownloadPackageGateAudits,
  listAnalysisRequestReportExportDownloadPackageGates,
  listAnalysisRequestReportExportDownloadPackageArtifactAudits,
  listAnalysisRequestReportExportDownloadPackageArtifacts,
  listAnalysisRequestReportExportPublicAccessExternalDeliveryGateAudits,
  listAnalysisRequestReportExportPublicAccessExternalDeliveryGates,
  listAnalysisRequestSummaryReportCandidateAudits,
  listAnalysisRequestSummaryReportCandidates,
  listAnalysisRequestRealPackageRowPreviews,
  listAnalysisRequestReviewOnlyCases,
  listAnalysisRequestReviewQueueActionAudits,
  listAnalysisRequestReviewQueueCompletionGates,
  listAnalysisRequestReviewQueueInitializations,
  listAnalysisRequestRowReaderDryRuns,
  listAnalysisRequestReviewDecisions,
  listAnalysisRequestPromotionDecisionAudits,
  listAnalysisRequestStagingImports,
  listAnalysisRequests,
} from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography
const { TextArea } = Input

const STATUS_COLOR = {
  draft: 'default',
  queued: 'blue',
  accepted: 'blue',
  planning: 'geekblue',
  safety_check: 'purple',
  blocked_by_safety_gate: 'red',
  needs_manual_snapshot: 'gold',
  running_safe: 'cyan',
  cooldown: 'orange',
  partial_success: 'gold',
  package_generated: 'blue',
  validation_running: 'geekblue',
  validation_warn: 'gold',
  validation_failed: 'red',
  package_ready: 'green',
  canceled: 'default',
  expired: 'default',
}

const SAFETY_COLOR = {
  safe: 'green',
  medium: 'gold',
  hold: 'orange',
  cooldown: 'orange',
  blocked: 'red',
}

const DEFAULT_FORM_VALUES = {
  title: 'Dong Lu / Sun Jihai selected public sample request',
  description: 'Create a local file-based analysis request. Provider execution stays outside Sentigraph.',
  keywords: ['董路', '孙继海', '青训'],
  negative_keywords: ['广告', '无关'],
  language: ['zh-CN'],
  event_type: 'public_opinion_demo',
  sensitive_flags: [],
  platforms: ['weibo', 'bilibili', 'tieba'],
  target_comment_count: 500,
  target_source_count: 30,
  max_runtime_minutes: 60,
  sample_strategy: 'stratified_public_sample',
  allow_manual_snapshot: true,
  allow_official_api: true,
  allow_vendor_api: true,
  allow_live_collection: false,
  allow_saved_profile: false,
  minor_sensitive_mode: true,
}

const BOUNDARY_TAGS = [
  'local file request only',
  'Evidence Package input',
  'provider execution outside Sentigraph',
  'no collector job',
  'no URL fetch',
  'no real API',
  'no real LLM',
  'not full-web coverage',
  'needs review',
]

const REVIEW_DECISION_OPTIONS = [
  { value: 'approve_import', label: 'approve future manual import' },
  { value: 'reject_import', label: 'reject import' },
  { value: 'request_more_source', label: 'request more source' },
  { value: 'mark_limited_sample', label: 'mark limited sample' },
  { value: 'hold_for_privacy_review', label: 'privacy hold' },
]

const TARGET_CASE_MODE_OPTIONS = [
  { value: 'new_review_case', label: 'new_review_case' },
  { value: 'existing_case', label: 'existing_case' },
  { value: 'reject_no_case', label: 'reject_no_case' },
]

const IMPORT_JOB_TARGET_CASE_OPTIONS = [
  { value: 'new_review_case', label: 'new_review_case' },
  { value: 'existing_case', label: 'existing_case' },
]

const ROW_READER_FIXTURE_OPTIONS = [
  { value: 'safe_evidence_items', label: 'safe fixture / 安全合成样本' },
  { value: 'mixed_evidence_items', label: 'mixed privacy fixture / 隔离演练样本' },
]

const REVIEW_CHECKLIST_ITEMS = [
  { value: 'coverage_reviewed', label: 'coverage reviewed' },
  { value: 'validation_reviewed', label: 'validation reviewed' },
  { value: 'privacy_reviewed', label: 'privacy reviewed' },
  { value: 'no_raw_author_identifiers', label: 'no raw author identifiers' },
  { value: 'not_full_web_acknowledged', label: 'not full-web acknowledged' },
  { value: 'not_full_platform_acknowledged', label: 'not full-platform acknowledged' },
  { value: 'not_full_thread_acknowledged', label: 'not full-thread acknowledged' },
  { value: 'review_needed_default_acknowledged', label: 'review_needed default acknowledged' },
  { value: 'trust_label_default_acknowledged', label: 'medium_low trust default acknowledged' },
  { value: 'dedup_required_acknowledged', label: 'dedup required acknowledged' },
  { value: 'no_auto_analysis_acknowledged', label: 'no auto analysis acknowledged' },
  { value: 'no_auto_report_acknowledged', label: 'no auto report acknowledged' },
]

const REVIEW_CHECKLIST_KEYS = REVIEW_CHECKLIST_ITEMS.map((item) => item.value)

const DEDUP_GROUP_STATUS_COLOR = {
  review_needed: 'gold',
  confirmed: 'green',
  split: 'purple',
  representative_changed: 'blue',
  marked_weak: 'orange',
  rejected: 'red',
  needs_more_source: 'volcano',
  privacy_hold: 'magenta',
}

const DEDUP_GROUP_ACTION_LABELS = {
  confirm_group: 'Confirm group',
  split_group: 'Split group',
  change_representative: 'Change representative',
  mark_group_weak: 'Mark group weak',
  reject_group: 'Reject group',
  request_more_source: 'Request more source',
  hold_group_for_privacy: 'Hold for privacy',
  reset_group_review: 'Reset group review',
}

const DEDUP_GROUP_ACTIONS = [
  'confirm_group',
  'split_group',
  'change_representative',
  'mark_group_weak',
  'reject_group',
  'request_more_source',
  'hold_group_for_privacy',
  'reset_group_review',
]

const PROMOTION_DECISION_OPTIONS = [
  { value: 'approve_for_future_manual_analysis_trigger', label: 'Approve for future manual trigger' },
  { value: 'hold_for_more_review', label: 'Hold for more review' },
  { value: 'reject_promotion', label: 'Reject promotion' },
]

const PROMOTION_GATE_STATUS_COLOR = {
  eligible_for_future_manual_analysis_trigger: 'green',
  held_by_human: 'gold',
  rejected_by_human: 'red',
  blocked: 'red',
  privacy_hold: 'magenta',
}

const MANUAL_TRIGGER_DECISION_OPTIONS = [
  { value: 'trigger_analysis', label: 'trigger_analysis / record trigger only' },
  { value: 'hold', label: 'hold' },
  { value: 'cancel', label: 'cancel' },
]

const MANUAL_TRIGGER_STATUS_COLOR = {
  trigger_recorded_ready_for_future_analysis_runtime: 'green',
  held: 'gold',
  cancelled: 'default',
  incomplete: 'orange',
  blocked: 'red',
  privacy_hold: 'magenta',
}

const FINAL_SUMMARY_REVIEW_DECISION_OPTIONS = [
  { value: 'approve_for_future_final_runtime', label: 'approve_for_future_final_runtime' },
  { value: 'request_revision', label: 'request_revision' },
  { value: 'block', label: 'block' },
  { value: 'privacy_hold', label: 'privacy_hold' },
]

const FINAL_SUMMARY_REVIEW_STATUS_COLOR = {
  ready_for_future_final_summary_report_runtime: 'green',
  needs_revision: 'gold',
  blocked: 'red',
  privacy_hold: 'magenta',
}

const FINAL_SUMMARY_EXPORT_DECISION_OPTIONS = [
  { value: 'approve_for_future_export_runtime', label: 'approve_for_future_export_runtime' },
  { value: 'request_revision', label: 'request_revision' },
  { value: 'block', label: 'block' },
  { value: 'privacy_hold', label: 'privacy_hold' },
]

const FINAL_SUMMARY_EXPORT_STATUS_COLOR = {
  ready_for_future_export_runtime: 'green',
  needs_revision: 'gold',
  blocked: 'red',
  privacy_hold: 'magenta',
}

const FINAL_SUMMARY_EXPORT_ARTIFACT_TYPE_OPTIONS = [
  { value: 'analyst_markdown', label: 'analyst_markdown / local .md' },
  { value: 'briefing_deck_outline', label: 'briefing_deck_outline / JSON outline only' },
  { value: 'evidence_appendix_package', label: 'evidence_appendix_package / JSON bundle' },
  { value: 'executive_pdf', label: 'executive_pdf / unsupported until safe renderer exists' },
]

const FINAL_SUMMARY_EXPORT_ARTIFACT_STATUS_COLOR = {
  export_artifact_created: 'green',
  unsupported_format: 'gold',
  blocked: 'red',
  privacy_hold: 'magenta',
}

const REPORT_EXPORT_DOWNLOAD_PACKAGE_DECISION_OPTIONS = [
  { value: 'approve_for_future_download_package_runtime', label: 'approve_for_future_download_package_runtime' },
  { value: 'request_revision', label: 'request_revision' },
  { value: 'block', label: 'block' },
  { value: 'privacy_hold', label: 'privacy_hold' },
]

const REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR = {
  ready_for_future_download_package_runtime: 'green',
  local_manifest_ready: 'green',
  ready_for_future_public_access_external_delivery_runtime: 'green',
  needs_revision: 'gold',
  blocked: 'red',
  privacy_hold: 'magenta',
  failed_safe: 'red',
}

const REPORT_EXPORT_PUBLIC_ACCESS_EXTERNAL_DELIVERY_DECISION_OPTIONS = [
  {
    value: 'approve_for_future_public_access_external_delivery_runtime',
    label: 'approve_for_future_public_access_external_delivery_runtime',
  },
  { value: 'request_revision', label: 'request_revision' },
  { value: 'block', label: 'block' },
  { value: 'privacy_hold', label: 'privacy_hold' },
]

function statusTag(status) {
  return <Tag color={STATUS_COLOR[status] || 'default'}>{status || 'no_result'}</Tag>
}

function safetyTag(status) {
  return <Tag color={SAFETY_COLOR[status] || 'default'}>{status || 'not_reported'}</Tag>
}

function splitTags(value) {
  if (Array.isArray(value)) return value
  return String(value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
}

function boolText(value) {
  return value ? 'yes' : 'no'
}

function buildReviewChecklist(selectedKeys = []) {
  const selected = new Set(Array.isArray(selectedKeys) ? selectedKeys : [])
  return Object.fromEntries(REVIEW_CHECKLIST_KEYS.map((key) => [key, selected.has(key)]))
}

function buildPayload(values) {
  return {
    created_by: 'sentigraph_local_ui',
    case_seed: {
      title: values.title,
      description: values.description || '',
      keywords: splitTags(values.keywords),
      negative_keywords: splitTags(values.negative_keywords),
      language: splitTags(values.language).length ? splitTags(values.language) : ['zh-CN'],
      event_type: values.event_type || 'public_opinion_event',
      sensitive_flags: splitTags(values.sensitive_flags),
    },
    sampling_plan: {
      platforms: splitTags(values.platforms),
      time_range: {},
      target_comment_count: Number(values.target_comment_count || 500),
      target_source_count: Number(values.target_source_count || 30),
      max_runtime_minutes: Number(values.max_runtime_minutes || 60),
      sample_strategy: values.sample_strategy || 'stratified_public_sample',
    },
    safety_policy: {
      allow_live_collection: Boolean(values.allow_live_collection),
      allow_saved_profile: Boolean(values.allow_saved_profile),
      allow_manual_snapshot: values.allow_manual_snapshot !== false,
      allow_official_api: values.allow_official_api !== false,
      allow_vendor_api: values.allow_vendor_api !== false,
      forbid_proxy_pool: true,
      forbid_captcha_bypass: true,
      forbid_private_content: true,
    },
    privacy_policy: {
      remove_raw_author_id: true,
      remove_raw_author_name: true,
      remove_profile_url: true,
      remove_private_messages: true,
      minor_sensitive_mode: values.minor_sensitive_mode !== false,
    },
    output: {
      package_schema: 'sentigraph_evidence_export_v1',
      package_slug: '',
      package_index_required: true,
    },
  }
}

function draftEligibility(record) {
  const result = record?.provider_result
  if (!record) return { eligible: false, reason: '请选择一个分析请求。' }
  if (record.result_warning) return { eligible: false, reason: `Provider result 无法解析：${record.result_warning}` }
  if (!result) return { eligible: false, reason: '等待 Evidence package metadata。' }
  if (!['package_ready', 'validation_warn'].includes(result.status)) {
    return { eligible: false, reason: `当前状态 ${result.status || 'unknown'} 不可生成草稿。` }
  }
  if (!['safe', 'medium'].includes(result.safety_status)) {
    return { eligible: false, reason: `安全状态 ${result.safety_status || 'unknown'} 不可生成草稿。` }
  }
  if (Number(result.validation?.errors || 0) > 0) {
    return { eligible: false, reason: 'validation.errors 必须为 0。' }
  }
  if (!result.package_name) return { eligible: false, reason: '缺少 package_name。' }
  if (Number(result.counts?.evidence || 0) <= 0) return { eligible: false, reason: 'counts.evidence 必须大于 0。' }
  if (result.coverage?.not_full_web !== true || result.coverage?.not_full_platform !== true || result.coverage?.not_full_thread !== true) {
    return { eligible: false, reason: '缺少覆盖范围限制说明。' }
  }
  if (
    result.privacy?.raw_author_ids_removed !== true ||
    result.privacy?.raw_author_names_removed !== true ||
    result.privacy?.profile_urls_removed !== true ||
    result.privacy?.private_messages_excluded !== true
  ) {
    return { eligible: false, reason: '隐私字段必须确认已移除或排除。' }
  }
  return { eligible: true, reason: '可创建本地案例草稿 handoff。' }
}

function importPlanEligibility(caseDraft) {
  if (!caseDraft) return { eligible: false, reason: '请先创建或读取 case draft handoff。' }
  if (!['ready_for_manual_review', 'ready_for_manual_import_review'].includes(caseDraft.readiness?.state)) {
    return { eligible: false, reason: `Draft readiness ${caseDraft.readiness?.state || 'unknown'} 不可创建导入计划。` }
  }
  if (!['safe', 'medium'].includes(caseDraft.provider_summary?.safety_status)) {
    return { eligible: false, reason: `安全状态 ${caseDraft.provider_summary?.safety_status || 'unknown'} 不可创建导入计划。` }
  }
  if (!caseDraft.package_reference?.package_name) return { eligible: false, reason: 'Draft 缺少 package_name。' }
  if (Number(caseDraft.counts?.evidence || 0) <= 0) return { eligible: false, reason: 'Draft evidence count 必须大于 0。' }
  if (!['passed', 'warn', 'not_run'].includes(caseDraft.validation?.status)) {
    return { eligible: false, reason: `Validation status ${caseDraft.validation?.status || 'unknown'} 不可创建导入计划。` }
  }
  if (Number(caseDraft.validation?.errors || 0) > 0) {
    return { eligible: false, reason: 'Draft validation.errors 必须为 0。' }
  }
  if (caseDraft.coverage?.not_full_web !== true || caseDraft.coverage?.not_full_platform !== true || caseDraft.coverage?.not_full_thread !== true) {
    return { eligible: false, reason: 'Draft 必须保留 not_full_web / not_full_platform / not_full_thread。' }
  }
  if (
    caseDraft.privacy?.raw_author_ids_removed !== true ||
    caseDraft.privacy?.raw_author_names_removed !== true ||
    caseDraft.privacy?.profile_urls_removed !== true ||
    caseDraft.privacy?.private_messages_excluded !== true
  ) {
    return { eligible: false, reason: 'Draft 隐私移除标记不完整。' }
  }
  return { eligible: true, reason: '可生成 Evidence 导入计划。' }
}

function importPreviewEligibility(importPlan) {
  if (!importPlan) return { eligible: false, reason: '请先创建或读取 Evidence 导入计划。' }
  if (!['ready_for_manual_import_review', 'ready_for_human_review'].includes(importPlan.readiness?.state)) {
    return { eligible: false, reason: `Import plan readiness ${importPlan.readiness?.state || 'unknown'} 不可生成预览。` }
  }
  if (!importPlan.package_reference?.package_name) return { eligible: false, reason: 'Import plan 缺少 package_name。' }
  if (Number(importPlan.counts?.evidence || 0) <= 0) return { eligible: false, reason: 'Import plan evidence count 必须大于 0。' }
  if (!['passed', 'warn'].includes(importPlan.validation?.status)) {
    return { eligible: false, reason: `Validation status ${importPlan.validation?.status || 'unknown'} 不可生成导入预览。` }
  }
  if (Number(importPlan.validation?.errors || 0) > 0) {
    return { eligible: false, reason: 'Import plan validation.errors 必须为 0。' }
  }
  if (importPlan.coverage?.not_full_web !== true || importPlan.coverage?.not_full_platform !== true || importPlan.coverage?.not_full_thread !== true) {
    return { eligible: false, reason: 'Import plan 必须保留 not_full_web / not_full_platform / not_full_thread。' }
  }
  if (
    importPlan.privacy?.raw_author_ids_removed !== true ||
    importPlan.privacy?.raw_author_names_removed !== true ||
    importPlan.privacy?.profile_urls_removed !== true ||
    importPlan.privacy?.private_messages_excluded !== true
  ) {
    return { eligible: false, reason: 'Import plan 隐私移除标记不完整。' }
  }
  if (
    importPlan.proposed_import?.import_evidence_rows_now === true ||
    importPlan.proposed_import?.create_case_now === true ||
    importPlan.proposed_import?.run_analysis_now === true ||
    importPlan.proposed_import?.generate_sandbox_now === true ||
    importPlan.proposed_import?.generate_report_now === true
  ) {
    return { eligible: false, reason: 'Import plan 不允许包含立即导入、建 case、分析、Sandbox 或报告生成意图。' }
  }
  return { eligible: true, reason: '可以生成 metadata-only Evidence 导入预览。' }
}

function importJobEligibility(importPreview, latestReviewDecision) {
  if (!importPreview) return { eligible: false, reason: 'Create an Evidence import preview first.' }
  if (!latestReviewDecision) return { eligible: false, reason: 'Record a human review decision first.' }
  if (latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must be approve_import.' }
  }
  if (latestReviewDecision.readiness?.state !== 'approved_for_future_manual_import') {
    return { eligible: false, reason: `Review readiness ${latestReviewDecision.readiness?.state || 'unknown'} is not eligible.` }
  }
  const acknowledged = Object.values(latestReviewDecision.checklist || {}).filter(Boolean).length
  if (acknowledged < REVIEW_CHECKLIST_KEYS.length) {
    return { eligible: false, reason: 'approve_import requires all checklist acknowledgements.' }
  }
  if (importPreview.sample_preview_policy?.read_rows_now === true) {
    return { eligible: false, reason: 'Import preview must stay metadata-only and read_rows_now=false.' }
  }
  if (Number(importPreview.validation_summary?.errors || 0) > 0) {
    return { eligible: false, reason: 'Import preview validation errors must be 0.' }
  }
  return { eligible: true, reason: 'Ready to create a dry-run import job draft.' }
}

function executionPreflightEligibility(latestImportJob, latestReviewDecision) {
  if (!latestImportJob) return { eligible: false, reason: 'Create a dry-run import job draft first.' }
  if (!latestReviewDecision) return { eligible: false, reason: 'Record an approve_import review decision first.' }
  if (latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must be approve_import.' }
  }
  if (latestImportJob.status !== 'draft_not_executed') {
    return { eligible: false, reason: `Import job status ${latestImportJob.status || 'unknown'} is not eligible.` }
  }
  if (latestImportJob.execution_mode !== 'dry_run_gate') {
    return { eligible: false, reason: `Import job execution_mode ${latestImportJob.execution_mode || 'unknown'} is not eligible.` }
  }
  if (latestImportJob.readiness?.state !== 'ready_for_future_manual_import_execution') {
    return { eligible: false, reason: `Import job readiness ${latestImportJob.readiness?.state || 'unknown'} is not eligible.` }
  }
  if (latestImportJob.readiness?.can_execute_now === true) {
    return { eligible: false, reason: 'Import job must remain can_execute_now=false.' }
  }
  const unsafeFlags = latestImportJob.dry_run_result || {}
  const enabled = Object.entries(unsafeFlags).filter(([, value]) => value === true)
  if (enabled.length) {
    return { eligible: false, reason: `Dry-run now flags must remain false: ${enabled.map(([key]) => key).join(', ')}` }
  }
  return { eligible: true, reason: 'Ready to create metadata/file-name execution preflight.' }
}

function rowReaderDryRunEligibility(latestExecutionPreflight) {
  if (!latestExecutionPreflight) return { eligible: false, reason: 'Create an execution preflight first.' }
  if (!['preflight_passed', 'preflight_warn'].includes(latestExecutionPreflight.status)) {
    return { eligible: false, reason: `Execution preflight status ${latestExecutionPreflight.status || 'unknown'} is not eligible.` }
  }
  if (latestExecutionPreflight.package_file_checks?.row_files_opened === true || latestExecutionPreflight.package_file_checks?.row_files_parsed === true) {
    return { eligible: false, reason: 'Execution preflight must show row_files_opened=false and row_files_parsed=false.' }
  }
  if (latestExecutionPreflight.future_row_reader_plan?.read_rows_now === true) {
    return { eligible: false, reason: 'Execution preflight must keep read_rows_now=false.' }
  }
  if (latestExecutionPreflight.readiness?.requires_separate_execution_phase === false) {
    return { eligible: false, reason: 'Execution preflight must require a future/separate phase.' }
  }
  return { eligible: true, reason: 'Ready to run synthetic fixture row reader dry-run.' }
}

function realPackageRowPreviewEligibility(latestExecutionPreflight, latestRowReaderDryRun, latestReviewDecision) {
  if (!latestExecutionPreflight) return { eligible: false, reason: 'Create an execution preflight first.' }
  if (!latestRowReaderDryRun) return { eligible: false, reason: 'Run a synthetic row reader dry-run first.' }
  if (!['passed', 'warn'].includes(latestRowReaderDryRun.status)) {
    return { eligible: false, reason: `Synthetic row reader status ${latestRowReaderDryRun.status || 'unknown'} is not eligible.` }
  }
  if (!latestReviewDecision || latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must remain approve_import.' }
  }
  if (!['preflight_passed', 'preflight_warn'].includes(latestExecutionPreflight.status)) {
    return { eligible: false, reason: `Execution preflight status ${latestExecutionPreflight.status || 'unknown'} is not eligible.` }
  }
  if (latestExecutionPreflight.package_file_checks?.evidence_items_jsonl_present !== true) {
    return { eligible: false, reason: 'Execution preflight must confirm evidence_items.jsonl exists.' }
  }
  return { eligible: true, reason: 'Ready to create a limited real package row preview.' }
}

function reviewOnlyCaseEligibility(latestRealPackagePreview, latestReviewDecision) {
  if (!latestRealPackagePreview) return { eligible: false, reason: 'Create a limited real package row preview first.' }
  if (!['passed', 'warn'].includes(latestRealPackagePreview.status)) {
    return { eligible: false, reason: `Real package preview status ${latestRealPackagePreview.status || 'unknown'} is not eligible.` }
  }
  if (latestRealPackagePreview.status === 'privacy_stop') {
    return { eligible: false, reason: 'Privacy stop preview blocks review-only case creation.' }
  }
  if (latestRealPackagePreview.privacy_scan?.privacy_stop_triggered === true) {
    return { eligible: false, reason: 'Privacy stop is triggered; privacy/security review is required first.' }
  }
  const privacyScan = latestRealPackagePreview.privacy_scan || {}
  const privacyHits = [
    privacyScan.raw_author_id_detected,
    privacyScan.raw_author_name_detected,
    privacyScan.profile_url_detected,
    privacyScan.private_message_detected,
    privacyScan.secret_like_value_detected,
    privacyScan.email_detected,
    privacyScan.phone_detected,
  ].some((value) => Number(value || 0) > 0)
  if (privacyHits) {
    return { eligible: false, reason: 'Preview detected forbidden/privacy fields; do not create a review-only case.' }
  }
  if (Number(latestRealPackagePreview.rows?.accepted_for_preview || 0) <= 0) {
    return { eligible: false, reason: 'Preview must contain at least one accepted redacted row.' }
  }
  if (latestRealPackagePreview.readiness?.can_import_now === true) {
    return { eligible: false, reason: 'Preview must remain can_import_now=false.' }
  }
  if (!latestReviewDecision || latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must remain approve_import.' }
  }
  return { eligible: true, reason: 'Ready to create a review-only governance container.' }
}

function stagingImportEligibility(latestReviewOnlyCase, latestRealPackagePreview, latestReviewDecision, stagingImports) {
  if (!latestReviewOnlyCase) return { eligible: false, reason: 'Create a review-only case container first.' }
  if (stagingImports?.length) return { eligible: false, reason: 'A review-only staging import already exists for this request.' }
  if (!['draft', 'staging_pending'].includes(latestReviewOnlyCase.status)) {
    return { eligible: false, reason: `Review-only case status ${latestReviewOnlyCase.status || 'unknown'} is not eligible.` }
  }
  if (latestReviewOnlyCase.visibility !== 'internal_review_only') {
    return { eligible: false, reason: 'Review-only case must remain internal_review_only.' }
  }
  if (
    latestReviewOnlyCase.analysis_included ||
    latestReviewOnlyCase.production_case_created ||
    latestReviewOnlyCase.evidence_rows_imported ||
    latestReviewOnlyCase.evidence_layer_written ||
    latestReviewOnlyCase.review_queue_created ||
    latestReviewOnlyCase.dedup_run ||
    latestReviewOnlyCase.analysis_run
  ) {
    return { eligible: false, reason: 'Review-only case has unsafe side-effect flags.' }
  }
  if (!latestRealPackagePreview) return { eligible: false, reason: 'Create a limited real package row preview first.' }
  if (latestReviewOnlyCase.source_preview_run_id !== latestRealPackagePreview.preview_run_id) {
    return { eligible: false, reason: 'Latest preview does not match the review-only case source preview.' }
  }
  if (!['passed', 'warn'].includes(latestRealPackagePreview.status)) {
    return { eligible: false, reason: `Real package preview status ${latestRealPackagePreview.status || 'unknown'} is not eligible.` }
  }
  if (latestRealPackagePreview.status === 'privacy_stop' || latestRealPackagePreview.privacy_scan?.privacy_stop_triggered) {
    return { eligible: false, reason: 'Privacy stop preview blocks staging import.' }
  }
  if (Number(latestRealPackagePreview.rows?.accepted_for_preview || 0) <= 0) {
    return { eligible: false, reason: 'Preview must contain accepted redacted rows.' }
  }
  if (!latestReviewDecision || latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must remain approve_import.' }
  }
  return { eligible: true, reason: 'Ready to create review-only staging import from redacted preview rows.' }
}

function reviewQueueInitEligibility(latestReviewOnlyCase, latestStagingImport, latestReviewDecision, stagedCandidateBatch, queueInitializations) {
  if (!latestReviewOnlyCase) return { eligible: false, reason: 'Create a review-only case container first.' }
  if (!latestStagingImport) return { eligible: false, reason: 'Create a review-only staging import first.' }
  if (queueInitializations?.length) return { eligible: false, reason: 'A review queue initialization already exists for this request.' }
  if (!['draft', 'staging_pending'].includes(latestReviewOnlyCase.status)) {
    return { eligible: false, reason: `Review-only case status ${latestReviewOnlyCase.status || 'unknown'} is not eligible.` }
  }
  if (latestReviewOnlyCase.visibility !== 'internal_review_only') {
    return { eligible: false, reason: 'Review-only case must remain internal_review_only.' }
  }
  if (
    latestReviewOnlyCase.analysis_included ||
    latestReviewOnlyCase.production_case_created ||
    latestReviewOnlyCase.evidence_layer_written ||
    latestReviewOnlyCase.review_queue_created ||
    latestReviewOnlyCase.dedup_run ||
    latestReviewOnlyCase.analysis_run
  ) {
    return { eligible: false, reason: 'Review-only case has unsafe side-effect flags.' }
  }
  if (!['completed', 'partial'].includes(latestStagingImport.status)) {
    return { eligible: false, reason: `Staging import status ${latestStagingImport.status || 'unknown'} is not eligible.` }
  }
  if (latestStagingImport.readiness?.state !== 'staged_for_review_only') {
    return { eligible: false, reason: 'Staging import readiness must be staged_for_review_only.' }
  }
  if (latestStagingImport.target?.production_case_created || latestStagingImport.target?.evidence_layer_written) {
    return { eligible: false, reason: 'Staging import has unsafe production target flags.' }
  }
  if (!stagedCandidateBatch?.items && !stagedCandidateBatch?.candidates?.length) {
    return { eligible: false, reason: 'Staged evidence candidate batch is required.' }
  }
  if (!latestReviewDecision || latestReviewDecision.decision !== 'approve_import') {
    return { eligible: false, reason: 'Latest review decision must remain approve_import.' }
  }
  return { eligible: true, reason: 'Ready to initialize review-only queue items from staged candidates.' }
}

function SummaryList({ title, items }) {
  return (
    <Card size="small" title={title}>
      {items?.length ? (
        <ul className="compact-list">
          {items.map((item) => (
            <li key={item}>{item}</li>
          ))}
        </ul>
      ) : (
        <Text type="secondary">none</Text>
      )}
    </Card>
  )
}

export function AnalysisRequests() {
  const { message } = AntApp.useApp()
  const [form] = Form.useForm()
  const [reviewForm] = Form.useForm()
  const [importJobForm] = Form.useForm()
  const [rowReaderForm] = Form.useForm()
  const [realPackagePreviewForm] = Form.useForm()
  const [reviewOnlyCaseForm] = Form.useForm()
  const [stagingImportForm] = Form.useForm()
  const [reviewQueueInitForm] = Form.useForm()
  const [reviewQueueActionForm] = Form.useForm()
  const [reviewQueueCompletionGateForm] = Form.useForm()
  const [dedupPreviewForm] = Form.useForm()
  const [dedupGroupReviewForm] = Form.useForm()
  const [analysisReadyPromotionGateForm] = Form.useForm()
  const [manualAnalysisTriggerForm] = Form.useForm()
  const [analysisResultBoundaryGateForm] = Form.useForm()
  const [manualAnalysisExecutionForm] = Form.useForm()
  const [reportGenerationGateForm] = Form.useForm()
  const [summaryReportCandidateForm] = Form.useForm()
  const [finalSummaryReportReviewGateForm] = Form.useForm()
  const [finalSummaryReportForm] = Form.useForm()
  const [finalSummaryReportExportGateForm] = Form.useForm()
  const [finalSummaryReportExportArtifactForm] = Form.useForm()
  const [reportExportDownloadPackageGateForm] = Form.useForm()
  const [reportExportDownloadPackageArtifactForm] = Form.useForm()
  const [reportExportPublicAccessExternalDeliveryGateForm] = Form.useForm()
  const [config, setConfig] = useState(null)
  const [requests, setRequests] = useState([])
  const [selectedRequestId, setSelectedRequestId] = useState('')
  const [detail, setDetail] = useState(null)
  const [caseDraft, setCaseDraft] = useState(null)
  const [importPlan, setImportPlan] = useState(null)
  const [importPreview, setImportPreview] = useState(null)
  const [reviewDecisions, setReviewDecisions] = useState([])
  const [importJobs, setImportJobs] = useState([])
  const [executionPreflights, setExecutionPreflights] = useState([])
  const [rowReaderDryRuns, setRowReaderDryRuns] = useState([])
  const [realPackagePreviews, setRealPackagePreviews] = useState([])
  const [reviewOnlyCases, setReviewOnlyCases] = useState([])
  const [stagingImports, setStagingImports] = useState([])
  const [stagedCandidateBatch, setStagedCandidateBatch] = useState(null)
  const [reviewQueueInitializations, setReviewQueueInitializations] = useState([])
  const [reviewQueueItemBatch, setReviewQueueItemBatch] = useState(null)
  const [reviewQueueActionAudits, setReviewQueueActionAudits] = useState([])
  const [reviewQueueCompletionGates, setReviewQueueCompletionGates] = useState([])
  const [dedupPreviews, setDedupPreviews] = useState([])
  const [dedupGroupReviewAudits, setDedupGroupReviewAudits] = useState([])
  const [analysisReadyPromotionGates, setAnalysisReadyPromotionGates] = useState([])
  const [promotionDecisionAudits, setPromotionDecisionAudits] = useState([])
  const [manualAnalysisTriggers, setManualAnalysisTriggers] = useState([])
  const [manualAnalysisTriggerAudits, setManualAnalysisTriggerAudits] = useState([])
  const [analysisResultBoundaryGates, setAnalysisResultBoundaryGates] = useState([])
  const [analysisResultBoundaryGateAudits, setAnalysisResultBoundaryGateAudits] = useState([])
  const [manualAnalysisExecutions, setManualAnalysisExecutions] = useState([])
  const [manualAnalysisResultCandidates, setManualAnalysisResultCandidates] = useState([])
  const [manualAnalysisExecutionAudits, setManualAnalysisExecutionAudits] = useState([])
  const [reportGenerationGates, setReportGenerationGates] = useState([])
  const [reportGenerationGateAudits, setReportGenerationGateAudits] = useState([])
  const [summaryReportCandidates, setSummaryReportCandidates] = useState([])
  const [summaryReportCandidateAudits, setSummaryReportCandidateAudits] = useState([])
  const [finalSummaryReportReviewGates, setFinalSummaryReportReviewGates] = useState([])
  const [finalSummaryReportReviewGateAudits, setFinalSummaryReportReviewGateAudits] = useState([])
  const [finalSummaryReports, setFinalSummaryReports] = useState([])
  const [finalSummaryReportAudits, setFinalSummaryReportAudits] = useState([])
  const [finalSummaryReportExportGates, setFinalSummaryReportExportGates] = useState([])
  const [finalSummaryReportExportGateAudits, setFinalSummaryReportExportGateAudits] = useState([])
  const [finalSummaryReportExportArtifacts, setFinalSummaryReportExportArtifacts] = useState([])
  const [finalSummaryReportExportArtifactAudits, setFinalSummaryReportExportArtifactAudits] = useState([])
  const [reportExportDownloadPackageGates, setReportExportDownloadPackageGates] = useState([])
  const [reportExportDownloadPackageGateAudits, setReportExportDownloadPackageGateAudits] = useState([])
  const [reportExportDownloadPackageArtifacts, setReportExportDownloadPackageArtifacts] = useState([])
  const [reportExportDownloadPackageArtifactAudits, setReportExportDownloadPackageArtifactAudits] = useState([])
  const [reportExportPublicAccessExternalDeliveryGates, setReportExportPublicAccessExternalDeliveryGates] = useState([])
  const [reportExportPublicAccessExternalDeliveryGateAudits, setReportExportPublicAccessExternalDeliveryGateAudits] = useState([])
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [canceling, setCanceling] = useState(false)
  const [draftLoading, setDraftLoading] = useState(false)
  const [planLoading, setPlanLoading] = useState(false)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [reviewLoading, setReviewLoading] = useState(false)
  const [importJobLoading, setImportJobLoading] = useState(false)
  const [executionPreflightLoading, setExecutionPreflightLoading] = useState(false)
  const [rowReaderDryRunLoading, setRowReaderDryRunLoading] = useState(false)
  const [realPackagePreviewLoading, setRealPackagePreviewLoading] = useState(false)
  const [reviewOnlyCaseLoading, setReviewOnlyCaseLoading] = useState(false)
  const [stagingImportLoading, setStagingImportLoading] = useState(false)
  const [reviewQueueInitLoading, setReviewQueueInitLoading] = useState(false)
  const [reviewQueueActionLoading, setReviewQueueActionLoading] = useState('')
  const [reviewQueueCompletionGateLoading, setReviewQueueCompletionGateLoading] = useState(false)
  const [dedupPreviewLoading, setDedupPreviewLoading] = useState(false)
  const [dedupGroupReviewLoading, setDedupGroupReviewLoading] = useState('')
  const [analysisReadyPromotionGateLoading, setAnalysisReadyPromotionGateLoading] = useState(false)
  const [manualAnalysisTriggerLoading, setManualAnalysisTriggerLoading] = useState(false)
  const [analysisResultBoundaryGateLoading, setAnalysisResultBoundaryGateLoading] = useState(false)
  const [manualAnalysisExecutionLoading, setManualAnalysisExecutionLoading] = useState(false)
  const [reportGenerationGateLoading, setReportGenerationGateLoading] = useState(false)
  const [summaryReportCandidateLoading, setSummaryReportCandidateLoading] = useState(false)
  const [finalSummaryReportReviewGateLoading, setFinalSummaryReportReviewGateLoading] = useState(false)
  const [finalSummaryReportLoading, setFinalSummaryReportLoading] = useState(false)
  const [finalSummaryReportExportGateLoading, setFinalSummaryReportExportGateLoading] = useState(false)
  const [finalSummaryReportExportArtifactLoading, setFinalSummaryReportExportArtifactLoading] = useState(false)
  const [reportExportDownloadPackageGateLoading, setReportExportDownloadPackageGateLoading] = useState(false)
  const [reportExportDownloadPackageArtifactLoading, setReportExportDownloadPackageArtifactLoading] = useState(false)
  const [reportExportPublicAccessExternalDeliveryGateLoading, setReportExportPublicAccessExternalDeliveryGateLoading] = useState(false)
  const [error, setError] = useState('')
  const [draftError, setDraftError] = useState('')
  const [planError, setPlanError] = useState('')
  const [previewError, setPreviewError] = useState('')
  const [reviewError, setReviewError] = useState('')
  const [importJobError, setImportJobError] = useState('')
  const [executionPreflightError, setExecutionPreflightError] = useState('')
  const [rowReaderDryRunError, setRowReaderDryRunError] = useState('')
  const [realPackagePreviewError, setRealPackagePreviewError] = useState('')
  const [reviewOnlyCaseError, setReviewOnlyCaseError] = useState('')
  const [stagingImportError, setStagingImportError] = useState('')
  const [reviewQueueInitError, setReviewQueueInitError] = useState('')
  const [reviewQueueActionError, setReviewQueueActionError] = useState('')
  const [reviewQueueCompletionGateError, setReviewQueueCompletionGateError] = useState('')
  const [dedupPreviewError, setDedupPreviewError] = useState('')
  const [dedupGroupReviewError, setDedupGroupReviewError] = useState('')
  const [analysisReadyPromotionGateError, setAnalysisReadyPromotionGateError] = useState('')
  const [manualAnalysisTriggerError, setManualAnalysisTriggerError] = useState('')
  const [analysisResultBoundaryGateError, setAnalysisResultBoundaryGateError] = useState('')
  const [manualAnalysisExecutionError, setManualAnalysisExecutionError] = useState('')
  const [reportGenerationGateError, setReportGenerationGateError] = useState('')
  const [summaryReportCandidateError, setSummaryReportCandidateError] = useState('')
  const [finalSummaryReportReviewGateError, setFinalSummaryReportReviewGateError] = useState('')
  const [finalSummaryReportError, setFinalSummaryReportError] = useState('')
  const [finalSummaryReportExportGateError, setFinalSummaryReportExportGateError] = useState('')
  const [finalSummaryReportExportArtifactError, setFinalSummaryReportExportArtifactError] = useState('')
  const [reportExportDownloadPackageGateError, setReportExportDownloadPackageGateError] = useState('')
  const [reportExportDownloadPackageArtifactError, setReportExportDownloadPackageArtifactError] = useState('')
  const [reportExportPublicAccessExternalDeliveryGateError, setReportExportPublicAccessExternalDeliveryGateError] = useState('')

  const selectedRecord = useMemo(
    () => detail || requests.find((item) => item.request_id === selectedRequestId) || null,
    [detail, requests, selectedRequestId],
  )
  const draftGate = useMemo(() => draftEligibility(selectedRecord), [selectedRecord])
  const planGate = useMemo(() => importPlanEligibility(caseDraft), [caseDraft])
  const previewGate = useMemo(() => importPreviewEligibility(importPlan), [importPlan])
  const watchedReviewDecision = Form.useWatch('decision', reviewForm)
  const watchedReviewChecklist = Form.useWatch('checklist', reviewForm)
  const watchedReviewerLabel = Form.useWatch('reviewer_label', reviewForm)
  const reviewSubmitDisabled = useMemo(() => {
    if (!importPreview || reviewLoading) return true
    if (!String(watchedReviewerLabel || '').trim()) return true
    if (watchedReviewDecision !== 'approve_import') return false
    const selected = new Set(Array.isArray(watchedReviewChecklist) ? watchedReviewChecklist : [])
    return REVIEW_CHECKLIST_KEYS.some((key) => !selected.has(key))
  }, [importPreview, reviewLoading, watchedReviewChecklist, watchedReviewDecision, watchedReviewerLabel])

  function clearManualAnalysisTriggerState() {
    setManualAnalysisTriggers([])
    setManualAnalysisTriggerAudits([])
    setManualAnalysisTriggerError('')
    setAnalysisResultBoundaryGates([])
    setAnalysisResultBoundaryGateAudits([])
    setAnalysisResultBoundaryGateError('')
    setManualAnalysisExecutions([])
    setManualAnalysisResultCandidates([])
    setManualAnalysisExecutionAudits([])
    setManualAnalysisExecutionError('')
    setReportGenerationGates([])
    setReportGenerationGateAudits([])
    setReportGenerationGateError('')
    setSummaryReportCandidates([])
    setSummaryReportCandidateAudits([])
    setSummaryReportCandidateError('')
    setFinalSummaryReportReviewGates([])
    setFinalSummaryReportReviewGateAudits([])
    setFinalSummaryReportReviewGateError('')
    setFinalSummaryReports([])
    setFinalSummaryReportAudits([])
    setFinalSummaryReportError('')
    setFinalSummaryReportExportGates([])
    setFinalSummaryReportExportGateAudits([])
    setFinalSummaryReportExportGateError('')
    setFinalSummaryReportExportArtifacts([])
    setFinalSummaryReportExportArtifactAudits([])
    setFinalSummaryReportExportArtifactError('')
    setReportExportDownloadPackageGates([])
    setReportExportDownloadPackageGateAudits([])
    setReportExportDownloadPackageGateError('')
    setReportExportDownloadPackageArtifacts([])
    setReportExportDownloadPackageArtifactAudits([])
    setReportExportDownloadPackageArtifactError('')
    setReportExportPublicAccessExternalDeliveryGates([])
    setReportExportPublicAccessExternalDeliveryGateAudits([])
    setReportExportPublicAccessExternalDeliveryGateError('')
  }

  async function loadDraftAndPlan(requestId) {
    if (!requestId) {
      setCaseDraft(null)
      setImportPlan(null)
      setImportPreview(null)
      setReviewDecisions([])
      setImportJobs([])
      setExecutionPreflights([])
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      setStagingImports([])
      setStagedCandidateBatch(null)
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      setReviewQueueActionAudits([])
      setReviewQueueCompletionGates([])
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      setReportExportPublicAccessExternalDeliveryGates([])
      setReportExportPublicAccessExternalDeliveryGateAudits([])
      clearManualAnalysisTriggerState()
      setDraftError('')
      setPlanError('')
      setPreviewError('')
      setReviewError('')
      setImportJobError('')
      setExecutionPreflightError('')
      setRowReaderDryRunError('')
      setRealPackagePreviewError('')
      setReviewOnlyCaseError('')
      setStagingImportError('')
      setReviewQueueInitError('')
      setReviewQueueActionError('')
      setReviewQueueCompletionGateError('')
      setDedupPreviewError('')
      setDedupGroupReviewError('')
      setAnalysisReadyPromotionGateError('')
      return
    }
    try {
      setCaseDraft(await getAnalysisRequestCaseDraft(requestId))
      setDraftError('')
    } catch {
      setCaseDraft(null)
      setDraftError('')
    }
    try {
      setImportPlan(await getAnalysisRequestImportPlan(requestId))
      setPlanError('')
    } catch {
      setImportPlan(null)
      setPlanError('')
    }
    try {
      setImportPreview(await getAnalysisRequestImportPreview(requestId))
      setPreviewError('')
    } catch {
      setImportPreview(null)
      setPreviewError('')
    }
    try {
      setReviewDecisions(await listAnalysisRequestReviewDecisions(requestId))
      setReviewError('')
    } catch {
      setReviewDecisions([])
      setReviewError('')
    }
    try {
      setImportJobs(await listAnalysisRequestImportJobs(requestId))
      setImportJobError('')
    } catch {
      setImportJobs([])
      setImportJobError('')
    }
    try {
      setExecutionPreflights(await listAnalysisRequestExecutionPreflights(requestId))
      setExecutionPreflightError('')
    } catch {
      setExecutionPreflights([])
      setExecutionPreflightError('')
    }
    try {
      setRowReaderDryRuns(await listAnalysisRequestRowReaderDryRuns(requestId))
      setRowReaderDryRunError('')
    } catch {
      setRowReaderDryRuns([])
      setRowReaderDryRunError('')
    }
    try {
      setRealPackagePreviews(await listAnalysisRequestRealPackageRowPreviews(requestId))
      setRealPackagePreviewError('')
    } catch {
      setRealPackagePreviews([])
      setRealPackagePreviewError('')
    }
    try {
      setReviewOnlyCases(await listAnalysisRequestReviewOnlyCases(requestId))
      setReviewOnlyCaseError('')
    } catch {
      setReviewOnlyCases([])
      setReviewOnlyCaseError('')
    }
    try {
      const nextStagingImports = await listAnalysisRequestStagingImports(requestId)
      setStagingImports(nextStagingImports)
      setStagingImportError('')
      if (nextStagingImports[0]?.staging_import_id) {
        setStagedCandidateBatch(
          await getAnalysisRequestStagingImportCandidates(requestId, nextStagingImports[0].staging_import_id),
        )
      } else {
        setStagedCandidateBatch(null)
      }
    } catch {
      setStagingImports([])
      setStagedCandidateBatch(null)
      setStagingImportError('')
    }
    try {
      const nextQueueInitializations = await listAnalysisRequestReviewQueueInitializations(requestId)
      setReviewQueueInitializations(nextQueueInitializations)
      setReviewQueueInitError('')
      if (nextQueueInitializations[0]?.queue_init_id) {
        setReviewQueueItemBatch(
          await getAnalysisRequestReviewQueueItems(requestId, nextQueueInitializations[0].queue_init_id),
        )
      } else {
        setReviewQueueItemBatch(null)
      }
      setReviewQueueActionAudits(await listAnalysisRequestReviewQueueActionAudits(requestId))
      setReviewQueueCompletionGates(await listAnalysisRequestReviewQueueCompletionGates(requestId))
      setDedupPreviews(await listAnalysisRequestDedupPreviews(requestId))
      setDedupGroupReviewAudits(await listAnalysisRequestDedupGroupReviewAudits(requestId))
      setAnalysisReadyPromotionGates(await listAnalysisRequestAnalysisReadyPromotionGates(requestId))
      setPromotionDecisionAudits(await listAnalysisRequestPromotionDecisionAudits(requestId))
      setManualAnalysisTriggers(await listAnalysisRequestManualAnalysisTriggers(requestId))
      setManualAnalysisTriggerAudits(await listAnalysisRequestManualAnalysisTriggerAudits(requestId))
      setAnalysisResultBoundaryGates(await listAnalysisRequestAnalysisResultBoundaryGates(requestId))
      setAnalysisResultBoundaryGateAudits(await listAnalysisRequestAnalysisResultBoundaryGateAudits(requestId))
      setManualAnalysisExecutions(await listAnalysisRequestManualAnalysisExecutions(requestId))
      setManualAnalysisResultCandidates(await listAnalysisRequestManualAnalysisResultCandidates(requestId))
      setManualAnalysisExecutionAudits(await listAnalysisRequestManualAnalysisExecutionAudits(requestId))
      setReportGenerationGates(await listAnalysisRequestReportGenerationGates(requestId))
      setReportGenerationGateAudits(await listAnalysisRequestReportGenerationGateAudits(requestId))
      setSummaryReportCandidates(await listAnalysisRequestSummaryReportCandidates(requestId))
      setSummaryReportCandidateAudits(await listAnalysisRequestSummaryReportCandidateAudits(requestId))
      setFinalSummaryReportReviewGates(await listAnalysisRequestFinalSummaryReportReviewGates(requestId))
      setFinalSummaryReportReviewGateAudits(await listAnalysisRequestFinalSummaryReportReviewGateAudits(requestId))
      setFinalSummaryReports(await listAnalysisRequestFinalSummaryReports(requestId))
      setFinalSummaryReportAudits(await listAnalysisRequestFinalSummaryReportAudits(requestId))
      setFinalSummaryReportExportGates(await listAnalysisRequestFinalSummaryReportExportGates(requestId))
      setFinalSummaryReportExportGateAudits(await listAnalysisRequestFinalSummaryReportExportGateAudits(requestId))
      setFinalSummaryReportExportArtifacts(await listAnalysisRequestFinalSummaryReportExportArtifacts(requestId))
      setFinalSummaryReportExportArtifactAudits(await listAnalysisRequestFinalSummaryReportExportArtifactAudits(requestId))
      setReportExportDownloadPackageGates(await listAnalysisRequestReportExportDownloadPackageGates(requestId))
      setReportExportDownloadPackageGateAudits(await listAnalysisRequestReportExportDownloadPackageGateAudits(requestId))
      setReportExportDownloadPackageArtifacts(await listAnalysisRequestReportExportDownloadPackageArtifacts(requestId))
      setReportExportDownloadPackageArtifactAudits(await listAnalysisRequestReportExportDownloadPackageArtifactAudits(requestId))
      setReportExportPublicAccessExternalDeliveryGates(await listAnalysisRequestReportExportPublicAccessExternalDeliveryGates(requestId))
      setReportExportPublicAccessExternalDeliveryGateAudits(await listAnalysisRequestReportExportPublicAccessExternalDeliveryGateAudits(requestId))
    } catch {
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      setReviewQueueActionAudits([])
      setReviewQueueCompletionGates([])
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      setReviewQueueInitError('')
      setReviewQueueActionError('')
      setReviewQueueCompletionGateError('')
      setDedupPreviewError('')
      setDedupGroupReviewError('')
      setAnalysisReadyPromotionGateError('')
      setReportExportPublicAccessExternalDeliveryGateError('')
    }
  }

  async function loadRequests(nextSelectedId = selectedRequestId) {
    setLoading(true)
    setError('')
    try {
      const [nextConfig, nextRequests] = await Promise.all([
        getAnalysisRequestConfig(),
        listAnalysisRequests(),
      ])
      setConfig(nextConfig)
      setRequests(nextRequests)
      const fallbackId = nextSelectedId || nextRequests[0]?.request_id || ''
      setSelectedRequestId(fallbackId)
      const nextDetail = fallbackId ? await getAnalysisRequest(fallbackId) : null
      setDetail(nextDetail)
      await loadDraftAndPlan(fallbackId)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load local analysis requests.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRequests('')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate(values) {
    setCreating(true)
    setError('')
    try {
      const created = await createAnalysisRequest(buildPayload(values))
      message.success('已创建本地分析请求 JSON')
      await loadRequests(created.request_id)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to create local analysis request.')
    } finally {
      setCreating(false)
    }
  }

  async function handleOpen(record) {
    setSelectedRequestId(record.request_id)
    setError('')
    setDraftError('')
    setPlanError('')
    setPreviewError('')
    setReviewError('')
    setImportJobError('')
    setExecutionPreflightError('')
    setRowReaderDryRunError('')
    setRealPackagePreviewError('')
    try {
      setDetail(await getAnalysisRequest(record.request_id))
      await loadDraftAndPlan(record.request_id)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to open analysis request.')
    }
  }

  async function handleCancel() {
    if (!selectedRecord?.request_id) return
    setCanceling(true)
    setError('')
    try {
      const result = await cancelAnalysisRequest(selectedRecord.request_id)
      if (result.warning) {
        message.warning(result.warning)
      } else {
        message.success('已记录本地 canceled 状态；未调用 Provider')
      }
      await loadRequests(selectedRecord.request_id)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to cancel local analysis request.')
    } finally {
      setCanceling(false)
    }
  }

  async function handleCreateCaseDraft() {
    if (!selectedRecord?.request_id) return
    setDraftLoading(true)
    setDraftError('')
    try {
      const draft = await createAnalysisRequestCaseDraft(selectedRecord.request_id)
      setCaseDraft(draft)
      message.success('已创建本地案例草稿 handoff')
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create case draft.'
      setDraftError(String(messageText))
    } finally {
      setDraftLoading(false)
    }
  }

  async function handleCreateImportPlan() {
    if (!selectedRecord?.request_id) return
    setPlanLoading(true)
    setPlanError('')
    try {
      const plan = await createAnalysisRequestImportPlan(selectedRecord.request_id)
      setImportPlan(plan)
      setImportPreview(null)
      setReviewDecisions([])
      setImportJobs([])
      setExecutionPreflights([])
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      message.success('已生成 Evidence 导入计划')
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create evidence import plan.'
      setPlanError(String(messageText))
    } finally {
      setPlanLoading(false)
    }
  }

  async function handleCreateImportPreview() {
    if (!selectedRecord?.request_id) return
    setPreviewLoading(true)
    setPreviewError('')
    try {
      const preview = await createAnalysisRequestImportPreview(selectedRecord.request_id)
      setImportPreview(preview)
      setReviewDecisions([])
      setImportJobs([])
      setExecutionPreflights([])
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      message.success('已生成 metadata-only Evidence 导入预览')
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create evidence import preview.'
      setPreviewError(String(messageText))
    } finally {
      setPreviewLoading(false)
    }
  }

  async function handleCreateReviewDecision(values) {
    if (!selectedRecord?.request_id) return
    setReviewLoading(true)
    setReviewError('')
    try {
      const decision = await createAnalysisRequestReviewDecision(selectedRecord.request_id, {
        reviewer_label: values.reviewer_label || '',
        decision: values.decision || 'request_more_source',
        target_case_mode: values.target_case_mode || 'new_review_case',
        target_case_id: values.target_case_id || null,
        notes: values.notes || '',
        checklist: buildReviewChecklist(values.checklist || []),
        created_by: 'sentigraph_local_ui',
      })
      setReviewDecisions(await listAnalysisRequestReviewDecisions(selectedRecord.request_id))
      setImportJobs([])
      setExecutionPreflights([])
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      message.success(`已记录人工审核决策：${decision.decision}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create review decision.'
      setReviewError(String(messageText))
    } finally {
      setReviewLoading(false)
    }
  }

  async function handleCreateImportJob(values) {
    if (!selectedRecord?.request_id) return
    setImportJobLoading(true)
    setImportJobError('')
    try {
      const payload = {
        decision_id: values.decision_id || undefined,
        target_case_mode: values.target_case_mode || 'new_review_case',
        target_case_id: values.target_case_mode === 'existing_case' ? values.target_case_id || '' : null,
        created_by: 'sentigraph_local_ui',
      }
      const job = await createAnalysisRequestImportJob(selectedRecord.request_id, payload)
      setImportJobs(await listAnalysisRequestImportJobs(selectedRecord.request_id))
      setExecutionPreflights([])
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      message.success(`Created dry-run import job draft: ${job.job_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create manual import job draft.'
      setImportJobError(String(messageText))
    } finally {
      setImportJobLoading(false)
    }
  }

  async function handleCreateExecutionPreflight() {
    if (!selectedRecord?.request_id) return
    setExecutionPreflightLoading(true)
    setExecutionPreflightError('')
    try {
      const preflight = await createAnalysisRequestExecutionPreflight(selectedRecord.request_id, {
        job_id: latestImportJob?.job_id || undefined,
        created_by: 'sentigraph_local_ui',
      })
      setExecutionPreflights(await listAnalysisRequestExecutionPreflights(selectedRecord.request_id))
      setRowReaderDryRuns([])
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      message.success(`Created execution preflight: ${preflight.preflight_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create execution preflight.'
      setExecutionPreflightError(String(messageText))
    } finally {
      setExecutionPreflightLoading(false)
    }
  }

  async function handleCreateRowReaderDryRun(values) {
    if (!selectedRecord?.request_id) return
    setRowReaderDryRunLoading(true)
    setRowReaderDryRunError('')
    try {
      const dryRun = await createAnalysisRequestRowReaderDryRun(selectedRecord.request_id, {
        preflight_id: latestExecutionPreflight?.preflight_id || undefined,
        fixture_name: values.fixture_name || 'safe_evidence_items',
        fixture_mode: 'synthetic_fixture',
        max_rows: Math.min(20, Math.max(1, Number(values.max_rows || 20))),
        created_by: 'sentigraph_local_ui',
      })
      setRowReaderDryRuns(await listAnalysisRequestRowReaderDryRuns(selectedRecord.request_id))
      setRealPackagePreviews([])
      setReviewOnlyCases([])
      message.success(`Created synthetic row reader dry-run: ${dryRun.dry_run_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create synthetic row reader dry-run.'
      setRowReaderDryRunError(String(messageText))
    } finally {
      setRowReaderDryRunLoading(false)
    }
  }

  async function handleCreateRealPackagePreview(values) {
    if (!selectedRecord?.request_id) return
    setRealPackagePreviewLoading(true)
    setRealPackagePreviewError('')
    try {
      const preview = await createAnalysisRequestRealPackageRowPreview(selectedRecord.request_id, {
        max_rows: Math.min(20, Math.max(1, Number(values.max_rows || 10))),
        acknowledge_real_package_preview: Boolean(values.acknowledge_real_package_preview),
        acknowledge_no_import: Boolean(values.acknowledge_no_import),
        acknowledge_preview_not_representative: Boolean(values.acknowledge_preview_not_representative),
        acknowledge_privacy_stop: Boolean(values.acknowledge_privacy_stop),
        created_by: 'sentigraph_local_ui',
      })
      setRealPackagePreviews(await listAnalysisRequestRealPackageRowPreviews(selectedRecord.request_id))
      setReviewOnlyCases([])
      setStagingImports([])
      setStagedCandidateBatch(null)
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      setReviewQueueActionAudits([])
      message.success(`Created limited real package row preview: ${preview.status}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create limited real package row preview.'
      setRealPackagePreviewError(String(messageText))
    } finally {
      setRealPackagePreviewLoading(false)
    }
  }

  async function handleCreateReviewOnlyCase(values) {
    if (!selectedRecord?.request_id) return
    setReviewOnlyCaseLoading(true)
    setReviewOnlyCaseError('')
    try {
      const reviewCase = await createAnalysisRequestReviewOnlyCase(selectedRecord.request_id, {
        source_preview_run_id: latestRealPackagePreview?.preview_run_id || undefined,
        target_case_mode: values.target_case_mode || 'new_review_case',
        target_case_id: values.target_case_mode === 'existing_case_review_wrapper' ? String(values.target_case_id || '').trim() : null,
        created_by: 'sentigraph_local_ui',
      })
      setReviewOnlyCases(await listAnalysisRequestReviewOnlyCases(selectedRecord.request_id))
      setStagingImports([])
      setStagedCandidateBatch(null)
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      message.success(`Created review-only case container: ${reviewCase.review_case_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create review-only case container.'
      setReviewOnlyCaseError(String(messageText))
    } finally {
      setReviewOnlyCaseLoading(false)
    }
  }

  async function handleCreateStagingImport(values) {
    if (!selectedRecord?.request_id) return
    setStagingImportLoading(true)
    setStagingImportError('')
    try {
      const stagingImport = await createAnalysisRequestStagingImport(selectedRecord.request_id, {
        review_case_id: values.review_case_id || latestReviewOnlyCase?.review_case_id || undefined,
        preview_run_id: values.preview_run_id || latestReviewOnlyCase?.source_preview_run_id || undefined,
        acknowledge_review_only_staging: Boolean(values.acknowledge_review_only_staging),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_analysis: Boolean(values.acknowledge_no_analysis),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        created_by: 'sentigraph_local_ui',
      })
      const nextStagingImports = await listAnalysisRequestStagingImports(selectedRecord.request_id)
      setStagingImports(nextStagingImports)
      setStagedCandidateBatch(
        await getAnalysisRequestStagingImportCandidates(selectedRecord.request_id, stagingImport.staging_import_id),
      )
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      setReviewQueueActionAudits([])
      setReviewQueueCompletionGates([])
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Created review-only staging import: ${stagingImport.staging_import_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create review-only staging import.'
      setStagingImportError(String(messageText))
    } finally {
      setStagingImportLoading(false)
    }
  }

  async function handleCreateReviewQueueInitialization(values) {
    if (!selectedRecord?.request_id) return
    setReviewQueueInitLoading(true)
    setReviewQueueInitError('')
    try {
      const queueInit = await createAnalysisRequestReviewQueueInitialization(selectedRecord.request_id, {
        review_case_id: values.review_case_id || latestReviewOnlyCase?.review_case_id || undefined,
        staging_import_id: values.staging_import_id || latestStagingImport?.staging_import_id || undefined,
        acknowledge_review_only_queue: Boolean(values.acknowledge_review_only_queue),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_dedup: Boolean(values.acknowledge_no_dedup),
        acknowledge_no_analysis: Boolean(values.acknowledge_no_analysis),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        created_by: 'sentigraph_local_ui',
      })
      const nextQueueInitializations = await listAnalysisRequestReviewQueueInitializations(selectedRecord.request_id)
      setReviewQueueInitializations(nextQueueInitializations)
      setReviewQueueItemBatch(
        await getAnalysisRequestReviewQueueItems(selectedRecord.request_id, queueInit.queue_init_id),
      )
      setReviewQueueActionAudits(await listAnalysisRequestReviewQueueActionAudits(selectedRecord.request_id))
      setReviewQueueCompletionGates(await listAnalysisRequestReviewQueueCompletionGates(selectedRecord.request_id))
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Initialized review-only queue: ${queueInit.queue_init_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to initialize review-only queue.'
      setReviewQueueInitError(String(messageText))
    } finally {
      setReviewQueueInitLoading(false)
    }
  }

  async function handleReviewQueueAction(item, action) {
    if (!selectedRecord?.request_id || !item?.review_item_id) return
    setReviewQueueActionLoading(`${item.review_item_id}:${action}`)
    setReviewQueueActionError('')
    try {
      const values = reviewQueueActionForm.getFieldsValue()
      const result = await createAnalysisRequestReviewQueueItemAction(selectedRecord.request_id, item.review_item_id, {
        action,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        duplicate_group_id: action === 'merge_duplicate' ? String(values.duplicate_group_id || '').trim() || undefined : undefined,
        duplicate_of_review_item_id:
          action === 'merge_duplicate' ? String(values.duplicate_of_review_item_id || '').trim() || undefined : undefined,
        acknowledge_review_only_action: Boolean(values.acknowledge_review_only_action),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_dedup: Boolean(values.acknowledge_no_dedup),
        acknowledge_no_analysis: Boolean(values.acknowledge_no_analysis),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
      })
      setReviewQueueItemBatch(
        await getAnalysisRequestReviewQueueItems(selectedRecord.request_id, result.queue_init_id || item.queue_init_id),
      )
      setReviewQueueActionAudits(await listAnalysisRequestReviewQueueActionAudits(selectedRecord.request_id))
      setReviewQueueCompletionGates(await listAnalysisRequestReviewQueueCompletionGates(selectedRecord.request_id))
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Recorded review action: ${action}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to record review queue action.'
      setReviewQueueActionError(String(messageText))
    } finally {
      setReviewQueueActionLoading('')
    }
  }

  async function handleCreateReviewQueueCompletionGate(values) {
    if (!selectedRecord?.request_id) return
    setReviewQueueCompletionGateLoading(true)
    setReviewQueueCompletionGateError('')
    try {
      const gate = await createAnalysisRequestReviewQueueCompletionGate(selectedRecord.request_id, {
        queue_init_id: values.queue_init_id || latestReviewQueueInitialization?.queue_init_id || undefined,
        review_case_id: values.review_case_id || latestReviewQueueInitialization?.review_case_id || undefined,
        minimum_reviewed_ratio: Number(values.minimum_reviewed_ratio ?? 1),
        allow_deferred_items: Boolean(values.allow_deferred_items),
        acknowledge_completion_is_not_dedup: Boolean(values.acknowledge_completion_is_not_dedup),
        acknowledge_completion_is_not_analysis: Boolean(values.acknowledge_completion_is_not_analysis),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        created_by: 'sentigraph_local_ui',
      })
      setReviewQueueCompletionGates(await listAnalysisRequestReviewQueueCompletionGates(selectedRecord.request_id))
      setDedupPreviews(await listAnalysisRequestDedupPreviews(selectedRecord.request_id))
      setDedupGroupReviewAudits(await listAnalysisRequestDedupGroupReviewAudits(selectedRecord.request_id))
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Evaluated completion gate: ${gate.status}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to evaluate review queue completion gate.'
      setReviewQueueCompletionGateError(String(messageText))
    } finally {
      setReviewQueueCompletionGateLoading(false)
    }
  }

  async function handleCreateDedupPreview(values) {
    if (!selectedRecord?.request_id) return
    setDedupPreviewLoading(true)
    setDedupPreviewError('')
    try {
      const preview = await createAnalysisRequestDedupPreview(selectedRecord.request_id, {
        review_case_id: values.review_case_id || latestReviewQueueCompletionGate?.review_case_id || undefined,
        queue_init_id: values.queue_init_id || latestReviewQueueCompletionGate?.queue_init_id || undefined,
        completion_gate_id: values.completion_gate_id || latestReviewQueueCompletionGate?.completion_gate_id || undefined,
        include_marked_weak: Boolean(values.include_marked_weak),
        include_duplicate_merged: Boolean(values.include_duplicate_merged),
        acknowledge_dedup_preview_only: Boolean(values.acknowledge_dedup_preview_only),
        acknowledge_no_production_dedup: Boolean(values.acknowledge_no_production_dedup),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_analysis: Boolean(values.acknowledge_no_analysis),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        created_by: 'sentigraph_local_ui',
      })
      setDedupPreviews(await listAnalysisRequestDedupPreviews(selectedRecord.request_id))
      setDedupGroupReviewAudits(await listAnalysisRequestDedupGroupReviewAudits(selectedRecord.request_id))
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Created dedup preview: ${preview.status}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create dedup preview.'
      setDedupPreviewError(String(messageText))
    } finally {
      setDedupPreviewLoading(false)
    }
  }

  async function handleDedupGroupReviewAction(group, action) {
    if (!selectedRecord?.request_id || !latestDedupPreview?.dedup_preview_id || !group?.group_candidate_id) return
    const values = dedupGroupReviewForm.getFieldsValue()
    const reviewerLabel = String(values.reviewer_label || '').trim()
    const note = String(values.note || '').trim()
    const splitItemIds = splitTags(values.split_item_ids)
    const representativeItemId = String(values.representative_item_id || group.representative_item_id || '').trim()
    if (!reviewerLabel || !note) {
      message.warning('Reviewer label and review note are required for dedup group review actions.')
      return
    }
    if (action === 'split_group' && !splitItemIds.length) {
      message.warning('split_group requires split item ids.')
      return
    }
    if (action === 'change_representative' && !representativeItemId) {
      message.warning('change_representative requires a representative item id.')
      return
    }
    setDedupGroupReviewLoading(`${group.group_candidate_id}:${action}`)
    setDedupGroupReviewError('')
    try {
      const result = await createAnalysisRequestDedupGroupReviewAction(
        selectedRecord.request_id,
        latestDedupPreview.dedup_preview_id,
        group.group_candidate_id,
        {
          action,
          target_group_candidate_id: group.group_candidate_id,
          reviewer_label: reviewerLabel,
          note,
          representative_item_id: action === 'change_representative' ? representativeItemId : undefined,
          split_item_ids: action === 'split_group' ? splitItemIds : [],
          acknowledge_review_only_group_action: Boolean(values.acknowledge_review_only_group_action),
          acknowledge_no_production_dedup: Boolean(values.acknowledge_no_production_dedup),
          acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
          acknowledge_no_analysis: Boolean(values.acknowledge_no_analysis),
          acknowledge_no_report: Boolean(values.acknowledge_no_report),
          write_evidence_layer_now: false,
          create_production_case_now: false,
          create_production_review_queue_now: false,
          run_production_dedup_now: false,
          run_analysis_now: false,
          generate_report_now: false,
          generate_sandbox_now: false,
          generate_public_event_now: false,
        },
      )
      setDedupPreviews(await listAnalysisRequestDedupPreviews(selectedRecord.request_id))
      setDedupGroupReviewAudits(await listAnalysisRequestDedupGroupReviewAudits(selectedRecord.request_id))
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      clearManualAnalysisTriggerState()
      message.success(`Recorded dedup group action: ${result?.new_group_status || action}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to record dedup group review action.'
      setDedupGroupReviewError(String(messageText))
    } finally {
      setDedupGroupReviewLoading('')
    }
  }

  async function handleCreateAnalysisReadyPromotionGate(values) {
    if (!selectedRecord?.request_id) return
    setAnalysisReadyPromotionGateLoading(true)
    setAnalysisReadyPromotionGateError('')
    try {
      const gate = await createAnalysisRequestAnalysisReadyPromotionGate(selectedRecord.request_id, {
        review_case_id: values.review_case_id || latestDedupPreview?.review_case_id || undefined,
        queue_init_id: values.queue_init_id || latestDedupPreview?.queue_init_id || undefined,
        completion_gate_id: values.completion_gate_id || latestDedupPreview?.completion_gate_id || undefined,
        dedup_preview_id: values.dedup_preview_id || latestDedupPreview?.dedup_preview_id || undefined,
        promotion_decision: values.promotion_decision || 'approve_for_future_manual_analysis_trigger',
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        coverage_limitations_acknowledged: Boolean(values.coverage_limitations_acknowledged),
        privacy_acknowledged: Boolean(values.privacy_acknowledged),
        weak_evidence_warning_acknowledged: Boolean(values.weak_evidence_warning_acknowledged),
        dedup_preview_warning_acknowledged: Boolean(values.dedup_preview_warning_acknowledged),
        provider_output_is_evidence_not_truth_acknowledged: Boolean(values.provider_output_is_evidence_not_truth_acknowledged),
        acknowledge_promotion_is_not_analysis: Boolean(values.acknowledge_promotion_is_not_analysis),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_production_dedup: Boolean(values.acknowledge_no_production_dedup),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        write_evidence_layer_now: false,
        create_production_case_now: false,
        create_production_review_queue_now: false,
        run_production_dedup_now: false,
        run_dedup_now: false,
        run_analysis_now: false,
        generate_report_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
        created_by: 'sentigraph_local_ui',
      })
      setAnalysisReadyPromotionGates(await listAnalysisRequestAnalysisReadyPromotionGates(selectedRecord.request_id))
      setPromotionDecisionAudits(await listAnalysisRequestPromotionDecisionAudits(selectedRecord.request_id))
      setManualAnalysisTriggers(await listAnalysisRequestManualAnalysisTriggers(selectedRecord.request_id))
      setManualAnalysisTriggerAudits(await listAnalysisRequestManualAnalysisTriggerAudits(selectedRecord.request_id))
      message.success(`Recorded promotion gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create analysis-ready promotion gate.'
      setAnalysisReadyPromotionGateError(String(messageText))
    } finally {
      setAnalysisReadyPromotionGateLoading(false)
    }
  }

  async function handleCreateManualAnalysisTrigger(values) {
    if (!selectedRecord?.request_id || !latestAnalysisReadyPromotionGate?.promotion_gate_id) return
    setManualAnalysisTriggerLoading(true)
    setManualAnalysisTriggerError('')
    try {
      const trigger = await createAnalysisRequestManualAnalysisTrigger(selectedRecord.request_id, {
        promotion_gate_id: values.promotion_gate_id || latestAnalysisReadyPromotionGate.promotion_gate_id,
        review_case_id: values.review_case_id || latestAnalysisReadyPromotionGate.review_case_id || undefined,
        trigger_decision: values.trigger_decision || 'trigger_analysis',
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        analysis_scope_mode: 'promotion_set_preview',
        coverage_acknowledged: Boolean(values.coverage_acknowledged),
        privacy_acknowledged: Boolean(values.privacy_acknowledged),
        weak_warning_acknowledged: Boolean(values.weak_warning_acknowledged),
        dedup_warning_acknowledged: Boolean(values.dedup_warning_acknowledged),
        provider_output_is_evidence_not_truth_acknowledged: Boolean(values.provider_output_is_evidence_not_truth_acknowledged),
        not_official_verification_acknowledged: Boolean(values.not_official_verification_acknowledged),
        not_full_web_coverage_acknowledged: Boolean(values.not_full_web_coverage_acknowledged),
        acknowledge_trigger_record_only: Boolean(values.acknowledge_trigger_record_only),
        acknowledge_no_analysis_run: Boolean(values.acknowledge_no_analysis_run),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_report: Boolean(values.acknowledge_no_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        write_evidence_layer_now: false,
        create_production_case_now: false,
        create_production_review_queue_now: false,
        run_production_dedup_now: false,
        run_dedup_now: false,
        run_analysis_now: false,
        generate_analysis_result_now: false,
        generate_report_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
      })
      setManualAnalysisTriggers(await listAnalysisRequestManualAnalysisTriggers(selectedRecord.request_id))
      setManualAnalysisTriggerAudits(await listAnalysisRequestManualAnalysisTriggerAudits(selectedRecord.request_id))
      setAnalysisResultBoundaryGates(await listAnalysisRequestAnalysisResultBoundaryGates(selectedRecord.request_id))
      setAnalysisResultBoundaryGateAudits(await listAnalysisRequestAnalysisResultBoundaryGateAudits(selectedRecord.request_id))
      setManualAnalysisExecutions([])
      setManualAnalysisResultCandidates([])
      setManualAnalysisExecutionAudits([])
      message.success(`Recorded manual trigger: ${trigger?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to record manual analysis trigger.'
      setManualAnalysisTriggerError(String(messageText))
    } finally {
      setManualAnalysisTriggerLoading(false)
    }
  }

  async function handleCreateAnalysisResultBoundaryGate(values) {
    if (!selectedRecord?.request_id || !latestManualAnalysisTrigger?.manual_trigger_id) return
    setAnalysisResultBoundaryGateLoading(true)
    setAnalysisResultBoundaryGateError('')
    try {
      const gate = await createAnalysisRequestAnalysisResultBoundaryGate(selectedRecord.request_id, {
        manual_trigger_id: values.manual_trigger_id || latestManualAnalysisTrigger.manual_trigger_id,
        promotion_gate_id: values.promotion_gate_id || latestManualAnalysisTrigger.promotion_gate_id,
        review_case_id: values.review_case_id || latestManualAnalysisTrigger.review_case_id || undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        coverage_limitation_acknowledged: Boolean(values.coverage_limitation_acknowledged),
        weak_evidence_warning_acknowledged: Boolean(values.weak_evidence_warning_acknowledged),
        rejected_evidence_exclusion_acknowledged: Boolean(values.rejected_evidence_exclusion_acknowledged),
        dedup_warning_acknowledged: Boolean(values.dedup_warning_acknowledged),
        provider_output_is_evidence_not_truth_acknowledged: Boolean(values.provider_output_is_evidence_not_truth_acknowledged),
        not_official_verification_acknowledged: Boolean(values.not_official_verification_acknowledged),
        not_full_web_coverage_acknowledged: Boolean(values.not_full_web_coverage_acknowledged),
        audit_trace_acknowledged: Boolean(values.audit_trace_acknowledged),
        acknowledge_boundary_gate_only: Boolean(values.acknowledge_boundary_gate_only),
        acknowledge_no_analysis_run: Boolean(values.acknowledge_no_analysis_run),
        acknowledge_no_analysis_result_generation: Boolean(values.acknowledge_no_analysis_result_generation),
        acknowledge_no_report_generation: Boolean(values.acknowledge_no_report_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        run_analysis_now: false,
        generate_analysis_result_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        run_production_dedup_now: false,
        generate_report_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        analysis_includes_rejected: false,
        duplicates_amplify_risk: false,
      })
      setAnalysisResultBoundaryGates(await listAnalysisRequestAnalysisResultBoundaryGates(selectedRecord.request_id))
      setAnalysisResultBoundaryGateAudits(await listAnalysisRequestAnalysisResultBoundaryGateAudits(selectedRecord.request_id))
      setManualAnalysisExecutions(await listAnalysisRequestManualAnalysisExecutions(selectedRecord.request_id))
      setManualAnalysisResultCandidates(await listAnalysisRequestManualAnalysisResultCandidates(selectedRecord.request_id))
      setManualAnalysisExecutionAudits(await listAnalysisRequestManualAnalysisExecutionAudits(selectedRecord.request_id))
      setReportGenerationGates([])
      setReportGenerationGateAudits([])
      message.success(`Recorded result boundary gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Analysis Result Boundary Gate.'
      setAnalysisResultBoundaryGateError(String(messageText))
    } finally {
      setAnalysisResultBoundaryGateLoading(false)
    }
  }

  async function handleCreateManualAnalysisExecution(values) {
    if (!selectedRecord?.request_id || !latestAnalysisResultBoundaryGate?.boundary_gate_id) return
    setManualAnalysisExecutionLoading(true)
    setManualAnalysisExecutionError('')
    try {
      const execution = await createAnalysisRequestManualAnalysisExecution(selectedRecord.request_id, {
        manual_trigger_id: values.manual_trigger_id || latestAnalysisResultBoundaryGate.manual_trigger_id,
        boundary_gate_id: values.boundary_gate_id || latestAnalysisResultBoundaryGate.boundary_gate_id,
        promotion_gate_id: values.promotion_gate_id || latestAnalysisResultBoundaryGate.promotion_gate_id,
        review_case_id: values.review_case_id || latestAnalysisResultBoundaryGate.review_case_id || undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        analysis_execution_mode: 'local_review_only_candidate',
        acknowledge_local_candidate_only: Boolean(values.acknowledge_local_candidate_only),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_no_report_generation: Boolean(values.acknowledge_no_report_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        write_evidence_layer_now: false,
        create_production_case_now: false,
        create_production_review_queue_now: false,
        run_production_dedup_now: false,
        run_analysis_now: false,
        generate_analysis_result_now: false,
        generate_report_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
        generate_b_end_report_now: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        real_api_call_requested: false,
        real_llm_call_requested: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        original_package_rows_read: false,
      })
      setManualAnalysisExecutions(await listAnalysisRequestManualAnalysisExecutions(selectedRecord.request_id))
      setManualAnalysisResultCandidates(await listAnalysisRequestManualAnalysisResultCandidates(selectedRecord.request_id))
      setManualAnalysisExecutionAudits(await listAnalysisRequestManualAnalysisExecutionAudits(selectedRecord.request_id))
      setReportGenerationGates(await listAnalysisRequestReportGenerationGates(selectedRecord.request_id))
      setReportGenerationGateAudits(await listAnalysisRequestReportGenerationGateAudits(selectedRecord.request_id))
      message.success(`Created local analysis candidate: ${execution?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create manual analysis execution candidate.'
      setManualAnalysisExecutionError(String(messageText))
    } finally {
      setManualAnalysisExecutionLoading(false)
    }
  }

  async function handleCreateReportGenerationGate(values) {
    if (!selectedRecord?.request_id || !latestManualAnalysisExecution?.manual_analysis_execution_id) return
    setReportGenerationGateLoading(true)
    setReportGenerationGateError('')
    try {
      const gate = await createAnalysisRequestReportGenerationGate(selectedRecord.request_id, {
        manual_analysis_execution_id:
          values.manual_analysis_execution_id || latestManualAnalysisExecution.manual_analysis_execution_id,
        result_candidate_id:
          values.result_candidate_id ||
          latestManualAnalysisResultCandidate?.result_candidate_id ||
          latestManualAnalysisExecution.candidate_result_id,
        boundary_gate_id: values.boundary_gate_id || latestManualAnalysisExecution.boundary_gate_id,
        review_case_id: values.review_case_id || latestManualAnalysisExecution.review_case_id || undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        requested_future_output: 'summary_report_candidate',
        acknowledge_gate_only: Boolean(values.acknowledge_gate_only),
        acknowledge_no_summary_report_generation: Boolean(values.acknowledge_no_summary_report_generation),
        acknowledge_no_b_end_report_generation: Boolean(values.acknowledge_no_b_end_report_generation),
        acknowledge_no_export_generation: Boolean(values.acknowledge_no_export_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        generate_summary_report_now: false,
        generate_report_now: false,
        generate_b_end_report_now: false,
        export_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
      })
      setReportGenerationGates(await listAnalysisRequestReportGenerationGates(selectedRecord.request_id))
      setReportGenerationGateAudits(await listAnalysisRequestReportGenerationGateAudits(selectedRecord.request_id))
      message.success(`Recorded report generation gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Report Generation Gate.'
      setReportGenerationGateError(String(messageText))
    } finally {
      setReportGenerationGateLoading(false)
    }
  }

  async function handleCreateSummaryReportCandidate(values) {
    if (!selectedRecord?.request_id || !latestReportGenerationGate?.report_gate_id) return
    setSummaryReportCandidateLoading(true)
    setSummaryReportCandidateError('')
    try {
      const candidate = await createAnalysisRequestSummaryReportCandidate(selectedRecord.request_id, {
        report_gate_id: values.report_gate_id || latestReportGenerationGate.report_gate_id,
        result_candidate_id:
          values.result_candidate_id ||
          latestManualAnalysisResultCandidate?.result_candidate_id ||
          latestReportGenerationGate.result_candidate_id,
        manual_analysis_execution_id:
          values.manual_analysis_execution_id ||
          latestManualAnalysisExecution?.manual_analysis_execution_id ||
          latestReportGenerationGate.manual_analysis_execution_id,
        boundary_gate_id:
          values.boundary_gate_id ||
          latestAnalysisResultBoundaryGate?.boundary_gate_id ||
          latestReportGenerationGate.boundary_gate_id,
        review_case_id:
          values.review_case_id ||
          latestReportGenerationGate.review_case_id ||
          latestManualAnalysisExecution?.review_case_id ||
          undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        candidate_mode: 'local_summary_report_candidate',
        acknowledge_candidate_only: Boolean(values.acknowledge_candidate_only),
        acknowledge_not_final_summary_report: Boolean(values.acknowledge_not_final_summary_report),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_export_generation: Boolean(values.acknowledge_no_export_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        final_report_now: false,
        b_end_report_now: false,
        export_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        claim_official_verification: false,
        claim_full_web_coverage: false,
        claim_full_platform_coverage: false,
        include_rejected_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
      })
      setSummaryReportCandidates(await listAnalysisRequestSummaryReportCandidates(selectedRecord.request_id))
      setSummaryReportCandidateAudits(await listAnalysisRequestSummaryReportCandidateAudits(selectedRecord.request_id))
      message.success(`Created Summary Report Candidate: ${candidate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Summary Report Candidate.'
      setSummaryReportCandidateError(String(messageText))
    } finally {
      setSummaryReportCandidateLoading(false)
    }
  }

  async function handleCreateFinalSummaryReportReviewGate(values) {
    if (!selectedRecord?.request_id || !latestSummaryReportCandidate?.summary_report_candidate_id) return
    setFinalSummaryReportReviewGateLoading(true)
    setFinalSummaryReportReviewGateError('')
    try {
      const requiredRevisions = String(values.required_revisions || '')
        .split(/\r?\n|,/)
        .map((item) => item.trim())
        .filter(Boolean)
      const gate = await createAnalysisRequestFinalSummaryReportReviewGate(selectedRecord.request_id, {
        summary_report_candidate_id: values.summary_report_candidate_id || latestSummaryReportCandidate.summary_report_candidate_id,
        report_gate_id: values.report_gate_id || latestSummaryReportCandidate.report_gate_id || latestReportGenerationGate?.report_gate_id,
        result_candidate_id:
          values.result_candidate_id ||
          latestSummaryReportCandidate.result_candidate_id ||
          latestManualAnalysisResultCandidate?.result_candidate_id,
        manual_analysis_execution_id:
          values.manual_analysis_execution_id ||
          latestSummaryReportCandidate.manual_analysis_execution_id ||
          latestManualAnalysisExecution?.manual_analysis_execution_id,
        boundary_gate_id:
          values.boundary_gate_id ||
          latestSummaryReportCandidate.boundary_gate_id ||
          latestAnalysisResultBoundaryGate?.boundary_gate_id,
        review_case_id:
          values.review_case_id ||
          latestSummaryReportCandidate.review_case_id ||
          latestReportGenerationGate?.review_case_id ||
          undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        review_decision: values.review_decision || 'approve_for_future_final_runtime',
        required_revisions: requiredRevisions,
        acknowledge_review_gate_only: Boolean(values.acknowledge_review_gate_only),
        acknowledge_no_final_summary_report_generation: Boolean(values.acknowledge_no_final_summary_report_generation),
        acknowledge_no_b_end_report_generation: Boolean(values.acknowledge_no_b_end_report_generation),
        acknowledge_no_export_generation: Boolean(values.acknowledge_no_export_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        final_report_now: false,
        final_summary_report_now: false,
        b_end_report_now: false,
        export_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        full_platform_coverage: false,
        full_thread_coverage: false,
      })
      setFinalSummaryReportReviewGates(await listAnalysisRequestFinalSummaryReportReviewGates(selectedRecord.request_id))
      setFinalSummaryReportReviewGateAudits(await listAnalysisRequestFinalSummaryReportReviewGateAudits(selectedRecord.request_id))
      message.success(`Created Final Summary Report Review Gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Final Summary Report Review Gate.'
      setFinalSummaryReportReviewGateError(String(messageText))
    } finally {
      setFinalSummaryReportReviewGateLoading(false)
    }
  }

  async function handleCreateFinalSummaryReport(values) {
    if (!selectedRecord?.request_id || !latestFinalSummaryReportReviewGate?.final_report_review_gate_id) return
    setFinalSummaryReportLoading(true)
    setFinalSummaryReportError('')
    try {
      const report = await createAnalysisRequestFinalSummaryReport(selectedRecord.request_id, {
        summary_report_candidate_id:
          values.summary_report_candidate_id ||
          latestFinalSummaryReportReviewGate.summary_report_candidate_id ||
          latestSummaryReportCandidate?.summary_report_candidate_id,
        final_report_review_gate_id:
          values.final_report_review_gate_id || latestFinalSummaryReportReviewGate.final_report_review_gate_id,
        report_gate_id:
          values.report_gate_id ||
          latestFinalSummaryReportReviewGate.report_gate_id ||
          latestSummaryReportCandidate?.report_gate_id,
        result_candidate_id:
          values.result_candidate_id ||
          latestFinalSummaryReportReviewGate.result_candidate_id ||
          latestSummaryReportCandidate?.result_candidate_id ||
          latestManualAnalysisResultCandidate?.result_candidate_id,
        manual_analysis_execution_id:
          values.manual_analysis_execution_id ||
          latestFinalSummaryReportReviewGate.manual_analysis_execution_id ||
          latestSummaryReportCandidate?.manual_analysis_execution_id ||
          latestManualAnalysisExecution?.manual_analysis_execution_id,
        boundary_gate_id:
          values.boundary_gate_id ||
          latestFinalSummaryReportReviewGate.boundary_gate_id ||
          latestSummaryReportCandidate?.boundary_gate_id ||
          latestAnalysisResultBoundaryGate?.boundary_gate_id,
        review_case_id:
          values.review_case_id ||
          latestFinalSummaryReportReviewGate.review_case_id ||
          latestSummaryReportCandidate?.review_case_id ||
          undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        acknowledge_local_final_summary_report_only: Boolean(values.acknowledge_local_final_summary_report_only),
        acknowledge_no_pdf_export: Boolean(values.acknowledge_no_pdf_export),
        acknowledge_no_markdown_export: Boolean(values.acknowledge_no_markdown_export),
        acknowledge_no_deck_export: Boolean(values.acknowledge_no_deck_export),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        pdf_export_now: false,
        markdown_export_now: false,
        deck_export_now: false,
        b_end_report_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        full_platform_coverage: false,
        full_thread_coverage: false,
      })
      setFinalSummaryReports(await listAnalysisRequestFinalSummaryReports(selectedRecord.request_id))
      setFinalSummaryReportAudits(await listAnalysisRequestFinalSummaryReportAudits(selectedRecord.request_id))
      message.success(`Created Final Summary Report: ${report?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Final Summary Report.'
      setFinalSummaryReportError(String(messageText))
    } finally {
      setFinalSummaryReportLoading(false)
    }
  }

  async function handleCreateFinalSummaryReportExportGate(values) {
    if (!selectedRecord?.request_id || !latestFinalSummaryReport?.final_summary_report_id) return
    setFinalSummaryReportExportGateLoading(true)
    setFinalSummaryReportExportGateError('')
    try {
      const requiredRevisions = String(values.required_revisions || '')
        .split(/\r?\n|,/)
        .map((item) => item.trim())
        .filter(Boolean)
      const gate = await createAnalysisRequestFinalSummaryReportExportGate(selectedRecord.request_id, {
        final_summary_report_id:
          values.final_summary_report_id || latestFinalSummaryReport.final_summary_report_id,
        final_summary_report_audit_id:
          values.final_summary_report_audit_id ||
          latestFinalSummaryReportAudit?.final_summary_report_audit_id ||
          undefined,
        summary_report_candidate_id:
          values.summary_report_candidate_id ||
          latestFinalSummaryReport.summary_report_candidate_id ||
          latestSummaryReportCandidate?.summary_report_candidate_id,
        final_report_review_gate_id:
          values.final_report_review_gate_id ||
          latestFinalSummaryReport.final_report_review_gate_id ||
          latestFinalSummaryReportReviewGate?.final_report_review_gate_id,
        report_gate_id:
          values.report_gate_id ||
          latestFinalSummaryReport.report_gate_id ||
          latestReportGenerationGate?.report_gate_id,
        result_candidate_id:
          values.result_candidate_id ||
          latestFinalSummaryReport.result_candidate_id ||
          latestManualAnalysisResultCandidate?.result_candidate_id,
        manual_analysis_execution_id:
          values.manual_analysis_execution_id ||
          latestFinalSummaryReport.manual_analysis_execution_id ||
          latestManualAnalysisExecution?.manual_analysis_execution_id,
        boundary_gate_id:
          values.boundary_gate_id ||
          latestFinalSummaryReport.boundary_gate_id ||
          latestAnalysisResultBoundaryGate?.boundary_gate_id,
        review_case_id:
          values.review_case_id ||
          latestFinalSummaryReport.review_case_id ||
          latestReviewOnlyCase?.review_case_id ||
          undefined,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        export_decision: values.export_decision,
        required_revisions: requiredRevisions,
        acknowledge_export_gate_only: Boolean(values.acknowledge_export_gate_only),
        acknowledge_no_markdown_file_now: Boolean(values.acknowledge_no_markdown_file_now),
        acknowledge_no_pdf_file_now: Boolean(values.acknowledge_no_pdf_file_now),
        acknowledge_no_pptx_file_now: Boolean(values.acknowledge_no_pptx_file_now),
        acknowledge_no_b_end_report_generation: Boolean(values.acknowledge_no_b_end_report_generation),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        markdown_file_now: false,
        pdf_file_now: false,
        pptx_file_now: false,
        b_end_report_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        full_platform_coverage: false,
        full_thread_coverage: false,
      })
      setFinalSummaryReportExportGates(await listAnalysisRequestFinalSummaryReportExportGates(selectedRecord.request_id))
      setFinalSummaryReportExportGateAudits(await listAnalysisRequestFinalSummaryReportExportGateAudits(selectedRecord.request_id))
      setFinalSummaryReportExportArtifacts(await listAnalysisRequestFinalSummaryReportExportArtifacts(selectedRecord.request_id))
      setFinalSummaryReportExportArtifactAudits(await listAnalysisRequestFinalSummaryReportExportArtifactAudits(selectedRecord.request_id))
      message.success(`Created Final Summary Report Export Gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Final Summary Report Export Gate.'
      setFinalSummaryReportExportGateError(String(messageText))
    } finally {
      setFinalSummaryReportExportGateLoading(false)
    }
  }

  async function handleCreateFinalSummaryReportExportArtifact(values) {
    if (!selectedRecord?.request_id || !latestFinalSummaryReportExportGate?.export_gate_id) return
    setFinalSummaryReportExportArtifactLoading(true)
    setFinalSummaryReportExportArtifactError('')
    try {
      const artifact = await createAnalysisRequestFinalSummaryReportExportArtifact(selectedRecord.request_id, {
        final_summary_report_id:
          values.final_summary_report_id ||
          latestFinalSummaryReportExportGate.final_summary_report_id ||
          latestFinalSummaryReport?.final_summary_report_id,
        export_gate_id: values.export_gate_id || latestFinalSummaryReportExportGate.export_gate_id,
        export_gate_audit_id:
          values.export_gate_audit_id ||
          latestFinalSummaryReportExportGateAudit?.export_gate_audit_id ||
          finalSummaryReportExportGateAudits[0]?.export_gate_audit_id,
        review_case_id:
          values.review_case_id ||
          latestFinalSummaryReportExportGate.review_case_id ||
          latestFinalSummaryReport?.review_case_id ||
          undefined,
        artifact_type: values.artifact_type,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        acknowledge_export_artifact_only: Boolean(values.acknowledge_export_artifact_only),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        b_end_report_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_original_rows_now: false,
        fetch_url_now: false,
        call_llm_now: false,
        include_rejected_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        full_platform_coverage: false,
        full_thread_coverage: false,
      })
      setFinalSummaryReportExportArtifacts(await listAnalysisRequestFinalSummaryReportExportArtifacts(selectedRecord.request_id))
      setFinalSummaryReportExportArtifactAudits(await listAnalysisRequestFinalSummaryReportExportArtifactAudits(selectedRecord.request_id))
      message.success(`Created local export artifact: ${artifact?.artifact_type || 'artifact'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Final Summary Report Export Artifact.'
      setFinalSummaryReportExportArtifactError(String(messageText))
    } finally {
      setFinalSummaryReportExportArtifactLoading(false)
    }
  }

  async function handleCreateReportExportDownloadPackageGate(values) {
    if (!selectedRecord?.request_id || !latestFinalSummaryReportExportArtifact?.export_artifact_id) return
    setReportExportDownloadPackageGateLoading(true)
    setReportExportDownloadPackageGateError('')
    try {
      const gate = await createAnalysisRequestReportExportDownloadPackageGate(selectedRecord.request_id, {
        export_artifact_id: values.export_artifact_id || latestFinalSummaryReportExportArtifact.export_artifact_id,
        export_artifact_audit_id:
          values.export_artifact_audit_id ||
          latestFinalSummaryReportExportArtifactAudit?.export_artifact_audit_id ||
          finalSummaryReportExportArtifactAudits[0]?.export_artifact_audit_id,
        final_summary_report_id:
          values.final_summary_report_id ||
          latestFinalSummaryReportExportArtifact.final_summary_report_id ||
          latestFinalSummaryReport?.final_summary_report_id,
        export_gate_id:
          values.export_gate_id ||
          latestFinalSummaryReportExportArtifact.export_gate_id ||
          latestFinalSummaryReportExportGate?.export_gate_id,
        review_case_id:
          values.review_case_id ||
          latestFinalSummaryReportExportArtifact.review_case_id ||
          latestFinalSummaryReportExportGate?.review_case_id ||
          latestFinalSummaryReport?.review_case_id,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        delivery_decision: values.delivery_decision,
        required_revisions: splitTags(values.required_revisions),
        acknowledge_download_package_gate_only: Boolean(values.acknowledge_download_package_gate_only),
        acknowledge_no_download_route_now: Boolean(values.acknowledge_no_download_route_now),
        acknowledge_no_package_or_zip_now: Boolean(values.acknowledge_no_package_or_zip_now),
        acknowledge_no_public_or_signed_url_now: Boolean(values.acknowledge_no_public_or_signed_url_now),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        download_route_now: false,
        zip_package_now: false,
        package_now: false,
        public_url_now: false,
        signed_url_now: false,
        b_end_report_now: false,
        sandbox_now: false,
        public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        read_runtime_file_content_now: false,
        read_original_rows_now: false,
        read_original_package_rows_now: false,
        call_llm_now: false,
        fetch_url_now: false,
        call_external_api_now: false,
        provider_execution_requested: false,
        collector_job_requested: false,
        include_rejected_evidence: false,
        include_privacy_hold_evidence: false,
        include_needs_more_source_evidence: false,
        remove_weak_warnings: false,
        duplicates_amplify_risk: false,
        provider_output_is_truth: false,
        official_verification: false,
        full_web_coverage: false,
        full_platform_coverage: false,
        full_thread_coverage: false,
      })
      setReportExportDownloadPackageGates(await listAnalysisRequestReportExportDownloadPackageGates(selectedRecord.request_id))
      setReportExportDownloadPackageGateAudits(await listAnalysisRequestReportExportDownloadPackageGateAudits(selectedRecord.request_id))
      message.success(`Created download/package gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create Report Export Download / Package Gate.'
      setReportExportDownloadPackageGateError(String(messageText))
    } finally {
      setReportExportDownloadPackageGateLoading(false)
    }
  }

  async function handleCreateReportExportDownloadPackageArtifact(values) {
    if (!selectedRecord?.request_id || !latestReportExportDownloadPackageGate?.download_package_gate_id) return
    setReportExportDownloadPackageArtifactLoading(true)
    setReportExportDownloadPackageArtifactError('')
    try {
      const artifact = await createAnalysisRequestReportExportDownloadPackageArtifact(selectedRecord.request_id, {
        download_package_gate_id: values.download_package_gate_id || latestReportExportDownloadPackageGate.download_package_gate_id,
        review_case_id:
          values.review_case_id ||
          latestReportExportDownloadPackageGate.review_case_id ||
          latestFinalSummaryReportExportArtifact?.review_case_id ||
          latestFinalSummaryReport?.review_case_id,
        package_mode: 'local_manifest_only',
        operator_label: String(values.operator_label || '').trim(),
        note: String(values.note || '').trim(),
        acknowledge_local_manifest_only: Boolean(values.acknowledge_local_manifest_only),
        acknowledge_no_download_route: Boolean(values.acknowledge_no_download_route),
        acknowledge_no_file_bytes: Boolean(values.acknowledge_no_file_bytes),
        acknowledge_no_zip: Boolean(values.acknowledge_no_zip),
        acknowledge_no_public_or_signed_url: Boolean(values.acknowledge_no_public_or_signed_url),
        acknowledge_no_runtime_file_exposure: Boolean(values.acknowledge_no_runtime_file_exposure),
        acknowledge_no_artifact_content_read: Boolean(values.acknowledge_no_artifact_content_read),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_weak_evidence_warning: Boolean(values.acknowledge_weak_evidence_warning),
        acknowledge_rejected_exclusion: Boolean(values.acknowledge_rejected_exclusion),
        acknowledge_dedup_no_risk_amplification: Boolean(values.acknowledge_dedup_no_risk_amplification),
        acknowledge_audit_trace_required: Boolean(values.acknowledge_audit_trace_required),
        create_download_route_now: false,
        return_file_bytes_now: false,
        generate_public_url_now: false,
        generate_signed_url_now: false,
        generate_zip_now: false,
        generate_binary_archive_now: false,
        expose_runtime_file_now: false,
        expose_absolute_path_now: false,
        copy_artifact_file_content_now: false,
        read_artifact_file_content_now: false,
        parse_artifact_file_content_now: false,
        generate_b_end_report_now: false,
        generate_sandbox_now: false,
        generate_public_event_now: false,
        write_evidence_layer_now: false,
        create_production_case_now: false,
        call_real_api_now: false,
        call_real_llm_now: false,
        fetch_url_now: false,
        scrape_now: false,
        read_original_package_rows_now: false,
      })
      setReportExportDownloadPackageArtifacts(await listAnalysisRequestReportExportDownloadPackageArtifacts(selectedRecord.request_id))
      setReportExportDownloadPackageArtifactAudits(await listAnalysisRequestReportExportDownloadPackageArtifactAudits(selectedRecord.request_id))
      message.success(`Created local manifest-only package artifact: ${artifact?.package_status || 'created'}`)
    } catch (requestError) {
      const messageText =
        requestError?.response?.data?.detail || requestError?.message || 'Unable to create Report Export Download / Package Artifact.'
      setReportExportDownloadPackageArtifactError(String(messageText))
    } finally {
      setReportExportDownloadPackageArtifactLoading(false)
    }
  }

  async function handleCreateReportExportPublicAccessExternalDeliveryGate(values) {
    if (!selectedRecord?.request_id || !latestReportExportDownloadPackageArtifact?.package_artifact_id) return
    setReportExportPublicAccessExternalDeliveryGateLoading(true)
    setReportExportPublicAccessExternalDeliveryGateError('')
    try {
      const gate = await createAnalysisRequestReportExportPublicAccessExternalDeliveryGate(selectedRecord.request_id, {
        package_artifact_id: values.package_artifact_id || latestReportExportDownloadPackageArtifact.package_artifact_id,
        download_package_gate_id:
          values.download_package_gate_id ||
          latestReportExportDownloadPackageArtifact.download_package_gate_id ||
          latestReportExportDownloadPackageGate?.download_package_gate_id,
        final_summary_report_id:
          values.final_summary_report_id ||
          latestReportExportDownloadPackageArtifact.final_summary_report_id ||
          latestFinalSummaryReport?.final_summary_report_id,
        review_case_id:
          values.review_case_id ||
          latestReportExportDownloadPackageArtifact.review_case_id ||
          latestReportExportDownloadPackageGate?.review_case_id ||
          latestFinalSummaryReport?.review_case_id,
        reviewer_label: String(values.reviewer_label || '').trim(),
        note: String(values.note || '').trim(),
        access_delivery_decision: values.access_delivery_decision,
        requested_future_access_modes: values.requested_future_access_modes || ['internal_handoff_future_candidate'],
        requested_future_delivery_modes: values.requested_future_delivery_modes || ['internal_handoff_future_candidate'],
        required_revisions: splitTags(values.required_revisions),
        acknowledge_gate_only: Boolean(values.acknowledge_gate_only),
        acknowledge_no_public_download_route: Boolean(values.acknowledge_no_public_download_route),
        acknowledge_no_file_byte_response: Boolean(values.acknowledge_no_file_byte_response),
        acknowledge_no_zip: Boolean(values.acknowledge_no_zip),
        acknowledge_no_public_or_signed_url: Boolean(values.acknowledge_no_public_or_signed_url),
        acknowledge_no_external_delivery: Boolean(values.acknowledge_no_external_delivery),
        acknowledge_no_email: Boolean(values.acknowledge_no_email),
        acknowledge_no_object_storage: Boolean(values.acknowledge_no_object_storage),
        acknowledge_no_portal_publication: Boolean(values.acknowledge_no_portal_publication),
        acknowledge_no_runtime_file_exposure: Boolean(values.acknowledge_no_runtime_file_exposure),
        acknowledge_no_manifest_content_exposure: Boolean(values.acknowledge_no_manifest_content_exposure),
        acknowledge_no_export_artifact_content_read: Boolean(values.acknowledge_no_export_artifact_content_read),
        acknowledge_no_b_end_report: Boolean(values.acknowledge_no_b_end_report),
        acknowledge_no_sandbox_or_public_event: Boolean(values.acknowledge_no_sandbox_or_public_event),
        acknowledge_no_evidence_layer_write: Boolean(values.acknowledge_no_evidence_layer_write),
        acknowledge_no_production_case: Boolean(values.acknowledge_no_production_case),
        acknowledge_provider_output_is_evidence_not_truth: Boolean(values.acknowledge_provider_output_is_evidence_not_truth),
        acknowledge_not_official_verification: Boolean(values.acknowledge_not_official_verification),
        acknowledge_not_full_web_coverage: Boolean(values.acknowledge_not_full_web_coverage),
        acknowledge_downstream_gates_required: Boolean(values.acknowledge_downstream_gates_required),
        creates_public_download_route_now: false,
        creates_file_byte_response_now: false,
        generates_public_url_now: false,
        generates_signed_url_now: false,
        performs_external_delivery_now: false,
        sends_email_now: false,
        uploads_to_object_storage_now: false,
        publishes_to_portal_now: false,
        exposes_runtime_file_now: false,
        exposes_absolute_path_now: false,
        exposes_manifest_file_content_now: false,
        exposes_export_artifact_content_now: false,
        reads_export_artifact_file_content_now: false,
        copies_export_artifact_content_now: false,
        generates_zip_now: false,
        generates_binary_archive_now: false,
        generates_b_end_report_now: false,
        generates_sandbox_now: false,
        generates_public_event_now: false,
        writes_evidence_layer_now: false,
        creates_production_case_now: false,
        calls_real_api_now: false,
        calls_real_llm_now: false,
        fetches_url_now: false,
        scrapes_now: false,
        reads_original_package_rows_now: false,
      })
      setReportExportPublicAccessExternalDeliveryGates(
        await listAnalysisRequestReportExportPublicAccessExternalDeliveryGates(selectedRecord.request_id),
      )
      setReportExportPublicAccessExternalDeliveryGateAudits(
        await listAnalysisRequestReportExportPublicAccessExternalDeliveryGateAudits(selectedRecord.request_id),
      )
      message.success(`Created public access / external delivery gate: ${gate?.gate_status || 'created'}`)
    } catch (requestError) {
      const messageText =
        requestError?.response?.data?.detail ||
        requestError?.message ||
        'Unable to create Report Export Public Access / External Delivery Gate.'
      setReportExportPublicAccessExternalDeliveryGateError(String(messageText))
    } finally {
      setReportExportPublicAccessExternalDeliveryGateLoading(false)
    }
  }

  async function copyText(text, successMessage) {
    try {
      await navigator.clipboard.writeText(text)
      message.success(successMessage)
    } catch {
      message.warning('当前浏览器不允许复制，请在 JSON 区域手动选择。')
    }
  }

  const columns = [
    {
      title: 'Request',
      dataIndex: 'request_id',
      key: 'request_id',
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Text strong>{record.request?.case_seed?.title || record.request_id}</Text>
          <Text type="secondary">{record.request_id}</Text>
          <Space wrap size={4}>
            <Tag>{record.request?.sampling_plan?.sample_strategy || 'stratified_public_sample'}</Tag>
            {(record.request?.sampling_plan?.platforms || []).slice(0, 3).map((platform) => (
              <Tag key={platform} color="cyan">{platform}</Tag>
            ))}
          </Space>
        </Space>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 190,
      render: (value) => <Text>{value || '-'}</Text>,
    },
    {
      title: 'Provider result',
      key: 'provider',
      width: 260,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Space wrap size={4}>
            {statusTag(record.provider_status || record.request_status)}
            {safetyTag(record.safety_status)}
          </Space>
          <Text type="secondary">{record.package_name || record.result_warning || '等待手动放入 result JSON'}</Text>
        </Space>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      width: 120,
      render: (_, record) => <Button onClick={() => handleOpen(record)}>查看</Button>,
    },
  ]

  const providerResult = selectedRecord?.provider_result
  const requestJson = selectedRecord?.request ? JSON.stringify(selectedRecord.request, null, 2) : ''
  const draftJson = caseDraft ? JSON.stringify(caseDraft, null, 2) : ''
  const importPlanJson = importPlan ? JSON.stringify(importPlan, null, 2) : ''
  const importPreviewJson = importPreview ? JSON.stringify(importPreview, null, 2) : ''
  const latestReviewDecision = reviewDecisions[0] || null
  const latestReviewDecisionJson = latestReviewDecision ? JSON.stringify(latestReviewDecision, null, 2) : ''
  const importJobGate = useMemo(
    () => importJobEligibility(importPreview, latestReviewDecision),
    [importPreview, latestReviewDecision],
  )
  const latestImportJob = importJobs[0] || null
  const latestImportJobJson = latestImportJob ? JSON.stringify(latestImportJob, null, 2) : ''
  const executionPreflightGate = useMemo(
    () => executionPreflightEligibility(latestImportJob, latestReviewDecision),
    [latestImportJob, latestReviewDecision],
  )
  const latestExecutionPreflight = executionPreflights[0] || null
  const latestExecutionPreflightJson = latestExecutionPreflight ? JSON.stringify(latestExecutionPreflight, null, 2) : ''
  const rowReaderGate = useMemo(
    () => rowReaderDryRunEligibility(latestExecutionPreflight),
    [latestExecutionPreflight],
  )
  const latestRowReaderDryRun = rowReaderDryRuns[0] || null
  const latestRowReaderDryRunJson = latestRowReaderDryRun ? JSON.stringify(latestRowReaderDryRun, null, 2) : ''
  const realPackagePreviewGate = useMemo(
    () => realPackageRowPreviewEligibility(latestExecutionPreflight, latestRowReaderDryRun, latestReviewDecision),
    [latestExecutionPreflight, latestRowReaderDryRun, latestReviewDecision],
  )
  const realPackagePreviewAcks = Form.useWatch([], realPackagePreviewForm) || {}
  const realPackagePreviewSubmitDisabled = useMemo(() => {
    if (!realPackagePreviewGate.eligible || realPackagePreviewLoading) return true
    return !(
      realPackagePreviewAcks.acknowledge_real_package_preview &&
      realPackagePreviewAcks.acknowledge_no_import &&
      realPackagePreviewAcks.acknowledge_preview_not_representative &&
      realPackagePreviewAcks.acknowledge_privacy_stop
    )
  }, [realPackagePreviewAcks, realPackagePreviewGate.eligible, realPackagePreviewLoading])
  const latestRealPackagePreview = realPackagePreviews[0] || null
  const latestRealPackagePreviewJson = latestRealPackagePreview ? JSON.stringify(latestRealPackagePreview, null, 2) : ''
  const reviewOnlyCaseGate = useMemo(
    () => reviewOnlyCaseEligibility(latestRealPackagePreview, latestReviewDecision),
    [latestRealPackagePreview, latestReviewDecision],
  )
  const latestReviewOnlyCase = reviewOnlyCases[0] || null
  const latestReviewOnlyCaseJson = latestReviewOnlyCase ? JSON.stringify(latestReviewOnlyCase, null, 2) : ''
  const watchedReviewOnlyCaseMode = Form.useWatch('target_case_mode', reviewOnlyCaseForm)
  const watchedReviewOnlyTargetCaseId = Form.useWatch('target_case_id', reviewOnlyCaseForm)
  const reviewOnlyCaseSubmitDisabled = useMemo(() => {
    if (!reviewOnlyCaseGate.eligible || reviewOnlyCaseLoading) return true
    if (watchedReviewOnlyCaseMode === 'existing_case_review_wrapper') {
      return !String(watchedReviewOnlyTargetCaseId || '').trim()
    }
    return false
  }, [reviewOnlyCaseGate.eligible, reviewOnlyCaseLoading, watchedReviewOnlyCaseMode, watchedReviewOnlyTargetCaseId])
  const latestStagingImport = stagingImports[0] || null
  const latestStagingImportJson = latestStagingImport ? JSON.stringify(latestStagingImport, null, 2) : ''
  const stagedCandidateBatchJson = stagedCandidateBatch ? JSON.stringify(stagedCandidateBatch, null, 2) : ''
  const stagingImportGate = useMemo(
    () => stagingImportEligibility(latestReviewOnlyCase, latestRealPackagePreview, latestReviewDecision, stagingImports),
    [latestReviewOnlyCase, latestRealPackagePreview, latestReviewDecision, stagingImports],
  )
  const stagingReviewAck = Form.useWatch('acknowledge_review_only_staging', stagingImportForm)
  const stagingNoEvidenceLayerAck = Form.useWatch('acknowledge_no_evidence_layer_write', stagingImportForm)
  const stagingNoProductionCaseAck = Form.useWatch('acknowledge_no_production_case', stagingImportForm)
  const stagingNoAnalysisAck = Form.useWatch('acknowledge_no_analysis', stagingImportForm)
  const stagingNoReportAck = Form.useWatch('acknowledge_no_report', stagingImportForm)
  const stagingImportSubmitDisabled = useMemo(() => {
    if (!stagingImportGate.eligible || stagingImportLoading) return true
    return !(
      stagingReviewAck &&
      stagingNoEvidenceLayerAck &&
      stagingNoProductionCaseAck &&
      stagingNoAnalysisAck &&
      stagingNoReportAck
    )
  }, [
    stagingImportGate.eligible,
    stagingImportLoading,
    stagingReviewAck,
    stagingNoEvidenceLayerAck,
    stagingNoProductionCaseAck,
    stagingNoAnalysisAck,
    stagingNoReportAck,
  ])
  const latestReviewQueueInitialization = reviewQueueInitializations[0] || null
  const latestReviewQueueInitializationJson = latestReviewQueueInitialization
    ? JSON.stringify(latestReviewQueueInitialization, null, 2)
    : ''
  const reviewQueueItemBatchJson = reviewQueueItemBatch ? JSON.stringify(reviewQueueItemBatch, null, 2) : ''
  const reviewQueueInitGate = useMemo(
    () => reviewQueueInitEligibility(
      latestReviewOnlyCase,
      latestStagingImport,
      latestReviewDecision,
      stagedCandidateBatch,
      reviewQueueInitializations,
    ),
    [latestReviewOnlyCase, latestStagingImport, latestReviewDecision, stagedCandidateBatch, reviewQueueInitializations],
  )
  const queueReviewAck = Form.useWatch('acknowledge_review_only_queue', reviewQueueInitForm)
  const queueNoEvidenceLayerAck = Form.useWatch('acknowledge_no_evidence_layer_write', reviewQueueInitForm)
  const queueNoProductionCaseAck = Form.useWatch('acknowledge_no_production_case', reviewQueueInitForm)
  const queueNoDedupAck = Form.useWatch('acknowledge_no_dedup', reviewQueueInitForm)
  const queueNoAnalysisAck = Form.useWatch('acknowledge_no_analysis', reviewQueueInitForm)
  const queueNoReportAck = Form.useWatch('acknowledge_no_report', reviewQueueInitForm)
  const reviewQueueInitSubmitDisabled = useMemo(() => {
    if (!reviewQueueInitGate.eligible || reviewQueueInitLoading) return true
    return !(
      queueReviewAck &&
      queueNoEvidenceLayerAck &&
      queueNoProductionCaseAck &&
      queueNoDedupAck &&
      queueNoAnalysisAck &&
      queueNoReportAck
    )
  }, [
    reviewQueueInitGate.eligible,
    reviewQueueInitLoading,
    queueReviewAck,
    queueNoEvidenceLayerAck,
    queueNoProductionCaseAck,
    queueNoDedupAck,
    queueNoAnalysisAck,
    queueNoReportAck,
  ])
  const reviewQueueActionValues = Form.useWatch([], reviewQueueActionForm) || {}
  const reviewQueueActionReady = useMemo(() => {
    return Boolean(
      String(reviewQueueActionValues.reviewer_label || '').trim() &&
        reviewQueueActionValues.acknowledge_review_only_action &&
        reviewQueueActionValues.acknowledge_no_evidence_layer_write &&
        reviewQueueActionValues.acknowledge_no_production_case &&
        reviewQueueActionValues.acknowledge_no_dedup &&
        reviewQueueActionValues.acknowledge_no_analysis &&
        reviewQueueActionValues.acknowledge_no_report,
    )
  }, [reviewQueueActionValues])
  const reviewQueueAuditsByItem = useMemo(() => {
    return reviewQueueActionAudits.reduce((acc, audit) => {
      const key = audit.review_item_id || 'unknown'
      if (!acc[key]) acc[key] = []
      acc[key].push(audit)
      return acc
    }, {})
  }, [reviewQueueActionAudits])
  const reviewQueueActionAuditsJson = reviewQueueActionAudits.length ? JSON.stringify(reviewQueueActionAudits, null, 2) : ''
  const latestReviewQueueCompletionGate = reviewQueueCompletionGates[0] || null
  const latestReviewQueueCompletionGateJson = latestReviewQueueCompletionGate
    ? JSON.stringify(latestReviewQueueCompletionGate, null, 2)
    : ''
  const reviewQueueCompletionGatesJson = reviewQueueCompletionGates.length
    ? JSON.stringify(reviewQueueCompletionGates, null, 2)
    : ''
  const reviewQueueCompletionValues = Form.useWatch([], reviewQueueCompletionGateForm) || {}
  const reviewQueueCompletionReady = useMemo(() => {
    return Boolean(
      latestReviewQueueInitialization?.queue_init_id &&
        reviewQueueCompletionValues.acknowledge_completion_is_not_dedup &&
        reviewQueueCompletionValues.acknowledge_completion_is_not_analysis &&
        reviewQueueCompletionValues.acknowledge_no_evidence_layer_write &&
        reviewQueueCompletionValues.acknowledge_no_production_case &&
        reviewQueueCompletionValues.acknowledge_no_report,
      )
  }, [latestReviewQueueInitialization?.queue_init_id, reviewQueueCompletionValues])
  const latestDedupPreview = dedupPreviews[0] || null
  const latestDedupPreviewJson = latestDedupPreview ? JSON.stringify(latestDedupPreview, null, 2) : ''
  const dedupPreviewsJson = dedupPreviews.length ? JSON.stringify(dedupPreviews, null, 2) : ''
  const dedupPreviewValues = Form.useWatch([], dedupPreviewForm) || {}
  const dedupPreviewReady = useMemo(() => {
    return Boolean(
      latestReviewQueueCompletionGate?.completion_gate_id &&
        latestReviewQueueCompletionGate?.status === 'complete_enough_for_future_dedup_preview' &&
        dedupPreviewValues.acknowledge_dedup_preview_only &&
        dedupPreviewValues.acknowledge_no_production_dedup &&
        dedupPreviewValues.acknowledge_no_evidence_layer_write &&
        dedupPreviewValues.acknowledge_no_analysis &&
        dedupPreviewValues.acknowledge_no_report,
    )
  }, [dedupPreviewValues, latestReviewQueueCompletionGate?.completion_gate_id, latestReviewQueueCompletionGate?.status])
  const dedupGroupReviewValues = Form.useWatch([], dedupGroupReviewForm) || {}
  const dedupGroupReviewReady = useMemo(() => {
    return Boolean(
      latestDedupPreview?.dedup_preview_id &&
        String(dedupGroupReviewValues.reviewer_label || '').trim() &&
        String(dedupGroupReviewValues.note || '').trim() &&
        dedupGroupReviewValues.acknowledge_review_only_group_action &&
        dedupGroupReviewValues.acknowledge_no_production_dedup &&
        dedupGroupReviewValues.acknowledge_no_evidence_layer_write &&
        dedupGroupReviewValues.acknowledge_no_analysis &&
        dedupGroupReviewValues.acknowledge_no_report,
    )
  }, [latestDedupPreview?.dedup_preview_id, dedupGroupReviewValues])
  const dedupGroupAuditsByGroup = useMemo(() => {
    return dedupGroupReviewAudits.reduce((acc, audit) => {
      const key = audit.group_candidate_id || 'unknown'
      if (!acc[key]) acc[key] = []
      acc[key].push(audit)
      return acc
    }, {})
  }, [dedupGroupReviewAudits])
  const dedupGroupReviewAuditsJson = dedupGroupReviewAudits.length
    ? JSON.stringify(dedupGroupReviewAudits, null, 2)
    : ''
  const latestAnalysisReadyPromotionGate = analysisReadyPromotionGates[0] || null
  const latestAnalysisReadyPromotionGateJson = latestAnalysisReadyPromotionGate
    ? JSON.stringify(latestAnalysisReadyPromotionGate, null, 2)
    : ''
  const analysisReadyPromotionGatesJson = analysisReadyPromotionGates.length
    ? JSON.stringify(analysisReadyPromotionGates, null, 2)
    : ''
  const promotionDecisionAuditsJson = promotionDecisionAudits.length
    ? JSON.stringify(promotionDecisionAudits, null, 2)
    : ''
  const latestManualAnalysisTrigger = manualAnalysisTriggers[0] || null
  const latestManualAnalysisTriggerJson = latestManualAnalysisTrigger
    ? JSON.stringify(latestManualAnalysisTrigger, null, 2)
    : ''
  const manualAnalysisTriggersJson = manualAnalysisTriggers.length
    ? JSON.stringify(manualAnalysisTriggers, null, 2)
    : ''
  const manualAnalysisTriggerAuditsJson = manualAnalysisTriggerAudits.length
    ? JSON.stringify(manualAnalysisTriggerAudits, null, 2)
    : ''
  const latestAnalysisResultBoundaryGate = analysisResultBoundaryGates[0] || null
  const latestAnalysisResultBoundaryGateJson = latestAnalysisResultBoundaryGate
    ? JSON.stringify(latestAnalysisResultBoundaryGate, null, 2)
    : ''
  const analysisResultBoundaryGatesJson = analysisResultBoundaryGates.length
    ? JSON.stringify(analysisResultBoundaryGates, null, 2)
    : ''
  const analysisResultBoundaryGateAuditsJson = analysisResultBoundaryGateAudits.length
    ? JSON.stringify(analysisResultBoundaryGateAudits, null, 2)
    : ''
  const latestManualAnalysisExecution = manualAnalysisExecutions[0] || null
  const latestManualAnalysisResultCandidate = manualAnalysisResultCandidates[0] || null
  const latestManualAnalysisExecutionJson = latestManualAnalysisExecution
    ? JSON.stringify(latestManualAnalysisExecution, null, 2)
    : ''
  const latestManualAnalysisResultCandidateJson = latestManualAnalysisResultCandidate
    ? JSON.stringify(latestManualAnalysisResultCandidate, null, 2)
    : ''
  const manualAnalysisExecutionsJson = manualAnalysisExecutions.length
    ? JSON.stringify(manualAnalysisExecutions, null, 2)
    : ''
  const manualAnalysisResultCandidatesJson = manualAnalysisResultCandidates.length
    ? JSON.stringify(manualAnalysisResultCandidates, null, 2)
    : ''
  const manualAnalysisExecutionAuditsJson = manualAnalysisExecutionAudits.length
    ? JSON.stringify(manualAnalysisExecutionAudits, null, 2)
    : ''
  const latestReportGenerationGate = reportGenerationGates[0] || null
  const latestReportGenerationGateJson = latestReportGenerationGate
    ? JSON.stringify(latestReportGenerationGate, null, 2)
    : ''
  const reportGenerationGatesJson = reportGenerationGates.length
    ? JSON.stringify(reportGenerationGates, null, 2)
    : ''
  const reportGenerationGateAuditsJson = reportGenerationGateAudits.length
    ? JSON.stringify(reportGenerationGateAudits, null, 2)
    : ''
  const latestSummaryReportCandidate = summaryReportCandidates[0] || null
  const latestSummaryReportCandidateJson = latestSummaryReportCandidate
    ? JSON.stringify(latestSummaryReportCandidate, null, 2)
    : ''
  const summaryReportCandidatesJson = summaryReportCandidates.length
    ? JSON.stringify(summaryReportCandidates, null, 2)
    : ''
  const summaryReportCandidateAuditsJson = summaryReportCandidateAudits.length
    ? JSON.stringify(summaryReportCandidateAudits, null, 2)
    : ''
  const latestFinalSummaryReportReviewGate = finalSummaryReportReviewGates[0] || null
  const latestFinalSummaryReportReviewGateJson = latestFinalSummaryReportReviewGate
    ? JSON.stringify(latestFinalSummaryReportReviewGate, null, 2)
    : ''
  const finalSummaryReportReviewGatesJson = finalSummaryReportReviewGates.length
    ? JSON.stringify(finalSummaryReportReviewGates, null, 2)
    : ''
  const finalSummaryReportReviewGateAuditsJson = finalSummaryReportReviewGateAudits.length
    ? JSON.stringify(finalSummaryReportReviewGateAudits, null, 2)
    : ''
  const latestFinalSummaryReport = finalSummaryReports[0] || null
  const latestFinalSummaryReportJson = latestFinalSummaryReport
    ? JSON.stringify(latestFinalSummaryReport, null, 2)
    : ''
  const finalSummaryReportsJson = finalSummaryReports.length
    ? JSON.stringify(finalSummaryReports, null, 2)
    : ''
  const finalSummaryReportAuditsJson = finalSummaryReportAudits.length
    ? JSON.stringify(finalSummaryReportAudits, null, 2)
    : ''
  const latestFinalSummaryReportAudit = finalSummaryReportAudits[0] || null
  const latestFinalSummaryReportExportGate = finalSummaryReportExportGates[0] || null
  const latestFinalSummaryReportExportGateJson = latestFinalSummaryReportExportGate
    ? JSON.stringify(latestFinalSummaryReportExportGate, null, 2)
    : ''
  const finalSummaryReportExportGatesJson = finalSummaryReportExportGates.length
    ? JSON.stringify(finalSummaryReportExportGates, null, 2)
    : ''
  const finalSummaryReportExportGateAuditsJson = finalSummaryReportExportGateAudits.length
    ? JSON.stringify(finalSummaryReportExportGateAudits, null, 2)
    : ''
  const latestFinalSummaryReportExportGateAudit = finalSummaryReportExportGateAudits[0] || null
  const latestFinalSummaryReportExportArtifact = finalSummaryReportExportArtifacts[0] || null
  const latestFinalSummaryReportExportArtifactJson = latestFinalSummaryReportExportArtifact
    ? JSON.stringify(latestFinalSummaryReportExportArtifact, null, 2)
    : ''
  const finalSummaryReportExportArtifactsJson = finalSummaryReportExportArtifacts.length
    ? JSON.stringify(finalSummaryReportExportArtifacts, null, 2)
    : ''
  const finalSummaryReportExportArtifactAuditsJson = finalSummaryReportExportArtifactAudits.length
    ? JSON.stringify(finalSummaryReportExportArtifactAudits, null, 2)
    : ''
  const latestFinalSummaryReportExportArtifactAudit = finalSummaryReportExportArtifactAudits[0] || null
  const latestReportExportDownloadPackageGate = reportExportDownloadPackageGates[0] || null
  const latestReportExportDownloadPackageGateJson = latestReportExportDownloadPackageGate
    ? JSON.stringify(latestReportExportDownloadPackageGate, null, 2)
    : ''
  const reportExportDownloadPackageGatesJson = reportExportDownloadPackageGates.length
    ? JSON.stringify(reportExportDownloadPackageGates, null, 2)
    : ''
  const reportExportDownloadPackageGateAuditsJson = reportExportDownloadPackageGateAudits.length
    ? JSON.stringify(reportExportDownloadPackageGateAudits, null, 2)
    : ''
  const latestReportExportDownloadPackageArtifact = reportExportDownloadPackageArtifacts[0] || null
  const latestReportExportDownloadPackageArtifactJson = latestReportExportDownloadPackageArtifact
    ? JSON.stringify(latestReportExportDownloadPackageArtifact, null, 2)
    : ''
  const reportExportDownloadPackageArtifactsJson = reportExportDownloadPackageArtifacts.length
    ? JSON.stringify(reportExportDownloadPackageArtifacts, null, 2)
    : ''
  const reportExportDownloadPackageArtifactAuditsJson = reportExportDownloadPackageArtifactAudits.length
    ? JSON.stringify(reportExportDownloadPackageArtifactAudits, null, 2)
    : ''
  const latestReportExportPublicAccessExternalDeliveryGate = reportExportPublicAccessExternalDeliveryGates[0] || null
  const latestReportExportPublicAccessExternalDeliveryGateJson = latestReportExportPublicAccessExternalDeliveryGate
    ? JSON.stringify(latestReportExportPublicAccessExternalDeliveryGate, null, 2)
    : ''
  const reportExportPublicAccessExternalDeliveryGatesJson = reportExportPublicAccessExternalDeliveryGates.length
    ? JSON.stringify(reportExportPublicAccessExternalDeliveryGates, null, 2)
    : ''
  const reportExportPublicAccessExternalDeliveryGateAuditsJson = reportExportPublicAccessExternalDeliveryGateAudits.length
    ? JSON.stringify(reportExportPublicAccessExternalDeliveryGateAudits, null, 2)
    : ''
  const analysisReadyPromotionGateValues = Form.useWatch([], analysisReadyPromotionGateForm) || {}
  const dedupGroupsNeedReview = useMemo(
    () => (latestDedupPreview?.groups || []).some((group) => !['confirmed', 'marked_weak', 'representative_changed', 'rejected'].includes(group.group_status)),
    [latestDedupPreview?.groups],
  )
  const analysisReadyPromotionReady = useMemo(() => {
    return Boolean(
      latestDedupPreview?.dedup_preview_id &&
        latestDedupPreview?.status === 'preview_ready' &&
        !dedupGroupsNeedReview &&
        String(analysisReadyPromotionGateValues.reviewer_label || '').trim() &&
        analysisReadyPromotionGateValues.coverage_limitations_acknowledged &&
        analysisReadyPromotionGateValues.privacy_acknowledged &&
        analysisReadyPromotionGateValues.weak_evidence_warning_acknowledged &&
        analysisReadyPromotionGateValues.dedup_preview_warning_acknowledged &&
        analysisReadyPromotionGateValues.provider_output_is_evidence_not_truth_acknowledged &&
        analysisReadyPromotionGateValues.acknowledge_promotion_is_not_analysis &&
        analysisReadyPromotionGateValues.acknowledge_no_evidence_layer_write &&
        analysisReadyPromotionGateValues.acknowledge_no_production_case &&
        analysisReadyPromotionGateValues.acknowledge_no_production_dedup &&
        analysisReadyPromotionGateValues.acknowledge_no_report,
    )
  }, [analysisReadyPromotionGateValues, dedupGroupsNeedReview, latestDedupPreview?.dedup_preview_id, latestDedupPreview?.status])
  const manualAnalysisTriggerValues = Form.useWatch([], manualAnalysisTriggerForm) || {}
  const manualAnalysisTriggerReady = useMemo(() => {
    return Boolean(
      latestAnalysisReadyPromotionGate?.promotion_gate_id &&
        latestAnalysisReadyPromotionGate?.status === 'eligible_for_future_manual_analysis_trigger' &&
        String(manualAnalysisTriggerValues.reviewer_label || '').trim() &&
        String(manualAnalysisTriggerValues.note || '').trim() &&
        manualAnalysisTriggerValues.coverage_acknowledged &&
        manualAnalysisTriggerValues.privacy_acknowledged &&
        manualAnalysisTriggerValues.weak_warning_acknowledged &&
        manualAnalysisTriggerValues.dedup_warning_acknowledged &&
        manualAnalysisTriggerValues.provider_output_is_evidence_not_truth_acknowledged &&
        manualAnalysisTriggerValues.not_official_verification_acknowledged &&
        manualAnalysisTriggerValues.not_full_web_coverage_acknowledged &&
        manualAnalysisTriggerValues.acknowledge_trigger_record_only &&
        manualAnalysisTriggerValues.acknowledge_no_analysis_run &&
        manualAnalysisTriggerValues.acknowledge_no_evidence_layer_write &&
        manualAnalysisTriggerValues.acknowledge_no_production_case &&
        manualAnalysisTriggerValues.acknowledge_no_report &&
        manualAnalysisTriggerValues.acknowledge_no_sandbox_or_public_event,
    )
  }, [latestAnalysisReadyPromotionGate?.promotion_gate_id, latestAnalysisReadyPromotionGate?.status, manualAnalysisTriggerValues])
  const analysisResultBoundaryGateValues = Form.useWatch([], analysisResultBoundaryGateForm) || {}
  const analysisResultBoundaryGateReady = useMemo(() => {
    return Boolean(
      latestManualAnalysisTrigger?.manual_trigger_id &&
        latestManualAnalysisTrigger?.status === 'trigger_recorded_ready_for_future_analysis_runtime' &&
        String(analysisResultBoundaryGateValues.reviewer_label || '').trim() &&
        String(analysisResultBoundaryGateValues.note || '').trim() &&
        analysisResultBoundaryGateValues.coverage_limitation_acknowledged &&
        analysisResultBoundaryGateValues.weak_evidence_warning_acknowledged &&
        analysisResultBoundaryGateValues.rejected_evidence_exclusion_acknowledged &&
        analysisResultBoundaryGateValues.dedup_warning_acknowledged &&
        analysisResultBoundaryGateValues.provider_output_is_evidence_not_truth_acknowledged &&
        analysisResultBoundaryGateValues.not_official_verification_acknowledged &&
        analysisResultBoundaryGateValues.not_full_web_coverage_acknowledged &&
        analysisResultBoundaryGateValues.audit_trace_acknowledged &&
        analysisResultBoundaryGateValues.acknowledge_boundary_gate_only &&
        analysisResultBoundaryGateValues.acknowledge_no_analysis_run &&
        analysisResultBoundaryGateValues.acknowledge_no_analysis_result_generation &&
        analysisResultBoundaryGateValues.acknowledge_no_report_generation &&
        analysisResultBoundaryGateValues.acknowledge_no_sandbox_or_public_event &&
        analysisResultBoundaryGateValues.acknowledge_no_evidence_layer_write &&
        analysisResultBoundaryGateValues.acknowledge_no_production_case,
    )
  }, [analysisResultBoundaryGateValues, latestManualAnalysisTrigger?.manual_trigger_id, latestManualAnalysisTrigger?.status])
  const manualAnalysisExecutionValues = Form.useWatch([], manualAnalysisExecutionForm) || {}
  const manualAnalysisExecutionReady = useMemo(() => {
    return Boolean(
      latestAnalysisResultBoundaryGate?.boundary_gate_id &&
        latestAnalysisResultBoundaryGate?.status === 'boundary_ready_for_future_analysis_result_runtime' &&
        String(manualAnalysisExecutionValues.reviewer_label || '').trim() &&
        String(manualAnalysisExecutionValues.note || '').trim() &&
        manualAnalysisExecutionValues.acknowledge_local_candidate_only &&
        manualAnalysisExecutionValues.acknowledge_no_evidence_layer_write &&
        manualAnalysisExecutionValues.acknowledge_no_production_case &&
        manualAnalysisExecutionValues.acknowledge_no_report_generation &&
        manualAnalysisExecutionValues.acknowledge_no_sandbox_or_public_event &&
        manualAnalysisExecutionValues.acknowledge_provider_output_is_evidence_not_truth &&
        manualAnalysisExecutionValues.acknowledge_not_official_verification &&
        manualAnalysisExecutionValues.acknowledge_not_full_web_coverage &&
        manualAnalysisExecutionValues.acknowledge_weak_evidence_warning &&
        manualAnalysisExecutionValues.acknowledge_rejected_exclusion &&
        manualAnalysisExecutionValues.acknowledge_dedup_no_risk_amplification,
    )
  }, [
    latestAnalysisResultBoundaryGate?.boundary_gate_id,
    latestAnalysisResultBoundaryGate?.status,
    manualAnalysisExecutionValues,
  ])
  const reportGenerationGateValues = Form.useWatch([], reportGenerationGateForm) || {}
  const reportGenerationGateReady = useMemo(() => {
    return Boolean(
      latestManualAnalysisExecution?.manual_analysis_execution_id &&
        latestManualAnalysisExecution?.status === 'analysis_result_candidate_created' &&
        latestManualAnalysisResultCandidate?.result_candidate_id &&
        String(reportGenerationGateValues.reviewer_label || '').trim() &&
        String(reportGenerationGateValues.note || '').trim() &&
        reportGenerationGateValues.acknowledge_gate_only &&
        reportGenerationGateValues.acknowledge_no_summary_report_generation &&
        reportGenerationGateValues.acknowledge_no_b_end_report_generation &&
        reportGenerationGateValues.acknowledge_no_export_generation &&
        reportGenerationGateValues.acknowledge_no_sandbox_or_public_event &&
        reportGenerationGateValues.acknowledge_no_evidence_layer_write &&
        reportGenerationGateValues.acknowledge_no_production_case &&
        reportGenerationGateValues.acknowledge_provider_output_is_evidence_not_truth &&
        reportGenerationGateValues.acknowledge_not_official_verification &&
        reportGenerationGateValues.acknowledge_not_full_web_coverage &&
        reportGenerationGateValues.acknowledge_weak_evidence_warning &&
        reportGenerationGateValues.acknowledge_rejected_exclusion &&
        reportGenerationGateValues.acknowledge_dedup_no_risk_amplification &&
        reportGenerationGateValues.acknowledge_audit_trace_required,
    )
  }, [
    latestManualAnalysisExecution?.manual_analysis_execution_id,
    latestManualAnalysisExecution?.status,
    latestManualAnalysisResultCandidate?.result_candidate_id,
    reportGenerationGateValues,
  ])
  const summaryReportCandidateValues = Form.useWatch([], summaryReportCandidateForm) || {}
  const summaryReportCandidateReady = useMemo(() => {
    return Boolean(
      latestReportGenerationGate?.report_gate_id &&
        latestReportGenerationGate?.status === 'report_gate_ready_for_future_runtime' &&
        latestManualAnalysisResultCandidate?.result_candidate_id &&
        String(summaryReportCandidateValues.reviewer_label || '').trim() &&
        String(summaryReportCandidateValues.note || '').trim() &&
        summaryReportCandidateValues.acknowledge_candidate_only &&
        summaryReportCandidateValues.acknowledge_not_final_summary_report &&
        summaryReportCandidateValues.acknowledge_no_b_end_report &&
        summaryReportCandidateValues.acknowledge_no_export_generation &&
        summaryReportCandidateValues.acknowledge_no_sandbox_or_public_event &&
        summaryReportCandidateValues.acknowledge_no_evidence_layer_write &&
        summaryReportCandidateValues.acknowledge_no_production_case &&
        summaryReportCandidateValues.acknowledge_provider_output_is_evidence_not_truth &&
        summaryReportCandidateValues.acknowledge_not_official_verification &&
        summaryReportCandidateValues.acknowledge_not_full_web_coverage &&
        summaryReportCandidateValues.acknowledge_weak_evidence_warning &&
        summaryReportCandidateValues.acknowledge_rejected_exclusion &&
        summaryReportCandidateValues.acknowledge_dedup_no_risk_amplification &&
        summaryReportCandidateValues.acknowledge_audit_trace_required,
    )
  }, [
    latestManualAnalysisResultCandidate?.result_candidate_id,
    latestReportGenerationGate?.report_gate_id,
    latestReportGenerationGate?.status,
    summaryReportCandidateValues,
  ])
  const finalSummaryReportReviewGateValues = Form.useWatch([], finalSummaryReportReviewGateForm) || {}
  const finalSummaryReportReviewGateReady = useMemo(() => {
    const requiresRevisionText =
      finalSummaryReportReviewGateValues.review_decision === 'request_revision'
        ? String(finalSummaryReportReviewGateValues.required_revisions || '').trim()
        : true
    return Boolean(
      latestSummaryReportCandidate?.summary_report_candidate_id &&
        latestSummaryReportCandidate?.status === 'summary_report_candidate_created' &&
        String(finalSummaryReportReviewGateValues.reviewer_label || '').trim() &&
        String(finalSummaryReportReviewGateValues.note || '').trim() &&
        finalSummaryReportReviewGateValues.review_decision &&
        requiresRevisionText &&
        finalSummaryReportReviewGateValues.acknowledge_review_gate_only &&
        finalSummaryReportReviewGateValues.acknowledge_no_final_summary_report_generation &&
        finalSummaryReportReviewGateValues.acknowledge_no_b_end_report_generation &&
        finalSummaryReportReviewGateValues.acknowledge_no_export_generation &&
        finalSummaryReportReviewGateValues.acknowledge_no_sandbox_or_public_event &&
        finalSummaryReportReviewGateValues.acknowledge_no_evidence_layer_write &&
        finalSummaryReportReviewGateValues.acknowledge_no_production_case &&
        finalSummaryReportReviewGateValues.acknowledge_provider_output_is_evidence_not_truth &&
        finalSummaryReportReviewGateValues.acknowledge_not_official_verification &&
        finalSummaryReportReviewGateValues.acknowledge_not_full_web_coverage &&
        finalSummaryReportReviewGateValues.acknowledge_weak_evidence_warning &&
        finalSummaryReportReviewGateValues.acknowledge_rejected_exclusion &&
        finalSummaryReportReviewGateValues.acknowledge_dedup_no_risk_amplification &&
        finalSummaryReportReviewGateValues.acknowledge_audit_trace_required,
    )
  }, [
    finalSummaryReportReviewGateValues,
    latestSummaryReportCandidate?.status,
    latestSummaryReportCandidate?.summary_report_candidate_id,
  ])
  const finalSummaryReportValues = Form.useWatch([], finalSummaryReportForm) || {}
  const finalSummaryReportReady = useMemo(() => {
    return Boolean(
      latestFinalSummaryReportReviewGate?.final_report_review_gate_id &&
        latestFinalSummaryReportReviewGate?.status === 'ready_for_future_final_summary_report_runtime' &&
        String(finalSummaryReportValues.reviewer_label || '').trim() &&
        String(finalSummaryReportValues.note || '').trim() &&
        finalSummaryReportValues.acknowledge_local_final_summary_report_only &&
        finalSummaryReportValues.acknowledge_no_pdf_export &&
        finalSummaryReportValues.acknowledge_no_markdown_export &&
        finalSummaryReportValues.acknowledge_no_deck_export &&
        finalSummaryReportValues.acknowledge_no_b_end_report &&
        finalSummaryReportValues.acknowledge_no_sandbox_or_public_event &&
        finalSummaryReportValues.acknowledge_no_evidence_layer_write &&
        finalSummaryReportValues.acknowledge_no_production_case &&
        finalSummaryReportValues.acknowledge_provider_output_is_evidence_not_truth &&
        finalSummaryReportValues.acknowledge_not_official_verification &&
        finalSummaryReportValues.acknowledge_not_full_web_coverage &&
        finalSummaryReportValues.acknowledge_weak_evidence_warning &&
        finalSummaryReportValues.acknowledge_rejected_exclusion &&
        finalSummaryReportValues.acknowledge_dedup_no_risk_amplification &&
        finalSummaryReportValues.acknowledge_audit_trace_required,
    )
  }, [
    finalSummaryReportValues,
    latestFinalSummaryReportReviewGate?.final_report_review_gate_id,
    latestFinalSummaryReportReviewGate?.status,
  ])
  const finalSummaryReportExportGateValues = Form.useWatch([], finalSummaryReportExportGateForm) || {}
  const finalSummaryReportExportGateReady = useMemo(() => {
    const requiresRevisionText =
      finalSummaryReportExportGateValues.export_decision === 'request_revision'
        ? String(finalSummaryReportExportGateValues.required_revisions || '').trim()
        : true
    return Boolean(
      latestFinalSummaryReport?.final_summary_report_id &&
        latestFinalSummaryReport?.status === 'final_summary_report_created' &&
        latestFinalSummaryReportAudit?.final_summary_report_audit_id &&
        String(finalSummaryReportExportGateValues.reviewer_label || '').trim() &&
        String(finalSummaryReportExportGateValues.note || '').trim() &&
        finalSummaryReportExportGateValues.export_decision &&
        requiresRevisionText &&
        finalSummaryReportExportGateValues.acknowledge_export_gate_only &&
        finalSummaryReportExportGateValues.acknowledge_no_markdown_file_now &&
        finalSummaryReportExportGateValues.acknowledge_no_pdf_file_now &&
        finalSummaryReportExportGateValues.acknowledge_no_pptx_file_now &&
        finalSummaryReportExportGateValues.acknowledge_no_b_end_report_generation &&
        finalSummaryReportExportGateValues.acknowledge_no_sandbox_or_public_event &&
        finalSummaryReportExportGateValues.acknowledge_no_evidence_layer_write &&
        finalSummaryReportExportGateValues.acknowledge_no_production_case &&
        finalSummaryReportExportGateValues.acknowledge_provider_output_is_evidence_not_truth &&
        finalSummaryReportExportGateValues.acknowledge_not_official_verification &&
        finalSummaryReportExportGateValues.acknowledge_not_full_web_coverage &&
        finalSummaryReportExportGateValues.acknowledge_weak_evidence_warning &&
        finalSummaryReportExportGateValues.acknowledge_rejected_exclusion &&
        finalSummaryReportExportGateValues.acknowledge_dedup_no_risk_amplification &&
        finalSummaryReportExportGateValues.acknowledge_audit_trace_required,
    )
  }, [
    finalSummaryReportExportGateValues,
    latestFinalSummaryReport?.final_summary_report_id,
    latestFinalSummaryReport?.status,
    latestFinalSummaryReportAudit?.final_summary_report_audit_id,
  ])
  const finalSummaryReportExportArtifactValues = Form.useWatch([], finalSummaryReportExportArtifactForm) || {}
  const finalSummaryReportExportArtifactReady = useMemo(() => {
    return Boolean(
      latestFinalSummaryReportExportGate?.export_gate_id &&
        latestFinalSummaryReportExportGate?.status === 'ready_for_future_export_runtime' &&
        latestFinalSummaryReportExportGateAudit?.export_gate_audit_id &&
        String(finalSummaryReportExportArtifactValues.reviewer_label || '').trim() &&
        String(finalSummaryReportExportArtifactValues.note || '').trim() &&
        finalSummaryReportExportArtifactValues.artifact_type &&
        finalSummaryReportExportArtifactValues.acknowledge_export_artifact_only &&
        finalSummaryReportExportArtifactValues.acknowledge_no_b_end_report &&
        finalSummaryReportExportArtifactValues.acknowledge_no_sandbox_or_public_event &&
        finalSummaryReportExportArtifactValues.acknowledge_no_evidence_layer_write &&
        finalSummaryReportExportArtifactValues.acknowledge_no_production_case &&
        finalSummaryReportExportArtifactValues.acknowledge_provider_output_is_evidence_not_truth &&
        finalSummaryReportExportArtifactValues.acknowledge_not_official_verification &&
        finalSummaryReportExportArtifactValues.acknowledge_not_full_web_coverage &&
        finalSummaryReportExportArtifactValues.acknowledge_weak_evidence_warning &&
        finalSummaryReportExportArtifactValues.acknowledge_rejected_exclusion &&
        finalSummaryReportExportArtifactValues.acknowledge_dedup_no_risk_amplification &&
        finalSummaryReportExportArtifactValues.acknowledge_audit_trace_required,
    )
  }, [
    finalSummaryReportExportArtifactValues,
    latestFinalSummaryReportExportGate?.export_gate_id,
    latestFinalSummaryReportExportGate?.status,
    latestFinalSummaryReportExportGateAudit?.export_gate_audit_id,
  ])
  const reportExportDownloadPackageGateValues = Form.useWatch([], reportExportDownloadPackageGateForm) || {}
  const reportExportDownloadPackageGateReady = useMemo(() => {
    const requiresRevisionText =
      reportExportDownloadPackageGateValues.delivery_decision === 'request_revision'
        ? String(reportExportDownloadPackageGateValues.required_revisions || '').trim()
        : true
    return Boolean(
      latestFinalSummaryReportExportArtifact?.export_artifact_id &&
        latestFinalSummaryReportExportArtifact?.status === 'export_artifact_created' &&
        latestFinalSummaryReportExportArtifactAudit?.export_artifact_audit_id &&
        String(reportExportDownloadPackageGateValues.reviewer_label || '').trim() &&
        String(reportExportDownloadPackageGateValues.note || '').trim() &&
        reportExportDownloadPackageGateValues.delivery_decision &&
        requiresRevisionText &&
        reportExportDownloadPackageGateValues.acknowledge_download_package_gate_only &&
        reportExportDownloadPackageGateValues.acknowledge_no_download_route_now &&
        reportExportDownloadPackageGateValues.acknowledge_no_package_or_zip_now &&
        reportExportDownloadPackageGateValues.acknowledge_no_public_or_signed_url_now &&
        reportExportDownloadPackageGateValues.acknowledge_no_b_end_report &&
        reportExportDownloadPackageGateValues.acknowledge_no_sandbox_or_public_event &&
        reportExportDownloadPackageGateValues.acknowledge_no_evidence_layer_write &&
        reportExportDownloadPackageGateValues.acknowledge_no_production_case &&
        reportExportDownloadPackageGateValues.acknowledge_provider_output_is_evidence_not_truth &&
        reportExportDownloadPackageGateValues.acknowledge_not_official_verification &&
        reportExportDownloadPackageGateValues.acknowledge_not_full_web_coverage &&
        reportExportDownloadPackageGateValues.acknowledge_weak_evidence_warning &&
        reportExportDownloadPackageGateValues.acknowledge_rejected_exclusion &&
        reportExportDownloadPackageGateValues.acknowledge_dedup_no_risk_amplification &&
        reportExportDownloadPackageGateValues.acknowledge_audit_trace_required,
    )
  }, [
    latestFinalSummaryReportExportArtifact?.export_artifact_id,
    latestFinalSummaryReportExportArtifact?.status,
    latestFinalSummaryReportExportArtifactAudit?.export_artifact_audit_id,
    reportExportDownloadPackageGateValues,
  ])
  const reportExportDownloadPackageArtifactValues = Form.useWatch([], reportExportDownloadPackageArtifactForm) || {}
  const reportExportDownloadPackageArtifactReady = useMemo(() => {
    return Boolean(
      latestReportExportDownloadPackageGate?.download_package_gate_id &&
        latestReportExportDownloadPackageGate?.status === 'ready_for_future_download_package_runtime' &&
        String(reportExportDownloadPackageArtifactValues.operator_label || '').trim() &&
        String(reportExportDownloadPackageArtifactValues.note || '').trim() &&
        reportExportDownloadPackageArtifactValues.acknowledge_local_manifest_only &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_download_route &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_file_bytes &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_zip &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_public_or_signed_url &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_runtime_file_exposure &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_artifact_content_read &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_b_end_report &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_sandbox_or_public_event &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_evidence_layer_write &&
        reportExportDownloadPackageArtifactValues.acknowledge_no_production_case &&
        reportExportDownloadPackageArtifactValues.acknowledge_provider_output_is_evidence_not_truth &&
        reportExportDownloadPackageArtifactValues.acknowledge_not_official_verification &&
        reportExportDownloadPackageArtifactValues.acknowledge_not_full_web_coverage &&
        reportExportDownloadPackageArtifactValues.acknowledge_weak_evidence_warning &&
        reportExportDownloadPackageArtifactValues.acknowledge_rejected_exclusion &&
        reportExportDownloadPackageArtifactValues.acknowledge_dedup_no_risk_amplification &&
        reportExportDownloadPackageArtifactValues.acknowledge_audit_trace_required,
    )
  }, [
    latestReportExportDownloadPackageGate?.download_package_gate_id,
    latestReportExportDownloadPackageGate?.status,
    reportExportDownloadPackageArtifactValues,
  ])
  const reportExportPublicAccessExternalDeliveryGateValues =
    Form.useWatch([], reportExportPublicAccessExternalDeliveryGateForm) || {}
  const reportExportPublicAccessExternalDeliveryGateReady = useMemo(() => {
    const requiresRevisionText =
      reportExportPublicAccessExternalDeliveryGateValues.access_delivery_decision === 'request_revision'
        ? String(reportExportPublicAccessExternalDeliveryGateValues.required_revisions || '').trim()
        : true
    return Boolean(
      latestReportExportDownloadPackageArtifact?.package_artifact_id &&
        latestReportExportDownloadPackageArtifact?.package_status === 'local_manifest_ready' &&
        String(reportExportPublicAccessExternalDeliveryGateValues.reviewer_label || '').trim() &&
        String(reportExportPublicAccessExternalDeliveryGateValues.note || '').trim() &&
        reportExportPublicAccessExternalDeliveryGateValues.access_delivery_decision &&
        requiresRevisionText &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_gate_only &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_public_download_route &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_file_byte_response &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_zip &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_public_or_signed_url &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_external_delivery &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_email &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_object_storage &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_portal_publication &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_runtime_file_exposure &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_manifest_content_exposure &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_export_artifact_content_read &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_b_end_report &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_sandbox_or_public_event &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_evidence_layer_write &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_no_production_case &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_provider_output_is_evidence_not_truth &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_not_official_verification &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_not_full_web_coverage &&
        reportExportPublicAccessExternalDeliveryGateValues.acknowledge_downstream_gates_required,
    )
  }, [
    latestReportExportDownloadPackageArtifact?.package_artifact_id,
    latestReportExportDownloadPackageArtifact?.package_status,
    reportExportPublicAccessExternalDeliveryGateValues,
  ])
  const requestPath = selectedRecord?.request_file || 'runtime/analysis_requests/requests/<request_id>.json'

  return (
    <div className="page-stack analysis-requests-page">
      <section className="external-collector-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">file-based MVP</Tag>
            <Tag color="default">provider-agnostic</Tag>
            <Tag color="default">no provider execution</Tag>
          </Space>
          <Title level={1}>Analysis Requests / 分析任务请求</Title>
          <Paragraph>
            创建本地 <Text code>sentigraph_analysis_request_v1</Text> JSON，读取手动放入的{' '}
            <Text code>sentigraph_provider_job_result_v1</Text>，并在 package metadata 合格时生成本地 case draft
            handoff 与 Evidence 导入计划。本页不会运行 collector，不会导入 Evidence rows，不会创建正式 case，不会抓取 URL，不会调用真实 API，也不会生成分析或报告。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<RefreshCw size={16} />} loading={loading} onClick={() => loadRequests()}>
              刷新本地请求
            </Button>
            <Tag color={config?.configured_by_env ? 'blue' : 'default'}>
              {config?.configured_by_env ? 'custom local dir' : 'repo runtime dir'}
            </Tag>
            <Tag>{config?.root_label || 'runtime/analysis_requests'}</Tag>
          </Space>
        </div>
        <Card className="panel-card external-collector-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Local requests</Text>
            <Title level={2}>{config?.request_count ?? requests.length}</Title>
            <Text type="secondary">Provider results: {config?.result_count ?? 0}</Text>
            <Text type="secondary">Env: SENTIGRAPH_ANALYSIS_REQUESTS_DIR</Text>
          </Space>
        </Card>
      </section>

      <Alert
        type="info"
        showIcon
        message="Boundary / 边界"
        description={
          <Space wrap>
            {BOUNDARY_TAGS.map((item) => (
              <Tag key={item}>{item}</Tag>
            ))}
          </Space>
        }
      />
      <Alert
        type="warning"
        showIcon
        message="Provider output is evidence, not official truth"
        description="Case draft 和 Evidence 导入计划都不是正式导入、官方验证、分析结果、报告、公开事件页或 Sandbox fixture。Evidence rows 需要后续人工导入与复核。"
      />
      {error ? <Alert type="error" showIcon message={error} /> : null}

      <Row gutter={[16, 16]}>
        <Col span={9}>
          <Card className="panel-card" title="创建分析请求">
            <Form
              form={form}
              layout="vertical"
              initialValues={DEFAULT_FORM_VALUES}
              onFinish={handleCreate}
            >
              <Form.Item name="title" label="事件标题" rules={[{ required: true, message: '请输入事件标题' }]}>
                <Input placeholder="例如：董路 / 孙继海青训争议" />
              </Form.Item>
              <Form.Item name="description" label="事件描述">
                <TextArea rows={3} placeholder="简要说明事件背景和分析目的" />
              </Form.Item>
              <Form.Item name="keywords" label="关键词">
                <Select mode="tags" tokenSeparators={[',']} placeholder="董路, 孙继海, 青训" />
              </Form.Item>
              <Form.Item name="negative_keywords" label="排除关键词">
                <Select mode="tags" tokenSeparators={[',']} placeholder="广告, 无关" />
              </Form.Item>
              <Form.Item name="language" label="语言">
                <Select mode="tags" tokenSeparators={[',']} options={[
                  { value: 'zh-CN', label: 'zh-CN' },
                  { value: 'en', label: 'en' },
                  { value: 'auto', label: 'auto' },
                ]} />
              </Form.Item>
              <Form.Item name="event_type" label="事件类型">
                <Select options={[
                  { value: 'public_opinion_demo', label: 'public_opinion_demo' },
                  { value: 'public_opinion_event', label: 'public_opinion_event' },
                  { value: 'brand_risk_event', label: 'brand_risk_event' },
                  { value: 'creator_community_event', label: 'creator_community_event' },
                ]} />
              </Form.Item>
              <Form.Item name="platforms" label="目标平台 / source hint">
                <Select mode="tags" tokenSeparators={[',']} placeholder="weibo, bilibili, tieba" />
              </Form.Item>
              <Row gutter={10}>
                <Col span={8}>
                  <Form.Item name="target_comment_count" label="评论目标">
                    <InputNumber min={0} max={100000} className="full-width" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="target_source_count" label="来源目标">
                    <InputNumber min={0} max={10000} className="full-width" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="max_runtime_minutes" label="分钟预算">
                    <InputNumber min={1} max={1440} className="full-width" />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item name="sample_strategy" label="采样策略">
                <Select options={[
                  { value: 'stratified_public_sample', label: 'stratified_public_sample' },
                  { value: 'manual_snapshot', label: 'manual_snapshot' },
                  { value: 'provider_selected_sample', label: 'provider_selected_sample' },
                ]} />
              </Form.Item>
              <Card size="small" title="Safety policy">
                <Form.Item name="allow_manual_snapshot" valuePropName="checked">
                  <Checkbox>允许 manual snapshot</Checkbox>
                </Form.Item>
                <Form.Item name="allow_official_api" valuePropName="checked">
                  <Checkbox>允许已批准 official API</Checkbox>
                </Form.Item>
                <Form.Item name="allow_vendor_api" valuePropName="checked">
                  <Checkbox>允许已合规 vendor API</Checkbox>
                </Form.Item>
                <Form.Item name="allow_live_collection" valuePropName="checked">
                  <Checkbox>允许 live collection（默认关闭，仅作为请求字段）</Checkbox>
                </Form.Item>
                <Form.Item name="allow_saved_profile" valuePropName="checked">
                  <Checkbox>允许 saved profile（默认关闭，Sentigraph 不存储）</Checkbox>
                </Form.Item>
                <Form.Item name="minor_sensitive_mode" valuePropName="checked">
                  <Checkbox>minor_sensitive_mode</Checkbox>
                </Form.Item>
              </Card>
              <Space className="form-actions" wrap>
                <Button type="primary" htmlType="submit" loading={creating}>
                  创建分析请求
                </Button>
                <Button onClick={() => form.resetFields()}>重置</Button>
              </Space>
            </Form>
          </Card>
        </Col>

        <Col span={15}>
          <Card className="panel-card" title="本地请求列表">
            <Table
              rowKey="request_id"
              columns={columns}
              dataSource={requests}
              loading={loading}
              pagination={{ pageSize: 6 }}
              locale={{ emptyText: <Empty description="暂无本地 analysis request JSON" /> }}
            />
          </Card>

          <Card className="panel-card" title="Request / Provider result detail">
            {selectedRecord ? (
              <Space direction="vertical" size={14} className="full-width">
                <Space wrap>
                  <Tag color="cyan">{selectedRecord.request_id}</Tag>
                  {statusTag(selectedRecord.provider_status || selectedRecord.request_status)}
                  {safetyTag(selectedRecord.safety_status)}
                  {selectedRecord.package_name ? <Tag color="blue">{selectedRecord.package_name}</Tag> : null}
                </Space>
                <Row gutter={[12, 12]}>
                  <Col span={6}>
                    <Statistic title="Target comments" value={selectedRecord.request?.sampling_plan?.target_comment_count || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Target sources" value={selectedRecord.request?.sampling_plan?.target_source_count || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Result evidence" value={providerResult?.counts?.evidence || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Result sources" value={providerResult?.counts?.sources || 0} />
                  </Col>
                </Row>
                <Descriptions column={1} size="small">
                  <Descriptions.Item label="title">{selectedRecord.request?.case_seed?.title || ''}</Descriptions.Item>
                  <Descriptions.Item label="request_file">{requestPath}</Descriptions.Item>
                  <Descriptions.Item label="result_file">
                    {selectedRecord.result_file || 'runtime/analysis_requests/results/<request_id>.json'}
                  </Descriptions.Item>
                  <Descriptions.Item label="provider execution">outside Sentigraph core</Descriptions.Item>
                  <Descriptions.Item label="privacy">
                    raw identity fields removed: {String(selectedRecord.request?.privacy_policy?.remove_raw_author_id !== false)}
                  </Descriptions.Item>
                </Descriptions>
                {selectedRecord.result_warning ? (
                  <Alert type="warning" showIcon message="Provider result warning" description={selectedRecord.result_warning} />
                ) : null}
                {providerResult ? (
                  <Alert
                    type={providerResult.status === 'package_ready' ? 'success' : 'info'}
                    showIcon
                    message={`Provider result: ${providerResult.status}`}
                    description={
                      <Space direction="vertical" size={4}>
                        <Text>package: {providerResult.package_name || 'not provided'}</Text>
                        <Text>coverage: {providerResult.coverage?.coverage_level || 'selected_public_sample'}</Text>
                        <Text>
                          validation: {providerResult.validation?.status || 'unknown'} /
                          errors {providerResult.validation?.errors || 0} /
                          warnings {providerResult.validation?.warnings || 0}
                        </Text>
                      </Space>
                    }
                  />
                ) : (
                  <Alert
                    type="info"
                    showIcon
                    message="等待外部 Provider result JSON"
                    description="如果外部 Provider 手动写入 runtime/analysis_requests/results/<request_id>.json，本页会读取并展示状态；不会启动 Provider。"
                  />
                )}

                <Card size="small" title="本地案例草稿 handoff">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={draftGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={draftGate.eligible ? '可创建本地案例草稿' : '暂不可创建本地案例草稿'}
                      description={caseDraft ? '已存在本地 handoff 草稿。' : draftGate.reason}
                    />
                    <Text type="secondary">
                      仅生成本地 handoff 草稿，不导入 Evidence rows，不创建正式 case，不运行分析，不生成报告。Provider output is evidence, not official truth.
                    </Text>
                    {draftError ? <Alert type="error" showIcon message={draftError} /> : null}
                    <Space wrap>
                      <Button
                        type="primary"
                        disabled={!draftGate.eligible && !caseDraft}
                        loading={draftLoading}
                        onClick={handleCreateCaseDraft}
                      >
                        创建案例草稿 / Create case draft
                      </Button>
                      {caseDraft ? (
                        <Button
                          icon={<ClipboardCopy size={16} />}
                          onClick={() => copyText(draftJson, 'Case draft JSON 已复制')}
                        >
                          复制 draft JSON
                        </Button>
                      ) : null}
                    </Space>
                    {caseDraft ? (
                      <Card className="panel-card" size="small">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="green">{caseDraft.readiness?.state || 'ready_for_manual_review'}</Tag>
                            <Tag color="default">can_import_evidence: {boolText(caseDraft.readiness?.can_import_evidence)}</Tag>
                            <Tag color="gold">needs human review</Tag>
                          </Space>
                          <Row gutter={[12, 12]}>
                            <Col span={6}><Statistic title="Evidence" value={caseDraft.counts?.evidence || 0} /></Col>
                            <Col span={6}><Statistic title="Comments" value={caseDraft.counts?.comments || 0} /></Col>
                            <Col span={6}><Statistic title="Sources" value={caseDraft.counts?.sources || 0} /></Col>
                            <Col span={6}><Statistic title="Roots" value={caseDraft.counts?.roots || 0} /></Col>
                          </Row>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="draft_id">{caseDraft.draft_id}</Descriptions.Item>
                            <Descriptions.Item label="package">{caseDraft.package_reference?.package_name || '-'}</Descriptions.Item>
                            <Descriptions.Item label="validation">
                              {caseDraft.validation?.status || 'unknown'} / errors {caseDraft.validation?.errors || 0} / warnings {caseDraft.validation?.warnings || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="coverage">
                              not_full_web={boolText(caseDraft.coverage?.not_full_web)}, not_full_platform={boolText(caseDraft.coverage?.not_full_platform)}, not_full_thread={boolText(caseDraft.coverage?.not_full_thread)}
                            </Descriptions.Item>
                            <Descriptions.Item label="privacy">
                              raw ids removed={boolText(caseDraft.privacy?.raw_author_ids_removed)}, raw names removed={boolText(caseDraft.privacy?.raw_author_names_removed)}, profile URLs removed={boolText(caseDraft.privacy?.profile_urls_removed)}, private messages excluded={boolText(caseDraft.privacy?.private_messages_excluded)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Boundary notes"
                            description={(caseDraft.boundary_notes || []).join(' ')}
                          />
                          <SummaryList title="Recommended next steps" items={caseDraft.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}
                  </Space>
                </Card>

                <Card size="small" title="Evidence 导入计划 / Manual import planning gate">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={planGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={planGate.eligible ? '可生成 Evidence 导入计划' : '暂不可生成 Evidence 导入计划'}
                      description={importPlan ? '已存在本地 Evidence import plan。' : planGate.reason}
                    />
                    <Text type="secondary">
                      只生成本地导入计划，不导入 Evidence rows，不创建正式 case，不运行分析，不生成 Sandbox，不生成报告。Evidence rows will require manual import and review in a later phase.
                    </Text>
                    {planError ? <Alert type="error" showIcon message={planError} /> : null}
                    <Space wrap>
                      <Button
                        type="primary"
                        disabled={!planGate.eligible && !importPlan}
                        loading={planLoading}
                        onClick={handleCreateImportPlan}
                      >
                        生成 Evidence 导入计划 / Create import plan
                      </Button>
                      {importPlan ? (
                        <Button
                          icon={<ClipboardCopy size={16} />}
                          onClick={() => copyText(importPlanJson, 'Import plan JSON 已复制')}
                        >
                          复制 plan JSON
                        </Button>
                      ) : null}
                    </Space>
                    {importPlan ? (
                      <Card className="panel-card" size="small">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="green">{importPlan.readiness?.state || 'ready_for_manual_import_review'}</Tag>
                            <Tag color="default">can_import_now: {boolText(importPlan.readiness?.can_import_now)}</Tag>
                            <Tag color="gold">{importPlan.default_evidence_policy?.review_status || 'review_needed'}</Tag>
                            <Tag color="purple">{importPlan.default_evidence_policy?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="plan_id">{importPlan.plan_id}</Descriptions.Item>
                            <Descriptions.Item label="draft_id">{importPlan.draft_id}</Descriptions.Item>
                            <Descriptions.Item label="package">{importPlan.package_reference?.package_name || '-'}</Descriptions.Item>
                            <Descriptions.Item label="counts">
                              evidence={importPlan.counts?.evidence || 0}, comments={importPlan.counts?.comments || 0}, sources={importPlan.counts?.sources || 0}, roots={importPlan.counts?.roots || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="validation">
                              {importPlan.validation?.status || 'unknown'} / errors {importPlan.validation?.errors || 0} / warnings {importPlan.validation?.warnings || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="coverage limitation">
                              not_full_web={boolText(importPlan.coverage?.not_full_web)}, not_full_platform={boolText(importPlan.coverage?.not_full_platform)}, not_full_thread={boolText(importPlan.coverage?.not_full_thread)}
                            </Descriptions.Item>
                            <Descriptions.Item label="privacy">
                              raw ids removed={boolText(importPlan.privacy?.raw_author_ids_removed)}, raw names removed={boolText(importPlan.privacy?.raw_author_names_removed)}, profile URLs removed={boolText(importPlan.privacy?.profile_urls_removed)}, private messages excluded={boolText(importPlan.privacy?.private_messages_excluded)}
                            </Descriptions.Item>
                            <Descriptions.Item label="proposed import">
                              mode={importPlan.proposed_import?.mode || 'manual_review_required'}, target={importPlan.proposed_import?.target || 'future_evidence_layer'}
                            </Descriptions.Item>
                            <Descriptions.Item label="do-now flags">
                              import_rows={boolText(importPlan.proposed_import?.import_evidence_rows_now)}, create_case={boolText(importPlan.proposed_import?.create_case_now)}, run_analysis={boolText(importPlan.proposed_import?.run_analysis_now)}, sandbox={boolText(importPlan.proposed_import?.generate_sandbox_now)}, report={boolText(importPlan.proposed_import?.generate_report_now)}
                            </Descriptions.Item>
                            <Descriptions.Item label="default evidence policy">
                              verification={importPlan.default_evidence_policy?.verification_status || 'source_url_provided_unverified'}, dedup={boolText(importPlan.default_evidence_policy?.dedup_required)}, audit={boolText(importPlan.default_evidence_policy?.audit_required)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Import plan boundary"
                            description="Import plan does not mean evidence has been imported, case has been created, analysis has finished, or report/Sandbox has been generated."
                          />
                          <SummaryList title="Manual review checklist" items={importPlan.manual_review_checklist || []} />
                          <SummaryList title="Blockers" items={importPlan.blockers || []} />
                          <SummaryList title="Recommended next steps" items={importPlan.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}
                  </Space>
                </Card>

                <Card size="small" title="Evidence 导入预览 / Metadata-only import preview">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={previewGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={previewGate.eligible ? '可生成 Evidence 导入预览' : '暂不可生成 Evidence 导入预览'}
                      description={importPreview ? '已存在本地 metadata-only import preview。' : previewGate.reason}
                    />
                    <Text type="secondary">
                      只生成 metadata-only 导入预览，不读取 evidence rows，不导入，不创建正式 case，不运行分析。Preview is not import, not truth verification, and not report/Sandbox/public event generation.
                    </Text>
                    {previewError ? <Alert type="error" showIcon message={previewError} /> : null}
                    <Space wrap>
                      <Button
                        type="primary"
                        disabled={!previewGate.eligible && !importPreview}
                        loading={previewLoading}
                        onClick={handleCreateImportPreview}
                      >
                        生成导入预览 / Create import preview
                      </Button>
                      {importPreview ? (
                        <Button
                          icon={<ClipboardCopy size={16} />}
                          onClick={() => copyText(importPreviewJson, 'Import preview JSON 已复制')}
                        >
                          复制 preview JSON
                        </Button>
                      ) : null}
                    </Space>
                    {importPreview ? (
                      <Card className="panel-card" size="small">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="green">{importPreview.readiness?.state || 'ready_for_human_review'}</Tag>
                            <Tag color="default">can_import_now: {boolText(importPreview.readiness?.can_import_now)}</Tag>
                            <Tag color="gold">requires_review: {boolText(importPreview.readiness?.requires_review_decision)}</Tag>
                            <Tag color="purple">{importPreview.proposed_evidence_defaults?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="preview_id">{importPreview.preview_id}</Descriptions.Item>
                            <Descriptions.Item label="plan_id">{importPreview.plan_id}</Descriptions.Item>
                            <Descriptions.Item label="draft_id">{importPreview.draft_id}</Descriptions.Item>
                            <Descriptions.Item label="package">{importPreview.package_reference?.package_name || '-'}</Descriptions.Item>
                            <Descriptions.Item label="metadata summary">
                              evidence={importPreview.metadata_summary?.evidence || 0}, comments={importPreview.metadata_summary?.comments || 0}, sources={importPreview.metadata_summary?.sources || 0}, roots={importPreview.metadata_summary?.roots || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="validation summary">
                              {importPreview.validation_summary?.status || 'unknown'} / errors {importPreview.validation_summary?.errors || 0} / warnings {importPreview.validation_summary?.warnings || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="coverage summary">
                              level={importPreview.coverage_summary?.coverage_level || 'selected_public_sample'}, not_full_web={boolText(importPreview.coverage_summary?.not_full_web)}, not_full_platform={boolText(importPreview.coverage_summary?.not_full_platform)}, not_full_thread={boolText(importPreview.coverage_summary?.not_full_thread)}
                            </Descriptions.Item>
                            <Descriptions.Item label="privacy summary">
                              raw ids removed={boolText(importPreview.privacy_summary?.raw_author_ids_removed)}, raw names removed={boolText(importPreview.privacy_summary?.raw_author_names_removed)}, profile URLs removed={boolText(importPreview.privacy_summary?.profile_urls_removed)}, private messages excluded={boolText(importPreview.privacy_summary?.private_messages_excluded)}
                            </Descriptions.Item>
                            <Descriptions.Item label="proposed defaults">
                              review={importPreview.proposed_evidence_defaults?.review_status || 'review_needed'}, verification={importPreview.proposed_evidence_defaults?.verification_status || 'source_url_provided_unverified'}, trust={importPreview.proposed_evidence_defaults?.trust_label || 'medium_low'}, dedup={boolText(importPreview.proposed_evidence_defaults?.dedup_required)}, audit={boolText(importPreview.proposed_evidence_defaults?.audit_required)}
                            </Descriptions.Item>
                            <Descriptions.Item label="dedup preview">
                              required={boolText(importPreview.dedup_preview?.required)}, computed_now={boolText(importPreview.dedup_preview?.computed_now)}, reason={importPreview.dedup_preview?.reason || '-'}
                            </Descriptions.Item>
                            <Descriptions.Item label="sample preview policy">
                              read_rows_now={boolText(importPreview.sample_preview_policy?.read_rows_now)}, future_safe_rows={importPreview.sample_preview_policy?.max_safe_sample_rows_future || 0}, redact_author_fields={boolText(importPreview.sample_preview_policy?.redact_author_fields)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Import preview boundary"
                            description="Import preview is not import. It does not read rows, create a case, run analysis, verify truth, or generate Sandbox/public event/report output. Evidence rows require later human review decision and manual import job."
                          />
                          <SummaryList title="Preview blockers" items={importPreview.blockers || []} />
                          <SummaryList title="Preview warnings" items={importPreview.warnings || []} />
                          <SummaryList title="Boundary notes" items={importPreview.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={importPreview.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}
                  </Space>
                </Card>

                <Card size="small" title="人工审核决策 / Human review decision">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={importPreview ? 'success' : 'info'}
                      showIcon
                      message={importPreview ? '可记录人工审核决策' : '请先生成 Evidence 导入预览'}
                      description="Review decision is not import. Approval only allows a future manual import job phase; it does not create case, run analysis, verify truth, or generate report/Sandbox/public event output."
                    />
                    {reviewError ? <Alert type="error" showIcon message={reviewError} /> : null}
                    {importPreview ? (
                      <Form
                        form={reviewForm}
                        layout="vertical"
                        initialValues={{
                          reviewer_label: 'sentigraph_local_reviewer',
                          decision: 'request_more_source',
                          target_case_mode: 'new_review_case',
                          checklist: [],
                        }}
                        onFinish={handleCreateReviewDecision}
                      >
                        <Row gutter={[12, 0]}>
                          <Col span={8}>
                            <Form.Item
                              name="reviewer_label"
                              label="reviewer_label"
                              rules={[{ required: true, message: 'Please enter reviewer_label' }]}
                            >
                              <Input placeholder="sentigraph_local_reviewer" />
                            </Form.Item>
                          </Col>
                          <Col span={8}>
                            <Form.Item name="decision" label="decision">
                              <Select options={REVIEW_DECISION_OPTIONS} />
                            </Form.Item>
                          </Col>
                          <Col span={8}>
                            <Form.Item name="target_case_mode" label="target_case_mode">
                              <Select options={TARGET_CASE_MODE_OPTIONS} />
                            </Form.Item>
                          </Col>
                        </Row>
                        <Form.Item name="target_case_id" label="target_case_id / optional existing case id">
                          <Input placeholder="Only meaningful when target_case_mode=existing_case" />
                        </Form.Item>
                        <Form.Item name="notes" label="review notes">
                          <TextArea rows={3} placeholder="例如：覆盖范围已确认，仅允许未来人工导入；或要求 provider 补充来源说明。" />
                        </Form.Item>
                        <Form.Item name="checklist" label="review checklist">
                          <Checkbox.Group className="full-width">
                            <Row gutter={[8, 8]}>
                              {REVIEW_CHECKLIST_ITEMS.map((item) => (
                                <Col span={12} key={item.value}>
                                  <Checkbox value={item.value}>{item.label}</Checkbox>
                                </Col>
                              ))}
                            </Row>
                          </Checkbox.Group>
                        </Form.Item>
                        <Space wrap>
                          <Button type="primary" htmlType="submit" loading={reviewLoading} disabled={reviewSubmitDisabled}>
                            记录人工审核决策 / Record review decision
                          </Button>
                          {watchedReviewDecision === 'approve_import' && reviewSubmitDisabled ? (
                            <Text type="secondary">approve_import requires all checklist acknowledgements.</Text>
                          ) : null}
                        </Space>
                      </Form>
                    ) : null}

                    {latestReviewDecision ? (
                      <Card className="panel-card" size="small" title="Latest review decision">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="green">{latestReviewDecision.readiness?.state || 'recorded'}</Tag>
                            <Tag color="blue">{latestReviewDecision.decision}</Tag>
                            <Tag color="default">can_create_import_job_now: {boolText(latestReviewDecision.readiness?.can_create_import_job_now)}</Tag>
                            <Tag color="purple">{latestReviewDecision.approved_defaults?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="decision_id">{latestReviewDecision.decision_id}</Descriptions.Item>
                            <Descriptions.Item label="reviewer_label">{latestReviewDecision.reviewer_label}</Descriptions.Item>
                            <Descriptions.Item label="reviewed_at">{latestReviewDecision.reviewed_at || '-'}</Descriptions.Item>
                            <Descriptions.Item label="target_case_mode">{latestReviewDecision.target_case_mode}</Descriptions.Item>
                            <Descriptions.Item label="target_case_id">{latestReviewDecision.target_case_id || '-'}</Descriptions.Item>
                            <Descriptions.Item label="approved defaults">
                              review={latestReviewDecision.approved_defaults?.review_status || 'review_needed'}, verification={latestReviewDecision.approved_defaults?.verification_status || 'source_url_provided_unverified'}, trust={latestReviewDecision.approved_defaults?.trust_label || 'medium_low'}
                            </Descriptions.Item>
                            <Descriptions.Item label="checklist">
                              {Object.entries(latestReviewDecision.checklist || {}).filter(([, value]) => value).length}/{REVIEW_CHECKLIST_KEYS.length} acknowledged
                            </Descriptions.Item>
                            <Descriptions.Item label="notes">{latestReviewDecision.notes || '-'}</Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Review decision boundary"
                            description="Even approve_import does not import evidence rows, create a case, run analysis, generate reports, or verify official truth. It only records a human decision for a later manual import phase."
                          />
                          <SummaryList title="Decision boundary notes" items={latestReviewDecision.boundary_notes || []} />
                          <Button
                            icon={<ClipboardCopy size={16} />}
                            onClick={() => copyText(latestReviewDecisionJson, 'Review decision JSON 已复制')}
                          >
                            复制 decision JSON
                          </Button>
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title={`Existing decisions (${reviewDecisions.length})`}>
                      {reviewDecisions.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {reviewDecisions.map((decision) => (
                            <Card size="small" key={decision.decision_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="blue">{decision.decision}</Tag>
                                  <Tag>{decision.readiness?.state || 'recorded'}</Tag>
                                  <Text type="secondary">{decision.decision_id}</Text>
                                </Space>
                                <Text>reviewer: {decision.reviewer_label || '-'}</Text>
                                <Text type="secondary">reviewed_at: {decision.reviewed_at || '-'}</Text>
                                <Text type="secondary">notes: {decision.notes || '-'}</Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No human review decision records yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Card size="small" title="Manual Evidence Import Job / Dry-run gate">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={importJobGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={importJobGate.eligible ? 'Ready to create import job draft' : 'Import job draft not ready'}
                      description={latestImportJob ? 'An append-only dry-run job draft already exists for this request.' : importJobGate.reason}
                    />
                    <Text type="secondary">
                      This creates only a local dry-run job draft. It does not import evidence rows, read or parse rows, create a production case, run dedup, create review queue items, run analysis, generate Sandbox/public event pages, or generate reports.
                    </Text>
                    {importJobError ? <Alert type="error" showIcon message={importJobError} /> : null}
                    <Form
                      form={importJobForm}
                      layout="vertical"
                      initialValues={{
                        target_case_mode: 'new_review_case',
                      }}
                      onFinish={handleCreateImportJob}
                    >
                      <Row gutter={[12, 0]}>
                        <Col span={8}>
                          <Form.Item name="target_case_mode" label="target_case_mode">
                            <Select options={IMPORT_JOB_TARGET_CASE_OPTIONS} />
                          </Form.Item>
                        </Col>
                        <Col span={8}>
                          <Form.Item name="target_case_id" label="target_case_id">
                            <Input placeholder="Required only for existing_case" />
                          </Form.Item>
                        </Col>
                        <Col span={8}>
                          <Form.Item name="decision_id" label="decision_id">
                            <Input placeholder={latestReviewDecision?.decision_id || 'latest approve_import decision'} />
                          </Form.Item>
                        </Col>
                      </Row>
                      <Space wrap>
                        <Button
                          type="primary"
                          htmlType="submit"
                          loading={importJobLoading}
                          disabled={!importJobGate.eligible}
                        >
                          Create import job draft / dry-run only
                        </Button>
                        {latestImportJob ? (
                          <Button
                            icon={<ClipboardCopy size={16} />}
                            onClick={() => copyText(latestImportJobJson, 'Import job JSON copied')}
                          >
                            Copy latest job JSON
                          </Button>
                        ) : null}
                      </Space>
                    </Form>

                    {latestImportJob ? (
                      <Card className="panel-card" size="small" title="Latest dry-run import job draft">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="green">{latestImportJob.status || 'draft_not_executed'}</Tag>
                            <Tag color="blue">{latestImportJob.execution_mode || 'dry_run_gate'}</Tag>
                            <Tag color="default">can_execute_now: {boolText(latestImportJob.readiness?.can_execute_now)}</Tag>
                            <Tag color="purple">{latestImportJob.approved_defaults?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="job_id">{latestImportJob.job_id}</Descriptions.Item>
                            <Descriptions.Item label="decision_id">{latestImportJob.decision_id}</Descriptions.Item>
                            <Descriptions.Item label="preview_id">{latestImportJob.preview_id}</Descriptions.Item>
                            <Descriptions.Item label="package">{latestImportJob.package_reference?.package_name || '-'}</Descriptions.Item>
                            <Descriptions.Item label="target_case">
                              mode={latestImportJob.target_case?.mode || 'new_review_case'}, target_case_id={latestImportJob.target_case?.target_case_id || '-'}, create_case_now={boolText(latestImportJob.target_case?.create_case_now)}
                            </Descriptions.Item>
                            <Descriptions.Item label="metadata summary">
                              evidence={latestImportJob.metadata_summary?.evidence || 0}, comments={latestImportJob.metadata_summary?.comments || 0}, sources={latestImportJob.metadata_summary?.sources || 0}, roots={latestImportJob.metadata_summary?.roots || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="approved defaults">
                              review={latestImportJob.approved_defaults?.review_status || 'review_needed'}, verification={latestImportJob.approved_defaults?.verification_status || 'source_url_provided_unverified'}, trust={latestImportJob.approved_defaults?.trust_label || 'medium_low'}
                            </Descriptions.Item>
                            <Descriptions.Item label="dry-run now flags">
                              import_rows={boolText(latestImportJob.dry_run_result?.import_evidence_rows_now)}, create_case={boolText(latestImportJob.dry_run_result?.create_case_now)}, dedup={boolText(latestImportJob.dry_run_result?.run_dedup_now)}, review_queue={boolText(latestImportJob.dry_run_result?.create_review_queue_now)}, analysis={boolText(latestImportJob.dry_run_result?.run_analysis_now)}, report={boolText(latestImportJob.dry_run_result?.generate_report_now)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Dry-run boundary"
                            description="Append-only job draft only: no evidence rows read, parsed, or imported; no production case; no analysis; no report; no provider or collector execution."
                          />
                          <SummaryList title="Preflight checks" items={Object.entries(latestImportJob.preflight_checks || {}).map(([key, value]) => `${key}: ${boolText(value)}`)} />
                          <SummaryList title="Boundary notes" items={latestImportJob.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={latestImportJob.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title={`Existing import job drafts (${importJobs.length})`}>
                      {importJobs.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {importJobs.map((job) => (
                            <Card size="small" key={job.job_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="blue">{job.execution_mode}</Tag>
                                  <Tag>{job.status}</Tag>
                                  <Text type="secondary">{job.job_id}</Text>
                                </Space>
                                <Text>package: {job.package_reference?.package_name || '-'}</Text>
                                <Text type="secondary">created_at: {job.created_at || '-'}</Text>
                                <Text type="secondary">target: {job.target_case?.mode || 'new_review_case'}</Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No import job drafts yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Card size="small" title="Manual Import Execution Preflight / 执行前检查">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={executionPreflightGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={executionPreflightGate.eligible ? 'Ready to create execution preflight' : 'Execution preflight not ready'}
                      description={
                        latestExecutionPreflight
                          ? 'An append-only execution preflight already exists for this request.'
                          : executionPreflightGate.reason
                      }
                    />
                    <Text type="secondary">
                      执行前检查只记录 package metadata 与文件名存在性。它不会打开、读取或解析 evidence row 文件，不会导入 Evidence，
                      不会创建生产 case，不会运行 dedup/review queue/analysis，也不会生成 Sandbox、公开事件页或报告。
                    </Text>
                    {executionPreflightError ? <Alert type="error" showIcon message={executionPreflightError} /> : null}
                    <Space wrap>
                      <Button
                        type="primary"
                        loading={executionPreflightLoading}
                        disabled={!executionPreflightGate.eligible}
                        onClick={handleCreateExecutionPreflight}
                      >
                        Create execution preflight / metadata only
                      </Button>
                      {latestExecutionPreflight ? (
                        <Button
                          icon={<ClipboardCopy size={16} />}
                          onClick={() => copyText(latestExecutionPreflightJson, 'Execution preflight JSON copied')}
                        >
                          Copy latest preflight JSON
                        </Button>
                      ) : null}
                    </Space>

                    {latestExecutionPreflight ? (
                      <Card className="panel-card" size="small" title="Latest execution preflight">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color={latestExecutionPreflight.status === 'preflight_warn' ? 'gold' : 'green'}>
                              {latestExecutionPreflight.status}
                            </Tag>
                            <Tag color="blue">{latestExecutionPreflight.execution_mode || 'preflight_only'}</Tag>
                            <Tag color="default">can_execute_now: {boolText(latestExecutionPreflight.readiness?.can_execute_now)}</Tag>
                            <Tag color="purple">source: {latestExecutionPreflight.source}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="preflight_id">{latestExecutionPreflight.preflight_id}</Descriptions.Item>
                            <Descriptions.Item label="job_id">{latestExecutionPreflight.job_id}</Descriptions.Item>
                            <Descriptions.Item label="package">{latestExecutionPreflight.package_reference?.package_name || '-'}</Descriptions.Item>
                            <Descriptions.Item label="file checks">
                              manifest={boolText(latestExecutionPreflight.package_file_checks?.manifest_present)},
                              validation_report={boolText(latestExecutionPreflight.package_file_checks?.validation_report_present)},
                              coverage_note={boolText(latestExecutionPreflight.package_file_checks?.coverage_note_present)},
                              jsonl={boolText(latestExecutionPreflight.package_file_checks?.evidence_items_jsonl_present)},
                              csv={boolText(latestExecutionPreflight.package_file_checks?.evidence_items_csv_present)}
                            </Descriptions.Item>
                            <Descriptions.Item label="row file behavior">
                              opened={boolText(latestExecutionPreflight.package_file_checks?.row_files_opened)},
                              parsed={boolText(latestExecutionPreflight.package_file_checks?.row_files_parsed)},
                              read_rows_now={boolText(latestExecutionPreflight.future_row_reader_plan?.read_rows_now)}
                            </Descriptions.Item>
                            <Descriptions.Item label="future staging">
                              stage_rows_now={boolText(latestExecutionPreflight.future_staging_plan?.stage_rows_now)},
                              default_review={latestExecutionPreflight.future_staging_plan?.default_review_status || 'review_needed'},
                              analysis_included={boolText(latestExecutionPreflight.future_staging_plan?.analysis_included)}
                            </Descriptions.Item>
                            <Descriptions.Item label="future governance">
                              dedup_now={boolText(latestExecutionPreflight.future_governance_plan?.dedup_run_now)},
                              review_queue_now={boolText(latestExecutionPreflight.future_governance_plan?.review_queue_created_now)},
                              audit_required={boolText(latestExecutionPreflight.future_governance_plan?.audit_required)}
                            </Descriptions.Item>
                            <Descriptions.Item label="metadata summary">
                              evidence={latestExecutionPreflight.metadata_summary?.evidence || 0},
                              comments={latestExecutionPreflight.metadata_summary?.comments || 0},
                              sources={latestExecutionPreflight.metadata_summary?.sources || 0},
                              roots={latestExecutionPreflight.metadata_summary?.roots || 0}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Preflight boundary"
                            description="Append-only preflight only: no row read, no row parse, no Evidence Layer write, no production case, no dedup/review queue, no analysis, no report, no provider execution."
                          />
                          <SummaryList title="Warnings" items={latestExecutionPreflight.warnings || []} />
                          <SummaryList title="Boundary notes" items={latestExecutionPreflight.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={latestExecutionPreflight.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title={`Existing execution preflights (${executionPreflights.length})`}>
                      {executionPreflights.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {executionPreflights.map((preflight) => (
                            <Card size="small" key={preflight.preflight_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="blue">{preflight.execution_mode}</Tag>
                                  <Tag>{preflight.status}</Tag>
                                  <Text type="secondary">{preflight.preflight_id}</Text>
                                </Space>
                                <Text>package: {preflight.package_reference?.package_name || '-'}</Text>
                                <Text type="secondary">created_at: {preflight.created_at || '-'}</Text>
                                <Text type="secondary">
                                  row files opened: {boolText(preflight.package_file_checks?.row_files_opened)} / parsed: {boolText(preflight.package_file_checks?.row_files_parsed)}
                                </Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No execution preflight records yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Card size="small" title="Synthetic Row Reader Dry-Run / 合成样本行读取演练">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={rowReaderGate.eligible ? 'success' : 'info'}
                      showIcon
                      message={rowReaderGate.eligible ? 'Ready to run synthetic fixture row reader' : 'Synthetic row reader dry-run not ready'}
                      description={
                        latestRowReaderDryRun
                          ? 'An append-only synthetic row reader dry-run already exists for this request.'
                          : rowReaderGate.reason
                      }
                    />
                    <Text type="secondary">
                      只读取项目内 synthetic fixture，不读取真实 provider package，不读取外部 collector package，不导入 evidence rows。
                      Preview rows are redacted; quarantined rows are not imported; invalid rows are rejected. Future real package row preview needs a separate phase.
                    </Text>
                    {rowReaderDryRunError ? <Alert type="error" showIcon message={rowReaderDryRunError} /> : null}
                    <Form
                      form={rowReaderForm}
                      layout="vertical"
                      initialValues={{
                        fixture_name: 'safe_evidence_items',
                        max_rows: 20,
                      }}
                      onFinish={handleCreateRowReaderDryRun}
                    >
                      <Row gutter={[12, 0]}>
                        <Col span={12}>
                          <Form.Item name="fixture_name" label="fixture">
                            <Select options={ROW_READER_FIXTURE_OPTIONS} />
                          </Form.Item>
                        </Col>
                        <Col span={12}>
                          <Form.Item name="max_rows" label="max_rows">
                            <InputNumber min={1} max={20} className="full-width" />
                          </Form.Item>
                        </Col>
                      </Row>
                      <Space wrap>
                        <Button
                          type="primary"
                          htmlType="submit"
                          loading={rowReaderDryRunLoading}
                          disabled={!rowReaderGate.eligible}
                        >
                          运行合成样本行读取演练 / Synthetic only
                        </Button>
                        {latestRowReaderDryRun ? (
                          <Button
                            icon={<ClipboardCopy size={16} />}
                            onClick={() => copyText(latestRowReaderDryRunJson, 'Row reader dry-run JSON copied')}
                          >
                            Copy latest dry-run JSON
                          </Button>
                        ) : null}
                      </Space>
                    </Form>

                    {latestRowReaderDryRun ? (
                      <Card className="panel-card" size="small" title="Latest synthetic row reader dry-run">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color={latestRowReaderDryRun.status === 'passed' ? 'green' : 'gold'}>
                              {latestRowReaderDryRun.status}
                            </Tag>
                            <Tag color="blue">{latestRowReaderDryRun.execution_mode}</Tag>
                            <Tag color="default">can_import_now: {boolText(latestRowReaderDryRun.readiness?.can_import_now)}</Tag>
                            <Tag color="purple">{latestRowReaderDryRun.governance_defaults?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="dry_run_id">{latestRowReaderDryRun.dry_run_id}</Descriptions.Item>
                            <Descriptions.Item label="preflight_id">{latestRowReaderDryRun.preflight_id}</Descriptions.Item>
                            <Descriptions.Item label="fixture policy">
                              synthetic_only={boolText(latestRowReaderDryRun.fixture_policy?.synthetic_fixture_only)},
                              real_package_allowed={boolText(latestRowReaderDryRun.fixture_policy?.real_provider_package_allowed)},
                              max_rows={latestRowReaderDryRun.fixture_policy?.max_rows || 20}
                            </Descriptions.Item>
                            <Descriptions.Item label="row source">
                              type={latestRowReaderDryRun.row_source?.source_type || '-'},
                              name={latestRowReaderDryRun.row_source?.source_name || '-'},
                              real_package_path_used={boolText(latestRowReaderDryRun.row_source?.real_package_path_used)}
                            </Descriptions.Item>
                            <Descriptions.Item label="counts">
                              rows_seen={latestRowReaderDryRun.counts?.rows_seen || 0},
                              accepted={latestRowReaderDryRun.counts?.accepted_for_preview || 0},
                              quarantined={latestRowReaderDryRun.counts?.quarantined || 0},
                              rejected={latestRowReaderDryRun.counts?.rejected || 0}
                            </Descriptions.Item>
                            <Descriptions.Item label="privacy scan">
                              raw_author_id={latestRowReaderDryRun.privacy_scan?.raw_author_id_detected || 0},
                              raw_author_name={latestRowReaderDryRun.privacy_scan?.raw_author_name_detected || 0},
                              profile_url={latestRowReaderDryRun.privacy_scan?.profile_url_detected || 0},
                              private_message={latestRowReaderDryRun.privacy_scan?.private_message_detected || 0},
                              privacy_stop={boolText(latestRowReaderDryRun.privacy_scan?.privacy_stop_triggered)}
                            </Descriptions.Item>
                            <Descriptions.Item label="now flags">
                              import={boolText(latestRowReaderDryRun.now_flags?.import_evidence_rows_now)},
                              evidence_layer={boolText(latestRowReaderDryRun.now_flags?.write_evidence_layer_now)},
                              case={boolText(latestRowReaderDryRun.now_flags?.create_case_now)},
                              review_queue={boolText(latestRowReaderDryRun.now_flags?.create_review_queue_now)},
                              dedup={boolText(latestRowReaderDryRun.now_flags?.run_dedup_now)},
                              analysis={boolText(latestRowReaderDryRun.now_flags?.run_analysis_now)},
                              report={boolText(latestRowReaderDryRun.now_flags?.generate_report_now)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Synthetic-only boundary"
                            description="This dry-run reads only local synthetic fixtures. It does not read real provider packages, import evidence, write the Evidence Layer, create cases, run review/dedup/analysis, or generate Sandbox/public event/report output."
                          />
                          <Card size="small" title={`Redacted preview rows (${latestRowReaderDryRun.redacted_preview_rows?.length || 0})`}>
                            {latestRowReaderDryRun.redacted_preview_rows?.length ? (
                              <Space direction="vertical" size={8} className="full-width">
                                {latestRowReaderDryRun.redacted_preview_rows.map((row) => (
                                  <Card size="small" key={row.row_index}>
                                    <Space direction="vertical" size={4} className="full-width">
                                      <Space wrap>
                                        <Tag>{row.status}</Tag>
                                        <Tag color="cyan">{row.evidence_candidate?.platform || '-'}</Tag>
                                        <Tag color="blue">{row.evidence_candidate?.evidence_type || '-'}</Tag>
                                      </Space>
                                      <Text strong>{row.evidence_candidate?.title || '-'}</Text>
                                      <Text type="secondary">{row.evidence_candidate?.body_text_preview || '-'}</Text>
                                      <Text type="secondary">review_status: {row.governance_defaults?.review_status || 'review_needed'} / analysis_included: {boolText(row.governance_defaults?.analysis_included)}</Text>
                                    </Space>
                                  </Card>
                                ))}
                              </Space>
                            ) : (
                              <Text type="secondary">No accepted preview rows.</Text>
                            )}
                          </Card>
                          <SummaryList title="Quarantine summary" items={(latestRowReaderDryRun.quarantine_summary || []).map((item) => `row ${item.row_index}: ${item.reason_code} (${(item.forbidden_fields_detected || []).join(', ')})`)} />
                          <SummaryList title="Rejection summary" items={(latestRowReaderDryRun.rejection_summary || []).map((item) => `row ${item.row_index}: ${item.reason_code}`)} />
                          <SummaryList title="Warnings" items={latestRowReaderDryRun.warnings || []} />
                          <SummaryList title="Boundary notes" items={latestRowReaderDryRun.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={latestRowReaderDryRun.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title={`Existing row reader dry-runs (${rowReaderDryRuns.length})`}>
                      {rowReaderDryRuns.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {rowReaderDryRuns.map((dryRun) => (
                            <Card size="small" key={dryRun.dry_run_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="blue">{dryRun.execution_mode}</Tag>
                                  <Tag>{dryRun.status}</Tag>
                                  <Text type="secondary">{dryRun.dry_run_id}</Text>
                                </Space>
                                <Text>fixture: {dryRun.row_source?.source_name || '-'}</Text>
                                <Text type="secondary">
                                  accepted={dryRun.counts?.accepted_for_preview || 0}, quarantined={dryRun.counts?.quarantined || 0}, rejected={dryRun.counts?.rejected || 0}
                                </Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No synthetic row reader dry-runs yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Card size="small" title="Limited Real Package Row Preview / 真实包行预览（受限）">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={realPackagePreviewGate.eligible ? 'warning' : 'info'}
                      showIcon
                      message={realPackagePreviewGate.eligible ? 'Ready for limited row preview' : 'Limited real package row preview not ready'}
                      description={
                        latestRealPackagePreview
                          ? 'An append-only limited real package row preview already exists for this request.'
                          : realPackagePreviewGate.reason
                      }
                    />
                    <Text type="secondary">
                      只读取本地 Evidence Export package 的极少量行用于 redacted safety preview。不会导入、不会建 case、不会创建 review queue、不会 dedup、不会分析或生成报告。Preview rows are not representative; provider output is evidence, not truth.
                    </Text>
                    {realPackagePreviewError ? <Alert type="error" showIcon message={realPackagePreviewError} /> : null}
                    <Form
                      form={realPackagePreviewForm}
                      layout="vertical"
                      initialValues={{
                        max_rows: 10,
                        acknowledge_real_package_preview: false,
                        acknowledge_no_import: false,
                        acknowledge_preview_not_representative: false,
                        acknowledge_privacy_stop: false,
                      }}
                      onFinish={handleCreateRealPackagePreview}
                    >
                      <Row gutter={[12, 0]}>
                        <Col span={8}>
                          <Form.Item name="max_rows" label="max_rows">
                            <InputNumber min={1} max={20} className="full-width" />
                          </Form.Item>
                        </Col>
                      </Row>
                      <Space direction="vertical" size={4} className="full-width">
                        <Form.Item name="acknowledge_real_package_preview" valuePropName="checked" noStyle>
                          <Checkbox>我确认这是 real package preview，不是 import。</Checkbox>
                        </Form.Item>
                        <Form.Item name="acknowledge_no_import" valuePropName="checked" noStyle>
                          <Checkbox>我确认不会导入 Evidence rows，不会写 Evidence Layer。</Checkbox>
                        </Form.Item>
                        <Form.Item name="acknowledge_preview_not_representative" valuePropName="checked" noStyle>
                          <Checkbox>我确认预览样本不代表全量覆盖、全平台覆盖或官方验证。</Checkbox>
                        </Form.Item>
                        <Form.Item name="acknowledge_privacy_stop" valuePropName="checked" noStyle>
                          <Checkbox>我确认如触发 privacy_stop，应停止并进入隐私/安全复核。</Checkbox>
                        </Form.Item>
                      </Space>
                      <Space wrap className="mt-12">
                        <Button
                          type="primary"
                          htmlType="submit"
                          loading={realPackagePreviewLoading}
                          disabled={realPackagePreviewSubmitDisabled}
                        >
                          生成受限行预览
                        </Button>
                        {latestRealPackagePreview ? (
                          <Button
                            icon={<ClipboardCopy size={16} />}
                            onClick={() => copyText(latestRealPackagePreviewJson, 'Real package row preview JSON copied')}
                          >
                            Copy latest preview JSON
                          </Button>
                        ) : null}
                      </Space>
                    </Form>

                    {latestRealPackagePreview ? (
                      <Card className="panel-card" size="small" title="Latest limited real package row preview">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color={latestRealPackagePreview.status === 'passed' ? 'green' : latestRealPackagePreview.status === 'privacy_stop' ? 'red' : 'gold'}>
                              {latestRealPackagePreview.status}
                            </Tag>
                            <Tag color="blue">{latestRealPackagePreview.execution_mode}</Tag>
                            <Tag color="default">can_import_now: {boolText(latestRealPackagePreview.readiness?.can_import_now)}</Tag>
                            <Tag color="purple">{latestRealPackagePreview.governance_defaults?.trust_label || 'medium_low'}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="preview_run_id">{latestRealPackagePreview.preview_run_id}</Descriptions.Item>
                            <Descriptions.Item label="preflight_id">{latestRealPackagePreview.preflight_id}</Descriptions.Item>
                            <Descriptions.Item label="package">
                              {latestRealPackagePreview.package_reference?.package_name || '-'} / {latestRealPackagePreview.package_reference?.package_role || '-'}
                            </Descriptions.Item>
                            <Descriptions.Item label="limits">
                              max_rows={latestRealPackagePreview.limits?.max_rows || 10},
                              hard_max_rows={latestRealPackagePreview.limits?.hard_max_rows || 20},
                              full_scan={boolText(latestRealPackagePreview.limits?.full_scan)},
                              import_rows={boolText(latestRealPackagePreview.limits?.import_rows)}
                            </Descriptions.Item>
                            <Descriptions.Item label="row counts">
                              rows_seen={latestRealPackagePreview.rows?.rows_seen || 0},
                              accepted={latestRealPackagePreview.rows?.accepted_for_preview || 0},
                              quarantined={latestRealPackagePreview.rows?.quarantined || 0},
                              rejected={latestRealPackagePreview.rows?.rejected || 0},
                              privacy_stop_at_row={latestRealPackagePreview.rows?.privacy_stop_at_row || '-'}
                            </Descriptions.Item>
                            <Descriptions.Item label="privacy scan">
                              raw_author_id={latestRealPackagePreview.privacy_scan?.raw_author_id_detected || 0},
                              raw_author_name={latestRealPackagePreview.privacy_scan?.raw_author_name_detected || 0},
                              profile_url={latestRealPackagePreview.privacy_scan?.profile_url_detected || 0},
                              private_message={latestRealPackagePreview.privacy_scan?.private_message_detected || 0},
                              secret={latestRealPackagePreview.privacy_scan?.secret_like_value_detected || 0},
                              email={latestRealPackagePreview.privacy_scan?.email_detected || 0},
                              phone={latestRealPackagePreview.privacy_scan?.phone_detected || 0},
                              privacy_stop={boolText(latestRealPackagePreview.privacy_scan?.privacy_stop_triggered)}
                            </Descriptions.Item>
                            <Descriptions.Item label="now flags">
                              import={boolText(latestRealPackagePreview.now_flags?.import_evidence_rows_now)},
                              evidence_layer={boolText(latestRealPackagePreview.now_flags?.write_evidence_layer_now)},
                              case={boolText(latestRealPackagePreview.now_flags?.create_case_now)},
                              review_queue={boolText(latestRealPackagePreview.now_flags?.create_review_queue_now)},
                              dedup={boolText(latestRealPackagePreview.now_flags?.run_dedup_now)},
                              analysis={boolText(latestRealPackagePreview.now_flags?.run_analysis_now)},
                              report={boolText(latestRealPackagePreview.now_flags?.generate_report_now)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Preview-only boundary"
                            description="This preview reads at most a tiny capped sample from a selected local package. It does not import evidence, write the Evidence Layer, create cases, run review/dedup/analysis, or generate Sandbox/public event/report output."
                          />
                          <Card size="small" title={`Redacted preview rows (${latestRealPackagePreview.redacted_preview_rows?.length || 0})`}>
                            {latestRealPackagePreview.redacted_preview_rows?.length ? (
                              <Space direction="vertical" size={8} className="full-width">
                                {latestRealPackagePreview.redacted_preview_rows.map((row) => (
                                  <Card size="small" key={row.row_index}>
                                    <Space direction="vertical" size={4} className="full-width">
                                      <Space wrap>
                                        <Tag>{row.status}</Tag>
                                        <Tag color="cyan">{row.evidence_candidate?.platform || '-'}</Tag>
                                        <Tag color="blue">{row.evidence_candidate?.evidence_type || '-'}</Tag>
                                      </Space>
                                      <Text strong>{row.evidence_candidate?.title_preview || '-'}</Text>
                                      <Text type="secondary">{row.evidence_candidate?.body_text_preview || '-'}</Text>
                                      <Text type="secondary">review_status: {row.governance_defaults?.review_status || 'review_needed'} / analysis_included: {boolText(row.governance_defaults?.analysis_included)}</Text>
                                    </Space>
                                  </Card>
                                ))}
                              </Space>
                            ) : (
                              <Text type="secondary">No accepted preview rows.</Text>
                            )}
                          </Card>
                          <SummaryList title="Quarantine summary" items={(latestRealPackagePreview.quarantine_summary || []).map((item) => `row ${item.row_index}: ${item.reason_code} (${(item.forbidden_fields_detected || []).join(', ')})`)} />
                          <SummaryList title="Rejection summary" items={(latestRealPackagePreview.rejection_summary || []).map((item) => `row ${item.row_index}: ${item.reason_code}`)} />
                          <SummaryList title="Warnings" items={latestRealPackagePreview.warnings || []} />
                          <SummaryList title="Boundary notes" items={latestRealPackagePreview.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={latestRealPackagePreview.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title={`Existing limited real package previews (${realPackagePreviews.length})`}>
                      {realPackagePreviews.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {realPackagePreviews.map((preview) => (
                            <Card size="small" key={preview.preview_run_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="blue">{preview.execution_mode}</Tag>
                                  <Tag>{preview.status}</Tag>
                                  <Text type="secondary">{preview.preview_run_id}</Text>
                                </Space>
                                <Text>package: {preview.package_reference?.package_name || '-'}</Text>
                                <Text type="secondary">
                                  accepted={preview.rows?.accepted_for_preview || 0}, quarantined={preview.rows?.quarantined || 0}, rejected={preview.rows?.rejected || 0}
                                </Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No limited real package row previews yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Card size="small" title="Review-only Case / 复核专用 Case 容器">
                  <Space direction="vertical" size={12} className="full-width">
                    <Alert
                      type={reviewOnlyCaseGate.eligible ? 'warning' : 'info'}
                      showIcon
                      message={reviewOnlyCaseGate.eligible ? 'Ready to create review-only container' : 'Review-only case not ready'}
                      description={
                        latestReviewOnlyCase
                          ? 'A review-only governance container already exists for this request.'
                          : reviewOnlyCaseGate.reason
                      }
                    />
                    <Text type="secondary">
                      Only creates an internal governance container. It does not import evidence rows, write the Evidence Layer,
                      create a production case, create review queue items, run dedup, run analysis, generate Sandbox output,
                      generate public event pages, or generate reports. Provider output is evidence, not official truth.
                    </Text>
                    {reviewOnlyCaseError ? <Alert type="error" showIcon message={reviewOnlyCaseError} /> : null}
                    <Form
                      form={reviewOnlyCaseForm}
                      layout="vertical"
                      initialValues={{ target_case_mode: 'new_review_case', target_case_id: '' }}
                      onFinish={handleCreateReviewOnlyCase}
                    >
                      <Row gutter={[12, 0]}>
                        <Col span={12}>
                          <Form.Item name="target_case_mode" label="target_case_mode">
                            <Select
                              options={[
                                { value: 'new_review_case', label: 'new_review_case' },
                                { value: 'existing_case_review_wrapper', label: 'existing_case_review_wrapper' },
                              ]}
                            />
                          </Form.Item>
                        </Col>
                        {watchedReviewOnlyCaseMode === 'existing_case_review_wrapper' ? (
                          <Col span={12}>
                            <Form.Item name="target_case_id" label="target_case_id">
                              <Input placeholder="case_xxx for review wrapper only" />
                            </Form.Item>
                          </Col>
                        ) : null}
                      </Row>
                      <Space wrap>
                        <Button
                          type="primary"
                          htmlType="submit"
                          loading={reviewOnlyCaseLoading}
                          disabled={reviewOnlyCaseSubmitDisabled}
                        >
                          Create Review-only Case container
                        </Button>
                        {latestReviewOnlyCase ? (
                          <Button
                            icon={<ClipboardCopy size={16} />}
                            onClick={() => copyText(latestReviewOnlyCaseJson, 'Review-only case JSON copied')}
                          >
                            Copy latest review-only case JSON
                          </Button>
                        ) : null}
                      </Space>
                    </Form>

                    {latestReviewOnlyCase ? (
                      <Card className="panel-card" size="small" title="Latest review-only case container">
                        <Space direction="vertical" size={12} className="full-width">
                          <Space wrap>
                            <Tag color="gold">{latestReviewOnlyCase.status}</Tag>
                            <Tag color="blue">{latestReviewOnlyCase.visibility}</Tag>
                            <Tag color="default">analysis_included: {boolText(latestReviewOnlyCase.analysis_included)}</Tag>
                            <Tag color="default">public_visible: {boolText(latestReviewOnlyCase.public_visible)}</Tag>
                            <Tag color="default">evidence_rows_imported: {boolText(latestReviewOnlyCase.evidence_rows_imported)}</Tag>
                          </Space>
                          <Descriptions column={1} size="small">
                            <Descriptions.Item label="review_case_id">{latestReviewOnlyCase.review_case_id}</Descriptions.Item>
                            <Descriptions.Item label="source_preview_run_id">{latestReviewOnlyCase.source_preview_run_id}</Descriptions.Item>
                            <Descriptions.Item label="source_preflight_id">{latestReviewOnlyCase.source_preflight_id}</Descriptions.Item>
                            <Descriptions.Item label="package">
                              {latestReviewOnlyCase.package_reference?.package_name || '-'} / {latestReviewOnlyCase.package_reference?.package_role || '-'}
                            </Descriptions.Item>
                            <Descriptions.Item label="preview summary">
                              status={latestReviewOnlyCase.source_preview_summary?.status || '-'},
                              rows_seen={latestReviewOnlyCase.source_preview_summary?.rows_seen || 0},
                              accepted={latestReviewOnlyCase.source_preview_summary?.accepted_for_preview || 0},
                              quarantined={latestReviewOnlyCase.source_preview_summary?.quarantined || 0},
                              rejected={latestReviewOnlyCase.source_preview_summary?.rejected || 0},
                              privacy_stop={boolText(latestReviewOnlyCase.source_preview_summary?.privacy_stop_triggered)}
                            </Descriptions.Item>
                            <Descriptions.Item label="coverage">
                              level={latestReviewOnlyCase.coverage?.coverage_level || '-'},
                              not_full_web={boolText(latestReviewOnlyCase.coverage?.not_full_web)},
                              not_full_platform={boolText(latestReviewOnlyCase.coverage?.not_full_platform)},
                              not_full_thread={boolText(latestReviewOnlyCase.coverage?.not_full_thread)}
                            </Descriptions.Item>
                            <Descriptions.Item label="governance defaults">
                              review_status={latestReviewOnlyCase.governance_defaults?.review_status || 'review_needed'},
                              verification_status={latestReviewOnlyCase.governance_defaults?.verification_status || 'source_url_provided_unverified'},
                              trust_label={latestReviewOnlyCase.governance_defaults?.trust_label || 'medium_low'},
                              analysis_included={boolText(latestReviewOnlyCase.governance_defaults?.analysis_included)}
                            </Descriptions.Item>
                            <Descriptions.Item label="target case">
                              mode={latestReviewOnlyCase.target_case_reference?.mode || 'new_review_case'},
                              target_case_id={latestReviewOnlyCase.target_case_reference?.target_case_id || '-'},
                              attach_now={boolText(latestReviewOnlyCase.target_case_reference?.attach_to_production_case_now)}
                            </Descriptions.Item>
                            <Descriptions.Item label="readiness">
                              state={latestReviewOnlyCase.readiness?.state || '-'},
                              can_import_rows_now={boolText(latestReviewOnlyCase.readiness?.can_import_rows_now)},
                              can_run_analysis_now={boolText(latestReviewOnlyCase.readiness?.can_run_analysis_now)},
                              can_generate_report_now={boolText(latestReviewOnlyCase.readiness?.can_generate_report_now)}
                            </Descriptions.Item>
                          </Descriptions>
                          <Alert
                            type="warning"
                            showIcon
                            message="Review-only boundary"
                            description="This is not a production case, not analysis-ready, not public, not full-web coverage, and not official verification. Analysis, Sandbox, public event and report generation remain disabled until future staging, review, dedup, audit and promotion gates."
                          />
                          <SummaryList title="Allowed actions" items={latestReviewOnlyCase.allowed_actions || []} />
                          <SummaryList title="Blocked actions" items={latestReviewOnlyCase.blocked_actions || []} />
                          <SummaryList title="Promotion requirements" items={latestReviewOnlyCase.promotion_requirements || []} />
                          <SummaryList title="Boundary notes" items={latestReviewOnlyCase.boundary_notes || []} />
                          <SummaryList title="Recommended next steps" items={latestReviewOnlyCase.recommended_next_steps || []} />
                        </Space>
                      </Card>
                    ) : null}

                    <Card size="small" title="Review-only Staging Import / 复核暂存导入">
                      <Space direction="vertical" size={12} className="full-width">
                        <Alert
                          type={stagingImportGate.eligible ? 'warning' : 'info'}
                          showIcon
                          message={stagingImportGate.eligible ? 'Ready for review-only staging import' : 'Review-only staging import not ready'}
                          description={
                            latestStagingImport
                              ? 'A review-only staging import already exists for this request.'
                              : stagingImportGate.reason
                          }
                        />
                        <Alert
                          type="warning"
                          showIcon
                          message="Review-only staging boundary"
                          description="Only accepted redacted preview rows become review-only staged evidence candidates. This does not write the production Evidence Layer, create a production case, create a review queue, run dedup, run analysis, generate reports, generate Sandbox output, or make provider output official truth."
                        />
                        {stagingImportError ? <Alert type="error" showIcon message={stagingImportError} /> : null}
                        <Form
                          form={stagingImportForm}
                          layout="vertical"
                          initialValues={{
                            review_case_id: latestReviewOnlyCase?.review_case_id || '',
                            preview_run_id: latestReviewOnlyCase?.source_preview_run_id || latestRealPackagePreview?.preview_run_id || '',
                          }}
                          onFinish={handleCreateStagingImport}
                        >
                          <Row gutter={[12, 0]}>
                            <Col span={12}>
                              <Form.Item name="review_case_id" label="review_case_id">
                                <Select
                                  placeholder={latestReviewOnlyCase?.review_case_id || 'select review-only case'}
                                  options={reviewOnlyCases.map((reviewCase) => ({
                                    value: reviewCase.review_case_id,
                                    label: reviewCase.review_case_id,
                                  }))}
                                />
                              </Form.Item>
                            </Col>
                            <Col span={12}>
                              <Form.Item name="preview_run_id" label="preview_run_id">
                                <Select
                                  placeholder={latestReviewOnlyCase?.source_preview_run_id || latestRealPackagePreview?.preview_run_id || 'select preview'}
                                  options={realPackagePreviews.map((preview) => ({
                                    value: preview.preview_run_id,
                                    label: `${preview.preview_run_id} / ${preview.status}`,
                                  }))}
                                />
                              </Form.Item>
                            </Col>
                          </Row>
                          <Row gutter={[12, 0]}>
                            <Col span={12}>
                              <Form.Item name="acknowledge_review_only_staging" valuePropName="checked">
                                <Checkbox>Confirm this is review-only staging, not production import.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                <Checkbox>Confirm no production Evidence Layer write.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_production_case" valuePropName="checked">
                                <Checkbox>Confirm no production case creation.</Checkbox>
                              </Form.Item>
                            </Col>
                            <Col span={12}>
                              <Form.Item name="acknowledge_no_analysis" valuePropName="checked">
                                <Checkbox>Confirm no analysis, dedup, or review queue run now.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                <Checkbox>Confirm no report, Sandbox, or public event output.</Checkbox>
                              </Form.Item>
                            </Col>
                          </Row>
                          <Space wrap>
                            <Button
                              type="primary"
                              htmlType="submit"
                              loading={stagingImportLoading}
                              disabled={stagingImportSubmitDisabled}
                            >
                              Create review-only staging import
                            </Button>
                            {latestStagingImport ? (
                              <Button
                                icon={<ClipboardCopy size={16} />}
                                onClick={() => copyText(latestStagingImportJson, 'Staging import JSON copied')}
                              >
                                Copy latest staging import JSON
                              </Button>
                            ) : null}
                            {stagedCandidateBatch ? (
                              <Button
                                icon={<ClipboardCopy size={16} />}
                                onClick={() => copyText(stagedCandidateBatchJson, 'Staged candidates JSON copied')}
                              >
                                Copy staged candidates JSON
                              </Button>
                            ) : null}
                          </Space>
                        </Form>

                        {latestStagingImport ? (
                          <Card className="panel-card" size="small" title="Latest review-only staging import">
                            <Space direction="vertical" size={12} className="full-width">
                              <Space wrap>
                                <Tag color={latestStagingImport.status === 'completed' ? 'green' : 'gold'}>
                                  {latestStagingImport.status}
                                </Tag>
                                <Tag color="blue">{latestStagingImport.execution_mode}</Tag>
                                <Tag color="default">analysis_included: {boolText(latestStagingImport.default_governance?.analysis_included)}</Tag>
                                <Tag color="default">evidence_layer_written: {boolText(latestStagingImport.target?.evidence_layer_written)}</Tag>
                              </Space>
                              <Descriptions column={1} size="small">
                                <Descriptions.Item label="staging_import_id">{latestStagingImport.staging_import_id}</Descriptions.Item>
                                <Descriptions.Item label="review_case_id">{latestStagingImport.review_case_id}</Descriptions.Item>
                                <Descriptions.Item label="source_preview_run_id">{latestStagingImport.source_preview_run_id}</Descriptions.Item>
                                <Descriptions.Item label="package">{latestStagingImport.package_name || '-'}</Descriptions.Item>
                                <Descriptions.Item label="counts">
                                  preview_seen={latestStagingImport.counts?.preview_rows_seen || 0},
                                  accepted={latestStagingImport.counts?.accepted_for_staging || 0},
                                  quarantined={latestStagingImport.counts?.quarantined_from_staging || 0},
                                  rejected={latestStagingImport.counts?.rejected_from_staging || 0},
                                  privacy_stop={boolText(latestStagingImport.counts?.privacy_stop)}
                                </Descriptions.Item>
                                <Descriptions.Item label="governance">
                                  review_status={latestStagingImport.default_governance?.review_status || 'review_needed'},
                                  verification={latestStagingImport.default_governance?.verification_status || 'source_url_provided_unverified'},
                                  trust={latestStagingImport.default_governance?.trust_label || 'medium_low'},
                                  dedup_required={boolText(latestStagingImport.default_governance?.dedup_required)}
                                </Descriptions.Item>
                                <Descriptions.Item label="readiness">
                                  state={latestStagingImport.readiness?.state || '-'},
                                  can_run_analysis_now={boolText(latestStagingImport.readiness?.can_run_analysis_now)},
                                  can_generate_report_now={boolText(latestStagingImport.readiness?.can_generate_report_now)},
                                  requires_review_queue_phase={boolText(latestStagingImport.readiness?.requires_review_queue_phase)}
                                </Descriptions.Item>
                                <Descriptions.Item label="rollback">
                                  available={boolText(latestStagingImport.rollback?.rollback_available)},
                                  rollback_id={latestStagingImport.rollback?.rollback_id || '-'},
                                  required_before_analysis={boolText(latestStagingImport.rollback?.rollback_required_before_analysis)}
                                </Descriptions.Item>
                              </Descriptions>
                              <SummaryList title="Boundary notes" items={latestStagingImport.boundary_notes || []} />
                              <SummaryList title="Recommended next steps" items={latestStagingImport.recommended_next_steps || []} />
                            </Space>
                          </Card>
                        ) : null}

                        <Card size="small" title={`Staged evidence candidates (${stagedCandidateBatch?.candidates?.length || 0})`}>
                          {stagedCandidateBatch?.candidates?.length ? (
                            <Space direction="vertical" size={8} className="full-width">
                              {stagedCandidateBatch.candidates.slice(0, 5).map((candidate) => (
                                <Card size="small" key={candidate.staging_id}>
                                  <Space direction="vertical" size={4} className="full-width">
                                    <Space wrap>
                                      <Tag color="gold">{candidate.row_status}</Tag>
                                      <Tag color="default">review_status: {candidate.governance?.review_status || 'review_needed'}</Tag>
                                      <Tag color="default">analysis_included: {boolText(candidate.governance?.analysis_included)}</Tag>
                                      <Tag color="default">dedup_required: {boolText(candidate.governance?.dedup_required)}</Tag>
                                    </Space>
                                    <Text strong>{candidate.evidence_candidate?.title_preview || 'Untitled staged candidate'}</Text>
                                    <Text type="secondary">{candidate.evidence_candidate?.body_text_preview || '-'}</Text>
                                    <Text type="secondary">
                                      source_url={candidate.evidence_candidate?.source_url || '-'}; verification=
                                      {candidate.governance?.verification_status || 'source_url_provided_unverified'}; trust=
                                      {candidate.governance?.trust_label || 'medium_low'}
                                    </Text>
                                  </Space>
                                </Card>
                              ))}
                            </Space>
                          ) : (
                            <Text type="secondary">No staged evidence candidates yet.</Text>
                          )}
                        </Card>

                        <Card size="small" title={`Existing staging imports (${stagingImports.length})`}>
                          {stagingImports.length ? (
                            <Space direction="vertical" size={8} className="full-width">
                              {stagingImports.map((item) => (
                                <Card size="small" key={item.staging_import_id}>
                                  <Space direction="vertical" size={4} className="full-width">
                                    <Space wrap>
                                      <Tag color={item.status === 'completed' ? 'green' : 'gold'}>{item.status}</Tag>
                                      <Text type="secondary">{item.staging_import_id}</Text>
                                    </Space>
                                    <Text>package: {item.package_name || '-'}</Text>
                                    <Text type="secondary">
                                      accepted_for_staging={item.counts?.accepted_for_staging || 0}, analysis_included=
                                      {boolText(item.default_governance?.analysis_included)}, evidence_layer_written=
                                      {boolText(item.target?.evidence_layer_written)}
                                    </Text>
                                  </Space>
                                </Card>
                              ))}
                            </Space>
                          ) : (
                            <Text type="secondary">No review-only staging imports yet.</Text>
                          )}
                        </Card>
                      </Space>
                    </Card>

                    <Card size="small" title="Review Queue Initialization / 复核队列初始化">
                      <Space direction="vertical" size={12} className="full-width">
                        <Alert
                          type={reviewQueueInitGate.eligible ? 'warning' : 'info'}
                          showIcon
                          message={reviewQueueInitGate.eligible ? 'Ready to initialize review-only queue' : 'Review queue initialization not ready'}
                          description={
                            latestReviewQueueInitialization
                              ? 'A review-only queue initialization already exists for this request.'
                              : reviewQueueInitGate.reason
                          }
                        />
                        <Alert
                          type="warning"
                          showIcon
                          message="Review-only queue boundary"
                          description="Only staged evidence candidates become review-only queue items. This does not write the production Evidence Layer, create a production case, create a production review queue, run dedup, run analysis, generate reports, generate Sandbox output, or make provider output official truth. Duplicate evidence must not amplify risk."
                        />
                        {reviewQueueInitError ? <Alert type="error" showIcon message={reviewQueueInitError} /> : null}
                        <Form
                          form={reviewQueueInitForm}
                          layout="vertical"
                          initialValues={{
                            review_case_id: latestReviewOnlyCase?.review_case_id || '',
                            staging_import_id: latestStagingImport?.staging_import_id || '',
                          }}
                          onFinish={handleCreateReviewQueueInitialization}
                        >
                          <Row gutter={[12, 0]}>
                            <Col span={12}>
                              <Form.Item name="review_case_id" label="review_case_id">
                                <Select
                                  placeholder={latestReviewOnlyCase?.review_case_id || 'select review-only case'}
                                  options={reviewOnlyCases.map((reviewCase) => ({
                                    value: reviewCase.review_case_id,
                                    label: reviewCase.review_case_id,
                                  }))}
                                />
                              </Form.Item>
                            </Col>
                            <Col span={12}>
                              <Form.Item name="staging_import_id" label="staging_import_id">
                                <Select
                                  placeholder={latestStagingImport?.staging_import_id || 'select staging import'}
                                  options={stagingImports.map((item) => ({
                                    value: item.staging_import_id,
                                    label: `${item.staging_import_id} / ${item.status}`,
                                  }))}
                                />
                              </Form.Item>
                            </Col>
                          </Row>
                          <Row gutter={[12, 0]}>
                            <Col span={12}>
                              <Form.Item name="acknowledge_review_only_queue" valuePropName="checked">
                                <Checkbox>Confirm this is review-only queue initialization, not production review.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                <Checkbox>Confirm no production Evidence Layer write.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_production_case" valuePropName="checked">
                                <Checkbox>Confirm no production case creation.</Checkbox>
                              </Form.Item>
                            </Col>
                            <Col span={12}>
                              <Form.Item name="acknowledge_no_dedup" valuePropName="checked">
                                <Checkbox>Confirm no dedup run.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_analysis" valuePropName="checked">
                                <Checkbox>Confirm no analysis run.</Checkbox>
                              </Form.Item>
                              <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                <Checkbox>Confirm no report, Sandbox, or public event output.</Checkbox>
                              </Form.Item>
                            </Col>
                          </Row>
                          <Space wrap>
                            <Button
                              type="primary"
                              htmlType="submit"
                              loading={reviewQueueInitLoading}
                              disabled={reviewQueueInitSubmitDisabled}
                            >
                              Initialize review-only queue
                            </Button>
                            {latestReviewQueueInitialization ? (
                              <Button
                                icon={<ClipboardCopy size={16} />}
                                onClick={() => copyText(latestReviewQueueInitializationJson, 'Review queue initialization JSON copied')}
                              >
                                Copy latest queue init JSON
                              </Button>
                            ) : null}
                            {reviewQueueItemBatch ? (
                              <Button
                                icon={<ClipboardCopy size={16} />}
                                onClick={() => copyText(reviewQueueItemBatchJson, 'Review queue items JSON copied')}
                              >
                                Copy review queue items JSON
                              </Button>
                            ) : null}
                          </Space>
                        </Form>

                        {latestReviewQueueInitialization ? (
                          <Card className="panel-card" size="small" title="Latest review queue initialization">
                            <Space direction="vertical" size={12} className="full-width">
                              <Space wrap>
                                <Tag color={latestReviewQueueInitialization.status === 'completed' ? 'green' : 'gold'}>
                                  {latestReviewQueueInitialization.status}
                                </Tag>
                                <Tag color="blue">{latestReviewQueueInitialization.execution_mode}</Tag>
                                <Tag color="default">queue_status: {latestReviewQueueInitialization.defaults?.queue_status || 'review_needed'}</Tag>
                                <Tag color="default">analysis_included: {boolText(latestReviewQueueInitialization.defaults?.analysis_included)}</Tag>
                              </Space>
                              <Descriptions column={1} size="small">
                                <Descriptions.Item label="queue_init_id">{latestReviewQueueInitialization.queue_init_id}</Descriptions.Item>
                                <Descriptions.Item label="review_case_id">{latestReviewQueueInitialization.review_case_id}</Descriptions.Item>
                                <Descriptions.Item label="staging_import_id">{latestReviewQueueInitialization.staging_import_id}</Descriptions.Item>
                                <Descriptions.Item label="package">{latestReviewQueueInitialization.package_name || '-'}</Descriptions.Item>
                                <Descriptions.Item label="counts">
                                  staged_seen={latestReviewQueueInitialization.counts?.staged_candidates_seen || 0},
                                  items_created={latestReviewQueueInitialization.counts?.queue_items_created || 0},
                                  excluded={latestReviewQueueInitialization.counts?.excluded_candidates || 0},
                                  privacy_hold={latestReviewQueueInitialization.counts?.privacy_hold_items || 0}
                                </Descriptions.Item>
                                <Descriptions.Item label="defaults">
                                  review_status={latestReviewQueueInitialization.defaults?.review_status || 'review_needed'},
                                  verification={latestReviewQueueInitialization.defaults?.verification_status || 'source_url_provided_unverified'},
                                  trust={latestReviewQueueInitialization.defaults?.trust_label || 'medium_low'},
                                  dedup_required={boolText(latestReviewQueueInitialization.defaults?.dedup_required)}
                                </Descriptions.Item>
                                <Descriptions.Item label="target">
                                  production_case_created={boolText(latestReviewQueueInitialization.target?.production_case_created)},
                                  evidence_layer_written={boolText(latestReviewQueueInitialization.target?.evidence_layer_written)},
                                  production_review_queue_created={boolText(latestReviewQueueInitialization.target?.production_review_queue_created)}
                                </Descriptions.Item>
                                <Descriptions.Item label="readiness">
                                  state={latestReviewQueueInitialization.readiness?.state || '-'},
                                  can_run_analysis_now={boolText(latestReviewQueueInitialization.readiness?.can_run_analysis_now)},
                                  can_generate_report_now={boolText(latestReviewQueueInitialization.readiness?.can_generate_report_now)},
                                  requires_review_actions_phase={boolText(latestReviewQueueInitialization.readiness?.requires_review_actions_phase)},
                                  requires_dedup_phase={boolText(latestReviewQueueInitialization.readiness?.requires_dedup_phase)}
                                </Descriptions.Item>
                              </Descriptions>
                              <SummaryList title="Boundary notes" items={latestReviewQueueInitialization.boundary_notes || []} />
                              <SummaryList title="Recommended next steps" items={latestReviewQueueInitialization.recommended_next_steps || []} />
                            </Space>
                          </Card>
                        ) : null}

                        <Card size="small" title={`Review queue items (${reviewQueueItemBatch?.items?.length || 0})`}>
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Review action boundary"
                              description="Approve only makes an item eligible for future dedup; it does not include it in analysis. Reject keeps the item audit-visible but analysis-excluded. Weak evidence remains warning-marked. Duplicate merge does not run dedup and must not amplify risk. Privacy hold blocks all downstream steps."
                            />
                            {reviewQueueActionError ? <Alert type="error" showIcon message={reviewQueueActionError} /> : null}
                            <Form
                              form={reviewQueueActionForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'human_reviewer',
                                acknowledge_review_only_action: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_no_dedup: true,
                                acknowledge_no_analysis: true,
                                acknowledge_no_report: true,
                              }}
                            >
                              <Row gutter={[12, 0]}>
                                <Col span={8}>
                                  <Form.Item label="reviewer_label" name="reviewer_label">
                                    <Input placeholder="human_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col span={8}>
                                  <Form.Item label="duplicate_group_id" name="duplicate_group_id">
                                    <Input placeholder="optional for merge_duplicate" />
                                  </Form.Item>
                                </Col>
                                <Col span={8}>
                                  <Form.Item label="duplicate_of_review_item_id" name="duplicate_of_review_item_id">
                                    <Input placeholder="optional for merge_duplicate" />
                                  </Form.Item>
                                </Col>
                                <Col span={24}>
                                  <Form.Item label="review note" name="note">
                                    <TextArea rows={2} placeholder="Required for reject, mark weak, request more source, merge duplicate, hold, and reset." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={[12, 0]}>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_review_only_action" valuePropName="checked">
                                    <Checkbox>Confirm this is a review-only action.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                    <Checkbox>Confirm no Evidence Layer write.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_production_case" valuePropName="checked">
                                    <Checkbox>Confirm no production case update.</Checkbox>
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_no_dedup" valuePropName="checked">
                                    <Checkbox>Confirm no dedup run.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_analysis" valuePropName="checked">
                                    <Checkbox>Confirm no analysis run.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                    <Checkbox>Confirm no report, Sandbox, or public event output.</Checkbox>
                                  </Form.Item>
                                </Col>
                              </Row>
                            </Form>
                            {reviewQueueItemBatch?.items?.length ? (
                              <Space direction="vertical" size={8} className="full-width">
                                {reviewQueueItemBatch.items.slice(0, 5).map((item) => {
                                  const itemAudits = reviewQueueAuditsByItem[item.review_item_id] || []
                                  const loadingPrefix = `${item.review_item_id}:`
                                  return (
                                    <Card size="small" key={item.review_item_id}>
                                      <Space direction="vertical" size={8} className="full-width">
                                        <Space wrap>
                                          <Tag color={item.queue_status === 'approved' ? 'green' : item.queue_status === 'rejected' ? 'red' : 'gold'}>
                                            {item.queue_status}
                                          </Tag>
                                          <Tag color="default">analysis_included: {boolText(item.governance?.analysis_included)}</Tag>
                                          <Tag color="default">dedup_status: {item.dedup?.dedup_status || 'not_run'}</Tag>
                                          <Tag color="default">may_amplify_risk: {boolText(item.dedup?.may_amplify_risk)}</Tag>
                                          <Tag color="blue">audits: {itemAudits.length}</Tag>
                                        </Space>
                                        <Text type="secondary">{item.review_item_id}</Text>
                                        <Text strong>{item.evidence_candidate?.title_preview || 'Untitled review queue item'}</Text>
                                        <Text type="secondary">{item.evidence_candidate?.body_text_preview || '-'}</Text>
                                        <Text type="secondary">
                                          source_url={item.evidence_candidate?.source_url || '-'}; verification=
                                          {item.governance?.verification_status || 'source_url_provided_unverified'}; trust=
                                          {item.governance?.trust_label || 'medium_low'}
                                        </Text>
                                        <Space wrap>
                                          {[
                                            ['approve', 'Approve'],
                                            ['reject', 'Reject'],
                                            ['mark_weak', 'Mark weak'],
                                            ['request_more_source', 'Request source'],
                                            ['merge_duplicate', 'Merge duplicate'],
                                            ['hold_for_privacy_review', 'Privacy hold'],
                                            ['reset_review', 'Reset review'],
                                          ].map(([action, label]) => (
                                            <Button
                                              key={action}
                                              size="small"
                                              danger={action === 'reject' || action === 'hold_for_privacy_review'}
                                              loading={reviewQueueActionLoading === `${item.review_item_id}:${action}`}
                                              disabled={!reviewQueueActionReady || reviewQueueActionLoading.startsWith(loadingPrefix)}
                                              onClick={() => handleReviewQueueAction(item, action)}
                                            >
                                              {label}
                                            </Button>
                                          ))}
                                        </Space>
                                        {itemAudits.length ? (
                                          <Card size="small" title="Audit timeline">
                                            <Space direction="vertical" size={4} className="full-width">
                                              {itemAudits.map((audit) => (
                                                <Text type="secondary" key={audit.audit_id}>
                                                  {audit.reviewed_at || '-'} / {audit.action}: {audit.previous_status} -&gt; {audit.new_status}; effect=
                                                  {audit.analysis_effect}; reviewer={audit.reviewer_label || '-'}
                                                </Text>
                                              ))}
                                            </Space>
                                          </Card>
                                        ) : null}
                                      </Space>
                                    </Card>
                                  )
                                })}
                              </Space>
                            ) : (
                              <Text type="secondary">No review queue items yet.</Text>
                            )}
                            {reviewQueueActionAudits.length ? (
                              <Space wrap>
                                <Tag color="blue">request audits: {reviewQueueActionAudits.length}</Tag>
                                <Button
                                  size="small"
                                  icon={<ClipboardCopy size={16} />}
                                  onClick={() => copyText(reviewQueueActionAuditsJson, 'Review queue audit JSON copied')}
                                >
                                  Copy audit timeline JSON
                                </Button>
                              </Space>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Review Queue Completion Gate / 复核完成门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Completion gate boundary"
                              description="Completion gate only evaluates whether local review-only queue status can be considered for a future dedup preview. It does not run dedup, does not run analysis, does not write the Evidence Layer, does not make items public, and does not generate reports, Sandbox fixtures, or public event pages."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Safe interpretation"
                              description="Rejected evidence remains audit-visible but analysis-excluded. Weak evidence remains warning-marked. Duplicate evidence must not amplify risk. A complete gate is not evidence verification and is not analysis readiness."
                            />
                            {reviewQueueCompletionGateError ? <Alert type="error" showIcon message={reviewQueueCompletionGateError} /> : null}
                            <Form
                              form={reviewQueueCompletionGateForm}
                              layout="vertical"
                              initialValues={{
                                queue_init_id: latestReviewQueueInitialization?.queue_init_id || '',
                                review_case_id: latestReviewQueueInitialization?.review_case_id || '',
                                minimum_reviewed_ratio: 1,
                                allow_deferred_items: false,
                                acknowledge_completion_is_not_dedup: true,
                                acknowledge_completion_is_not_analysis: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_no_report: true,
                              }}
                              onFinish={handleCreateReviewQueueCompletionGate}
                            >
                              <Row gutter={[12, 0]}>
                                <Col span={12}>
                                  <Form.Item label="queue_init_id" name="queue_init_id">
                                    <Select
                                      placeholder="Select review queue initialization"
                                      options={reviewQueueInitializations.map((item) => ({
                                        value: item.queue_init_id,
                                        label: item.queue_init_id,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item label="review_case_id" name="review_case_id">
                                    <Input placeholder={latestReviewQueueInitialization?.review_case_id || 'review_only_case_id'} />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item label="minimum_reviewed_ratio" name="minimum_reviewed_ratio">
                                    <InputNumber min={0} max={1} step={0.05} className="full-width" />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item name="allow_deferred_items" valuePropName="checked">
                                    <Checkbox>Allow needs_more_source items only as explicitly deferred local review items.</Checkbox>
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={[12, 0]}>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_completion_is_not_dedup" valuePropName="checked">
                                    <Checkbox>Completion is not dedup.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_completion_is_not_analysis" valuePropName="checked">
                                    <Checkbox>Completion is not analysis.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                    <Checkbox>No Evidence Layer write.</Checkbox>
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_no_production_case" valuePropName="checked">
                                    <Checkbox>No production case creation or update.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                    <Checkbox>No report, Sandbox, or public event generation.</Checkbox>
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  loading={reviewQueueCompletionGateLoading}
                                  disabled={!reviewQueueCompletionReady || reviewQueueCompletionGateLoading}
                                >
                                  Evaluate review completion gate
                                </Button>
                                {latestReviewQueueCompletionGate ? (
                                  <Button
                                    icon={<ClipboardCopy size={16} />}
                                    onClick={() => copyText(latestReviewQueueCompletionGateJson, 'Review completion gate JSON copied')}
                                  >
                                    Copy latest completion gate JSON
                                  </Button>
                                ) : null}
                                {reviewQueueCompletionGates.length ? (
                                  <Button
                                    icon={<ClipboardCopy size={16} />}
                                    onClick={() => copyText(reviewQueueCompletionGatesJson, 'Review completion gate history JSON copied')}
                                  >
                                    Copy completion gate history JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>

                            {latestReviewQueueCompletionGate ? (
                              <Card size="small" title="Latest completion gate">
                                <Space direction="vertical" size={10} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestReviewQueueCompletionGate.status === 'complete_enough_for_future_dedup_preview' ? 'green' : latestReviewQueueCompletionGate.status === 'blocked' ? 'red' : 'gold'}>
                                      {latestReviewQueueCompletionGate.status}
                                    </Tag>
                                    <Tag color="default">eligible_for_future_dedup_preview: {boolText(latestReviewQueueCompletionGate.downstream_eligibility?.eligible_for_future_dedup_preview)}</Tag>
                                    <Tag color="default">run_dedup_now: {boolText(latestReviewQueueCompletionGate.now_flags?.run_dedup_now)}</Tag>
                                    <Tag color="default">run_analysis_now: {boolText(latestReviewQueueCompletionGate.now_flags?.run_analysis_now)}</Tag>
                                  </Space>
                                  <Descriptions column={1} size="small">
                                    <Descriptions.Item label="completion_gate_id">{latestReviewQueueCompletionGate.completion_gate_id}</Descriptions.Item>
                                    <Descriptions.Item label="counts">
                                      total={latestReviewQueueCompletionGate.counts?.total_items || 0},
                                      reviewed={latestReviewQueueCompletionGate.counts?.reviewed_count || 0},
                                      ratio={latestReviewQueueCompletionGate.counts?.reviewed_ratio || 0},
                                      review_needed={latestReviewQueueCompletionGate.counts?.review_needed || 0},
                                      approved={latestReviewQueueCompletionGate.counts?.approved || 0},
                                      rejected={latestReviewQueueCompletionGate.counts?.rejected || 0},
                                      weak={latestReviewQueueCompletionGate.counts?.marked_weak || 0},
                                      duplicate_merged={latestReviewQueueCompletionGate.counts?.duplicate_merged || 0},
                                      privacy_hold={latestReviewQueueCompletionGate.counts?.privacy_hold || 0}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="audit_summary">
                                      items_with_audit={latestReviewQueueCompletionGate.audit_summary?.items_with_audit || 0},
                                      missing_audit={latestReviewQueueCompletionGate.audit_summary?.items_missing_audit || 0},
                                      latest_action_at={latestReviewQueueCompletionGate.audit_summary?.latest_action_at || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream">
                                      can_run_dedup_now={boolText(latestReviewQueueCompletionGate.downstream_eligibility?.can_run_dedup_now)},
                                      can_run_analysis_now={boolText(latestReviewQueueCompletionGate.downstream_eligibility?.can_run_analysis_now)},
                                      can_generate_report_now={boolText(latestReviewQueueCompletionGate.downstream_eligibility?.can_generate_report_now)}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <SummaryList title="Blocked reasons" items={latestReviewQueueCompletionGate.blocked_reasons || []} />
                                  <SummaryList title="Warnings" items={latestReviewQueueCompletionGate.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestReviewQueueCompletionGate.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestReviewQueueCompletionGate.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No completion gate record yet.</Text>
                            )}

                            {reviewQueueCompletionGates.length ? (
                              <Card size="small" title={`Existing completion gate records (${reviewQueueCompletionGates.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {reviewQueueCompletionGates.map((item) => (
                                    <Space wrap key={item.completion_gate_id}>
                                      <Tag color={item.status === 'complete_enough_for_future_dedup_preview' ? 'green' : item.status === 'blocked' ? 'red' : 'gold'}>
                                        {item.status}
                                      </Tag>
                                      <Text type="secondary">{item.completion_gate_id}</Text>
                                      <Text type="secondary">reviewed_ratio={item.counts?.reviewed_ratio || 0}</Text>
                                      <Text type="secondary">created_at={item.created_at || '-'}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Dedup Preview / 重复证据预览">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Dedup preview boundary"
                              description="Dedup preview only creates duplicate group candidates from local review-only queue items. It does not run production dedup, does not write the Evidence Layer, does not run analysis, does not generate reports, and does not make evidence verified or analysis-ready."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Safe interpretation"
                              description="Duplicate evidence must not amplify risk, sentiment, coverage, or conclusions. Human confirmation and a later analysis promotion gate are required before any merge or analysis effect."
                            />
                            {dedupPreviewError ? <Alert type="error" showIcon message={dedupPreviewError} /> : null}
                            <Form
                              form={dedupPreviewForm}
                              layout="vertical"
                              initialValues={{
                                completion_gate_id: latestReviewQueueCompletionGate?.completion_gate_id || '',
                                queue_init_id: latestReviewQueueCompletionGate?.queue_init_id || '',
                                review_case_id: latestReviewQueueCompletionGate?.review_case_id || '',
                                include_marked_weak: true,
                                include_duplicate_merged: true,
                                acknowledge_dedup_preview_only: true,
                                acknowledge_no_production_dedup: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_analysis: true,
                                acknowledge_no_report: true,
                              }}
                              onFinish={handleCreateDedupPreview}
                            >
                              <Row gutter={[12, 0]}>
                                <Col span={12}>
                                  <Form.Item label="completion_gate_id" name="completion_gate_id">
                                    <Select
                                      placeholder="Select completion gate"
                                      options={reviewQueueCompletionGates.map((item) => ({
                                        value: item.completion_gate_id,
                                        label: `${item.status} / ${item.completion_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item label="queue_init_id" name="queue_init_id">
                                    <Input placeholder={latestReviewQueueCompletionGate?.queue_init_id || 'review_queue_init_id'} />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item label="review_case_id" name="review_case_id">
                                    <Input placeholder={latestReviewQueueCompletionGate?.review_case_id || 'review_only_case_id'} />
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item name="include_marked_weak" valuePropName="checked">
                                    <Checkbox>Include marked_weak items as warning-marked preview candidates.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="include_duplicate_merged" valuePropName="checked">
                                    <Checkbox>Include duplicate_merged items as reviewer merge hints.</Checkbox>
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={[12, 0]}>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_dedup_preview_only" valuePropName="checked">
                                    <Checkbox>Dedup Preview is preview only.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_production_dedup" valuePropName="checked">
                                    <Checkbox>No production dedup or merge effect.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                    <Checkbox>No Evidence Layer write.</Checkbox>
                                  </Form.Item>
                                </Col>
                                <Col span={12}>
                                  <Form.Item name="acknowledge_no_analysis" valuePropName="checked">
                                    <Checkbox>No analysis and no analysis-ready promotion.</Checkbox>
                                  </Form.Item>
                                  <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                    <Checkbox>No report, Sandbox, or public event generation.</Checkbox>
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  loading={dedupPreviewLoading}
                                  disabled={!dedupPreviewReady || dedupPreviewLoading}
                                >
                                  Generate Dedup Preview
                                </Button>
                                {latestDedupPreview ? (
                                  <Button
                                    icon={<ClipboardCopy size={16} />}
                                    onClick={() => copyText(latestDedupPreviewJson, 'Dedup preview JSON copied')}
                                  >
                                    Copy latest dedup preview JSON
                                  </Button>
                                ) : null}
                                {dedupPreviews.length ? (
                                  <Button
                                    icon={<ClipboardCopy size={16} />}
                                    onClick={() => copyText(dedupPreviewsJson, 'Dedup preview history JSON copied')}
                                  >
                                    Copy dedup preview history JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>

                            <Card size="small" title="Dedup Group Review / duplicate group governance">
                              <Space direction="vertical" size={10} className="full-width">
                                <Alert
                                  type="info"
                                  showIcon
                                  message="Group review is local governance only"
                                  description="Confirming a duplicate group does not run production dedup, does not write the Evidence Layer, does not make evidence analysis-ready, and does not generate reports, Sandbox output, or public events. Future group-review completion and analysis-promotion gates are still required."
                                />
                                {dedupGroupReviewError ? <Alert type="error" showIcon message={dedupGroupReviewError} /> : null}
                                <Form
                                  form={dedupGroupReviewForm}
                                  layout="vertical"
                                  initialValues={{
                                    reviewer_label: 'sentigraph_local_reviewer',
                                    note: 'Local review-only duplicate group action.',
                                    representative_item_id: '',
                                    split_item_ids: [],
                                    acknowledge_review_only_group_action: true,
                                    acknowledge_no_production_dedup: true,
                                    acknowledge_no_evidence_layer_write: true,
                                    acknowledge_no_analysis: true,
                                    acknowledge_no_report: true,
                                  }}
                                >
                                  <Row gutter={[12, 0]}>
                                    <Col span={8}>
                                      <Form.Item label="reviewer_label" name="reviewer_label">
                                        <Input placeholder="human reviewer label" />
                                      </Form.Item>
                                    </Col>
                                    <Col span={8}>
                                      <Form.Item label="representative_item_id" name="representative_item_id">
                                        <Input placeholder="required for change_representative" />
                                      </Form.Item>
                                    </Col>
                                    <Col span={8}>
                                      <Form.Item label="split_item_ids" name="split_item_ids">
                                        <Select mode="tags" placeholder="required for split_group" />
                                      </Form.Item>
                                    </Col>
                                    <Col span={24}>
                                      <Form.Item label="review note" name="note">
                                        <TextArea rows={2} placeholder="Explain this local review-only group decision." />
                                      </Form.Item>
                                    </Col>
                                  </Row>
                                  <Row gutter={[12, 0]}>
                                    <Col span={12}>
                                      <Form.Item name="acknowledge_review_only_group_action" valuePropName="checked">
                                        <Checkbox>Review-only group action; duplicate groups are candidates, not facts.</Checkbox>
                                      </Form.Item>
                                      <Form.Item name="acknowledge_no_production_dedup" valuePropName="checked">
                                        <Checkbox>No production dedup, merge, or count-amplification effect.</Checkbox>
                                      </Form.Item>
                                      <Form.Item name="acknowledge_no_evidence_layer_write" valuePropName="checked">
                                        <Checkbox>No Evidence Layer write and no production case/review queue creation.</Checkbox>
                                      </Form.Item>
                                    </Col>
                                    <Col span={12}>
                                      <Form.Item name="acknowledge_no_analysis" valuePropName="checked">
                                        <Checkbox>No analysis, no risk update, and no analysis_included=true.</Checkbox>
                                      </Form.Item>
                                      <Form.Item name="acknowledge_no_report" valuePropName="checked">
                                        <Checkbox>No report, Sandbox fixture, public event, or B-end output generation.</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  </Row>
                                  {dedupGroupReviewAudits.length ? (
                                    <Button
                                      icon={<ClipboardCopy size={16} />}
                                      onClick={() => copyText(dedupGroupReviewAuditsJson, 'Dedup group review audit JSON copied')}
                                    >
                                      Copy group review audit JSON
                                    </Button>
                                  ) : null}
                                </Form>
                              </Space>
                            </Card>

                            {latestDedupPreview ? (
                              <Card size="small" title="Latest dedup preview">
                                <Space direction="vertical" size={10} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestDedupPreview.status === 'preview_ready' ? 'green' : latestDedupPreview.status === 'blocked' ? 'red' : 'gold'}>
                                      {latestDedupPreview.status}
                                    </Tag>
                                    <Tag color="default">can_run_dedup_now: {boolText(latestDedupPreview.readiness?.can_run_dedup_now)}</Tag>
                                    <Tag color="default">can_run_analysis_now: {boolText(latestDedupPreview.readiness?.can_run_analysis_now)}</Tag>
                                    <Tag color="default">human_confirmation_required: {boolText(latestDedupPreview.readiness?.requires_human_dedup_confirmation)}</Tag>
                                  </Space>
                                  <Descriptions column={1} size="small">
                                    <Descriptions.Item label="dedup_preview_id">{latestDedupPreview.dedup_preview_id}</Descriptions.Item>
                                    <Descriptions.Item label="counts">
                                      seen={latestDedupPreview.counts?.items_seen || 0},
                                      eligible={latestDedupPreview.counts?.items_eligible_for_preview || 0},
                                      excluded={latestDedupPreview.counts?.items_excluded || 0},
                                      groups={latestDedupPreview.counts?.duplicate_group_candidates || 0},
                                      unique_candidates={latestDedupPreview.counts?.unique_candidate_count || 0}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="signals">
                                      exact_url={boolText(latestDedupPreview.dedup_signals?.exact_url_match)},
                                      normalized_url={boolText(latestDedupPreview.dedup_signals?.normalized_url_match)},
                                      content_hash={boolText(latestDedupPreview.dedup_signals?.content_preview_hash_match)},
                                      lineage={boolText(latestDedupPreview.dedup_signals?.lineage_match)},
                                      reviewer_hint={boolText(latestDedupPreview.dedup_signals?.reviewer_merge_hint)},
                                      semantic_llm={boolText(latestDedupPreview.dedup_signals?.semantic_llm_match)}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  {latestDedupPreview.groups?.length ? (
                                    <Space direction="vertical" size={8} className="full-width">
                                      {latestDedupPreview.groups.map((group) => {
                                        const groupAudits = dedupGroupAuditsByGroup[group.group_candidate_id] || []
                                        return (
                                          <Card size="small" key={group.group_candidate_id}>
                                            <Space direction="vertical" size={8} className="full-width">
                                              <Space wrap>
                                                <Tag color={DEDUP_GROUP_STATUS_COLOR[group.group_status] || 'default'}>
                                                  {group.group_status || 'review_needed'}
                                                </Tag>
                                                <Tag color="blue">{group.reason}</Tag>
                                                <Tag color={group.confidence === 'high' ? 'green' : group.confidence === 'low' ? 'gold' : 'cyan'}>
                                                  {group.confidence}
                                                </Tag>
                                                <Tag color="default">audit_count: {groupAudits.length}</Tag>
                                                <Text type="secondary">{group.group_candidate_id}</Text>
                                              </Space>
                                              <Text>representative: {group.representative_item_id || '-'}</Text>
                                              <Text type="secondary">
                                                items: {(group.item_ids || []).join(', ') || '-'}
                                              </Text>
                                              {group.split_item_ids?.length ? (
                                                <Text type="secondary">split_item_ids: {group.split_item_ids.join(', ')}</Text>
                                              ) : null}
                                              <Text type="secondary">
                                                duplicate_count_preview={group.duplicate_count_preview || 0}, may_amplify_risk=
                                                {boolText(group.may_amplify_risk)}, human_confirmation_required=
                                                {boolText(group.human_confirmation_required)}, analysis_effect={group.analysis_effect}
                                              </Text>
                                              <Space wrap>
                                                {DEDUP_GROUP_ACTIONS.map((action) => {
                                                  const requiresSplit = action === 'split_group'
                                                  const requiresRepresentative = action === 'change_representative'
                                                  const missingSplit = requiresSplit && !splitTags(dedupGroupReviewValues.split_item_ids).length
                                                  const missingRepresentative = requiresRepresentative && !String(dedupGroupReviewValues.representative_item_id || '').trim()
                                                  const loadingKey = `${group.group_candidate_id}:${action}`
                                                  return (
                                                    <Button
                                                      size="small"
                                                      key={action}
                                                      danger={['reject_group', 'hold_group_for_privacy'].includes(action)}
                                                      loading={dedupGroupReviewLoading === loadingKey}
                                                      disabled={!dedupGroupReviewReady || missingSplit || missingRepresentative || Boolean(dedupGroupReviewLoading)}
                                                      onClick={() => handleDedupGroupReviewAction(group, action)}
                                                    >
                                                      {DEDUP_GROUP_ACTION_LABELS[action]}
                                                    </Button>
                                                  )
                                                })}
                                              </Space>
                                              {groupAudits.length ? (
                                                <Card size="small" title="Group audit timeline">
                                                  <Space direction="vertical" size={6} className="full-width">
                                                    {groupAudits.map((audit) => (
                                                      <Space direction="vertical" size={2} key={audit.audit_id} className="full-width">
                                                        <Space wrap>
                                                          <Tag color="default">{audit.action}</Tag>
                                                          <Tag color={DEDUP_GROUP_STATUS_COLOR[audit.new_group_status] || 'default'}>
                                                            {audit.previous_group_status || '-'} → {audit.new_group_status || '-'}
                                                          </Tag>
                                                          <Text type="secondary">{audit.reviewed_at || '-'}</Text>
                                                          <Text type="secondary">{audit.reviewer_label || '-'}</Text>
                                                        </Space>
                                                        <Text type="secondary">
                                                          analysis_effect={audit.analysis_effect}, dedup_effect={audit.dedup_effect}, trust_effect={audit.trust_label_effect}
                                                        </Text>
                                                        <Text>{audit.note || '-'}</Text>
                                                      </Space>
                                                    ))}
                                                  </Space>
                                                </Card>
                                              ) : (
                                                <Text type="secondary">No group review audit yet.</Text>
                                              )}
                                              <SummaryList title="Notes" items={group.notes || []} />
                                            </Space>
                                          </Card>
                                        )
                                      })}
                                    </Space>
                                  ) : (
                                    <Text type="secondary">No duplicate group candidates found in latest preview.</Text>
                                  )}
                                  {latestDedupPreview.excluded_items?.length ? (
                                    <Card size="small" title="Excluded items">
                                      <Space direction="vertical" size={4} className="full-width">
                                        {latestDedupPreview.excluded_items.map((item) => (
                                          <Text type="secondary" key={`${item.review_item_id}:${item.reason}`}>
                                            {item.review_item_id}: {item.reason} / status={item.queue_status || '-'}
                                          </Text>
                                        ))}
                                      </Space>
                                    </Card>
                                  ) : null}
                                  <Descriptions column={1} size="small">
                                    <Descriptions.Item label="privacy_scan">
                                      raw_identifier_found={boolText(latestDedupPreview.privacy_scan?.raw_identifier_found)},
                                      secret_like_found={boolText(latestDedupPreview.privacy_scan?.secret_like_found)},
                                      privacy_stop={boolText(latestDedupPreview.privacy_scan?.privacy_stop)}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <SummaryList title="Blockers" items={latestDedupPreview.blockers || []} />
                                  <SummaryList title="Warnings" items={latestDedupPreview.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestDedupPreview.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestDedupPreview.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No dedup preview record yet.</Text>
                            )}

                            {dedupPreviews.length ? (
                              <Card size="small" title={`Existing dedup preview records (${dedupPreviews.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {dedupPreviews.map((item) => (
                                    <Space wrap key={item.dedup_preview_id}>
                                      <Tag color={item.status === 'preview_ready' ? 'green' : item.status === 'blocked' ? 'red' : 'gold'}>
                                        {item.status}
                                      </Tag>
                                      <Text type="secondary">{item.dedup_preview_id}</Text>
                                      <Text type="secondary">groups={item.counts?.duplicate_group_candidates || 0}</Text>
                                      <Text type="secondary">created_at={item.created_at || '-'}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Analysis-ready Promotion Gate / future manual trigger only">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Promotion gate is not analysis"
                              description="This gate only records whether a review-only case is eligible for a future manual analysis trigger. It does not write the Evidence Layer, create a production case, run production dedup, run analysis, generate reports, generate Sandbox fixtures, or create public event pages."
                            />
                            {analysisReadyPromotionGateError ? <Alert type="error" showIcon message={analysisReadyPromotionGateError} /> : null}
                            <Form
                              form={analysisReadyPromotionGateForm}
                              layout="vertical"
                              initialValues={{
                                promotion_decision: 'approve_for_future_manual_analysis_trigger',
                                reviewer_label: 'promotion_reviewer',
                                coverage_limitations_acknowledged: true,
                                privacy_acknowledged: true,
                                weak_evidence_warning_acknowledged: true,
                                dedup_preview_warning_acknowledged: true,
                                provider_output_is_evidence_not_truth_acknowledged: true,
                                acknowledge_promotion_is_not_analysis: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_no_production_dedup: true,
                                acknowledge_no_report: true,
                              }}
                              onFinish={handleCreateAnalysisReadyPromotionGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Promotion decision" name="promotion_decision">
                                    <Select options={PROMOTION_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="promotion_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Dedup preview id" name="dedup_preview_id">
                                    <Select
                                      allowClear
                                      placeholder={latestDedupPreview?.dedup_preview_id || 'latest ready preview'}
                                      options={dedupPreviews.map((item) => ({
                                        value: item.dedup_preview_id,
                                        label: `${item.status} / ${item.dedup_preview_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item label="Decision note" name="note">
                                    <TextArea rows={2} placeholder="Why this review-only case is held, rejected, or eligible for a future manual trigger." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                {[
                                  ['coverage_limitations_acknowledged', 'Coverage limitations acknowledged'],
                                  ['privacy_acknowledged', 'Privacy blockers reviewed'],
                                  ['weak_evidence_warning_acknowledged', 'Weak evidence remains warning-marked'],
                                  ['dedup_preview_warning_acknowledged', 'Dedup preview reviewed; duplicate count is not truth strength'],
                                  ['provider_output_is_evidence_not_truth_acknowledged', 'Provider output is evidence, not truth'],
                                  ['acknowledge_promotion_is_not_analysis', 'This does not run analysis'],
                                  ['acknowledge_no_evidence_layer_write', 'No Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'No production case'],
                                  ['acknowledge_no_production_dedup', 'No production dedup'],
                                  ['acknowledge_no_report', 'No report generation'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={analysisReadyPromotionGateLoading}
                                  disabled={!analysisReadyPromotionReady || analysisReadyPromotionGateLoading}
                                >
                                  Record promotion gate
                                </Button>
                                {latestAnalysisReadyPromotionGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestAnalysisReadyPromotionGateJson, 'Promotion gate JSON copied')}
                                  >
                                    Copy latest gate JSON
                                  </Button>
                                ) : null}
                                {analysisReadyPromotionGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(analysisReadyPromotionGatesJson, 'Promotion gate history JSON copied')}
                                  >
                                    Copy gate history JSON
                                  </Button>
                                ) : null}
                                {promotionDecisionAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(promotionDecisionAuditsJson, 'Promotion decision audit JSON copied')}
                                  >
                                    Copy promotion audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {dedupGroupsNeedReview ? (
                              <Alert
                                type="info"
                                showIcon
                                message="Dedup group review is not complete"
                                description="All duplicate group candidates must be confirmed, marked weak, representative-changed, or rejected before this gate can create an eligible record."
                              />
                            ) : null}
                            {latestAnalysisReadyPromotionGate ? (
                              <Card size="small" title="Latest promotion gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={PROMOTION_GATE_STATUS_COLOR[latestAnalysisReadyPromotionGate.status] || 'default'}>
                                      {latestAnalysisReadyPromotionGate.status}
                                    </Tag>
                                    <Tag color="default">
                                      eligible_future_manual_trigger:{' '}
                                      {boolText(latestAnalysisReadyPromotionGate.readiness?.eligible_for_future_manual_analysis_trigger)}
                                    </Tag>
                                    <Tag color="default">
                                      can_run_analysis_now: {boolText(latestAnalysisReadyPromotionGate.readiness?.can_run_analysis_now)}
                                    </Tag>
                                    <Tag color="default">
                                      run_analysis_now: {boolText(latestAnalysisReadyPromotionGate.now_flags?.run_analysis_now)}
                                    </Tag>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="promotion_gate_id">{latestAnalysisReadyPromotionGate.promotion_gate_id}</Descriptions.Item>
                                    <Descriptions.Item label="decision">{latestAnalysisReadyPromotionGate.promotion_decision?.decision || '-'}</Descriptions.Item>
                                    <Descriptions.Item label="analysis_effect">
                                      {latestAnalysisReadyPromotionGate.promotion_decision?.analysis_effect || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="counts">
                                      seen={latestAnalysisReadyPromotionGate.counts?.items_seen || 0}, eligible=
                                      {latestAnalysisReadyPromotionGate.counts?.items_eligible_for_promotion_preview || 0}, excluded=
                                      {latestAnalysisReadyPromotionGate.counts?.items_excluded || 0}, groups=
                                      {latestAnalysisReadyPromotionGate.counts?.confirmed_duplicate_groups || 0}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <SummaryList title="Promotion warnings" items={latestAnalysisReadyPromotionGate.warnings || []} />
                                  <SummaryList title="Promotion blockers" items={latestAnalysisReadyPromotionGate.blockers || []} />
                                  <SummaryList title="Boundary notes" items={latestAnalysisReadyPromotionGate.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestAnalysisReadyPromotionGate.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No analysis-ready promotion gate record yet.</Text>
                            )}
                            {promotionDecisionAudits.length ? (
                              <Card size="small" title={`Promotion decision audit timeline (${promotionDecisionAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {promotionDecisionAudits.map((audit) => (
                                    <Space wrap key={audit.promotion_decision_id}>
                                      <Tag color={audit.new_status === 'eligible_for_future_manual_analysis_trigger' ? 'green' : 'gold'}>
                                        {audit.decision}
                                      </Tag>
                                      <Text type="secondary">{audit.new_status}</Text>
                                      <Text type="secondary">{audit.reviewed_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Manual Analysis Trigger / 人工分析触发">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Trigger record only: no analysis runs here"
                              description="This records a manual analysis trigger decision only. It does not run analysis, does not generate Analysis Result, does not write Evidence Layer, does not create a production case, and does not generate report, Sandbox, or public event output."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Eligible promotion gate is not automatic analysis"
                              description="Weak evidence remains warning-marked, rejected evidence remains excluded, duplicate evidence must not amplify risk, provider output is evidence not truth, and coverage limitations must be shown in any future analysis."
                            />
                            {manualAnalysisTriggerError ? <Alert type="error" showIcon message={manualAnalysisTriggerError} /> : null}
                            <Form
                              form={manualAnalysisTriggerForm}
                              layout="vertical"
                              initialValues={{
                                trigger_decision: 'trigger_analysis',
                                reviewer_label: 'manual_trigger_reviewer',
                                coverage_acknowledged: true,
                                privacy_acknowledged: true,
                                weak_warning_acknowledged: true,
                                dedup_warning_acknowledged: true,
                                provider_output_is_evidence_not_truth_acknowledged: true,
                                not_official_verification_acknowledged: true,
                                not_full_web_coverage_acknowledged: true,
                                acknowledge_trigger_record_only: true,
                                acknowledge_no_analysis_run: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_no_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                              }}
                              onFinish={handleCreateManualAnalysisTrigger}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Trigger decision" name="trigger_decision">
                                    <Select options={MANUAL_TRIGGER_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="manual_trigger_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Promotion gate id" name="promotion_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestAnalysisReadyPromotionGate?.promotion_gate_id || 'latest eligible promotion gate'}
                                      options={analysisReadyPromotionGates.map((item) => ({
                                        value: item.promotion_gate_id,
                                        label: `${item.status} / ${item.promotion_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item label="Decision note" name="note" rules={[{ required: true }]}>
                                    <TextArea rows={2} placeholder="Why this promoted review-only set should be triggered, held, or cancelled." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                {[
                                  ['coverage_acknowledged', 'Coverage limitations acknowledged'],
                                  ['privacy_acknowledged', 'Privacy boundaries acknowledged'],
                                  ['weak_warning_acknowledged', 'Weak evidence warning acknowledged'],
                                  ['dedup_warning_acknowledged', 'Dedup warning acknowledged'],
                                  ['provider_output_is_evidence_not_truth_acknowledged', 'Provider output is evidence, not truth'],
                                  ['not_official_verification_acknowledged', 'Not official verification'],
                                  ['not_full_web_coverage_acknowledged', 'Not full-web coverage'],
                                  ['acknowledge_trigger_record_only', 'Trigger record only'],
                                  ['acknowledge_no_analysis_run', 'No analysis run'],
                                  ['acknowledge_no_evidence_layer_write', 'No Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'No production case'],
                                  ['acknowledge_no_report', 'No report generation'],
                                  ['acknowledge_no_sandbox_or_public_event', 'No Sandbox/public event generation'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={manualAnalysisTriggerLoading}
                                  disabled={!manualAnalysisTriggerReady || manualAnalysisTriggerLoading}
                                >
                                  Record Manual Trigger
                                </Button>
                                {latestManualAnalysisTrigger ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestManualAnalysisTriggerJson, 'Manual trigger JSON copied')}
                                  >
                                    Copy latest trigger JSON
                                  </Button>
                                ) : null}
                                {manualAnalysisTriggers.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(manualAnalysisTriggersJson, 'Manual trigger history JSON copied')}
                                  >
                                    Copy trigger history JSON
                                  </Button>
                                ) : null}
                                {manualAnalysisTriggerAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(manualAnalysisTriggerAuditsJson, 'Manual trigger audit JSON copied')}
                                  >
                                    Copy trigger audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestManualAnalysisTrigger ? (
                              <Card size="small" title="Latest manual trigger">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={MANUAL_TRIGGER_STATUS_COLOR[latestManualAnalysisTrigger.status] || 'default'}>
                                      {latestManualAnalysisTrigger.status}
                                    </Tag>
                                    <Tag color="default">decision: {latestManualAnalysisTrigger.trigger_decision || '-'}</Tag>
                                    <Tag color="default">
                                      can_run_analysis_now: {boolText(latestManualAnalysisTrigger.readiness?.can_run_analysis_now)}
                                    </Tag>
                                    <Tag color="default">
                                      run_analysis_now: {boolText(latestManualAnalysisTrigger.now_flags?.run_analysis_now)}
                                    </Tag>
                                    <Tag color="default">
                                      generate_analysis_result_now:{' '}
                                      {boolText(latestManualAnalysisTrigger.now_flags?.generate_analysis_result_now)}
                                    </Tag>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="manual_trigger_id">{latestManualAnalysisTrigger.manual_trigger_id}</Descriptions.Item>
                                    <Descriptions.Item label="promotion_gate_id">{latestManualAnalysisTrigger.promotion_gate_id}</Descriptions.Item>
                                    <Descriptions.Item label="scope">
                                      include_items={(latestManualAnalysisTrigger.analysis_scope?.include_item_ids || []).length}, include_groups=
                                      {(latestManualAnalysisTrigger.analysis_scope?.include_group_ids || []).length}, excluded=
                                      {(latestManualAnalysisTrigger.analysis_scope?.exclude_item_ids || []).length}, weak=
                                      {(latestManualAnalysisTrigger.analysis_scope?.weak_warning_item_ids || []).length}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="readiness">
                                      runtime_not_implemented=
                                      {boolText(latestManualAnalysisTrigger.readiness?.analysis_runtime_not_implemented_here)}, result_gate_required=
                                      {boolText(latestManualAnalysisTrigger.readiness?.requires_analysis_result_boundary_gate)}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <SummaryList title="Required coverage warnings" items={latestManualAnalysisTrigger.required_warnings?.coverage_limitations || []} />
                                  <SummaryList title="Weak evidence warnings" items={latestManualAnalysisTrigger.required_warnings?.weak_evidence_warnings || []} />
                                  <SummaryList title="Dedup warnings" items={latestManualAnalysisTrigger.required_warnings?.dedup_preview_warnings || []} />
                                  <SummaryList title="Trigger warnings" items={latestManualAnalysisTrigger.warnings || []} />
                                  <SummaryList title="Blocked reasons" items={latestManualAnalysisTrigger.blocked_reasons || []} />
                                  <SummaryList title="Boundary notes" items={latestManualAnalysisTrigger.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestManualAnalysisTrigger.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No manual analysis trigger record yet.</Text>
                            )}
                            {manualAnalysisTriggerAudits.length ? (
                              <Card size="small" title={`Manual trigger audit timeline (${manualAnalysisTriggerAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {manualAnalysisTriggerAudits.map((audit) => (
                                    <Space wrap key={audit.manual_trigger_audit_id}>
                                      <Tag color={audit.decision === 'trigger_analysis' ? 'green' : audit.decision === 'hold' ? 'gold' : 'default'}>
                                        {audit.decision}
                                      </Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">run_analysis_now={boolText(audit.now_flags?.run_analysis_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Analysis Result Boundary Gate / 分析结果边界门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Boundary readiness only: no Analysis Result is generated here"
                              description="This records boundary readiness only. It does not run analysis, does not generate Analysis Result or Summary Report, does not write Evidence Layer, and does not generate Sandbox, public event, or B-end report output."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Warnings must travel with future results"
                              description="Weak evidence remains warning-marked, rejected evidence remains excluded, duplicate evidence must not amplify risk, provider output is evidence not truth, and coverage limitations must be displayed in any future analysis result."
                            />
                            {analysisResultBoundaryGateError ? <Alert type="error" showIcon message={analysisResultBoundaryGateError} /> : null}
                            <Form
                              form={analysisResultBoundaryGateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'boundary_gate_reviewer',
                                coverage_limitation_acknowledged: true,
                                weak_evidence_warning_acknowledged: true,
                                rejected_evidence_exclusion_acknowledged: true,
                                dedup_warning_acknowledged: true,
                                provider_output_is_evidence_not_truth_acknowledged: true,
                                not_official_verification_acknowledged: true,
                                not_full_web_coverage_acknowledged: true,
                                audit_trace_acknowledged: true,
                                acknowledge_boundary_gate_only: true,
                                acknowledge_no_analysis_run: true,
                                acknowledge_no_analysis_result_generation: true,
                                acknowledge_no_report_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                              }}
                              onFinish={handleCreateAnalysisResultBoundaryGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Manual trigger id" name="manual_trigger_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisTrigger?.manual_trigger_id || 'latest ready manual trigger'}
                                      options={manualAnalysisTriggers.map((item) => ({
                                        value: item.manual_trigger_id,
                                        label: `${item.status} / ${item.manual_trigger_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Promotion gate id" name="promotion_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisTrigger?.promotion_gate_id || 'from manual trigger'}
                                      options={analysisReadyPromotionGates.map((item) => ({
                                        value: item.promotion_gate_id,
                                        label: `${item.status} / ${item.promotion_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="boundary_gate_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item label="Boundary note" name="note" rules={[{ required: true }]}>
                                    <TextArea rows={2} placeholder="Confirm warnings, exclusions, dedup, coverage, and audit boundaries before any future result runtime." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                {[
                                  ['coverage_limitation_acknowledged', 'Coverage limitation acknowledged'],
                                  ['weak_evidence_warning_acknowledged', 'Weak evidence warning acknowledged'],
                                  ['rejected_evidence_exclusion_acknowledged', 'Rejected evidence exclusion acknowledged'],
                                  ['dedup_warning_acknowledged', 'Dedup warning acknowledged'],
                                  ['provider_output_is_evidence_not_truth_acknowledged', 'Provider output is evidence, not truth'],
                                  ['not_official_verification_acknowledged', 'Not official verification'],
                                  ['not_full_web_coverage_acknowledged', 'Not full-web coverage'],
                                  ['audit_trace_acknowledged', 'Audit trace acknowledged'],
                                  ['acknowledge_boundary_gate_only', 'Boundary gate only'],
                                  ['acknowledge_no_analysis_run', 'No analysis run'],
                                  ['acknowledge_no_analysis_result_generation', 'No Analysis Result generation'],
                                  ['acknowledge_no_report_generation', 'No report generation'],
                                  ['acknowledge_no_sandbox_or_public_event', 'No Sandbox/public event generation'],
                                  ['acknowledge_no_evidence_layer_write', 'No Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'No production case'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={analysisResultBoundaryGateLoading}
                                  disabled={!analysisResultBoundaryGateReady || analysisResultBoundaryGateLoading}
                                >
                                  Create Boundary Gate
                                </Button>
                                {latestAnalysisResultBoundaryGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestAnalysisResultBoundaryGateJson, 'Boundary gate JSON copied')}
                                  >
                                    Copy latest boundary gate JSON
                                  </Button>
                                ) : null}
                                {analysisResultBoundaryGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(analysisResultBoundaryGatesJson, 'Boundary gate history JSON copied')}
                                  >
                                    Copy boundary gate history JSON
                                  </Button>
                                ) : null}
                                {analysisResultBoundaryGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(analysisResultBoundaryGateAuditsJson, 'Boundary gate audit JSON copied')}
                                  >
                                    Copy boundary gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestAnalysisResultBoundaryGate ? (
                              <Card size="small" title="Latest Analysis Result Boundary Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestAnalysisResultBoundaryGate.status === 'boundary_ready_for_future_analysis_result_runtime' ? 'green' : 'gold'}>
                                      {latestAnalysisResultBoundaryGate.status}
                                    </Tag>
                                    <Tag color="default">
                                      can_present_analysis_result_now:{' '}
                                      {boolText(latestAnalysisResultBoundaryGate.readiness?.can_present_analysis_result_now)}
                                    </Tag>
                                    <Tag color="default">
                                      run_analysis_now: {boolText(latestAnalysisResultBoundaryGate.now_flags?.run_analysis_now)}
                                    </Tag>
                                    <Tag color="default">
                                      generate_analysis_result_now:{' '}
                                      {boolText(latestAnalysisResultBoundaryGate.now_flags?.generate_analysis_result_now)}
                                    </Tag>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="boundary_gate_id">
                                      {latestAnalysisResultBoundaryGate.boundary_gate_id}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="manual_trigger_id">
                                      {latestAnalysisResultBoundaryGate.manual_trigger_id}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="input boundary">
                                      source={latestAnalysisResultBoundaryGate.analysis_input_boundary?.source || '-'}, provider_truth=
                                      {boolText(latestAnalysisResultBoundaryGate.analysis_input_boundary?.provider_output_is_truth)}, official_verification=
                                      {boolText(latestAnalysisResultBoundaryGate.analysis_input_boundary?.official_verification)}, full_web=
                                      {boolText(latestAnalysisResultBoundaryGate.analysis_input_boundary?.full_web_coverage)}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="counts">
                                      included={latestAnalysisResultBoundaryGate.counts?.included_item_count || 0}, rejected_excluded=
                                      {latestAnalysisResultBoundaryGate.counts?.excluded_rejected_count || 0}, weak=
                                      {latestAnalysisResultBoundaryGate.counts?.weak_warning_count || 0}, duplicate_groups=
                                      {latestAnalysisResultBoundaryGate.counts?.duplicate_group_count || 0}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <SummaryList title="Boundary sections" items={Object.entries(latestAnalysisResultBoundaryGate.required_boundary_sections || {}).map(([key, value]) => `${key}: ${boolText(value)}`)} />
                                  <SummaryList title="Boundary warnings" items={latestAnalysisResultBoundaryGate.warnings || []} />
                                  <SummaryList title="Blocked reasons" items={latestAnalysisResultBoundaryGate.blocked_reasons || []} />
                                  <SummaryList title="Boundary notes" items={latestAnalysisResultBoundaryGate.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestAnalysisResultBoundaryGate.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Analysis Result Boundary Gate record yet.</Text>
                            )}
                            {analysisResultBoundaryGateAudits.length ? (
                              <Card size="small" title={`Boundary gate audit timeline (${analysisResultBoundaryGateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {analysisResultBoundaryGateAudits.map((audit) => (
                                    <Space wrap key={audit.boundary_gate_audit_id}>
                                      <Tag color="green">boundary gate</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">run_analysis_now={boolText(audit.now_flags?.run_analysis_now)}</Text>
                                      <Text type="secondary">
                                        generate_analysis_result_now={boolText(audit.now_flags?.generate_analysis_result_now)}
                                      </Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Manual Analysis Execution / 人工分析执行候选">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local candidate only: no downstream product artifact is generated"
                              description="This creates a local analysis result candidate from the approved manual-trigger scope. It does not write the Evidence Layer, create a production case, run production dedup, generate a Summary Report, generate Sandbox/public event output, or create a B-end report."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Boundary notes remain attached"
                              description="Provider output is evidence, not truth. Rejected evidence stays excluded, weak evidence keeps warnings, duplicate evidence must not amplify risk, and coverage is not full-web or official verification."
                            />
                            {manualAnalysisExecutionError ? <Alert type="error" showIcon message={manualAnalysisExecutionError} /> : null}
                            <Form
                              form={manualAnalysisExecutionForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'manual_analysis_executor',
                                acknowledge_local_candidate_only: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_no_report_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                              }}
                              onFinish={handleCreateManualAnalysisExecution}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Manual trigger id" name="manual_trigger_id">
                                    <Select
                                      allowClear
                                      placeholder={latestAnalysisResultBoundaryGate?.manual_trigger_id || 'latest trigger from boundary gate'}
                                      options={manualAnalysisTriggers.map((item) => ({
                                        value: item.manual_trigger_id,
                                        label: `${item.status} / ${item.manual_trigger_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Boundary gate id" name="boundary_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestAnalysisResultBoundaryGate?.boundary_gate_id || 'latest ready boundary gate'}
                                      options={analysisResultBoundaryGates.map((item) => ({
                                        value: item.boundary_gate_id,
                                        label: `${item.status} / ${item.boundary_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Promotion gate id" name="promotion_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestAnalysisResultBoundaryGate?.promotion_gate_id || 'promotion gate from boundary'}
                                      options={analysisReadyPromotionGates.map((item) => ({
                                        value: item.promotion_gate_id,
                                        label: `${item.status} / ${item.promotion_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="manual_analysis_executor" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={16}>
                                  <Form.Item label="Execution note" name="note" rules={[{ required: true }]}>
                                    <TextArea
                                      rows={2}
                                      placeholder="Create a local analysis candidate only; preserve all boundary warnings."
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Form.Item label="Required acknowledgements">
                                <Row gutter={[8, 4]}>
                                  {[
                                    ['acknowledge_local_candidate_only', 'local result candidate only'],
                                    ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                    ['acknowledge_no_production_case', 'no production case'],
                                    ['acknowledge_no_report_generation', 'no report generation'],
                                    ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                    ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                    ['acknowledge_not_official_verification', 'not official verification'],
                                    ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                    ['acknowledge_weak_evidence_warning', 'weak evidence warning preserved'],
                                    ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                    ['acknowledge_dedup_no_risk_amplification', 'duplicate evidence not amplified'],
                                  ].map(([name, label]) => (
                                    <Col xs={24} md={8} key={name}>
                                      <Form.Item name={name} valuePropName="checked" noStyle>
                                        <Checkbox>{label}</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  ))}
                                </Row>
                              </Form.Item>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={manualAnalysisExecutionLoading}
                                  disabled={!manualAnalysisExecutionReady || manualAnalysisExecutionLoading}
                                >
                                  Create Analysis Result Candidate
                                </Button>
                                {latestManualAnalysisExecution ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestManualAnalysisExecutionJson, 'Manual analysis execution JSON copied')}
                                  >
                                    Copy latest execution JSON
                                  </Button>
                                ) : null}
                                {latestManualAnalysisResultCandidate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestManualAnalysisResultCandidateJson, 'Analysis candidate JSON copied')}
                                  >
                                    Copy latest candidate JSON
                                  </Button>
                                ) : null}
                                {manualAnalysisExecutions.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(manualAnalysisExecutionsJson, 'Manual analysis execution history JSON copied')}
                                  >
                                    Copy execution history JSON
                                  </Button>
                                ) : null}
                                {manualAnalysisResultCandidates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(manualAnalysisResultCandidatesJson, 'Analysis candidate history JSON copied')}
                                  >
                                    Copy candidate history JSON
                                  </Button>
                                ) : null}
                                {manualAnalysisExecutionAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(manualAnalysisExecutionAuditsJson, 'Manual analysis execution audit JSON copied')}
                                  >
                                    Copy execution audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestManualAnalysisExecution ? (
                              <Card size="small" title="Latest Manual Analysis Execution">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestManualAnalysisExecution.status === 'analysis_result_candidate_created' ? 'green' : 'gold'}>
                                      {latestManualAnalysisExecution.status}
                                    </Tag>
                                    <Tag>{latestManualAnalysisExecution.analysis_execution_mode}</Tag>
                                    <Text type="secondary">{latestManualAnalysisExecution.manual_analysis_execution_id}</Text>
                                  </Space>
                                  <Text type="secondary">
                                    candidate_result_id={latestManualAnalysisExecution.candidate_result_id || '-'} / original_package_rows_read=
                                    {boolText(latestManualAnalysisExecution.input_scope?.original_package_rows_read || latestManualAnalysisExecution.safe_mode?.original_package_rows_re_read)}
                                  </Text>
                                  <Space wrap>
                                    <Tag color="default">run_analysis_now={boolText(latestManualAnalysisExecution.now_flags?.run_analysis_now)}</Tag>
                                    <Tag color="default">generate_analysis_result_now={boolText(latestManualAnalysisExecution.now_flags?.generate_analysis_result_now)}</Tag>
                                    <Tag color="default">write_evidence_layer_now={boolText(latestManualAnalysisExecution.now_flags?.write_evidence_layer_now)}</Tag>
                                    <Tag color="default">generate_report_now={boolText(latestManualAnalysisExecution.now_flags?.generate_report_now)}</Tag>
                                    <Tag color="default">generate_public_event_now={boolText(latestManualAnalysisExecution.now_flags?.generate_public_event_now)}</Tag>
                                  </Space>
                                  <SummaryList title="Execution warnings" items={latestManualAnalysisExecution.warnings || []} />
                                  <SummaryList title="Execution limitations" items={latestManualAnalysisExecution.limitations || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No manual analysis execution candidate yet.</Text>
                            )}
                            {latestManualAnalysisResultCandidate ? (
                              <Card size="small" title="Latest Analysis Result Candidate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color="blue">{latestManualAnalysisResultCandidate.analysis_input_source}</Tag>
                                    <Text type="secondary">{latestManualAnalysisResultCandidate.result_candidate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={2} bordered>
                                    <Descriptions.Item label="Included items">
                                      {latestManualAnalysisResultCandidate.source_scope_summary?.included_item_count || 0}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="Included groups">
                                      {latestManualAnalysisResultCandidate.source_scope_summary?.included_group_count || 0}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="Weak warning count">
                                      {latestManualAnalysisResultCandidate.source_scope_summary?.weak_evidence_count || 0}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="Duplicate groups">
                                      {latestManualAnalysisResultCandidate.source_scope_summary?.duplicate_group_count || 0}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Card size="small" title="Candidate summary">
                                    <pre className="code-preview">{JSON.stringify(latestManualAnalysisResultCandidate.analysis_summary || {}, null, 2)}</pre>
                                  </Card>
                                  <Space wrap>
                                    {Object.entries(latestManualAnalysisResultCandidate.downstream_flags || {}).map(([key, value]) => (
                                      <Tag color={value ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Confidence notes" items={latestManualAnalysisResultCandidate.confidence_notes || []} />
                                  <SummaryList title="Candidate limitations" items={latestManualAnalysisResultCandidate.limitations || []} />
                                </Space>
                              </Card>
                            ) : null}
                            {manualAnalysisExecutionAudits.length ? (
                              <Card size="small" title={`Manual analysis execution audit timeline (${manualAnalysisExecutionAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {manualAnalysisExecutionAudits.map((audit) => (
                                    <Space wrap key={audit.manual_analysis_execution_audit_id}>
                                      <Tag color="green">{audit.effect}</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">run_analysis_now={boolText(audit.now_flags?.run_analysis_now)}</Text>
                                      <Text type="secondary">generate_report_now={boolText(audit.now_flags?.generate_report_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Report Generation Gate / 报告生成门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Gate only: no report artifact is generated"
                              description="This records readiness for a future report runtime only. It does not generate Summary Report, B-end report, PDF, Markdown, deck, Sandbox, public event, Evidence Layer write, production case, or any real LLM output."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Future report inputs stay bounded"
                              description="The future report must carry weak evidence warnings, rejected evidence exclusion, dedup no-amplification, coverage limits, and the rule that provider output is evidence, not truth."
                            />
                            {reportGenerationGateError ? <Alert type="error" showIcon message={reportGenerationGateError} /> : null}
                            <Form
                              form={reportGenerationGateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'report_gate_reviewer',
                                acknowledge_gate_only: true,
                                acknowledge_no_summary_report_generation: true,
                                acknowledge_no_b_end_report_generation: true,
                                acknowledge_no_export_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateReportGenerationGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Manual analysis execution id" name="manual_analysis_execution_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisExecution?.manual_analysis_execution_id || 'latest execution candidate'}
                                      options={manualAnalysisExecutions.map((item) => ({
                                        value: item.manual_analysis_execution_id,
                                        label: `${item.status} / ${item.manual_analysis_execution_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Result candidate id" name="result_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisResultCandidate?.result_candidate_id || 'latest result candidate'}
                                      options={manualAnalysisResultCandidates.map((item) => ({
                                        value: item.result_candidate_id,
                                        label: `${item.analysis_input_source} / ${item.result_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Boundary gate id" name="boundary_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisExecution?.boundary_gate_id || 'boundary from execution'}
                                      options={analysisResultBoundaryGates.map((item) => ({
                                        value: item.boundary_gate_id,
                                        label: `${item.status} / ${item.boundary_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="report_gate_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={16}>
                                  <Form.Item label="Gate note" name="note" rules={[{ required: true }]}>
                                    <TextArea
                                      rows={2}
                                      placeholder="Confirm future report boundaries; do not generate report artifacts in this step."
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Form.Item label="Required acknowledgements">
                                <Row gutter={[8, 4]}>
                                  {[
                                    ['acknowledge_gate_only', 'report generation gate only'],
                                    ['acknowledge_no_summary_report_generation', 'no Summary Report generation'],
                                    ['acknowledge_no_b_end_report_generation', 'no B-end report generation'],
                                    ['acknowledge_no_export_generation', 'no PDF/Markdown/deck export'],
                                    ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event generation'],
                                    ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                    ['acknowledge_no_production_case', 'no production case'],
                                    ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                    ['acknowledge_not_official_verification', 'not official verification'],
                                    ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                    ['acknowledge_weak_evidence_warning', 'weak evidence warning preserved'],
                                    ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                    ['acknowledge_dedup_no_risk_amplification', 'duplicate evidence not amplified'],
                                    ['acknowledge_audit_trace_required', 'audit trace required'],
                                  ].map(([name, label]) => (
                                    <Col xs={24} md={8} key={name}>
                                      <Form.Item name={name} valuePropName="checked" noStyle>
                                        <Checkbox>{label}</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  ))}
                                </Row>
                              </Form.Item>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={reportGenerationGateLoading}
                                  disabled={!reportGenerationGateReady || reportGenerationGateLoading}
                                >
                                  Create Report Gate
                                </Button>
                                {latestReportGenerationGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestReportGenerationGateJson, 'Report gate JSON copied')}
                                  >
                                    Copy latest report gate JSON
                                  </Button>
                                ) : null}
                                {reportGenerationGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportGenerationGatesJson, 'Report gate history JSON copied')}
                                  >
                                    Copy report gate history JSON
                                  </Button>
                                ) : null}
                                {reportGenerationGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportGenerationGateAuditsJson, 'Report gate audit JSON copied')}
                                  >
                                    Copy report gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestReportGenerationGate ? (
                              <Card size="small" title="Latest Report Generation Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestReportGenerationGate.status === 'report_gate_ready_for_future_runtime' ? 'green' : 'gold'}>
                                      {latestReportGenerationGate.status}
                                    </Tag>
                                    <Tag>{latestReportGenerationGate.requested_future_output}</Tag>
                                    <Text type="secondary">{latestReportGenerationGate.report_gate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="result_candidate_id">
                                      {latestReportGenerationGate.result_candidate_id}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="manual_analysis_execution_id">
                                      {latestReportGenerationGate.manual_analysis_execution_id}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="input boundary">
                                      source={latestReportGenerationGate.input_boundary?.source || '-'}, official_verification=
                                      {boolText(latestReportGenerationGate.input_boundary?.official_verification)}, full_web=
                                      {boolText(latestReportGenerationGate.input_boundary?.full_web_coverage)}, provider_truth=
                                      {boolText(latestReportGenerationGate.input_boundary?.provider_output_is_truth)}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="readiness">
                                      can_generate_summary_report_now=
                                      {boolText(latestReportGenerationGate.readiness?.can_generate_summary_report_now)}, requires_report_runtime=
                                      {boolText(latestReportGenerationGate.readiness?.requires_report_runtime)}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestReportGenerationGate.now_flags || {}).map(([key, value]) => (
                                      <Tag color={value ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList
                                    title="Allowed future outputs"
                                    items={Object.entries(latestReportGenerationGate.allowed_future_outputs || {}).map(
                                      ([key, value]) => `${key}: ${boolText(value)}`,
                                    )}
                                  />
                                  <SummaryList
                                    title="Required report sections"
                                    items={Object.entries(latestReportGenerationGate.required_report_sections || {}).map(
                                      ([key, value]) => `${key}: ${boolText(value)}`,
                                    )}
                                  />
                                  <SummaryList title="Report gate warnings" items={latestReportGenerationGate.warnings || []} />
                                  <SummaryList title="Blocked reasons" items={latestReportGenerationGate.blocked_reasons || []} />
                                  <SummaryList title="Boundary notes" items={latestReportGenerationGate.boundary_notes || []} />
                                  <SummaryList title="Recommended next steps" items={latestReportGenerationGate.recommended_next_steps || []} />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Report Generation Gate record yet.</Text>
                            )}
                            {reportGenerationGateAudits.length ? (
                              <Card size="small" title={`Report generation gate audit timeline (${reportGenerationGateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {reportGenerationGateAudits.map((audit) => (
                                    <Space wrap key={audit.report_gate_audit_id}>
                                      <Tag color="green">{audit.decision}</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">summary_report={boolText(audit.now_flags?.generate_summary_report_now)}</Text>
                                      <Text type="secondary">export={boolText(audit.now_flags?.export_now)}</Text>
                                      <Text type="secondary">public_event={boolText(audit.now_flags?.generate_public_event_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Summary Report Candidate / 摘要报告候选">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local candidate only / 仅创建本地候选摘要"
                              description="This creates a local Summary Report Candidate plus append-only audit only. It does not generate a final Summary Report, B-end report, PDF/Markdown/deck export, Sandbox fixture, public event, Evidence Layer write, production case, real API call, URL fetch, or LLM call."
                            />
                            {summaryReportCandidateError ? <Alert type="error" showIcon message={summaryReportCandidateError} /> : null}
                            <Form
                              form={summaryReportCandidateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'summary_candidate_reviewer',
                                note: 'Create local Summary Report Candidate only; do not generate final report artifacts.',
                                acknowledge_candidate_only: true,
                                acknowledge_not_final_summary_report: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_export_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateSummaryReportCandidate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Report gate id" name="report_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestReportGenerationGate?.report_gate_id || 'latest report gate'}
                                      options={reportGenerationGates.map((item) => ({
                                        value: item.report_gate_id,
                                        label: `${item.status} / ${item.report_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Result candidate id" name="result_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisResultCandidate?.result_candidate_id || 'latest result candidate'}
                                      options={manualAnalysisResultCandidates.map((item) => ({
                                        value: item.result_candidate_id,
                                        label: `${item.analysis_input_source} / ${item.result_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Manual execution id" name="manual_analysis_execution_id">
                                    <Select
                                      allowClear
                                      placeholder={latestManualAnalysisExecution?.manual_analysis_execution_id || 'latest execution'}
                                      options={manualAnalysisExecutions.map((item) => ({
                                        value: item.manual_analysis_execution_id,
                                        label: `${item.status} / ${item.manual_analysis_execution_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Boundary gate id" name="boundary_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestAnalysisResultBoundaryGate?.boundary_gate_id || 'latest boundary gate'}
                                      options={analysisResultBoundaryGates.map((item) => ({
                                        value: item.boundary_gate_id,
                                        label: `${item.status} / ${item.boundary_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={8}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="summary_candidate_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={16}>
                                  <Form.Item label="Candidate note" name="note" rules={[{ required: true }]}>
                                    <TextArea
                                      rows={2}
                                      placeholder="Confirm this remains a local candidate and does not generate final report artifacts."
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Form.Item label="Required acknowledgements">
                                <Row gutter={[8, 4]}>
                                  {[
                                    ['acknowledge_candidate_only', 'candidate only'],
                                    ['acknowledge_not_final_summary_report', 'not final Summary Report'],
                                    ['acknowledge_no_b_end_report', 'no B-end report'],
                                    ['acknowledge_no_export_generation', 'no export generation'],
                                    ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                    ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                    ['acknowledge_no_production_case', 'no production case'],
                                    ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                    ['acknowledge_not_official_verification', 'not official verification'],
                                    ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                    ['acknowledge_weak_evidence_warning', 'weak evidence warning preserved'],
                                    ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                    ['acknowledge_dedup_no_risk_amplification', 'duplicate evidence not amplified'],
                                    ['acknowledge_audit_trace_required', 'audit trace required'],
                                  ].map(([name, label]) => (
                                    <Col xs={24} md={8} key={name}>
                                      <Form.Item name={name} valuePropName="checked" noStyle>
                                        <Checkbox>{label}</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  ))}
                                </Row>
                              </Form.Item>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={summaryReportCandidateLoading}
                                  disabled={!summaryReportCandidateReady || summaryReportCandidateLoading}
                                >
                                  Create Summary Report Candidate
                                </Button>
                                {latestSummaryReportCandidate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestSummaryReportCandidateJson, 'Summary candidate JSON copied')}
                                  >
                                    Copy latest summary candidate JSON
                                  </Button>
                                ) : null}
                                {summaryReportCandidates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(summaryReportCandidatesJson, 'Summary candidate history JSON copied')}
                                  >
                                    Copy summary candidate history JSON
                                  </Button>
                                ) : null}
                                {summaryReportCandidateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(summaryReportCandidateAuditsJson, 'Summary candidate audit JSON copied')}
                                  >
                                    Copy summary candidate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestSummaryReportCandidate ? (
                              <Card size="small" title="Latest Summary Report Candidate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestSummaryReportCandidate.status === 'summary_report_candidate_created' ? 'green' : 'gold'}>
                                      {latestSummaryReportCandidate.status}
                                    </Tag>
                                    <Text type="secondary">{latestSummaryReportCandidate.summary_report_candidate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="title">
                                      {latestSummaryReportCandidate.executive_summary_candidate?.title || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="candidate note">
                                      {latestSummaryReportCandidate.executive_summary_candidate?.candidate_only_note || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="source scope">
                                      {latestSummaryReportCandidate.evidence_scope_section?.source_scope_summary || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream flags">
                                      {Object.entries(latestSummaryReportCandidate.downstream_flags || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestSummaryReportCandidate.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'summary_report_candidate_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Summary candidate warnings" items={latestSummaryReportCandidate.warnings || []} />
                                  <SummaryList title="Limitations" items={latestSummaryReportCandidate.limitations || []} />
                                  <SummaryList
                                    title="Boundary block"
                                    items={Object.entries(latestSummaryReportCandidate.boundary_block || {}).map(
                                      ([key, value]) => `${key}: ${String(value)}`,
                                    )}
                                  />
                                  <SummaryList
                                    title="Representative evidence notes"
                                    items={[
                                      latestSummaryReportCandidate.representative_evidence_section?.redaction_note,
                                      latestSummaryReportCandidate.representative_evidence_section?.rejected_exclusion_note,
                                      latestSummaryReportCandidate.representative_evidence_section?.weak_evidence_note,
                                      latestSummaryReportCandidate.representative_evidence_section?.duplicate_no_amplification_note,
                                    ].filter(Boolean)}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Summary Report Candidate record yet.</Text>
                            )}
                            {summaryReportCandidateAudits.length ? (
                              <Card size="small" title={`Summary report candidate audit timeline (${summaryReportCandidateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {summaryReportCandidateAudits.map((audit) => (
                                    <Space wrap key={audit.summary_report_candidate_audit_id}>
                                      <Tag color="green">{audit.decision}</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">final_report={boolText(audit.now_flags?.final_report_now)}</Text>
                                      <Text type="secondary">export={boolText(audit.now_flags?.export_now)}</Text>
                                      <Text type="secondary">sandbox={boolText(audit.now_flags?.sandbox_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Final Summary Report Review Gate / 最终摘要报告复核门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local final-review gate only / 仅本地最终复核门"
                              description="This creates a local final-review gate plus append-only audit only. It does not create final Summary Report, B-end report, export files, Sandbox, public event, Evidence Layer write, production case, real API call, URL fetch, or LLM call."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Boundary rules"
                              description="Future final report runtime must preserve the boundary block. Weak evidence remains warning-marked, rejected evidence remains excluded, duplicate evidence must not amplify risk, provider output is evidence not truth, and this is not official verification or full-web coverage."
                            />
                            {finalSummaryReportReviewGateError ? (
                              <Alert type="error" showIcon message={finalSummaryReportReviewGateError} />
                            ) : null}
                            <Form
                              form={finalSummaryReportReviewGateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'final_summary_reviewer',
                                note: 'Review local Summary Report Candidate for future final runtime only; do not generate final artifacts.',
                                review_decision: 'approve_for_future_final_runtime',
                                acknowledge_review_gate_only: true,
                                acknowledge_no_final_summary_report_generation: true,
                                acknowledge_no_b_end_report_generation: true,
                                acknowledge_no_export_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateFinalSummaryReportReviewGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Summary candidate id" name="summary_report_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestSummaryReportCandidate?.summary_report_candidate_id || 'latest summary candidate'}
                                      options={summaryReportCandidates.map((item) => ({
                                        value: item.summary_report_candidate_id,
                                        label: `${item.status} / ${item.summary_report_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Report gate id" name="report_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestSummaryReportCandidate?.report_gate_id || latestReportGenerationGate?.report_gate_id || 'latest report gate'}
                                      options={reportGenerationGates.map((item) => ({
                                        value: item.report_gate_id,
                                        label: `${item.status} / ${item.report_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Result candidate id" name="result_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestSummaryReportCandidate?.result_candidate_id || 'latest result candidate'}
                                      options={manualAnalysisResultCandidates.map((item) => ({
                                        value: item.result_candidate_id,
                                        label: `${item.analysis_input_source} / ${item.result_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Manual execution id" name="manual_analysis_execution_id">
                                    <Select
                                      allowClear
                                      placeholder={latestSummaryReportCandidate?.manual_analysis_execution_id || 'latest execution'}
                                      options={manualAnalysisExecutions.map((item) => ({
                                        value: item.manual_analysis_execution_id,
                                        label: `${item.status} / ${item.manual_analysis_execution_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Boundary gate id" name="boundary_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestSummaryReportCandidate?.boundary_gate_id || 'latest boundary gate'}
                                      options={analysisResultBoundaryGates.map((item) => ({
                                        value: item.boundary_gate_id,
                                        label: `${item.status} / ${item.boundary_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Review decision" name="review_decision" rules={[{ required: true }]}>
                                    <Select options={FINAL_SUMMARY_REVIEW_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="final_summary_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Review case id" name="review_case_id">
                                    <Input placeholder={latestSummaryReportCandidate?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item label="Review note" name="note" rules={[{ required: true }]}>
                                    <TextArea
                                      rows={2}
                                      placeholder="Confirm this gate remains local review only and does not generate final report artifacts."
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item
                                    label="Required revisions (one per line; required for request_revision)"
                                    name="required_revisions"
                                  >
                                    <TextArea rows={2} placeholder="Clarify evidence scope wording before future final runtime." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Form.Item label="Required acknowledgements">
                                <Row gutter={[8, 4]}>
                                  {[
                                    ['acknowledge_review_gate_only', 'review gate only'],
                                    ['acknowledge_no_final_summary_report_generation', 'no final Summary Report'],
                                    ['acknowledge_no_b_end_report_generation', 'no B-end report'],
                                    ['acknowledge_no_export_generation', 'no export generation'],
                                    ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                    ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                    ['acknowledge_no_production_case', 'no production case'],
                                    ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                    ['acknowledge_not_official_verification', 'not official verification'],
                                    ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                    ['acknowledge_weak_evidence_warning', 'weak evidence warning preserved'],
                                    ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                    ['acknowledge_dedup_no_risk_amplification', 'duplicate evidence not amplified'],
                                    ['acknowledge_audit_trace_required', 'audit trace required'],
                                  ].map(([name, label]) => (
                                    <Col xs={24} md={8} key={name}>
                                      <Form.Item name={name} valuePropName="checked" noStyle>
                                        <Checkbox>{label}</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  ))}
                                </Row>
                              </Form.Item>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={finalSummaryReportReviewGateLoading}
                                  disabled={!finalSummaryReportReviewGateReady || finalSummaryReportReviewGateLoading}
                                >
                                  Create Final Review Gate
                                </Button>
                                {latestFinalSummaryReportReviewGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestFinalSummaryReportReviewGateJson, 'Final review gate JSON copied')}
                                  >
                                    Copy latest final review gate JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportReviewGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportReviewGatesJson, 'Final review gate history JSON copied')}
                                  >
                                    Copy final review gate history JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportReviewGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportReviewGateAuditsJson, 'Final review gate audit JSON copied')}
                                  >
                                    Copy final review gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestFinalSummaryReportReviewGate ? (
                              <Card size="small" title="Latest Final Summary Report Review Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={FINAL_SUMMARY_REVIEW_STATUS_COLOR[latestFinalSummaryReportReviewGate.status] || 'default'}>
                                      {latestFinalSummaryReportReviewGate.status}
                                    </Tag>
                                    <Tag color="blue">{latestFinalSummaryReportReviewGate.review_decision}</Tag>
                                    <Text type="secondary">{latestFinalSummaryReportReviewGate.final_report_review_gate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="summary_candidate">
                                      {latestFinalSummaryReportReviewGate.summary_report_candidate_id || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="input_boundary">
                                      {Object.entries(latestFinalSummaryReportReviewGate.input_boundary || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream_readiness">
                                      {Object.entries(latestFinalSummaryReportReviewGate.downstream_readiness || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportReviewGate.required_final_report_sections || {}).map(([key, value]) => (
                                      <Tag color={value ? 'green' : 'red'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportReviewGate.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'final_summary_report_review_gate_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Blocked reasons / revision requests" items={latestFinalSummaryReportReviewGate.blocked_reasons || []} />
                                  <SummaryList title="Required revisions" items={latestFinalSummaryReportReviewGate.required_revisions || []} />
                                  <SummaryList title="Warnings" items={latestFinalSummaryReportReviewGate.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestFinalSummaryReportReviewGate.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit refs"
                                    items={Object.entries(latestFinalSummaryReportReviewGate.audit_refs || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Final Summary Report Review Gate record yet.</Text>
                            )}
                            {finalSummaryReportReviewGateAudits.length ? (
                              <Card size="small" title={`Final review gate audit timeline (${finalSummaryReportReviewGateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {finalSummaryReportReviewGateAudits.map((audit) => (
                                    <Space wrap key={audit.final_report_review_gate_audit_id}>
                                      <Tag color="green">{audit.review_decision || 'review_recorded'}</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">final_report={boolText(audit.now_flags?.final_summary_report_now)}</Text>
                                      <Text type="secondary">b_end={boolText(audit.now_flags?.b_end_report_now)}</Text>
                                      <Text type="secondary">export={boolText(audit.now_flags?.export_now)}</Text>
                                      <Text type="secondary">sandbox={boolText(audit.now_flags?.generate_sandbox_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.generate_public_event_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Final Summary Report / 最终摘要报告">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local final summary report only"
                              description="This creates a local FinalSummaryReport object only. It does not export PDF/Markdown/deck, create B-end report, Sandbox, public event, Evidence Layer write, or production case."
                            />
                            <Alert
                              type="info"
                              showIcon
                              message="Required boundaries"
                              description="Export/B-end/Sandbox/public event require separate gates. Provider output is evidence, not truth. This is not official verification and not full-web, full-platform, or full-thread coverage."
                            />
                            {finalSummaryReportError ? (
                              <Alert type="error" showIcon message={finalSummaryReportError} />
                            ) : null}
                            <Form
                              form={finalSummaryReportForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'final_summary_report_reviewer',
                                note: 'Create local Final Summary Report object only; preserve boundary notes and keep downstream outputs disabled.',
                                acknowledge_local_final_summary_report_only: true,
                                acknowledge_no_pdf_export: true,
                                acknowledge_no_markdown_export: true,
                                acknowledge_no_deck_export: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateFinalSummaryReport}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Summary candidate id" name="summary_report_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.summary_report_candidate_id || 'latest summary candidate'}
                                      options={summaryReportCandidates.map((item) => ({
                                        value: item.summary_report_candidate_id,
                                        label: `${item.status} / ${item.summary_report_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Final review gate id" name="final_report_review_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.final_report_review_gate_id || 'latest final review gate'}
                                      options={finalSummaryReportReviewGates.map((item) => ({
                                        value: item.final_report_review_gate_id,
                                        label: `${item.status} / ${item.final_report_review_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Report gate id" name="report_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.report_gate_id || 'latest report gate'}
                                      options={reportGenerationGates.map((item) => ({
                                        value: item.report_gate_id,
                                        label: `${item.status} / ${item.report_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Boundary gate id" name="boundary_gate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.boundary_gate_id || 'latest boundary gate'}
                                      options={analysisResultBoundaryGates.map((item) => ({
                                        value: item.boundary_gate_id,
                                        label: `${item.status} / ${item.boundary_gate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={12}>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Result candidate id" name="result_candidate_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.result_candidate_id || 'latest result candidate'}
                                      options={manualAnalysisResultCandidates.map((item) => ({
                                        value: item.result_candidate_id,
                                        label: `${item.analysis_input_source} / ${item.result_candidate_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Manual execution id" name="manual_analysis_execution_id">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportReviewGate?.manual_analysis_execution_id || 'latest execution'}
                                      options={manualAnalysisExecutions.map((item) => ({
                                        value: item.manual_analysis_execution_id,
                                        label: `${item.status} / ${item.manual_analysis_execution_id}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Reviewer label" name="reviewer_label" rules={[{ required: true }]}>
                                    <Input placeholder="final_summary_report_reviewer" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={6}>
                                  <Form.Item label="Review case id" name="review_case_id">
                                    <Input placeholder={latestFinalSummaryReportReviewGate?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Form.Item label="Final report note" name="note" rules={[{ required: true }]}>
                                <TextArea
                                  rows={2}
                                  placeholder="Confirm this is a local final summary report object only and all downstream outputs require later gates."
                                />
                              </Form.Item>
                              <Form.Item label="Required acknowledgements">
                                <Row gutter={[8, 4]}>
                                  {[
                                    ['acknowledge_local_final_summary_report_only', 'local final summary report object only'],
                                    ['acknowledge_no_pdf_export', 'no PDF export'],
                                    ['acknowledge_no_markdown_export', 'no Markdown export'],
                                    ['acknowledge_no_deck_export', 'no briefing deck export'],
                                    ['acknowledge_no_b_end_report', 'no B-end report'],
                                    ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                    ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                    ['acknowledge_no_production_case', 'no production case'],
                                    ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                    ['acknowledge_not_official_verification', 'not official verification'],
                                    ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                    ['acknowledge_weak_evidence_warning', 'weak evidence warning preserved'],
                                    ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                    ['acknowledge_dedup_no_risk_amplification', 'duplicate evidence not amplified'],
                                    ['acknowledge_audit_trace_required', 'audit trace required'],
                                  ].map(([name, label]) => (
                                    <Col xs={24} md={8} key={name}>
                                      <Form.Item name={name} valuePropName="checked" noStyle>
                                        <Checkbox>{label}</Checkbox>
                                      </Form.Item>
                                    </Col>
                                  ))}
                                </Row>
                              </Form.Item>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={finalSummaryReportLoading}
                                  disabled={!finalSummaryReportReady || finalSummaryReportLoading}
                                >
                                  Create Local Final Summary Report
                                </Button>
                                {latestFinalSummaryReport ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestFinalSummaryReportJson, 'Final summary report JSON copied')}
                                  >
                                    Copy latest final report JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReports.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportsJson, 'Final summary report history JSON copied')}
                                  >
                                    Copy final report history JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportAuditsJson, 'Final summary report audit JSON copied')}
                                  >
                                    Copy final report audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestFinalSummaryReport ? (
                              <Card size="small" title="Latest Final Summary Report">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={latestFinalSummaryReport.status === 'final_summary_report_created' ? 'green' : 'gold'}>
                                      {latestFinalSummaryReport.status}
                                    </Tag>
                                    <Text type="secondary">{latestFinalSummaryReport.final_summary_report_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="source">
                                      {Object.entries(latestFinalSummaryReport.source_and_scope || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream flags">
                                      {Object.entries(latestFinalSummaryReport.downstream_flags || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="required next gates">
                                      {Object.entries(latestFinalSummaryReport.required_next_gates || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReport.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'local_final_summary_report_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Final report warnings" items={latestFinalSummaryReport.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestFinalSummaryReport.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit trace"
                                    items={Object.entries(latestFinalSummaryReport.report_sections?.audit_trace || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                  <Card size="small" title="Report sections preview">
                                    <pre className="code-preview">
                                      {JSON.stringify(latestFinalSummaryReport.report_sections || {}, null, 2)}
                                    </pre>
                                  </Card>
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Final Summary Report record yet.</Text>
                            )}
                            {finalSummaryReportAudits.length ? (
                              <Card size="small" title={`Final summary report audit timeline (${finalSummaryReportAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {finalSummaryReportAudits.map((audit) => (
                                    <Space wrap key={audit.final_summary_report_audit_id}>
                                      <Tag color="green">final_report_created</Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">pdf={boolText(audit.now_flags?.pdf_export_now)}</Text>
                                      <Text type="secondary">markdown={boolText(audit.now_flags?.markdown_export_now)}</Text>
                                      <Text type="secondary">deck={boolText(audit.now_flags?.deck_export_now)}</Text>
                                      <Text type="secondary">b_end={boolText(audit.now_flags?.b_end_report_now)}</Text>
                                      <Text type="secondary">sandbox={boolText(audit.now_flags?.generate_sandbox_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.generate_public_event_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Final Summary Report Export Gate / 最终摘要报告导出门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="info"
                              showIcon
                              message="Export gate records future readiness only"
                              description="This gate does not generate Markdown, PDF, PPTX, B-end report, Sandbox fixture, public event, Evidence Layer write, production case, or any real LLM/API output. Future export runtime must preserve evidence boundaries, weak warnings, rejected-evidence exclusion, dedup no-amplification, and coverage limitations."
                            />
                            {finalSummaryReportExportGateError ? (
                              <Alert type="error" showIcon message={finalSummaryReportExportGateError} />
                            ) : null}
                            <Form
                              form={finalSummaryReportExportGateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'local_export_gate_reviewer',
                                note: 'Review local Final Summary Report for future export runtime only; do not generate files now.',
                                export_decision: 'approve_for_future_export_runtime',
                                acknowledge_export_gate_only: true,
                                acknowledge_no_markdown_file_now: true,
                                acknowledge_no_pdf_file_now: true,
                                acknowledge_no_pptx_file_now: true,
                                acknowledge_no_b_end_report_generation: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateFinalSummaryReportExportGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_summary_report_id" label="Final Summary Report ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReport?.final_summary_report_id || 'latest final summary report'}
                                      options={finalSummaryReports.map((item) => ({
                                        value: item.final_summary_report_id,
                                        label: `${item.final_summary_report_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_summary_report_audit_id" label="Final Summary Report Audit ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportAudit?.final_summary_report_audit_id || 'latest final report audit'}
                                      options={finalSummaryReportAudits.map((item) => ({
                                        value: item.final_summary_report_audit_id,
                                        label: `${item.final_summary_report_audit_id} / ${item.decided_at || '-'}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="summary_report_candidate_id" label="Summary Report Candidate ID">
                                    <Input placeholder={latestFinalSummaryReport?.summary_report_candidate_id || 'latest summary candidate'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_report_review_gate_id" label="Final Report Review Gate ID">
                                    <Input placeholder={latestFinalSummaryReport?.final_report_review_gate_id || 'latest final review gate'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="report_gate_id" label="Report Gate ID">
                                    <Input placeholder={latestFinalSummaryReport?.report_gate_id || 'latest report gate'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="boundary_gate_id" label="Boundary Gate ID">
                                    <Input placeholder={latestFinalSummaryReport?.boundary_gate_id || 'latest boundary gate'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="result_candidate_id" label="Analysis Result Candidate ID">
                                    <Input placeholder={latestFinalSummaryReport?.result_candidate_id || 'latest result candidate'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="manual_analysis_execution_id" label="Manual Analysis Execution ID">
                                    <Input placeholder={latestFinalSummaryReport?.manual_analysis_execution_id || 'latest execution'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="review_case_id" label="Review-only Case ID">
                                    <Input placeholder={latestFinalSummaryReport?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_decision" label="Export gate decision" rules={[{ required: true }]}>
                                    <Select options={FINAL_SUMMARY_EXPORT_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="reviewer_label" label="Reviewer label" rules={[{ required: true }]}>
                                    <Input />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="note" label="Gate note" rules={[{ required: true }]}>
                                    <TextArea rows={2} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="required_revisions" label="Required revisions (required only for request_revision)">
                                    <TextArea rows={2} placeholder="One revision per line, or comma separated." />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={8}>
                                {[
                                  ['acknowledge_export_gate_only', 'export gate record only'],
                                  ['acknowledge_no_markdown_file_now', 'no Markdown file now'],
                                  ['acknowledge_no_pdf_file_now', 'no PDF file now'],
                                  ['acknowledge_no_pptx_file_now', 'no PPTX/deck file now'],
                                  ['acknowledge_no_b_end_report_generation', 'no B-end report now'],
                                  ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                  ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'no production case'],
                                  ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                  ['acknowledge_not_official_verification', 'not official verification'],
                                  ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                  ['acknowledge_weak_evidence_warning', 'preserve weak evidence warning'],
                                  ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                  ['acknowledge_dedup_no_risk_amplification', 'dedup no risk amplification'],
                                  ['acknowledge_audit_trace_required', 'audit trace required'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={finalSummaryReportExportGateLoading}
                                  disabled={!finalSummaryReportExportGateReady || finalSummaryReportExportGateLoading}
                                >
                                  Create Export Gate
                                </Button>
                                {latestFinalSummaryReportExportGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestFinalSummaryReportExportGateJson, 'Export gate JSON copied')}
                                  >
                                    Copy latest export gate JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportExportGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportExportGatesJson, 'Export gate history JSON copied')}
                                  >
                                    Copy export gate history JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportExportGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportExportGateAuditsJson, 'Export gate audit JSON copied')}
                                  >
                                    Copy export gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestFinalSummaryReportExportGate ? (
                              <Card size="small" title="Latest Final Summary Report Export Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={FINAL_SUMMARY_EXPORT_STATUS_COLOR[latestFinalSummaryReportExportGate.status] || 'default'}>
                                      {latestFinalSummaryReportExportGate.status}
                                    </Tag>
                                    <Tag color="blue">{latestFinalSummaryReportExportGate.export_decision}</Tag>
                                    <Text type="secondary">{latestFinalSummaryReportExportGate.export_gate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="final_summary_report_id">
                                      {latestFinalSummaryReportExportGate.final_summary_report_id || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="allowed future exports">
                                      {Object.entries(latestFinalSummaryReportExportGate.allowed_future_exports || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="not allowed now">
                                      {Object.entries(latestFinalSummaryReportExportGate.not_allowed_now || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream readiness">
                                      {Object.entries(latestFinalSummaryReportExportGate.downstream_readiness || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="input boundary">
                                      {Object.entries(latestFinalSummaryReportExportGate.input_boundary || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportExportGate.required_export_sections || {}).map(([key, value]) => (
                                      <Tag color={value ? 'blue' : 'red'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportExportGate.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'final_summary_report_export_gate_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Blocked reasons" items={latestFinalSummaryReportExportGate.blocked_reasons || []} />
                                  <SummaryList title="Required revisions" items={latestFinalSummaryReportExportGate.required_revisions || []} />
                                  <SummaryList title="Warnings" items={latestFinalSummaryReportExportGate.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestFinalSummaryReportExportGate.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit refs"
                                    items={Object.entries(latestFinalSummaryReportExportGate.audit_refs || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Final Summary Report Export Gate record yet.</Text>
                            )}
                            {finalSummaryReportExportGateAudits.length ? (
                              <Card size="small" title={`Export gate audit timeline (${finalSummaryReportExportGateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {finalSummaryReportExportGateAudits.map((audit) => (
                                    <Space wrap key={audit.export_gate_audit_id}>
                                      <Tag color={FINAL_SUMMARY_EXPORT_STATUS_COLOR[audit.export_decision] || 'blue'}>
                                        {audit.export_decision}
                                      </Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">markdown={boolText(audit.now_flags?.markdown_file_now)}</Text>
                                      <Text type="secondary">pdf={boolText(audit.now_flags?.pdf_file_now)}</Text>
                                      <Text type="secondary">pptx={boolText(audit.now_flags?.pptx_file_now)}</Text>
                                      <Text type="secondary">b_end={boolText(audit.now_flags?.b_end_report_now)}</Text>
                                      <Text type="secondary">sandbox={boolText(audit.now_flags?.sandbox_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.public_event_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Final Summary Report Export Artifact / 最终摘要报告导出物">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local runtime export artifact only"
                              description="This creates a local artifact under ignored runtime only. It is not a B-end report, Sandbox fixture, public event, Evidence Layer write, production case, official verification, full-web/full-platform/full-thread coverage, or public download. PDF is unsupported unless a safe repo-local renderer exists; PPTX binary is unsupported and deck outline is JSON only."
                            />
                            {finalSummaryReportExportArtifactError ? (
                              <Alert type="error" showIcon message={finalSummaryReportExportArtifactError} />
                            ) : null}
                            <Form
                              form={finalSummaryReportExportArtifactForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'local_export_artifact_reviewer',
                                note: 'Create local export artifact under ignored runtime only.',
                                artifact_type: 'analyst_markdown',
                                acknowledge_export_artifact_only: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateFinalSummaryReportExportArtifact}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_summary_report_id" label="Final Summary Report ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportGate?.final_summary_report_id || 'latest final summary report'}
                                      options={finalSummaryReports.map((item) => ({
                                        value: item.final_summary_report_id,
                                        label: `${item.final_summary_report_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_gate_id" label="Export Gate ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportGate?.export_gate_id || 'latest ready export gate'}
                                      options={finalSummaryReportExportGates.map((item) => ({
                                        value: item.export_gate_id,
                                        label: `${item.export_gate_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_gate_audit_id" label="Export Gate Audit ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportGateAudit?.export_gate_audit_id || 'latest export gate audit'}
                                      options={finalSummaryReportExportGateAudits.map((item) => ({
                                        value: item.export_gate_audit_id,
                                        label: `${item.export_gate_audit_id} / ${item.decided_at || '-'}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="review_case_id" label="Review-only Case ID">
                                    <Input placeholder={latestFinalSummaryReportExportGate?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="artifact_type" label="Artifact type" rules={[{ required: true }]}>
                                    <Select options={FINAL_SUMMARY_EXPORT_ARTIFACT_TYPE_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="reviewer_label" label="Reviewer label" rules={[{ required: true }]}>
                                    <Input />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="note" label="Artifact note" rules={[{ required: true }]}>
                                    <TextArea rows={2} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={8}>
                                {[
                                  ['acknowledge_export_artifact_only', 'local export artifact only'],
                                  ['acknowledge_no_b_end_report', 'not B-end report'],
                                  ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                  ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'no production case'],
                                  ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                  ['acknowledge_not_official_verification', 'not official verification'],
                                  ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                  ['acknowledge_weak_evidence_warning', 'preserve weak evidence warning'],
                                  ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                  ['acknowledge_dedup_no_risk_amplification', 'dedup no risk amplification'],
                                  ['acknowledge_audit_trace_required', 'audit trace required'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<FileJson size={16} />}
                                  loading={finalSummaryReportExportArtifactLoading}
                                  disabled={!finalSummaryReportExportArtifactReady || finalSummaryReportExportArtifactLoading}
                                >
                                  Create Local Export Artifact
                                </Button>
                                {latestFinalSummaryReportExportArtifact ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestFinalSummaryReportExportArtifactJson, 'Export artifact JSON copied')}
                                  >
                                    Copy latest artifact JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportExportArtifacts.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportExportArtifactsJson, 'Export artifact history JSON copied')}
                                  >
                                    Copy artifact history JSON
                                  </Button>
                                ) : null}
                                {finalSummaryReportExportArtifactAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(finalSummaryReportExportArtifactAuditsJson, 'Export artifact audit JSON copied')}
                                  >
                                    Copy artifact audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestFinalSummaryReportExportArtifact ? (
                              <Card size="small" title="Latest Final Summary Report Export Artifact">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={FINAL_SUMMARY_EXPORT_ARTIFACT_STATUS_COLOR[latestFinalSummaryReportExportArtifact.status] || 'default'}>
                                      {latestFinalSummaryReportExportArtifact.status}
                                    </Tag>
                                    <Tag color="blue">{latestFinalSummaryReportExportArtifact.artifact_type}</Tag>
                                    <Tag>{latestFinalSummaryReportExportArtifact.artifact_format}</Tag>
                                    <Text type="secondary">{latestFinalSummaryReportExportArtifact.export_artifact_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="local_runtime_path">
                                      {latestFinalSummaryReportExportArtifact.artifact_paths?.local_runtime_path || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="public_url">
                                      {latestFinalSummaryReportExportArtifact.artifact_paths?.public_url || 'none'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="artifact scope">
                                      {Object.entries(latestFinalSummaryReportExportArtifact.artifact_scope || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="source and scope">
                                      {Object.entries(latestFinalSummaryReportExportArtifact.source_and_scope || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream flags">
                                      {Object.entries(latestFinalSummaryReportExportArtifact.downstream_flags || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="required next gates">
                                      {Object.entries(latestFinalSummaryReportExportArtifact.required_next_gates || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportExportArtifact.export_sections || {}).map(([key, value]) => (
                                      <Tag color={value ? 'blue' : 'red'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <Space wrap>
                                    {Object.entries(latestFinalSummaryReportExportArtifact.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'local_export_artifact_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Warnings" items={latestFinalSummaryReportExportArtifact.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestFinalSummaryReportExportArtifact.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit refs"
                                    items={Object.entries(latestFinalSummaryReportExportArtifact.audit_refs || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Final Summary Report Export Artifact yet.</Text>
                            )}
                            {finalSummaryReportExportArtifactAudits.length ? (
                              <Card size="small" title={`Export artifact audit timeline (${finalSummaryReportExportArtifactAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {finalSummaryReportExportArtifactAudits.map((audit) => (
                                    <Space wrap key={audit.export_artifact_audit_id}>
                                      <Tag color="green">{audit.artifact_type}</Tag>
                                      <Tag>{audit.artifact_format}</Tag>
                                      <Text type="secondary">{audit.created_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">b_end={boolText(audit.now_flags?.b_end_report_now)}</Text>
                                      <Text type="secondary">sandbox={boolText(audit.now_flags?.generate_sandbox_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.generate_public_event_now)}</Text>
                                      <Text type="secondary">llm={boolText(audit.now_flags?.call_llm_now)}</Text>
                                      <Text type="secondary">fetch={boolText(audit.now_flags?.fetch_url_now)}</Text>
                                      <Text type="secondary">rows={boolText(audit.now_flags?.read_original_rows_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Report Export Download / Package Gate / 报告导出下载打包门">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Gate record only: no download route, no ZIP package, no public or signed URL"
                              description="This records whether the local export artifact is eligible for a future download/package runtime. It does not create a downloadable file, package archive, B-end report, Sandbox fixture, public event page, Evidence Layer write, production case, or official verification."
                            />
                            {reportExportDownloadPackageGateError ? (
                              <Alert type="error" showIcon message={reportExportDownloadPackageGateError} />
                            ) : null}
                            <Form
                              form={reportExportDownloadPackageGateForm}
                              layout="vertical"
                              initialValues={{
                                reviewer_label: 'download_package_gate_reviewer',
                                note: 'Record future download/package eligibility only. Do not create routes, packages, public URLs, or signed URLs.',
                                delivery_decision: 'approve_for_future_download_package_runtime',
                                acknowledge_download_package_gate_only: true,
                                acknowledge_no_download_route_now: true,
                                acknowledge_no_package_or_zip_now: true,
                                acknowledge_no_public_or_signed_url_now: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateReportExportDownloadPackageGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_artifact_id" label="Export Artifact ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportArtifact?.export_artifact_id || 'latest export artifact'}
                                      options={finalSummaryReportExportArtifacts.map((item) => ({
                                        value: item.export_artifact_id,
                                        label: `${item.export_artifact_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_artifact_audit_id" label="Export Artifact Audit ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportArtifactAudit?.export_artifact_audit_id || 'latest artifact audit'}
                                      options={finalSummaryReportExportArtifactAudits.map((item) => ({
                                        value: item.export_artifact_audit_id,
                                        label: `${item.export_artifact_audit_id} / ${item.created_at || '-'}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_summary_report_id" label="Final Summary Report ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportArtifact?.final_summary_report_id || 'latest final summary report'}
                                      options={finalSummaryReports.map((item) => ({
                                        value: item.final_summary_report_id,
                                        label: `${item.final_summary_report_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="export_gate_id" label="Export Gate ID">
                                    <Select
                                      allowClear
                                      placeholder={latestFinalSummaryReportExportArtifact?.export_gate_id || 'latest export gate'}
                                      options={finalSummaryReportExportGates.map((item) => ({
                                        value: item.export_gate_id,
                                        label: `${item.export_gate_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="review_case_id" label="Review-only Case ID">
                                    <Input placeholder={latestFinalSummaryReportExportArtifact?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="delivery_decision" label="Delivery decision" rules={[{ required: true }]}>
                                    <Select options={REPORT_EXPORT_DOWNLOAD_PACKAGE_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="reviewer_label" label="Reviewer label" rules={[{ required: true }]}>
                                    <Input />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="required_revisions" label="Required revisions">
                                    <Input placeholder="required when decision=request_revision" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="note" label="Gate note" rules={[{ required: true }]}>
                                    <TextArea rows={2} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={8}>
                                {[
                                  ['acknowledge_download_package_gate_only', 'download/package gate only'],
                                  ['acknowledge_no_download_route_now', 'no download route now'],
                                  ['acknowledge_no_package_or_zip_now', 'no package or ZIP now'],
                                  ['acknowledge_no_public_or_signed_url_now', 'no public or signed URL now'],
                                  ['acknowledge_no_b_end_report', 'not B-end report'],
                                  ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                  ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'no production case'],
                                  ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                  ['acknowledge_not_official_verification', 'not official verification'],
                                  ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                  ['acknowledge_weak_evidence_warning', 'preserve weak evidence warning'],
                                  ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                  ['acknowledge_dedup_no_risk_amplification', 'dedup no risk amplification'],
                                  ['acknowledge_audit_trace_required', 'audit trace required'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={reportExportDownloadPackageGateLoading}
                                  disabled={!reportExportDownloadPackageGateReady || reportExportDownloadPackageGateLoading}
                                >
                                  Create Download / Package Gate
                                </Button>
                                {latestReportExportDownloadPackageGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestReportExportDownloadPackageGateJson, 'Download/package gate JSON copied')}
                                  >
                                    Copy latest gate JSON
                                  </Button>
                                ) : null}
                                {reportExportDownloadPackageGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportExportDownloadPackageGatesJson, 'Download/package gate history JSON copied')}
                                  >
                                    Copy gate history JSON
                                  </Button>
                                ) : null}
                                {reportExportDownloadPackageGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportExportDownloadPackageGateAuditsJson, 'Download/package gate audit JSON copied')}
                                  >
                                    Copy gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestReportExportDownloadPackageGate ? (
                              <Card size="small" title="Latest Report Export Download / Package Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[latestReportExportDownloadPackageGate.status] || 'default'}>
                                      {latestReportExportDownloadPackageGate.status}
                                    </Tag>
                                    <Tag color="blue">{latestReportExportDownloadPackageGate.delivery_decision}</Tag>
                                    <Text type="secondary">{latestReportExportDownloadPackageGate.download_package_gate_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="export_artifact_id">
                                      {latestReportExportDownloadPackageGate.export_artifact_id || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="future delivery candidates">
                                      {Object.entries(latestReportExportDownloadPackageGate.allowed_future_delivery || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="not allowed now">
                                      {Object.entries(latestReportExportDownloadPackageGate.not_allowed_now || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="input boundary">
                                      {Object.entries(latestReportExportDownloadPackageGate.input_boundary || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="delivery boundary">
                                      {Object.entries(latestReportExportDownloadPackageGate.delivery_boundary || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream readiness">
                                      {Object.entries(latestReportExportDownloadPackageGate.downstream_readiness || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestReportExportDownloadPackageGate.safe_mode || {}).map(([key, value]) => (
                                      <Tag color={value && key !== 'report_export_download_package_gate_only' ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Blocked reasons" items={latestReportExportDownloadPackageGate.blocked_reasons || []} />
                                  <SummaryList title="Required revisions" items={latestReportExportDownloadPackageGate.required_revisions || []} />
                                  <SummaryList title="Warnings" items={latestReportExportDownloadPackageGate.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestReportExportDownloadPackageGate.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit refs"
                                    items={Object.entries(latestReportExportDownloadPackageGate.audit_refs || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No Report Export Download / Package Gate yet.</Text>
                            )}
                            {reportExportDownloadPackageGateAudits.length ? (
                              <Card size="small" title={`Download/package gate audit timeline (${reportExportDownloadPackageGateAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {reportExportDownloadPackageGateAudits.map((audit) => (
                                    <Space wrap key={audit.download_package_gate_audit_id}>
                                      <Tag color={REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[audit.delivery_decision] || 'blue'}>
                                        {audit.delivery_decision}
                                      </Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">download={boolText(audit.now_flags?.download_route_now)}</Text>
                                      <Text type="secondary">zip={boolText(audit.now_flags?.zip_package_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.public_url_now)}</Text>
                                      <Text type="secondary">signed={boolText(audit.now_flags?.signed_url_now)}</Text>
                                      <Text type="secondary">rows={boolText(audit.now_flags?.read_original_rows_now)}</Text>
                                      <Text type="secondary">file_content={boolText(audit.now_flags?.read_runtime_file_content_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Report Export Download / Package Runtime">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Local manifest-only runtime: no download route, no file bytes, no ZIP, no public or signed URL"
                              description="This creates only safe local manifest metadata under ignored runtime storage. It does not expose runtime files, read or parse report artifact file content, copy export content into a bundle, generate B-end report, Sandbox, public event, Evidence Layer write, production case, real API, real LLM, URL fetch, or scraping."
                            />
                            {reportExportDownloadPackageArtifactError ? (
                              <Alert type="error" showIcon message={reportExportDownloadPackageArtifactError} />
                            ) : null}
                            <Form
                              form={reportExportDownloadPackageArtifactForm}
                              layout="vertical"
                              initialValues={{
                                package_mode: 'local_manifest_only',
                                operator_label: 'download_package_artifact_reviewer',
                                note: 'Create local manifest-only package metadata. Do not create download routes, file bytes, ZIP, public URLs, signed URLs, or external delivery.',
                                acknowledge_local_manifest_only: true,
                                acknowledge_no_download_route: true,
                                acknowledge_no_file_bytes: true,
                                acknowledge_no_zip: true,
                                acknowledge_no_public_or_signed_url: true,
                                acknowledge_no_runtime_file_exposure: true,
                                acknowledge_no_artifact_content_read: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_weak_evidence_warning: true,
                                acknowledge_rejected_exclusion: true,
                                acknowledge_dedup_no_risk_amplification: true,
                                acknowledge_audit_trace_required: true,
                              }}
                              onFinish={handleCreateReportExportDownloadPackageArtifact}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item name="download_package_gate_id" label="Download / Package Gate ID">
                                    <Select
                                      allowClear
                                      placeholder={latestReportExportDownloadPackageGate?.download_package_gate_id || 'latest ready gate'}
                                      options={reportExportDownloadPackageGates
                                        .filter((item) => item.status === 'ready_for_future_download_package_runtime')
                                        .map((item) => ({
                                          value: item.download_package_gate_id,
                                          label: `${item.download_package_gate_id} / ${item.status}`,
                                        }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="review_case_id" label="Review-only Case ID">
                                    <Input placeholder={latestReportExportDownloadPackageGate?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="package_mode" label="Package mode">
                                    <Select
                                      disabled
                                      options={[{ value: 'local_manifest_only', label: 'local_manifest_only / safe metadata only' }]}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="operator_label" label="Operator label" rules={[{ required: true }]}>
                                    <Input />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="note" label="Runtime note" rules={[{ required: true }]}>
                                    <TextArea rows={2} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={8}>
                                {[
                                  ['acknowledge_local_manifest_only', 'local manifest only'],
                                  ['acknowledge_no_download_route', 'no download route'],
                                  ['acknowledge_no_file_bytes', 'no file bytes'],
                                  ['acknowledge_no_zip', 'no ZIP or binary archive'],
                                  ['acknowledge_no_public_or_signed_url', 'no public or signed URL'],
                                  ['acknowledge_no_runtime_file_exposure', 'no runtime file exposure'],
                                  ['acknowledge_no_artifact_content_read', 'do not read artifact content'],
                                  ['acknowledge_no_b_end_report', 'not B-end report'],
                                  ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                  ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'no production case'],
                                  ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                  ['acknowledge_not_official_verification', 'not official verification'],
                                  ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                  ['acknowledge_weak_evidence_warning', 'preserve weak evidence warning'],
                                  ['acknowledge_rejected_exclusion', 'rejected evidence remains excluded'],
                                  ['acknowledge_dedup_no_risk_amplification', 'dedup no risk amplification'],
                                  ['acknowledge_audit_trace_required', 'audit trace required'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={reportExportDownloadPackageArtifactLoading}
                                  disabled={!reportExportDownloadPackageArtifactReady || reportExportDownloadPackageArtifactLoading}
                                >
                                  Create local manifest package artifact
                                </Button>
                                {latestReportExportDownloadPackageArtifact ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(latestReportExportDownloadPackageArtifactJson, 'Package artifact JSON copied')}
                                  >
                                    Copy latest package artifact JSON
                                  </Button>
                                ) : null}
                                {reportExportDownloadPackageArtifacts.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportExportDownloadPackageArtifactsJson, 'Package artifact history JSON copied')}
                                  >
                                    Copy package artifact history JSON
                                  </Button>
                                ) : null}
                                {reportExportDownloadPackageArtifactAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() => copyText(reportExportDownloadPackageArtifactAuditsJson, 'Package artifact audit JSON copied')}
                                  >
                                    Copy package artifact audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestReportExportDownloadPackageArtifact ? (
                              <Card size="small" title="Latest local manifest package artifact">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag color={REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[latestReportExportDownloadPackageArtifact.package_status] || 'default'}>
                                      {latestReportExportDownloadPackageArtifact.package_status}
                                    </Tag>
                                    <Tag color="blue">{latestReportExportDownloadPackageArtifact.package_mode}</Tag>
                                    <Text type="secondary">{latestReportExportDownloadPackageArtifact.package_artifact_id}</Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="manifest_runtime_ref (text only, not a download link)">
                                      <Text code>{latestReportExportDownloadPackageArtifact.manifest_runtime_ref || '-'}</Text>
                                    </Descriptions.Item>
                                    <Descriptions.Item label="manifest summary">
                                      {Object.entries(latestReportExportDownloadPackageArtifact.manifest_summary || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="file inventory summary">
                                      {Object.entries(latestReportExportDownloadPackageArtifact.file_inventory_summary || {})
                                        .map(([key, value]) => `${key}=${Array.isArray(value) ? value.join('|') : String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="source export artifacts">
                                      {(latestReportExportDownloadPackageArtifact.source_export_artifact_refs || [])
                                        .map((item) =>
                                          [item.export_artifact_id, item.artifact_type, item.artifact_format, item.status].filter(Boolean).join(' / '),
                                        )
                                        .join('; ') || '-'}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestReportExportDownloadPackageArtifact.boundary_block || {}).map(([key, value]) => (
                                      <Tag
                                        color={value && key !== 'generates_local_manifest_package_now' ? 'red' : 'default'}
                                        key={key}
                                      >
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Unsupported modes" items={latestReportExportDownloadPackageArtifact.unsupported_modes || []} />
                                  <SummaryList title="Warnings" items={latestReportExportDownloadPackageArtifact.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestReportExportDownloadPackageArtifact.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit trace"
                                    items={Object.entries(latestReportExportDownloadPackageArtifact.audit_trace || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No local manifest-only package artifact yet.</Text>
                            )}
                            {reportExportDownloadPackageArtifactAudits.length ? (
                              <Card size="small" title={`Package artifact audit timeline (${reportExportDownloadPackageArtifactAudits.length})`}>
                                <Space direction="vertical" size={8} className="full-width">
                                  {reportExportDownloadPackageArtifactAudits.map((audit) => (
                                    <Space wrap key={audit.package_artifact_audit_id}>
                                      <Tag color={REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[audit.new_status] || 'blue'}>
                                        {audit.new_status}
                                      </Tag>
                                      <Text type="secondary">{audit.created_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">download={boolText(audit.now_flags?.download_route_now)}</Text>
                                      <Text type="secondary">file_bytes={boolText(audit.now_flags?.return_file_bytes_now)}</Text>
                                      <Text type="secondary">zip={boolText(audit.now_flags?.zip_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.public_url_now)}</Text>
                                      <Text type="secondary">signed={boolText(audit.now_flags?.signed_url_now)}</Text>
                                      <Text type="secondary">artifact_content={boolText(audit.now_flags?.read_artifact_file_content_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title="Report Export Public Access / External Delivery Gate">
                          <Space direction="vertical" size={12} className="full-width">
                            <Alert
                              type="warning"
                              showIcon
                              message="Gate only: no public access and no external delivery"
                              description="This records local governance approval status only. It does not create a public download route, file-byte response, ZIP, public URL, signed URL, email, object storage upload, portal publication, B-end report, Sandbox fixture, public event page, Evidence Layer write, production case, real API call, real LLM call, URL fetch, or scraping."
                            />
                            {reportExportPublicAccessExternalDeliveryGateError ? (
                              <Alert type="error" showIcon message={reportExportPublicAccessExternalDeliveryGateError} />
                            ) : null}
                            <Form
                              form={reportExportPublicAccessExternalDeliveryGateForm}
                              layout="vertical"
                              initialValues={{
                                access_delivery_decision: 'approve_for_future_public_access_external_delivery_runtime',
                                requested_future_access_modes: ['internal_handoff_future_candidate'],
                                requested_future_delivery_modes: ['internal_handoff_future_candidate'],
                                reviewer_label: 'public_access_delivery_reviewer',
                                note: 'Create public access / external delivery gate record only. Do not create routes, file bytes, ZIP, public URLs, signed URLs, email, object storage, portal publication, or external delivery.',
                                acknowledge_gate_only: true,
                                acknowledge_no_public_download_route: true,
                                acknowledge_no_file_byte_response: true,
                                acknowledge_no_zip: true,
                                acknowledge_no_public_or_signed_url: true,
                                acknowledge_no_external_delivery: true,
                                acknowledge_no_email: true,
                                acknowledge_no_object_storage: true,
                                acknowledge_no_portal_publication: true,
                                acknowledge_no_runtime_file_exposure: true,
                                acknowledge_no_manifest_content_exposure: true,
                                acknowledge_no_export_artifact_content_read: true,
                                acknowledge_no_b_end_report: true,
                                acknowledge_no_sandbox_or_public_event: true,
                                acknowledge_no_evidence_layer_write: true,
                                acknowledge_no_production_case: true,
                                acknowledge_provider_output_is_evidence_not_truth: true,
                                acknowledge_not_official_verification: true,
                                acknowledge_not_full_web_coverage: true,
                                acknowledge_downstream_gates_required: true,
                              }}
                              onFinish={handleCreateReportExportPublicAccessExternalDeliveryGate}
                            >
                              <Row gutter={12}>
                                <Col xs={24} md={12}>
                                  <Form.Item name="package_artifact_id" label="Package Artifact ID">
                                    <Select
                                      allowClear
                                      placeholder={latestReportExportDownloadPackageArtifact?.package_artifact_id || 'latest local manifest package'}
                                      options={reportExportDownloadPackageArtifacts
                                        .filter((item) => item.package_status === 'local_manifest_ready')
                                        .map((item) => ({
                                          value: item.package_artifact_id,
                                          label: `${item.package_artifact_id} / ${item.package_status}`,
                                        }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="download_package_gate_id" label="Download / Package Gate ID">
                                    <Select
                                      allowClear
                                      placeholder={latestReportExportDownloadPackageArtifact?.download_package_gate_id || 'latest upstream gate'}
                                      options={reportExportDownloadPackageGates
                                        .filter((item) => item.status === 'ready_for_future_download_package_runtime')
                                        .map((item) => ({
                                          value: item.download_package_gate_id,
                                          label: `${item.download_package_gate_id} / ${item.status}`,
                                        }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="final_summary_report_id" label="Final Summary Report ID">
                                    <Select
                                      allowClear
                                      placeholder={latestReportExportDownloadPackageArtifact?.final_summary_report_id || 'latest final summary report'}
                                      options={finalSummaryReports.map((item) => ({
                                        value: item.final_summary_report_id,
                                        label: `${item.final_summary_report_id} / ${item.status}`,
                                      }))}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="review_case_id" label="Review-only Case ID">
                                    <Input placeholder={latestReportExportDownloadPackageArtifact?.review_case_id || 'latest review case'} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="access_delivery_decision" label="Access / delivery decision" rules={[{ required: true }]}>
                                    <Select options={REPORT_EXPORT_PUBLIC_ACCESS_EXTERNAL_DELIVERY_DECISION_OPTIONS} />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="requested_future_access_modes" label="Future access labels">
                                    <Select
                                      mode="multiple"
                                      options={[
                                        { value: 'public_download_route_future_candidate', label: 'public_download_route_future_candidate' },
                                        { value: 'file_byte_response_future_candidate', label: 'file_byte_response_future_candidate' },
                                        { value: 'signed_url_future_candidate', label: 'signed_url_future_candidate' },
                                        { value: 'public_url_future_candidate', label: 'public_url_future_candidate' },
                                        { value: 'restricted_portal_access_future_candidate', label: 'restricted_portal_access_future_candidate' },
                                        { value: 'object_storage_publication_future_candidate', label: 'object_storage_publication_future_candidate' },
                                        { value: 'external_delivery_future_candidate', label: 'external_delivery_future_candidate' },
                                        { value: 'internal_handoff_future_candidate', label: 'internal_handoff_future_candidate' },
                                      ]}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="requested_future_delivery_modes" label="Future delivery labels">
                                    <Select
                                      mode="multiple"
                                      options={[
                                        { value: 'internal_handoff_future_candidate', label: 'internal_handoff_future_candidate' },
                                        { value: 'external_delivery_future_candidate', label: 'external_delivery_future_candidate' },
                                        { value: 'restricted_portal_access_future_candidate', label: 'restricted_portal_access_future_candidate' },
                                        { value: 'object_storage_publication_future_candidate', label: 'object_storage_publication_future_candidate' },
                                        { value: 'public_download_route_future_candidate', label: 'public_download_route_future_candidate' },
                                        { value: 'file_byte_response_future_candidate', label: 'file_byte_response_future_candidate' },
                                        { value: 'signed_url_future_candidate', label: 'signed_url_future_candidate' },
                                        { value: 'public_url_future_candidate', label: 'public_url_future_candidate' },
                                      ]}
                                    />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="reviewer_label" label="Reviewer label" rules={[{ required: true }]}>
                                    <Input />
                                  </Form.Item>
                                </Col>
                                <Col xs={24} md={12}>
                                  <Form.Item name="required_revisions" label="Required revisions">
                                    <Input placeholder="required when decision=request_revision" />
                                  </Form.Item>
                                </Col>
                                <Col xs={24}>
                                  <Form.Item name="note" label="Gate note" rules={[{ required: true }]}>
                                    <TextArea rows={2} />
                                  </Form.Item>
                                </Col>
                              </Row>
                              <Row gutter={8}>
                                {[
                                  ['acknowledge_gate_only', 'gate record only'],
                                  ['acknowledge_no_public_download_route', 'no public download route'],
                                  ['acknowledge_no_file_byte_response', 'no file-byte response'],
                                  ['acknowledge_no_zip', 'no ZIP or binary archive'],
                                  ['acknowledge_no_public_or_signed_url', 'no public or signed URL'],
                                  ['acknowledge_no_external_delivery', 'no external delivery'],
                                  ['acknowledge_no_email', 'no email'],
                                  ['acknowledge_no_object_storage', 'no object storage upload'],
                                  ['acknowledge_no_portal_publication', 'no portal publication'],
                                  ['acknowledge_no_runtime_file_exposure', 'no runtime file exposure'],
                                  ['acknowledge_no_manifest_content_exposure', 'no manifest content exposure'],
                                  ['acknowledge_no_export_artifact_content_read', 'do not read export artifact content'],
                                  ['acknowledge_no_b_end_report', 'not B-end report'],
                                  ['acknowledge_no_sandbox_or_public_event', 'no Sandbox/public event'],
                                  ['acknowledge_no_evidence_layer_write', 'no Evidence Layer write'],
                                  ['acknowledge_no_production_case', 'no production case'],
                                  ['acknowledge_provider_output_is_evidence_not_truth', 'provider output is evidence, not truth'],
                                  ['acknowledge_not_official_verification', 'not official verification'],
                                  ['acknowledge_not_full_web_coverage', 'not full-web coverage'],
                                  ['acknowledge_downstream_gates_required', 'downstream gates required'],
                                ].map(([name, label]) => (
                                  <Col xs={24} md={12} key={name}>
                                    <Form.Item name={name} valuePropName="checked">
                                      <Checkbox>{label}</Checkbox>
                                    </Form.Item>
                                  </Col>
                                ))}
                              </Row>
                              <Space wrap>
                                <Button
                                  type="primary"
                                  htmlType="submit"
                                  icon={<ShieldCheck size={16} />}
                                  loading={reportExportPublicAccessExternalDeliveryGateLoading}
                                  disabled={!reportExportPublicAccessExternalDeliveryGateReady || reportExportPublicAccessExternalDeliveryGateLoading}
                                >
                                  Create Public Access / External Delivery Gate
                                </Button>
                                {latestReportExportPublicAccessExternalDeliveryGate ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() =>
                                      copyText(
                                        latestReportExportPublicAccessExternalDeliveryGateJson,
                                        'Public access / external delivery gate JSON copied',
                                      )
                                    }
                                  >
                                    Copy latest public access gate JSON
                                  </Button>
                                ) : null}
                                {reportExportPublicAccessExternalDeliveryGates.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() =>
                                      copyText(
                                        reportExportPublicAccessExternalDeliveryGatesJson,
                                        'Public access / external delivery gate history JSON copied',
                                      )
                                    }
                                  >
                                    Copy public access gate history JSON
                                  </Button>
                                ) : null}
                                {reportExportPublicAccessExternalDeliveryGateAudits.length ? (
                                  <Button
                                    icon={<FileJson size={16} />}
                                    onClick={() =>
                                      copyText(
                                        reportExportPublicAccessExternalDeliveryGateAuditsJson,
                                        'Public access / external delivery gate audit JSON copied',
                                      )
                                    }
                                  >
                                    Copy public access gate audit JSON
                                  </Button>
                                ) : null}
                              </Space>
                            </Form>
                            {latestReportExportPublicAccessExternalDeliveryGate ? (
                              <Card size="small" title="Latest Public Access / External Delivery Gate">
                                <Space direction="vertical" size={8} className="full-width">
                                  <Space wrap>
                                    <Tag
                                      color={
                                        REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[
                                          latestReportExportPublicAccessExternalDeliveryGate.gate_status
                                        ] || 'default'
                                      }
                                    >
                                      {latestReportExportPublicAccessExternalDeliveryGate.gate_status}
                                    </Tag>
                                    <Tag color="blue">{latestReportExportPublicAccessExternalDeliveryGate.access_delivery_decision}</Tag>
                                    <Text type="secondary">
                                      {latestReportExportPublicAccessExternalDeliveryGate.public_access_delivery_gate_id}
                                    </Text>
                                  </Space>
                                  <Descriptions size="small" column={1}>
                                    <Descriptions.Item label="package_artifact_id">
                                      {latestReportExportPublicAccessExternalDeliveryGate.package_artifact_id || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="upstream package status">
                                      {latestReportExportPublicAccessExternalDeliveryGate.upstream_package_artifact_status || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="future access labels">
                                      {(latestReportExportPublicAccessExternalDeliveryGate.requested_future_access_modes || []).join(', ') || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="future delivery labels">
                                      {(latestReportExportPublicAccessExternalDeliveryGate.requested_future_delivery_modes || []).join(', ') || '-'}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="eligibility summary">
                                      {Object.entries(latestReportExportPublicAccessExternalDeliveryGate.eligibility_summary || {})
                                        .map(([key, value]) => `${key}=${String(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                    <Descriptions.Item label="downstream gates">
                                      {Object.entries(latestReportExportPublicAccessExternalDeliveryGate.downstream_gate_policy || {})
                                        .map(([key, value]) => `${key}=${boolText(value)}`)
                                        .join(', ')}
                                    </Descriptions.Item>
                                  </Descriptions>
                                  <Space wrap>
                                    {Object.entries(latestReportExportPublicAccessExternalDeliveryGate.boundary_block || {}).map(([key, value]) => (
                                      <Tag color={value ? 'red' : 'default'} key={key}>
                                        {key}={boolText(value)}
                                      </Tag>
                                    ))}
                                  </Space>
                                  <SummaryList title="Blockers" items={latestReportExportPublicAccessExternalDeliveryGate.blockers || []} />
                                  <SummaryList title="Required revisions" items={latestReportExportPublicAccessExternalDeliveryGate.required_revisions || []} />
                                  <SummaryList title="Warnings" items={latestReportExportPublicAccessExternalDeliveryGate.warnings || []} />
                                  <SummaryList title="Boundary notes" items={latestReportExportPublicAccessExternalDeliveryGate.boundary_notes || []} />
                                  <SummaryList
                                    title="Audit trace"
                                    items={Object.entries(latestReportExportPublicAccessExternalDeliveryGate.audit_trace || {}).map(
                                      ([key, value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : String(value)}`,
                                    )}
                                  />
                                </Space>
                              </Card>
                            ) : (
                              <Text type="secondary">No public access / external delivery gate yet.</Text>
                            )}
                            {reportExportPublicAccessExternalDeliveryGateAudits.length ? (
                              <Card
                                size="small"
                                title={`Public access / external delivery gate audit timeline (${reportExportPublicAccessExternalDeliveryGateAudits.length})`}
                              >
                                <Space direction="vertical" size={8} className="full-width">
                                  {reportExportPublicAccessExternalDeliveryGateAudits.map((audit) => (
                                    <Space wrap key={audit.public_access_delivery_gate_audit_id}>
                                      <Tag color={REPORT_EXPORT_DOWNLOAD_PACKAGE_STATUS_COLOR[audit.new_status] || 'blue'}>
                                        {audit.new_status}
                                      </Tag>
                                      <Text type="secondary">{audit.decided_at || '-'}</Text>
                                      <Text type="secondary">effect={audit.analysis_effect}</Text>
                                      <Text type="secondary">download={boolText(audit.now_flags?.public_download_route_now)}</Text>
                                      <Text type="secondary">file_bytes={boolText(audit.now_flags?.file_byte_response_now)}</Text>
                                      <Text type="secondary">zip={boolText(audit.now_flags?.zip_now)}</Text>
                                      <Text type="secondary">public={boolText(audit.now_flags?.public_url_now)}</Text>
                                      <Text type="secondary">signed={boolText(audit.now_flags?.signed_url_now)}</Text>
                                      <Text type="secondary">delivery={boolText(audit.now_flags?.external_delivery_now)}</Text>
                                      <Text type="secondary">object_storage={boolText(audit.now_flags?.object_storage_upload_now)}</Text>
                                      <Text type="secondary">artifact_content={boolText(audit.now_flags?.read_export_artifact_file_content_now)}</Text>
                                    </Space>
                                  ))}
                                </Space>
                              </Card>
                            ) : null}
                          </Space>
                        </Card>

                        <Card size="small" title={`Existing review queue initializations (${reviewQueueInitializations.length})`}>
                          {reviewQueueInitializations.length ? (
                            <Space direction="vertical" size={8} className="full-width">
                              {reviewQueueInitializations.map((item) => (
                                <Card size="small" key={item.queue_init_id}>
                                  <Space direction="vertical" size={4} className="full-width">
                                    <Space wrap>
                                      <Tag color={item.status === 'completed' ? 'green' : 'gold'}>{item.status}</Tag>
                                      <Text type="secondary">{item.queue_init_id}</Text>
                                    </Space>
                                    <Text>package: {item.package_name || '-'}</Text>
                                    <Text type="secondary">
                                      queue_items_created={item.counts?.queue_items_created || 0}, analysis_included=
                                      {boolText(item.defaults?.analysis_included)}, production_review_queue_created=
                                      {boolText(item.target?.production_review_queue_created)}
                                    </Text>
                                  </Space>
                                </Card>
                              ))}
                            </Space>
                          ) : (
                            <Text type="secondary">No review queue initializations yet.</Text>
                          )}
                        </Card>
                      </Space>
                    </Card>

                    <Card size="small" title={`Existing review-only case containers (${reviewOnlyCases.length})`}>
                      {reviewOnlyCases.length ? (
                        <Space direction="vertical" size={8} className="full-width">
                          {reviewOnlyCases.map((reviewCase) => (
                            <Card size="small" key={reviewCase.review_case_id}>
                              <Space direction="vertical" size={4} className="full-width">
                                <Space wrap>
                                  <Tag color="gold">{reviewCase.status}</Tag>
                                  <Tag color="blue">{reviewCase.visibility}</Tag>
                                  <Text type="secondary">{reviewCase.review_case_id}</Text>
                                </Space>
                                <Text>package: {reviewCase.package_reference?.package_name || '-'}</Text>
                                <Text type="secondary">
                                  analysis_included={boolText(reviewCase.analysis_included)}, production_case_created={boolText(reviewCase.production_case_created)}, evidence_rows_imported={boolText(reviewCase.evidence_rows_imported)}
                                </Text>
                              </Space>
                            </Card>
                          ))}
                        </Space>
                      ) : (
                        <Text type="secondary">No review-only case containers yet.</Text>
                      )}
                    </Card>
                  </Space>
                </Card>

                <Alert
                  type="info"
                  showIcon
                  message="Coverage / trust note"
                  description="Provider 输出仍是 evidence，不是 official truth。进入正式 case 前仍需 validation、trust/provenance、review、dedup、coverage 和 audit。"
                />
                <Space wrap>
                  <Button icon={<ClipboardCopy size={16} />} onClick={() => copyText(requestJson, 'Request JSON 已复制')}>
                    复制 request JSON
                  </Button>
                  <Button icon={<XCircle size={16} />} loading={canceling} onClick={handleCancel}>
                    本地取消请求
                  </Button>
                  <Button icon={<RefreshCw size={16} />} onClick={() => handleOpen(selectedRecord)}>
                    刷新详情
                  </Button>
                </Space>
                <Card size="small" title={<Space><FileJson size={16} />Request JSON preview</Space>}>
                  <pre className="code-preview">{requestJson}</pre>
                </Card>
              </Space>
            ) : (
              <Empty description="创建或选择一个本地分析请求" />
            )}
          </Card>
        </Col>
      </Row>

      <Card className="panel-card" title={<Space><ShieldCheck size={17} />Intentional non-goals</Space>}>
        <Space wrap>
          <Tag>no evidence row parsing</Tag>
          <Tag>no evidence row import</Tag>
          <Tag>no production case creation</Tag>
          <Tag>no analysis generation</Tag>
          <Tag>no Sandbox fixture generation</Tag>
          <Tag>no public event page generation</Tag>
          <Tag>no report generation</Tag>
          <Tag>no provider execution</Tag>
          <Tag>no collector jobs</Tag>
          <Tag>no subprocess provider execution</Tag>
          <Tag>no live collection</Tag>
          <Tag>no URL fetching</Tag>
          <Tag>no scraping</Tag>
          <Tag>no real API calls</Tag>
          <Tag>no real LLM</Tag>
        </Space>
      </Card>
    </div>
  )
}
