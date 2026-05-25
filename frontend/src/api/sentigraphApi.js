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

export async function getPlatformReadiness() {
  const { data } = await apiClient.get(`${API_PREFIX}/platforms/readiness`)
  return data
}

export async function getSourceCatalog() {
  const { data } = await apiClient.get(`${API_PREFIX}/sources/catalog`)
  return normalizeSourceCatalog(data)
}

export async function getSearchDiscoveryStatus() {
  const { data } = await apiClient.get(`${API_PREFIX}/search-discovery/status`)
  return normalizeSearchDiscoveryStatus(data)
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

export async function exportSimulationStrategyMarkdownReport(payload) {
  const { data } = await apiClient.post(`${API_PREFIX}/simulation/report/markdown`, payload)
  return normalizeSimulationStrategyReportResponse(data)
}

export async function initializeCaseSimulation(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/simulation/initialize`)
  return normalizeCaseSimulationInitialization(data)
}

export async function previewCaseSimulationInitialization(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/simulation/initialization-preview`)
  return normalizeCaseSimulationInitialization(data)
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

export async function createCase(payload) {
  return createAnalysisCase(payload)
}

export async function getAnalysisCase(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}`)
  return normalizeCaseDetail(data)
}

export async function getCase(caseId) {
  return getAnalysisCase(caseId)
}

export async function runAnalysisCase(caseId) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/run`)
  return normalizeCaseDetail(data)
}

export async function runCase(caseId) {
  return runAnalysisCase(caseId)
}

export async function crawlCaseRawData(caseId, payload = {}) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/crawl/start`, payload)
  return normalizeCaseDetail(data)
}

export async function getCaseEvidence(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence`)
  return normalizeEvidenceIngestionResult(data)
}

export async function getCaseEvidenceTrustSummary(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/trust-summary`)
  return normalizeEvidenceTrustSummary(data)
}

export async function getCaseEvidenceDedupSummary(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/dedup-summary`)
  return normalizeEvidenceDeduplicationSummary(data)
}

export async function getCaseEvidenceSummary(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/summary`)
  return normalizeEvidenceBatchSummary(data)
}

export async function getCaseEvidenceJobs(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/jobs`)
  return Array.isArray(data) ? data.map(normalizeEvidenceIngestionJob).filter(Boolean) : []
}

export async function getCaseEvidenceCoverage(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/coverage`)
  return normalizeEvidenceCoverageSummary(data)
}

export async function getCaseEvidenceReviewQueue(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/review-queue`)
  return normalizeEvidenceReviewSummary(data)
}

export async function getCaseEvidenceReviewSummary(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/review-summary`)
  return normalizeEvidenceReviewSummary(data)
}

export async function getCaseEvidenceReviewTimeline(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/review-timeline`)
  return normalizeEvidenceReviewTimeline(data)
}

export async function getCaseEvidenceReviewAuditSummary(caseId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/review-audit-summary`)
  return normalizeEvidenceReviewAuditSummary(data)
}

export async function getCaseEvidenceReviewHistory(caseId, evidenceId) {
  const { data } = await apiClient.get(`${API_PREFIX}/cases/${caseId}/evidence/${evidenceId}/review-history`)
  return normalizeEvidenceReviewTimeline(data)
}

export async function reviewCaseEvidence(caseId, evidenceId, payload = {}) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/evidence/${evidenceId}/review`, payload)
  return normalizeEvidenceReviewDecisionResult(data)
}

export async function attachCaseEvidence(caseId, payload = {}) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/evidence/attach`, payload)
  return normalizeEvidenceIngestionResult(data)
}

export async function previewCaseEvidenceImport(caseId, payload = {}) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/evidence/import/preview`, payload)
  return normalizeEvidenceImportPreview(data)
}

export async function commitCaseEvidenceImport(caseId, payload = {}) {
  const { data } = await apiClient.post(`${API_PREFIX}/cases/${caseId}/evidence/import/commit`, payload)
  return normalizeEvidenceImportCommit(data)
}

export function getEvidenceImportTemplateCsvUrl() {
  const baseUrl = String(apiClient.defaults.baseURL || '').replace(/\/$/, '')
  return `${baseUrl}${API_PREFIX}/evidence/import/template.csv`
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
    evidence_item_count: Number(data.evidence_item_count || 0),
    evidence_source_distribution: normalizeNumberMap(data.evidence_source_distribution),
    evidence_type_counts: normalizeNumberMap(data.evidence_type_counts),
    evidence_trust_label_distribution: normalizeNumberMap(data.evidence_trust_label_distribution),
    evidence_verification_status_distribution: normalizeNumberMap(data.evidence_verification_status_distribution),
    evidence_provenance_type_distribution: normalizeNumberMap(data.evidence_provenance_type_distribution),
    evidence_review_needed_count: Number(data.evidence_review_needed_count || 0),
    evidence_unique_item_count: Number(data.evidence_unique_item_count || 0),
    evidence_duplicate_item_count: Number(data.evidence_duplicate_item_count || 0),
    evidence_review_excluded_count: Number(data.evidence_review_excluded_count || 0),
  }
}

function normalizeCaseDetail(data) {
  if (!data || typeof data !== 'object') return data
  return {
    ...data,
    analysis_result: normalizeRiskExtension(data.analysis_result),
    visualization_data: normalizeRiskExtension(data.visualization_data),
    report: normalizeRiskExtension(data.report),
    evidence_items: Array.isArray(data.evidence_items) ? data.evidence_items.map(normalizeEvidenceItem).filter(Boolean) : [],
    evidence_ingestion_jobs: Array.isArray(data.evidence_ingestion_jobs)
      ? data.evidence_ingestion_jobs.map(normalizeEvidenceIngestionJob).filter(Boolean)
      : [],
    evidence_item_count: Number(data.evidence_item_count || 0),
    monitoring_config: normalizeMonitoringConfig(data.monitoring_config),
  }
}

function normalizeEvidenceIngestionResult(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      status: 'empty',
      evidence_items: [],
      evidence_item_count: 0,
      source_distribution: {},
      evidence_type_counts: {},
      top_titles: [],
      representative_comments: [],
      trust_summary: normalizeEvidenceTrustSummary(null),
      deduplication_summary: normalizeEvidenceDeduplicationSummary(null),
      warnings: [],
      safe_mode: {},
    }
  }
  return {
    ...data,
    case_id: String(data.case_id || ''),
    status: String(data.status || 'empty'),
    evidence_items: Array.isArray(data.evidence_items) ? data.evidence_items.map(normalizeEvidenceItem).filter(Boolean) : [],
    evidence_item_count: Number(data.evidence_item_count || 0),
    source_distribution: normalizeNumberMap(data.source_distribution),
    evidence_type_counts: normalizeNumberMap(data.evidence_type_counts),
    top_titles: Array.isArray(data.top_titles) ? data.top_titles.map((item) => String(item)) : [],
    representative_comments: Array.isArray(data.representative_comments)
      ? data.representative_comments.map((item) => String(item))
      : [],
    trust_summary: normalizeEvidenceTrustSummary(data.trust_summary),
    deduplication_summary: normalizeEvidenceDeduplicationSummary(data.deduplication_summary),
    warnings: Array.isArray(data.warnings) ? data.warnings.map((item) => String(item)) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceTrustSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      trust_label_distribution: {},
      verification_status_distribution: {},
      provenance_type_distribution: {},
      warning_counts: {},
      review_needed_count: 0,
      low_trust_count: 0,
      unverified_count: 0,
      duplicate_summary: normalizeEvidenceDeduplicationSummary(null),
      safe_mode: {},
    }
  }
  return {
    trust_label_distribution: normalizeNumberMap(data.trust_label_distribution),
    verification_status_distribution: normalizeNumberMap(data.verification_status_distribution),
    provenance_type_distribution: normalizeNumberMap(data.provenance_type_distribution),
    warning_counts: normalizeNumberMap(data.warning_counts),
    review_needed_count: Number(data.review_needed_count || 0),
    low_trust_count: Number(data.low_trust_count || 0),
    unverified_count: Number(data.unverified_count || 0),
    duplicate_summary: normalizeEvidenceDeduplicationSummary(data.duplicate_summary),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceDeduplicationSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      total_items: 0,
      unique_items: 0,
      duplicate_items: 0,
      duplicate_group_count: 0,
      top_duplicate_groups: [],
    }
  }
  return {
    total_items: Number(data.total_items || 0),
    unique_items: Number(data.unique_items || 0),
    duplicate_items: Number(data.duplicate_items || 0),
    duplicate_group_count: Number(data.duplicate_group_count || 0),
    top_duplicate_groups: Array.isArray(data.top_duplicate_groups)
      ? data.top_duplicate_groups.map(normalizeEvidenceDuplicateGroup).filter(Boolean)
      : [],
  }
}

function normalizeEvidenceDuplicateGroup(group) {
  if (!group || typeof group !== 'object') return null
  return {
    duplicate_group_id: String(group.duplicate_group_id || ''),
    duplicate_group_size: Number(group.duplicate_group_size || 0),
    representative_evidence_id: group.representative_evidence_id ? String(group.representative_evidence_id) : '',
    normalized_content_hash: group.normalized_content_hash ? String(group.normalized_content_hash) : '',
    canonical_url_hash: group.canonical_url_hash ? String(group.canonical_url_hash) : '',
    sample_text: group.sample_text ? String(group.sample_text) : '',
  }
}

function normalizeEvidenceBatchSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      evidence_count: 0,
      unique_evidence_count: 0,
      duplicate_evidence_count: 0,
      evidence_type_counts: {},
      source_distribution: {},
      acquisition_mode_distribution: {},
      trust_label_distribution: {},
      verification_status_distribution: {},
      review_status_distribution: {},
      rejected_count: 0,
      weak_evidence_count: 0,
      latest_jobs: [],
      latest_review_events: [],
      coverage_note: '',
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    evidence_count: Number(data.evidence_count || 0),
    unique_evidence_count: Number(data.unique_evidence_count || 0),
    duplicate_evidence_count: Number(data.duplicate_evidence_count || 0),
    evidence_type_counts: normalizeNumberMap(data.evidence_type_counts),
    source_distribution: normalizeNumberMap(data.source_distribution),
    acquisition_mode_distribution: normalizeNumberMap(data.acquisition_mode_distribution),
    trust_label_distribution: normalizeNumberMap(data.trust_label_distribution),
    verification_status_distribution: normalizeNumberMap(data.verification_status_distribution),
    review_status_distribution: normalizeNumberMap(data.review_status_distribution),
    rejected_count: Number(data.rejected_count || 0),
    weak_evidence_count: Number(data.weak_evidence_count || 0),
    latest_jobs: Array.isArray(data.latest_jobs) ? data.latest_jobs.map(normalizeEvidenceIngestionJob).filter(Boolean) : [],
    latest_review_events: Array.isArray(data.latest_review_events)
      ? data.latest_review_events.map(normalizeEvidenceReviewHistoryEntry).filter(Boolean)
      : [],
    coverage_note: data.coverage_note ? String(data.coverage_note) : '',
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceIngestionJob(job) {
  if (!job || typeof job !== 'object') return null
  return {
    job_id: String(job.job_id || ''),
    case_id: String(job.case_id || ''),
    status: String(job.status || 'completed'),
    source_type: String(job.source_type || ''),
    acquisition_mode: String(job.acquisition_mode || ''),
    input_type: String(job.input_type || ''),
    total_rows: Number(job.total_rows || 0),
    accepted_rows: Number(job.accepted_rows || 0),
    rejected_rows: Number(job.rejected_rows || 0),
    duplicate_rows: Number(job.duplicate_rows || 0),
    warning_count: Number(job.warning_count || 0),
    review_needed_count: Number(job.review_needed_count || 0),
    created_at: job.created_at ? String(job.created_at) : '',
    updated_at: job.updated_at ? String(job.updated_at) : '',
    completed_at: job.completed_at ? String(job.completed_at) : '',
    error_summary: job.error_summary ? String(job.error_summary) : '',
    progress: normalizeEvidenceIngestionProgress(job.progress),
    safe_metadata: job.safe_metadata && typeof job.safe_metadata === 'object' ? normalizeSafeObject(job.safe_metadata) : {},
    safe_mode: job.safe_mode && typeof job.safe_mode === 'object' ? normalizeBooleanMap(job.safe_mode) : {},
  }
}

function normalizeEvidenceIngestionProgress(progress) {
  if (!progress || typeof progress !== 'object') {
    return {
      total_rows: 0,
      processed_rows: 0,
      accepted_rows: 0,
      rejected_rows: 0,
      duplicate_rows: 0,
      warning_count: 0,
      review_needed_count: 0,
      progress_percent: 0,
      current_stage: '',
    }
  }
  return {
    total_rows: Number(progress.total_rows || 0),
    processed_rows: Number(progress.processed_rows || 0),
    accepted_rows: Number(progress.accepted_rows || 0),
    rejected_rows: Number(progress.rejected_rows || 0),
    duplicate_rows: Number(progress.duplicate_rows || 0),
    warning_count: Number(progress.warning_count || 0),
    review_needed_count: Number(progress.review_needed_count || 0),
    progress_percent: Number(progress.progress_percent || 0),
    current_stage: String(progress.current_stage || ''),
  }
}

function normalizeEvidenceCoverageSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      platforms_covered: [],
      source_types_covered: [],
      acquisition_modes_used: [],
      earliest_evidence_time: '',
      latest_evidence_time: '',
      evidence_count_by_platform: {},
      evidence_count_by_type: {},
      evidence_count_by_trust_label: {},
      source_coverage: [],
      warnings: [],
      coverage_note: '',
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    platforms_covered: Array.isArray(data.platforms_covered) ? data.platforms_covered.map((item) => String(item)) : [],
    source_types_covered: Array.isArray(data.source_types_covered) ? data.source_types_covered.map((item) => String(item)) : [],
    acquisition_modes_used: Array.isArray(data.acquisition_modes_used) ? data.acquisition_modes_used.map((item) => String(item)) : [],
    earliest_evidence_time: data.earliest_evidence_time ? String(data.earliest_evidence_time) : '',
    latest_evidence_time: data.latest_evidence_time ? String(data.latest_evidence_time) : '',
    evidence_count_by_platform: normalizeNumberMap(data.evidence_count_by_platform),
    evidence_count_by_type: normalizeNumberMap(data.evidence_count_by_type),
    evidence_count_by_trust_label: normalizeNumberMap(data.evidence_count_by_trust_label),
    source_coverage: Array.isArray(data.source_coverage) ? data.source_coverage.map(normalizeEvidenceSourceCoverage).filter(Boolean) : [],
    warnings: Array.isArray(data.warnings) ? data.warnings.map((item) => String(item)) : [],
    coverage_note: data.coverage_note ? String(data.coverage_note) : '',
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceSourceCoverage(item) {
  if (!item || typeof item !== 'object') return null
  return {
    platform: String(item.platform || ''),
    source_type: String(item.source_type || ''),
    acquisition_mode: String(item.acquisition_mode || ''),
    evidence_count: Number(item.evidence_count || 0),
    evidence_type_counts: normalizeNumberMap(item.evidence_type_counts),
    trust_label_counts: normalizeNumberMap(item.trust_label_counts),
  }
}

function normalizeEvidenceItem(item) {
  if (!item || typeof item !== 'object') return null
  return {
    evidence_id: String(item.evidence_id || ''),
    case_id: item.case_id ? String(item.case_id) : '',
    platform: String(item.platform || ''),
    source_type: String(item.source_type || ''),
    acquisition_mode: String(item.acquisition_mode || ''),
    evidence_type: String(item.evidence_type || ''),
    title: item.title ? String(item.title) : '',
    body_text: item.body_text ? String(item.body_text) : '',
    comment_text: item.comment_text ? String(item.comment_text) : '',
    parent_id: item.parent_id ? String(item.parent_id) : '',
    root_id: item.root_id ? String(item.root_id) : '',
    author_name: item.author_name ? String(item.author_name) : '',
    url: item.url ? String(item.url) : '',
    created_at: item.created_at ? String(item.created_at) : '',
    like_count: Number(item.like_count || 0),
    reply_count: Number(item.reply_count || 0),
    share_count: Number(item.share_count || 0),
    view_count: Number(item.view_count || 0),
    language: String(item.language || 'unknown'),
    confidence: normalizeRatio(item.confidence, 0),
    content_visibility: String(item.content_visibility || ''),
    access_scope: String(item.access_scope || ''),
    provenance_type: String(item.provenance_type || ''),
    verification_status: String(item.verification_status || ''),
    trust_score: normalizeRatio(item.trust_score, 0),
    trust_label: String(item.trust_label || ''),
    source_url_present: Boolean(item.source_url_present),
    source_url: item.source_url ? String(item.source_url) : '',
    source_platform_claim: item.source_platform_claim ? String(item.source_platform_claim) : '',
    source_capture_method: item.source_capture_method ? String(item.source_capture_method) : '',
    submitted_by_label: item.submitted_by_label ? String(item.submitted_by_label) : '',
    submitted_at: item.submitted_at ? String(item.submitted_at) : '',
    user_attestation_required: Boolean(item.user_attestation_required),
    user_attestation_text: item.user_attestation_text ? String(item.user_attestation_text) : '',
    verification_notes: Array.isArray(item.verification_notes) ? item.verification_notes.map((note) => String(note)) : [],
    duplicate_group_id: item.duplicate_group_id ? String(item.duplicate_group_id) : '',
    duplicate_count: Number(item.duplicate_count || 1),
    duplicate_group_size: Number(item.duplicate_group_size || 1),
    risk_flags: Array.isArray(item.risk_flags) ? item.risk_flags.map((flag) => String(flag)) : [],
    review_status: String(item.review_status || 'not_reviewed'),
    review_reason_codes: Array.isArray(item.review_reason_codes) ? item.review_reason_codes.map((code) => String(code)) : [],
    reviewed_at: item.reviewed_at ? String(item.reviewed_at) : '',
    reviewer_label: item.reviewer_label ? String(item.reviewer_label) : '',
    review_notes: Array.isArray(item.review_notes) ? item.review_notes.map((note) => String(note)) : [],
    review_history: Array.isArray(item.review_history) ? item.review_history.map(normalizeEvidenceReviewHistoryEntry).filter(Boolean) : [],
  }
}

function normalizeEvidenceReviewSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      total_evidence_count: 0,
      queue_count: 0,
      review_needed_count: 0,
      low_trust_count: 0,
      duplicate_group_count: 0,
      rejected_count: 0,
      approved_count: 0,
      marked_weak_count: 0,
      needs_more_source_count: 0,
      duplicate_merged_count: 0,
      queue_items: [],
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    total_evidence_count: Number(data.total_evidence_count || 0),
    queue_count: Number(data.queue_count || 0),
    review_needed_count: Number(data.review_needed_count || 0),
    low_trust_count: Number(data.low_trust_count || 0),
    duplicate_group_count: Number(data.duplicate_group_count || 0),
    rejected_count: Number(data.rejected_count || 0),
    approved_count: Number(data.approved_count || 0),
    marked_weak_count: Number(data.marked_weak_count || 0),
    needs_more_source_count: Number(data.needs_more_source_count || 0),
    duplicate_merged_count: Number(data.duplicate_merged_count || 0),
    queue_items: Array.isArray(data.queue_items) ? data.queue_items.map(normalizeEvidenceReviewQueueItem).filter(Boolean) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceReviewQueueItem(item) {
  if (!item || typeof item !== 'object') return null
  return {
    evidence_id: String(item.evidence_id || ''),
    case_id: item.case_id ? String(item.case_id) : '',
    platform: String(item.platform || ''),
    evidence_type: String(item.evidence_type || ''),
    title: item.title ? String(item.title) : '',
    body_text_preview: item.body_text_preview ? String(item.body_text_preview) : '',
    comment_text_preview: item.comment_text_preview ? String(item.comment_text_preview) : '',
    url: item.url ? String(item.url) : '',
    provenance_type: String(item.provenance_type || ''),
    verification_status: String(item.verification_status || ''),
    trust_label: String(item.trust_label || ''),
    trust_score: normalizeRatio(item.trust_score, 0),
    risk_flags: Array.isArray(item.risk_flags) ? item.risk_flags.map((flag) => String(flag)) : [],
    duplicate_group_id: item.duplicate_group_id ? String(item.duplicate_group_id) : '',
    duplicate_count: Number(item.duplicate_count || 1),
    source_url_present: Boolean(item.source_url_present),
    user_attestation_required: Boolean(item.user_attestation_required),
    user_attestation_text: item.user_attestation_text ? String(item.user_attestation_text) : '',
    review_status: String(item.review_status || 'not_reviewed'),
    review_reason_codes: Array.isArray(item.review_reason_codes) ? item.review_reason_codes.map((code) => String(code)) : [],
    created_at: item.created_at ? String(item.created_at) : '',
    submitted_at: item.submitted_at ? String(item.submitted_at) : '',
  }
}

function normalizeEvidenceReviewDecisionResult(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      evidence_id: '',
      decision: '',
      review_status: '',
      evidence_item: null,
      summary: normalizeEvidenceReviewSummary(null),
      history_entry: null,
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    evidence_id: String(data.evidence_id || ''),
    decision: String(data.decision || ''),
    review_status: String(data.review_status || ''),
    evidence_item: normalizeEvidenceItem(data.evidence_item),
    summary: normalizeEvidenceReviewSummary(data.summary),
    history_entry: normalizeEvidenceReviewHistoryEntry(data.history_entry),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceReviewHistoryEntry(entry) {
  if (!entry || typeof entry !== 'object') return null
  return {
    review_event_id: String(entry.review_event_id || ''),
    evidence_id: String(entry.evidence_id || ''),
    case_id: entry.case_id ? String(entry.case_id) : '',
    previous_review_status: String(entry.previous_review_status || 'not_reviewed'),
    new_review_status: String(entry.new_review_status || 'not_reviewed'),
    decision: String(entry.decision || ''),
    reason_code: entry.reason_code ? String(entry.reason_code) : '',
    reviewer_label: entry.reviewer_label ? String(entry.reviewer_label) : '',
    reviewed_at: entry.reviewed_at ? String(entry.reviewed_at) : '',
    note: entry.note ? String(entry.note) : '',
    trust_label_before: String(entry.trust_label_before || ''),
    trust_label_after: String(entry.trust_label_after || ''),
    verification_status_before: String(entry.verification_status_before || ''),
    verification_status_after: String(entry.verification_status_after || ''),
    analysis_effect: String(entry.analysis_effect || ''),
    safe_mode: entry.safe_mode && typeof entry.safe_mode === 'object' ? normalizeBooleanMap(entry.safe_mode) : {},
  }
}

function normalizeEvidenceReviewTimeline(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      evidence_id: '',
      entries: [],
      total_review_events: 0,
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    evidence_id: data.evidence_id ? String(data.evidence_id) : '',
    entries: Array.isArray(data.entries) ? data.entries.map(normalizeEvidenceReviewHistoryEntry).filter(Boolean) : [],
    total_review_events: Number(data.total_review_events || 0),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceReviewAuditSummary(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      total_review_events: 0,
      approved_count: 0,
      rejected_count: 0,
      marked_weak_count: 0,
      needs_more_source_count: 0,
      duplicate_merged_count: 0,
      reset_count: 0,
      latest_reviewed_at: '',
      evidence_with_history_count: 0,
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    total_review_events: Number(data.total_review_events || 0),
    approved_count: Number(data.approved_count || 0),
    rejected_count: Number(data.rejected_count || 0),
    marked_weak_count: Number(data.marked_weak_count || 0),
    needs_more_source_count: Number(data.needs_more_source_count || 0),
    duplicate_merged_count: Number(data.duplicate_merged_count || 0),
    reset_count: Number(data.reset_count || 0),
    latest_reviewed_at: data.latest_reviewed_at ? String(data.latest_reviewed_at) : '',
    evidence_with_history_count: Number(data.evidence_with_history_count || 0),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceImportPreview(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      filename: '',
      status: 'empty',
      detected_format: '',
      detected_columns: [],
      column_mapping: {},
      total_rows: 0,
      valid_row_count: 0,
      duplicate_row_count: 0,
      skipped_row_count: 0,
      preview_rows: [],
      warnings: [],
      safe_mode: {},
    }
  }
  return {
    ...data,
    case_id: String(data.case_id || ''),
    filename: String(data.filename || ''),
    status: String(data.status || 'empty'),
    detected_format: data.detected_format ? String(data.detected_format) : '',
    detected_columns: Array.isArray(data.detected_columns) ? data.detected_columns.map((item) => String(item)) : [],
    column_mapping: normalizeStringMap(data.column_mapping),
    total_rows: Number(data.total_rows || 0),
    valid_row_count: Number(data.valid_row_count || 0),
    duplicate_row_count: Number(data.duplicate_row_count || 0),
    skipped_row_count: Number(data.skipped_row_count || 0),
    preview_rows: Array.isArray(data.preview_rows) ? data.preview_rows.map(normalizeEvidenceImportRow).filter(Boolean) : [],
    warnings: Array.isArray(data.warnings) ? data.warnings.map(normalizeEvidenceImportWarning).filter(Boolean) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceImportCommit(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      filename: '',
      status: 'empty',
      imported_count: 0,
      total_evidence_item_count: 0,
      duplicate_row_count: 0,
      skipped_row_count: 0,
      evidence_items: [],
      source_distribution: {},
      evidence_type_counts: {},
      warnings: [],
      safe_mode: {},
    }
  }
  return {
    ...data,
    case_id: String(data.case_id || ''),
    filename: String(data.filename || ''),
    status: String(data.status || 'empty'),
    detected_format: data.detected_format ? String(data.detected_format) : '',
    imported_count: Number(data.imported_count || 0),
    total_evidence_item_count: Number(data.total_evidence_item_count || 0),
    duplicate_row_count: Number(data.duplicate_row_count || 0),
    skipped_row_count: Number(data.skipped_row_count || 0),
    evidence_items: Array.isArray(data.evidence_items) ? data.evidence_items.map(normalizeEvidenceItem).filter(Boolean) : [],
    source_distribution: normalizeNumberMap(data.source_distribution),
    evidence_type_counts: normalizeNumberMap(data.evidence_type_counts),
    warnings: Array.isArray(data.warnings) ? data.warnings.map(normalizeEvidenceImportWarning).filter(Boolean) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEvidenceImportRow(row) {
  if (!row || typeof row !== 'object') return null
  return {
    row_number: Number(row.row_number || 0),
    evidence_id: String(row.evidence_id || ''),
    platform: String(row.platform || ''),
    source_type: String(row.source_type || ''),
    acquisition_mode: String(row.acquisition_mode || ''),
    evidence_type: String(row.evidence_type || ''),
    title: row.title ? String(row.title) : '',
    body_text: row.body_text ? String(row.body_text) : '',
    comment_text: row.comment_text ? String(row.comment_text) : '',
    author_name: row.author_name ? String(row.author_name) : '',
    url: row.url ? String(row.url) : '',
    created_at: row.created_at ? String(row.created_at) : '',
    like_count: Number(row.like_count || 0),
    reply_count: Number(row.reply_count || 0),
    share_count: Number(row.share_count || 0),
    view_count: Number(row.view_count || 0),
    provenance_type: String(row.provenance_type || ''),
    verification_status: String(row.verification_status || ''),
    trust_label: String(row.trust_label || ''),
    risk_flags: Array.isArray(row.risk_flags) ? row.risk_flags.map((flag) => String(flag)) : [],
    warnings: Array.isArray(row.warnings) ? row.warnings.map(normalizeEvidenceImportWarning).filter(Boolean) : [],
  }
}

function normalizeEvidenceImportWarning(warning) {
  if (!warning || typeof warning !== 'object') return null
  return {
    row_number: warning.row_number === null || warning.row_number === undefined ? null : Number(warning.row_number),
    field: warning.field ? String(warning.field) : '',
    code: String(warning.code || ''),
    message: String(warning.message || ''),
    severity: String(warning.severity || 'warning'),
  }
}

function normalizeSourceCatalog(data) {
  if (!data || typeof data !== 'object') {
    return {
      categories: [],
      total_categories: 0,
      total_sources: 0,
      safe_mode: {},
    }
  }
  return {
    categories: Array.isArray(data.categories)
      ? data.categories.map(normalizeSourceCatalogCategory).filter(Boolean)
      : [],
    total_categories: Number(data.total_categories || 0),
    total_sources: Number(data.total_sources || 0),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeSourceCatalogCategory(category) {
  if (!category || typeof category !== 'object') return null
  return {
    category_id: String(category.category_id || ''),
    display_name: String(category.display_name || ''),
    description: String(category.description || ''),
    sources: Array.isArray(category.sources)
      ? category.sources.map(normalizeSourceCatalogEntry).filter(Boolean)
      : [],
  }
}

function normalizeSourceCatalogEntry(source) {
  if (!source || typeof source !== 'object') return null
  return {
    source_id: String(source.source_id || ''),
    display_name: String(source.display_name || ''),
    category: String(source.category || ''),
    feasibility_status: String(source.feasibility_status || ''),
    acquisition_modes: Array.isArray(source.acquisition_modes)
      ? source.acquisition_modes.map((item) => String(item))
      : [],
    allowed_data_types: Array.isArray(source.allowed_data_types)
      ? source.allowed_data_types.map((item) => String(item))
      : [],
    forbidden_data_types: Array.isArray(source.forbidden_data_types)
      ? source.forbidden_data_types.map((item) => String(item))
      : [],
    current_status: String(source.current_status || ''),
    compliance_notes: String(source.compliance_notes || ''),
    next_action: String(source.next_action || ''),
    priority: String(source.priority || ''),
  }
}

function normalizeSearchDiscoveryStatus(data) {
  if (!data || typeof data !== 'object') {
    return {
      status: 'planning_mock_only',
      provider_statuses: [],
      review_flow: [],
      next_actions: [],
      safe_mode: {},
    }
  }
  return {
    status: String(data.status || 'planning_mock_only'),
    provider_statuses: Array.isArray(data.provider_statuses)
      ? data.provider_statuses.map(normalizeSearchDiscoveryProvider).filter(Boolean)
      : [],
    review_flow: Array.isArray(data.review_flow) ? data.review_flow.map((item) => String(item)) : [],
    next_actions: Array.isArray(data.next_actions) ? data.next_actions.map((item) => String(item)) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeSearchDiscoveryProvider(provider) {
  if (!provider || typeof provider !== 'object') return null
  return {
    provider_id: String(provider.provider_id || ''),
    display_name: String(provider.display_name || ''),
    provider_class: String(provider.provider_class || ''),
    status: String(provider.status || ''),
    allowed_use: String(provider.allowed_use || ''),
    forbidden_use: String(provider.forbidden_use || ''),
    data_returned: Array.isArray(provider.data_returned)
      ? provider.data_returned.map((item) => String(item))
      : [],
    full_content_available: Boolean(provider.full_content_available),
    requires_api_key: Boolean(provider.requires_api_key),
    credential_present: Boolean(provider.credential_present),
    user_review_required: provider.user_review_required !== false,
    current_sentigraph_status: String(provider.current_sentigraph_status || ''),
    next_action: String(provider.next_action || ''),
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
  const provider = String(data.provider || '')
  const operation = String(data.operation || '')
  const timestamp = data.timestamp ? String(data.timestamp) : ''
  const inputChars = Number(data.input_chars || 0)
  const outputChars = Number(data.output_chars || 0)
  const estimatedInputTokens = Number(data.estimated_input_tokens || 0)
  const estimatedOutputTokens = Number(data.estimated_output_tokens || 0)
  const success = data.success !== false
  const failureCategory = data.failure_category ? String(data.failure_category) : null

  return {
    record_key: [
      provider,
      operation,
      timestamp,
      inputChars,
      outputChars,
      estimatedInputTokens,
      estimatedOutputTokens,
      success ? 'ok' : 'failed',
      failureCategory || 'none',
    ].join('-'),
    provider,
    operation,
    input_chars: inputChars,
    output_chars: outputChars,
    estimated_input_tokens: estimatedInputTokens,
    estimated_output_tokens: estimatedOutputTokens,
    timestamp,
    success,
    failure_category: failureCategory,
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
    visibility_intervention: normalizeVisibilityIntervention(data.visibility_intervention),
  }
}

function normalizeVisibilityIntervention(data) {
  if (!data || typeof data !== 'object') return null
  return {
    intervention_type: String(data.intervention_type || 'content_removal_with_explanation'),
    target_message_reach: normalizeRatio(data.target_message_reach, 0.82),
    current_visibility: normalizeRatio(data.current_visibility, 1),
    removal_time: normalizeRatio(data.removal_time, 0.35),
    residual_copies: normalizeRatio(data.residual_copies, 0.18),
    screenshot_probability: normalizeRatio(data.screenshot_probability, 0.22),
    repost_migration_probability: normalizeRatio(data.repost_migration_probability, 0.18),
    perceived_suppression: normalizeRatio(data.perceived_suppression, 0.3),
    policy_violation_clarity: normalizeRatio(data.policy_violation_clarity, 0.78),
    legitimacy_of_removal: normalizeRatio(data.legitimacy_of_removal, 0.72),
    public_explanation_quality: normalizeRatio(data.public_explanation_quality, 0.76),
    reactance_amplification: normalizeRatio(data.reactance_amplification, 0.32),
    martyr_effect: normalizeRatio(data.martyr_effect, 0.2),
    cross_platform_spillover: normalizeRatio(data.cross_platform_spillover, 0.22),
    neutral_audience_negative_shift: normalizeRatio(data.neutral_audience_negative_shift, 0.1),
    hard_opposition_negative_shift: normalizeRatio(data.hard_opposition_negative_shift, 0.22),
    policy_basis: String(data.policy_basis || 'platform_policy'),
    authorization_source: String(data.authorization_source || 'platform_policy'),
    public_explanation_required: data.public_explanation_required !== false,
  }
}

function normalizeVisibilityInterventionResult(data) {
  if (!data || typeof data !== 'object') return null
  return {
    intervention_type: String(data.intervention_type || 'content_removal_with_explanation'),
    exposure_reduction: normalizeBounded(data.exposure_reduction, 0, 100, 0),
    backlash_cost: normalizeBounded(data.backlash_cost, 0, 100, 0),
    trust_loss: normalizeBounded(data.trust_loss, 0, 100, 0),
    spillover_risk: normalizeBounded(data.spillover_risk, 0, 100, 0),
    net_risk_change: normalizeBounded(data.net_risk_change, 0, 100, 0),
    removal_legitimacy_score: normalizeBounded(data.removal_legitimacy_score, 0, 100, 0),
    public_explanation_quality_score: normalizeBounded(data.public_explanation_quality_score, 0, 100, 0),
    neutral_audience_impact: normalizeBounded(data.neutral_audience_impact, 0, 100, 0),
    opposition_group_impact: normalizeBounded(data.opposition_group_impact, 0, 100, 0),
    recommendation: String(data.recommendation || 'conditional_human_review'),
    explanation: String(data.explanation || ''),
    audience_impact:
      data.audience_impact && typeof data.audience_impact === 'object' && !Array.isArray(data.audience_impact)
        ? {
            neutral_audience_impact: normalizeBounded(data.audience_impact.neutral_audience_impact, 0, 100, 0),
            opposition_group_impact: normalizeBounded(data.audience_impact.opposition_group_impact, 0, 100, 0),
            neutral_audience_negative_shift: normalizeRatio(data.audience_impact.neutral_audience_negative_shift, 0),
            hard_opposition_negative_shift: normalizeRatio(data.audience_impact.hard_opposition_negative_shift, 0),
            high_concern: Boolean(data.audience_impact.high_concern),
            explanation: String(data.audience_impact.explanation || ''),
          }
        : null,
    human_review_required: data.human_review_required !== false,
    aggregate_level_only: data.aggregate_level_only !== false,
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
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
      visibility_intervention_result: null,
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
    visibility_intervention_result: normalizeVisibilityInterventionResult(data.visibility_intervention_result),
    key_findings: Array.isArray(data.key_findings)
      ? data.key_findings.map((finding) => String(finding))
      : [],
    recommended_interpretation: String(data.recommended_interpretation || ''),
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizeSimulationStrategyReportResponse(data) {
  const report = data?.report && typeof data.report === 'object' ? data.report : {}
  return {
    markdown: typeof data?.markdown === 'string' ? data.markdown : '',
    report: {
      title: String(report.title || 'Simulation Lab Strategy Report'),
      generated_at: report.generated_at ? String(report.generated_at) : null,
      scenario_name: String(report.scenario_name || ''),
      simulation_mode: String(report.simulation_mode || 'single'),
      intervention_a: String(report.intervention_a || ''),
      intervention_b: report.intervention_b ? String(report.intervention_b) : '',
      summary: String(report.summary || ''),
      ethical_risk_flags: Array.isArray(report.ethical_risk_flags)
        ? report.ethical_risk_flags.map((flag) => String(flag))
        : [],
      human_review_required: Boolean(report.human_review_required ?? true),
      limitations: Array.isArray(report.limitations) ? report.limitations.map((item) => String(item)) : [],
    },
    safe_mode: data?.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeCaseSimulationInitialization(data) {
  if (!data || typeof data !== 'object') {
    return {
      case_id: '',
      status: 'partial',
      generated_at: null,
      model_version: 'case_to_simulation_initializer_v1',
      event_frame: normalizeEventFrame(null),
      audience_segments: [],
      persona_clusters: [],
      frame_gap_analysis: normalizeFrameGapAnalysis(null),
      strategy_implications: [],
      simulation_scenario: normalizeSimulationScenario(null),
      warnings: [],
      safe_mode: {},
    }
  }
  return {
    case_id: String(data.case_id || ''),
    status: String(data.status || 'partial'),
    generated_at: data.generated_at ? String(data.generated_at) : null,
    model_version: String(data.model_version || 'case_to_simulation_initializer_v1'),
    event_frame: normalizeEventFrame(data.event_frame),
    audience_segments: Array.isArray(data.audience_segments)
      ? data.audience_segments.map(normalizeAudienceSegment).filter(Boolean)
      : [],
    persona_clusters: Array.isArray(data.persona_clusters)
      ? data.persona_clusters.map(normalizePersonaCluster).filter(Boolean)
      : [],
    frame_gap_analysis: normalizeFrameGapAnalysis(data.frame_gap_analysis),
    strategy_implications: Array.isArray(data.strategy_implications)
      ? data.strategy_implications.map(normalizeStrategyImplication).filter(Boolean)
      : [],
    simulation_scenario: normalizeSimulationScenario(data.simulation_scenario),
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
    safe_mode: data.safe_mode && typeof data.safe_mode === 'object' ? normalizeBooleanMap(data.safe_mode) : {},
  }
}

function normalizeEventFrame(data) {
  if (!data || typeof data !== 'object') {
    return {
      event_frame_id: '',
      case_id: '',
      event_title: '',
      event_summary: '',
      sub_issues: [],
      observed_frame_profile: {},
      baseline_public_profile: {},
      frame_gap_analysis: normalizeFrameGapAnalysis(null),
      strategy_implications: [],
      initialization_hints: {},
      uncertainty_label: 'medium',
      uncertainty_reasons: [],
      assumption_log: {},
    }
  }
  return {
    event_frame_id: String(data.event_frame_id || ''),
    case_id: data.case_id ? String(data.case_id) : '',
    event_title: String(data.event_title || ''),
    event_summary: String(data.event_summary || ''),
    generated_at: data.generated_at ? String(data.generated_at) : null,
    source_mode: String(data.source_mode || 'aggregate_case_output'),
    data_safety: data.data_safety && typeof data.data_safety === 'object' ? normalizeBooleanMap(data.data_safety) : {},
    sub_issues: Array.isArray(data.sub_issues) ? data.sub_issues.map(normalizeSubIssue).filter(Boolean) : [],
    observed_frame_profile:
      data.observed_frame_profile && typeof data.observed_frame_profile === 'object'
        ? {
            observed_comment_count: Number(data.observed_frame_profile.observed_comment_count || 0),
            observed_platforms: Array.isArray(data.observed_frame_profile.observed_platforms)
              ? data.observed_frame_profile.observed_platforms.map((platform) => String(platform))
              : [],
            sentiment_distribution: normalizeNumberMap(data.observed_frame_profile.sentiment_distribution),
            manipulation_signal_score: Number(data.observed_frame_profile.manipulation_signal_score || 0),
            real_crisis_signal_score: Number(data.observed_frame_profile.real_crisis_signal_score || 0),
            harm_salience: normalizeRatio(data.observed_frame_profile.harm_salience, 0),
            loss_sensitivity: normalizeRatio(data.observed_frame_profile.loss_sensitivity, 0),
            moral_outrage_sensitivity: normalizeRatio(data.observed_frame_profile.moral_outrage_sensitivity, 0),
            crisis_legitimacy_pressure: normalizeRatio(data.observed_frame_profile.crisis_legitimacy_pressure, 0),
            uncertainty_label: String(data.observed_frame_profile.uncertainty_label || 'medium'),
            confidence_warnings: Array.isArray(data.observed_frame_profile.confidence_warnings)
              ? data.observed_frame_profile.confidence_warnings.map((warning) => String(warning))
              : [],
          }
        : {},
    baseline_public_profile:
      data.baseline_public_profile && typeof data.baseline_public_profile === 'object'
        ? {
            baseline_id: String(data.baseline_public_profile.baseline_id || ''),
            event_category: String(data.baseline_public_profile.event_category || 'unknown'),
            expected_average_reaction: normalizeSignedScore(data.baseline_public_profile.expected_average_reaction),
            expected_loss_sensitivity: normalizeRatio(data.baseline_public_profile.expected_loss_sensitivity, 0),
            expected_authority_trust: normalizeRatio(data.baseline_public_profile.expected_authority_trust, 0),
            limitations: Array.isArray(data.baseline_public_profile.limitations)
              ? data.baseline_public_profile.limitations.map((item) => String(item))
              : [],
          }
        : {},
    frame_gap_analysis: normalizeFrameGapAnalysis(data.frame_gap_analysis),
    strategy_implications: Array.isArray(data.strategy_implications)
      ? data.strategy_implications.map(normalizeStrategyImplication).filter(Boolean)
      : [],
    initialization_hints:
      data.initialization_hints && typeof data.initialization_hints === 'object' && !Array.isArray(data.initialization_hints)
        ? data.initialization_hints
        : {},
    uncertainty_label: String(data.uncertainty_label || 'medium'),
    uncertainty_reasons: Array.isArray(data.uncertainty_reasons)
      ? data.uncertainty_reasons.map((reason) => String(reason))
      : [],
    assumption_log: data.assumption_log && typeof data.assumption_log === 'object' ? data.assumption_log : {},
  }
}

function normalizeSubIssue(data) {
  if (!data || typeof data !== 'object') return null
  return {
    sub_issue_id: String(data.sub_issue_id || ''),
    category: String(data.category || 'unknown'),
    title: String(data.title || ''),
    summary: String(data.summary || ''),
    observed_volume: normalizeRatio(data.observed_volume, 0),
    negative_ratio: normalizeRatio(data.negative_ratio, 0),
    topic_risk_score: normalizeBounded(data.topic_risk_score, 0, 100, 0),
    risk_score: normalizeBounded(data.risk_score ?? data.topic_risk_score, 0, 100, 0),
    risk_level: String(data.risk_level || 'low'),
    evidence_quality: String(data.evidence_quality || 'mixed'),
    evidence_examples: Array.isArray(data.evidence_examples)
      ? data.evidence_examples.map((example) => String(example))
      : [],
  }
}

function normalizeAudienceSegment(data) {
  if (!data || typeof data !== 'object') return null
  return {
    segment_id: String(data.segment_id || ''),
    label: String(data.label || ''),
    segment_type: String(data.segment_type || ''),
    proportion: normalizeRatio(data.proportion, 0),
    color_hint: String(data.color_hint || 'gray'),
    average_attention_level: normalizeRatio(data.average_attention_level, 0),
    opinion_baseline: normalizeSignedScore(data.opinion_baseline),
    action_threshold: normalizeRatio(data.action_threshold, 0),
    influence_proxy: normalizeBounded(data.influence_proxy, 0, 100, 0),
    bridge_score: normalizeRatio(data.bridge_score, 0),
    warnings: Array.isArray(data.warnings) ? data.warnings.map((warning) => String(warning)) : [],
  }
}

function normalizePersonaCluster(data) {
  if (!data || typeof data !== 'object') return null
  return {
    cluster_id: String(data.cluster_id || ''),
    segment_id: String(data.segment_id || ''),
    label: String(data.label || ''),
    confirmation_bias: normalizeRatio(data.confirmation_bias, 0),
    authority_trust: normalizeRatio(data.authority_trust, 0),
    reactance: normalizeRatio(data.reactance, 0),
    negativity_weight: normalizeRatio(data.negativity_weight, 0),
    loss_sensitivity: normalizeRatio(data.loss_sensitivity, 0),
    moral_outrage_sensitivity: normalizeRatio(data.moral_outrage_sensitivity, 0),
    harm_salience: normalizeRatio(data.harm_salience, 0),
    crisis_legitimacy_pressure: normalizeRatio(data.crisis_legitimacy_pressure, 0),
    no_individual_profile: data.no_individual_profile !== false,
  }
}

function normalizeFrameGapAnalysis(data) {
  if (!data || typeof data !== 'object') {
    return {
      primary_classification: 'insufficient_data',
      secondary_classifications: [],
      gap_scores: {},
      summary: '',
      strategy_cautions: [],
      monitoring_recommendations: [],
      uncertainty_label: 'medium',
    }
  }
  return {
    analysis_id: String(data.analysis_id || ''),
    primary_classification: String(data.primary_classification || 'insufficient_data'),
    secondary_classifications: Array.isArray(data.secondary_classifications)
      ? data.secondary_classifications.map((item) => String(item))
      : [],
    gap_scores: normalizeNumberMap(data.gap_scores),
    summary: String(data.summary || ''),
    strategy_cautions: Array.isArray(data.strategy_cautions)
      ? data.strategy_cautions.map((item) => String(item))
      : [],
    monitoring_recommendations: Array.isArray(data.monitoring_recommendations)
      ? data.monitoring_recommendations.map((item) => String(item))
      : [],
    uncertainty_label: String(data.uncertainty_label || 'medium'),
    aggregate_only: data.aggregate_only !== false,
    no_individual_targeting: data.no_individual_targeting !== false,
  }
}

function normalizeStrategyImplication(data) {
  if (!data || typeof data !== 'object') return null
  return {
    implication_id: String(data.implication_id || ''),
    frame_gap_classification: String(data.frame_gap_classification || ''),
    recommended_simulation_options: Array.isArray(data.recommended_simulation_options)
      ? data.recommended_simulation_options.map((item) => String(item))
      : [],
    discouraged_options: Array.isArray(data.discouraged_options)
      ? data.discouraged_options.map((item) => String(item))
      : [],
    rationale: String(data.rationale || ''),
    human_review_required: data.human_review_required !== false,
    confidence_label: String(data.confidence_label || 'medium'),
    safety_warnings: Array.isArray(data.safety_warnings)
      ? data.safety_warnings.map((warning) => String(warning))
      : [],
  }
}

function normalizeNumberMap(data) {
  if (!data || typeof data !== 'object' || Array.isArray(data)) return {}
  return Object.fromEntries(
    Object.entries(data).map(([key, value]) => [
      String(key),
      Number.isFinite(Number(value)) ? Number(value) : 0,
    ]),
  )
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
    visibility_intervention_result: normalizeVisibilityInterventionResult(data.visibility_intervention_result),
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

function normalizeSafeObject(value) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return {}
  return Object.fromEntries(
    Object.entries(value).map(([key, mapValue]) => {
      if (mapValue === null || mapValue === undefined) return [String(key), '']
      if (typeof mapValue === 'boolean' || typeof mapValue === 'number' || typeof mapValue === 'string') {
        return [String(key), mapValue]
      }
      return [String(key), JSON.stringify(mapValue)]
    }),
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
