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
  listAnalysisRequestDedupGroupReviewAudits,
  listAnalysisRequestDedupPreviews,
  listAnalysisRequestImportJobs,
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
    } catch {
      setReviewQueueInitializations([])
      setReviewQueueItemBatch(null)
      setReviewQueueActionAudits([])
      setReviewQueueCompletionGates([])
      setDedupPreviews([])
      setDedupGroupReviewAudits([])
      setAnalysisReadyPromotionGates([])
      setPromotionDecisionAudits([])
      setReviewQueueInitError('')
      setReviewQueueActionError('')
      setReviewQueueCompletionGateError('')
      setDedupPreviewError('')
      setDedupGroupReviewError('')
      setAnalysisReadyPromotionGateError('')
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
      message.success(`Recorded promotion gate: ${gate?.status || 'created'}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create analysis-ready promotion gate.'
      setAnalysisReadyPromotionGateError(String(messageText))
    } finally {
      setAnalysisReadyPromotionGateLoading(false)
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
