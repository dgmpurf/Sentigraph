import React from 'react'
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  within,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  apiClientGet: vi.fn(),
  apiClientPost: vi.fn(),
  getInternalAlphaReviewConsoleProjection: vi.fn(),
  getInternalAlphaLocalExchangeSampleCatalog: vi.fn(),
  getInternalAlphaLocalExchangeProjection: vi.fn(),
  getInternalAlphaLocalExchangeIdentityReadyV02Projection: vi.fn(),
}))

const identityReadyDecisionCandidateMocks = vi.hoisted(() => ({
  build: vi.fn(),
}))

vi.mock('../api/client.js', () => ({
  apiClient: {
    get: apiMocks.apiClientGet,
    post: apiMocks.apiClientPost,
  },
}))

vi.mock('../api/sentigraphApi.js', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    getInternalAlphaReviewConsoleProjection:
      apiMocks.getInternalAlphaReviewConsoleProjection,
    getInternalAlphaLocalExchangeSampleCatalog:
      apiMocks.getInternalAlphaLocalExchangeSampleCatalog,
    getInternalAlphaLocalExchangeProjection:
      apiMocks.getInternalAlphaLocalExchangeProjection,
    getInternalAlphaLocalExchangeIdentityReadyV02Projection:
      apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
  }
})

vi.mock('../utils/internalAlphaIdentityReadyReviewDecisionCandidate.js', async (importOriginal) => {
  const actual = await importOriginal()
  identityReadyDecisionCandidateMocks.build.mockImplementation(
    actual.buildInternalAlphaIdentityReadyReviewDecisionCandidate,
  )
  return {
    ...actual,
    buildInternalAlphaIdentityReadyReviewDecisionCandidate:
      identityReadyDecisionCandidateMocks.build,
  }
})

import {
  B05_REVIEW_SUBJECT_IDENTITY_FIELDS,
  INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_AUDIT_ERROR_FIELDS,
  INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_AUDIT_SUCCESS_FIELDS,
  INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_ERROR_FIELDS,
  INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_ROW_FIELDS,
  INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_SUCCESS_FIELDS,
  INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID,
  INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES,
  INTERNAL_ALPHA_GOVERNED_REVIEW_FORMAL_STATE_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTION_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_PROJECTION_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_CATALOG_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_FIELDS,
  getInternalAlphaGovernedReviewFormalState,
  getInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory,
  getInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection,
  normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory,
  normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection,
  normalizeInternalAlphaGovernedReviewFormalStateProjection,
  normalizeInternalAlphaGovernedReviewDecisionPostResponse,
  normalizeInternalAlphaLocalExchangeProjection,
  normalizeInternalAlphaLocalExchangeIdentityReadyV02Projection,
  normalizeInternalAlphaLocalExchangeSampleCatalog,
  postInternalAlphaIdentityReadyGovernedReviewDecision,
  postInternalAlphaGovernedReviewDecision,
} from '../api/sentigraphApi.js'
import { InternalAlphaReviewConsole } from './InternalAlphaReviewConsole.jsx'

const CURRENT_HANDLE = 'helldivers2-psn-demo'
const HISTORICAL_HANDLE = 'helldivers2-psn-demo-20260614'
const CURRENT_LABEL = 'Current curated sample'
const HISTORICAL_LABEL = 'Accepted historical sample'
const CURRENT_MARKER = 'synthetic_current_visible_marker'
const HISTORICAL_MARKER = 'synthetic_historical_visible_marker'
const RAW_ERROR_MARKER = 'synthetic_raw_exception_message'
const RAW_RECEIPT_MARKER = 'synthetic_raw_receipt_private_marker'
const RAW_CONFIGURATION_MARKER = 'synthetic_configuration_secret_marker'
const GOVERNED_DECISION_ID = 'ghrd-0123456789abcdef0123456789abcdef'
const IDENTITY_READY_DECISION_ID = 'irghrd-0123456789abcdef0123456789abcdef'
const IDENTITY_READY_AUDIT_REFERENCE = 'irghrd-receipt-0123456789abcdef0123456789abcdef'
const FORMAL_STATE_PRIVATE_DECISION_ID = 'ghrd-fedcba9876543210fedcba9876543210'
const IDENTITY_READY_V02_BINDING_SAFE_HASH =
  'fd1cc2237cade22be397c0007eb8706aa64dced9dbc941cef180aa312c324966'

const SENSITIVE_MARKERS = Object.freeze([
  'synthetic_private_path_marker',
  'synthetic_configuration_value_marker',
  'synthetic_receipt_marker',
  'synthetic_provider_result_content_marker',
  'synthetic_raw_metadata_marker',
  'provider_result_helldivers2-psn-demo_20260720_123627.json',
  RAW_ERROR_MARKER,
  RAW_RECEIPT_MARKER,
  RAW_CONFIGURATION_MARKER,
])

function createGovernedProjectionPayload({
  status = 'governed_record_review_ready',
  humanReviewRequired = true,
  noAutomaticTrustUpgrade = true,
  allowedActions = INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES,
} = {}) {
  return {
    projection_id: INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID,
    projection_status: status,
    projection: {
      projection_status: status,
      source_chain_boundary: 'synthetic_governed_source_boundary',
      record_count_class: status === 'governed_record_review_ready' ? 'exactly_one' : 'zero',
      reservation_count_class: 'exactly_one',
      human_review_required: humanReviewRequired,
      no_automatic_trust_upgrade: noAutomaticTrustUpgrade,
      allowed_actions: Array.isArray(allowedActions) ? [...allowedActions] : allowedActions,
      blocked_actions: ['trust_approval', 'production_promotion'],
      blockers: [],
    },
  }
}

function createGovernedDecisionPostResponse(
  decisionType,
  { status = 201, malformed = false } = {},
) {
  const created = status === 201
  const falseFlags = {
    production_evidenceitem_changed: false,
    production_case_changed: false,
    downstream_runtime_called: false,
    correction_or_revocation_performed: false,
    deleted_or_updated: false,
  }
  const decision = {
    decision_id: GOVERNED_DECISION_ID,
    decision_type: decisionType,
    decision_status: 'recorded_append_only_nonproduction',
    human_review_required: true,
    no_automatic_trust_upgrade: true,
    ...falseFlags,
    private_marker: RAW_CONFIGURATION_MARKER,
  }
  const receipt = {
    decision_id: GOVERNED_DECISION_ID,
    decision_type: decisionType,
    decision_status: 'recorded_append_only_nonproduction',
    outcome: created
      ? 'created_exactly_one_human_review_decision'
      : 'already_exists_same_human_review_decision',
    mutation_count: created ? 1 : 0,
    human_review_required: true,
    no_automatic_trust_upgrade: true,
    ...falseFlags,
    private_marker: RAW_RECEIPT_MARKER,
  }
  return {
    status,
    data: {
      response_schema: malformed
        ? 'synthetic_malformed_schema'
        : 'sentigraph_internal_alpha_governed_review_decision_post_response_v0_1',
      route_mode:
        'internal_disabled_by_default_append_only_nonproduction_human_review_decision_ledger',
      decision_id: GOVERNED_DECISION_ID,
      decision,
      receipt,
      human_review_required: true,
      no_automatic_trust_upgrade: true,
      decision_ledger_write_performed: created,
      production_object_enabled: false,
      review_queue_runtime_enabled: false,
      operator_runtime_ready: false,
      public_ready: false,
      production_ready: false,
    },
  }
}

function createGovernedFormalStateResponse({
  status = 404,
  count = 0,
  extraFields = null,
} = {}) {
  const statusContract = {
    200: ['formal_state_ready', null],
    404: ['formal_state_disabled', 'formal_state_projection_disabled'],
    409: ['formal_state_inconsistent', 'formal_state_integrity_failure'],
    503: ['formal_state_unavailable', 'formal_state_target_unavailable'],
  }[status]
  const ready = status === 200
  const values = {
    response_schema: 'sentigraph_internal_alpha_governed_review_formal_state_projection_v0_1',
    response_version: '0.1',
    route_mode: 'internal_disabled_by_default_read_only_formal_human_review_state_projection',
    projection_status: statusContract[0],
    projection_error_code: statusContract[1],
    formal_first_decision_present: ready,
    formal_second_decision_present: ready && count === 2,
    formal_second_decision_type:
      ready && count === 2 ? 'request_more_governance_review' : null,
    formal_decision_count: ready ? count : 0,
    human_review_required: true,
    no_automatic_trust_upgrade: true,
    write_performed: false,
    production_object_enabled: false,
    review_queue_runtime_enabled: false,
    operator_runtime_ready: false,
    public_ready: false,
    production_ready: false,
    mutable_authority_granted: false,
    third_decision_allowed: false,
  }
  return {
    status,
    data: {
      ...orderedObject(INTERNAL_ALPHA_GOVERNED_REVIEW_FORMAL_STATE_FIELDS, values),
      ...(extraFields || {}),
    },
  }
}

function createIdentityReadyDecisionBindingResponse(
  decisionType = 'keep_pending_human_review',
  { status = 201, malformed = false } = {},
) {
  return {
    status,
    data: {
      response_schema: malformed
        ? 'synthetic_malformed_schema'
        : 'sentigraph_internal_alpha_identity_ready_governed_review_decision_binding_response_v0_1',
      response_version: '0.1',
      route_mode:
        'internal_disabled_by_default_append_only_nonproduction_identity_ready_human_review_decision_ledger',
      request_status: status === 201 ? 'created' : 'already_exists',
      decision_id: IDENTITY_READY_DECISION_ID,
      audit_receipt_reference: IDENTITY_READY_AUDIT_REFERENCE,
      decision_type: decisionType,
      sample_handle: CURRENT_HANDLE,
      review_subject_binding_safe_hash: IDENTITY_READY_V02_BINDING_SAFE_HASH,
      decision_status: 'recorded_append_only_nonproduction_identity_ready',
      outcome:
        status === 201
          ? 'created_exactly_one_identity_ready_human_review_decision'
          : 'already_exists_same_identity_ready_human_review_decision',
      decision_ledger_write_performed: status === 201,
      human_review_required: true,
      no_automatic_trust_upgrade: true,
      production_object_enabled: false,
      analysis_triggered: false,
      report_triggered: false,
    },
  }
}

function createIdentityReadyDecisionAuditResponse({
  status = 200,
  readbackStatus = status === 200 ? 'decision_audit_ready' : 'decision_not_found',
  extraFields = null,
} = {}) {
  const base = {
    response_schema:
      'sentigraph_internal_alpha_identity_ready_governed_review_decision_audit_projection_response_v0_1',
    response_version: '0.1',
    route_mode:
      'internal_disabled_by_default_read_only_identity_ready_human_review_decision_audit_projection',
    readback_status: readbackStatus,
  }
  const values =
    status === 200
      ? {
          ...base,
          decision_id: IDENTITY_READY_DECISION_ID,
          audit_receipt_reference: IDENTITY_READY_AUDIT_REFERENCE,
          sample_handle: CURRENT_HANDLE,
          decision_type: 'keep_pending_human_review',
          decision_status: 'recorded_append_only_nonproduction_identity_ready',
          recorded_at: '2026-08-27T00:00:00Z',
          human_review_required: true,
          no_automatic_trust_upgrade: true,
          production_object_enabled: false,
          review_queue_runtime_enabled: false,
          evidence_layer_write_performed: false,
          provider_or_b05_called: false,
          analysis_triggered: false,
          report_triggered: false,
        }
      : base
  const fields =
    status === 200
      ? INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_AUDIT_SUCCESS_FIELDS
      : INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_AUDIT_ERROR_FIELDS
  return {
    status,
    data: {
      ...orderedObject(fields, values),
      ...(extraFields || {}),
    },
  }
}

function createIdentityReadyDecisionAuditHistoryRow({
  decisionId = IDENTITY_READY_DECISION_ID,
  recordedAt = '2026-08-27T00:00:00Z',
  decisionType = 'keep_pending_human_review',
  extraFields = null,
} = {}) {
  const suffix = decisionId.replace('irghrd-', '')
  return {
    ...orderedObject(
      INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_ROW_FIELDS,
      {
        decision_id: decisionId,
        audit_receipt_reference: `irghrd-receipt-${suffix}`,
        sample_handle: CURRENT_HANDLE,
        decision_type: decisionType,
        decision_status: 'recorded_append_only_nonproduction_identity_ready',
        recorded_at: recordedAt,
        human_review_required: true,
        no_automatic_trust_upgrade: true,
        production_object_enabled: false,
        review_queue_runtime_enabled: false,
        evidence_layer_write_performed: false,
        provider_or_b05_called: false,
        analysis_triggered: false,
        report_triggered: false,
      },
    ),
    ...(extraFields || {}),
  }
}

function createIdentityReadyDecisionAuditHistoryResponse({
  status = 200,
  historyStatus = status === 200 ? 'decision_history_ready' : 'audit_target_absent',
  decisions = [createIdentityReadyDecisionAuditHistoryRow()],
  requestedLimit = 20,
  extraFields = null,
} = {}) {
  const base = {
    response_schema:
      'sentigraph_internal_alpha_identity_ready_governed_review_decision_audit_history_response_v0_1',
    response_version: '0.1',
    route_mode:
      'internal_disabled_by_default_bounded_read_only_identity_ready_human_review_decision_audit_history',
    history_status: historyStatus,
  }
  const values =
    status === 200
      ? {
          ...base,
          requested_limit: requestedLimit,
          returned_count: decisions.length,
          ordering: 'recorded_at_desc_decision_id_desc',
          decisions,
        }
      : base
  const fields =
    status === 200
      ? INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_SUCCESS_FIELDS
      : INTERNAL_ALPHA_IDENTITY_READY_GOVERNED_REVIEW_DECISION_HISTORY_ERROR_FIELDS
  return {
    status,
    data: {
      ...orderedObject(fields, values),
      ...(extraFields || {}),
    },
  }
}

function orderedObject(fields, values) {
  return Object.fromEntries(fields.map((field) => [field, values[field]]))
}

function syntheticSample({
  sampleHandle,
  displayLabel,
  sampleRole,
  isDefault,
  catalogOrder,
}) {
  return orderedObject(INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_FIELDS, {
    sample_handle: sampleHandle,
    display_label: displayLabel,
    sample_role: sampleRole,
    is_default: isDefault,
    enabled: true,
    catalog_order: catalogOrder,
  })
}

function createSyntheticCatalog() {
  return normalizeInternalAlphaLocalExchangeSampleCatalog(
    orderedObject(INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_CATALOG_FIELDS, {
      schema: 'sentigraph_internal_alpha_local_exchange_sample_catalog_v0_1',
      version: '0.1',
      mode: 'internal_alpha_read_only_local_exchange_sample_catalog',
      status: 'ready',
      sample_count: 2,
      default_sample_handle: CURRENT_HANDLE,
      samples: [
        syntheticSample({
          sampleHandle: CURRENT_HANDLE,
          displayLabel: CURRENT_LABEL,
          sampleRole: 'current_curated',
          isDefault: true,
          catalogOrder: 0,
        }),
        syntheticSample({
          sampleHandle: HISTORICAL_HANDLE,
          displayLabel: HISTORICAL_LABEL,
          sampleRole: 'accepted_historical',
          isDefault: false,
          catalogOrder: 1,
        }),
      ],
      read_only: true,
      human_review_required: true,
      production_ready: false,
      mutable_authority_granted: false,
    }),
  )
}

function createSyntheticProjection({
  status,
  marker = null,
  errorCode = null,
  candidateCount = 1,
  blockers = [],
  hiddenBoundaryValues = false,
}) {
  const values = {
    projection_schema: 'sentigraph_local_exchange_review_only_candidate_projection_v0_1',
    projection_version: '0.1',
    projection_mode: 'internal_governed_read_only_review_projection',
    projection_status: status,
    projection_error_code: errorCode,
    source_chain_boundary: hiddenBoundaryValues
      ? 'synthetic_configuration_value_marker'
      : 'synthetic_read_only_source_boundary',
    result_file_name: hiddenBoundaryValues
      ? 'synthetic_private_path_marker.json'
      : 'synthetic_fixture.json',
    upstream_schema: hiddenBoundaryValues
      ? 'synthetic_receipt_marker'
      : 'synthetic_upstream_schema_v0_1',
    upstream_status: 'synthetic_metadata_ready',
    reader_status: 'metadata_ready',
    adapter_status: 'adapted',
    provider_result_status: 'accepted_metadata_only',
    package_resolution_status: 'accepted_metadata_only',
    candidate_count: candidateCount,
    staging_candidate_id: 'synthetic_staging_candidate',
    gate_result_id: 'synthetic_gate_result',
    analysis_request_id: 'synthetic_analysis_request',
    provider_result_id: hiddenBoundaryValues
      ? 'synthetic_provider_result_content_marker'
      : 'synthetic_provider_result',
    package_name: hiddenBoundaryValues
      ? 'synthetic_raw_metadata_marker'
      : 'synthetic_package',
    case_id_hint: 'synthetic_case',
    case_title_hint: hiddenBoundaryValues ? RAW_ERROR_MARKER : 'Synthetic review case',
    validation_summary: hiddenBoundaryValues
      ? { marker: 'synthetic_receipt_marker' }
      : { status: 'synthetic_valid' },
    coverage_summary: hiddenBoundaryValues
      ? { marker: 'synthetic_provider_result_content_marker' }
      : { evidence_count: 1, source_count: 1, comment_count: 1, root_candidate_count: 1 },
    review_status: 'pending_human_review',
    promotion_status: 'not_authorized',
    staging_status: 'in_memory_only',
    gate_summary: hiddenBoundaryValues
      ? { marker: 'synthetic_raw_metadata_marker' }
      : { read_only: true },
    warnings: marker ? [marker] : [],
    blockers,
    allowed_actions: ['review_metadata'],
    blocked_actions: ['persist', 'promote', 'publish', 'export', 'deliver'],
    metadata_only: true,
    review_only: true,
    human_review_required: true,
    no_automatic_trust_upgrade: true,
    candidate_persistence: 'in_memory_only',
    persistent_staging_write: false,
    review_decision_write: false,
    evidence_layer_write: false,
    production_evidenceitem_created: false,
    production_case_created: false,
    analysis_run_created: false,
    analysis_result_created: false,
    frontend_action_enabled: false,
    public_output_enabled: false,
    export_delivery_enabled: false,
    path_exposed: false,
    raw_metadata_exposed: false,
    trust_approved: false,
    production_ready: false,
    promotion_completed: false,
    mutable_authority_granted: false,
  }

  return normalizeInternalAlphaLocalExchangeProjection(
    orderedObject(INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTION_FIELDS, values),
  )
}

function createSyntheticIdentityReadyV02ProjectionRaw() {
  const legacyProjection = createSyntheticProjection({
    status: 'ready_for_human_review',
  })
  const reviewSubjectIdentity = orderedObject(B05_REVIEW_SUBJECT_IDENTITY_FIELDS, {
    identity_schema: 'sentigraph_b05_review_subject_identity_v0_1',
    identity_version: '0.1',
    identity_status: 'ready',
    sample_handle: CURRENT_HANDLE,
    result_file_name: legacyProjection.result_file_name,
    package_name: legacyProjection.package_name,
    provider_result_content_bytes: 1234,
    provider_result_content_sha256: '1'.repeat(64),
    metadata_profile: 'governed_b05_five_file',
    metadata_entry_count: 5,
    safe_metadata_bundle_sha256: '2'.repeat(64),
    review_subject_content_safe_hash: '3'.repeat(64),
    review_subject_binding_safe_hash: IDENTITY_READY_V02_BINDING_SAFE_HASH,
  })
  return orderedObject(INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_PROJECTION_FIELDS, {
    ...legacyProjection,
    projection_schema: 'sentigraph_local_exchange_review_only_candidate_projection_v0_2',
    projection_version: '0.2',
    review_status: 'ready_for_human_review',
    review_subject_identity: reviewSubjectIdentity,
  })
}

const SYNTHETIC_CATALOG = createSyntheticCatalog()
const CURRENT_PROJECTION = createSyntheticProjection({
  status: 'ready_for_human_review',
  marker: CURRENT_MARKER,
})
const HISTORICAL_PROJECTION = createSyntheticProjection({
  status: 'manual_review_required',
  marker: HISTORICAL_MARKER,
})
const IDENTITY_READY_V02_PROJECTION_RAW = createSyntheticIdentityReadyV02ProjectionRaw()
const IDENTITY_READY_V02_PROJECTION =
  normalizeInternalAlphaLocalExchangeIdentityReadyV02Projection(
    IDENTITY_READY_V02_PROJECTION_RAW,
  )

function deferred() {
  let resolve
  let reject
  const promise = new Promise((resolvePromise, rejectPromise) => {
    resolve = resolvePromise
    reject = rejectPromise
  })
  return { promise, resolve, reject }
}

async function chooseAntDesignOption(selectorLabel, optionLabel) {
  const selector = screen.getByRole('combobox', { name: selectorLabel })
  fireEvent.mouseDown(selector)

  const option = await waitFor(() => {
    const candidates = screen.getAllByText(optionLabel, { exact: true })
    const optionContent = candidates.find((candidate) =>
      candidate.closest('.ant-select-item-option'),
    )
    if (!optionContent) throw new Error('synthetic_option_not_ready')
    return optionContent
  })

  fireEvent.click(option)
  await waitFor(() => {
    const selectRoot = selector.closest('.ant-select')
    expect(selectRoot?.textContent).toContain(optionLabel)
  })
}

function expectSelectedLabel(selectorLabel, selectedLabel) {
  const selector = screen.getByRole('combobox', { name: selectorLabel })
  expect(selector.closest('.ant-select')?.textContent).toContain(selectedLabel)
}

async function openLocalExchangeReview() {
  await chooseAntDesignOption(
    'Read-only review surface',
    'Local-exchange projection review',
  )
}

async function openIdentityReadyV02Review() {
  await chooseAntDesignOption(
    'Read-only review surface',
    'Local-exchange identity-ready review v0.2',
  )
}

async function openIdentityReadyDurableDecisionAuditReadback() {
  await chooseAntDesignOption(
    'Read-only review surface',
    'Identity-ready durable decision audit readback',
  )
}

async function renderResolvedProjection(projection) {
  apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
  apiMocks.getInternalAlphaLocalExchangeProjection.mockResolvedValue(projection)
  render(<InternalAlphaReviewConsole />)
  await openLocalExchangeReview()
  await waitFor(() => {
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(1)
  })
}

async function renderGovernedProjection(payload = createGovernedProjectionPayload()) {
  apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
  apiMocks.getInternalAlphaReviewConsoleProjection.mockResolvedValue(payload)
  const renderResult = render(<InternalAlphaReviewConsole />)
  const expectedStatus = payload?.error
    ? payload.error === 'route_disabled'
      ? 'disabled'
      : 'governed_disabled'
    : payload.projection_status
  await screen.findByText(expectedStatus, { exact: true })
  return renderResult
}

async function selectGovernedDecision(decisionType) {
  await chooseAntDesignOption('Governed human-review decision type', decisionType)
}

describe('InternalAlphaReviewConsole StrictMode hydration', () => {
  it('requests the governed projection once and applies the retained first result', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)

    render(
      <React.StrictMode>
        <InternalAlphaReviewConsole />
      </React.StrictMode>,
    )

    expect(await screen.findByText('disabled', { exact: true })).toBeTruthy()
    expect(screen.getByText('backend route disabled', { exact: true })).toBeTruthy()
    expect(apiMocks.getInternalAlphaReviewConsoleProjection).toHaveBeenCalledTimes(1)
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
  })
})

const compatibilityDescriptors = new Map()
const networkDescriptors = new Map()
let consoleErrors
let consoleWarnings
let consoleErrorSpy
let consoleWarningSpy
let networkAttempts

function rememberAndReplace(target, property, value, descriptorStore) {
  descriptorStore.set(`${target === globalThis ? 'global' : 'prototype'}:${property}`, {
    target,
    property,
    descriptor: Object.getOwnPropertyDescriptor(target, property),
  })
  Object.defineProperty(target, property, {
    configurable: true,
    writable: true,
    value,
  })
}

function restoreDescriptors(descriptorStore) {
  for (const { target, property, descriptor } of descriptorStore.values()) {
    if (descriptor) Object.defineProperty(target, property, descriptor)
    else delete target[property]
  }
  descriptorStore.clear()
}

beforeEach(() => {
  identityReadyDecisionCandidateMocks.build.mockClear()
  apiMocks.apiClientGet.mockReset()
  apiMocks.apiClientPost.mockReset()
  apiMocks.getInternalAlphaReviewConsoleProjection.mockReset()
  apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockReset()
  apiMocks.getInternalAlphaLocalExchangeProjection.mockReset()
  apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection.mockReset()
  apiMocks.apiClientGet.mockResolvedValue(createGovernedFormalStateResponse())
  apiMocks.getInternalAlphaReviewConsoleProjection.mockResolvedValue({ error: 'route_disabled' })

  consoleErrors = []
  consoleWarnings = []
  consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation((...args) => {
    consoleErrors.push(args.map(String).join(' '))
  })
  consoleWarningSpy = vi.spyOn(console, 'warn').mockImplementation((...args) => {
    consoleWarnings.push(args.map(String).join(' '))
  })

  const originalGetComputedStyle = window.getComputedStyle.bind(window)
  rememberAndReplace(
    window,
    'getComputedStyle',
    (element) => originalGetComputedStyle(element),
    compatibilityDescriptors,
  )
  rememberAndReplace(
    window,
    'matchMedia',
    vi.fn().mockImplementation((query) => ({
      matches: false,
      media: query,
      onchange: null,
      addListener: vi.fn(),
      removeListener: vi.fn(),
      addEventListener: vi.fn(),
      removeEventListener: vi.fn(),
      dispatchEvent: vi.fn(() => false),
    })),
    compatibilityDescriptors,
  )
  class TestResizeObserver {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  rememberAndReplace(globalThis, 'ResizeObserver', TestResizeObserver, compatibilityDescriptors)
  rememberAndReplace(
    HTMLElement.prototype,
    'scrollIntoView',
    vi.fn(),
    compatibilityDescriptors,
  )
  rememberAndReplace(HTMLElement.prototype, 'scrollTo', vi.fn(), compatibilityDescriptors)

  networkAttempts = 0
  const failNetwork = (mechanism) => {
    networkAttempts += 1
    throw new Error(`unexpected_${mechanism}_network_attempt`)
  }
  rememberAndReplace(
    globalThis,
    'fetch',
    vi.fn(() => failNetwork('fetch')),
    networkDescriptors,
  )
  rememberAndReplace(
    globalThis,
    'XMLHttpRequest',
    class GuardedXMLHttpRequest {
      constructor() {
        failNetwork('xml_http_request')
      }
    },
    networkDescriptors,
  )
  rememberAndReplace(
    globalThis,
    'WebSocket',
    class GuardedWebSocket {
      constructor() {
        failNetwork('web_socket')
      }
    },
    networkDescriptors,
  )
  rememberAndReplace(
    globalThis,
    'EventSource',
    class GuardedEventSource {
      constructor() {
        failNetwork('event_source')
      }
    },
    networkDescriptors,
  )
})

afterEach(() => {
  cleanup()
  expect(networkAttempts).toBe(0)
  expect(consoleErrors).toEqual([])
  expect(consoleWarnings).toEqual([])
  consoleErrorSpy.mockRestore()
  consoleWarningSpy.mockRestore()
  restoreDescriptors(networkDescriptors)
  restoreDescriptors(compatibilityDescriptors)
  vi.clearAllMocks()
})

describe('InternalAlphaReviewConsole bounded formal-state hydration contract', () => {
  it.each([
    [1, false, null],
    [2, true, 'request_more_governance_review'],
  ])('normalizes the exact 19-field ready projection for count=%s', (
    count,
    secondPresent,
    secondType,
  ) => {
    const response = createGovernedFormalStateResponse({ status: 200, count })
    const result = normalizeInternalAlphaGovernedReviewFormalStateProjection(
      response.data,
      response.status,
    )

    expect(Object.keys(result)).toEqual(INTERNAL_ALPHA_GOVERNED_REVIEW_FORMAL_STATE_FIELDS)
    expect(result.formal_decision_count).toBe(count)
    expect(result.formal_first_decision_present).toBe(true)
    expect(result.formal_second_decision_present).toBe(secondPresent)
    expect(result.formal_second_decision_type).toBe(secondType)
    expect(result.write_performed).toBe(false)
    expect(result.no_automatic_trust_upgrade).toBe(true)
    expect(result.production_ready).toBe(false)
    expect(result.mutable_authority_granted).toBe(false)
  })

  it.each([
    [404, 'formal_state_disabled', 'formal_state_projection_disabled'],
    [409, 'formal_state_inconsistent', 'formal_state_integrity_failure'],
    [503, 'formal_state_unavailable', 'formal_state_target_unavailable'],
  ])('maps HTTP %s to one bounded non-ready state', async (
    status,
    projectionStatus,
    errorCode,
  ) => {
    const response = createGovernedFormalStateResponse({ status })
    apiMocks.apiClientGet.mockRejectedValue({ response })

    const result = await getInternalAlphaGovernedReviewFormalState()

    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
    expect(apiMocks.apiClientGet).toHaveBeenCalledWith(
      '/api/v1/internal/alpha/governed-review-decisions/formal-state',
    )
    expect(result.projection_status).toBe(projectionStatus)
    expect(result.projection_error_code).toBe(errorCode)
    expect(result.formal_decision_count).toBe(0)
    expect(result.formal_first_decision_present).toBe(false)
    expect(result.formal_second_decision_present).toBe(false)
  })

  it('rejects an extra raw decision identity field', () => {
    const response = createGovernedFormalStateResponse({
      status: 200,
      count: 2,
      extraFields: { decision_id: FORMAL_STATE_PRIVATE_DECISION_ID },
    })

    expect(() =>
      normalizeInternalAlphaGovernedReviewFormalStateProjection(
        response.data,
        response.status,
      ),
    ).toThrow('frontend_governed_review_formal_state_contract_mismatch')
  })

  it('performs exactly one bounded hydration GET per page mount', async () => {
    apiMocks.apiClientGet.mockResolvedValue(
      createGovernedFormalStateResponse({ status: 404 }),
    )

    await renderGovernedProjection()

    expect(await screen.findByText('formal_state_disabled', { exact: true })).toBeTruthy()
    expect(screen.getByText('formal_state_projection_disabled', { exact: true })).toBeTruthy()
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
    expect(apiMocks.apiClientGet).toHaveBeenCalledWith(
      '/api/v1/internal/alpha/governed-review-decisions/formal-state',
    )
  })

  it.each([
    [1, null],
    [2, 'request_more_governance_review'],
  ])('renders only the bounded ready summary for count=%s', async (
    count,
    secondType,
  ) => {
    apiMocks.apiClientGet.mockResolvedValue(
      createGovernedFormalStateResponse({ status: 200, count }),
    )

    const { container } = await renderGovernedProjection()

    expect(await screen.findByText('formal_state_ready', { exact: true })).toBeTruthy()
    if (secondType) {
      const secondDecisionTypeLabel = screen.getByText('formal_second_decision_type', { exact: true })
      const secondDecisionTypeItem = secondDecisionTypeLabel.closest('tr')

      expect(secondDecisionTypeItem).not.toBeNull()
      expect(within(secondDecisionTypeItem).getByText(secondType, { exact: true })).toBeTruthy()
    }
    expect(container.textContent).not.toContain(FORMAL_STATE_PRIVATE_DECISION_ID)
    expect(container.textContent).not.toContain('idempotency_key')
    expect(container.textContent).not.toContain('recorded_at')
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
  })

  it('uses no client persistence and performs no GET after the governed POST', async () => {
    const localGet = vi.spyOn(Storage.prototype, 'getItem')
    const localSet = vi.spyOn(Storage.prototype, 'setItem')
    const localRemove = vi.spyOn(Storage.prototype, 'removeItem')
    try {
      apiMocks.apiClientGet.mockResolvedValue(
        createGovernedFormalStateResponse({ status: 200, count: 2 }),
      )
      apiMocks.apiClientPost.mockResolvedValue(
        createGovernedDecisionPostResponse('keep_pending_human_review'),
      )
      const { container } = await renderGovernedProjection()
      await waitFor(() => {
        expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
      })
      await selectGovernedDecision('keep_pending_human_review')

      fireEvent.click(screen.getByRole('button', { name: 'Confirm governed decision' }))

      await waitFor(() => {
        expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
      })
      expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
      expect(localGet).toHaveBeenCalledTimes(0)
      expect(localSet).toHaveBeenCalledTimes(0)
      expect(localRemove).toHaveBeenCalledTimes(0)
      expect(container.textContent).not.toContain(FORMAL_STATE_PRIVATE_DECISION_ID)
    } finally {
      localGet.mockRestore()
      localSet.mockRestore()
      localRemove.mockRestore()
    }
  })

  it('maps an unbounded transport failure to a fixed frontend error surface', async () => {
    apiMocks.apiClientGet.mockRejectedValue(new Error(RAW_ERROR_MARKER))

    const { container } = await renderGovernedProjection()

    expect(
      await screen.findByText('Formal decision state failed closed', { exact: true }),
    ).toBeTruthy()
    expect(container.textContent).not.toContain(RAW_ERROR_MARKER)
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
  })
})

describe('InternalAlphaReviewConsole governed human-review decision contract', () => {
  it('performs zero governed decision POSTs on page render', async () => {
    await renderGovernedProjection({ error: 'route_disabled' })

    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it.each([
    ['route disabled', { error: 'route_disabled' }],
    ['governed projection disabled', { error: 'governed_record_projection_disabled' }],
    [
      'record absent',
      createGovernedProjectionPayload({ status: 'governed_record_absent' }),
    ],
    [
      'record inconsistent',
      createGovernedProjectionPayload({ status: 'governed_record_inconsistent' }),
    ],
    [
      'record blocked',
      createGovernedProjectionPayload({
        status: 'governed_record_read_blocked_sidecar_present',
      }),
    ],
    [
      'target unavailable',
      createGovernedProjectionPayload({ status: 'governed_record_target_unavailable' }),
    ],
    [
      'bounded read-only audit failure',
      createGovernedProjectionPayload({ status: 'governed_record_read_only_audit_failed' }),
    ],
    [
      'missing allowed-actions array',
      createGovernedProjectionPayload({ allowedActions: null }),
    ],
    [
      'missing human-review requirement',
      createGovernedProjectionPayload({ humanReviewRequired: false }),
    ],
    [
      'automatic trust-upgrade invariant mismatch',
      createGovernedProjectionPayload({ noAutomaticTrustUpgrade: false }),
    ],
  ])('keeps decision controls inactive for %s', async (_label, payload) => {
    await renderGovernedProjection(payload)

    expect(screen.getByRole('combobox', { name: 'Governed human-review decision type' }).disabled).toBe(true)
    expect(screen.getByRole('button', { name: 'Confirm governed decision' }).disabled).toBe(true)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it('does not expose governed decision controls on the Local-exchange review surface', async () => {
    apiMocks.getInternalAlphaLocalExchangeProjection.mockResolvedValue(CURRENT_PROJECTION)
    await renderGovernedProjection()
    await openLocalExchangeReview()

    expect(screen.queryByRole('combobox', { name: 'Governed human-review decision type' })).toBeNull()
    expect(screen.queryByRole('button', { name: 'Confirm governed decision' })).toBeNull()
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it('exposes exactly the two allowed decision labels without unsafe action controls', async () => {
    await renderGovernedProjection()

    const selector = screen.getByRole('combobox', {
      name: 'Governed human-review decision type',
    })
    expect(selector.disabled).toBe(false)
    expect(INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES).toEqual([
      'keep_pending_human_review',
      'request_more_governance_review',
    ])

    fireEvent.mouseDown(selector)
    for (const decisionType of INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES) {
      const optionMatches = await screen.findAllByText(decisionType, { exact: true })
      expect(
        optionMatches.filter((candidate) => candidate.closest('.ant-select-item-option')),
      ).toHaveLength(1)
    }

    const forbiddenControlName = /trust|production|correction|revocation|delete|publish|export|deliver/i
    for (const role of ['button', 'checkbox', 'radio', 'switch']) {
      expect(screen.queryByRole(role, { name: forbiddenControlName })).toBeNull()
    }
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it('performs zero POSTs when a decision is selected without confirmation', async () => {
    await renderGovernedProjection()
    await selectGovernedDecision('keep_pending_human_review')

    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it.each(INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES)(
    'posts %s exactly once only after explicit confirmation',
    async (decisionType) => {
      apiMocks.apiClientPost.mockResolvedValue(
        createGovernedDecisionPostResponse(decisionType),
      )
      await renderGovernedProjection()
      await selectGovernedDecision(decisionType)

      fireEvent.click(screen.getByRole('button', { name: 'Confirm governed decision' }))

      await waitFor(() => {
        expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
      })
      expect(apiMocks.apiClientPost).toHaveBeenCalledWith(
        '/api/v1/internal/alpha/governed-review-decisions/decisions',
        {
          request_schema:
            'sentigraph_governed_nonproduction_human_review_decision_request_v0_1',
          request_version: '0.1',
          decision_type: decisionType,
        },
      )
      expect(await screen.findByText('created', { exact: true })).toBeTruthy()
    },
  )

  it('allows at most one POST attempt per page mount while the request is pending', async () => {
    const postRequest = deferred()
    apiMocks.apiClientPost.mockReturnValue(postRequest.promise)
    await renderGovernedProjection()
    await selectGovernedDecision('keep_pending_human_review')
    const confirmButton = screen.getByRole('button', { name: 'Confirm governed decision' })

    fireEvent.click(confirmButton)
    fireEvent.click(confirmButton)

    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
    await act(async () => {
      postRequest.resolve(
        createGovernedDecisionPostResponse('keep_pending_human_review'),
      )
      await postRequest.promise
    })
    expect(await screen.findByText('created', { exact: true })).toBeTruthy()
    fireEvent.click(confirmButton)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
  })

  it('displays only the normalized bounded success subset', async () => {
    apiMocks.apiClientPost.mockResolvedValue(
      createGovernedDecisionPostResponse('request_more_governance_review'),
    )
    const { container } = await renderGovernedProjection()
    await selectGovernedDecision('request_more_governance_review')
    fireEvent.click(screen.getByRole('button', { name: 'Confirm governed decision' }))

    expect(await screen.findByText(GOVERNED_DECISION_ID, { exact: true })).toBeTruthy()
    expect(screen.getByText('recorded_append_only_nonproduction', { exact: true })).toBeTruthy()
    expect(
      screen.getByText('created_exactly_one_human_review_decision', { exact: true }),
    ).toBeTruthy()
    for (const marker of [RAW_RECEIPT_MARKER, RAW_CONFIGURATION_MARKER]) {
      expect(container.textContent).not.toContain(marker)
    }
  })

  it('fails closed without exposing a raw backend error', async () => {
    apiMocks.apiClientPost.mockRejectedValue(new Error(RAW_ERROR_MARKER))
    const { container } = await renderGovernedProjection()
    await selectGovernedDecision('keep_pending_human_review')
    fireEvent.click(screen.getByRole('button', { name: 'Confirm governed decision' }))

    expect(
      await screen.findByText('Governed decision request failed closed', { exact: true }),
    ).toBeTruthy()
    expect(container.textContent).not.toContain(RAW_ERROR_MARKER)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
  })

  it('fails closed on a malformed success response', async () => {
    const malformed = createGovernedDecisionPostResponse(
      'keep_pending_human_review',
      { malformed: true },
    )
    expect(() =>
      normalizeInternalAlphaGovernedReviewDecisionPostResponse(
        malformed.data,
        malformed.status,
        'keep_pending_human_review',
      ),
    ).toThrow('frontend_governed_review_decision_contract_mismatch')

    apiMocks.apiClientPost.mockResolvedValue(malformed)
    await renderGovernedProjection()
    await selectGovernedDecision('keep_pending_human_review')
    fireEvent.click(screen.getByRole('button', { name: 'Confirm governed decision' }))
    expect(
      await screen.findByText('Governed decision request failed closed', { exact: true }),
    ).toBeTruthy()
  })

  it('normalizes an idempotent HTTP 200 response to the bounded safe subset', async () => {
    apiMocks.apiClientPost.mockResolvedValue(
      createGovernedDecisionPostResponse('keep_pending_human_review', { status: 200 }),
    )

    const result = await postInternalAlphaGovernedReviewDecision(
      'keep_pending_human_review',
    )

    expect(result).toEqual({
      request_status: 'already_exists',
      decision_id: GOVERNED_DECISION_ID,
      decision_type: 'keep_pending_human_review',
      decision_status: 'recorded_append_only_nonproduction',
      outcome: 'already_exists_same_human_review_decision',
      decision_ledger_write_performed: false,
      human_review_required: true,
      no_automatic_trust_upgrade: true,
      production_ready: false,
    })
    expect(JSON.stringify(result)).not.toContain(RAW_RECEIPT_MARKER)
    expect(JSON.stringify(result)).not.toContain(RAW_CONFIGURATION_MARKER)
  })

  it('maps an expected non-success response to a fixed bounded state', async () => {
    const response = createGovernedDecisionPostResponse(
      'request_more_governance_review',
      { status: 404 },
    )
    apiMocks.apiClientPost.mockRejectedValue({ response })

    const result = await postInternalAlphaGovernedReviewDecision(
      'request_more_governance_review',
    )

    expect(result).toEqual({
      request_status: 'blocked_http_404',
      decision_ledger_write_performed: false,
      human_review_required: true,
      no_automatic_trust_upgrade: true,
      production_ready: false,
    })
    expect(JSON.stringify(result)).not.toContain(RAW_RECEIPT_MARKER)
    expect(JSON.stringify(result)).not.toContain(RAW_CONFIGURATION_MARKER)
  })

  it('rejects an unsupported client decision type before HTTP', async () => {
    await expect(
      postInternalAlphaGovernedReviewDecision('trust_approval'),
    ).rejects.toThrow('frontend_governed_review_decision_contract_mismatch')
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })
})

describe('InternalAlphaReviewConsole synthetic local-exchange component contract', () => {
  it('loads the catalog, defaults to current, switches samples, and reuses each handle cache', async () => {
    const catalogRequest = deferred()
    const currentRequest = deferred()
    const historicalRequest = deferred()
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockReturnValue(catalogRequest.promise)
    apiMocks.getInternalAlphaLocalExchangeProjection.mockImplementation((sampleHandle) => {
      if (sampleHandle === CURRENT_HANDLE) return currentRequest.promise
      if (sampleHandle === HISTORICAL_HANDLE) return historicalRequest.promise
      return Promise.reject(new Error('unexpected_synthetic_handle'))
    })

    render(<InternalAlphaReviewConsole />)
    await openLocalExchangeReview()

    expect(screen.getByText('Loading sample catalog', { exact: true })).toBeTruthy()
    expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(0)

    await act(async () => {
      catalogRequest.resolve(SYNTHETIC_CATALOG)
      await catalogRequest.promise
    })

    await waitFor(() => {
      expectSelectedLabel('Read-only local-exchange sample', CURRENT_LABEL)
      expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledWith(CURRENT_HANDLE)
    })
    expect(screen.getByRole('heading', { name: 'loading' })).toBeTruthy()

    await act(async () => {
      currentRequest.resolve(CURRENT_PROJECTION)
      await currentRequest.promise
    })
    expect(await screen.findByText(CURRENT_MARKER, { exact: true })).toBeTruthy()
    expect(screen.getAllByText('ready_for_human_review', { exact: true }).length).toBeGreaterThan(0)

    await chooseAntDesignOption('Read-only local-exchange sample', HISTORICAL_LABEL)
    await waitFor(() => {
      expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledWith(HISTORICAL_HANDLE)
    })
    expect(screen.getByRole('heading', { name: 'loading' })).toBeTruthy()

    await act(async () => {
      historicalRequest.resolve(HISTORICAL_PROJECTION)
      await historicalRequest.promise
    })
    expect(await screen.findByText(HISTORICAL_MARKER, { exact: true })).toBeTruthy()
    expect(screen.getAllByText('manual_review_required', { exact: true }).length).toBeGreaterThan(0)

    await chooseAntDesignOption('Read-only local-exchange sample', CURRENT_LABEL)
    expect(await screen.findByText(CURRENT_MARKER, { exact: true })).toBeTruthy()
    await chooseAntDesignOption('Read-only local-exchange sample', HISTORICAL_LABEL)
    expect(await screen.findByText(HISTORICAL_MARKER, { exact: true })).toBeTruthy()

    expect(apiMocks.getInternalAlphaReviewConsoleProjection).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(2)
    expect(
      apiMocks.getInternalAlphaLocalExchangeProjection.mock.calls.filter(
        ([sampleHandle]) => sampleHandle === CURRENT_HANDLE,
      ),
    ).toHaveLength(1)
    expect(
      apiMocks.getInternalAlphaLocalExchangeProjection.mock.calls.filter(
        ([sampleHandle]) => sampleHandle === HISTORICAL_HANDLE,
      ),
    ).toHaveLength(1)
  })

  it('renders the blocked_upstream projection phase without broadening authority', async () => {
    const projection = createSyntheticProjection({
      status: 'blocked_upstream',
      errorCode: 'synthetic_upstream_blocked',
      candidateCount: 0,
      blockers: ['synthetic_blocked_upstream_marker'],
    })
    await renderResolvedProjection(projection)

    expect(await screen.findByText('synthetic_blocked_upstream_marker', { exact: true })).toBeTruthy()
    expect(screen.getAllByText('blocked_upstream', { exact: true }).length).toBeGreaterThan(0)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(1)
  })

  it('renders the projection_unavailable phase as unavailable', async () => {
    const projection = createSyntheticProjection({
      status: 'projection_unavailable',
      errorCode: 'synthetic_projection_unavailable',
      candidateCount: 0,
    })
    await renderResolvedProjection(projection)

    expect(await screen.findByRole('heading', { name: 'unavailable' })).toBeTruthy()
    expect(screen.getAllByText('projection_unavailable', { exact: true }).length).toBeGreaterThan(0)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(1)
  })

  it('maps a rejected projection helper to bounded_error without exposing the raw error', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.getInternalAlphaLocalExchangeProjection.mockRejectedValue(new Error(RAW_ERROR_MARKER))
    const { container } = render(<InternalAlphaReviewConsole />)
    await openLocalExchangeReview()

    expect(await screen.findByRole('heading', { name: 'bounded_error' })).toBeTruthy()
    expect(screen.getByText('error code = frontend_projection_contract_mismatch', { exact: true })).toBeTruthy()
    expect(container.textContent).not.toContain(RAW_ERROR_MARKER)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(1)
  })

  it('fails closed when the sample catalog is unavailable and issues zero projection requests', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockRejectedValue(
      new Error('synthetic_catalog_private_error'),
    )
    const { container } = render(<InternalAlphaReviewConsole />)
    await openLocalExchangeReview()

    expect(
      (await screen.findAllByText('Sample catalog unavailable', { exact: true })).length,
    ).toBeGreaterThanOrEqual(1)
    expect(container.textContent).not.toContain('synthetic_catalog_private_error')
    expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(0)
  })

  it('renders the read-only human-review safety boundary without mutation controls or sensitive markers', async () => {
    const safetyProjection = createSyntheticProjection({
      status: 'ready_for_human_review',
      hiddenBoundaryValues: true,
    })
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.getInternalAlphaLocalExchangeProjection.mockResolvedValue(safetyProjection)
    const { container } = render(<InternalAlphaReviewConsole />)
    await openLocalExchangeReview()
    await screen.findByRole('heading', { name: 'loaded' })

    for (const visibleBoundary of [
      'Read-only and human-review-only.',
      'Not a persisted governed record.',
      'Not trust approval.',
      'Not production readiness.',
      'metadata_only = true',
      'review_only = true',
      'no_automatic_trust_upgrade = true',
      'persistent_staging_write = false',
      'review_decision_write = false',
      'production_ready = false',
      'public_output_enabled = false',
    ]) {
      expect(screen.getByText(visibleBoundary, { exact: true })).toBeTruthy()
    }

    const forbiddenControlName = /approve|persist|promote|publish|export|deliver|mutation/i
    for (const role of ['button', 'link', 'menuitem', 'checkbox', 'radio', 'switch']) {
      expect(screen.queryByRole(role, { name: forbiddenControlName })).toBeNull()
    }
    for (const marker of SENSITIVE_MARKERS) {
      expect(container.textContent).not.toContain(marker)
    }

    expect(apiMocks.getInternalAlphaReviewConsoleProjection).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(1)
  })
})

describe('InternalAlphaReviewConsole identity-ready v0.2 read-only surface', () => {
  it('strictly normalizes the exact ordered 53/13-field contract and fails closed', () => {
    const normalized = normalizeInternalAlphaLocalExchangeIdentityReadyV02Projection(
      IDENTITY_READY_V02_PROJECTION_RAW,
    )

    expect(Object.keys(normalized)).toEqual(
      INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_PROJECTION_FIELDS,
    )
    expect(Object.keys(normalized.review_subject_identity)).toEqual(
      B05_REVIEW_SUBJECT_IDENTITY_FIELDS,
    )
    expect(normalized.projection_schema).toBe(
      'sentigraph_local_exchange_review_only_candidate_projection_v0_2',
    )
    expect(normalized.projection_version).toBe('0.2')
    expect(normalized.review_subject_identity.identity_status).toBe('ready')
    expect(normalized.review_subject_identity.review_subject_binding_safe_hash).toBe(
      IDENTITY_READY_V02_BINDING_SAFE_HASH,
    )

    expect(() =>
      normalizeInternalAlphaLocalExchangeIdentityReadyV02Projection({
        ...IDENTITY_READY_V02_PROJECTION_RAW,
        unexpected_field: true,
      }),
    ).toThrow('frontend_identity_ready_v0_2_projection_contract_mismatch')

    const mismatchedIdentity = orderedObject(B05_REVIEW_SUBJECT_IDENTITY_FIELDS, {
      ...IDENTITY_READY_V02_PROJECTION_RAW.review_subject_identity,
      review_subject_binding_safe_hash: '0'.repeat(64),
    })
    const mismatchedProjection = orderedObject(
      INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_PROJECTION_FIELDS,
      {
        ...IDENTITY_READY_V02_PROJECTION_RAW,
        review_subject_identity: mismatchedIdentity,
      },
    )
    expect(() =>
      normalizeInternalAlphaLocalExchangeIdentityReadyV02Projection(
        mismatchedProjection,
      ),
    ).toThrow('frontend_identity_ready_v0_2_projection_contract_mismatch')
  })

  it('allows only the exact current handle and issues one GET to the exact v0.2 URL', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    apiMocks.apiClientGet.mockResolvedValue({ data: IDENTITY_READY_V02_PROJECTION_RAW })

    const projection =
      await actualApi.getInternalAlphaLocalExchangeIdentityReadyV02Projection(
        INTERNAL_ALPHA_LOCAL_EXCHANGE_IDENTITY_READY_V02_SAMPLE_HANDLE,
      )

    expect(projection).toEqual(IDENTITY_READY_V02_PROJECTION)
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
    expect(apiMocks.apiClientGet).toHaveBeenCalledWith(
      '/api/v1/internal/alpha/review-console/v0.2/local-exchange-projections/helldivers2-psn-demo',
    )
    await expect(
      actualApi.getInternalAlphaLocalExchangeIdentityReadyV02Projection(
        HISTORICAL_HANDLE,
      ),
    ).rejects.toThrow('Unsupported internal alpha identity-ready v0.2 sample handle')
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(1)
  })

  it('waits for explicit selection, requests once per mount, and keeps the panel display-only', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection.mockResolvedValue(
      IDENTITY_READY_V02_PROJECTION,
    )

    const { container } = render(<InternalAlphaReviewConsole />)
    await waitFor(() => {
      expect(apiMocks.getInternalAlphaLocalExchangeSampleCatalog).toHaveBeenCalledTimes(1)
    })
    expect(apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection).toHaveBeenCalledTimes(0)

    await openIdentityReadyV02Review()
    await waitFor(() => {
      expect(
        apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
      ).toHaveBeenCalledTimes(1)
    })
    expect(
      apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
    ).toHaveBeenCalledWith(CURRENT_HANDLE)
    expect(await screen.findByText(IDENTITY_READY_V02_BINDING_SAFE_HASH, { exact: true })).toBeTruthy()

    for (const visibleText of [
      'Curated display label = Current curated sample',
      'sample_handle = helldivers2-psn-demo',
      'Human review required.',
      'Metadata-only.',
      'In-memory-only.',
      'No automatic trust upgrade.',
      'Not full-web coverage.',
      'Not full-platform coverage.',
      'Not official verification.',
      'No decision has yet been made.',
      'metadata_only = true',
      'candidate_persistence = in_memory_only',
    ]) {
      expect(screen.getByText(visibleText, { exact: true })).toBeTruthy()
    }

    for (const role of ['button', 'link', 'menuitem', 'checkbox', 'radio', 'switch']) {
      expect(
        screen.queryByRole(role, {
          name: /approve|reject|weak|source|merge|reset|promote|persist|analyze|report|publish|export|deliver|copy/i,
        }),
      ).toBeNull()
    }
    for (const sensitiveField of [
      'result_file_name',
      'package_name',
      'provider_result_content_bytes',
      'provider_result_content_sha256',
      'safe_metadata_bundle_sha256',
    ]) {
      expect(container.textContent).not.toContain(sensitiveField)
    }

    await chooseAntDesignOption(
      'Read-only review surface',
      'Governed record review (default)',
    )
    await openIdentityReadyV02Review()
    expect(
      apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
    ).toHaveBeenCalledTimes(1)
    expect(apiMocks.getInternalAlphaLocalExchangeProjection).toHaveBeenCalledTimes(0)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })
})

describe('InternalAlphaReviewConsole identity-ready governed decision candidate surface', () => {
  async function renderIdentityReadyDecisionCandidateSurface() {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection.mockResolvedValue(
      IDENTITY_READY_V02_PROJECTION,
    )

    const renderResult = render(<InternalAlphaReviewConsole />)
    await openIdentityReadyV02Review()
    await waitFor(() => {
      expect(
        apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
      ).toHaveBeenCalledTimes(1)
    })
    await screen.findByText(IDENTITY_READY_V02_BINDING_SAFE_HASH, { exact: true })
    return renderResult
  }

  it('starts without an action or candidate and exposes only the two safe actions', async () => {
    await renderIdentityReadyDecisionCandidateSurface()

    const selector = screen.getByRole('combobox', {
      name: 'Identity-ready human-review decision candidate action',
    })
    const confirmButton = screen.getByRole('button', {
      name: 'Confirm local decision candidate',
    })
    expect(selector).toBeTruthy()
    expect(confirmButton.disabled).toBe(true)
    expect(
      screen.queryByText(
        'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
        { exact: true },
      ),
    ).toBeNull()

    fireEvent.mouseDown(selector)
    expect(await screen.findByText('Keep pending human review', { exact: true })).toBeTruthy()
    expect(
      await screen.findByText('Request more governance review', { exact: true }),
    ).toBeTruthy()
    expect(screen.queryByText('Approve trust', { exact: true })).toBeNull()
    expect(screen.queryByText('Reject identity', { exact: true })).toBeNull()
    expect(identityReadyDecisionCandidateMocks.build).toHaveBeenCalledTimes(0)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
  })

  it.each([
    ['Keep pending human review', 'keep_pending_human_review'],
    ['Request more governance review', 'request_more_governance_review'],
  ])(
    'requires explicit confirmation for %s and creates one immutable page-local candidate',
    async (actionLabel, decisionType) => {
      const storageSetItemSpy = vi.spyOn(Storage.prototype, 'setItem')
      try {
        await renderIdentityReadyDecisionCandidateSurface()

        await chooseAntDesignOption(
          'Identity-ready human-review decision candidate action',
          actionLabel,
        )
        expect(identityReadyDecisionCandidateMocks.build).toHaveBeenCalledTimes(0)
        expect(
          screen.queryByText(
            'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
            { exact: true },
          ),
        ).toBeNull()

        const confirmButton = screen.getByRole('button', {
          name: 'Confirm local decision candidate',
        })
        expect(confirmButton.disabled).toBe(false)
        fireEvent.click(confirmButton)

        expect(identityReadyDecisionCandidateMocks.build).toHaveBeenCalledTimes(1)
        expect(identityReadyDecisionCandidateMocks.build).toHaveBeenCalledWith(
          IDENTITY_READY_V02_PROJECTION.review_subject_identity,
          decisionType,
        )
        expect(
          screen.getByText(
            'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
            { exact: true },
          ),
        ).toBeTruthy()
        const decisionTypeRow = screen.getByText('decision_type', { exact: true }).closest('tr')
        expect(within(decisionTypeRow).getByText(decisionType, { exact: true })).toBeTruthy()
        expect(
          screen.getAllByText(IDENTITY_READY_V02_BINDING_SAFE_HASH, { exact: true }),
        ).toHaveLength(2)
        expect(screen.getByText('candidate_only = true', { exact: true })).toBeTruthy()
        expect(screen.getByText('persisted = false', { exact: true })).toBeTruthy()
        expect(screen.getByText('trust_upgraded = false', { exact: true })).toBeTruthy()
        expect(screen.getByText('production_object = false', { exact: true })).toBeTruthy()
        expect(confirmButton.disabled).toBe(true)
        fireEvent.click(confirmButton)
        expect(identityReadyDecisionCandidateMocks.build).toHaveBeenCalledTimes(1)
        expect(
          screen.getAllByText(
            'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
            { exact: true },
          ),
        ).toHaveLength(1)
        expect(storageSetItemSpy).toHaveBeenCalledTimes(0)
        expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
      } finally {
        storageSetItemSpy.mockRestore()
      }
    },
  )

  it('keeps persistence separate, then performs exactly one explicit auditable-decision POST', async () => {
    const localSetItemSpy = vi.spyOn(Storage.prototype, 'setItem')
    apiMocks.apiClientPost.mockResolvedValue(createIdentityReadyDecisionBindingResponse())
    try {
      await renderIdentityReadyDecisionCandidateSurface()
      await chooseAntDesignOption(
        'Identity-ready human-review decision candidate action',
        'Keep pending human review',
      )
      fireEvent.click(screen.getByRole('button', { name: 'Confirm local decision candidate' }))

      const persistButton = screen.getByRole('button', {
        name: 'Record auditable nonproduction decision',
      })
      expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
      expect(persistButton.disabled).toBe(false)

      fireEvent.click(persistButton)
      fireEvent.click(persistButton)

      await waitFor(() => expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1))
      const [endpoint, payload] = apiMocks.apiClientPost.mock.calls[0]
      expect(endpoint).toBe(
        '/api/v1/internal/alpha/governed-review-decisions/identity-ready/v0.1/decisions',
      )
      expect(payload.request_schema).toBe(
        'sentigraph_internal_alpha_identity_ready_governed_review_decision_binding_request_v0_1',
      )
      expect(payload.request_version).toBe('0.1')
      expect(payload.candidate).toEqual(
        expect.objectContaining({
          schema: 'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
          sample_handle: CURRENT_HANDLE,
          review_subject_binding_safe_hash: IDENTITY_READY_V02_BINDING_SAFE_HASH,
          decision_type: 'keep_pending_human_review',
          candidate_only: true,
          persisted: false,
        }),
      )
      expect(await screen.findByText(IDENTITY_READY_DECISION_ID, { exact: true })).toBeTruthy()
      expect(screen.getByText(IDENTITY_READY_AUDIT_REFERENCE, { exact: true })).toBeTruthy()
      expect(
        screen.getByText('recorded_append_only_nonproduction_identity_ready', { exact: true }),
      ).toBeTruthy()
      expect(screen.getAllByText('false', { exact: true }).length).toBeGreaterThanOrEqual(3)
      expect(localSetItemSpy).toHaveBeenCalledTimes(0)
    } finally {
      localSetItemSpy.mockRestore()
    }
  })

  it('fails closed on a malformed persistence response without retrying or mutating the candidate', async () => {
    apiMocks.apiClientPost.mockResolvedValue(
      createIdentityReadyDecisionBindingResponse('request_more_governance_review', {
        malformed: true,
      }),
    )
    await renderIdentityReadyDecisionCandidateSurface()
    await chooseAntDesignOption(
      'Identity-ready human-review decision candidate action',
      'Request more governance review',
    )
    fireEvent.click(screen.getByRole('button', { name: 'Confirm local decision candidate' }))
    fireEvent.click(
      screen.getByRole('button', { name: 'Record auditable nonproduction decision' }),
    )

    expect(
      await screen.findByText('Auditable decision request failed closed', { exact: true }),
    ).toBeTruthy()
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(1)
    expect(
      screen.getByText(
        'sentigraph_internal_alpha_identity_ready_review_decision_candidate_v0_1',
        { exact: true },
      ),
    ).toBeTruthy()
    expect(screen.queryByText(RAW_CONFIGURATION_MARKER, { exact: false })).toBeNull()
  })

  it('normalizes only the bounded identity-ready receipt subset', async () => {
    apiMocks.apiClientPost.mockResolvedValue(createIdentityReadyDecisionBindingResponse())
    const candidate = identityReadyDecisionCandidateMocks.build(
      IDENTITY_READY_V02_PROJECTION.review_subject_identity,
      'keep_pending_human_review',
    )

    const result = await postInternalAlphaIdentityReadyGovernedReviewDecision(candidate)

    expect(result).toEqual({
      request_status: 'created',
      decision_id: IDENTITY_READY_DECISION_ID,
      audit_receipt_reference: IDENTITY_READY_AUDIT_REFERENCE,
      decision_type: 'keep_pending_human_review',
      sample_handle: CURRENT_HANDLE,
      review_subject_binding_safe_hash: IDENTITY_READY_V02_BINDING_SAFE_HASH,
      decision_status: 'recorded_append_only_nonproduction_identity_ready',
      outcome: 'created_exactly_one_identity_ready_human_review_decision',
      decision_ledger_write_performed: true,
      human_review_required: true,
      no_automatic_trust_upgrade: true,
      production_object_enabled: false,
      analysis_triggered: false,
      report_triggered: false,
    })
  })
})

describe('InternalAlphaReviewConsole identity-ready durable decision audit readback', () => {
  const auditEndpoint =
    '/api/v1/internal/alpha/governed-review-decisions/identity-ready/v0.1/decisions/' +
    `${IDENTITY_READY_DECISION_ID}/audit-projection`

  function auditGetCalls() {
    return apiMocks.apiClientGet.mock.calls.filter(([url]) =>
      String(url).endsWith('/audit-projection'),
    )
  }

  it('performs zero audit GETs on mount and selection, then one GET on explicit action only', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.apiClientGet.mockImplementation((url) => {
      if (url === auditEndpoint) {
        return Promise.resolve(createIdentityReadyDecisionAuditResponse())
      }
      return Promise.resolve(createGovernedFormalStateResponse())
    })

    render(<InternalAlphaReviewConsole />)
    expect(auditGetCalls()).toHaveLength(0)
    await openIdentityReadyDurableDecisionAuditReadback()
    expect(auditGetCalls()).toHaveLength(0)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
    expect(
      apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection,
    ).toHaveBeenCalledTimes(0)

    const input = screen.getByRole('textbox', {
      name: 'Identity-ready durable decision audit identifier',
    })
    const readButton = screen.getByRole('button', {
      name: 'Read exact audit projection',
    })
    expect(readButton.disabled).toBe(true)
    fireEvent.change(input, { target: { value: IDENTITY_READY_DECISION_ID } })
    expect(readButton.disabled).toBe(false)

    fireEvent.click(readButton)
    fireEvent.click(readButton)

    await screen.findByText('Safe durable decision audit projection', { exact: true })
    expect(auditGetCalls()).toHaveLength(1)
    expect(auditGetCalls()[0][0]).toBe(auditEndpoint)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
    expect(screen.getByText(IDENTITY_READY_AUDIT_REFERENCE, { exact: true })).toBeTruthy()
    expect(screen.getByText('decision_audit_ready', { exact: true })).toBeTruthy()
    expect(screen.queryByText(RAW_CONFIGURATION_MARKER, { exact: false })).toBeNull()
  })

  it('accepts a validated identifier retained from the bounded persistence receipt without GET on copy', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.getInternalAlphaLocalExchangeIdentityReadyV02Projection.mockResolvedValue(
      IDENTITY_READY_V02_PROJECTION,
    )
    apiMocks.apiClientPost.mockResolvedValue(createIdentityReadyDecisionBindingResponse())

    render(<InternalAlphaReviewConsole />)
    await openIdentityReadyV02Review()
    await screen.findByText(IDENTITY_READY_V02_BINDING_SAFE_HASH, { exact: true })
    await chooseAntDesignOption(
      'Identity-ready human-review decision candidate action',
      'Keep pending human review',
    )
    fireEvent.click(screen.getByRole('button', { name: 'Confirm local decision candidate' }))
    fireEvent.click(
      screen.getByRole('button', { name: 'Record auditable nonproduction decision' }),
    )
    await screen.findByText(IDENTITY_READY_AUDIT_REFERENCE, { exact: true })

    await openIdentityReadyDurableDecisionAuditReadback()
    expect(auditGetCalls()).toHaveLength(0)
    fireEvent.click(
      screen.getByRole('button', { name: 'Use bounded receipt decision ID' }),
    )
    expect(
      screen.getByRole('textbox', {
        name: 'Identity-ready durable decision audit identifier',
      }).value,
    ).toBe(IDENTITY_READY_DECISION_ID)
    expect(auditGetCalls()).toHaveLength(0)
  })

  it('normalizes only the exact safe success and bounded error field sets', () => {
    const success = createIdentityReadyDecisionAuditResponse()
    expect(
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection(
        success.data,
        success.status,
        IDENTITY_READY_DECISION_ID,
      ),
    ).toEqual(success.data)

    const bounded404 = createIdentityReadyDecisionAuditResponse({ status: 404 })
    expect(
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection(
        bounded404.data,
        bounded404.status,
        IDENTITY_READY_DECISION_ID,
      ),
    ).toEqual(bounded404.data)

    const extra = createIdentityReadyDecisionAuditResponse({
      extraFields: { decision_canonical_hash: RAW_CONFIGURATION_MARKER },
    })
    expect(() =>
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection(
        extra.data,
        extra.status,
        IDENTITY_READY_DECISION_ID,
      ),
    ).toThrow(
      'frontend_identity_ready_governed_review_decision_audit_projection_contract_mismatch',
    )
  })

  it('rejects an invalid identifier before any API GET', async () => {
    await expect(
      getInternalAlphaIdentityReadyGovernedReviewDecisionAuditProjection('not-an-id'),
    ).rejects.toThrow(
      'frontend_identity_ready_governed_review_decision_audit_projection_contract_mismatch',
    )
    expect(apiMocks.apiClientGet).toHaveBeenCalledTimes(0)
  })
})

describe('InternalAlphaReviewConsole bounded decision audit history', () => {
  const historyEndpoint =
    '/api/v1/internal/alpha/governed-review-decisions/identity-ready/v0.1/decisions/audit-projections'

  function historyGetCalls() {
    return apiMocks.apiClientGet.mock.calls.filter(([url]) => url === historyEndpoint)
  }

  function pointAuditGetCalls() {
    return apiMocks.apiClientGet.mock.calls.filter(([url]) =>
      String(url).endsWith('/audit-projection'),
    )
  }

  it('loads at most twenty ordered safe rows only after one explicit action', async () => {
    const pending = deferred()
    const secondDecisionId = 'irghrd-fedcba9876543210fedcba9876543210'
    const orderedRows = [
      createIdentityReadyDecisionAuditHistoryRow({
        decisionId: secondDecisionId,
        recordedAt: '2026-08-28T00:00:00Z',
        decisionType: 'request_more_governance_review',
      }),
      createIdentityReadyDecisionAuditHistoryRow(),
    ]
    const canonicalSafeHistoryFields = [
      'decision_id',
      'audit_receipt_reference',
      'sample_handle',
      'decision_type',
      'decision_status',
      'recorded_at',
      'human_review_required',
      'no_automatic_trust_upgrade',
      'production_object_enabled',
      'review_queue_runtime_enabled',
      'evidence_layer_write_performed',
      'provider_or_b05_called',
      'analysis_triggered',
      'report_triggered',
    ]
    expect(Object.keys(orderedRows[0])).toEqual(canonicalSafeHistoryFields)
    expect(Object.keys(orderedRows[1])).toEqual(canonicalSafeHistoryFields)
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.apiClientGet.mockImplementation((url) => {
      if (url === historyEndpoint) return pending.promise
      return Promise.resolve(createGovernedFormalStateResponse())
    })

    render(<InternalAlphaReviewConsole />)
    expect(historyGetCalls()).toHaveLength(0)
    await openIdentityReadyDurableDecisionAuditReadback()
    expect(historyGetCalls()).toHaveLength(0)
    expect(screen.getByText('history_state = not_loaded', { exact: true })).toBeTruthy()

    const loadButton = screen.getByRole('button', {
      name: 'Load recent auditable decisions',
    })
    fireEvent.click(loadButton)
    fireEvent.click(loadButton)
    expect(historyGetCalls()).toHaveLength(1)
    expect(historyGetCalls()[0][1]).toEqual({ params: { limit: 20 } })

    await act(async () => {
      pending.resolve(
        createIdentityReadyDecisionAuditHistoryResponse({ decisions: orderedRows }),
      )
      await pending.promise
    })
    await screen.findByText('history_state = bounded_success', { exact: true })
    const historyList = screen.getByLabelText('Recent auditable decision history')
    const renderedText = historyList.textContent
    expect(renderedText.indexOf(secondDecisionId)).toBeLessThan(
      renderedText.indexOf(IDENTITY_READY_DECISION_ID),
    )
    canonicalSafeHistoryFields.forEach((field) => {
      expect(within(historyList).getAllByText(field, { exact: true })).toHaveLength(2)
    })
    expect(renderedText).toMatch(/review_queue_runtime_enabled\s*false/)
    expect(renderedText).toMatch(/evidence_layer_write_performed\s*false/)
    expect(pointAuditGetCalls()).toHaveLength(0)
    expect(apiMocks.apiClientPost).toHaveBeenCalledTimes(0)
    expect(renderedText).not.toContain('decision_canonical_hash')
    expect(renderedText).not.toContain('review_subject_binding_safe_hash')
  })

  it('renders a bounded empty state', async () => {
    apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockResolvedValue(SYNTHETIC_CATALOG)
    apiMocks.apiClientGet.mockImplementation((url) => {
      if (url === historyEndpoint) {
        return Promise.resolve(
          createIdentityReadyDecisionAuditHistoryResponse({ decisions: [] }),
        )
      }
      return Promise.resolve(createGovernedFormalStateResponse())
    })
    render(<InternalAlphaReviewConsole />)
    await openIdentityReadyDurableDecisionAuditReadback()
    fireEvent.click(
      screen.getByRole('button', { name: 'Load recent auditable decisions' }),
    )
    await screen.findByText('No recent auditable decisions', { exact: true })
    expect(historyGetCalls()).toHaveLength(1)
    expect(pointAuditGetCalls()).toHaveLength(0)
  })

  it('rejects unsafe extra top-level and row fields and invalid limits before GET', async () => {
    const safe = createIdentityReadyDecisionAuditHistoryResponse()
    expect(
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(
        safe.data,
        safe.status,
        20,
      ),
    ).toEqual(safe.data)

    const extraTop = createIdentityReadyDecisionAuditHistoryResponse({
      extraFields: { decision_canonical_hash: RAW_CONFIGURATION_MARKER },
    })
    expect(() =>
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(
        extraTop.data,
        extraTop.status,
        20,
      ),
    ).toThrow(
      'frontend_identity_ready_governed_review_decision_audit_history_contract_mismatch',
    )

    const extraRow = createIdentityReadyDecisionAuditHistoryResponse({
      decisions: [
        createIdentityReadyDecisionAuditHistoryRow({
          extraFields: { review_subject_binding_safe_hash: RAW_CONFIGURATION_MARKER },
        }),
      ],
    })
    expect(() =>
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(
        extraRow.data,
        extraRow.status,
        20,
      ),
    ).toThrow(
      'frontend_identity_ready_governed_review_decision_audit_history_contract_mismatch',
    )

    const twentyRows = Array.from({ length: 20 }, (_value, index) =>
      createIdentityReadyDecisionAuditHistoryRow({
        decisionId: `irghrd-${index.toString(16).padStart(32, '0')}`,
      }),
    )
    const boundedTwenty = createIdentityReadyDecisionAuditHistoryResponse({
      decisions: twentyRows,
    })
    expect(
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(
        boundedTwenty.data,
        boundedTwenty.status,
        20,
      ).decisions,
    ).toHaveLength(20)
    const overLimit = createIdentityReadyDecisionAuditHistoryResponse({
      decisions: [...twentyRows, createIdentityReadyDecisionAuditHistoryRow()],
    })
    expect(() =>
      normalizeInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(
        overLimit.data,
        overLimit.status,
        20,
      ),
    ).toThrow(
      'frontend_identity_ready_governed_review_decision_audit_history_contract_mismatch',
    )

    await expect(
      getInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(0),
    ).rejects.toThrow(
      'frontend_identity_ready_governed_review_decision_audit_history_contract_mismatch',
    )
    await expect(
      getInternalAlphaIdentityReadyGovernedReviewDecisionAuditHistory(21),
    ).rejects.toThrow(
      'frontend_identity_ready_governed_review_decision_audit_history_contract_mismatch',
    )
    expect(historyGetCalls()).toHaveLength(0)
  })
})
