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
  getInternalAlphaReviewConsoleProjection: vi.fn(),
  getInternalAlphaLocalExchangeSampleCatalog: vi.fn(),
  getInternalAlphaLocalExchangeProjection: vi.fn(),
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
  INTERNAL_ALPHA_LOCAL_EXCHANGE_PROJECTION_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_CATALOG_FIELDS,
  INTERNAL_ALPHA_LOCAL_EXCHANGE_SAMPLE_FIELDS,
  normalizeInternalAlphaLocalExchangeProjection,
  normalizeInternalAlphaLocalExchangeSampleCatalog,
} from '../api/sentigraphApi.js'
import { InternalAlphaReviewConsole } from './InternalAlphaReviewConsole.jsx'

const CURRENT_HANDLE = 'helldivers2-psn-demo'
const HISTORICAL_HANDLE = 'helldivers2-psn-demo-20260614'
const CURRENT_LABEL = 'Current curated sample'
const HISTORICAL_LABEL = 'Accepted historical sample'
const CURRENT_MARKER = 'synthetic_current_visible_marker'
const HISTORICAL_MARKER = 'synthetic_historical_visible_marker'
const RAW_ERROR_MARKER = 'synthetic_raw_exception_message'

const SENSITIVE_MARKERS = Object.freeze([
  'synthetic_private_path_marker',
  'synthetic_configuration_value_marker',
  'synthetic_receipt_marker',
  'synthetic_provider_result_content_marker',
  'synthetic_raw_metadata_marker',
  'provider_result_helldivers2-psn-demo_20260720_123627.json',
  RAW_ERROR_MARKER,
])

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
