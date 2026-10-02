import { describe, expect, it } from 'vitest'
import {
  buildGuidedCaseCreatePayload, guidedAnalysisPair, guidedResultIsCurrent,
  guidedReviewReadiness, makeGuidedEvidenceScope, scopeFromReviewedAttach,
} from './guidedCaseFlow.js'

const scope = makeGuidedEvidenceScope({ case_id: 'case_a', evidence_ids: ['e1', 'e2'], query: 'Event A' })
function persisted(statuses = ['approved', 'rejected']) {
  return {
    case_id: 'case_a', status: 'completed', analysis_revision: 7, analysis_run_id: 'run_a7',
    analysis_result: {}, report: {},
    evidence_items: statuses.map((review_status, i) => ({
      case_id: 'case_a', evidence_id: `e${i + 1}`, review_status,
      trust_label: review_status === 'rejected' ? 'rejected' : 'medium',
      verification_status: review_status === 'rejected' ? 'rejected' : 'verified_by_official_api',
    })),
  }
}

describe('guided case flow pure UI policy', () => {
  it('normalizes the query and creates only the existing case payload with official platforms and language', () => {
    expect(buildGuidedCaseCreatePayload('  Event\n   A  ')).toEqual({
      keyword: 'Event A', title: 'Event A', platforms: ['youtube'], report_language: 'zh-CN',
    })
    expect(buildGuidedCaseCreatePayload('Mock', false).platforms).toEqual([])
  })
  it.each(['', ' \t\n ', 'x'.repeat(121)])('blocks invalid create query %j', (query) => {
    expect(buildGuidedCaseCreatePayload(query)).toBeNull()
  })
  it('accepts exactly the 120-character limit without inventing a case ID', () => {
    const payload = buildGuidedCaseCreatePayload('x'.repeat(120))
    expect(payload.keyword).toHaveLength(120)
    expect(payload).not.toHaveProperty('case_id')
  })
  it('copies and freezes only safe receipt fields and never retains provider content', () => {
    const ids = ['e1']
    const input = { case_id: 'case_a', evidence_ids: ids, query: ' Event A ', author: 'secret-author',
      body_text: 'provider-text', credentials: 'never-retain', raw_envelope: {}, private_path: 'private' }
    const receipt = makeGuidedEvidenceScope(input)
    ids.push('e2')
    expect(receipt).toEqual({ case_id: 'case_a', evidence_ids: ['e1'], query: 'Event A', step: 'evidence_review' })
    expect(Object.isFrozen(receipt)).toBe(true)
    expect(Object.isFrozen(receipt.evidence_ids)).toBe(true)
    expect(JSON.stringify(receipt)).not.toMatch(/secret-author|provider-text|never-retain|private|envelope/)
  })
  it.each([[], ['e1', 'e1'], ['e1', 'e2', 'e3', 'e4'], [''], ['unsafe/id']])(
    'rejects missing, duplicated, excessive or malformed scoped IDs %j', (evidence_ids) => {
      expect(makeGuidedEvidenceScope({ case_id: 'case_a', query: 'A', evidence_ids })).toBeNull()
    },
  )
  it('binds a receipt only to the captured target and preserves distinct Evidence IDs', () => {
    const receipt = { case_id: 'case_a', status: 'attached', attached_discussion_count: 2,
      attached_evidence_items: [{ case_id: 'case_a', evidence_id: 'e1', comment_text: 'discard' },
        { case_id: 'case_a', evidence_id: 'e2' }] }
    expect(scopeFromReviewedAttach(receipt, 'A', 'case_a').evidence_ids).toEqual(['e1', 'e2'])
    expect(scopeFromReviewedAttach(receipt, 'A', 'case_b')).toBeNull()
    expect(scopeFromReviewedAttach({ ...receipt, attached_discussion_count: 1 }, 'A', 'case_a')).toBeNull()
    expect(scopeFromReviewedAttach({ ...receipt, attached_evidence_items: [{ case_id: 'case_b', evidence_id: 'e1' }] }, 'A', 'case_a')).toBeNull()
  })
  it.each([
    ['approved', 'marked_weak'], ['approved', 'rejected'], ['marked_weak', 'duplicate_merged'],
  ])('requires all resolved and at least one usable item: %s / %s', (a, b) => {
    expect(guidedReviewReadiness(persisted([a, b]), scope).ready).toBe(true)
  })
  it.each(['not_reviewed', 'review_needed', 'needs_more_source', 'reset_review', undefined])(
    'keeps unresolved/reset %j blocked even with one usable item', (status) => {
      expect(guidedReviewReadiness(persisted(['approved', status]), scope).reason).toBe('unresolved_review')
    },
  )
  it('does not make all-rejected or all-merged items usable and keeps them in the case', () => {
    const value = persisted(['rejected', 'duplicate_merged'])
    expect(guidedReviewReadiness(value, scope).reason).toBe('no_usable_evidence')
    expect(value.evidence_items).toHaveLength(2)
  })
  it('never promotes rejected trust/verification to usable through an inconsistent approved label', () => {
    const value = persisted(['approved', 'duplicate_merged'])
    value.evidence_items[0].verification_status = 'rejected'
    expect(guidedReviewReadiness(value, scope).ready).toBe(false)
  })
  it('blocks wrong case, absent/wrong/duplicate scoped evidence and in-flight review', () => {
    expect(guidedReviewReadiness({ ...persisted(), case_id: 'case_b' }, scope).reason).toBe('wrong_case')
    expect(guidedReviewReadiness({ ...persisted(), evidence_items: [] }, scope).ready).toBe(false)
    const value = persisted()
    value.evidence_items[0].case_id = 'case_b'
    expect(guidedReviewReadiness(value, scope).ready).toBe(false)
    const duplicate = persisted()
    duplicate.evidence_items.push({ ...duplicate.evidence_items[0] })
    expect(guidedReviewReadiness(duplicate, scope).ready).toBe(false)
    expect(guidedReviewReadiness(persisted(), scope, true).reason).toBe('review_pending')
  })
  it('is scoped rather than a new global evidence policy', () => {
    const value = persisted()
    value.evidence_items.push({ case_id: 'case_a', evidence_id: 'unrelated', review_status: 'not_reviewed' })
    expect(guidedReviewReadiness(value, scope).ready).toBe(true)
  })
  it('current result requires the exact case/revision/run pair and completed case payload', () => {
    const value = persisted()
    const flow = { scope, last_run_pair: guidedAnalysisPair(value), review_pending: false }
    expect(guidedResultIsCurrent(value, flow)).toBe(true)
    for (const patch of [
      { case_id: 'case_b' }, { analysis_revision: 8 }, { analysis_run_id: 'run_other' },
      { analysis_run_id: null, run_id: 'run_a7' }, { analysis_revision: null },
      { status: 'draft' }, { analysis_result: null }, { report: null },
    ]) expect(guidedResultIsCurrent({ ...value, ...patch }, flow)).toBe(false)
    expect(guidedResultIsCurrent(value, { ...flow, last_run_pair: null })).toBe(false)
    expect(guidedResultIsCurrent(value, { ...flow, review_pending: true })).toBe(false)
  })
  it('timestamps cannot rescue stale results after a review invalidation', () => {
    const value = persisted()
    const flow = { scope, last_run_pair: guidedAnalysisPair(value) }
    const reset = { ...value, updated_at: '2099-01-01', status: 'draft', analysis_run_id: null,
      analysis_result: value.analysis_result, report: value.report }
    expect(guidedResultIsCurrent(reset, flow)).toBe(false)
  })
})
