// @vitest-environment jsdom
import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  getCase: vi.fn(),
  attachCaseEvidence: vi.fn(),
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

import { Cases, EvidenceReviewQueuePanel, ManualEvidencePanel } from './Cases.jsx'
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

describe('manual evidence explicit submission and exact persisted review scope', () => {
  const manualCaseId = 'case_manual_synthetic'
  const newManualId = 'manual_added_synthetic'
  const reviewLabel = '复核本次新增证据'
  const duplicateNotice = '已保存，但无法唯一确认本次新增证据；请在正常证据复核队列中核对。'
  const uncertainNotice = '提交可能已保存，但尚未完成持久化确认；请在正常证据复核队列中核对，不要重复提交。'

  function fixtures() {
    const prior = { ...queueItem, case_id: manualCaseId, evidence_id: 'manual_prior_synthetic', acquisition_mode: 'manual_url' }
    const recent = { ...prior, evidence_id: 'manual_recent_synthetic' }
    const added = { ...prior, evidence_id: newManualId, platform: 'manual_url', source_type: 'public_web',
      evidence_type: 'comment', url: null, source_url: null, title: null, body_text: null,
      comment_text: 'Synthetic public comment; no collected data.', review_status: 'not_reviewed' }
    const baseline = { ...currentCase, case_id: manualCaseId, keyword: 'Synthetic baseline keyword',
      evidence_item_count: 2, evidence_items: [prior, recent] }
    // The submitted prop is stale, and the new item is not the final receipt/readback row.
    const propCase = { ...baseline, keyword: 'Stale prop keyword', evidence_item_count: 1, evidence_items: [prior] }
    const readback = { ...baseline, keyword: '  Synthetic  current\n keyword  ',
      evidence_item_count: 3, evidence_items: [added, recent, prior] }
    const receipt = { ...readback, status: 'attached', evidence_items: [recent, added, prior],
      source_distribution: {}, evidence_type_counts: {}, trust_summary: {}, deduplication_summary: {}, warnings: [] }
    return { baseline, propCase, readback, receipt, added }
  }

  function configure(value = fixtures()) {
    apiMocks.getCase.mockResolvedValueOnce(value.baseline).mockResolvedValue(value.readback)
    apiMocks.attachCaseEvidence.mockResolvedValue(value.receipt)
    return value
  }

  function view(value = fixtures(), props = {}) {
    const callbacks = { onCaseReady: vi.fn(), onOpenGuidedEvidenceReview: vi.fn(), onRunCase: vi.fn(), ...props }
    const rendered = render(<ManualEvidencePanel currentCase={value.propCase} {...callbacks} />)
    return { ...callbacks, rendered }
  }

  function enterManualText() {
    fireEvent.change(screen.getByPlaceholderText('手动粘贴公开评论或回复内容'), {
      target: { value: 'Synthetic public comment; no collected data.' },
    })
  }

  async function submitManual(times = 1) {
    const form = screen.getByRole('button', { name: '添加到案例' }).closest('form')
    await act(async () => {
      for (let index = 0; index < times; index += 1) fireEvent.submit(form)
    })
  }

  async function settledManual() {
    await waitFor(() => expect(screen.getByRole('button', { name: '添加到案例' }).classList.contains('ant-btn-loading')).toBe(false))
  }

  function expectReviewBlocked(onOpenGuidedEvidenceReview) {
    const review = screen.queryByRole('button', { name: reviewLabel })
    if (review) {
      expect(review.disabled).toBe(true)
      fireEvent.click(review)
    }
    expect(onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(screen.queryByRole('button', { name: '添加后运行分析' })).toBeNull()
  }

  function deferred() {
    let resolve
    const promise = new Promise((done) => { resolve = done })
    return { promise, resolve }
  }

  it('does no baseline read, attach, review or Run on mount, typing, focus or hover', async () => {
    const callbacks = view()
    enterManualText()
    fireEvent.change(screen.getByPlaceholderText('https://example.com/public-post'), {
      target: { value: 'https://example.com/synthetic-public-post' },
    })
    const submit = screen.getByRole('button', { name: '添加到案例' })
    fireEvent.focus(submit)
    fireEvent.mouseEnter(submit)
    await act(async () => {})
    expect(apiMocks.getCase).not.toHaveBeenCalled()
    expect(apiMocks.attachCaseEvidence).not.toHaveBeenCalled()
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
  })

  it('requires content before any baseline read or mutation', async () => {
    const callbacks = view()
    await submitManual()
    await screen.findByText('请至少填写标题、正文/摘要或评论内容之一。')
    expect(apiMocks.getCase).not.toHaveBeenCalled()
    expect(apiMocks.attachCaseEvidence).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
  })

  it('preserves the manual payload and opens only the uniquely persisted new ID on a separate click', async () => {
    const value = fixtures()
    Object.assign(value.added, { platform: 'synthetic_public', source_type: 'public_web', evidence_type: 'comment',
      url: 'https://example.com/synthetic-public-post', source_url: 'https://example.com/synthetic-public-post',
      title: 'Synthetic manual title', body_text: 'Synthetic public body', comment_text: 'Synthetic public comment' })
    configure(value)
    const callbacks = view(value)
    const fields = [
      ['https://example.com/public-post', ' https://example.com/synthetic-public-post '],
      ['manual_url / youtube / news_site', ' synthetic_public '],
      ['公开文章、视频或帖子标题', ' Synthetic manual title '],
      ['手动粘贴公开正文、摘要或视频描述', ' Synthetic public body '],
      ['手动粘贴公开评论或回复内容', ' Synthetic public comment '],
      ['公开作者名或来源名，可留空', ' Synthetic author '],
      ['回复所属评论 ID，可留空', ' parent_synthetic '],
      ['文章/视频/帖子 ID，可留空', ' root_synthetic '],
      ['公开作者 ID，可留空', ' author_synthetic '],
      ['2026-05-25T09:00:00Z', '2026-10-10T00:00:00Z'],
      ['zh-CN / en-US，可留空自动推断', ' zh-CN '],
    ]
    for (const [placeholder, text] of fields) fireEvent.change(screen.getByPlaceholderText(placeholder), { target: { value: text } })
    for (const [label, count] of [['点赞数', 4], ['回复数', 3], ['分享数', 2], ['浏览数', 1]]) {
      fireEvent.change(screen.getByRole('spinbutton', { name: label }), { target: { value: String(count) } })
    }
    fireEvent.click(screen.getByRole('checkbox', { name: '我确认该证据来源合法，且有权提交用于分析' }))
    await submitManual()
    await screen.findByText('手动证据已添加')
    expect(apiMocks.getCase).toHaveBeenNthCalledWith(1, manualCaseId)
    expect(apiMocks.getCase).toHaveBeenNthCalledWith(2, manualCaseId)
    expect(apiMocks.getCase).toHaveBeenCalledTimes(2)
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledExactlyOnceWith(manualCaseId, {
      source: {
        platform: 'synthetic_public', source_type: 'public_web', acquisition_mode: 'manual_url',
        source_name: 'Manual URL evidence', source_url: 'https://example.com/synthetic-public-post',
        access_scope: 'manual_url_user_provided', credential_present: false,
        notes: 'User-entered public evidence text only; Sentigraph does not fetch this URL.',
      },
      evidence_items: [{
        platform: 'synthetic_public', source_type: 'public_web', acquisition_mode: 'manual_url', evidence_type: 'comment',
        title: 'Synthetic manual title', body_text: 'Synthetic public body', comment_text: 'Synthetic public comment',
        parent_id: 'parent_synthetic', root_id: 'root_synthetic', author_id: 'author_synthetic', author_name: 'Synthetic author',
        url: 'https://example.com/synthetic-public-post', created_at: '2026-10-10T00:00:00Z',
        like_count: 4, reply_count: 3, share_count: 2, view_count: 1, language: 'zh-CN',
        content_visibility: 'public_or_user_provided', access_scope: 'manual_url_user_provided',
        provenance_type: 'manual_url', verification_status: 'needs_review',
        source_url: 'https://example.com/synthetic-public-post', source_url_present: true,
        source_platform_claim: 'synthetic_public', source_capture_method: 'manual_entry', user_attestation_required: true,
        user_attestation_text: 'User confirmed lawful source/right to submit this public-opinion evidence.',
        raw_data_safe: { manual_entry: true, no_url_fetch: true, no_scraping: true, user_attested_public_or_lawful_source: true },
      }],
    })
    const baselineOrder = apiMocks.getCase.mock.invocationCallOrder[0]
    const attachOrder = apiMocks.attachCaseEvidence.mock.invocationCallOrder[0]
    const readbackOrder = apiMocks.getCase.mock.invocationCallOrder[1]
    expect(baselineOrder).toBeLessThan(attachOrder)
    expect(attachOrder).toBeLessThan(readbackOrder)
    expect(callbacks.onCaseReady).toHaveBeenCalledWith(value.readback)
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expect(screen.queryByRole('button', { name: '添加后运行分析' })).toBeNull()
    const review = screen.getByRole('button', { name: reviewLabel })
    expect(review.disabled).toBe(false)
    fireEvent.focus(review)
    fireEvent.mouseEnter(review)
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    fireEvent.click(review)
    const expectedScope = makeGuidedEvidenceScope({ case_id: manualCaseId,
      evidence_ids: [newManualId], query: value.readback.keyword })
    expect(callbacks.onOpenGuidedEvidenceReview).toHaveBeenCalledExactlyOnceWith(expectedScope)
    expect(Object.keys(callbacks.onOpenGuidedEvidenceReview.mock.calls[0][0]).sort()).toEqual(['case_id', 'evidence_ids', 'query', 'step'])
    expect(expectedScope.query).toBe('Synthetic current keyword')
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
  })

  it('blocks a second submit synchronously while the fresh baseline is pending', async () => {
    const value = fixtures(), pending = deferred()
    apiMocks.getCase.mockReturnValueOnce(pending.promise).mockResolvedValue(value.readback)
    apiMocks.attachCaseEvidence.mockResolvedValue(value.receipt)
    const callbacks = view(value)
    enterManualText()
    await submitManual(2)
    expect(apiMocks.getCase).toHaveBeenCalledExactlyOnceWith(manualCaseId)
    expect(apiMocks.attachCaseEvidence).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    await act(async () => pending.resolve(value.baseline))
    await screen.findByText('手动证据已添加')
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1)
    expect(apiMocks.getCase).toHaveBeenCalledTimes(2)
  })

  it.each([
    ['wrong case', (value) => ({ ...value.baseline, case_id: 'case_foreign_synthetic' })],
    ['missing evidence list', (value) => ({ ...value.baseline, evidence_items: undefined })],
    ['duplicate baseline ID', (value) => ({ ...value.baseline, evidence_items: [value.baseline.evidence_items[0], value.baseline.evidence_items[0]] })],
    ['foreign baseline item', (value) => ({ ...value.baseline, evidence_items: [{ ...value.baseline.evidence_items[0], case_id: 'case_foreign_synthetic' }] })],
  ])('fails before attach for a fresh baseline with %s', async (_, changeBaseline) => {
    const value = fixtures()
    apiMocks.getCase.mockResolvedValue(changeBaseline(value))
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await settledManual()
    expect(apiMocks.getCase).toHaveBeenCalledExactlyOnceWith(manualCaseId)
    expect(apiMocks.attachCaseEvidence).not.toHaveBeenCalled()
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(screen.queryByText('手动证据已添加')).toBeNull()
  })

  it('does not attach or auto-retry after a fresh baseline read failure', async () => {
    apiMocks.getCase.mockRejectedValue(new Error('Synthetic baseline unavailable'))
    const callbacks = view()
    enterManualText()
    await submitManual()
    await settledManual()
    expect(apiMocks.getCase).toHaveBeenCalledTimes(1)
    expect(apiMocks.attachCaseEvidence).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(screen.queryByText('手动证据已添加')).toBeNull()
  })

  it.each([
    ['no new evidence ID', (value) => ({ ...value, receipt: { ...value.receipt, evidence_items: value.baseline.evidence_items }, readback: value.baseline })],
    ['two new evidence IDs', (value) => {
      const items = [...value.readback.evidence_items, { ...value.added, evidence_id: 'manual_second_added_synthetic' }]
      return { ...value, receipt: { ...value.receipt, evidence_items: items }, readback: { ...value.readback, evidence_items: items } }
    }],
    ['wrong receipt case', (value) => ({ ...value, receipt: { ...value.receipt, case_id: 'case_foreign_synthetic' } })],
    ['non-attached receipt status', (value) => ({ ...value, receipt: { ...value.receipt, status: 'empty' } })],
    ['duplicate receipt ID', (value) => ({ ...value, receipt: { ...value.receipt, evidence_items: [...value.receipt.evidence_items, value.added] } })],
    ['foreign receipt item', (value) => ({ ...value, receipt: { ...value.receipt, evidence_items: [{ ...value.added, case_id: 'case_foreign_synthetic' }, ...value.baseline.evidence_items] } })],
    ['wrong readback case', (value) => ({ ...value, readback: { ...value.readback, case_id: 'case_foreign_synthetic' } })],
    ['duplicate persisted new ID', (value) => ({ ...value, readback: { ...value.readback, evidence_items: [...value.readback.evidence_items, value.added] } })],
    ['different receipt and readback new IDs', (value) => ({ ...value, readback: { ...value.readback,
      evidence_items: [{ ...value.added, evidence_id: 'manual_different_added_synthetic' }, ...value.baseline.evidence_items] } })],
    ['deleted prior persisted ID', (value) => ({ ...value, readback: { ...value.readback, evidence_items: [value.added, value.baseline.evidence_items[0]] } })],
    ['foreign persisted new item', (value) => ({ ...value, readback: { ...value.readback,
      evidence_items: [{ ...value.added, case_id: 'case_foreign_synthetic' }, ...value.baseline.evidence_items] } })],
    ['non-manual acquisition mode', (value) => ({ ...value, readback: { ...value.readback,
      evidence_items: [{ ...value.added, acquisition_mode: 'official_api' }, ...value.baseline.evidence_items] } })],
    ['same text from a different concurrent platform', (value) => {
      const items = [{ ...value.added, platform: 'concurrent_other_platform' }, ...value.baseline.evidence_items]
      return { ...value, receipt: { ...value.receipt, evidence_items: items }, readback: { ...value.readback, evidence_items: items } }
    }],
    ['unsafe new navigation ID', (value) => {
      const items = [{ ...value.added, evidence_id: 'unsafe/id' }, ...value.baseline.evidence_items]
      return { ...value, receipt: { ...value.receipt, evidence_items: items }, readback: { ...value.readback, evidence_items: items } }
    }],
    ['empty actual keyword', (value) => ({ ...value, readback: { ...value.readback, keyword: '  ' } })],
    ['oversized actual keyword', (value) => ({ ...value, readback: { ...value.readback, keyword: 'x'.repeat(121) } })],
  ])('does not expose a confirmed scope for %s', async (_, change) => {
    const value = configure(change(fixtures()))
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await settledManual()
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1)
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expect(screen.queryByText('手动证据已添加')).toBeNull()
    expect(screen.queryByText(duplicateNotice) || screen.queryByText(uncertainNotice)).not.toBeNull()
  })

  it('reports a saved duplicate without a new-item scope or a success shortcut', async () => {
    const value = fixtures()
    value.receipt = { ...value.receipt, evidence_items: value.baseline.evidence_items, evidence_item_count: 2,
      deduplication_summary: { duplicate_items: 1 } }
    value.readback = value.baseline
    configure(value)
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await screen.findByText(duplicateNotice)
    expect(screen.queryByText('手动证据已添加')).toBeNull()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
  })

  it.each(['attach', 'readback'])('keeps a possibly saved %s failure uncertain and disables resubmission without retrying', async (stage) => {
    const value = fixtures()
    apiMocks.getCase.mockResolvedValueOnce(value.baseline)
    if (stage === 'attach') apiMocks.attachCaseEvidence.mockRejectedValue(new Error('Synthetic transport ambiguity'))
    else {
      apiMocks.attachCaseEvidence.mockResolvedValue(value.receipt)
      apiMocks.getCase.mockRejectedValue(new Error('Synthetic readback unavailable'))
    }
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await screen.findByText(uncertainNotice)
    expect(screen.getByRole('button', { name: '添加到案例' }).disabled).toBe(true)
    expect(screen.queryByText('手动证据已添加')).toBeNull()
    expect(screen.getByPlaceholderText('手动粘贴公开评论或回复内容').value).toBe('Synthetic public comment; no collected data.')
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    await submitManual(2)
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1)
    expect(apiMocks.getCase).toHaveBeenCalledTimes(stage === 'attach' ? 1 : 2)
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
  })

  it.each(['baseline', 'attach', 'readback'])('fences a pending %s response across case A→B→A', async (stage) => {
    const value = fixtures(), pending = deferred()
    apiMocks.getCase.mockResolvedValue(value.readback)
    apiMocks.getCase.mockResolvedValueOnce(value.baseline)
    apiMocks.attachCaseEvidence.mockResolvedValue(value.receipt)
    if (stage === 'baseline') apiMocks.getCase.mockReset().mockReturnValueOnce(pending.promise).mockResolvedValue(value.readback)
    if (stage === 'attach') apiMocks.attachCaseEvidence.mockReturnValueOnce(pending.promise)
    if (stage === 'readback') apiMocks.getCase.mockReturnValueOnce(pending.promise)
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await waitFor(() => expect(apiMocks.getCase).toHaveBeenCalledTimes(stage === 'readback' ? 2 : 1))
    if (stage !== 'baseline') await waitFor(() => expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1))
    callbacks.rendered.rerender(<ManualEvidencePanel currentCase={{ ...value.propCase, case_id: 'case_manual_b_synthetic' }} {...callbacks} />)
    callbacks.rendered.rerender(<ManualEvidencePanel currentCase={value.propCase} {...callbacks} />)
    await act(async () => pending.resolve(stage === 'baseline' ? value.baseline : stage === 'attach' ? value.receipt : value.readback))
    expect(apiMocks.getCase).toHaveBeenCalledTimes(stage === 'readback' ? 2 : 1)
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(stage === 'baseline' ? 0 : 1)
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expect(screen.queryByText('手动证据已添加')).toBeNull()
  })

  it.each(['baseline', 'attach', 'readback'])('ignores a pending %s response after unmount', async (stage) => {
    const value = fixtures(), pending = deferred()
    apiMocks.getCase.mockResolvedValueOnce(value.baseline).mockResolvedValue(value.readback)
    apiMocks.attachCaseEvidence.mockResolvedValue(value.receipt)
    if (stage === 'baseline') apiMocks.getCase.mockReset().mockReturnValueOnce(pending.promise).mockResolvedValue(value.readback)
    if (stage === 'attach') apiMocks.attachCaseEvidence.mockReturnValueOnce(pending.promise)
    if (stage === 'readback') apiMocks.getCase.mockReturnValueOnce(pending.promise)
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await waitFor(() => expect(apiMocks.getCase).toHaveBeenCalledTimes(stage === 'readback' ? 2 : 1))
    if (stage !== 'baseline') await waitFor(() => expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1))
    callbacks.rendered.unmount()
    await act(async () => pending.resolve(stage === 'baseline' ? value.baseline : stage === 'attach' ? value.receipt : value.readback))
    expect(apiMocks.getCase).toHaveBeenCalledTimes(stage === 'readback' ? 2 : 1)
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(stage === 'baseline' ? 0 : 1)
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
  })

  it('removes a confirmed review scope immediately when the active case changes', async () => {
    const value = configure()
    const callbacks = view(value)
    enterManualText()
    await submitManual()
    await screen.findByText('手动证据已添加')
    expect(screen.getByRole('button', { name: reviewLabel }).disabled).toBe(false)
    callbacks.rendered.rerender(<ManualEvidencePanel currentCase={{ ...value.propCase, case_id: 'case_manual_b_synthetic' }} {...callbacks} />)
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    callbacks.rendered.rerender(<ManualEvidencePanel currentCase={value.propCase} {...callbacks} />)
    expectReviewBlocked(callbacks.onOpenGuidedEvidenceReview)
    expect(apiMocks.attachCaseEvidence).toHaveBeenCalledTimes(1)
  })
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
