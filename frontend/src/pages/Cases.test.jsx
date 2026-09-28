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
}))

vi.mock('../api/sentigraphApi.js', async (importOriginal) => ({
  ...(await importOriginal()),
  ...apiMocks,
}))

import { EvidenceReviewQueuePanel } from './Cases.jsx'

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

beforeEach(() => {
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
})

afterEach(() => {
  cleanup()
  vi.restoreAllMocks()
  vi.unstubAllGlobals()
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
