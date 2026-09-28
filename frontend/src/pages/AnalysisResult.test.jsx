import React from 'react'
import { App as AntApp } from 'antd'
import { cleanup, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../components/charts/SentimentTrendChart.jsx', () => ({
  SentimentTrendChart: () => <div>Sentiment trend fixture</div>,
}))

import { AnalysisResult } from './AnalysisResult.jsx'

const baseAnalysis = {
  summary: 'Fresh synthetic analysis',
  analysis_input_source: 'case_evidence_items',
  risk: { risk_score: 12, risk_level: 'low' },
  sentiment: { positive_ratio: 0.5, neutral_ratio: 0.3, negative_ratio: 0.2 },
  bot_score: { suspected_bot_ratio: 0, suspected_bot_comment_ratio: 0 },
  topics: [], bot_accounts: [], conflicts: [],
}

beforeEach(() => {
  const getComputedStyle = window.getComputedStyle.bind(window)
  vi.stubGlobal('getComputedStyle', (element) => getComputedStyle(element))
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    unobserve() {}
    disconnect() {}
  })
  vi.stubGlobal('matchMedia', (query) => ({
    matches: false, media: query, onchange: null,
    addListener() {}, removeListener() {}, addEventListener() {}, removeEventListener() {}, dispatchEvent() { return false },
  }))
})

afterEach(() => {
  cleanup()
  vi.unstubAllGlobals()
})

describe('AnalysisResult case currentness', () => {
  it('blocks a retained old analysis prop after Evidence review', () => {
    render(
      <AntApp>
        <AnalysisResult
          analysis={{ ...baseAnalysis, summary: 'Old analysis must be hidden' }}
          currentCase={{ case_id: 'case_1', status: 'draft', report: null, analysis_result: null }}
        />
      </AntApp>,
    )
    expect(screen.getByText('当前案例分析不再有效')).toBeTruthy()
    expect(screen.getByText(/Run analysis 重新运行/)).toBeTruthy()
    expect(screen.queryByText('Old analysis must be hidden')).toBeNull()
  })

  it.each(['case_evidence_items', 'case_raw_data', 'mock_data_fallback'])(
    'renders a fresh completed %s source distinctly',
    (source) => {
      const analysis = { ...baseAnalysis, analysis_input_source: source }
      render(
        <AntApp>
          <AnalysisResult
            analysis={analysis}
            currentCase={{ case_id: 'case_1', status: 'completed', report: { overall_summary: 'Current' }, analysis_result: analysis }}
          />
        </AntApp>,
      )
      expect(screen.getAllByText('Fresh synthetic analysis').length).toBeGreaterThan(0)
      expect(screen.getByText(`analysis_input_source=${source}`)).toBeTruthy()
    },
  )
})
