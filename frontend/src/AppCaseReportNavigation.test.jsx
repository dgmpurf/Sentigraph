// @vitest-environment jsdom
// Synthetic frontend mocked-API integration only; not actual API or browser E2E.
import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => Object.fromEntries([
  'createAnalysisCase', 'disableCaseMonitoring', 'enableCaseMonitoring', 'expandKeywords',
  'generateRecommendation', 'generateSummary', 'getAnalysisCase', 'getAlerts', 'getCaseForecast',
  'getAnalysisResult', 'getCaseMonitoringConfig', 'getCaseMarkdownReport',
  'getNotificationOutboxStatus', 'getPlatformStatus', 'getPropagation', 'getSchedulerStatus',
  'getVisualizationData', 'listCaseAlerts', 'listCaseNotifications', 'listAnalysisCases',
  'listCaseSnapshots', 'markNotificationRead', 'runDueMonitoringJobs', 'runAnalysisCase',
  'runCaseForecast', 'runCaseMonitoringCheck', 'simulateSendNotification',
  'simulateSendPendingNotifications', 'attachCaseEvidence', 'commitCaseEvidenceImport',
  'getCase', 'getCaseEvidenceCoverage', 'getCaseEvidenceJobs', 'getCaseEvidenceReviewAuditSummary',
  'getCaseEvidenceReviewHistory', 'getCaseEvidenceReviewQueue', 'getCaseEvidenceReviewTimeline',
  'getCaseEvidenceSummary', 'previewCaseEvidenceImport', 'reviewCaseEvidence',
].map((name) => [name, vi.fn()])))

vi.mock('./api/sentigraphApi.js', async (importOriginal) => ({ ...(await importOriginal()), ...apiMocks }))
vi.mock('./components/layout/AppShell.jsx', () => ({
  AppShell: ({ children, activePage, caseTitle, loading, alertsCount, onNavigate }) => <div>
    <output data-testid="active-page">{activePage}</output>
    <output data-testid="current-case-title">{caseTitle || 'none'}</output>
    <output data-testid="app-loading">{String(loading)}</output>
    <output data-testid="current-alert-count">{alertsCount}</output>
    <button onClick={() => onNavigate('cases')}>Navigate cases</button>
    <button onClick={() => onNavigate('summary')}>Navigate summary</button>
    <button onClick={() => onNavigate('publicDemoGuide')}>Navigate elsewhere</button>
    {children}
  </div>,
}))
vi.mock('./pages/PublicDemoGuide.jsx', () => ({ PublicDemoGuide: () => <div>Synthetic static page</div> }))
vi.mock('./pages/Cases.jsx', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, Cases: (props) => <>
    <button onClick={() => props.onCaseReady({ ...props.currentCase, status: 'draft',
      analysis_revision: 2, analysis_run_id: null, report: null, analysis_result: null,
      visualization_data: null, markdown_available: false })}>Invalidate current persisted report</button>
    <actual.Cases {...props} />
  </> }
})

import App from './App.jsx'

function completedCase(letter) {
  return { case_id: `case_${letter}`, project_id: `synthetic_project_${letter}`,
    title: `Synthetic case ${letter.toUpperCase()}`, keyword: `Synthetic ${letter}`,
    status: 'completed', platforms: ['mock'], analysis_revision: 1, analysis_run_id: `run_${letter}_1`,
    analysis_input_source: 'case_evidence_items', evidence_item_count: 0, evidence_items: [],
    analysis_result: { summary: `Synthetic analysis ${letter}`, analysis_input_source: 'case_evidence_items' },
    report: { summary: `Synthetic report ${letter.toUpperCase()}`, report_language: 'zh-CN' },
    visualization_data: {}, markdown_available: true }
}
const CASE_A = completedCase('a')
const CASE_B = completedCase('b')

function deferred() {
  let resolve, reject
  const promise = new Promise((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
async function resolveRequest(request, value) {
  await act(async () => { request.resolve(value); await request.promise })
}
async function rejectRequest(request) {
  await act(async () => {
    request.reject(new Error('Synthetic failure: private exception details must not be rendered'))
    await request.promise.catch(() => {})
  })
}
async function openCases() {
  window.history.replaceState(null, '', '#/demo')
  const rendered = render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Navigate cases' }))
  await screen.findByRole('row', { name: /Synthetic case A/ })
  await waitFor(() => expect(screen.getByTestId('app-loading').textContent).toBe('false'))
  return rendered
}
function clickCase(record, action = '报告') {
  const row = screen.getByRole('row', { name: new RegExp(record.title) })
  fireEvent.click(within(row).getByRole('button', { name: action }))
}
async function expectCurrentReport(record) {
  await waitFor(() => expect(screen.getByTestId('active-page').textContent).toBe('summary'))
  await screen.findByText(record.case_id, { exact: true })
  expect(screen.getByTestId('current-case-title').textContent).toBe(record.title)
  expect(screen.getAllByText(record.report.summary, { exact: true }).length).toBeGreaterThan(0)
  expect(screen.getByTestId('app-loading').textContent).toBe('false')
}

let networkAttempts
beforeEach(() => {
  networkAttempts = 0
  for (const key of ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']) {
    vi.stubGlobal(key, function blockedNetwork() { networkAttempts += 1; throw new Error('Synthetic-only test') })
  }
  vi.stubGlobal('matchMedia', (query) => ({ matches: false, media: query, addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {}, dispatchEvent() {} }))
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
  const style = window.getComputedStyle.bind(window)
  vi.spyOn(window, 'getComputedStyle').mockImplementation((element) => style(element))
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
  for (const mock of Object.values(apiMocks)) mock.mockReset().mockResolvedValue({})
  for (const key of ['listCaseSnapshots', 'listCaseAlerts', 'listCaseNotifications', 'getCaseEvidenceJobs']) {
    apiMocks[key].mockResolvedValue([])
  }
  apiMocks.listAnalysisCases.mockResolvedValue([CASE_A, CASE_B])
  apiMocks.getCaseForecast.mockResolvedValue(null)
  apiMocks.getAnalysisCase.mockImplementation(async (id) => id === CASE_A.case_id ? CASE_A : CASE_B)
  apiMocks.getCaseEvidenceReviewQueue.mockResolvedValue({ queue_items: [] })
  apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue({ entries: [] })
})
afterEach(() => {
  cleanup()
  expect(networkAttempts).toBe(0)
  for (const key of ['runAnalysisCase', 'runCaseMonitoringCheck', 'runCaseForecast', 'getCaseMarkdownReport',
    'attachCaseEvidence', 'commitCaseEvidenceImport', 'previewCaseEvidenceImport', 'reviewCaseEvidence']) {
    expect(apiMocks[key]).not.toHaveBeenCalled()
  }
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
  window.history.replaceState(null, '', '/')
})

describe('App → actual Cases report action → actual SummaryReport (synthetic APIs)', () => {
  it('opens a completed matching case and its persisted report', async () => {
    await openCases()
    clickCase(CASE_A)
    await expectCurrentReport(CASE_A)
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledExactlyOnceWith(CASE_A.case_id)
  })

  it('keeps report B when response A resolves after B', async () => {
    const a = deferred(), b = deferred()
    apiMocks.getAnalysisCase.mockImplementation((id) => id === CASE_A.case_id ? a.promise : b.promise)
    await openCases()
    clickCase(CASE_A)
    clickCase(CASE_B)
    await resolveRequest(b, CASE_B)
    await expectCurrentReport(CASE_B)
    await resolveRequest(a, CASE_A)
    await expectCurrentReport(CASE_B)
    expect(screen.queryByText(CASE_A.report.summary, { exact: true })).toBeNull()
    expect(apiMocks.listCaseSnapshots).toHaveBeenCalledExactlyOnceWith(CASE_B.case_id)
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(2)
  })

  it('does not apply a response claiming a different case ID', async () => {
    apiMocks.getAnalysisCase.mockResolvedValue(CASE_B)
    await openCases()
    clickCase(CASE_A)
    await screen.findAllByText('The selected case report response does not match the requested case.')
    expect(screen.getByTestId('active-page').textContent).toBe('cases')
    expect(screen.getByTestId('current-case-title').textContent).toBe('none')
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
    expect(apiMocks.listCaseSnapshots).not.toHaveBeenCalled()
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(1)
  })

  it('settles loading on navigation and cannot force a late report back into view', async () => {
    const request = deferred()
    apiMocks.getAnalysisCase.mockReturnValue(request.promise)
    await openCases()
    clickCase(CASE_A)
    expect(screen.getByTestId('app-loading').textContent).toBe('true')
    fireEvent.click(screen.getByRole('button', { name: 'Navigate elsewhere' }))
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
    await resolveRequest(request, CASE_A)
    expect(screen.getByTestId('active-page').textContent).toBe('publicDemoGuide')
    expect(screen.getByTestId('current-case-title').textContent).toBe('none')
    expect(apiMocks.listCaseSnapshots).not.toHaveBeenCalled()
  })

  it('opens the valid report even when an auxiliary monitoring read fails, without invented data', async () => {
    apiMocks.listCaseSnapshots.mockRejectedValue(new Error('Synthetic monitoring unavailable'))
    apiMocks.listCaseAlerts.mockResolvedValue([{ case_id: CASE_B.case_id, lineage_status: 'CURRENT' }])
    await openCases()
    clickCase(CASE_A)
    await expectCurrentReport(CASE_A)
    expect(screen.getByTestId('current-alert-count').textContent).toBe('0')
    expect(screen.queryByText(/Synthetic monitoring unavailable/)).toBeNull()
    expect(apiMocks.listCaseSnapshots).toHaveBeenCalledTimes(1)
  })

  it('does not clear newer loading or replace a newer operation with a stale failure', async () => {
    const a = deferred(), b = deferred()
    apiMocks.getAnalysisCase.mockImplementation((id) => id === CASE_A.case_id ? a.promise : b.promise)
    await openCases()
    clickCase(CASE_A)
    clickCase(CASE_B)
    await rejectRequest(a)
    expect(screen.getByTestId('app-loading').textContent).toBe('true')
    expect(screen.queryByText('Unable to open the selected case report.')).toBeNull()
    await resolveRequest(b, CASE_B)
    await expectCurrentReport(CASE_B)
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(2)
  })

  it('keeps the active safe error and never replays either failed request', async () => {
    const a = deferred(), b = deferred()
    apiMocks.getAnalysisCase.mockImplementation((id) => id === CASE_A.case_id ? a.promise : b.promise)
    await openCases()
    clickCase(CASE_A)
    clickCase(CASE_B)
    await resolveRequest(b, { ...CASE_B, case_id: 'not_case_b' })
    await screen.findAllByText('The selected case report response does not match the requested case.')
    await rejectRequest(a)
    expect(screen.getAllByText('The selected case report response does not match the requested case.').length)
      .toBeGreaterThan(0)
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
    expect(screen.queryByText('Unable to open the selected case report.')).toBeNull()
    expect(screen.queryByText(/private exception details/)).toBeNull()
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(2)
  })

  it('lets a newer ordinary case-open invalidate a pending report-open', async () => {
    const a = deferred()
    apiMocks.getAnalysisCase.mockImplementation((id) => id === CASE_A.case_id ? a.promise : Promise.resolve(CASE_B))
    await openCases()
    clickCase(CASE_A)
    clickCase(CASE_B, '打开')
    await waitFor(() => expect(screen.getByTestId('current-case-title').textContent).toBe(CASE_B.title))
    await resolveRequest(a, CASE_A)
    expect(screen.getByTestId('active-page').textContent).toBe('cases')
    expect(screen.getByTestId('current-case-title').textContent).toBe(CASE_B.title)
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
  })

  it('lets a newer report-open invalidate an older ordinary case-open', async () => {
    const a = deferred()
    apiMocks.getAnalysisCase.mockImplementation((id) => id === CASE_A.case_id ? a.promise : Promise.resolve(CASE_B))
    await openCases()
    clickCase(CASE_A, '打开')
    clickCase(CASE_B)
    await expectCurrentReport(CASE_B)
    await resolveRequest(a, CASE_A)
    await expectCurrentReport(CASE_B)
  })

  it('rechecks navigation after a successful detail read while auxiliary work is pending', async () => {
    const monitoring = deferred()
    apiMocks.listCaseSnapshots.mockReturnValue(monitoring.promise)
    await openCases()
    clickCase(CASE_A)
    await waitFor(() => expect(apiMocks.listCaseSnapshots).toHaveBeenCalledWith(CASE_A.case_id))
    fireEvent.click(screen.getByRole('button', { name: 'Navigate elsewhere' }))
    await resolveRequest(monitoring, [])
    expect(screen.getByTestId('active-page').textContent).toBe('publicDemoGuide')
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
  })

  it('rechecks same-case analysis identity and retains invalid-report rules after auxiliary work', async () => {
    const monitoring = deferred()
    apiMocks.listCaseSnapshots.mockReturnValue(monitoring.promise)
    await openCases()
    clickCase(CASE_A)
    await waitFor(() => expect(apiMocks.listCaseSnapshots).toHaveBeenCalledWith(CASE_A.case_id))
    fireEvent.click(screen.getByRole('button', { name: 'Invalidate current persisted report' }))
    await resolveRequest(monitoring, [])
    expect(screen.getByTestId('active-page').textContent).toBe('cases')
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
    fireEvent.click(screen.getByRole('button', { name: 'Navigate summary' }))
    await screen.findByText('当前案例报告不再有效')
    expect(screen.queryByText(CASE_A.report.summary, { exact: true })).toBeNull()
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(1)
  })

  it.each(['draft', 'missing_report'])('does not present an invalid persisted report as current: %s', async (reason) => {
    apiMocks.getAnalysisCase.mockResolvedValue(reason === 'draft' ? { ...CASE_A, status: 'draft' }
      : { ...CASE_A, report: null })
    await openCases()
    clickCase(CASE_A)
    await screen.findByText('当前案例报告不再有效')
    expect(screen.queryByText(CASE_A.report.summary, { exact: true })).toBeNull()
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
  })

  it('invalidates report navigation on a browser hash change', async () => {
    const request = deferred()
    apiMocks.getAnalysisCase.mockReturnValue(request.promise)
    await openCases()
    clickCase(CASE_A)
    act(() => {
      window.history.replaceState(null, '', '#/demo')
      window.dispatchEvent(new HashChangeEvent('hashchange'))
    })
    await resolveRequest(request, CASE_A)
    expect(screen.getByTestId('active-page').textContent).toBe('publicDemoGuide')
    expect(screen.getByTestId('app-loading').textContent).toBe('false')
    expect(screen.getByTestId('current-case-title').textContent).toBe('none')
  })

  it('does not accept or start auxiliary work for a late response after unmount', async () => {
    const request = deferred()
    apiMocks.getAnalysisCase.mockReturnValue(request.promise)
    const rendered = await openCases()
    clickCase(CASE_A)
    rendered.unmount()
    await resolveRequest(request, CASE_A)
    expect(apiMocks.listCaseSnapshots).not.toHaveBeenCalled()
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(1)
  })
})
