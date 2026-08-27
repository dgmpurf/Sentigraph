const EXPECTED_IDENTITY_FIELDS = Object.freeze([
  'identity_schema',
  'identity_version',
  'identity_status',
  'sample_handle',
  'result_file_name',
  'package_name',
  'provider_result_content_bytes',
  'provider_result_content_sha256',
  'metadata_profile',
  'metadata_entry_count',
  'safe_metadata_bundle_sha256',
  'review_subject_content_safe_hash',
  'review_subject_binding_safe_hash',
])

export const INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES = Object.freeze([
  'keep_pending_human_review',
  'request_more_governance_review',
])

const CURRENT_SAMPLE_HANDLE = 'helldivers2-psn-demo'
const LOWER_HEX_64_PATTERN = /^[0-9a-f]{64}$/
const RESULT_FILE_NAME_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]*\.json$/
const PACKAGE_NAME_PATTERN = /^[A-Za-z0-9][A-Za-z0-9._-]*$/

function contractError() {
  throw new Error('frontend_identity_ready_review_decision_candidate_contract_mismatch')
}

function isPlainObject(value) {
  return value !== null && typeof value === 'object' && !Array.isArray(value)
}

function hasExactIdentityFields(identity) {
  const keys = Object.keys(identity)
  return (
    keys.length === EXPECTED_IDENTITY_FIELDS.length &&
    keys.every((field) => EXPECTED_IDENTITY_FIELDS.includes(field))
  )
}

function isLowerHex64(value) {
  return typeof value === 'string' && LOWER_HEX_64_PATTERN.test(value)
}

function validateEstablishedIdentity(identity) {
  if (!isPlainObject(identity) || !hasExactIdentityFields(identity)) contractError()
  if (
    identity.identity_schema !== 'sentigraph_b05_review_subject_identity_v0_1' ||
    identity.identity_version !== '0.1' ||
    identity.identity_status !== 'ready' ||
    identity.sample_handle !== CURRENT_SAMPLE_HANDLE ||
    typeof identity.result_file_name !== 'string' ||
    identity.result_file_name.length > 160 ||
    !RESULT_FILE_NAME_PATTERN.test(identity.result_file_name) ||
    typeof identity.package_name !== 'string' ||
    identity.package_name.length > 160 ||
    !PACKAGE_NAME_PATTERN.test(identity.package_name) ||
    !Number.isInteger(identity.provider_result_content_bytes) ||
    identity.provider_result_content_bytes < 0 ||
    identity.metadata_profile !== 'governed_b05_five_file' ||
    identity.metadata_entry_count !== 5
  ) {
    contractError()
  }

  for (const field of [
    'provider_result_content_sha256',
    'safe_metadata_bundle_sha256',
    'review_subject_content_safe_hash',
    'review_subject_binding_safe_hash',
  ]) {
    if (!isLowerHex64(identity[field])) contractError()
  }
}

export function buildInternalAlphaIdentityReadyReviewDecisionCandidate(
  identity,
  decisionType,
) {
  validateEstablishedIdentity(identity)
  if (!INTERNAL_ALPHA_IDENTITY_READY_REVIEW_DECISION_TYPES.includes(decisionType)) {
    contractError()
  }

  return Object.freeze({
    schema: 'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
    mode: 'frontend_local_nonpersistent_governed_human_review_decision_candidate',
    identity_schema: identity.identity_schema,
    identity_version: identity.identity_version,
    identity_status: identity.identity_status,
    sample_handle: identity.sample_handle,
    review_subject_binding_safe_hash: identity.review_subject_binding_safe_hash,
    decision_type: decisionType,
    candidate_only: true,
    persisted: false,
    trust_upgraded: false,
    production_object: false,
    human_review_required: true,
    no_automatic_trust_upgrade: true,
  })
}
