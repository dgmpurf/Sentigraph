// @vitest-environment jsdom
import React from 'react'
import { App as AntApp } from 'antd'
import { cleanup, fireEvent, render, screen } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { guidedAnalysisPair, makeGuidedEvidenceScope } from '../utils/guidedCaseFlow.js'

vi.mock('../components/charts/SentimentTrendChart.jsx', () => ({ SentimentTrendChart: () => null }))
import { AnalysisResult } from './AnalysisResult.jsx'

const scope = makeGuidedEvidenceScope({ case_id: 'case_result', evidence_ids: ['ev_result'], query: 'Synthetic Event' })
function completed() {
  return {
    case_id: 'case_result', status: 'completed', analysis_revision: 3, analysis_run_id: 'analysis_r3',
    platforms: ['youtube'], evidence_item_count: 1, analysis_input_source: 'case_evidence_items',
    evidence_items: [{ case_id: 'case_result', evidence_id: 'ev_result', review_status: 'marked_weak',
      source_type: 'youtube', evidence_type: 'comment', acquisition_mode: 'official_api_public',
      provenance_type: 'official_api', trust_label: 'low', verification_status: 'verified_by_official_api' }],
    analysis_result: { summary: 'SYNTHETIC CURRENT RESULT', analysis_input_source: 'case_evidence_items',
      evidence_item_count: 1, evidence_review_excluded_count: 0 },
    report: { summary: 'Synthetic case report' }, visualization_data: {},
  }
}
function view(caseDetail = completed(), flow = { scope, last_run_pair: guidedAnalysisPair(completed()) }) {
  return render(<AntApp><AnalysisResult currentCase={caseDetail} guidedCaseFlow={flow}
    analysis={{ summary: 'STALE PROJECT PAYLOAD' }} summary={{ summary: 'STALE REPORT' }} /></AntApp>)
}

let attempts
beforeEach(() => {
  attempts = 0
  for (const key of ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']) {
    vi.stubGlobal(key, () => { attempts += 1; throw new Error('No network in synthetic result test') })
  }
  vi.stubGlobal('matchMedia', (query) => ({ matches: false, media: query, addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {}, dispatchEvent() {} }))
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
  const getComputedStyle = window.getComputedStyle.bind(window)
  vi.spyOn(window, 'getComputedStyle').mockImplementation((element) => getComputedStyle(element))
})
afterEach(() => { cleanup(); expect(attempts).toBe(0); vi.restoreAllMocks(); vi.unstubAllGlobals() })

describe('guided current-result display', () => {
  it('shows the exact current case and analysis pair from the completed case rather than stale props', () => {
    view()
    expect(screen.getByText('case_id=case_result')).toBeTruthy()
    expect(screen.getByText('analysis_revision=3')).toBeTruthy()
    expect(screen.getByText('analysis_run_id=analysis_r3')).toBeTruthy()
    expect(screen.getByText('Current guided result')).toBeTruthy()
    expect(screen.getByText('SYNTHETIC CURRENT RESULT')).toBeTruthy()
    expect(screen.queryByText('STALE PROJECT PAYLOAD')).toBeNull()
    expect(screen.queryByText('STALE REPORT')).toBeNull()
    expect(screen.getByText('Analysis: Offline')).toBeTruthy()
    expect(screen.getByText('LLM: Mock')).toBeTruthy()
    expect(screen.getByText('evidence_items: 1')).toBeTruthy()
    expect(screen.getByText('official_api: 1')).toBeTruthy()
    expect(screen.getByText('marked_weak: 1')).toBeTruthy()
    expect(screen.queryByText(/not necessarily analysis input/)).toBeNull()
  })
  it.each([
    { case_id: 'case_other' }, { analysis_revision: 4 }, { analysis_run_id: 'analysis_other' },
    { analysis_run_id: null, run_id: 'analysis_r3' }, { analysis_revision: null },
    { status: 'draft' }, { analysis_result: null }, { report: null },
  ])('does not label a stale/wrong/absent pair as current: %j', (patch) => {
    view({ ...completed(), ...patch })
    expect(screen.getByText('当前案例分析不再有效')).toBeTruthy()
    expect(screen.queryByText('Current guided result')).toBeNull()
    expect(screen.queryByText('SYNTHETIC CURRENT RESULT')).toBeNull()
  })
  it('invalidates display on fresh review/reset without any automatic analysis action', () => {
    const value = completed()
    const flow = { scope, last_run_pair: guidedAnalysisPair(value) }
    const rendered = view(value, flow)
    value.evidence_items = [{ ...value.evidence_items[0], review_status: 'not_reviewed' }]
    rendered.rerender(<AntApp><AnalysisResult currentCase={value} guidedCaseFlow={flow} /></AntApp>)
    expect(screen.getByText('当前案例分析不再有效')).toBeTruthy()
    expect(screen.queryByRole('button', { name: /Run analysis/ })).toBeNull()
    fireEvent.mouseEnter(screen.getByText('当前案例分析不再有效'))
    expect(attempts).toBe(0)
  })
  it('needs a successful explicit guided run receipt, not merely an already-completed case', () => {
    view(completed(), { scope, last_run_pair: null })
    expect(screen.queryByText('Current guided result')).toBeNull()
  })
  it('preserves the legacy unguided analysis view', () => {
    render(<AntApp><AnalysisResult analysis={{ summary: 'Legacy offline summary' }} /></AntApp>)
    expect(screen.getAllByText('Legacy offline summary').length).toBeGreaterThan(0)
    expect(screen.getByText('LLM: Mock')).toBeTruthy()
    expect(screen.queryByText('Current guided result')).toBeNull()
  })
})
