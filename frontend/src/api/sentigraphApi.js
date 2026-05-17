import { apiClient } from './client.js'

const API_PREFIX = '/api/v1'
const DEFAULT_REPORT_LANGUAGE = 'zh-CN'

export async function expandKeywords(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/keywords/expand`, payload)
  return data
}

export async function getPlatforms() {
  const { data } = await apiClient.get(`${API_PREFIX}/platforms`)
  return data
}

export async function getPlatformStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/platforms/status`)
  return data
}

export async function getPublicParserStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/public-parsers/status`)
  return normalizePublicParserStatus(data)
}

export async function previewPublicParser(platform, limit = 3, use_live_fetch = false) {
  const { data } = await apiClient.post(`${API_PREFIX}/public-parsers/preview`, {
    platform,
    limit,
    use_live_fetch,
  })
  return normalizePublicParserPreview(data)
}

export async function suggestSelectorRepair(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/public-parsers/selector-repair/suggest`, {
    platform_id: payload.platform_id || payload.platform || '',
    html: payload.html || '',
    profile: payload.profile && typeof payload.profile === 'object' ? payload.profile : {},
    extraction_targets: Array.isArray(payload.extraction_targets) ? payload.extraction_targets : [],
    error_summary: payload.error_summary || '',
  })
  return normalizeSelectorRepairSuggestion(data)
}

export async function previewSelectorRepair(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/public-parsers/selector-repair/preview`, {
    platform_id: payload.platform_id || payload.platform || '',
    suggestion: payload.suggestion,
    fixture_html: payload.fixture_html || payload.html || '',
  })
  return normalizeSelectorRepairPreview(data)
}

export async function listAnalysisCases() {
  const { data } = await apiClient.get(`${API_PREFIX}/cases`)
  return Array.isArray(data) ? data : []
}

export async function createAnalysisCase(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases`, {
    report_language: DEFAULT_REPORT_LANGUAGE,
    ...payload,
  })
  return normalizeCaseDetail(data)
}

export async function getAnalysisCase(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}`)
  return normalizeCaseDetail(data)
}

export async function runAnalysisCase(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/run`)
  return normalizeCaseDetail(data)
}

export async function getCaseMarkdownReport(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/report/markdown`)
  return data
}

export async function listCaseSnapshots(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/snapshots`)
  return Array.isArray(data) ? data : []
}

export async function runCaseMonitoringCheck(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/monitor/run`)
  return normalizeMonitoringStatus(data)
}

export async function listCaseAlerts(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/alerts`)
  return Array.isArray(data) ? data : []
}

export async function listNotifications() {
  const { data } = await apiClient.get(`${API_PREFIX}/notifications`)
  return Array.isArray(data) ? data.map(normalizeNotification) : []
}

export async function listCaseNotifications(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/notifications`)
  return Array.isArray(data) ? data.map(normalizeNotification) : []
}

export async function markNotificationRead(notificationId) {
  const { data } = await apiClient.post(`${API_PREFIX}/notifications/${notificationId}/read`)
  return normalizeNotification(data)
}

export async function simulateSendNotification(notificationId) {
  const { data } = await apiClient.post(`${API_PREFIX}/notifications/${notificationId}/simulate-send`)
  return normalizeNotificationSendResult(data)
}

export async function simulateSendPendingNotifications() {
  const { data } = await apiClient.post(`${API_PREFIX}/notifications/simulate-send-pending`)
  return Array.isArray(data) ? data.map(normalizeNotificationSendResult) : []
}

export async function getNotificationOutboxStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/notifications/outbox/status`)
  return normalizeNotificationOutboxStatus(data)
}

export async function getCaseMonitoringConfig(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/monitoring/config`)
  return normalizeMonitoringConfig(data)
}

export async function updateCaseMonitoringConfig(caseId, payload) {
  const { data } = await apiClient.put(`${API_PREFIX}/cases/${caseId}/monitoring/config`, payload)
  return normalizeMonitoringConfig(data)
}

export async function enableCaseMonitoring(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/monitoring/enable`)
  return normalizeMonitoringConfig(data)
}

export async function disableCaseMonitoring(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/monitoring/disable`)
  return normalizeMonitoringConfig(data)
}

export async function getSchedulerStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/scheduler/status`)
  return normalizeSchedulerStatus(data)
}

export async function runDueMonitoringJobs() {
  const { data } = await apiClient.post(`${API_PREFIX}/scheduler/run-due`)
  return normalizeSchedulerRunDueResponse(data)
}

export async function listAllAlertEvents() {
  const { data } = await apiClient.get(`${API_PREFIX}/alerts`)
  return Array.isArray(data) ? data : []
}

export async function startCrawl(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/crawl/start`, payload)
  return data
}

export async function runAnalysis(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/analysis/run`, payload)
  return data
}

export async function getAnalysisResult(projectId) {
  const { data } = await apiClient.get(`${API_PREFIX}/analysis/${projectId}`)
  return normalizeRiskExtension(data)
}

export async function getVisualizationData(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/visualization/data`, payload)
  return normalizeRiskExtension(data)
}

export async function generateSummary(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/summary/generate`, {
    include_representative_comments: true,
    report_language: DEFAULT_REPORT_LANGUAGE,
    ...payload,
  })
  return normalizeRiskExtension(data)
}

export async function generateRecommendation(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/recommendation/generate`, {
    user_type: 'brand',
    tone: 'professional',
    report_language: DEFAULT_REPORT_LANGUAGE,
    ...payload,
  })
  return normalizeRiskExtension(data)
}

export async function getPropagation(projectId) {
  const { data } = await apiClient.get(`${API_PREFIX}/propagation/${projectId}`)
  return data
}

export async function getAlerts(projectId) {
  const { data } = await apiClient.get(`${API_PREFIX}/alerts/${projectId}`)
  return data
}

function normalizeRiskExtension(data) {
  if (!data || typeof data !== 'object') return data
  const topicRisks = Array.isArray(data.topic_risks) ? data.topic_risks : []
  const topRiskTopics =
    Array.isArray(data.top_risk_topics) && data.top_risk_topics.length > 0
      ? data.top_risk_topics
      : topicRisks.slice(0, 3)

  return {
    ...data,
    risk_model_version: data.risk_model_version || 'v1_static_mvp',
    overall_risk: normalizeOptionalScore(data.overall_risk),
    topic_risks: topicRisks,
    top_risk_topics: topRiskTopics,
    max_topic_risk: normalizeOptionalScore(data.max_topic_risk),
    average_topic_risk: normalizeOptionalScore(data.average_topic_risk),
    real_crisis_risk: normalizeOptionalScore(data.real_crisis_risk),
    manipulation_risk: normalizeOptionalScore(data.manipulation_risk),
    risk_explanation: typeof data.risk_explanation === 'string' ? data.risk_explanation : '',
  }
}

function normalizeCaseDetail(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    analysis_result: normalizeRiskExtension(data.analysis_result),
    visualization_data: normalizeRiskExtension(data.visualization_data),
    report: normalizeRiskExtension(data.report),
    monitoring_config: normalizeMonitoringConfig(data.monitoring_config),
  }
}

function normalizeMonitoringStatus(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    latest_snapshot: normalizeSnapshot(data.latest_snapshot),
    previous_snapshot: normalizeSnapshot(data.previous_snapshot),
    alerts: Array.isArray(data.alerts) ? data.alerts : [],
  }
}

function normalizeNotification(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    notification_id: String(data.notification_id || ''),
    alert_id: String(data.alert_id || ''),
    case_id: String(data.case_id || ''),
    level: data.level || 'info',
    title: String(data.title || '舆情通知'),
    message: String(data.message || ''),
    channel_type: data.channel_type || 'in_app',
    status: data.status || 'pending',
    created_at: data.created_at || null,
    read_at: data.read_at || null,
    simulated_sent_at: data.simulated_sent_at || null,
    metadata: data.metadata && typeof data.metadata === 'object' ? data.metadata : {},
  }
}

function normalizeNotificationSendResult(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    notification_id: String(data.notification_id || ''),
    channel_type: data.channel_type || 'in_app',
    status: data.status || 'pending',
    simulated: Boolean(data.simulated),
    simulated_sent_at: data.simulated_sent_at || data.notification?.simulated_sent_at || null,
    message: String(data.message || ''),
    notification: normalizeNotification(data.notification),
  }
}

function normalizeNotificationOutboxStatus(data) {
  if (!data || typeof data !== 'object') {
    return {
      total: 0,
      unread: 0,
      pending: 0,
      simulated_sent: 0,
      failed: 0,
      mock_only: true,
      channels: [],
      message: '通知出箱仅用于本地模拟。',
    }
  }
  return {
    ...data,
    total: Number(data.total || 0),
    unread: Number(data.unread || 0),
    pending: Number(data.pending || 0),
    simulated_sent: Number(data.simulated_sent || 0),
    failed: Number(data.failed || 0),
    mock_only: data.mock_only !== false,
    channels: Array.isArray(data.channels) ? data.channels : [],
    message: String(data.message || ''),
  }
}

function normalizeSnapshot(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    top_risk_topics: Array.isArray(data.top_risk_topics) ? data.top_risk_topics : [],
    risk_score: normalizeOptionalScore(data.risk_score) ?? 0,
    overall_risk: normalizeOptionalScore(data.overall_risk) ?? 0,
    real_crisis_risk: normalizeOptionalScore(data.real_crisis_risk) ?? 0,
    manipulation_risk: normalizeOptionalScore(data.manipulation_risk) ?? 0,
  }
}

function normalizeMonitoringConfig(data) {
  if (!data || typeof data !== 'object') {
    return {
      enabled: false,
      interval_minutes: 60,
      last_run_at: null,
      next_run_at: null,
      threshold_config: {},
      status: 'disabled',
    }
  }
  return {
    ...data,
    enabled: Boolean(data.enabled),
    interval_minutes: Number.isFinite(Number(data.interval_minutes)) ? Number(data.interval_minutes) : 60,
    last_run_at: data.last_run_at || null,
    next_run_at: data.next_run_at || null,
    threshold_config: data.threshold_config && typeof data.threshold_config === 'object' ? data.threshold_config : {},
    status: data.status || (data.enabled ? 'scheduled' : 'disabled'),
  }
}

function normalizeSchedulerStatus(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    job_states: Array.isArray(data.job_states) ? data.job_states.map(normalizeMonitoringJobState) : [],
    total_cases: Number(data.total_cases || 0),
    enabled_cases: Number(data.enabled_cases || 0),
    due_cases: Number(data.due_cases || 0),
  }
}

function normalizeSchedulerRunDueResponse(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    monitoring_results: Array.isArray(data.monitoring_results)
      ? data.monitoring_results.map(normalizeMonitoringStatus)
      : [],
    job_states: Array.isArray(data.job_states) ? data.job_states.map(normalizeMonitoringJobState) : [],
    due_case_count: Number(data.due_case_count || 0),
    executed_case_count: Number(data.executed_case_count || 0),
    skipped_case_count: Number(data.skipped_case_count || 0),
  }
}

function normalizeMonitoringJobState(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    enabled: Boolean(data.enabled),
    interval_minutes: Number.isFinite(Number(data.interval_minutes)) ? Number(data.interval_minutes) : 60,
    is_due: Boolean(data.is_due),
    snapshot_count: Number(data.snapshot_count || 0),
    alert_count: Number(data.alert_count || 0),
  }
}

function normalizePublicParserStatus(data) {
  if (!data || typeof data !== 'object') {
    return {
      parsers: [],
      total: 0,
      live_fetch_enabled_default: false,
    }
  }
  return {
    ...data,
    parsers: Array.isArray(data.parsers) ? data.parsers.map(normalizePublicParserStatusItem).filter(Boolean) : [],
    total: Number(data.total || 0),
    live_fetch_enabled_default: Boolean(data.live_fetch_enabled_default),
  }
}

function normalizePublicParserStatusItem(data) {
  if (!data || typeof data !== 'object') return null
  return {
    platform_id: String(data.platform_id || ''),
    display_name: String(data.display_name || data.platform_id || ''),
    source_type: String(data.source_type || 'public_page_parser'),
    parser_status: String(data.parser_status || 'unknown'),
    live_fetch_enabled: Boolean(data.live_fetch_enabled),
    fixture_available: Boolean(data.fixture_available),
    profile_available: Boolean(data.profile_available),
    comments_supported: Boolean(data.comments_supported),
    last_test_status: data.last_test_status ? String(data.last_test_status) : null,
    notes: String(data.notes || ''),
    safe_limit: Number.isFinite(Number(data.safe_limit)) ? Number(data.safe_limit) : 3,
    rate_limit_seconds: Number.isFinite(Number(data.rate_limit_seconds)) ? Number(data.rate_limit_seconds) : 3,
  }
}

function normalizePublicParserPreview(data) {
  if (!data || typeof data !== 'object') {
    return {
      platform: '',
      source_type: 'public_page_parser',
      parser_status: 'unknown',
      live_fetch_enabled: false,
      live_fetch_attempted: false,
      fallback_used: true,
      fallback_reason_category: null,
      post_count: 0,
      comment_count: 0,
      raw_post_schema_valid: false,
      raw_comment_schema_valid: false,
      sample_posts: [],
      sample_comments: [],
      warnings: ['empty_preview_response'],
    }
  }
  return {
    ...data,
    platform: String(data.platform || ''),
    source_type: String(data.source_type || 'public_page_parser'),
    parser_status: String(data.parser_status || 'unknown'),
    live_fetch_enabled: Boolean(data.live_fetch_enabled),
    live_fetch_attempted: Boolean(data.live_fetch_attempted),
    fallback_used: Boolean(data.fallback_used),
    fallback_reason_category: data.fallback_reason_category ? String(data.fallback_reason_category) : null,
    post_count: Number(data.post_count || 0),
    comment_count: Number(data.comment_count || 0),
    raw_post_schema_valid: data.raw_post_schema_valid !== false,
    raw_comment_schema_valid: data.raw_comment_schema_valid !== false,
    sample_posts: Array.isArray(data.sample_posts) ? data.sample_posts.map(normalizeRawPostPreview).filter(Boolean) : [],
    sample_comments: Array.isArray(data.sample_comments)
      ? data.sample_comments.map(normalizeRawCommentPreview).filter(Boolean)
      : [],
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizeRawPostPreview(data) {
  if (!data || typeof data !== 'object') return null
  return {
    platform: String(data.platform || ''),
    post_id: String(data.post_id || ''),
    author_id: String(data.author_id || ''),
    author_name: String(data.author_name || data.author_id || ''),
    title: String(data.title || 'Untitled public post'),
    content: String(data.content || ''),
    like_count: Number(data.like_count || 0),
    reply_count: Number(data.reply_count || 0),
    share_count: Number(data.share_count || 0),
    created_at: data.created_at || null,
    url: data.url || '',
  }
}

function normalizeRawCommentPreview(data) {
  if (!data || typeof data !== 'object') return null
  return {
    platform: String(data.platform || ''),
    post_id: String(data.post_id || ''),
    comment_id: String(data.comment_id || ''),
    parent_id: data.parent_id ? String(data.parent_id) : null,
    author_id: String(data.author_id || ''),
    author_name: String(data.author_name || data.author_id || ''),
    content: String(data.content || ''),
    like_count: Number(data.like_count || 0),
    reply_count: Number(data.reply_count || 0),
    share_count: Number(data.share_count || 0),
    created_at: data.created_at || null,
    url: data.url || '',
  }
}

function normalizeSelectorRepairSuggestion(data) {
  if (!data || typeof data !== 'object') {
    return {
      platform_id: '',
      status: 'error',
      candidates: [],
      warnings: ['empty_selector_repair_response'],
      provider: 'mock',
      generated_by_mock: true,
      applied: false,
      review_required: true,
      draft_id: null,
    }
  }
  return {
    ...data,
    platform_id: String(data.platform_id || ''),
    status: String(data.status || 'error'),
    candidates: Array.isArray(data.candidates)
      ? data.candidates.map(normalizeSelectorCandidate).filter(Boolean)
      : [],
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
    provider: String(data.provider || 'mock'),
    generated_by_mock: data.generated_by_mock !== false,
    applied: Boolean(data.applied),
    review_required: data.review_required !== false,
    draft_id: data.draft_id ? String(data.draft_id) : null,
  }
}

function normalizeSelectorCandidate(data) {
  if (!data || typeof data !== 'object') return null
  return {
    target: String(data.target || ''),
    selector: String(data.selector || ''),
    selector_type: String(data.selector_type || 'css'),
    confidence: Number.isFinite(Number(data.confidence)) ? Number(data.confidence) : 0,
    rationale: String(data.rationale || ''),
    source: String(data.source || 'mock_provider'),
    warning: data.warning ? String(data.warning) : '',
  }
}

function normalizeSelectorRepairPreview(data) {
  if (!data || typeof data !== 'object') {
    return {
      platform_id: '',
      status: 'preview_failed',
      matched_targets: {},
      sample_values: {},
      warnings: ['empty_selector_repair_preview_response'],
      suggestion: null,
      profile_modified: false,
    }
  }
  return {
    ...data,
    platform_id: String(data.platform_id || ''),
    status: String(data.status || 'preview_failed'),
    matched_targets: normalizeBooleanMap(data.matched_targets),
    sample_values: normalizeStringMap(data.sample_values),
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
    suggestion: data.suggestion ? normalizeSelectorRepairSuggestion(data.suggestion) : null,
    profile_modified: Boolean(data.profile_modified),
  }
}

function normalizeBooleanMap(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {}
  return Object.fromEntries(
    Object.entries(value).map(([key, mapValue]) => [String(key), Boolean(mapValue)]),
  )
}

function normalizeStringMap(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {}
  return Object.fromEntries(
    Object.entries(value).map(([key, mapValue]) => [String(key), String(mapValue ?? '')]),
  )
}

function normalizeOptionalScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue : null
}
