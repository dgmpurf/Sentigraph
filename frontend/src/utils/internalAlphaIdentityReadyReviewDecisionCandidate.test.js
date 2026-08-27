import { describe, expect, it } from 'vitest'

import {
  buildInternalAlphaIdentityReadyReviewDecisionCandidate,
  INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES,
} from './internalAlphaIdentityReadyReviewDecisionCandidate.js'

const VALID_IDENTITY = Object.freeze({
  identity_schema: 'sentigraph_b05_review_subject_identity_v0_1',
  identity_version: '0.1',
  identity_status: 'ready',
  sample_handle: 'helldivers2-psn-demo',
  result_file_name: 'provider_result.json',
  package_name: 'synthetic_provider_package',
  provider_result_content_bytes: 1234,
  provider_result_content_sha256: '1'.repeat(64),
  metadata_profile: 'governed_b05_five_file',
  metadata_entry_count: 5,
  safe_metadata_bundle_sha256: '2'.repeat(64),
  review_subject_content_safe_hash: '3'.repeat(64),
  review_subject_binding_safe_hash: '4'.repeat(64),
})

const EXPECTED_BASE_CANDIDATE = Object.freeze({
  schema: 'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
  mode: 'frontend_local_nonpersistent_governed_human_review_decision_candidate',
  identity_schema: VALID_IDENTITY.identity_schema,
  identity_version: VALID_IDENTITY.identity_version,
  identity_status: VALID_IDENTITY.identity_status,
  sample_handle: VALID_IDENTITY.sample_handle,
  review_subject_binding_safe_hash: VALID_IDENTITY.review_subject_binding_safe_hash,
  candidate_only: true,
  persisted: false,
  trust_upgraded: false,
  production_object: false,
  human_review_required: true,
  no_automatic_trust_upgrade: true,
})

describe('identity-ready governed human-review decision candidate builder', () => {
  it.each(INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES)(
    'builds one deterministic immutable %s candidate from the established identity',
    (decisionType) => {
      const first = buildInternalAlphaIdentityReadyReviewDecisionCandidate(
        VALID_IDENTITY,
        decisionType,
      )
      const second = buildInternalAlphaIdentityReadyReviewDecisionCandidate(
        VALID_IDENTITY,
        decisionType,
      )

      expect(first).toEqual({
        ...EXPECTED_BASE_CANDIDATE,
        decision_type: decisionType,
      })
      expect(second).toEqual(first)
      expect(Object.isFrozen(first)).toBe(true)
      expect(first.review_subject_binding_safe_hash).toBe(
        VALID_IDENTITY.review_subject_binding_safe_hash,
      )
      expect(first).not.toHaveProperty('result_file_name')
      expect(first).not.toHaveProperty('package_name')
      expect(first).not.toHaveProperty('provider_result_content_sha256')
      expect(first).not.toHaveProperty('safe_metadata_bundle_sha256')
      expect(first).not.toHaveProperty('review_subject_content_safe_hash')
      expect(first).not.toHaveProperty('created_at')
      expect(first).not.toHaveProperty('decision_id')
    },
  )

  it.each([
    ['missing identity', null, 'keep_pending_human_review'],
    ['wrong schema', { ...VALID_IDENTITY, identity_schema: 'wrong' }, 'keep_pending_human_review'],
    ['wrong version', { ...VALID_IDENTITY, identity_version: '0.2' }, 'keep_pending_human_review'],
    ['not ready', { ...VALID_IDENTITY, identity_status: 'blocked' }, 'keep_pending_human_review'],
    ['wrong sample', { ...VALID_IDENTITY, sample_handle: 'another-sample' }, 'keep_pending_human_review'],
    [
      'non-lowercase hash',
      { ...VALID_IDENTITY, review_subject_binding_safe_hash: 'A'.repeat(64) },
      'keep_pending_human_review',
    ],
    [
      'extra governance field',
      { ...VALID_IDENTITY, persisted: true },
      'keep_pending_human_review',
    ],
    ['unsupported decision', VALID_IDENTITY, 'approve_trust'],
  ])('fails closed for %s', (_label, identity, decisionType) => {
    expect(() =>
      buildInternalAlphaIdentityReadyReviewDecisionCandidate(identity, decisionType),
    ).toThrow('frontend_identity_ready_review_decision_candidate_contract_mismatch')
  })
})
