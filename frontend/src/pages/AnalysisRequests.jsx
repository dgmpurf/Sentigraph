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
  createAnalysisRequest,
  createAnalysisRequestCaseDraft,
  createAnalysisRequestImportJob,
  createAnalysisRequestImportPlan,
  createAnalysisRequestImportPreview,
  createAnalysisRequestReviewDecision,
  getAnalysisRequest,
  getAnalysisRequestCaseDraft,
  getAnalysisRequestConfig,
  getAnalysisRequestImportPlan,
  getAnalysisRequestImportPreview,
  listAnalysisRequestImportJobs,
  listAnalysisRequestReviewDecisions,
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
  const [config, setConfig] = useState(null)
  const [requests, setRequests] = useState([])
  const [selectedRequestId, setSelectedRequestId] = useState('')
  const [detail, setDetail] = useState(null)
  const [caseDraft, setCaseDraft] = useState(null)
  const [importPlan, setImportPlan] = useState(null)
  const [importPreview, setImportPreview] = useState(null)
  const [reviewDecisions, setReviewDecisions] = useState([])
  const [importJobs, setImportJobs] = useState([])
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [canceling, setCanceling] = useState(false)
  const [draftLoading, setDraftLoading] = useState(false)
  const [planLoading, setPlanLoading] = useState(false)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [reviewLoading, setReviewLoading] = useState(false)
  const [importJobLoading, setImportJobLoading] = useState(false)
  const [error, setError] = useState('')
  const [draftError, setDraftError] = useState('')
  const [planError, setPlanError] = useState('')
  const [previewError, setPreviewError] = useState('')
  const [reviewError, setReviewError] = useState('')
  const [importJobError, setImportJobError] = useState('')

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
      setImportJobs([])
      setDraftError('')
      setPlanError('')
      setPreviewError('')
      setReviewError('')
      setImportJobError('')
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
      message.success(`Created dry-run import job draft: ${job.job_id}`)
    } catch (requestError) {
      const messageText = requestError?.response?.data?.detail || requestError?.message || 'Unable to create manual import job draft.'
      setImportJobError(String(messageText))
    } finally {
      setImportJobLoading(false)
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
