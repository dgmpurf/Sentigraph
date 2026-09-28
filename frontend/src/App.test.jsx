import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, expect, it, vi } from 'vitest'

const cases = vi.hoisted(() => {
  const completed = {
    case_id: 'case_synthetic', project_id: 'project_synthetic', keyword: 'Synthetic',
    status: 'completed', markdown_available: true,
    analysis_result: { summary: 'Completed synthetic analysis', analysis_input_source: 'case_evidence_items' },
    visualization_data: { risk_score: 12 },
    report: { overall_summary: 'Completed synthetic report' },
    monitoring_config: null,
  }
  return {
    completed,
    reviewed: {
      ...completed, status: 'draft', markdown_available: false,
      analysis_result: null, visualization_data: null, report: null,
    },
    rerun: {
      ...completed,
      analysis_result: { summary: 'Fresh synthetic analysis', analysis_input_source: 'case_evidence_items' },
      report: { overall_summary: 'Fresh synthetic report' },
    },
  }
})

const apiMocks = vi.hoisted(() => ({
  getCaseMarkdownReport: vi.fn().mockResolvedValue({ case_id: 'case_synthetic', markdown: '# Fresh' }),
}))

vi.mock('./api/sentigraphApi.js', async (importOriginal) => ({
  ...(await importOriginal()),
  getAnalysisResult: vi.fn().mockResolvedValue(null),
  getVisualizationData: vi.fn().mockResolvedValue(null),
  generateSummary: vi.fn().mockResolvedValue(null),
  generateRecommendation: vi.fn().mockResolvedValue(null),
  getPropagation: vi.fn().mockResolvedValue(null),
  getAlerts: vi.fn().mockResolvedValue({ alerts: [] }),
  getNotificationOutboxStatus: vi.fn().mockResolvedValue({}),
  listAnalysisCases: vi.fn().mockResolvedValue([]),
  getPlatformStatus: vi.fn().mockResolvedValue({ platforms: [] }),
  getSchedulerStatus: vi.fn().mockResolvedValue({}),
  listCaseSnapshots: vi.fn().mockResolvedValue([]),
  listCaseAlerts: vi.fn().mockResolvedValue([]),
  listCaseNotifications: vi.fn().mockResolvedValue([]),
  getCaseForecast: vi.fn().mockResolvedValue(null),
  getCaseMonitoringConfig: vi.fn().mockResolvedValue(null),
  ...apiMocks,
}))

vi.mock('./components/layout/AppShell.jsx', () => ({ AppShell: ({ children }) => <div>{children}</div> }))
vi.mock('./pages/Dashboard.jsx', () => ({
  Dashboard: ({ analysis, currentCase, markdownReport, onCaseReady, onGetMarkdownReport, recommendation, summary, visualization }) => (
    <div>
      <button onClick={() => onCaseReady(cases.completed)}>Apply completed</button>
      <button onClick={() => onCaseReady(cases.reviewed)}>Apply reviewed</button>
      <button onClick={() => onCaseReady(cases.rerun)}>Apply rerun</button>
      <button onClick={() => { void onGetMarkdownReport().catch(() => {}) }}>Get Markdown</button>
      <span data-testid="case-status">{currentCase?.status || 'none'}</span>
      <span data-testid="analysis-state">{analysis?.summary || 'none'}</span>
      <span data-testid="visualization-state">{visualization?.risk_score ?? 'none'}</span>
      <span data-testid="summary-state">{summary?.overall_summary || 'none'}</span>
      <span data-testid="recommendation-state">{recommendation?.overall_summary || 'none'}</span>
      <span data-testid="markdown-state">{markdownReport?.markdown || 'none'}</span>
    </div>
  ),
}))

import App from './App.jsx'

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
  apiMocks.getCaseMarkdownReport.mockClear()
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
