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
  }
}

function normalizeOptionalScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue : null
}
