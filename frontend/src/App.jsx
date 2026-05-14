import { Alert, App as AntApp, ConfigProvider, Spin, theme } from 'antd'
import { motion } from 'framer-motion'
import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  createAnalysisCase,
  expandKeywords,
  generateRecommendation,
  generateSummary,
  getAnalysisCase,
  getAlerts,
  getAnalysisResult,
  getCaseMarkdownReport,
  getPlatforms,
  getPropagation,
  getVisualizationData,
  listAnalysisCases,
  runAnalysisCase,
} from './api/sentigraphApi.js'
import { AppShell } from './components/layout/AppShell.jsx'
import { AnalysisResult } from './pages/AnalysisResult.jsx'
import { Cases } from './pages/Cases.jsx'
import { Dashboard } from './pages/Dashboard.jsx'
import { KeywordSearch } from './pages/KeywordSearch.jsx'
import { PropagationGraph } from './pages/PropagationGraph.jsx'
import { RiskMonitor } from './pages/RiskMonitor.jsx'
import { SummaryReport } from './pages/SummaryReport.jsx'

const DEFAULT_PROJECT_ID = 'project_001'
const DEFAULT_DATE_RANGE = { start: '2026-05-01', end: '2026-05-13' }
const DEFAULT_REPORT_LANGUAGE = 'zh-CN'
const DEFAULT_PLATFORMS = [
  'reddit',
  'weibo',
  'bilibili',
  'douyin',
  'kuaishou',
  'xiaohongshu',
  'zhihu',
  'douban',
  'toutiao',
]
const FALLBACK_PLATFORM_OPTIONS = [
  { label: 'Reddit', value: 'reddit' },
  { label: 'Weibo', value: 'weibo' },
  { label: 'Bilibili', value: 'bilibili' },
  { label: 'Douyin', value: 'douyin' },
  { label: 'Kuaishou', value: 'kuaishou' },
  { label: 'Xiaohongshu', value: 'xiaohongshu' },
  { label: 'Zhihu', value: 'zhihu' },
  { label: 'Douban', value: 'douban' },
  { label: 'Toutiao', value: 'toutiao' },
]

function App() {
  const [activePage, setActivePage] = useState('dashboard')
  const [projectId, setProjectId] = useState(DEFAULT_PROJECT_ID)
  const [keyword, setKeyword] = useState('Tesla')
  const [expandedKeywords, setExpandedKeywords] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [visualization, setVisualization] = useState(null)
  const [summary, setSummary] = useState(null)
  const [recommendation, setRecommendation] = useState(null)
  const [propagation, setPropagation] = useState(null)
  const [platformRegistry, setPlatformRegistry] = useState([])
  const [cases, setCases] = useState([])
  const [currentCase, setCurrentCase] = useState(null)
  const [markdownReport, setMarkdownReport] = useState(null)
  const [markdownLoading, setMarkdownLoading] = useState(false)
  const [alerts, setAlerts] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const platformOptions = useMemo(() => {
    const enabledPlatforms = platformRegistry.filter((platform) => platform.selectable_for_mock)
    if (!enabledPlatforms.length) return FALLBACK_PLATFORM_OPTIONS
    return enabledPlatforms.map((platform) => ({
      label: platform.display_name,
      value: platform.platform_id,
    }))
  }, [platformRegistry])

  const activeMvpPlatforms = useMemo(
    () => platformOptions.map((platform) => platform.value),
    [platformOptions],
  )

  const applyCaseDetail = useCallback((caseDetail) => {
    if (!caseDetail) return
    setCurrentCase(caseDetail)
    setProjectId(caseDetail.project_id || DEFAULT_PROJECT_ID)
    setKeyword(caseDetail.keyword || 'Tesla')
    setMarkdownReport(null)

    if (caseDetail.analysis_result) {
      setAnalysis(caseDetail.analysis_result)
    }
    if (caseDetail.visualization_data) {
      setVisualization(caseDetail.visualization_data)
      setPropagation(null)
    }
    if (caseDetail.report) {
      setSummary(caseDetail.report)
      setRecommendation(caseDetail.report)
    }
  }, [])

  const refreshCases = useCallback(async () => {
    const caseList = await listAnalysisCases()
    setCases(caseList)
    return caseList
  }, [])

  const loadProjectData = useCallback(async (nextProjectId = DEFAULT_PROJECT_ID) => {
    setLoading(true)
    setError('')
    try {
      const selectedPlatforms = activeMvpPlatforms.length ? activeMvpPlatforms : DEFAULT_PLATFORMS
      const request = {
        project_id: nextProjectId,
        date_range: DEFAULT_DATE_RANGE,
        platforms: selectedPlatforms,
      }
      const [analysisData, visualizationData, summaryData, recommendationData, propagationData, alertsData] =
        await Promise.all([
          getAnalysisResult(nextProjectId),
          getVisualizationData(request),
          generateSummary({
            project_id: nextProjectId,
            include_representative_comments: true,
            report_language: DEFAULT_REPORT_LANGUAGE,
          }),
          generateRecommendation({
            project_id: nextProjectId,
            user_type: 'brand',
            tone: 'professional',
            report_language: DEFAULT_REPORT_LANGUAGE,
          }),
          getPropagation(nextProjectId),
          getAlerts(nextProjectId),
        ])
      setAnalysis(analysisData)
      setVisualization(visualizationData)
      setSummary(summaryData)
      setRecommendation(recommendationData)
      setPropagation(propagationData)
      setAlerts(alertsData.alerts || [])
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load mock analysis data.')
    } finally {
      setLoading(false)
    }
  }, [activeMvpPlatforms])

  useEffect(() => {
    loadProjectData(DEFAULT_PROJECT_ID)
  }, [loadProjectData])

  useEffect(() => {
    let isMounted = true
    listAnalysisCases()
      .then((caseList) => {
        if (isMounted) {
          setCases(caseList)
        }
      })
      .catch(() => {
        if (isMounted) {
          setCases([])
        }
      })
    return () => {
      isMounted = false
    }
  }, [])

  useEffect(() => {
    let isMounted = true
    getPlatforms()
      .then((registry) => {
        if (isMounted) {
          setPlatformRegistry(registry.platforms || [])
        }
      })
      .catch(() => {
        if (isMounted) {
          setPlatformRegistry([])
        }
      })
    return () => {
      isMounted = false
    }
  }, [])

  const handleStartAnalysis = useCallback(async (formValues) => {
    setLoading(true)
    setError('')
    try {
      const selectedPlatforms = formValues.platforms?.length ? formValues.platforms : activeMvpPlatforms
      const keywordData = await expandKeywords({
        keyword: formValues.keyword,
        platforms: selectedPlatforms,
        language: formValues.language,
      })
      const caseDetail = await createAnalysisCase({
        title: formValues.title,
        keyword: formValues.keyword,
        platforms: selectedPlatforms,
        report_language: DEFAULT_REPORT_LANGUAGE,
      })
      const completedCase = await runAnalysisCase(caseDetail.case_id)
      setKeyword(formValues.keyword)
      setExpandedKeywords(keywordData)
      applyCaseDetail(completedCase)
      await refreshCases()
      const alertsData = await getAlerts(completedCase.project_id)
      setAlerts(alertsData.alerts || [])
      setActivePage('dashboard')
    } catch (requestError) {
      setError(requestError?.message || 'Unable to create and run mock analysis case.')
    } finally {
      setLoading(false)
    }
  }, [activeMvpPlatforms, applyCaseDetail, refreshCases])

  const handleRunCase = useCallback(async (caseId, nextPage = 'dashboard') => {
    setLoading(true)
    setError('')
    try {
      const completedCase = await runAnalysisCase(caseId)
      applyCaseDetail(completedCase)
      await refreshCases()
      const alertsData = await getAlerts(completedCase.project_id)
      setAlerts(alertsData.alerts || [])
      setActivePage(nextPage)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to run mock analysis case.')
    } finally {
      setLoading(false)
    }
  }, [applyCaseDetail, refreshCases])

  const handleOpenCaseReport = useCallback(async (caseId) => {
    setLoading(true)
    setError('')
    try {
      const caseDetail = await getAnalysisCase(caseId)
      applyCaseDetail(caseDetail)
      const alertsData = await getAlerts(caseDetail.project_id)
      setAlerts(alertsData.alerts || [])
      setActivePage('summary')
    } catch (requestError) {
      setError(requestError?.message || 'Unable to open the selected case report.')
    } finally {
      setLoading(false)
    }
  }, [applyCaseDetail])

  const handleGetMarkdownReport = useCallback(async () => {
    if (!currentCase?.case_id) {
      throw new Error('No analysis case is currently selected.')
    }
    if (markdownReport?.case_id === currentCase.case_id) {
      return markdownReport
    }

    setMarkdownLoading(true)
    try {
      const report = await getCaseMarkdownReport(currentCase.case_id)
      setMarkdownReport(report)
      return report
    } finally {
      setMarkdownLoading(false)
    }
  }, [currentCase, markdownReport])

  const handleRefreshCurrent = useCallback(() => {
    if (currentCase?.case_id) {
      handleRunCase(currentCase.case_id, activePage)
      return
    }
    loadProjectData(projectId)
  }, [activePage, currentCase, handleRunCase, loadProjectData, projectId])

  const appTheme = useMemo(
    () => ({
      algorithm: theme.darkAlgorithm,
      token: {
        colorPrimary: '#42f5d7',
        colorBgBase: '#08090d',
        colorBgContainer: '#11131a',
        colorBorder: '#283043',
        colorTextBase: '#f4f7fb',
        borderRadius: 8,
        fontFamily:
          'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
      },
      components: {
        Card: {
          colorBgContainer: '#11131a',
          colorBorderSecondary: '#283043',
        },
        Layout: {
          bodyBg: '#08090d',
          headerBg: '#0d1016',
          siderBg: '#0d1016',
        },
      },
    }),
    [],
  )

  const pageProps = {
    alerts,
    analysis,
    cases,
    currentCase,
    error,
    expandedKeywords,
    keyword,
    loading,
    markdownLoading,
    markdownReport,
    onGetMarkdownReport: handleGetMarkdownReport,
    onNavigateToKeyword: () => setActivePage('keyword'),
    onOpenCaseReport: handleOpenCaseReport,
    onRefreshCases: refreshCases,
    onRunCase: handleRunCase,
    onStartAnalysis: handleStartAnalysis,
    platformOptions,
    platformRegistry,
    initialPlatforms: activeMvpPlatforms,
    propagation,
    recommendation,
    summary,
    visualization,
  }

  const currentPage = {
    dashboard: <Dashboard {...pageProps} />,
    cases: <Cases {...pageProps} />,
    keyword: <KeywordSearch {...pageProps} />,
    analysis: <AnalysisResult {...pageProps} />,
    propagation: <PropagationGraph {...pageProps} />,
    risk: <RiskMonitor {...pageProps} />,
    summary: <SummaryReport {...pageProps} />,
  }[activePage]

  const riskScore = visualization?.risk_score ?? analysis?.risk?.risk_score ?? 0
  const riskLevel = visualization?.risk_level ?? analysis?.risk?.risk_level ?? 'low'

  return (
    <ConfigProvider theme={appTheme}>
      <AntApp>
        <AppShell
          activePage={activePage}
          alertsCount={alerts.length}
          caseTitle={currentCase?.title}
          loading={loading}
          onNavigate={setActivePage}
          onRefresh={handleRefreshCurrent}
          projectId={projectId}
          riskLevel={riskLevel}
          riskScore={riskScore}
        >
          {error ? <Alert className="app-alert" message={error} type="error" showIcon /> : null}
          <Spin spinning={loading} tip="Loading mock intelligence">
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.22, ease: 'easeOut' }}
            >
              {currentPage}
            </motion.div>
          </Spin>
        </AppShell>
      </AntApp>
    </ConfigProvider>
  )
}

export default App
