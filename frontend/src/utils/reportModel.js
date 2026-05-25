const DEFAULT_REPORT_LANGUAGE = 'zh-CN'
const DEFAULT_RISK_MODEL_VERSION = 'v1_static_mvp'

export function buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization }) {
  const normalizedReport = getNormalizedReport(summary, recommendation)
  const reportLanguage =
    normalizedReport?.report_language ||
    summary?.report_language ||
    recommendation?.report_language ||
    DEFAULT_REPORT_LANGUAGE
  const riskLevel = normalizedReport?.risk_level ?? visualization?.risk_level ?? analysis?.risk_level ?? analysis?.risk?.risk_level ?? 'low'
  const keyFindings = firstNonEmpty(
    normalizeStringArray(normalizedReport?.key_findings),
    normalizeStringArray(summary?.key_findings),
    normalizeStringArray(recommendation?.key_findings),
  )
  const recommendationRisks = normalizeStringArray(recommendation?.main_risks)
  const normalizedRiskFactors = normalizeStringArray(normalizedReport?.main_risk_factors)
  const normalizedBotSignals = normalizeStringArray(normalizedReport?.suspected_bot_signals)
  const summaryRiskFactors = keyFindings.filter((finding) => !isNegativeTopicFinding(finding) && !isBotSignal(finding))
  const recommendationRiskFactors = recommendationRisks.filter((risk) => !isBotSignal(risk))
  const topicFindings = keyFindings
    .filter(isNegativeTopicFinding)
    .map((finding) => finding.replace('Negative topic:', '').replace('负面议题：', '').trim())
  const topNegativeTopics = firstNonEmpty(
    normalizeStringArray(normalizedReport?.top_negative_topics),
    normalizeStringArray(summary?.top_negative_topics),
    normalizeStringArray(recommendation?.top_negative_topics),
    topicFindings,
    buildFallbackNegativeTopics(analysis?.topics, visualization?.topic_clusters),
  )
  const botSignals = [...keyFindings, ...recommendationRisks].filter(isBotSignal)
  const botImpact =
    visualization?.bot_impact?.suspected_bot_comment_ratio ??
    analysis?.bot_score?.suspected_bot_comment_ratio ??
    0
  const fallbackBotSignals =
    botImpact > 0 ? [`疑似机器人或重复话术评论占比为 ${formatPercentValue(botImpact)}。`] : []
  const suspectedBotSignals = firstNonEmpty(normalizedBotSignals, botSignals, fallbackBotSignals)
  const mainRiskFactors = firstNonEmpty(
    normalizedRiskFactors,
    summaryRiskFactors,
    recommendationRiskFactors,
    keyFindings,
    recommendationRisks,
  )
  const representativeComments = firstNonEmpty(
    normalizeStringArray(normalizedReport?.representative_comments),
    normalizeStringArray(summary?.representative_comments),
    normalizeStringArray(recommendation?.representative_comments),
    extractRepresentativeComments(analysis?.topics),
  )
  const recommendedActions = firstNonEmpty(
    normalizeStringArray(recommendation?.recommended_actions),
    normalizeStringArray(summary?.recommended_actions),
    normalizeStringArray(normalizedReport?.recommended_actions),
  )
  const suggestedPublicResponse =
    recommendation?.suggested_public_response ||
    summary?.suggested_public_response ||
    normalizedReport?.suggested_public_response ||
    recommendation?.suggested_response ||
    ''
  const responseTopicRisks = firstNonEmptyObjects(
    normalizeTopicRisks(normalizedReport?.topic_risks),
    normalizeTopicRisks(summary?.topic_risks),
    normalizeTopicRisks(recommendation?.topic_risks),
    normalizeTopicRisks(visualization?.topic_risks),
    normalizeTopicRisks(analysis?.topic_risks),
  )
  const topicRisks = firstNonEmptyObjects(
    responseTopicRisks,
    buildFallbackTopicRisks(analysis?.topics, visualization?.topic_clusters),
  )
  const topRiskTopics = firstNonEmptyObjects(
    normalizeTopicRisks(normalizedReport?.top_risk_topics),
    normalizeTopicRisks(summary?.top_risk_topics),
    normalizeTopicRisks(recommendation?.top_risk_topics),
    normalizeTopicRisks(visualization?.top_risk_topics),
    normalizeTopicRisks(analysis?.top_risk_topics),
    topicRisks.slice(0, 3),
  )
  const realCrisisRisk = firstDefinedNumber(
    normalizedReport?.real_crisis_risk,
    summary?.real_crisis_risk,
    recommendation?.real_crisis_risk,
    visualization?.real_crisis_risk,
    analysis?.real_crisis_risk,
  )
  const manipulationRisk = firstDefinedNumber(
    normalizedReport?.manipulation_risk,
    summary?.manipulation_risk,
    recommendation?.manipulation_risk,
    visualization?.manipulation_risk,
    analysis?.manipulation_risk,
  )
  const riskExplanation =
    normalizedReport?.risk_explanation ||
    summary?.risk_explanation ||
    recommendation?.risk_explanation ||
    visualization?.risk_explanation ||
    analysis?.risk_explanation ||
    topRiskTopics[0]?.explanation ||
    ''

  return {
    projectId: normalizedReport?.project_id || summary?.project_id || recommendation?.project_id || analysis?.project_id || '',
    overallSummary: normalizedReport?.overall_summary || summary?.summary || recommendation?.summary || analysis?.summary || '',
    keyFindings,
    mainRiskFactors,
    topNegativeTopics,
    topicRisks,
    topRiskTopics,
    representativeComments,
    suspectedBotSignals,
    recommendedActions,
    suggestedPublicResponse,
    sentimentExplanation: buildSentimentExplanation(analysis, visualization),
    botSignalExplanation: buildBotSignalExplanation(suspectedBotSignals, botImpact),
    riskScore:
      normalizedReport?.risk_score ??
      visualization?.risk_score ??
      analysis?.overall_risk ??
      analysis?.risk_score ??
      analysis?.risk?.risk_score ??
      0,
    riskLevel,
    riskLevelLabel: normalizedReport?.risk_level_label || getRiskLevelLabel(riskLevel, reportLanguage),
    riskModelVersion:
      normalizedReport?.risk_model_version ||
      summary?.risk_model_version ||
      recommendation?.risk_model_version ||
      visualization?.risk_model_version ||
      analysis?.risk_model_version ||
      DEFAULT_RISK_MODEL_VERSION,
    maxTopicRisk: firstDefinedNumber(
      normalizedReport?.max_topic_risk,
      summary?.max_topic_risk,
      recommendation?.max_topic_risk,
      visualization?.max_topic_risk,
      analysis?.max_topic_risk,
    ),
    averageTopicRisk: firstDefinedNumber(
      normalizedReport?.average_topic_risk,
      summary?.average_topic_risk,
      recommendation?.average_topic_risk,
      visualization?.average_topic_risk,
      analysis?.average_topic_risk,
    ),
    overallRisk: firstDefinedNumber(
      normalizedReport?.overall_risk,
      summary?.overall_risk,
      recommendation?.overall_risk,
      visualization?.overall_risk,
      analysis?.overall_risk,
    ),
    realCrisisRisk,
    manipulationRisk,
    riskExplanation,
    reportLanguage,
    analysisInputSource:
      normalizedReport?.analysis_input_source ||
      summary?.analysis_input_source ||
      recommendation?.analysis_input_source ||
      analysis?.analysis_input_source ||
      '',
    generatedFromMockPipeline: Boolean(normalizedReport?.generated_from_mock_pipeline),
    hasSummaryData: Boolean(summary),
    hasRecommendationData: Boolean(recommendation),
  }
}

export function arrayOrEmpty(value) {
  return Array.isArray(value) ? value : []
}

export function normalizeStringArray(value) {
  return arrayOrEmpty(value)
    .filter((item) => typeof item === 'string')
    .map((item) => item.trim())
    .filter(Boolean)
}

export function hasReportContent(report) {
  if (!report) return false
  return Boolean(
    report.overallSummary ||
      report.keyFindings.length ||
      report.mainRiskFactors.length ||
      report.topNegativeTopics.length ||
      report.topicRisks.length ||
      report.topRiskTopics.length ||
      report.representativeComments.length ||
      report.suspectedBotSignals.length ||
      report.recommendedActions.length ||
      report.suggestedPublicResponse,
  )
}

function buildFallbackNegativeTopics(topics, visualizationTopics) {
  const analysisTopics = arrayOrEmpty(topics)
    .filter((topic) => Number(topic.average_sentiment_score) < 0)
    .map(
      (topic) =>
        `${topic.topic}: ${topic.comment_count} comments, average sentiment ${formatFixed(
          topic.average_sentiment_score,
        )}`,
    )
  if (analysisTopics.length) return analysisTopics

  return arrayOrEmpty(visualizationTopics)
    .filter((topic) => Number(topic.sentiment_score) < 0)
    .map(
      (topic) =>
        `${topic.name}: ${topic.value} comment(s), average sentiment ${formatFixed(topic.sentiment_score)}`,
    )
}

function buildFallbackTopicRisks(topics, visualizationTopics) {
  const analysisRisks = arrayOrEmpty(topics).map((topic, index) => {
    const sentimentScore = Number(topic.average_sentiment_score) || 0
    const commentCount = Number(topic.comment_count) || 0
    const riskScore = estimateTopicRiskScore(sentimentScore, commentCount)
    return {
      clusterId: topic.cluster_id || `topic_${index + 1}`,
      topicId: topic.cluster_id || `topic_${index + 1}`,
      topic: topic.topic || '未命名话题',
      commentCount,
      negativeRatio: sentimentScore < 0 ? Math.min(1, Math.abs(sentimentScore)) : 0,
      averageSentimentScore: sentimentScore,
      negSeverity: sentimentScore < 0 ? Math.min(1, Math.abs(sentimentScore)) : 0,
      spreadSignal: Math.min(1, Math.log10(Math.max(1, commentCount)) / 2),
      controversySignal: 0,
      botSignal: 0,
      influenceProxy: Math.min(1, Math.log10(Math.max(1, commentCount)) / 2),
      riskScore,
      riskLevel: getRiskLevelFromScore(riskScore),
      explanation: topic.summary || `平均情绪 ${formatFixed(sentimentScore)}，评论数 ${commentCount}。`,
    }
  })

  if (analysisRisks.length) {
    return analysisRisks.sort((left, right) => right.riskScore - left.riskScore)
  }

  return arrayOrEmpty(visualizationTopics).map((topic, index) => {
    const sentimentScore = Number(topic.sentiment_score) || 0
    const volume = Number(topic.value) || 0
    const riskScore = estimateTopicRiskScore(sentimentScore, volume)
    return {
      clusterId: `visual_topic_${index + 1}`,
      topicId: `visual_topic_${index + 1}`,
      topic: topic.name || '未命名话题',
      commentCount: volume,
      negativeRatio: sentimentScore < 0 ? Math.min(1, Math.abs(sentimentScore)) : 0,
      averageSentimentScore: sentimentScore,
      negSeverity: sentimentScore < 0 ? Math.min(1, Math.abs(sentimentScore)) : 0,
      spreadSignal: Math.min(1, Math.log10(Math.max(1, volume)) / 2),
      controversySignal: 0,
      botSignal: 0,
      influenceProxy: Math.min(1, Math.log10(Math.max(1, volume)) / 2),
      riskScore,
      riskLevel: getRiskLevelFromScore(riskScore),
      explanation: `可视化话题热度 ${volume}，平均情绪 ${formatFixed(sentimentScore)}。`,
    }
  })
}

function normalizeTopicRisks(value) {
  return arrayOrEmpty(value)
    .map((item, index) => {
      if (!item || typeof item !== 'object') return null
      const riskScore = Number(item.topic_risk_score ?? item.risk_score ?? item.riskScore ?? 0)
      const riskLevel = item.topic_risk_level || item.risk_level || item.riskLevel || getRiskLevelFromScore(riskScore)
      return {
        clusterId: String(item.cluster_id || item.clusterId || item.topic_id || `topic_risk_${index + 1}`),
        topicId: String(item.topic_id || item.topicId || item.cluster_id || `topic_risk_${index + 1}`),
        topic: String(item.topic || item.name || '未命名话题'),
        commentCount: Number(item.comment_count ?? item.commentCount ?? 0),
        negativeRatio: Number(item.negative_ratio ?? item.negativeRatio ?? 0),
        averageSentimentScore: Number(item.average_sentiment_score ?? item.averageSentimentScore ?? 0),
        negSeverity: Number(item.neg_severity ?? item.negSeverity ?? 0),
        spreadSignal: Number(item.spread_signal ?? item.spreadSignal ?? 0),
        controversySignal: Number(item.controversy_signal ?? item.controversySignal ?? 0),
        botSignal: Number(item.bot_signal ?? item.botSignal ?? 0),
        influenceProxy: Number(item.influence_proxy ?? item.influenceProxy ?? 0),
        riskScore,
        riskLevel,
        explanation: String(item.risk_explanation || item.explanation || ''),
      }
    })
    .filter(Boolean)
}

function buildSentimentExplanation(analysis, visualization) {
  const sentiment = analysis?.sentiment
  if (!sentiment) {
    return '暂无情绪解释数据。'
  }
  const trendPoints = arrayOrEmpty(visualization?.sentiment_trend)
  const trendNote =
    trendPoints.length > 1
      ? `系统已观察到 ${trendPoints.length} 个情绪时间段，可继续用于判断负面趋势是否加速。`
      : '当前只有有限的模拟时间段，趋势判断应结合后续监测。'
  return `负面情绪占比为 ${formatPercentValue(sentiment.negative_ratio)}，平均情绪分为 ${formatFixed(
    sentiment.average_sentiment_score,
  )}。${trendNote}`
}

function buildBotSignalExplanation(signals, botImpact) {
  if (signals.length) {
    return signals[0]
  }
  if (botImpact > 0) {
    return `疑似机器人或重复话术评论占比为 ${formatPercentValue(botImpact)}。`
  }
  return '暂无显著疑似水军或重复话术信号。'
}

function estimateTopicRiskScore(sentimentScore, volume) {
  const negativePressure = Math.max(0, -Number(sentimentScore)) * 72
  const volumePressure = Math.min(28, Math.log10(Math.max(1, Number(volume))) * 18)
  return Math.round(Math.max(0, Math.min(100, negativePressure + volumePressure)))
}

function getRiskLevelFromScore(score) {
  if (score >= 85) return 'critical'
  if (score >= 70) return 'high'
  if (score >= 40) return 'medium'
  return 'low'
}

function formatFixed(value) {
  return typeof value === 'number' ? value.toFixed(2) : Number(value || 0).toFixed(2)
}

function formatPercentValue(value) {
  return `${Math.round((Number(value) || 0) * 100)}%`
}

function firstNonEmpty(...groups) {
  return groups.find((group) => group.length > 0) || []
}

function firstNonEmptyObjects(...groups) {
  return groups.find((group) => Array.isArray(group) && group.length > 0) || []
}

function firstDefinedNumber(...values) {
  for (const value of values) {
    if (value === null || value === undefined || value === '') continue
    const numericValue = Number(value)
    if (Number.isFinite(numericValue)) return numericValue
  }
  return null
}

function isNegativeTopicFinding(value) {
  return value.startsWith('Negative topic:') || value.startsWith('负面议题：')
}

function isBotSignal(value) {
  const normalized = value.toLowerCase()
  return (
    normalized.includes('bot') ||
    normalized.includes('automated') ||
    normalized.includes('script') ||
    normalized.includes('coordination') ||
    value.includes('机器人') ||
    value.includes('重复话术') ||
    value.includes('协同') ||
    value.includes('水军')
  )
}

function extractRepresentativeComments(topics) {
  return arrayOrEmpty(topics).flatMap((topic) => normalizeStringArray(topic.representative_comments))
}

function getNormalizedReport(summary, recommendation) {
  if (summary?.overall_summary) return summary
  if (recommendation?.overall_summary) return recommendation
  return null
}

function getRiskLevelLabel(riskLevel, reportLanguage) {
  if (reportLanguage !== DEFAULT_REPORT_LANGUAGE) return `${riskLevel} risk`
  const labelMap = {
    low: '低风险',
    medium: '中等风险',
    high: '高风险',
    critical: '严重风险',
  }
  return labelMap[riskLevel] || riskLevel
}
