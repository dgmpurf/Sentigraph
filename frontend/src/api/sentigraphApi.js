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

export async function getLlmStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/llm/status`)
  return normalizeLlmStatus(data)
}

export async function getLlmUsage() {
  const { data } = await apiClient.get(`${API_PREFIX}/llm/usage`)
  return normalizeLlmUsage(data)
}

export async function getLatestBenchmarkSummary() {
  const { data } = await apiClient.get(`${API_PREFIX}/benchmarks/latest`)
  return normalizeBenchmarkSummary(data)
}

export async function getBenchmarkHistory() {
  const { data } = await apiClient.get(`${API_PREFIX}/benchmarks/history`)
  return normalizeBenchmarkHistory(data)
}

export async function getBenchmarkRegression() {
  const { data } = await apiClient.get(`${API_PREFIX}/benchmarks/regression`)
  return normalizeBenchmarkRegression(data)
}

export async function getSimulationDemoScenario() {
  const { data } = await apiClient.get(`${API_PREFIX}/simulation/demo-scenario`)
  return normalizeSimulationScenario(data)
}

export async function getSimulationEthicsPolicy() {
  const { data } = await apiClient.get(`${API_PREFIX}/simulation/ethics-policy`)
  return normalizeSimulationEthicsPolicy(data)
}

export async function runSimulation(scenario) {
  const { data } = await apiClient.post(`${API_PREFIX}/simulation/run`, scenario)
  return normalizeSimulationRunResult(data)
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

export async function getCaseForecast(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/forecast`)
  return normalizeForecast(data)
}

export async function runCaseForecast(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/forecast/run`)
  return normalizeForecast(data)
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

function normalizeForecast(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      forecast_status: 'insufficient_history',
      generated_at: null,
      risk_model_version: null,
      snapshot_count: 0,
      latest_snapshot_id: null,
      horizon: 'next_check',
      latest_risk: 0,
      moving_average: 0,
      slope: 0,
      acceleration: 0,
      volatility: 0,
      trend_direction: 'unknown',
      forecast_confidence: 'insufficient_history',
      predicted_risk_score: 0,
      predicted_risk_level: 'low',
      predicted_real_crisis_risk: 0,
      predicted_manipulation_risk: 0,
      real_crisis_trend_direction: 'unknown',
      manipulation_trend_direction: 'unknown',
      risk_forecasts: [],
      topic_forecasts: [],
      input_snapshots: [],
      recommended_action: '请先运行监控检查，生成监控快照后再运行风险预测。',
      message: '历史不足，需更多监控快照。',
    }
  }
  return {
    ...data,
    case_id: String(data.case_id || ''),
    forecast_status: String(data.forecast_status || 'insufficient_history'),
    generated_at: data.generated_at ? String(data.generated_at) : null,
    risk_model_version: data.risk_model_version ? String(data.risk_model_version) : null,
    snapshot_count: Number(data.snapshot_count || 0),
    latest_snapshot_id: data.latest_snapshot_id ? String(data.latest_snapshot_id) : null,
    horizon: String(data.horizon || 'next_check'),
    latest_risk: normalizeOptionalScore(data.latest_risk) ?? 0,
    moving_average: normalizeOptionalScore(data.moving_average) ?? 0,
    slope: normalizeOptionalScore(data.slope) ?? 0,
    acceleration: normalizeOptionalScore(data.acceleration) ?? 0,
    volatility: normalizeOptionalScore(data.volatility) ?? 0,
    trend_direction: String(data.trend_direction || 'unknown'),
    forecast_confidence: String(data.forecast_confidence || 'insufficient_history'),
    predicted_risk_score: normalizeOptionalScore(data.predicted_risk_score) ?? 0,
    predicted_risk_level: String(data.predicted_risk_level || 'low'),
    predicted_real_crisis_risk: normalizeOptionalScore(data.predicted_real_crisis_risk) ?? 0,
    predicted_manipulation_risk: normalizeOptionalScore(data.predicted_manipulation_risk) ?? 0,
    real_crisis_trend_direction: String(data.real_crisis_trend_direction || 'unknown'),
    manipulation_trend_direction: String(data.manipulation_trend_direction || 'unknown'),
    risk_forecasts: Array.isArray(data.risk_forecasts)
      ? data.risk_forecasts.map(normalizeRiskForecast).filter(Boolean)
      : [],
    topic_forecasts: Array.isArray(data.topic_forecasts)
      ? data.topic_forecasts.map(normalizeTopicRiskForecast).filter(Boolean)
      : [],
    input_snapshots: Array.isArray(data.input_snapshots)
      ? data.input_snapshots.map(normalizeSnapshot).filter(Boolean)
      : [],
    recommended_action: String(data.recommended_action || ''),
    message: String(data.message || ''),
  }
}

function normalizeRiskForecast(data) {
  if (!data || typeof data !== 'object') return null
  return {
    horizon: String(data.horizon || 'next_check'),
    predicted_risk_score: normalizeOptionalScore(data.predicted_risk_score) ?? 0,
    predicted_risk_level: String(data.predicted_risk_level || 'low'),
    predicted_real_crisis_risk: normalizeOptionalScore(data.predicted_real_crisis_risk) ?? 0,
    predicted_manipulation_risk: normalizeOptionalScore(data.predicted_manipulation_risk) ?? 0,
    trend_direction: String(data.trend_direction || 'unknown'),
    real_crisis_trend_direction: String(data.real_crisis_trend_direction || 'unknown'),
    manipulation_trend_direction: String(data.manipulation_trend_direction || 'unknown'),
    forecast_confidence: String(data.forecast_confidence || 'insufficient_history'),
    forecast_reason: String(data.forecast_reason || ''),
  }
}

function normalizeTopicRiskForecast(data) {
  if (!data || typeof data !== 'object') return null
  return {
    topic_id: String(data.topic_id || ''),
    topic: String(data.topic || '未命名话题'),
    current_topic_risk_score: normalizeOptionalScore(data.current_topic_risk_score) ?? 0,
    predicted_topic_risk_score: normalizeOptionalScore(data.predicted_topic_risk_score) ?? 0,
    predicted_topic_risk_level: String(data.predicted_topic_risk_level || 'low'),
    trend_direction: String(data.trend_direction || 'unknown'),
    risk_explanation: String(data.risk_explanation || ''),
    forecast_reason: String(data.forecast_reason || ''),
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
      schema_valid: null,
      comment_count: null,
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
    schema_valid: typeof data.schema_valid === 'boolean' ? data.schema_valid : null,
    comment_count: Number.isFinite(Number(data.comment_count)) ? Number(data.comment_count) : null,
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
    suggestion: data.suggestion ? normalizeSelectorRepairSuggestion(data.suggestion) : null,
    profile_modified: Boolean(data.profile_modified),
  }
}

function normalizeLlmStatus(data) {
  if (!data || typeof data !== 'object') {
    return {
      provider_name: 'mock',
      provider_status: 'unknown',
      real_calls_enabled: false,
      api_key_present: false,
      available_providers: [],
      providers: [],
      tracking_enabled: true,
      daily_call_limit: 100,
      daily_token_limit: 100000,
      max_input_chars: 20000,
      guardrail_mode: 'mock',
      safety_flags: {},
    }
  }
  return {
    ...data,
    provider_name: String(data.provider_name || 'mock'),
    provider_status: String(data.provider_status || 'unknown'),
    real_calls_enabled: Boolean(data.real_calls_enabled),
    api_key_present: Boolean(data.api_key_present),
    available_providers: Array.isArray(data.available_providers)
      ? data.available_providers.map((provider) => String(provider))
      : [],
    providers: Array.isArray(data.providers) ? data.providers.map(normalizeLlmProviderStatus).filter(Boolean) : [],
    tracking_enabled: data.tracking_enabled !== false,
    daily_call_limit: Number.isFinite(Number(data.daily_call_limit)) ? Number(data.daily_call_limit) : 100,
    daily_token_limit: Number.isFinite(Number(data.daily_token_limit)) ? Number(data.daily_token_limit) : 100000,
    max_input_chars: Number.isFinite(Number(data.max_input_chars)) ? Number(data.max_input_chars) : 20000,
    guardrail_mode: String(data.guardrail_mode || 'mock'),
    safety_flags: normalizeBooleanMap(data.safety_flags),
  }
}

function normalizeLlmProviderStatus(data) {
  if (!data || typeof data !== 'object') return null
  return {
    provider_name: String(data.provider_name || ''),
    provider_status: String(data.provider_status || 'unknown'),
    real_calls_enabled: Boolean(data.real_calls_enabled),
    api_key_present: Boolean(data.api_key_present),
    api_key_required: Boolean(data.api_key_required),
    available: Boolean(data.available),
  }
}

function normalizeLlmUsage(data) {
  if (!data || typeof data !== 'object') {
    return {
      tracking_enabled: true,
      guardrail_mode: 'mock',
      daily_call_limit: 100,
      daily_token_limit: 100000,
      max_input_chars: 20000,
      total_calls: 0,
      daily_calls: 0,
      daily_input_tokens: 0,
      daily_output_tokens: 0,
      daily_total_tokens: 0,
      recent_records: [],
    }
  }
  return {
    ...data,
    tracking_enabled: data.tracking_enabled !== false,
    guardrail_mode: String(data.guardrail_mode || 'mock'),
    daily_call_limit: Number.isFinite(Number(data.daily_call_limit)) ? Number(data.daily_call_limit) : 100,
    daily_token_limit: Number.isFinite(Number(data.daily_token_limit)) ? Number(data.daily_token_limit) : 100000,
    max_input_chars: Number.isFinite(Number(data.max_input_chars)) ? Number(data.max_input_chars) : 20000,
    total_calls: Number(data.total_calls || 0),
    daily_calls: Number(data.daily_calls || 0),
    daily_input_tokens: Number(data.daily_input_tokens || 0),
    daily_output_tokens: Number(data.daily_output_tokens || 0),
    daily_total_tokens: Number(data.daily_total_tokens || 0),
    recent_records: Array.isArray(data.recent_records)
      ? data.recent_records.map(normalizeLlmUsageRecord).filter(Boolean)
      : [],
  }
}

function normalizeLlmUsageRecord(data) {
  if (!data || typeof data !== 'object') return null
  return {
    provider: String(data.provider || ''),
    operation: String(data.operation || ''),
    input_chars: Number(data.input_chars || 0),
    output_chars: Number(data.output_chars || 0),
    estimated_input_tokens: Number(data.estimated_input_tokens || 0),
    estimated_output_tokens: Number(data.estimated_output_tokens || 0),
    timestamp: data.timestamp ? String(data.timestamp) : '',
    success: data.success !== false,
    failure_category: data.failure_category ? String(data.failure_category) : null,
  }
}

function normalizeBenchmarkSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      source: 'offline_benchmark_summary',
      available: false,
      status: 'missing',
      generated_at: null,
      benchmark_version: null,
      total_passed: 0,
      total_failed: 0,
      total_warnings: 0,
      suites: [],
      message: 'Benchmark summary is unavailable.',
    }
  }
  return {
    ...data,
    source: String(data.source || 'offline_benchmark_summary'),
    available: Boolean(data.available),
    status: String(data.status || 'unknown'),
    benchmark_id: data.benchmark_id ? String(data.benchmark_id) : null,
    generated_at: data.generated_at ? String(data.generated_at) : null,
    benchmark_version: data.benchmark_version ? String(data.benchmark_version) : null,
    duration_seconds: Number.isFinite(Number(data.duration_seconds)) ? Number(data.duration_seconds) : null,
    total_passed: Number(data.total_passed || 0),
    total_failed: Number(data.total_failed || 0),
    total_warnings: Number(data.total_warnings || 0),
    suites: Array.isArray(data.suites) ? data.suites.map(normalizeBenchmarkSuite).filter(Boolean) : [],
    regression_detected:
      typeof data.regression_detected === 'boolean' ? data.regression_detected : null,
    message: String(data.message || ''),
  }
}

function normalizeBenchmarkSuite(data) {
  if (!data || typeof data !== 'object') return null
  return {
    suite: String(data.suite || ''),
    status: String(data.status || 'unknown'),
    case_count: Number(data.case_count || 0),
    passed: Number(data.passed || 0),
    failed: Number(data.failed || 0),
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizeBenchmarkHistory(data) {
  if (!data || typeof data !== 'object') {
    return {
      source: 'offline_benchmark_history',
      available: false,
      status: 'missing',
      total_entries: 0,
      malformed_entries: 0,
      entries: [],
      message: 'Benchmark history is unavailable.',
    }
  }
  return {
    ...data,
    source: String(data.source || 'offline_benchmark_history'),
    available: Boolean(data.available),
    status: String(data.status || 'unknown'),
    total_entries: Number(data.total_entries || 0),
    malformed_entries: Number(data.malformed_entries || 0),
    entries: Array.isArray(data.entries)
      ? data.entries.map(normalizeBenchmarkHistoryEntry).filter(Boolean)
      : [],
    message: String(data.message || ''),
  }
}

function normalizeBenchmarkHistoryEntry(data) {
  if (!data || typeof data !== 'object') return null
  return {
    source: String(data.source || 'offline_benchmark'),
    benchmark_id: String(data.benchmark_id || ''),
    generated_at: data.generated_at ? String(data.generated_at) : null,
    benchmark_version: data.benchmark_version ? String(data.benchmark_version) : null,
    duration_seconds: Number.isFinite(Number(data.duration_seconds)) ? Number(data.duration_seconds) : null,
    total_passed: Number(data.total_passed || 0),
    total_failed: Number(data.total_failed || 0),
    total_warnings: Number(data.total_warnings || 0),
    suites: Array.isArray(data.suites) ? data.suites.map(normalizeBenchmarkSuite).filter(Boolean) : [],
    regression_detected:
      typeof data.regression_detected === 'boolean' ? data.regression_detected : null,
  }
}

function normalizeBenchmarkRegression(data) {
  if (!data || typeof data !== 'object') {
    return {
      source: 'offline_benchmark_regression',
      available: false,
      status: 'missing',
      regression_detected: false,
      changed_suites: [],
      previous_benchmark_id: null,
      latest_benchmark_id: null,
      previous_generated_at: null,
      latest_generated_at: null,
      previous_total_failed: null,
      latest_total_failed: 0,
      previous_total_warnings: null,
      latest_total_warnings: 0,
      previous_total_passed: null,
      latest_total_passed: 0,
      reason_categories: [],
      message: 'Benchmark regression status is unavailable.',
    }
  }
  return {
    ...data,
    source: String(data.source || 'offline_benchmark_regression'),
    available: Boolean(data.available),
    status: String(data.status || 'unknown'),
    regression_detected: Boolean(data.regression_detected),
    changed_suites: Array.isArray(data.changed_suites)
      ? data.changed_suites.map(normalizeBenchmarkSuiteChange).filter(Boolean)
      : [],
    previous_benchmark_id: data.previous_benchmark_id ? String(data.previous_benchmark_id) : null,
    latest_benchmark_id: data.latest_benchmark_id ? String(data.latest_benchmark_id) : null,
    previous_generated_at: data.previous_generated_at ? String(data.previous_generated_at) : null,
    latest_generated_at: data.latest_generated_at ? String(data.latest_generated_at) : null,
    previous_total_failed:
      data.previous_total_failed === null || data.previous_total_failed === undefined
        ? null
        : Number(data.previous_total_failed || 0),
    latest_total_failed: Number(data.latest_total_failed || 0),
    previous_total_warnings:
      data.previous_total_warnings === null || data.previous_total_warnings === undefined
        ? null
        : Number(data.previous_total_warnings || 0),
    latest_total_warnings: Number(data.latest_total_warnings || 0),
    previous_total_passed:
      data.previous_total_passed === null || data.previous_total_passed === undefined
        ? null
        : Number(data.previous_total_passed || 0),
    latest_total_passed: Number(data.latest_total_passed || 0),
    reason_categories: Array.isArray(data.reason_categories)
      ? data.reason_categories.map((reason) => String(reason))
      : [],
    message: String(data.message || ''),
  }
}

function normalizeBenchmarkSuiteChange(data) {
  if (!data || typeof data !== 'object') return null
  return {
    suite: String(data.suite || ''),
    change_types: Array.isArray(data.change_types)
      ? data.change_types.map((changeType) => String(changeType))
      : [],
    previous_status: String(data.previous_status || 'unknown'),
    latest_status: String(data.latest_status || 'unknown'),
    previous_failed: Number(data.previous_failed || 0),
    latest_failed: Number(data.latest_failed || 0),
    previous_warnings: Number(data.previous_warnings || 0),
    latest_warnings: Number(data.latest_warnings || 0),
  }
}

function normalizeSimulationScenario(data) {
  if (!data || typeof data !== 'object') {
    return {
      scenario_id: '',
      name: '',
      description: '',
      topic: 'brand_crisis',
      agents: [],
      network_edges: [],
      messages: [],
      interventions: [],
      config: { steps: 6, seed: null, model_version: 'simulation_lab_mvp_v1' },
      responsibility_level: 0.5,
      metadata: {},
    }
  }
  return {
    ...data,
    scenario_id: String(data.scenario_id || ''),
    name: String(data.name || ''),
    description: String(data.description || ''),
    topic: String(data.topic || 'brand_crisis'),
    agents: Array.isArray(data.agents) ? data.agents.map(normalizeSimulationAgent).filter(Boolean) : [],
    network_edges: Array.isArray(data.network_edges)
      ? data.network_edges.map(normalizeSimulationEdge).filter(Boolean)
      : [],
    messages: Array.isArray(data.messages)
      ? data.messages.map(normalizeSimulationMessage).filter(Boolean)
      : [],
    interventions: Array.isArray(data.interventions)
      ? data.interventions.map(normalizeSimulationIntervention).filter(Boolean)
      : [],
    config: normalizeSimulationConfig(data.config),
    responsibility_level: normalizeRatio(data.responsibility_level, 0.5),
    metadata: data.metadata && typeof data.metadata === 'object' && !Array.isArray(data.metadata) ? data.metadata : {},
  }
}

function normalizeSimulationAgent(data) {
  if (!data || typeof data !== 'object') return null
  return {
    agent_id: String(data.agent_id || ''),
    community_id: String(data.community_id || 'neutral'),
    latent_opinion: normalizeSignedScore(data.latent_opinion),
    expressed_opinion: normalizeSignedScore(data.expressed_opinion),
    prior_anchor: normalizeSignedScore(data.prior_anchor),
    stubbornness: normalizeRatio(data.stubbornness, 0.5),
    confidence_radius: normalizeBounded(data.confidence_radius, 0, 2, 0.5),
    action_threshold: normalizeRatio(data.action_threshold, 0.5),
    confirmation_bias: normalizeRatio(data.confirmation_bias, 0.5),
    negativity_weight: normalizeBounded(data.negativity_weight, 0, 3, 1),
    reactance: normalizeRatio(data.reactance, 0.3),
    authority_trust: normalizeRatio(data.authority_trust, 0.5),
    conformity: normalizeRatio(data.conformity, 0.4),
    attention_budget: normalizeRatio(data.attention_budget, 0.5),
    fatigue: normalizeRatio(data.fatigue, 0),
    identity_group: String(data.identity_group || 'general_public'),
    status: String(data.status || 'active'),
  }
}

function normalizeSimulationEdge(data) {
  if (!data || typeof data !== 'object') return null
  return {
    source_agent_id: String(data.source_agent_id || ''),
    target_agent_id: String(data.target_agent_id || ''),
    weight: normalizeRatio(data.weight, 1),
    bridge_score: normalizeRatio(data.bridge_score, 0),
    relationship_type: String(data.relationship_type || 'peer'),
  }
}

function normalizeSimulationMessage(data) {
  if (!data || typeof data !== 'object') return null
  return {
    message_id: String(data.message_id || ''),
    topic: String(data.topic || ''),
    source_type: String(data.source_type || 'public_posts'),
    source_credibility: normalizeRatio(data.source_credibility, 0.5),
    stance_direction: normalizeSignedScore(data.stance_direction),
    emotional_intensity: normalizeRatio(data.emotional_intensity, 0),
    evidence_strength: normalizeRatio(data.evidence_strength, 0),
    framing: String(data.framing || 'neutral'),
    novelty: normalizeRatio(data.novelty, 0.5),
    repetition: normalizeRatio(data.repetition, 0),
    platform_reach: normalizeRatio(data.platform_reach, 0.5),
  }
}

function normalizeSimulationIntervention(data) {
  if (!data || typeof data !== 'object') return null
  return {
    intervention_id: String(data.intervention_id || ''),
    intervention_type: String(data.intervention_type || 'no_response'),
    topic: String(data.topic || 'brand_crisis'),
    source_type: String(data.source_type || 'official'),
    message: String(data.message || ''),
    target_scope: String(data.target_scope || 'aggregate'),
    publication_step: Number(data.publication_step || 1),
    source_credibility: normalizeRatio(data.source_credibility, 0.75),
    stance_direction: normalizeSignedScore(data.stance_direction),
    emotional_intensity: normalizeRatio(data.emotional_intensity, 0.25),
    evidence_strength: normalizeRatio(data.evidence_strength, 0.65),
    framing: String(data.framing || 'clarifying'),
    responsibility_acknowledgement: normalizeRatio(data.responsibility_acknowledgement, 0.4),
    transparency_level: normalizeRatio(data.transparency_level, 0.7),
    intensity: normalizeRatio(data.intensity, 0.6),
  }
}

function normalizeSimulationConfig(data) {
  if (!data || typeof data !== 'object') {
    return { steps: 6, seed: null, model_version: 'simulation_lab_mvp_v1' }
  }
  return {
    ...data,
    steps: Math.min(50, Math.max(1, Number.isFinite(Number(data.steps)) ? Number(data.steps) : 6)),
    seed:
      data.seed === null || data.seed === undefined || !Number.isFinite(Number(data.seed))
        ? null
        : Number(data.seed),
    peer_influence_weight: normalizeRatio(data.peer_influence_weight, 0.28),
    message_influence_weight: normalizeRatio(data.message_influence_weight, 0.32),
    prior_persistence_weight: normalizeRatio(data.prior_persistence_weight, 0.35),
    attention_decay: normalizeRatio(data.attention_decay, 0.08),
    fatigue_increase: normalizeRatio(data.fatigue_increase, 0.035),
    model_version: String(data.model_version || 'simulation_lab_mvp_v1'),
  }
}

function normalizeSimulationEthicsPolicy(data) {
  if (!data || typeof data !== 'object') {
    return {
      allowed_intervention_types: [],
      forbidden_intervention_types: [],
      policy_summary: '',
      aggregate_level_only: true,
    }
  }
  return {
    allowed_intervention_types: Array.isArray(data.allowed_intervention_types)
      ? data.allowed_intervention_types.map((item) => String(item))
      : [],
    forbidden_intervention_types: Array.isArray(data.forbidden_intervention_types)
      ? data.forbidden_intervention_types.map((item) => String(item))
      : [],
    policy_summary: String(data.policy_summary || ''),
    aggregate_level_only: data.aggregate_level_only !== false,
  }
}

function normalizeSimulationRunResult(data) {
  if (!data || typeof data !== 'object') {
    return {
      scenario_id: '',
      scenario_name: '',
      simulation_status: 'rejected',
      generated_at: null,
      model_version: 'simulation_lab_mvp_v1',
      steps_requested: 0,
      steps_completed: 0,
      ethics_check: normalizeSimulationEthicsCheck(null),
      initial_metrics: normalizeSimulationMetrics(null),
      final_metrics: normalizeSimulationMetrics(null),
      step_results: [],
      key_findings: [],
      recommended_interpretation: '',
      safe_mode: {},
      warnings: [],
    }
  }
  return {
    ...data,
    scenario_id: String(data.scenario_id || ''),
    scenario_name: String(data.scenario_name || ''),
    simulation_status: String(data.simulation_status || 'completed'),
    generated_at: data.generated_at ? String(data.generated_at) : null,
    model_version: String(data.model_version || 'simulation_lab_mvp_v1'),
    steps_requested: Number(data.steps_requested || 0),
    steps_completed: Number(data.steps_completed || 0),
    ethics_check: normalizeSimulationEthicsCheck(data.ethics_check),
    initial_metrics: normalizeSimulationMetrics(data.initial_metrics),
    final_metrics: normalizeSimulationMetrics(data.final_metrics),
    step_results: Array.isArray(data.step_results)
      ? data.step_results.map(normalizeSimulationStepResult).filter(Boolean)
      : [],
    key_findings: Array.isArray(data.key_findings)
      ? data.key_findings.map((finding) => String(finding))
      : [],
    recommended_interpretation: String(data.recommended_interpretation || ''),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizeSimulationEthicsCheck(data) {
  if (!data || typeof data !== 'object') {
    return {
      allowed: false,
      reason: '',
      blocked_categories: [],
      allowed_intervention_types: [],
      forbidden_intervention_types: [],
      warnings: [],
    }
  }
  return {
    allowed: Boolean(data.allowed),
    reason: String(data.reason || ''),
    blocked_categories: Array.isArray(data.blocked_categories)
      ? data.blocked_categories.map((item) => String(item))
      : [],
    allowed_intervention_types: Array.isArray(data.allowed_intervention_types)
      ? data.allowed_intervention_types.map((item) => String(item))
      : [],
    forbidden_intervention_types: Array.isArray(data.forbidden_intervention_types)
      ? data.forbidden_intervention_types.map((item) => String(item))
      : [],
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizeSimulationStepResult(data) {
  if (!data || typeof data !== 'object') return null
  return {
    step: Number(data.step || 0),
    active_intervention_type: String(data.active_intervention_type || 'no_response'),
    metrics: normalizeSimulationMetrics(data.metrics),
    trend_direction: String(data.trend_direction || 'unknown'),
    forecast_reason: String(data.forecast_reason || ''),
    community_metrics:
      data.community_metrics && typeof data.community_metrics === 'object' && !Array.isArray(data.community_metrics)
        ? Object.fromEntries(
            Object.entries(data.community_metrics).map(([key, value]) => [
              String(key),
              normalizeSimulationMetrics(value),
            ]),
          )
        : {},
  }
}

function normalizeSimulationMetrics(data) {
  if (!data || typeof data !== 'object') {
    return {
      average_latent_opinion: 0,
      average_expressed_opinion: 0,
      negative_ratio: 0,
      neutral_ratio: 1,
      positive_ratio: 0,
      polarization_index: 0,
      attention_level: 0,
      trust_recovery_proxy: 0,
      intervention_effect_score: 0,
      false_belief_proxy: 0,
      min_latent_opinion: 0,
      max_latent_opinion: 0,
      min_expressed_opinion: 0,
      max_expressed_opinion: 0,
      ethical_risk_flags: [],
    }
  }
  return {
    average_latent_opinion: normalizeSignedScore(data.average_latent_opinion),
    average_expressed_opinion: normalizeSignedScore(data.average_expressed_opinion),
    negative_ratio: normalizeRatio(data.negative_ratio, 0),
    neutral_ratio: normalizeRatio(data.neutral_ratio, 0),
    positive_ratio: normalizeRatio(data.positive_ratio, 0),
    polarization_index: normalizeRatio(data.polarization_index, 0),
    attention_level: normalizeRatio(data.attention_level, 0),
    trust_recovery_proxy: normalizeRatio(data.trust_recovery_proxy, 0),
    intervention_effect_score: normalizeOptionalScore(data.intervention_effect_score) ?? 0,
    false_belief_proxy: normalizeRatio(data.false_belief_proxy, 0),
    min_latent_opinion: normalizeSignedScore(data.min_latent_opinion),
    max_latent_opinion: normalizeSignedScore(data.max_latent_opinion),
    min_expressed_opinion: normalizeSignedScore(data.min_expressed_opinion),
    max_expressed_opinion: normalizeSignedScore(data.max_expressed_opinion),
    ethical_risk_flags: Array.isArray(data.ethical_risk_flags)
      ? data.ethical_risk_flags.map((flag) => String(flag))
      : [],
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

function normalizeSignedScore(value) {
  const numericValue = Number(value)
  if (!Number.isFinite(numericValue)) return 0
  return Math.min(1, Math.max(-1, numericValue))
}

function normalizeRatio(value, fallback = 0) {
  const numericValue = Number(value)
  if (!Number.isFinite(numericValue)) return fallback
  return Math.min(1, Math.max(0, numericValue))
}

function normalizeBounded(value, min, max, fallback = min) {
  const numericValue = Number(value)
  if (!Number.isFinite(numericValue)) return fallback
  return Math.min(max, Math.max(min, numericValue))
}
