// @vitest-environment jsdom
import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  getCase: vi.fn(),
  attachCaseEvidence: vi.fn(),
  previewCaseEvidenceImport: vi.fn(),
  commitCaseEvidenceImport: vi.fn(),
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

import { Cases, EvidenceImportPanel, EvidenceReviewQueuePanel, ManualEvidencePanel } from './Cases.jsx'
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

describe('CSV complete small-batch identity and explicit persisted Review navigation', () => {
  const caseId = 'case_csv_synthetic', filename = 'synthetic.csv'
  const reviewLabel = '复核本次导入的证据'
  const previewButton = () => screen.getByRole('button', { name: '预览导入结果' })
  const commitButton = () => screen.getByRole('button', { name: '确认导入' })
  function fixtures(n = 1) {
    const items = Array.from({ length: n }, (_, index) => ({
      case_id: caseId, evidence_id: `csv_evidence_${index + 1}`, normalized_content_hash: String(index + 1).repeat(64),
      platform: 'uploaded_dataset', source_type: 'uploaded_dataset', acquisition_mode: 'user_upload',
      evidence_type: 'comment', title: `Synthetic CSV ${index + 1}`, body_text: null,
      comment_text: `Synthetic public CSV comment ${index + 1}`, url: null,
      review_status: 'not_reviewed', trust_label: 'unverified', verification_status: 'needs_review',
      duplicate_count: 1, review_reason_codes: [],
    }))
    const baseline = { case_id: caseId, keyword: 'Synthetic CSV query', status: 'draft', case_revision: 0,
      evidence_items: [], evidence_item_count: 0, raw_posts: [], raw_comments: [], raw_post_count: 0,
      raw_comment_count: 0, analysis_result: null, report: null, markdown_available: false,
      analysis_revision: null, analysis_run_id: null }
    const preview = { case_id: caseId, filename, status: 'preview_ready', detected_format: 'csv',
      detected_columns: ['platform', 'comment_text'], column_mapping: { comment_text: 'comment_text' },
      total_rows: n, valid_row_count: n, duplicate_row_count: 0, skipped_row_count: 0, warnings: [],
      preview_rows: items.map((item, index) => ({ ...item, row_number: index + 2, warnings: [] })) }
    const receipt = { case_id: caseId, filename, status: 'committed', detected_format: 'csv',
      imported_count: n, total_evidence_item_count: n, duplicate_row_count: 0, skipped_row_count: 0,
      evidence_items: items, source_distribution: {}, evidence_type_counts: {} }
    const persisted = { ...baseline, case_revision: 1, evidence_items: items, evidence_item_count: n }
    return { baseline, preview, receipt, persisted }
  }
  function configure(value = fixtures()) {
    apiMocks.previewCaseEvidenceImport.mockResolvedValue(value.preview)
    apiMocks.commitCaseEvidenceImport.mockResolvedValue(value.receipt)
    apiMocks.getCase.mockResolvedValueOnce(value.baseline).mockResolvedValue(value.persisted)
    return value
  }
  function view(value = fixtures()) {
    const callbacks = { onCaseReady: vi.fn(), onOpenGuidedEvidenceReview: vi.fn(), onRunCase: vi.fn() }
    const rendered = render(<EvidenceImportPanel currentCase={value.baseline} {...callbacks} />)
    return { ...callbacks, rendered }
  }
  async function selectFile(rendered, name = filename) {
    const file = new File(['platform,comment_text\nuploaded_dataset,Synthetic public CSV comment'], name, { type: 'text/csv' })
    fireEvent.change(rendered.container.querySelector('input[type="file"]'), { target: { files: [file] } })
    await screen.findByText(name, { exact: true })
  }
  async function prepare(rendered) {
    await selectFile(rendered)
    await waitFor(() => expect(previewButton().disabled).toBe(false), { timeout: 5000 })
    fireEvent.click(previewButton())
    await waitFor(() => expect(commitButton().disabled).toBe(false), { timeout: 5000 })
  }
  async function commitSettled() {
    await waitFor(() => expect(previewButton().classList.contains('ant-btn-loading')).toBe(false), { timeout: 5000 })
  }
  function expectNoReview(callbacks) {
    expect(screen.queryByRole('button', { name: reviewLabel })).toBeNull()
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    expect(apiMocks.reviewCaseEvidence).not.toHaveBeenCalled()
    expect(screen.queryByRole('button', { name: '导入后运行分析' })).toBeNull()
  }
  function csvDeferred() {
    let resolve, reject
    const promise = new Promise((yes, no) => { resolve = yes; reject = no })
    return { promise, resolve, reject }
  }
  async function changeMapping() {
    fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
    const options = await screen.findAllByText('platform', { exact: true })
    fireEvent.click(options.at(-1))
  }

  it('mount, file selection, focus and hover have no API or business side effects', async () => {
    const callbacks = view()
    await selectFile(callbacks.rendered)
    fireEvent.focus(previewButton()); fireEvent.mouseEnter(previewButton())
    await act(async () => {})
    for (const mock of Object.values(apiMocks)) expect(mock).not.toHaveBeenCalled()
    expectNoReview(callbacks)
  })

  it.each([1, 2, 3])('binds all %i new persisted IDs, never a slice, only on a separate Review click', async (n) => {
    const value = configure(fixtures(n)), callbacks = view(value)
    await prepare(callbacks.rendered)
    expect(apiMocks.getCase).not.toHaveBeenCalled()
    const frozenPreview = apiMocks.previewCaseEvidenceImport.mock.calls[0][1]
    fireEvent.click(commitButton())
    const review = await screen.findByRole('button', { name: reviewLabel })
    expect(apiMocks.getCase).toHaveBeenCalledTimes(2)
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledExactlyOnceWith(caseId, {
      ...frozenPreview, column_mapping: value.preview.column_mapping,
    })
    expect(apiMocks.getCase.mock.invocationCallOrder[0]).toBeLessThan(apiMocks.commitCaseEvidenceImport.mock.invocationCallOrder[0])
    expect(callbacks.onCaseReady).toHaveBeenCalledExactlyOnceWith(value.persisted)
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
    fireEvent.click(review)
    const scope = callbacks.onOpenGuidedEvidenceReview.mock.calls[0][0]
    expect(scope).toEqual(makeGuidedEvidenceScope({ case_id: caseId,
      evidence_ids: value.persisted.evidence_items.map((item) => item.evidence_id), query: value.baseline.keyword }))
    expect(Object.keys(scope).sort()).toEqual(['case_id', 'evidence_ids', 'query', 'step'])
    expect(JSON.stringify(scope)).not.toMatch(/comment|normalized_content_hash|source_type|column_mapping|content_base64/)
    expect(previewButton().disabled).toBe(true)
    expect(commitButton().disabled).toBe(true)
    expect(screen.queryByRole('button', { name: '导入后运行分析' })).toBeNull()
  })

  it('single-flights Preview and Commit synchronously, including baseline and readback waits', async () => {
    const value = configure(), callbacks = view(value), preview = csvDeferred(), baseline = csvDeferred(), post = csvDeferred()
    apiMocks.previewCaseEvidenceImport.mockReturnValue(preview.promise)
    apiMocks.getCase.mockReset().mockReturnValueOnce(baseline.promise).mockReturnValueOnce(post.promise)
    await selectFile(callbacks.rendered)
    act(() => { fireEvent.click(previewButton()); fireEvent.click(previewButton()) })
    expect(apiMocks.previewCaseEvidenceImport).toHaveBeenCalledTimes(1)
    await act(async () => preview.resolve(value.preview))
    act(() => { fireEvent.click(commitButton()); fireEvent.click(commitButton()) })
    expect(apiMocks.getCase).toHaveBeenCalledTimes(1)
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    await act(async () => baseline.resolve(value.baseline))
    await waitFor(() => expect(apiMocks.getCase).toHaveBeenCalledTimes(2))
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expectNoReview(callbacks)
    await act(async () => post.resolve(value.persisted))
    await screen.findByRole('button', { name: reviewLabel })
    expect(apiMocks.previewCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
  })

  it.each([{ numbers: [2, 4] }, { numbers: [5, 10] }])('accepts parsed-record gaps $numbers without deriving IDs from row numbers', async ({ numbers }) => {
    const value = fixtures(2)
    value.preview.preview_rows.forEach((row, index) => { row.row_number = numbers[index] })
    configure(value)
    const callbacks = view(value)
    await prepare(callbacks.rendered); fireEvent.click(commitButton())
    fireEvent.click(await screen.findByRole('button', { name: reviewLabel }))
    expect(callbacks.onOpenGuidedEvidenceReview).toHaveBeenCalledExactlyOnceWith(makeGuidedEvidenceScope({
      case_id: caseId, evidence_ids: ['csv_evidence_1', 'csv_evidence_2'], query: value.baseline.keyword,
    }))
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expect(callbacks.onRunCase).not.toHaveBeenCalled()
  })

  it.each([
    ['four rows', (value) => Object.assign(value, fixtures(4))],
    ['hidden fourth row', (value) => { value.preview.total_rows = 4 }],
    ['skipped row', (value) => { value.preview.skipped_row_count = 1 }],
    ['duplicate row', (value) => { value.preview.duplicate_row_count = 1 }],
    ['truncated preview', (value) => { value.preview.preview_rows.pop() }],
    ['duplicate ID', (value) => { value.preview.preview_rows[1].evidence_id = value.preview.preview_rows[0].evidence_id }],
    ['duplicate row number', (value) => { value.preview.preview_rows[1].row_number = 2 }],
    ['header row number', (value) => { value.preview.preview_rows[0].row_number = 1 }],
    ['noninteger record number', (value) => { value.preview.preview_rows[0].row_number = 2.5 }],
    ['unsafe record number', (value) => { value.preview.preview_rows[1].row_number = Number.MAX_SAFE_INTEGER + 1 }],
    ['decreasing record numbers', (value) => { value.preview.preview_rows[0].row_number = 4 }],
    ['unsafe ID', (value) => { value.preview.preview_rows[0].evidence_id = '../foreign' }],
    ['clipped body', (value) => { value.preview.preview_rows[0].body_text = 'x'.repeat(180) }],
    ['error warning', (value) => { value.preview.warnings = [{ code: 'synthetic_error', severity: 'error' }] }],
    ['non-CSV format', (value) => { value.preview.detected_format = 'xlsx' }],
  ])('keeps %s available only through normal import and persisted Queue, not guided Run', async (_, change) => {
    const value = fixtures(2); change(value); configure(value)
    const callbacks = view(value)
    await prepare(callbacks.rendered)
    fireEvent.click(commitButton())
    await commitSettled()
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expectNoReview(callbacks)
    expect(screen.getByText(/请使用正常持久化证据复核队列/)).toBeTruthy()
  })

  it.each([
    ['foreign case', (value) => { value.preview.case_id = 'case_foreign' }],
    ['foreign file', (value) => { value.preview.filename = 'other.csv' }],
    ['missing rows', (value) => { value.preview.preview_rows = null }],
    ['invalid mapping', (value) => { value.preview.column_mapping = { comment_text: { raw: 'invalid' } } }],
  ])('rejects %s preview without a Commit or automatic retry', async (_, change) => {
    const value = fixtures(); change(value); configure(value)
    const callbacks = view(value)
    await selectFile(callbacks.rendered); fireEvent.click(previewButton())
    await screen.findByText(/Import preview failed or changed context/)
    expect(commitButton().disabled).toBe(true)
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    expect(apiMocks.previewCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expectNoReview(callbacks)
  })

  it.each([
    ['preexisting Evidence', (value) => { value.baseline.evidence_items = [value.persisted.evidence_items[0]]; value.baseline.evidence_item_count = 1 }],
    ['raw posts', (value) => { value.baseline.raw_posts = [{}]; value.baseline.raw_post_count = 1 }],
    ['raw comments', (value) => { value.baseline.raw_comments = [{}]; value.baseline.raw_comment_count = 1 }],
    ['completed analysis', (value) => { value.baseline.analysis_result = { summary: 'prior' } }],
    ['old analysis identity', (value) => { value.baseline.analysis_run_id = 'prior_run' }],
    ['non-draft case', (value) => { value.baseline.status = 'completed' }],
    ['concurrent same-ID mutation', (value) => { value.persisted.case_revision = 2 }],
    ['additional concurrent ID', (value) => { value.persisted.evidence_items = [...value.persisted.evidence_items, { ...value.persisted.evidence_items[0], evidence_id: 'external_id' }]; value.persisted.evidence_item_count = 2 }],
    ['missing persisted ID', (value) => { value.persisted.evidence_items = []; value.persisted.evidence_item_count = 0 }],
    ['ambiguous receipt ID', (value) => { value.receipt.evidence_items = [{ ...value.receipt.evidence_items[0], evidence_id: 'different_id' }] }],
    ['foreign persisted item', (value) => { value.persisted.evidence_items = [{ ...value.persisted.evidence_items[0], case_id: 'case_foreign' }] }],
    ['changed content', (value) => { value.persisted.evidence_items = [{ ...value.persisted.evidence_items[0], comment_text: 'Different content' }] }],
    ['changed content hash', (value) => { value.persisted.evidence_items = [{ ...value.persisted.evidence_items[0], normalized_content_hash: 'f'.repeat(64) }] }],
    ['wrong receipt count', (value) => { value.receipt.imported_count = 0 }],
  ])('does not create a guided scope for %s; preserves actual normal import state', async (_, change) => {
    const value = fixtures(); change(value); configure(value)
    const callbacks = view(value)
    await prepare(callbacks.rendered); fireEvent.click(commitButton()); await commitSettled()
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expect(apiMocks.getCase).toHaveBeenCalledTimes(2)
    expectNoReview(callbacks)
    expect(screen.getByText(/未确认完整的新小批次身份/)).toBeTruthy()
  })

  it.each(['foreign baseline', 'changed query'])('does not POST after %s readback', async (kind) => {
    const value = configure(), callbacks = view(value)
    apiMocks.getCase.mockReset().mockResolvedValue({ ...value.baseline,
      ...(kind === 'foreign baseline' ? { case_id: 'case_other' } : { keyword: 'Other query' }) })
    await prepare(callbacks.rendered); fireEvent.click(commitButton())
    await screen.findByText(/未提交导入/)
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    expectNoReview(callbacks)
  })

  it.each(['commit failure', 'readback failure', 'foreign receipt', 'foreign readback'])('retains unknown writes after %s without rollback, Review or resubmit', async (kind) => {
    const value = configure(), callbacks = view(value)
    if (kind === 'commit failure') apiMocks.commitCaseEvidenceImport.mockRejectedValue(new Error('synthetic unknown write'))
    if (kind === 'readback failure') apiMocks.getCase.mockReset().mockResolvedValueOnce(value.baseline).mockRejectedValue(new Error('synthetic read unavailable'))
    if (kind === 'foreign receipt') apiMocks.commitCaseEvidenceImport.mockResolvedValue({ ...value.receipt, case_id: 'case_other' })
    if (kind === 'foreign readback') apiMocks.getCase.mockReset().mockResolvedValueOnce(value.baseline).mockResolvedValue({ ...value.persisted, case_id: 'case_other' })
    await prepare(callbacks.rendered); fireEvent.click(commitButton())
    await screen.findByText(/提交可能已保存/)
    await commitSettled(); fireEvent.click(commitButton()); fireEvent.click(previewButton())
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expect(commitButton().disabled).toBe(true)
    expectNoReview(callbacks)
    if (kind === 'readback failure' || kind === 'foreign readback') {
      expect(screen.getByText('imported: 1')).toBeTruthy()
      expect(screen.getByText('已收到导入回执，持久化状态尚未确认')).toBeTruthy()
      expect(screen.queryByText('导入完成', { exact: true })).toBeNull()
    }
  })

  it.each(['case A→B→A', 'new file', 'mapping', 'unmount'])('ignores pending Preview after %s', async (kind) => {
    const value = configure(), callbacks = view(value), pending = csvDeferred()
    if (kind === 'mapping') await prepare(callbacks.rendered)
    else await selectFile(callbacks.rendered)
    apiMocks.previewCaseEvidenceImport.mockReturnValue(pending.promise)
    fireEvent.click(previewButton())
    if (kind === 'case A→B→A') {
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={{ ...value.baseline, case_id: 'case_b' }} {...callbacks} />)
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={value.baseline} {...callbacks} />)
    } else if (kind === 'new file') await selectFile(callbacks.rendered, 'replacement.csv')
    else if (kind === 'mapping') await changeMapping()
    else callbacks.rendered.unmount()
    await act(async () => pending.resolve(value.preview))
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    if (kind !== 'unmount') expect(commitButton().disabled).toBe(true)
  })

  it.each(['case A→B→A', 'new file', 'mapping', 'unmount'])('invalidates pending baseline on %s before any POST', async (kind) => {
    const value = configure(), callbacks = view(value), pending = csvDeferred()
    apiMocks.getCase.mockReset().mockReturnValue(pending.promise)
    await prepare(callbacks.rendered); fireEvent.click(commitButton())
    if (kind === 'case A→B→A') {
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={{ ...value.baseline, case_id: 'case_b' }} {...callbacks} />)
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={value.baseline} {...callbacks} />)
    } else if (kind === 'new file') await selectFile(callbacks.rendered, 'replacement.csv')
    else if (kind === 'mapping') await changeMapping()
    else callbacks.rendered.unmount()
    await act(async () => pending.resolve(value.baseline))
    expect(apiMocks.getCase).toHaveBeenCalledTimes(1)
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
  })

  it.each(['case A→B→A', 'new file', 'mapping', 'unmount'])('never retries an already posted import after %s', async (kind) => {
    const value = configure(), callbacks = view(value), pending = csvDeferred()
    apiMocks.commitCaseEvidenceImport.mockReturnValue(pending.promise)
    await prepare(callbacks.rendered); fireEvent.click(commitButton())
    await waitFor(() => expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1))
    if (kind === 'case A→B→A') {
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={{ ...value.baseline, case_id: 'case_b' }} {...callbacks} />)
      callbacks.rendered.rerender(<EvidenceImportPanel currentCase={value.baseline} {...callbacks} />)
    } else if (kind === 'new file') await selectFile(callbacks.rendered, 'replacement.csv')
    else if (kind === 'mapping') await changeMapping()
    else callbacks.rendered.unmount()
    await act(async () => pending.resolve(value.receipt))
    expect(apiMocks.getCase).toHaveBeenCalledTimes(1)
    expect(apiMocks.commitCaseEvidenceImport).toHaveBeenCalledTimes(1)
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
    expect(callbacks.onOpenGuidedEvidenceReview).not.toHaveBeenCalled()
    if (kind !== 'unmount') {
      expect(screen.getByText(/此案例有尚未确认的导入请求/)).toBeTruthy()
      expect(commitButton().disabled).toBe(true)
    }
  })

  it('ignores a superseded file read rather than pairing an old file with the new selection', async () => {
    const value = configure(), callbacks = view(value), readers = []
    vi.stubGlobal('FileReader', class {
      constructor() { readers.push(this) }
      readAsDataURL() {}
    })
    const input = callbacks.rendered.container.querySelector('input[type="file"]')
    fireEvent.change(input, { target: { files: [new File(['old'], 'old.csv', { type: 'text/csv' })] } })
    await waitFor(() => expect(readers).toHaveLength(1))
    fireEvent.change(callbacks.rendered.container.querySelector('input[type="file"]'), {
      target: { files: [new File(['new'], filename, { type: 'text/csv' })] },
    })
    await waitFor(() => expect(readers).toHaveLength(2))
    await act(async () => { readers[1].result = 'data:text/csv;base64,bmV3'; readers[1].onload() })
    await act(async () => { readers[0].result = 'data:text/csv;base64,b2xk'; readers[0].onload() })
    fireEvent.click(previewButton())
    await waitFor(() => expect(apiMocks.previewCaseEvidenceImport).toHaveBeenCalledTimes(1))
    expect(apiMocks.previewCaseEvidenceImport).toHaveBeenCalledWith(caseId, {
      filename, content_base64: 'bmV3', column_mapping: {},
    })
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
  })

  it('unmount during file read performs no Preview, Commit or callback', async () => {
    const callbacks = view(), readers = []
    vi.stubGlobal('FileReader', class {
      constructor() { readers.push(this) }
      readAsDataURL() {}
    })
    fireEvent.change(callbacks.rendered.container.querySelector('input[type="file"]'), {
      target: { files: [new File(['synthetic'], filename, { type: 'text/csv' })] },
    })
    await waitFor(() => expect(readers).toHaveLength(1))
    callbacks.rendered.unmount()
    await act(async () => { readers[0].result = 'data:text/csv;base64,c3ludGhldGlj'; readers[0].onload() })
    expect(apiMocks.previewCaseEvidenceImport).not.toHaveBeenCalled()
    expect(apiMocks.commitCaseEvidenceImport).not.toHaveBeenCalled()
    expect(callbacks.onCaseReady).not.toHaveBeenCalled()
  })
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
