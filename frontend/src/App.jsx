import { Alert, App as AntApp, ConfigProvider, Spin, theme } from 'antd'
import { motion } from 'framer-motion'
import { lazy, Suspense, useCallback, useEffect, useMemo, useRef, useState } from 'react'

import {
  createAnalysisCase,
  disableCaseMonitoring,
  enableCaseMonitoring,
  expandKeywords,
  generateRecommendation,
  generateSummary,
  getAnalysisCase,
  getAlerts,
  getCaseForecast,
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
  runCaseForecast,
  runCaseMonitoringCheck,
  simulateSendNotification,
  simulateSendPendingNotifications,
} from './api/sentigraphApi.js'
import { AppShell } from './components/layout/AppShell.jsx'
import { ErrorBoundary } from './components/layout/ErrorBoundary.jsx'
import { NotFound } from './pages/NotFound.jsx'
import { getAnalysisSourceStatus } from './utils/dataSourceStatus.js'

const DEFAULT_PROJECT_ID = 'project_001'
const DEFAULT_DATE_RANGE = { start: '2026-05-01', end: '2026-05-13' }
const DEFAULT_REPORT_LANGUAGE = 'zh-CN'
const DEMO_CASE_TITLE = 'Tesla Demo Case'
const DEMO_CASE_KEYWORD = 'Tesla'
const DEMO_CASE_PLATFORMS = ['reddit', 'weibo', 'bilibili']
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
const STATIC_PUBLIC_PAGES = [
  'businessReportDongluSunjihaiSample',
  'businessReportSample',
  'opinionEcosystem',
  'publicDemoGuide',
  'publicEventPlaza',
  'publicEventDetail',
  'publicEventRequest',
]

function lazyNamed(importer, exportName) {
  return lazy(() => importer().then((module) => ({ default: module[exportName] })))
}

const Dashboard = lazyNamed(() => import('./pages/Dashboard.jsx'), 'Dashboard')
const DemoFlow = lazyNamed(() => import('./pages/DemoFlow.jsx'), 'DemoFlow')
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
const SearchDiscovery = lazyNamed(() => import('./pages/SearchDiscovery.jsx'), 'SearchDiscovery')
const AnalysisRequests = lazyNamed(() => import('./pages/AnalysisRequests.jsx'), 'AnalysisRequests')
const ExternalCollectorBridge = lazyNamed(
  () => import('./pages/ExternalCollectorBridge.jsx'),
  'ExternalCollectorBridge',
)
const PublicDemoGuide = lazyNamed(() => import('./pages/PublicDemoGuide.jsx'), 'PublicDemoGuide')
const PublicEventPlaza = lazyNamed(() => import('./pages/PublicEventPlaza.jsx'), 'PublicEventPlaza')
const PublicEventDetail = lazyNamed(() => import('./pages/PublicEventDetail.jsx'), 'PublicEventDetail')
const PublicEventRequest = lazyNamed(() => import('./pages/PublicEventRequest.jsx'), 'PublicEventRequest')
const BusinessReportSample = lazyNamed(() => import('./pages/BusinessReportSample.jsx'), 'BusinessReportSample')
const BusinessReportDongluSunjihaiSample = lazyNamed(
  () => import('./pages/BusinessReportDongluSunjihaiSample.jsx'),
  'BusinessReportDongluSunjihaiSample',
)
const SelectorRepairTool = lazyNamed(() => import('./pages/SelectorRepairTool.jsx'), 'SelectorRepairTool')
const LlmAdminStatus = lazyNamed(() => import('./pages/LlmAdminStatus.jsx'), 'LlmAdminStatus')
const BenchmarkDashboard = lazyNamed(() => import('./pages/BenchmarkDashboard.jsx'), 'BenchmarkDashboard')
const SimulationLab = lazyNamed(() => import('./pages/SimulationLab.jsx'), 'SimulationLab')
const OpinionEcosystemSandbox = lazyNamed(
  () => import('./pages/OpinionEcosystemSandbox.jsx'),
  'OpinionEcosystemSandbox',
)

function pageFromHash() {
  const hash = window.location.hash.split('?')[0]
  if (hash === '#/demo') return 'publicDemoGuide'
  if (hash === '#/public-events') return 'publicEventPlaza'
  if (hash === '#/public-events/request') return 'publicEventRequest'
  if (hash === '#/public-events/helldivers-psn') return 'publicEventDetail'
  if (hash === '#/public-events/donglu-sunjihai-youth-football') return 'publicEventDetail'
  if (hash === '#/reports/helldivers-psn-sample') return 'businessReportSample'
  if (hash === '#/reports/donglu-sunjihai-youth-football-sample') return 'businessReportDongluSunjihaiSample'
  if (hash === '#/opinion-ecosystem') return 'opinionEcosystem'
  if (hash === '#/external-collector') return 'externalCollectorBridge'
  if (hash === '#/analysis-requests') return 'analysisRequests'
  return 'dashboard'
}

function App() {
  const [activePage, setActivePage] = useState(pageFromHash)
  const [currentHash, setCurrentHash] = useState(window.location.hash)
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
  const [caseForecast, setCaseForecast] = useState(null)
  const [forecastLoading, setForecastLoading] = useState(false)
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
  const hasLoadedProjectDataRef = useRef(false)
  const skipBootstrapData = STATIC_PUBLIC_PAGES.includes(activePage)
  const isStaticPublicPage = STATIC_PUBLIC_PAGES.includes(activePage)
  const isGuidedPublicEventFlow = currentHash.includes('guided=1')

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
    setCaseForecast(null)
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

  const refreshCaseForecast = useCallback(async (caseId) => {
    if (!caseId) {
      setCaseForecast(null)
      return null
    }
    try {
      const forecast = await getCaseForecast(caseId)
      setCaseForecast(forecast)
      return forecast
    } catch {
      setCaseForecast(null)
      return null
    }
  }, [])

  const loadCaseMonitoring = useCallback(async (caseId) => {
    if (!caseId) {
      setCaseSnapshots([])
      setCaseForecast(null)
      setAlerts([])
      setNotifications([])
      setNotificationOutboxStatus(null)
      setMonitoringConfig(null)
      setMonitoringStatus(null)
      return { snapshots: [], alerts: [] }
    }

    const [snapshots, caseAlertEvents, config, notificationState, forecast] = await Promise.all([
      listCaseSnapshots(caseId),
      listCaseAlerts(caseId),
      getCaseMonitoringConfig(caseId),
      refreshNotificationOutbox(caseId),
      refreshCaseForecast(caseId),
    ])
    setCaseSnapshots(snapshots)
    setAlerts(caseAlertEvents)
    setMonitoringConfig(config)
    return { snapshots, alerts: caseAlertEvents, notifications: notificationState.notifications, forecast }
  }, [refreshCaseForecast, refreshNotificationOutbox])

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
      setCaseForecast(null)
      setMonitoringConfig(null)
      setMonitoringStatus(null)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load mock analysis data.')
    } finally {
      setLoading(false)
    }
  }, [activeMvpPlatforms])

  useEffect(() => {
    if (skipBootstrapData || hasLoadedProjectDataRef.current) return
    hasLoadedProjectDataRef.current = true
    loadProjectData(DEFAULT_PROJECT_ID)
  }, [loadProjectData, skipBootstrapData])

  useEffect(() => {
    const handleHashChange = () => {
      setCurrentHash(window.location.hash)
      const nextPage = pageFromHash()
      if (nextPage !== 'dashboard') {
        setActivePage(nextPage)
      }
    }
    window.addEventListener('hashchange', handleHashChange)
    return () => window.removeEventListener('hashchange', handleHashChange)
  }, [])

  useEffect(() => {
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' })
    document.querySelector('.app-content')?.scrollTo?.({ top: 0, left: 0, behavior: 'auto' })
  }, [activePage, currentHash])

  useEffect(() => {
    if (skipBootstrapData) return undefined
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
  }, [skipBootstrapData])

  useEffect(() => {
    if (skipBootstrapData) return undefined
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
  }, [skipBootstrapData])

  useEffect(() => {
    if (skipBootstrapData) return undefined
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
  }, [skipBootstrapData])

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

  const handleLoadDemoCase = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const caseList = await refreshCases()
      const existingDemoCase = caseList.find((item) => {
        const title = String(item.title || '').toLowerCase()
        const keywordValue = String(item.keyword || '').toLowerCase()
        return title === DEMO_CASE_TITLE.toLowerCase() || keywordValue === DEMO_CASE_KEYWORD.toLowerCase()
      })

      let caseDetail = existingDemoCase
        ? await getAnalysisCase(existingDemoCase.case_id)
        : await createAnalysisCase({
            title: DEMO_CASE_TITLE,
            keyword: DEMO_CASE_KEYWORD,
            platforms: DEMO_CASE_PLATFORMS,
            report_language: DEFAULT_REPORT_LANGUAGE,
          })

      if (caseDetail.status !== 'completed') {
        caseDetail = await runAnalysisCase(caseDetail.case_id)
      }

      applyCaseDetail(caseDetail)
      let monitoringState = await loadCaseMonitoring(caseDetail.case_id)
      if ((monitoringState.snapshots?.length || 0) < 3) {
        await runCaseMonitoringCheck(caseDetail.case_id)
        await runCaseMonitoringCheck(caseDetail.case_id)
        monitoringState = await loadCaseMonitoring(caseDetail.case_id)
      }

      try {
        const config = await enableCaseMonitoring(caseDetail.case_id)
        setMonitoringConfig(config)
      } catch {
        // Demo prep remains usable even if schedule config is unavailable.
      }

      try {
        const forecast = await runCaseForecast(caseDetail.case_id)
        setCaseForecast(forecast)
      } catch {
        setCaseForecast(null)
      }

      const refreshedCase = await getAnalysisCase(caseDetail.case_id)
      applyCaseDetail(refreshedCase)
      await loadCaseMonitoring(refreshedCase.case_id)
      setSchedulerStatus(await getSchedulerStatus())
      await refreshCases()
      setActivePage('demoFlow')
      return refreshedCase
    } catch (requestError) {
      setError(requestError?.message || 'Unable to prepare the deterministic demo case.')
      return null
    } finally {
      setLoading(false)
    }
  }, [applyCaseDetail, loadCaseMonitoring, refreshCases])

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

  const handleCaseReady = useCallback(async (caseDetail) => {
    if (!caseDetail?.case_id) return
    applyCaseDetail(caseDetail)
    await refreshCases()
    try {
      await loadCaseMonitoring(caseDetail.case_id)
    } catch {
      // A just-created case can still be useful before monitoring artifacts exist.
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

  const handleRunForecast = useCallback(async () => {
    if (!currentCase?.case_id) {
      setError('Please create or open a case before running a forecast.')
      return null
    }
    setForecastLoading(true)
    setError('')
    try {
      const forecast = await runCaseForecast(currentCase.case_id)
      setCaseForecast(forecast)
      return forecast
    } catch (requestError) {
      setError(requestError?.message || 'Unable to run deterministic risk forecast.')
      return null
    } finally {
      setForecastLoading(false)
    }
  }, [currentCase])

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

  const handleStaticPageRefresh = useCallback(() => {
    window.location.reload()
  }, [])

  const handleNavigate = useCallback((pageKey, hashOverride = null) => {
    const hashByPage = {
      publicDemoGuide: '#/demo',
      publicEventPlaza: '#/public-events',
      publicEventRequest: '#/public-events/request',
      publicEventDetail: '#/public-events/helldivers-psn',
      businessReportSample: '#/reports/helldivers-psn-sample',
      businessReportDongluSunjihaiSample: '#/reports/donglu-sunjihai-youth-football-sample',
      opinionEcosystem: '#/opinion-ecosystem',
      externalCollectorBridge: '#/external-collector',
      analysisRequests: '#/analysis-requests',
    }
    if (hashOverride) {
      window.location.hash = hashOverride
    } else if (hashByPage[pageKey]) {
      window.location.hash = hashByPage[pageKey]
    } else if (window.location.hash) {
      window.history.replaceState(null, '', `${window.location.pathname}${window.location.search}`)
    }
    setActivePage(pageKey)
  }, [])

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

  const sourceStatus = useMemo(
    () => getAnalysisSourceStatus({ analysis, currentCase }),
    [analysis, currentCase],
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
    caseForecast,
    forecastLoading,
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
    onCaseReady: handleCaseReady,
    onLoadDemoCase: handleLoadDemoCase,
    onEnableMonitoring: handleEnableMonitoring,
    onDisableMonitoring: handleDisableMonitoring,
    onMarkNotificationRead: handleMarkNotificationRead,
    onNavigate: handleNavigate,
    onNavigateToKeyword: () => handleNavigate('keyword'),
    onOpenCaseReport: handleOpenCaseReport,
    onRefreshCases: refreshCases,
    onRunCase: handleRunCase,
    onRunDueMonitoringJobs: handleRunDueMonitoringJobs,
    onRunForecast: handleRunForecast,
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
    demoFlow: <DemoFlow {...pageProps} />,
    cases: <Cases {...pageProps} />,
    keyword: <KeywordSearch {...pageProps} />,
    analysis: <AnalysisResult {...pageProps} />,
    propagation: <PropagationGraph {...pageProps} />,
    risk: <RiskMonitor {...pageProps} />,
    summary: <SummaryReport {...pageProps} />,
    publicParsers: <PublicParserStatus />,
    platformIntegrations: <PlatformIntegrationOverview />,
    searchDiscovery: <SearchDiscovery {...pageProps} />,
    analysisRequests: <AnalysisRequests />,
    externalCollectorBridge: <ExternalCollectorBridge />,
    publicDemoGuide: <PublicDemoGuide />,
    publicEventPlaza: <PublicEventPlaza guided={isGuidedPublicEventFlow} onNavigate={handleNavigate} />,
    publicEventDetail: <PublicEventDetail onNavigate={handleNavigate} />,
    publicEventRequest: <PublicEventRequest />,
    businessReportSample: <BusinessReportSample />,
    businessReportDongluSunjihaiSample: <BusinessReportDongluSunjihaiSample />,
    selectorRepair: <SelectorRepairTool />,
    llmSafety: <LlmAdminStatus />,
    benchmarks: <BenchmarkDashboard />,
    simulationLab: <SimulationLab cases={cases} currentCase={currentCase} />,
    opinionEcosystem: <OpinionEcosystemSandbox />,
  }[activePage] || <NotFound activePage={activePage} onNavigate={setActivePage} />

  const riskScore = visualization?.risk_score ?? analysis?.risk?.risk_score ?? 0
  const riskLevel = visualization?.risk_level ?? analysis?.risk?.risk_level ?? 'low'
  const showGlobalError = error && !STATIC_PUBLIC_PAGES.includes(activePage)

  return (
    <ConfigProvider theme={appTheme}>
      <AntApp>
        <AppShell
          activePage={activePage}
          alertsCount={alerts.length}
          caseTitle={currentCase?.title}
          loading={loading}
          onNavigate={handleNavigate}
          onRefresh={isStaticPublicPage ? handleStaticPageRefresh : handleRefreshCurrent}
          projectId={projectId}
          riskLevel={riskLevel}
          riskScore={riskScore}
          sourceStatus={sourceStatus}
          isPublicDemoPage={isStaticPublicPage}
        >
          {showGlobalError ? <Alert className="app-alert" message={error} type="error" showIcon /> : null}
          <Spin spinning={loading}>
            <motion.div
              key={activePage}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.22, ease: 'easeOut' }}
            >
              <ErrorBoundary resetKey={activePage} onReset={() => setActivePage('dashboard')}>
                <Suspense
                  fallback={
                    <div className="app-suspense-loader">
                      <Spin />
                    </div>
                  }
                >
                  {currentPage}
                </Suspense>
              </ErrorBoundary>
            </motion.div>
          </Spin>
        </AppShell>
      </AntApp>
    </ConfigProvider>
  )
}

export default App
