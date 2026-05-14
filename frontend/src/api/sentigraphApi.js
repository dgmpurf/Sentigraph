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

function normalizeOptionalScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue : null
}
