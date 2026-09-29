import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'
import { apiClient } from './api/client.js'

const cases = vi.hoisted(() => {
  const completed = {
    case_id: 'case_synthetic', project_id: 'project_synthetic', keyword: 'Synthetic',
    status: 'completed', case_revision: 2, analysis_revision: 1, analysis_run_id: 'run_a', markdown_available: true,
    analysis_result: { summary: 'Completed synthetic analysis', analysis_input_source: 'case_evidence_items' },
    visualization_data: { risk_score: 12 },
    report: { overall_summary: 'Completed synthetic report' },
    monitoring_config: null,
  }
  return {
    completed,
    reviewed: {
      ...completed, status: 'draft', markdown_available: false,
      case_revision: 3, analysis_revision: null, analysis_run_id: null,
      analysis_result: null, visualization_data: null, report: null,
    },
    rerun: {
      ...completed, case_revision: 4, analysis_revision: 2, analysis_run_id: 'run_b',
      analysis_result: { summary: 'Fresh synthetic analysis', analysis_input_source: 'case_evidence_items' },
      report: { overall_summary: 'Fresh synthetic report' },
    },
    configBump: { ...completed, case_revision: 9 },
  }
})

const apiMocks = vi.hoisted(() => ({
  getCaseMarkdownReport: vi.fn(),
  listCaseSnapshots: vi.fn(),
  listCaseAlerts: vi.fn(),
  listCaseNotifications: vi.fn(),
  getNotificationOutboxStatus: vi.fn(),
  getCaseForecast: vi.fn(),
  getCaseMonitoringConfig: vi.fn(),
  enableCaseMonitoring: vi.fn(),
  disableCaseMonitoring: vi.fn(),
  runCaseMonitoringCheck: vi.fn(),
  runCaseForecast: vi.fn(),
  markNotificationRead: vi.fn(),
}))

vi.mock('./api/sentigraphApi.js', async (importOriginal) => ({
  ...(await importOriginal()),
  getAnalysisResult: vi.fn().mockResolvedValue(null),
  getVisualizationData: vi.fn().mockResolvedValue(null),
  generateSummary: vi.fn().mockResolvedValue(null),
  generateRecommendation: vi.fn().mockResolvedValue(null),
  getPropagation: vi.fn().mockResolvedValue(null),
  getAlerts: vi.fn().mockResolvedValue({ alerts: [] }),
  listAnalysisCases: vi.fn().mockResolvedValue([]),
  getPlatformStatus: vi.fn().mockResolvedValue({ platforms: [] }),
  getSchedulerStatus: vi.fn().mockResolvedValue({}),
  ...apiMocks,
}))

vi.mock('./components/layout/AppShell.jsx', () => ({ AppShell: ({ children }) => <div>{children}</div> }))
vi.mock('./pages/Dashboard.jsx', () => ({
  Dashboard: ({ analysis, currentCase, markdownReport, caseSnapshots, alerts, notifications, caseForecast, monitoringConfig, monitoringStatus, notificationOutboxStatus, onCaseReady, onGetMarkdownReport, onRunMonitoringCheck, onRunForecast, onEnableMonitoring, onDisableMonitoring, onMarkNotificationRead, recommendation, summary, visualization }) => (
    <div>
      <button onClick={() => onCaseReady(cases.completed)}>Apply completed</button>
      <button onClick={() => onCaseReady(cases.reviewed)}>Apply reviewed</button>
      <button onClick={() => onCaseReady(cases.rerun)}>Apply rerun</button>
      <button onClick={() => onCaseReady(cases.configBump)}>Apply config bump</button>
      <button onClick={() => { void onGetMarkdownReport().catch(() => {}) }}>Get Markdown</button>
      <button onClick={() => { void onRunMonitoringCheck() }}>Run monitoring</button>
      <button onClick={() => { void onRunForecast() }}>Run forecast</button>
      <button onClick={() => { void onEnableMonitoring() }}>Enable monitoring</button>
      <button onClick={() => { void onDisableMonitoring() }}>Disable monitoring</button>
      <button onClick={() => { void onMarkNotificationRead('notice_a') }}>Mark notice read</button>
      <span data-testid="case-status">{currentCase?.status || 'none'}</span>
      <span data-testid="analysis-state">{analysis?.summary || 'none'}</span>
      <span data-testid="visualization-state">{visualization?.risk_score ?? 'none'}</span>
      <span data-testid="summary-state">{summary?.overall_summary || 'none'}</span>
      <span data-testid="recommendation-state">{recommendation?.overall_summary || 'none'}</span>
      <span data-testid="markdown-state">{markdownReport?.markdown || 'none'}</span>
      <span data-testid="snapshot-state">{caseSnapshots.map((item) => item.snapshot_id).join(',') || 'none'}</span>
      <span data-testid="alert-state">{alerts.map((item) => item.alert_id).join(',') || 'none'}</span>
      <span data-testid="notification-state">{notifications.map((item) => item.notification_id).join(',') || 'none'}</span>
      <span data-testid="outbox-state">{notificationOutboxStatus?.current_pending ?? 'none'}</span>
      <span data-testid="forecast-state">{caseForecast?.source_analysis_run_id || 'none'}</span>
      <span data-testid="monitor-state">{monitoringStatus?.source_analysis_run_id || 'none'}</span>
      <span data-testid="monitor-config-state">{monitoringConfig?.status || 'none'}</span>
    </div>
  ),
}))

import App from './App.jsx'

function deferred() {
  let resolve
  const promise = new Promise((accept) => { resolve = accept })
  return { promise, resolve }
}

beforeEach(() => {
  window.location.hash = ''
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    unobserve() {}
    disconnect() {}
  })
  vi.stubGlobal('matchMedia', (query) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false },
  }))
  vi.stubGlobal('scrollTo', vi.fn())
  for (const mock of Object.values(apiMocks)) mock.mockReset()
  apiMocks.getCaseMarkdownReport.mockImplementation(async () => ({
    case_id: 'case_synthetic', markdown: '# Fresh',
    source_analysis_revision: apiMocks.getCaseMarkdownReport.mock.calls.length === 1 ? 1 : 2,
    source_analysis_run_id: apiMocks.getCaseMarkdownReport.mock.calls.length === 1 ? 'run_a' : 'run_b',
  }))
  apiMocks.listCaseSnapshots.mockResolvedValue([])
  apiMocks.listCaseAlerts.mockResolvedValue([])
  apiMocks.listCaseNotifications.mockResolvedValue([])
  apiMocks.getNotificationOutboxStatus.mockResolvedValue({ current_pending: 0 })
  apiMocks.getCaseForecast.mockResolvedValue(null)
  apiMocks.getCaseMonitoringConfig.mockResolvedValue(null)
  apiMocks.enableCaseMonitoring.mockResolvedValue(null)
  apiMocks.disableCaseMonitoring.mockResolvedValue(null)
  apiMocks.runCaseMonitoringCheck.mockResolvedValue(null)
  apiMocks.runCaseForecast.mockResolvedValue(null)
  apiMocks.markNotificationRead.mockResolvedValue(null)
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

it('clears case-derived state and Markdown cache after review, then restores only after explicit rerun', async () => {
  render(<App />)
  fireEvent.click(await screen.findByText('Apply completed'))
  await waitFor(() => expect(screen.getByTestId('analysis-state').textContent).toBe('Completed synthetic analysis'))
  expect(screen.getByTestId('summary-state').textContent).toBe('Completed synthetic report')
  fireEvent.click(screen.getByText('Get Markdown'))
  await waitFor(() => expect(screen.getByTestId('markdown-state').textContent).toBe('# Fresh'))
  expect(apiMocks.getCaseMarkdownReport).toHaveBeenCalledTimes(1)

  fireEvent.click(screen.getByText('Apply reviewed'))
  await waitFor(() => expect(screen.getByTestId('case-status').textContent).toBe('draft'))
  for (const id of ['analysis-state', 'visualization-state', 'summary-state', 'recommendation-state', 'markdown-state']) {
    expect(screen.getByTestId(id).textContent).toBe('none')
  }
  fireEvent.click(screen.getByText('Get Markdown'))
  await waitFor(() => expect(apiMocks.getCaseMarkdownReport).toHaveBeenCalledTimes(1))

  fireEvent.click(screen.getByText('Apply rerun'))
  await waitFor(() => expect(screen.getByTestId('analysis-state').textContent).toBe('Fresh synthetic analysis'))
  expect(screen.getByTestId('summary-state').textContent).toBe('Fresh synthetic report')
  fireEvent.click(screen.getByText('Get Markdown'))
  await waitFor(() => expect(apiMocks.getCaseMarkdownReport).toHaveBeenCalledTimes(2))
})

it('discards a late Pair A monitoring batch after Pair B is selected', async () => {
  const oldSnapshots = deferred()
  apiMocks.listCaseSnapshots.mockImplementationOnce(() => oldSnapshots.promise)
    .mockResolvedValue([{ snapshot_id: 'snapshot_b', lineage_status: 'CURRENT' }])
  apiMocks.listCaseAlerts.mockResolvedValueOnce([{ alert_id: 'alert_a', lineage_status: 'CURRENT' }])
    .mockResolvedValue([{ alert_id: 'alert_b', lineage_status: 'CURRENT' }])
  apiMocks.listCaseNotifications.mockResolvedValueOnce([{ notification_id: 'notice_a', lineage_status: 'CURRENT' }])
    .mockResolvedValue([{ notification_id: 'notice_b', lineage_status: 'CURRENT' }])
  apiMocks.getNotificationOutboxStatus.mockResolvedValueOnce({ current_pending: 1 })
    .mockResolvedValue({ current_pending: 2 })
  apiMocks.getCaseForecast.mockResolvedValueOnce({
    case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
  }).mockResolvedValue({ case_id: 'case_synthetic', source_analysis_revision: 2, source_analysis_run_id: 'run_b' })

  render(<App />)
  fireEvent.click(await screen.findByText('Apply completed'))
  await waitFor(() => expect(apiMocks.listCaseSnapshots).toHaveBeenCalledTimes(1))
  fireEvent.click(screen.getByText('Apply rerun'))
  await waitFor(() => expect(screen.getByTestId('snapshot-state').textContent).toBe('snapshot_b'))
  await act(async () => oldSnapshots.resolve([{ snapshot_id: 'snapshot_a', lineage_status: 'CURRENT' }]))
  expect(screen.getByTestId('snapshot-state').textContent).toBe('snapshot_b')
  expect(screen.getByTestId('alert-state').textContent).toBe('alert_b')
  expect(screen.getByTestId('notification-state').textContent).toBe('notice_b')
  expect(screen.getByTestId('outbox-state').textContent).toBe('2')
  expect(screen.getByTestId('forecast-state').textContent).toBe('run_b')
})

it('accepts a late batch when only case_revision changed but analysis pair did not', async () => {
  const firstSnapshots = deferred()
  const secondSnapshots = deferred()
  apiMocks.listCaseSnapshots.mockImplementationOnce(() => firstSnapshots.promise)
    .mockImplementationOnce(() => secondSnapshots.promise)
  render(<App />)
  fireEvent.click(await screen.findByText('Apply completed'))
  await waitFor(() => expect(apiMocks.listCaseSnapshots).toHaveBeenCalledTimes(1))
  fireEvent.click(screen.getByText('Apply config bump'))
  await waitFor(() => expect(apiMocks.listCaseSnapshots).toHaveBeenCalledTimes(2))
  await act(async () => firstSnapshots.resolve([{ snapshot_id: 'same_pair_snapshot', lineage_status: 'CURRENT' }]))
  expect(screen.getByTestId('snapshot-state').textContent).toBe('same_pair_snapshot')
  await act(async () => secondSnapshots.resolve([{ snapshot_id: 'same_pair_snapshot', lineage_status: 'CURRENT' }]))
})

it('does not cache late Pair A Markdown under the same case ID after Pair B rerun', async () => {
  const oldMarkdown = deferred()
  apiMocks.getCaseMarkdownReport.mockImplementationOnce(() => oldMarkdown.promise).mockResolvedValue({
    case_id: 'case_synthetic', markdown: '# Pair B', source_analysis_revision: 2, source_analysis_run_id: 'run_b',
  })
  render(<App />)
  fireEvent.click(await screen.findByText('Apply completed'))
  await waitFor(() => expect(screen.getByTestId('case-status').textContent).toBe('completed'))
  fireEvent.click(screen.getByText('Get Markdown'))
  await waitFor(() => expect(apiMocks.getCaseMarkdownReport).toHaveBeenCalledTimes(1))
  fireEvent.click(screen.getByText('Apply rerun'))
  await act(async () => oldMarkdown.resolve({
    case_id: 'case_synthetic', markdown: '# Pair A', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
  }))
  expect(screen.getByTestId('markdown-state').textContent).toBe('none')
  fireEvent.click(screen.getByText('Get Markdown'))
  await waitFor(() => expect(screen.getByTestId('markdown-state').textContent).toBe('# Pair B'))
  expect(apiMocks.getCaseMarkdownReport).toHaveBeenCalledTimes(2)
})

it('rejects stale forecast and monitoring status responses but accepts the selected pair', async () => {
  render(<App />)
  fireEvent.click(await screen.findByText('Apply rerun'))
  await waitFor(() => expect(screen.getByTestId('case-status').textContent).toBe('completed'))
  apiMocks.runCaseForecast.mockResolvedValueOnce({
    case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
  }).mockResolvedValue({ case_id: 'case_synthetic', source_analysis_revision: 2, source_analysis_run_id: 'run_b' })
  fireEvent.click(screen.getByText('Run forecast'))
  await waitFor(() => expect(apiMocks.runCaseForecast).toHaveBeenCalledTimes(1))
  expect(screen.getByTestId('forecast-state').textContent).toBe('none')
  fireEvent.click(screen.getByText('Run forecast'))
  await waitFor(() => expect(screen.getByTestId('forecast-state').textContent).toBe('run_b'))

  apiMocks.runCaseMonitoringCheck.mockResolvedValueOnce({
    case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
  }).mockResolvedValue({ case_id: 'case_synthetic', source_analysis_revision: 2, source_analysis_run_id: 'run_b' })
  fireEvent.click(screen.getByText('Run monitoring'))
  await waitFor(() => expect(apiMocks.runCaseMonitoringCheck).toHaveBeenCalledTimes(1))
  expect(screen.getByTestId('monitor-state').textContent).toBe('none')
  fireEvent.click(screen.getByText('Run monitoring'))
  await waitFor(() => expect(screen.getByTestId('monitor-state').textContent).toBe('run_b'))
})

it('does not apply a late monitoring configuration from an earlier analysis pair', async () => {
  const oldConfig = deferred()
  apiMocks.enableCaseMonitoring.mockImplementationOnce(() => oldConfig.promise)
  render(<App />)
  fireEvent.click(await screen.findByText('Apply completed'))
  await waitFor(() => expect(screen.getByTestId('case-status').textContent).toBe('completed'))
  fireEvent.click(screen.getByText('Enable monitoring'))
  await waitFor(() => expect(apiMocks.enableCaseMonitoring).toHaveBeenCalledTimes(1))
  fireEvent.click(screen.getByText('Apply rerun'))
  await act(async () => oldConfig.resolve({ status: 'scheduled', enabled: true }))
  expect(screen.getByTestId('monitor-config-state').textContent).toBe('none')
})

it('preserves normalized auxiliary lineage and current outbox counts through public API functions', async () => {
  const api = await vi.importActual('./api/sentigraphApi.js')
  const get = vi.spyOn(apiClient, 'get').mockImplementation(async (url) => {
    if (url.endsWith('/cases/case_synthetic')) return { data: cases.completed }
    if (url.endsWith('/snapshots')) return { data: [
      { snapshot_id: 'current', lineage_status: 'CURRENT', source_analysis_revision: 1, source_analysis_run_id: 'run_a' },
      { snapshot_id: 'bad', lineage_status: 'UNKNOWN', source_analysis_revision: null, source_analysis_run_id: null },
    ] }
    if (url.endsWith('/alerts')) return { data: [
      { alert_id: 'history', lineage_status: 'HISTORICAL' }, { alert_id: 'missing' },
    ] }
    if (url.endsWith('/notifications')) return { data: [
      { notification_id: 'notice', lineage_status: 'CURRENT' }, { notification_id: 'legacy' },
    ] }
    if (url.endsWith('/forecast')) return { data: {
      case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
      input_snapshots: [{ snapshot_id: 'input', source_analysis_revision: 1, source_analysis_run_id: 'run_a' }],
    } }
    if (url.endsWith('/report/markdown')) return { data: {
      case_id: 'case_synthetic', markdown: '# Bound', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
    } }
    if (url.endsWith('/outbox/status')) return { data: {
      pending: 9, unread: 8, current_pending: 2, current_unread: 1, current_total: 3,
      current_simulated_sent: 1, current_failed: 0, historical_or_unbound_total: 6,
    } }
    throw new Error(`Unexpected URL ${url}`)
  })
  const post = vi.spyOn(apiClient, 'post').mockResolvedValue({ data: {
    case_id: 'case_synthetic', source_analysis_revision: 1, source_analysis_run_id: 'run_a',
    latest_snapshot: { source_analysis_revision: 1, source_analysis_run_id: 'run_a' }, alerts: [{ alert_id: 'missing' }],
  } })
  const caseDetail = await api.getAnalysisCase('case_synthetic')
  expect(caseDetail.analysis_revision).toBe(1)
  expect(caseDetail.analysis_run_id).toBe('run_a')
  expect(api.caseAnalysisIdentity(caseDetail)).toBe(api.caseAnalysisIdentity(cases.configBump))
  const snapshots = await api.listCaseSnapshots('case_synthetic')
  expect(snapshots.map((item) => item.lineage_status)).toEqual(['CURRENT', 'UNBOUND_LEGACY'])
  expect(snapshots[0].source_analysis_run_id).toBe('run_a')
  expect((await api.listCaseAlerts('case_synthetic')).map((item) => item.lineage_status)).toEqual(['HISTORICAL', 'UNBOUND_LEGACY'])
  expect((await api.listCaseNotifications('case_synthetic')).map((item) => item.lineage_status)).toEqual(['CURRENT', 'UNBOUND_LEGACY'])
  const forecast = await api.getCaseForecast('case_synthetic')
  expect(api.sameAnalysisPair(caseDetail, forecast)).toBe(true)
  expect(forecast.input_snapshots[0].source_analysis_run_id).toBe('run_a')
  const markdown = await api.getCaseMarkdownReport('case_synthetic')
  expect(api.sameAnalysisPair(caseDetail, markdown)).toBe(true)
  const status = await api.runCaseMonitoringCheck('case_synthetic')
  expect(api.sameAnalysisPair(caseDetail, status)).toBe(true)
  expect(status.latest_snapshot.source_analysis_run_id).toBe('run_a')
  expect(status.alerts[0].lineage_status).toBe('UNBOUND_LEGACY')
  const outbox = await api.getNotificationOutboxStatus()
  expect(outbox.current_pending).toBe(2)
  expect(outbox.current_unread).toBe(1)
  expect(outbox.pending).toBe(9)
  get.mockRestore()
  post.mockRestore()
})
