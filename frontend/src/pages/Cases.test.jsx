// @vitest-environment jsdom
import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  getCase: vi.fn(),
  getCaseEvidenceReviewQueue: vi.fn(),
  getCaseEvidenceReviewTimeline: vi.fn(),
  getCaseEvidenceReviewAuditSummary: vi.fn(),
  getCaseEvidenceReviewHistory: vi.fn(),
  reviewCaseEvidence: vi.fn(),
  getCaseEvidenceSummary: vi.fn(),
  getCaseEvidenceJobs: vi.fn(),
  getCaseEvidenceCoverage: vi.fn(),
}))

vi.mock('../api/sentigraphApi.js', async (importOriginal) => ({
  ...(await importOriginal()),
  ...apiMocks,
}))

import { Cases, EvidenceReviewQueuePanel } from './Cases.jsx'
import { guidedAnalysisPair, makeGuidedEvidenceScope } from '../utils/guidedCaseFlow.js'

const currentCase = { case_id: 'case_exact_audit', evidence_item_count: 1, updated_at: '2026-09-29T00:00:00Z' }
const evidenceId = 'evidence_exact_audit'
const queueItem = {
  evidence_id: evidenceId,
  evidence_type: 'comment',
  platform: 'public_web',
  title: 'Synthetic queue row',
  comment_text_preview: 'Synthetic preview only',
  review_status: 'review_needed',
  review_reason_codes: [],
  trust_label: 'unverified',
  verification_status: 'needs_review',
  provenance_type: 'manual',
  source_url_present: false,
  duplicate_count: 1,
  user_attestation_required: false,
}
const queue = { queue_items: [queueItem], queue_count: 1, review_needed_count: 1 }
const emptyCaseTimeline = { case_id: currentCase.case_id, entries: [], total_review_events: 0 }
const emptyExactTimeline = { ...emptyCaseTimeline, evidence_id: evidenceId }
const audit = { case_id: currentCase.case_id, total_review_events: 0 }

function reviewEntry() {
  return {
    review_event_id: 'review_event_1', evidence_id: evidenceId, case_id: currentCase.case_id,
    decision: 'approve', previous_review_status: 'review_needed', new_review_status: 'approved',
    reason_code: 'decision:approve', reviewer_label: 'qa', reviewed_at: '2026-09-29T00:01:00Z',
    note: 'sanitized synthetic note', analysis_effect: 'included_in_analysis',
  }
}

async function renderReviewPanel() {
  render(<EvidenceReviewQueuePanel currentCase={currentCase} />)
  await screen.findByRole('button', { name: 'View review history' })
}

function decisionButton(label) {
  // Ant Design inserts a visual space between two Chinese characters.
  const name = label.length === 2 ? new RegExp([...label].join('\\s*')) : label
  return screen.getByRole('button', { name })
}

let syntheticNetworkAttempts
beforeEach(() => {
  syntheticNetworkAttempts = 0
  for (const key of ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']) {
    vi.stubGlobal(key, function blockedNetwork() { syntheticNetworkAttempts += 1; throw new Error('Synthetic-only Cases test') })
  }
  const getComputedStyle = window.getComputedStyle.bind(window)
  vi.spyOn(window, 'getComputedStyle').mockImplementation((element) => getComputedStyle(element))
  vi.stubGlobal('ResizeObserver', class {
    observe() {}
    unobserve() {}
    disconnect() {}
  })
  vi.stubGlobal('matchMedia', (query) => ({
    matches: false, media: query, onchange: null, addListener: vi.fn(), removeListener: vi.fn(),
    addEventListener: vi.fn(), removeEventListener: vi.fn(), dispatchEvent: vi.fn(),
  }))
  for (const mock of Object.values(apiMocks)) mock.mockReset()
  apiMocks.getCase.mockResolvedValue(currentCase)
  apiMocks.getCaseEvidenceReviewQueue.mockResolvedValue(queue)
  apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue(emptyCaseTimeline)
  apiMocks.getCaseEvidenceReviewAuditSummary.mockResolvedValue(audit)
  apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue(emptyExactTimeline)
  apiMocks.reviewCaseEvidence.mockResolvedValue({ summary: queue, review_status: 'approved' })
  apiMocks.getCaseEvidenceSummary.mockResolvedValue({})
  apiMocks.getCaseEvidenceJobs.mockResolvedValue([])
  apiMocks.getCaseEvidenceCoverage.mockResolvedValue({})
})

afterEach(() => {
  cleanup()
  expect(syntheticNetworkAttempts).toBe(0)
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
})

describe('guided Cases review and explicit Run UI', () => {
  const scope = makeGuidedEvidenceScope({ case_id: currentCase.case_id, evidence_ids: [evidenceId], query: 'Synthetic query' })
  function persisted(review_status = 'not_reviewed') {
    return { ...currentCase, status: 'draft', platforms: ['youtube'],
      evidence_items: [{ ...queueItem, case_id: currentCase.case_id, review_status }] }
  }
  function view(value = persisted(), extras = {}) {
    return render(<Cases currentCase={value} guidedCaseFlow={{ scope, last_run_pair: null }} {...extras} />)
  }
  it.each(['not_reviewed', 'review_needed', 'needs_more_source', 'rejected', 'duplicate_merged'])(
    'has no guided Run shortcut for unresolved or unusable %s', async (status) => {
      const onRunCase = vi.fn()
      view(persisted(status), { onRunCase })
      await screen.findByTestId('guided-case-review')
      expect(screen.getByRole('button', { name: 'Run analysis' }).disabled).toBe(true)
      fireEvent.click(screen.getByRole('button', { name: 'Run analysis' }))
      expect(onRunCase).not.toHaveBeenCalled()
    },
  )
  it.each(['approved', 'marked_weak'])('runs only on the separate explicit button for usable %s', async (status) => {
    let resolveRun
    const onRunCase = vi.fn(() => new Promise((resolve) => { resolveRun = resolve }))
    view(persisted(status), { onRunCase })
    const button = await screen.findByRole('button', { name: 'Run analysis' })
    expect(button.disabled).toBe(false)
    fireEvent.focus(button); fireEvent.mouseEnter(button)
    expect(onRunCase).not.toHaveBeenCalled()
    act(() => { fireEvent.click(button); fireEvent.click(button) })
    expect(onRunCase).toHaveBeenCalledExactlyOnceWith(currentCase.case_id, 'analysis')
    await act(async () => resolveRun(undefined))
  })
  it('does not expose the unguided list/manual/import Run for an active guided case', async () => {
    const onRunCase = vi.fn()
    view(persisted('approved'), { cases: [{ ...currentCase, title: 'Guided synthetic case', platforms: [] }], onRunCase })
    const legacy = await screen.findByRole('button', { name: /运\s*行/ })
    expect(legacy.disabled).toBe(true)
    expect(screen.queryByText('Manual Evidence')).toBeNull()
    fireEvent.click(legacy)
    expect(onRunCase).not.toHaveBeenCalled()
  })
  it('blocks Run synchronously during a review decision and waits for fresh persisted readback', async () => {
    let resolveDecision
    apiMocks.reviewCaseEvidence.mockReturnValue(new Promise((resolve) => { resolveDecision = resolve }))
    apiMocks.getCase.mockResolvedValue(persisted('not_reviewed'))
    const onRunCase = vi.fn(), onCaseReady = vi.fn()
    view(persisted('approved'), { onRunCase, onCaseReady })
    await screen.findByRole('button', { name: 'View review history' })
    act(() => { fireEvent.click(decisionButton('重置')); fireEvent.click(screen.getByRole('button', { name: 'Run analysis' })) })
    expect(onRunCase).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).toHaveBeenCalledTimes(1)
    await act(async () => resolveDecision({ summary: queue, review_status: 'not_reviewed' }))
    await waitFor(() => expect(onCaseReady).toHaveBeenCalledWith(persisted('not_reviewed'), { review_readback: true }))
  })
  it('shows current-result navigation only for the exact completed successful pair', async () => {
    const value = { ...persisted('approved'), status: 'completed', analysis_revision: 1,
      analysis_run_id: 'run_ui1', analysis_result: {}, report: {} }
    const onNavigate = vi.fn()
    view(value, { guidedCaseFlow: { scope, last_run_pair: guidedAnalysisPair(value) }, onNavigate })
    const button = await screen.findByRole('button', { name: 'View current result' })
    expect(button.disabled).toBe(false)
    fireEvent.click(button)
    expect(onNavigate).toHaveBeenCalledExactlyOnceWith('analysis')
  })
  it('fences an old review response across case A→B→A and never applies it to the reopened case', async () => {
    let resolveDecision
    apiMocks.reviewCaseEvidence.mockReturnValue(new Promise((resolve) => { resolveDecision = resolve }))
    const onCaseReady = vi.fn(), onReviewPendingChange = vi.fn()
    const rendered = render(<EvidenceReviewQueuePanel currentCase={currentCase} onCaseReady={onCaseReady}
      onReviewPendingChange={onReviewPendingChange} />)
    await screen.findByRole('button', { name: 'View review history' })
    act(() => { fireEvent.click(decisionButton('通过')); fireEvent.click(decisionButton('通过')) })
    expect(apiMocks.reviewCaseEvidence).toHaveBeenCalledTimes(1)
    rendered.rerender(<EvidenceReviewQueuePanel currentCase={{ ...currentCase, case_id: 'case_b' }} onCaseReady={onCaseReady}
      onReviewPendingChange={onReviewPendingChange} />)
    rendered.rerender(<EvidenceReviewQueuePanel currentCase={currentCase} onCaseReady={onCaseReady}
      onReviewPendingChange={onReviewPendingChange} />)
    await act(async () => resolveDecision({ summary: queue, review_status: 'approved' }))
    expect(onCaseReady).not.toHaveBeenCalled()
    expect(apiMocks.getCase).not.toHaveBeenCalled()
  })
})

describe('EvidenceReviewQueuePanel exact persisted-item history', () => {
  it('does not read exact history on mount or review-note typing', async () => {
    await renderReviewPanel()
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(screen.queryByText('Selected evidence review history')).toBeNull()
    fireEvent.change(screen.getByPlaceholderText(/Optional audit note/), { target: { value: 'Synthetic note' } })
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('does not treat focus, hover or a queue-row click as a history request', async () => {
    await renderReviewPanel()
    const historyButton = screen.getByRole('button', { name: 'View review history' })
    fireEvent.focus(historyButton)
    fireEvent.mouseEnter(historyButton)
    fireEvent.click(screen.getByText('Synthetic preview only'))
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('reads only the exact target after the explicit view action and never mutates', async () => {
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue({
      case_id: currentCase.case_id, evidence_id: evidenceId,
      entries: [reviewEntry()], total_review_events: 1,
    })
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('sanitized synthetic note')
    expect(apiMocks.getCaseEvidenceReviewHistory).toHaveBeenCalledExactlyOnceWith(currentCase.case_id, evidenceId)
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(screen.queryByText('Synthetic preview only', { exact: false })).not.toBeNull()
  })

  it('preserves delegated audit attribution without claiming personal inspection', async () => {
    const note = 'Authorized delegated mark_weak; the user did not personally inspect this evidence item.'
    const entry = {
      ...reviewEntry(), decision: 'mark_weak', new_review_status: 'marked_weak',
      reason_code: 'decision:mark_weak', reviewer_label: 'local_human_reviewer', note,
    }
    apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue({
      ...emptyCaseTimeline, entries: [entry], total_review_events: 1,
    })
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue({
      ...emptyExactTimeline, entries: [entry], total_review_events: 1,
    })
    await renderReviewPanel()
    await screen.findByText(note)
    expect(screen.getByText('local_human_reviewer').textContent).toBe('local_human_reviewer')
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    const notice = screen.getByText(/Review history records explicit decisions/).textContent
    expect(notice).toContain('authorized delegated actions')
    expect(notice).toContain('Recorded reviewer labels do not verify identity')
    expect(notice).toContain('does not prove the user personally inspected the evidence')
    expect(notice).toContain('Official API provenance does not certify factual truth')
    expect(screen.queryByText(/Audit records only capture human review decisions/)).toBeNull()
    fireEvent.change(screen.getByPlaceholderText(/Optional audit note/), { target: { value: 'Unsaved synthetic note' } })
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await waitFor(() => expect(screen.getAllByText(note)).toHaveLength(2))
    expect(screen.getAllByText('local_human_reviewer')).toHaveLength(2)
    expect(screen.getAllByText('mark_weak')).toHaveLength(2)
    expect(screen.getAllByRole('columnheader', { name: 'Recorded reviewer label' })).toHaveLength(2)
    expect(apiMocks.getCaseEvidenceReviewHistory).toHaveBeenCalledExactlyOnceWith(currentCase.case_id, evidenceId)
    expect(apiMocks.getCaseEvidenceReviewTimeline).toHaveBeenCalledExactlyOnceWith(currentCase.case_id)
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it.each([
    ['absent', undefined], ['null', null], ['empty', ''], ['blank', '   '],
  ])('shows an %s reviewer label neutrally in both history views', async (_, reviewerLabel) => {
    const entry = { ...reviewEntry(), reviewer_label: reviewerLabel }
    if (reviewerLabel === undefined) delete entry.reviewer_label
    apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue({
      ...emptyCaseTimeline, entries: [entry], total_review_events: 1,
    })
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue({
      ...emptyExactTimeline, entries: [entry], total_review_events: 1,
    })
    await renderReviewPanel()
    await screen.findByText('Not recorded')
    expect(screen.queryByText('local_human_reviewer')).toBeNull()
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await waitFor(() => expect(screen.getAllByText('Not recorded')).toHaveLength(2))
    expect(screen.queryByText('local_human_reviewer')).toBeNull()
    expect(apiMocks.getCaseEvidenceReviewHistory).toHaveBeenCalledExactlyOnceWith(currentCase.case_id, evidenceId)
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('displays a nonblank recorded reviewer label exactly as stored', async () => {
    const reviewerLabel = '  delegated reviewer  '
    const entry = { ...reviewEntry(), reviewer_label: reviewerLabel }
    apiMocks.getCaseEvidenceReviewTimeline.mockResolvedValue({
      ...emptyCaseTimeline, entries: [entry], total_review_events: 1,
    })
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue({
      ...emptyExactTimeline, entries: [entry], total_review_events: 1,
    })
    await renderReviewPanel()
    expect((await screen.findByText('delegated reviewer')).textContent).toBe(reviewerLabel)
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await waitFor(() => expect(screen.getAllByText('delegated reviewer')).toHaveLength(2))
    expect(screen.getAllByText('delegated reviewer').map((label) => label.textContent)).toEqual([reviewerLabel, reviewerLabel])
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('shows loading, then a valid empty history distinct from missing evidence', async () => {
    let resolveHistory
    apiMocks.getCaseEvidenceReviewHistory.mockReturnValue(new Promise((resolve) => { resolveHistory = resolve }))
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    expect(screen.getByText('Loading review history...')).not.toBeNull()
    await act(async () => resolveHistory(emptyExactTimeline))
    expect(screen.getByText('No review history for this persisted evidence item.')).not.toBeNull()
    expect(screen.queryByText('Persisted evidence item not found')).toBeNull()
  })

  it('fails closed visibly for a missing exact item or mismatched response', async () => {
    apiMocks.getCaseEvidenceReviewHistory.mockRejectedValueOnce({ response: { status: 404 } })
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('Persisted evidence item not found')
    expect(screen.queryByText('No review history for this persisted evidence item.')).toBeNull()
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValueOnce({ ...emptyExactTimeline, evidence_id: 'other_item' })
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('Review history request failed')
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('shows a safe generic request failure without echoing raw error text', async () => {
    apiMocks.getCaseEvidenceReviewHistory.mockRejectedValue(new Error('private-synthetic-error-marker'))
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('Review history request failed')
    expect(screen.queryByText('private-synthetic-error-marker')).toBeNull()
  })

  it.each([
    ['通过', 'approve'], ['驳回', 'reject'], ['标记为弱证据', 'mark_weak'],
    ['要求补充来源', 'request_more_source'], ['合并重复', 'merge_duplicate'], ['重置', 'reset_review'],
  ])('mutates only on an explicit %s decision click', async (label, decision) => {
    await renderReviewPanel()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    fireEvent.click(decisionButton(label))
    await waitFor(() => expect(apiMocks.reviewCaseEvidence).toHaveBeenCalledExactlyOnceWith(
      currentCase.case_id, evidenceId,
      { decision, reviewer_label: 'local_human_reviewer', notes: undefined },
    ))
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
  })

  it('refreshes already-open same-item history after a successful explicit decision', async () => {
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('No review history for this persisted evidence item.')
    apiMocks.getCaseEvidenceReviewHistory.mockResolvedValue({
      case_id: currentCase.case_id, evidence_id: evidenceId,
      entries: [reviewEntry()], total_review_events: 1,
    })
    fireEvent.click(decisionButton('通过'))
    await screen.findByText('sanitized synthetic note')
    expect(apiMocks.getCaseEvidenceReviewHistory).toHaveBeenCalledTimes(2)
  })

  it('keeps closed history closed after a successful decision', async () => {
    await renderReviewPanel()
    fireEvent.click(decisionButton('通过'))
    await waitFor(() => expect(apiMocks.reviewCaseEvidence).toHaveBeenCalledTimes(1))
    expect(apiMocks.getCaseEvidenceReviewHistory).not.toHaveBeenCalled()
    expect(screen.queryByText('Selected evidence review history')).toBeNull()
  })

  it('does not reopen history closed while a review decision is pending', async () => {
    await renderReviewPanel()
    fireEvent.click(screen.getByRole('button', { name: 'View review history' }))
    await screen.findByText('No review history for this persisted evidence item.')
    let resolveReview
    apiMocks.reviewCaseEvidence.mockReturnValue(new Promise((resolve) => { resolveReview = resolve }))
    fireEvent.click(decisionButton('通过'))
    fireEvent.click(screen.getByRole('button', { name: 'Close history' }))
    await act(async () => resolveReview({ summary: queue, review_status: 'approved' }))
    await waitFor(() => expect(apiMocks.getCase).toHaveBeenCalledTimes(1))
    expect(apiMocks.getCaseEvidenceReviewHistory).toHaveBeenCalledTimes(1)
    expect(screen.queryByText('Selected evidence review history')).toBeNull()
  })
})
