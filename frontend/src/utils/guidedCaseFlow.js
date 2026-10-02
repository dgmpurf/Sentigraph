// UI-only guidance over existing case APIs; never a backend authorization policy.
export function normalizeGuidedQuery(value) {
  return String(value ?? '').replace(/\s+/g, ' ').trim()
}

export function buildGuidedCaseCreatePayload(query, live = true) {
  const keyword = normalizeGuidedQuery(query)
  if (!keyword || keyword.length > 120) return null
  return { keyword, title: keyword, platforms: live ? ['youtube'] : [], report_language: 'zh-CN' }
}

function safeId(value) {
  return typeof value === 'string' && /^[A-Za-z0-9_-]{1,200}$/.test(value)
}

/** Copy only safe navigation identifiers; discard provider bodies and unknown fields. */
export function makeGuidedEvidenceScope({ case_id, evidence_ids, query } = {}) {
  const normalized = normalizeGuidedQuery(query)
  if (!safeId(case_id) || !normalized || normalized.length > 120 || !Array.isArray(evidence_ids) ||
      evidence_ids.length < 1 || evidence_ids.length > 3 || !evidence_ids.every(safeId) ||
      new Set(evidence_ids).size !== evidence_ids.length) return null
  return Object.freeze({
    case_id, evidence_ids: Object.freeze([...evidence_ids]), query: normalized, step: 'evidence_review',
  })
}

export function scopeFromReviewedAttach(receipt, query, expectedCaseId) {
  if (receipt?.case_id !== expectedCaseId || receipt?.status !== 'attached' ||
      !Array.isArray(receipt.attached_evidence_items) ||
      receipt.attached_discussion_count !== receipt.attached_evidence_items.length ||
      receipt.attached_evidence_items.some((item) => item.case_id !== expectedCaseId)) return null
  return makeGuidedEvidenceScope({
    case_id: expectedCaseId,
    evidence_ids: receipt.attached_evidence_items.map((item) => item.evidence_id), query,
  })
}

const RESOLVED = new Set(['approved', 'marked_weak', 'rejected', 'duplicate_merged'])
const USABLE = new Set(['approved', 'marked_weak'])

/** Recompute from the fresh persisted case, not a cached readiness boolean or timestamp. */
export function guidedReviewReadiness(caseDetail, scope, pending = false) {
  const validScope = makeGuidedEvidenceScope(scope)
  const blocked = (reason, usable = 0) => ({ ready: false, reason, usable })
  if (!validScope) return blocked('invalid_scope')
  if (caseDetail?.case_id !== validScope.case_id) return blocked('wrong_case')
  if (pending) return blocked('review_pending')
  const items = Array.isArray(caseDetail.evidence_items) ? caseDetail.evidence_items : []
  const scoped = validScope.evidence_ids.map((id) => items.filter((item) => item.evidence_id === id))
  if (scoped.some((matches) => matches.length !== 1 ||
      matches[0].case_id !== validScope.case_id)) return blocked('missing_or_mismatched_evidence')
  const resolvedItems = scoped.map(([item]) => item)
  const usable = resolvedItems.filter((item) => USABLE.has(item.review_status) &&
    item.trust_label !== 'rejected' && item.verification_status !== 'rejected').length
  if (resolvedItems.some((item) => !RESOLVED.has(item.review_status))) return blocked('unresolved_review', usable)
  if (!usable) return blocked('no_usable_evidence')
  return { ready: true, reason: 'review_resolved', usable }
}

export function guidedAnalysisPair(caseDetail) {
  if (!safeId(caseDetail?.case_id) || !Number.isInteger(caseDetail.analysis_revision) ||
      caseDetail.analysis_revision < 0 || !safeId(caseDetail.analysis_run_id)) return null
  return Object.freeze({
    case_id: caseDetail.case_id,
    analysis_revision: caseDetail.analysis_revision,
    analysis_run_id: caseDetail.analysis_run_id,
  })
}

export function guidedResultIsCurrent(caseDetail, flow) {
  const pair = guidedAnalysisPair(caseDetail)
  const expected = flow?.last_run_pair
  return Boolean(pair && expected && flow.scope?.case_id === pair.case_id &&
    caseDetail.status === 'completed' && caseDetail.analysis_result && caseDetail.report &&
    guidedReviewReadiness(caseDetail, flow.scope, flow.review_pending || flow.review_readback_required).ready &&
    expected.case_id === pair.case_id && expected.analysis_revision === pair.analysis_revision &&
    expected.analysis_run_id === pair.analysis_run_id)
}
