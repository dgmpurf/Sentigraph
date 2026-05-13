export function buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization }) {
  const keyFindings = arrayOrEmpty(summary?.key_findings)
  const mainRisks = arrayOrEmpty(recommendation?.main_risks)
  const topicFallback = arrayOrEmpty(analysis?.topics)
    .filter((topic) => Number(topic.average_sentiment_score) < 0)
    .map(
      (topic) =>
        `${topic.topic}: ${topic.comment_count} comments, average sentiment ${formatFixed(
          topic.average_sentiment_score,
        )}`,
    )

  const topNegativeTopics = keyFindings
    .filter((finding) => finding.startsWith('Negative topic:'))
    .map((finding) => finding.replace('Negative topic:', '').trim())

  const botSignals = keyFindings.filter((finding) => {
    const normalized = finding.toLowerCase()
    return normalized.includes('bot') || normalized.includes('automated') || normalized.includes('script')
  })

  return {
    overallSummary: summary?.summary || recommendation?.summary || analysis?.summary || '',
    mainRiskFactors: mainRisks.length ? mainRisks : keyFindings.filter((finding) => !finding.startsWith('Negative topic:')),
    topNegativeTopics: topNegativeTopics.length ? topNegativeTopics : topicFallback,
    representativeComments: arrayOrEmpty(summary?.representative_comments),
    suspectedBotSignals: botSignals.length
      ? botSignals
      : mainRisks.filter((risk) => {
          const normalized = risk.toLowerCase()
          return normalized.includes('bot') || normalized.includes('automated') || normalized.includes('script')
        }),
    recommendedActions: arrayOrEmpty(recommendation?.recommended_actions),
    suggestedPublicResponse: recommendation?.suggested_response || '',
    riskScore: visualization?.risk_score ?? analysis?.risk?.risk_score ?? 0,
    riskLevel: visualization?.risk_level ?? analysis?.risk?.risk_level ?? 'low',
  }
}

export function arrayOrEmpty(value) {
  return Array.isArray(value) ? value : []
}

export function hasReportContent(report) {
  if (!report) return false
  return Boolean(
    report.overallSummary ||
      report.mainRiskFactors.length ||
      report.topNegativeTopics.length ||
      report.representativeComments.length ||
      report.suspectedBotSignals.length ||
      report.recommendedActions.length ||
      report.suggestedPublicResponse,
  )
}

function formatFixed(value) {
  return typeof value === 'number' ? value.toFixed(2) : '0.00'
}
