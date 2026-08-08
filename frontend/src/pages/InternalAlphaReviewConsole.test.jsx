import React from 'react'
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
  waitFor,
} from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  apiClientPost: vi.fn(),
  getInternalAlphaReviewConsoleProjection: vi.fn(),
  getInternalAlphaLocalExchangeSampleCatalog: vi.fn(),
  getInternalAlphaLocalExchangeProjection: vi.fn(),
}))

vi.mock('../api/client.js', () => ({
  apiClient: {
    get: vi.fn(),
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
  }
})

import {
  INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID,
  INTERNAL_ALPHA_GOVERNED_REVIEW_DECISION_TYPES,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTION_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_CATALOG_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_FIELDS,
  normalizeInternalAlphaGovernedReviewDecisionPostResponse,
  normalizeInternalAlphaLocalExchangeProjection,
  normalizeInternalAlphaLocalExchangeSampleCatalog,
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

const SYNTHETIC_CATALOG = createSyntheticCatalog()
const CURRENT_PROJECTION = createSyntheticProjection({
  status: 'ready_for_human_review',
  marker: CURRENT_MARKER,
})
const HISTORICAL_PROJECTION = createSyntheticProjection({
  status: 'manual_review_required',
  marker: HISTORICAL_MARKER,
})

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
  apiMocks.apiClientPost.mockReset()
  apiMocks.getInternalAlphaReviewConsoleProjection.mockReset()
  apiMocks.getInternalAlphaLocalExchangeSampleCatalog.mockReset()
  apiMocks.getInternalAlphaLocalExchangeProjection.mockReset()
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
