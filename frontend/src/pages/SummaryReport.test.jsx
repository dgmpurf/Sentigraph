import React from 'react'
import { App as AntApp } from 'antd'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../components/report/PublicOpinionReport.jsx', () => ({
  PublicOpinionReport: ({ report }) => <div>{report.overallSummary}</div>,
}))
vi.mock('../utils/clipboard.js', () => ({ copyTextToClipboard: vi.fn().mockResolvedValue(true) }))

import { SummaryReport } from './SummaryReport.jsx'

const report = {
  overall_summary: 'Fresh synthetic report',
  analysis_input_source: 'case_evidence_items',
  risk_score: 12,
  risk_level: 'low',
}
const analysis = { analysis_input_source: 'case_evidence_items', sentiment: {}, bot_score: {} }

beforeEach(() => {
  vi.stubGlobal('matchMedia', (query) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false },
  }))
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('SummaryReport case currentness', () => {
  it('hides old report data and Markdown actions for a reviewed draft case', () => {
    const onGetMarkdownReport = vi.fn()
    render(
      <AntApp>
        <SummaryReport
          analysis={analysis}
          currentCase={{ case_id: 'case_1', status: 'draft', report: null, markdown_available: false }}
          summary={{ ...report, overall_summary: 'Old report must be hidden' }}
          recommendation={report}
          markdownReport={{ case_id: 'case_1', markdown: 'Old Markdown' }}
          onGetMarkdownReport={onGetMarkdownReport}
        />
      </AntApp>,
    )
    expect(screen.getByText('当前案例报告不再有效')).toBeTruthy()
    expect(screen.getByText(/Run analysis 重新运行/)).toBeTruthy()
    expect(screen.queryByText('Old report must be hidden')).toBeNull()
    expect(screen.queryByTestId('summary-copy-markdown-button')).toBeNull()
    expect(screen.queryByTestId('summary-download-markdown-button')).toBeNull()
    expect(onGetMarkdownReport).not.toHaveBeenCalled()
  })

  it('restores current report and fetches Markdown through the guarded owner callback', async () => {
    const onGetMarkdownReport = vi.fn().mockResolvedValue({ case_id: 'case_1', markdown: '# Fresh', filename: 'fresh.md' })
    render(
      <AntApp>
        <SummaryReport
          analysis={analysis}
          currentCase={{ case_id: 'case_1', status: 'completed', report, markdown_available: true }}
          summary={report}
          recommendation={report}
          markdownReport={{ case_id: 'case_1', markdown: 'Old Markdown' }}
          onGetMarkdownReport={onGetMarkdownReport}
        />
      </AntApp>,
    )
    expect(screen.getByText('Fresh synthetic report')).toBeTruthy()
    expect(screen.getByText('analysis_input_source=case_evidence_items')).toBeTruthy()
    const copyButton = screen.getByTestId('summary-copy-markdown-button')
    expect(copyButton.disabled).toBe(false)
    expect(screen.getByTestId('summary-download-markdown-button').disabled).toBe(false)
    fireEvent.click(copyButton)
    await waitFor(() => expect(onGetMarkdownReport).toHaveBeenCalledTimes(1))
  })

  it.each(['case_evidence_items', 'case_raw_data', 'mock_data_fallback'])(
    'shows the fresh %s report source',
    (source) => {
      const sourcedReport = { ...report, analysis_input_source: source }
      render(
        <AntApp>
          <SummaryReport
            analysis={{ ...analysis, analysis_input_source: source }}
            currentCase={{ case_id: 'case_1', status: 'completed', report: sourcedReport, markdown_available: true }}
            summary={sourcedReport}
            recommendation={sourcedReport}
          />
        </AntApp>,
      )
      expect(screen.getByText(`analysis_input_source=${source}`)).toBeTruthy()
    },
  )
})
