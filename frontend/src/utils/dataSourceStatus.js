export function getAnalysisSourceStatus({ analysis, currentCase } = {}) {
  const source =
    analysis?.analysis_input_source ||
    currentCase?.analysis_input_source ||
    currentCase?.analysis_result?.analysis_input_source ||
    ''
  const platforms = normalizePlatforms(currentCase?.platforms || analysis?.platforms || [])
  const isCaseRawData = source === 'case_raw_data'
  const isYoutubeRealData = isCaseRawData && platforms.includes('youtube')

  let dataLabel = 'Data source: Mock data'
  let dataTagColor = 'default'
  if (isYoutubeRealData) {
    dataLabel = 'Data source: YouTube Real'
    dataTagColor = 'red'
  } else if (isCaseRawData) {
    dataLabel = 'Data source: Attached case raw data'
    dataTagColor = 'cyan'
  }

  return {
    analysisDescription: isCaseRawData
      ? 'Offline deterministic analysis from attached case raw data.'
      : 'Offline deterministic analysis from mock fallback data.',
    analysisLabel: 'Analysis: Offline deterministic',
    dataLabel,
    dataTagColor,
    isCaseRawData,
    isYoutubeRealData,
    llmLabel: 'LLM: Mock',
    source: source || 'unknown',
    sourceDetail: `analysis_input_source=${source || 'unknown'}`,
  }
}

function normalizePlatforms(platforms) {
  if (!Array.isArray(platforms)) return []
  return platforms.map((platform) => String(platform || '').toLowerCase()).filter(Boolean)
}
