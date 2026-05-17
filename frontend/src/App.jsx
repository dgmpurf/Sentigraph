import { Alert, App as AntApp, ConfigProvider, Spin, theme } from 'antd'
import { motion } from 'framer-motion'
import { lazy, Suspense, useCallback, useEffect, useMemo, useState } from 'react'

import {
  createAnalysisCase,
  disableCaseMonitoring,
  enableCaseMonitoring,
  expandKeywords,
  generateRecommendation,
  generateSummary,
  getAnalysisCase,
  getAlerts,
  getAnalysisResult,
  getCaseMonitoringConfig,
  getCaseMarkdownReport,
  getNotificationOutboxStatus,
  getPlatformStatus,
  getPropagation,
  getSchedulerStatus,
  getVisualizationData,
  listCaseAlerts,
  listCaseNotifications,
  listAnalysisCases,
  listCaseSnapshots,
  markNotificationRead,
  runDueMonitoringJobs,
  runAnalysisCase,
  runCaseMonitoringCheck,
  simulateSendNotification,
  simulateSendPendingNotifications,
} from './api/sentigraphApi.js'
import { AppShell } from './components/layout/AppShell.jsx'
import { ErrorBoundary } from './components/layout/ErrorBoundary.jsx'
import { NotFound } from './pages/NotFound.jsx'

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

function lazyNamed(importer, exportName) {
  return lazy(() => importer().then((module) => ({ default: module[exportName] })))
}

const Dashboard = lazyNamed(() => import('./pages/Dashboard.jsx'), 'Dashboard')
const Cases = lazyNamed(() => import('./pages/Cases.jsx'), 'Cases')
const KeywordSearch = lazyNamed(() => import('./pages/KeywordSearch.jsx'), 'KeywordSearch')
const AnalysisResult = lazyNamed(() => import('./pages/AnalysisResult.jsx'), 'AnalysisResult')
const PropagationGraph = lazyNamed(() => import('./pages/PropagationGraph.jsx'), 'PropagationGraph')
const RiskMonitor = lazyNamed(() => import('./pages/RiskMonitor.jsx'), 'RiskMonitor')
const SummaryReport = lazyNamed(() => import('./pages/SummaryReport.jsx'), 'SummaryReport')
const PublicParserStatus = lazyNamed(() => import('./pages/PublicParserStatus.jsx'), 'PublicParserStatus')
const PlatformIntegrationOverview = lazyNamed(
  () => import('./pages/PlatformIntegrationOverview.jsx'),
  'PlatformIntegrationOverview',
)
const SelectorRepairTool = lazyNamed(() => import('./pages/SelectorRepairTool.jsx'), 'SelectorRepairTool')
const LlmAdminStatus = lazyNamed(() => import('./pages/LlmAdminStatus.jsx'), 'LlmAdminStatus')

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
  const [caseSnapshots, setCaseSnapshots] = useState([])
  const [monitoringConfig, setMonitoringConfig] = useState(null)
  const [monitoringStatus, setMonitoringStatus] = useState(null)
  const [monitoringLoading, setMonitoringLoading] = useState(false)
  const [schedulerStatus, setSchedulerStatus] = useState(null)
  const [schedulerLoading, setSchedulerLoading] = useState(false)
  const [alerts, setAlerts] = useState([])
  const [notifications, setNotifications] = useState([])
  const [notificationOutboxStatus, setNotificationOutboxStatus] = useState(null)
  const [notificationLoading, setNotificationLoading] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const platformOptions = useMemo(() => {
    const enabledPlatforms = platformRegistry.filter((platform) => platform.selectable_for_mock && platform.mock_available)
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
    setMonitoringStatus(null)
    setMonitoringConfig(caseDetail.monitoring_config || null)

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

  const refreshNotificationOutbox = useCallback(async (caseId) => {
    const [caseNotifications, outboxStatus] = await Promise.all([
      caseId ? listCaseNotifications(caseId) : Promise.resolve([]),
      getNotificationOutboxStatus(),
    ])
    setNotifications(caseNotifications)
    setNotificationOutboxStatus(outboxStatus)
    return { notifications: caseNotifications, outboxStatus }
  }, [])

  const loadCaseMonitoring = useCallback(async (caseId) => {
    if (!caseId) {
      setCaseSnapshots([])
      setAlerts([])
      setNotifications([])
      setNotificationOutboxStatus(null)
      setMonitoringConfig(null)
      setMonitoringStatus(null)
      return { snapshots: [], alerts: [] }
    }

    const [snapshots, caseAlertEvents, config, notificationState] = await Promise.all([
      listCaseSnapshots(caseId),
      listCaseAlerts(caseId),
      getCaseMonitoringConfig(caseId),
      refreshNotificationOutbox(caseId),
    ])
    setCaseSnapshots(snapshots)
    setAlerts(caseAlertEvents)
    setMonitoringConfig(config)
    return { snapshots, alerts: caseAlertEvents, notifications: notificationState.notifications }
  }, [refreshNotificationOutbox])

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
      setNotifications([])
      setNotificationOutboxStatus(await getNotificationOutboxStatus())
      setCaseSnapshots([])
      setMonitoringConfig(null)
      setMonitoringStatus(null)
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
    getPlatformStatus()
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

  useEffect(() => {
    let isMounted = true
    getSchedulerStatus()
      .then((status) => {
        if (isMounted) {
          setSchedulerStatus(status)
        }
      })
      .catch(() => {
        if (isMounted) {
          setSchedulerStatus(null)
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
      await loadCaseMonitoring(completedCase.case_id)
      setActivePage('dashboard')
    } catch (requestError) {
      setError(requestError?.message || 'Unable to create and run mock analysis case.')
    } finally {
      setLoading(false)
    }
  }, [activeMvpPlatforms, applyCaseDetail, loadCaseMonitoring, refreshCases])

  const handleRunCase = useCallback(async (caseId, nextPage = 'dashboard') => {
    setLoading(true)
    setError('')
    try {
      const completedCase = await runAnalysisCase(caseId)
      applyCaseDetail(completedCase)
      await refreshCases()
      await loadCaseMonitoring(completedCase.case_id)
      setActivePage(nextPage)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to run mock analysis case.')
    } finally {
      setLoading(false)
    }
  }, [applyCaseDetail, loadCaseMonitoring, refreshCases])

  const handleOpenCaseReport = useCallback(async (caseId) => {
    setLoading(true)
    setError('')
    try {
      const caseDetail = await getAnalysisCase(caseId)
      applyCaseDetail(caseDetail)
      await loadCaseMonitoring(caseDetail.case_id)
      setActivePage('summary')
    } catch (requestError) {
      setError(requestError?.message || 'Unable to open the selected case report.')
    } finally {
      setLoading(false)
    }
  }, [applyCaseDetail, loadCaseMonitoring])

  const handleRunMonitoringCheck = useCallback(async () => {
    if (!currentCase?.case_id) {
      setError('Please create or open a case before running monitoring.')
      return null
    }
    setMonitoringLoading(true)
    setError('')
    try {
      const status = await runCaseMonitoringCheck(currentCase.case_id)
      setMonitoringStatus(status)
      await loadCaseMonitoring(currentCase.case_id)
      setSchedulerStatus(await getSchedulerStatus())
      return status
    } catch (requestError) {
      setError(requestError?.message || 'Unable to run mock monitoring check.')
      return null
    } finally {
      setMonitoringLoading(false)
    }
  }, [currentCase, loadCaseMonitoring])

  const handleEnableMonitoring = useCallback(async () => {
    if (!currentCase?.case_id) {
      setError('Please create or open a case before enabling monitoring.')
      return null
    }
    setSchedulerLoading(true)
    setError('')
    try {
      const config = await enableCaseMonitoring(currentCase.case_id)
      setMonitoringConfig(config)
      setSchedulerStatus(await getSchedulerStatus())
      await refreshCases()
      return config
    } catch (requestError) {
      setError(requestError?.message || 'Unable to enable scheduled monitoring.')
      return null
    } finally {
      setSchedulerLoading(false)
    }
  }, [currentCase, refreshCases])

  const handleDisableMonitoring = useCallback(async () => {
    if (!currentCase?.case_id) {
      setError('Please create or open a case before disabling monitoring.')
      return null
    }
    setSchedulerLoading(true)
    setError('')
    try {
      const config = await disableCaseMonitoring(currentCase.case_id)
      setMonitoringConfig(config)
      setSchedulerStatus(await getSchedulerStatus())
      await refreshCases()
      return config
    } catch (requestError) {
      setError(requestError?.message || 'Unable to disable scheduled monitoring.')
      return null
    } finally {
      setSchedulerLoading(false)
    }
  }, [currentCase, refreshCases])

  const handleRunDueMonitoringJobs = useCallback(async () => {
    setSchedulerLoading(true)
    setError('')
    try {
      const response = await runDueMonitoringJobs()
      setSchedulerStatus(await getSchedulerStatus())
      if (currentCase?.case_id) {
        const currentResult = response.monitoring_results?.find((item) => item.case_id === currentCase.case_id)
        const refreshedCase = await getAnalysisCase(currentCase.case_id)
        applyCaseDetail(refreshedCase)
        await loadCaseMonitoring(currentCase.case_id)
        if (currentResult) {
          setMonitoringStatus(currentResult)
        }
      }
      await refreshCases()
      return response
    } catch (requestError) {
      setError(requestError?.message || 'Unable to run due monitoring jobs.')
      return null
    } finally {
      setSchedulerLoading(false)
    }
  }, [applyCaseDetail, currentCase, loadCaseMonitoring, refreshCases])

  const handleMarkNotificationRead = useCallback(async (notificationId) => {
    if (!notificationId) return null
    setNotificationLoading(true)
    setError('')
    try {
      const notification = await markNotificationRead(notificationId)
      await refreshNotificationOutbox(currentCase?.case_id)
      return notification
    } catch (requestError) {
      setError(requestError?.message || 'Unable to mark notification as read.')
      return null
    } finally {
      setNotificationLoading(false)
    }
  }, [currentCase, refreshNotificationOutbox])

  const handleSimulateSendNotification = useCallback(async (notificationId) => {
    if (!notificationId) return null
    setNotificationLoading(true)
    setError('')
    try {
      const result = await simulateSendNotification(notificationId)
      await refreshNotificationOutbox(currentCase?.case_id)
      return result
    } catch (requestError) {
      setError(requestError?.message || 'Unable to simulate notification send.')
      return null
    } finally {
      setNotificationLoading(false)
    }
  }, [currentCase, refreshNotificationOutbox])

  const handleSimulateSendPendingNotifications = useCallback(async () => {
    setNotificationLoading(true)
    setError('')
    try {
      const results = await simulateSendPendingNotifications()
      await refreshNotificationOutbox(currentCase?.case_id)
      return results
    } catch (requestError) {
      setError(requestError?.message || 'Unable to simulate pending notification send.')
      return []
    } finally {
      setNotificationLoading(false)
    }
  }, [currentCase, refreshNotificationOutbox])

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
    caseSnapshots,
    markdownLoading,
    markdownReport,
    monitoringConfig,
    monitoringLoading,
    monitoringStatus,
    notificationLoading,
    notificationOutboxStatus,
    notifications,
    schedulerLoading,
    schedulerStatus,
    onGetMarkdownReport: handleGetMarkdownReport,
    onEnableMonitoring: handleEnableMonitoring,
    onDisableMonitoring: handleDisableMonitoring,
    onMarkNotificationRead: handleMarkNotificationRead,
    onNavigateToKeyword: () => setActivePage('keyword'),
    onOpenCaseReport: handleOpenCaseReport,
    onRefreshCases: refreshCases,
    onRunCase: handleRunCase,
    onRunDueMonitoringJobs: handleRunDueMonitoringJobs,
    onRunMonitoringCheck: handleRunMonitoringCheck,
    onSimulateSendNotification: handleSimulateSendNotification,
    onSimulateSendPendingNotifications: handleSimulateSendPendingNotifications,
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
    publicParsers: <PublicParserStatus />,
    platformIntegrations: <PlatformIntegrationOverview />,
    selectorRepair: <SelectorRepairTool />,
    llmSafety: <LlmAdminStatus />,
  }[activePage] || <NotFound activePage={activePage} onNavigate={setActivePage} />

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
              <ErrorBoundary resetKey={activePage} onReset={() => setActivePage('dashboard')}>
                <Suspense fallback={<Spin spinning tip="Loading page" />}>{currentPage}</Suspense>
              </ErrorBoundary>
            </motion.div>
          </Spin>
        </AppShell>
      </AntApp>
    </ConfigProvider>
  )
}

export default App
