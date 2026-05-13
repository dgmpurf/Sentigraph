import { apiClient } from './client.js'

const API_PREFIX = '/api/v1'

export async function expandKeywords(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/keywords/expand`, payload)
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
  return data
}

export async function getVisualizationData(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/visualization/data`, payload)
  return data
}

export async function generateSummary(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/summary/generate`, payload)
  return data
}

export async function generateRecommendation(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/recommendation/generate`, payload)
  return data
}

export async function getPropagation(projectId) {
  const { data } = await apiClient.get(`${API_PREFIX}/propagation/${projectId}`)
  return data
}

export async function getAlerts(projectId) {
  const { data } = await apiClient.get(`${API_PREFIX}/alerts/${projectId}`)
  return data
}

