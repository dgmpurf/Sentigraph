// @vitest-environment jsdom
import React, { StrictMode } from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import { makeGuidedEvidenceScope } from '../utils/guidedCaseFlow.js'

const controls = vi.hoisted(() => ({ appHarness: false }))
const apiMocks = vi.hoisted(() => Object.fromEntries([
  'attachSearchDiscoveryCandidates', 'attachYouTubeOfficialApiReviewedPublicDiscussion', 'createAnalysisCase',
  'getAnalysisCase', 'getCase', 'getExternalCollectorStatus', 'getExternalCollectorDiscovery',
  'getMockSearchDiscoveryCandidates', 'getSearchDiscoveryProviders', 'getYouTubeOfficialApiLiveCandidates',
  'getYouTubeOfficialApiLivePublicDiscussion', 'getYouTubeOfficialApiMockCandidates',
  'disableCaseMonitoring', 'enableCaseMonitoring', 'expandKeywords', 'generateRecommendation', 'generateSummary',
  'getAlerts', 'getCaseForecast', 'getAnalysisResult', 'getCaseMonitoringConfig', 'getCaseMarkdownReport',
  'getNotificationOutboxStatus', 'getPlatformStatus', 'getPropagation', 'getSchedulerStatus', 'getVisualizationData',
  'listCaseAlerts', 'listCaseNotifications', 'listAnalysisCases', 'listCaseSnapshots', 'markNotificationRead',
  'runDueMonitoringJobs', 'runAnalysisCase', 'runCaseForecast', 'runCaseMonitoringCheck',
  'simulateSendNotification', 'simulateSendPendingNotifications', 'getCaseEvidenceCoverage', 'getCaseEvidenceJobs',
  'getCaseEvidenceReviewAuditSummary', 'getCaseEvidenceReviewHistory', 'getCaseEvidenceReviewQueue',
  'getCaseEvidenceReviewTimeline', 'getCaseEvidenceSummary', 'reviewCaseEvidence',
].map((name) => [name, vi.fn()])))

vi.mock('../api/sentigraphApi.js', async (importOriginal) => ({ ...(await importOriginal()), ...apiMocks }))
vi.mock('../components/charts/SentimentTrendChart.jsx', () => ({ SentimentTrendChart: () => null }))
vi.mock('../components/layout/ErrorBoundary.jsx', () => ({ ErrorBoundary: ({ children }) => children }))
vi.mock('../components/layout/AppShell.jsx', () => ({
  AppShell: ({ children, onNavigate, onRefresh }) => <div>
    <button onClick={() => onNavigate('searchDiscovery')}>Navigate search</button>
    <button onClick={() => onNavigate('cases')}>Navigate cases</button>
    <button onClick={() => onNavigate('analysis')}>Navigate result</button>
    <button onClick={onRefresh}>Refresh current</button>
    {children}
  </div>,
}))
vi.mock('./PublicDemoGuide.jsx', () => ({ PublicDemoGuide: () => <div>Synthetic bootstrap</div> }))
vi.mock('./SearchDiscovery.jsx', async (importOriginal) => {
  const actual = await importOriginal()
  return { ...actual, SearchDiscovery: (props) => controls.appHarness ? <div>
    <span data-testid="synthetic-opened-case">{props.currentCase?.case_id || 'none'}</span>
    <button onClick={() => props.onOpenGuidedEvidenceReview({
      case_id: 'case_a', evidence_ids: ['ev_a'], query: 'Synthetic A', body_text: 'must-discard',
    })}>Open synthetic receipt</button>
    <button onClick={() => props.onOpenCase('case_b')}>Open synthetic other case</button>
  </div> : <actual.SearchDiscovery {...props} /> }
})

import { SearchDiscovery } from './SearchDiscovery.jsx'
import App from '../App.jsx'

const LIVE_LABEL = 'Synthetic official lane'
const PROVIDER = { provider_id: 'youtube_official_api_live', provider_type: 'youtube_official_api',
  display_name: LIVE_LABEL, live_fetch_enabled: true }
const CASE_A = { case_id: 'case_a', title: 'Synthetic A', keyword: 'Synthetic A', status: 'draft',
  evidence_item_count: 1, evidence_items: [{ case_id: 'case_a', evidence_id: 'ev_a',
    review_status: 'not_reviewed', trust_label: 'medium', verification_status: 'verified_by_official_api',
    source_type: 'youtube', provenance_type: 'official_api', acquisition_mode: 'official_api_public',
    evidence_type: 'comment' }] }
const CASE_B = { ...CASE_A, case_id: 'case_b', title: 'Synthetic B', keyword: 'Synthetic B', evidence_items: [] }
const BATCH = { query: 'Synthetic A', candidates: [{ candidate_id: 'video_candidate', query: 'Synthetic A',
  title: 'Synthetic metadata', url: 'https://www.youtube.com/watch?v=current_001', provider: 'youtube_official_api_live',
  platform_hint: 'youtube', status: 'pending_review' }], provider_statuses: [], safe_mode: {} }
const DISCUSSION = { video_id: 'current_001', item_count: 1, generated_at: '2026-10-03T00:00:00Z', review_batch_safe_hash: 'a'.repeat(64),
  review_item_safe_hashes: { discussion_one: 'b'.repeat(64) }, items: [{ discussion_id: 'discussion_one',
    video_id: 'current_001', body_text: 'Synthetic provider body stays in local preview', provider: 'youtube_official_api',
    platform_hint: 'youtube', comment_id: 'synthetic_comment', published_at: '2026-10-03T00:00:00Z',
    like_count: 0, reply_count: 0, status: 'pending_review', safety_notes: [] }], safe_mode: {} }
const ATTACH = { case_id: 'case_a', video_id: 'current_001', status: 'attached', attached_discussion_count: 1,
  attached_evidence_items: [{ ...CASE_A.evidence_items[0], body_text: 'DO NOT NAVIGATE THIS BODY' }],
  review_binding_mode: 'selected_item_v1', safe_mode: { server_side_refetch: true } }
const QUEUE_ITEM = { ...CASE_A.evidence_items[0], title: 'Synthetic review row', platform: 'youtube',
  review_reason_codes: [], duplicate_count: 1, source_url_present: true }

function deferred() {
  let resolve, reject
  const promise = new Promise((yes, no) => { resolve = yes; reject = no })
  return { promise, resolve, reject }
}
async function chooseLane() {
  await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalled())
  fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
  fireEvent.click(await screen.findByText(LIVE_LABEL, { exact: true }))
  fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic A' } })
}
async function chooseCase(record = CASE_A) {
  fireEvent.mouseDown(screen.getAllByRole('combobox')[1])
  const options = await screen.findAllByText(`${record.title} · ${record.case_id}`, { exact: true })
  fireEvent.click(options.at(-1))
}
async function searchAndSelectDiscussion() {
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
  await screen.findByText('Synthetic metadata')
  fireEvent.click(screen.getByRole('button', { name: '接受' }))
  fireEvent.click(screen.getByRole('button', { name: /Load provider-backed public discussion/ }))
  await screen.findByText(DISCUSSION.items[0].body_text, { exact: true })
  fireEvent.click(screen.getByRole('button', { name: 'Accept discussion_one' }))
}
function renderSearch(props = {}, strict = false) {
  const page = <SearchDiscovery cases={[CASE_A, CASE_B]} liveRouteFrontendEnabled
    publicDiscussionReviewFrontendEnabled publicDiscussionAttachFrontendEnabled {...props} />
  return render(strict ? <StrictMode>{page}</StrictMode> : page)
}
function completedCase() {
  return { ...CASE_A, status: 'completed', analysis_revision: 4, analysis_run_id: 'run_a4',
    evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'approved' }],
    analysis_result: { summary: 'SYNTHETIC GUIDED COMPLETION', analysis_input_source: 'case_evidence_items' },
    analysis_input_source: 'case_evidence_items', report: { summary: 'Synthetic report' }, visualization_data: {} }
}
async function openHarnessCase(value = CASE_A) {
  controls.appHarness = true
  apiMocks.getAnalysisCase.mockResolvedValue(value)
  window.history.replaceState(null, '', '#/demo')
  render(<App />)
  fireEvent.click(screen.getByRole('button', { name: 'Navigate search' }))
  fireEvent.click(await screen.findByRole('button', { name: 'Open synthetic receipt' }))
  await screen.findByTestId('guided-case-review')
  await screen.findByRole('button', { name: /通\s*过/ })
}

let networkAttempts
beforeEach(() => {
  controls.appHarness = false
  networkAttempts = 0
  for (const key of ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']) {
    vi.stubGlobal(key, function blockedSyntheticNetwork() { networkAttempts += 1; throw new Error('Synthetic-only test') })
  }
  vi.stubGlobal('matchMedia', (query) => ({ matches: false, media: query, addListener() {}, removeListener() {},
    addEventListener() {}, removeEventListener() {}, dispatchEvent() {} }))
  vi.stubGlobal('ResizeObserver', class { observe() {} unobserve() {} disconnect() {} })
  const style = window.getComputedStyle.bind(window)
  vi.spyOn(window, 'getComputedStyle').mockImplementation((element) => style(element))
  vi.spyOn(window, 'scrollTo').mockImplementation(() => {})
  HTMLElement.prototype.scrollIntoView = vi.fn()
  for (const mock of Object.values(apiMocks)) mock.mockReset().mockResolvedValue({})
  for (const key of ['listAnalysisCases', 'listCaseSnapshots', 'listCaseAlerts', 'listCaseNotifications', 'getCaseEvidenceJobs']) {
    apiMocks[key].mockResolvedValue([])
  }
  apiMocks.getCaseForecast.mockResolvedValue(null)
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([PROVIDER])
  apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: false, exists: false })
  apiMocks.createAnalysisCase.mockResolvedValue(CASE_A)
  apiMocks.getAnalysisCase.mockResolvedValue(CASE_A)
  apiMocks.getCase.mockResolvedValue(CASE_A)
  apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue(BATCH)
  apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockResolvedValue(DISCUSSION)
  apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mockResolvedValue(ATTACH)
  apiMocks.getCaseEvidenceReviewQueue.mockResolvedValue({ queue_items: [QUEUE_ITEM] })
  apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue({ case_id: 'case_a', entries: [] })
  apiMocks.runAnalysisCase.mockResolvedValue(completedCase())
  apiMocks.reviewCaseEvidence.mockResolvedValue({ summary: { queue_items: [QUEUE_ITEM] }, review_status: 'approved' })
})
afterEach(() => {
  cleanup()
  expect(networkAttempts).toBe(0)
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
  window.history.replaceState(null, '', '/')
})

describe('guided SearchDiscovery explicit creation and safe receipt navigation', () => {
  it('does not create, attach, review or Run on mount, typing, hover or focus, even under StrictMode', async () => {
    renderSearch({}, true)
    await chooseLane()
    fireEvent.focus(screen.getByRole('button', { name: 'Create case from query' }))
    fireEvent.mouseEnter(screen.getByRole('button', { name: 'Create case from query' }))
    expect(apiMocks.createAnalysisCase).not.toHaveBeenCalled()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
  })
  it('creates one server-owned draft from the normalized official query, adopts it, and never Runs', async () => {
    const onCaseReady = vi.fn()
    renderSearch({ onCaseReady })
    await chooseLane()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: '  Synthetic   A  ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Create case from query' }))
    await screen.findByText(/Created draft case=case_a/)
    expect(apiMocks.createAnalysisCase).toHaveBeenCalledExactlyOnceWith({
      keyword: 'Synthetic A', title: 'Synthetic A', platforms: ['youtube'], report_language: 'zh-CN',
    })
    expect(onCaseReady).toHaveBeenCalledExactlyOnceWith(CASE_A)
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
    await searchAndSelectDiscussion()
    expect(screen.getByRole('button', { name: 'Attach reviewed public discussion to case' }).disabled).toBe(false)
  })
  it('rejects blank and excessive input without a create request', async () => {
    renderSearch()
    await chooseLane()
    for (const query of ['  ', 'x'.repeat(121)]) {
      fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: query } })
      const button = screen.getByRole('button', { name: 'Create case from query' })
      expect(button.disabled).toBe(true)
      fireEvent.click(button)
    }
    expect(apiMocks.createAnalysisCase).not.toHaveBeenCalled()
  })
  it('synchronously suppresses duplicate creation clicks', async () => {
    const pending = deferred()
    apiMocks.createAnalysisCase.mockReturnValue(pending.promise)
    renderSearch()
    await chooseLane()
    const button = screen.getByRole('button', { name: 'Create case from query' })
    act(() => { fireEvent.click(button); fireEvent.click(button) })
    expect(apiMocks.createAnalysisCase).toHaveBeenCalledTimes(1)
    await act(async () => pending.resolve(CASE_A))
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
  })
  it.each(['success', 'error'])('discards a stale creation %s after query A→B→A without rollback or retry', async (outcome) => {
    const pending = deferred(), onCaseReady = vi.fn(), onRefreshCases = vi.fn()
    apiMocks.createAnalysisCase.mockReturnValue(pending.promise)
    renderSearch({ onCaseReady, onRefreshCases })
    await chooseLane()
    fireEvent.click(screen.getByRole('button', { name: 'Create case from query' }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic B' } })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic A' } })
    await act(async () => outcome === 'success' ? pending.resolve(CASE_A) : pending.reject(new Error('PRIVATE ERROR')))
    expect(onCaseReady).not.toHaveBeenCalled()
    expect(onRefreshCases).not.toHaveBeenCalled()
    expect(screen.queryByText(/Created draft/)).toBeNull()
    expect(screen.queryByText('PRIVATE ERROR')).toBeNull()
    expect(apiMocks.createAnalysisCase).toHaveBeenCalledTimes(1)
  })
  it('suppresses creation adoption after deliberate target changes and unmount', async () => {
    const pending = deferred(), onCaseReady = vi.fn()
    apiMocks.createAnalysisCase.mockReturnValue(pending.promise)
    const page = renderSearch({ onCaseReady })
    await chooseLane()
    fireEvent.click(screen.getByRole('button', { name: 'Create case from query' }))
    await chooseCase(CASE_B)
    await chooseCase(CASE_A)
    page.unmount()
    await act(async () => pending.resolve(CASE_A))
    expect(onCaseReady).not.toHaveBeenCalled()
    expect(apiMocks.createAnalysisCase).toHaveBeenCalledTimes(1)
  })
  it('shows a generic create failure without echoing raw errors or automatically retrying', async () => {
    apiMocks.createAnalysisCase.mockRejectedValue(new Error('PRIVATE CREATION ERROR'))
    renderSearch()
    await chooseLane()
    fireEvent.click(screen.getByRole('button', { name: 'Create case from query' }))
    await screen.findByText(/Unable to create the case/)
    expect(screen.queryByText('PRIVATE CREATION ERROR')).toBeNull()
    expect(apiMocks.createAnalysisCase).toHaveBeenCalledTimes(1)
  })
  it('does not infer a live target from cases[0] or an opened current case', async () => {
    renderSearch({ currentCase: CASE_B })
    await chooseLane()
    await searchAndSelectDiscussion()
    expect(screen.getByRole('button', { name: 'Attach reviewed public discussion to case' }).disabled).toBe(true)
    fireEvent.click(screen.getByRole('button', { name: 'Use opened current case' }))
    expect(screen.getByRole('button', { name: 'Attach reviewed public discussion to case' }).disabled).toBe(false)
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })
  it('navigates only on Open Evidence review with immutable identifiers, never provider bodies', async () => {
    const onOpenGuidedEvidenceReview = vi.fn(), onRunCase = vi.fn()
    renderSearch({ onOpenGuidedEvidenceReview, onRunCase })
    await chooseLane(); await chooseCase(); await searchAndSelectDiscussion()
    fireEvent.click(screen.getByRole('button', { name: 'Attach reviewed public discussion to case' }))
    const button = await screen.findByRole('button', { name: 'Open Evidence review' })
    await waitFor(() => expect(button.disabled).toBe(false))
    expect(onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(onRunCase).not.toHaveBeenCalled()
    fireEvent.click(button)
    const scope = onOpenGuidedEvidenceReview.mock.calls[0][0]
    expect(scope).toEqual({ case_id: 'case_a', evidence_ids: ['ev_a'], query: 'Synthetic A', step: 'evidence_review' })
    expect(Object.isFrozen(scope)).toBe(true)
    expect(Object.isFrozen(scope.evidence_ids)).toBe(true)
    expect(JSON.stringify(scope)).not.toMatch(/BODY|body_text|author|credential|envelope/)
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledExactlyOnceWith('Synthetic A', 5)
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledExactlyOnceWith('current_001', 3)
    expect(Object.keys(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mock.calls[0][2]).sort()).toEqual([
      'review_batch_safe_hash', 'review_binding_mode', 'selected_discussion_ids', 'selected_discussion_safe_hashes',
    ])
    onOpenGuidedEvidenceReview.mockClear()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic B' } })
    await chooseCase(CASE_B)
    expect(onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'Open Evidence review' }))
    expect(onOpenGuidedEvidenceReview).toHaveBeenCalledExactlyOnceWith(scope)
    expect(onRunCase).not.toHaveBeenCalled()
  })
  it('late attach receipt remains case A after target B, and does not auto-navigate or Run', async () => {
    const pending = deferred(), onOpenGuidedEvidenceReview = vi.fn(), onRunCase = vi.fn()
    apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mockReturnValue(pending.promise)
    renderSearch({ onOpenGuidedEvidenceReview, onRunCase })
    await chooseLane(); await chooseCase(); await searchAndSelectDiscussion()
    fireEvent.click(screen.getByRole('button', { name: 'Attach reviewed public discussion to case' }))
    await chooseCase(CASE_B)
    await act(async () => pending.resolve(ATTACH))
    await waitFor(() => expect(screen.getByRole('button', { name: 'Open Evidence review' }).disabled).toBe(false))
    expect(onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'Open Evidence review' }))
    expect(onOpenGuidedEvidenceReview.mock.calls[0][0].case_id).toBe('case_a')
    expect(onRunCase).not.toHaveBeenCalled()
  })
})

describe('App guided case integration with synthetic API replacements', () => {
  it.each(['available', 'unavailable'])('ordinary case B open restores list and monitoring hydration when auxiliary data is %s, without business writes', async (availability) => {
    await openHarnessCase()
    fireEvent.click(screen.getByRole('button', { name: 'Navigate search' }))
    const openOtherCase = await screen.findByRole('button', { name: 'Open synthetic other case' })
    const priorListReads = apiMocks.listAnalysisCases.mock.calls.length
    const priorSummaryCalls = apiMocks.generateSummary.mock.calls.length
    const priorRecommendationCalls = apiMocks.generateRecommendation.mock.calls.length
    apiMocks.getAnalysisCase.mockResolvedValue(CASE_B)
    if (availability === 'unavailable') {
      apiMocks.listCaseSnapshots.mockRejectedValueOnce(new Error('Synthetic auxiliary read unavailable'))
    }

    fireEvent.click(openOtherCase)
    await waitFor(() => {
      expect(apiMocks.getAnalysisCase).toHaveBeenLastCalledWith('case_b')
      expect(apiMocks.listAnalysisCases).toHaveBeenCalledTimes(priorListReads + 1)
      for (const reader of ['listCaseSnapshots', 'listCaseAlerts', 'getCaseMonitoringConfig',
        'listCaseNotifications', 'getCaseForecast']) {
        expect(apiMocks[reader]).toHaveBeenCalledExactlyOnceWith('case_b')
      }
    })
    await act(async () => { await Promise.resolve() })
    expect(screen.getByTestId('synthetic-opened-case').textContent).toBe('case_b')
    expect(screen.queryByText('Unable to open the selected case.')).toBeNull()
    expect(apiMocks.getAnalysisCase.mock.invocationCallOrder.at(-1))
      .toBeLessThan(apiMocks.listAnalysisCases.mock.invocationCallOrder.at(-1))
    expect(apiMocks.listAnalysisCases.mock.invocationCallOrder.at(-1))
      .toBeLessThan(apiMocks.listCaseSnapshots.mock.invocationCallOrder.at(-1))
    for (const action of ['createAnalysisCase', 'runAnalysisCase', 'reviewCaseEvidence',
      'attachSearchDiscoveryCandidates', 'attachYouTubeOfficialApiReviewedPublicDiscussion',
      'getYouTubeOfficialApiLiveCandidates', 'getYouTubeOfficialApiLivePublicDiscussion',
      'runCaseForecast', 'runCaseMonitoringCheck', 'enableCaseMonitoring', 'disableCaseMonitoring',
      'simulateSendNotification', 'simulateSendPendingNotifications', 'markNotificationRead',
      'getCaseMarkdownReport']) {
      expect(apiMocks[action]).not.toHaveBeenCalled()
    }
    expect(apiMocks.generateSummary).toHaveBeenCalledTimes(priorSummaryCalls)
    expect(apiMocks.generateRecommendation).toHaveBeenCalledTimes(priorRecommendationCalls)
  })

  it('opens the immutable receipt case for persisted human review, then requires a separate explicit Run', async () => {
    await openHarnessCase()
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledWith('case_a')
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
    expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(true)
    const reviewed = { ...CASE_A, evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'approved' }] }
    apiMocks.getCase.mockResolvedValue(reviewed)
    fireEvent.click(screen.getByRole('button', { name: /通\s*过/ }))
    await waitFor(() => expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(false))
    expect(apiMocks.reviewCaseEvidence.mock.calls[0].slice(0, 2)).toEqual(['case_a', 'ev_a'])
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
    const button = screen.getByRole('button', { name: 'Run analysis' })
    act(() => { fireEvent.click(button); fireEvent.click(button) })
    await screen.findByText('Current guided result')
    expect(apiMocks.runAnalysisCase).toHaveBeenCalledExactlyOnceWith('case_a')
    expect(screen.getByText('analysis_revision=4')).toBeTruthy()
    expect(screen.getByText('analysis_run_id=run_a4')).toBeTruthy()
  })
  it('review/reset after analysis clears the successful pair and never automatically reruns', async () => {
    await openHarnessCase({ ...CASE_A, evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'marked_weak' }] })
    fireEvent.click(screen.getByRole('button', { name: 'Run analysis' }))
    await screen.findByText('Current guided result')
    fireEvent.click(screen.getByRole('button', { name: 'Navigate cases' }))
    await screen.findByRole('button', { name: /重\s*置/ })
    apiMocks.getCase.mockResolvedValue(CASE_A)
    fireEvent.click(screen.getByRole('button', { name: /重\s*置/ }))
    await waitFor(() => expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(true))
    fireEvent.click(screen.getByRole('button', { name: 'Navigate result' }))
    await screen.findByText('当前案例分析不再有效')
    expect(screen.queryByText('Current guided result')).toBeNull()
    expect(apiMocks.runAnalysisCase).toHaveBeenCalledTimes(1)
  })
  it('does not apply or navigate a late Run result after an explicit case B open intent', async () => {
    const pending = deferred()
    apiMocks.runAnalysisCase.mockReturnValue(pending.promise)
    await openHarnessCase({ ...CASE_A, evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'approved' }] })
    fireEvent.click(screen.getByRole('button', { name: 'Run analysis' }))
    fireEvent.click(screen.getByRole('button', { name: 'Navigate search' }))
    apiMocks.getAnalysisCase.mockResolvedValue(CASE_B)
    fireEvent.click(await screen.findByRole('button', { name: 'Open synthetic other case' }))
    await waitFor(() => expect(apiMocks.getAnalysisCase).toHaveBeenCalledWith('case_b'))
    await act(async () => pending.resolve(completedCase()))
    expect(screen.queryByText('Current guided result')).toBeNull()
    expect(screen.getByRole('button', { name: 'Open synthetic other case' })).toBeTruthy()
    expect(apiMocks.runAnalysisCase).toHaveBeenCalledTimes(1)
  })
  it('Refresh current performs only a case read, not a guided Run or analysis-result GET', async () => {
    await openHarnessCase({ ...CASE_A, evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'approved' }] })
    const priorAnalysisReads = apiMocks.getAnalysisResult.mock.calls.length
    fireEvent.click(screen.getByRole('button', { name: 'Refresh current' }))
    await waitFor(() => expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(2))
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
    expect(apiMocks.getAnalysisResult).toHaveBeenCalledTimes(priorAnalysisReads)
    expect(apiMocks.getCaseMarkdownReport).not.toHaveBeenCalled()
  })
  it('a failed persisted review readback stays blocked until an explicit successful refresh', async () => {
    await openHarnessCase({ ...CASE_A, evidence_items: [{ ...CASE_A.evidence_items[0], review_status: 'approved' }] })
    apiMocks.getCase.mockRejectedValue(new Error('Synthetic readback unavailable'))
    fireEvent.click(screen.getByRole('button', { name: /重\s*置/ }))
    await screen.findByText(/Review decision failed/)
    expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(true)
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
    apiMocks.getAnalysisCase.mockResolvedValue(CASE_A)
    fireEvent.click(screen.getByRole('button', { name: 'Refresh current' }))
    await waitFor(() => expect(apiMocks.getAnalysisCase).toHaveBeenCalledTimes(2))
    expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(true)
    expect(apiMocks.runAnalysisCase).not.toHaveBeenCalled()
  })
})
