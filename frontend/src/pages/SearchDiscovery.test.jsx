// @vitest-environment jsdom
import React from 'react'
import { act, cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  attachSearchDiscoveryCandidates: vi.fn(),
  attachYouTubeOfficialApiReviewedPublicDiscussion: vi.fn(),
  createAnalysisCase: vi.fn(),
  getAnalysisCase: vi.fn(),
  getExternalCollectorStatus: vi.fn(),
  getExternalCollectorDiscovery: vi.fn(),
  listExternalCollectorPackages: vi.fn(),
  getExternalCollectorPackage: vi.fn(),
  validateExternalCollectorPackage: vi.fn(),
  getMockSearchDiscoveryCandidates: vi.fn(),
  getSearchDiscoveryProviders: vi.fn(),
  getYouTubeOfficialApiLiveCandidates: vi.fn(),
  getYouTubeOfficialApiLivePublicDiscussion: vi.fn(),
  getYouTubeOfficialApiMockCandidates: vi.fn(),
}))

const browserNetworkPrimitiveNames = ['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource']
const browserNetworkAttempts = Object.fromEntries(
  browserNetworkPrimitiveNames.map((name) => [name, 0]),
)

function installFailClosedBrowserNetworkSentinels() {
  for (const name of browserNetworkPrimitiveNames) {
    browserNetworkAttempts[name] = 0
    if (!(name in globalThis)) continue

    vi.stubGlobal(name, function failClosedBrowserNetworkPrimitive() {
      browserNetworkAttempts[name] += 1
      throw new Error(`Unexpected browser network primitive: ${name}`)
    })
  }
}

function expectNoBrowserNetworkAttempts() {
  expect(browserNetworkAttempts).toEqual({
    fetch: 0,
    XMLHttpRequest: 0,
    WebSocket: 0,
    EventSource: 0,
  })
}

vi.mock('../api/sentigraphApi.js', async (importOriginal) => {
  const actual = await importOriginal()
  return {
    ...actual,
    attachSearchDiscoveryCandidates: apiMocks.attachSearchDiscoveryCandidates,
    attachYouTubeOfficialApiReviewedPublicDiscussion: apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion,
    getAnalysisCase: apiMocks.getAnalysisCase,
    getExternalCollectorStatus: apiMocks.getExternalCollectorStatus,
    getExternalCollectorDiscovery: apiMocks.getExternalCollectorDiscovery,
    listExternalCollectorPackages: apiMocks.listExternalCollectorPackages,
    getExternalCollectorPackage: apiMocks.getExternalCollectorPackage,
    validateExternalCollectorPackage: apiMocks.validateExternalCollectorPackage,
    getMockSearchDiscoveryCandidates: apiMocks.getMockSearchDiscoveryCandidates,
    getSearchDiscoveryProviders: apiMocks.getSearchDiscoveryProviders,
    getYouTubeOfficialApiLiveCandidates: apiMocks.getYouTubeOfficialApiLiveCandidates,
    getYouTubeOfficialApiLivePublicDiscussion: apiMocks.getYouTubeOfficialApiLivePublicDiscussion,
    getYouTubeOfficialApiMockCandidates: apiMocks.getYouTubeOfficialApiMockCandidates,
  }
})

import { SearchDiscovery } from './SearchDiscovery.jsx'

const OFFLINE_PROVIDER = {
  provider_id: 'youtube_official_api',
  provider_type: 'youtube_official_api',
  display_name: 'YouTube Official API — offline mocked response (Phase 1)',
  status: 'mock_only',
  live_fetch_enabled: false,
  requires_api_key: false,
  requires_network: false,
  safety_notes: [
    'Offline mocked official response only',
    'No live YouTube API call',
    'Human review required before attach',
  ],
}

const OFFLINE_BATCH = {
  query: 'Synthetic launch',
  generated_at: '2026-08-22T00:00:00Z',
  candidate_count: 1,
  candidates: [
    {
      candidate_id: 'youtube_official_api_synthetic_001',
      query: 'Synthetic launch',
      provider: 'youtube_official_api',
      platform_hint: 'youtube',
      title: 'Synthetic launch official-shaped video candidate 1',
      snippet: 'Synthetic offline fixture metadata only.',
      url: 'https://www.youtube.com/watch?v=synthetic_001',
      published_at: '2026-08-22T00:00:00Z',
      source_name: 'Synthetic YouTube Official API Fixture',
      content_type_hint: 'video',
      confidence: 0.61,
      acquisition_mode: 'search_discovery',
      status: 'pending_review',
      safety_notes: ['Offline mocked official response only', 'URL was not fetched'],
    },
  ],
  provider_statuses: [OFFLINE_PROVIDER],
  safe_mode: {
    offline_mocked_official_response: true,
    mock_candidates_only: true,
    real_search_api_calls: false,
    url_fetching: false,
  },
}

const LIVE_PROVIDER_LABEL = 'YouTube Official API — internal live metadata search'

const LIVE_PROVIDER = {
  provider_id: 'youtube_official_api_live',
  provider_type: 'youtube_official_api',
  display_name: LIVE_PROVIDER_LABEL,
  status: 'guarded_internal',
  live_fetch_enabled: true,
  safety_notes: ['Credentials not checked; provider availability not established'],
}

const LIVE_BATCH = {
  query: 'Current launch',
  generated_at: '2026-08-23T00:00:00Z',
  candidate_count: 1,
  candidates: [
    {
      candidate_id: 'youtube_official_api_live_current_001',
      query: 'Current launch',
      provider: 'youtube_official_api_live',
      platform_hint: 'youtube',
      title: 'Current launch guarded live metadata candidate',
      snippet: 'Official API metadata preview only.',
      url: 'https://www.youtube.com/watch?v=current_001',
      published_at: '2026-08-23T00:00:00Z',
      source_name: 'YouTube Official API',
      content_type_hint: 'video',
      confidence: 0.72,
      acquisition_mode: 'search_discovery',
      status: 'pending_review',
      safety_notes: ['Official API metadata only', 'URL content not fetched'],
    },
  ],
  provider_statuses: [],
  safe_mode: {
    human_review_required: true,
    url_fetching: false,
    evidence_write: false,
  },
}

const ATTACH_RESULT = {
  case_id: 'case_phase1',
  status: 'attached',
  attached_candidate_count: 1,
  skipped_candidate_count: 0,
  rejected_candidate_count: 0,
  attached_evidence_items: [
    {
      evidence_id: 'evidence_phase1',
      title: 'Synthetic launch official-shaped video candidate 1',
      body_text: 'Synthetic offline fixture metadata only.',
      acquisition_mode: 'search_discovery',
      provenance_type: 'search_discovery_candidate',
      verification_status: 'source_url_provided_unverified',
      review_status: 'review_needed',
    },
  ],
  safe_mode: { real_search_api_calls: false },
}

function selectFirstComboboxOption(label) {
  const combobox = screen.getAllByRole('combobox')[0]
  fireEvent.mouseDown(combobox)
  return screen.findAllByText(label, { exact: true }).then((options) => {
    expect(options).toHaveLength(1)
    fireEvent.click(options[0])
  })
}

function deferred() {
  let resolve
  let reject
  const promise = new Promise((resolvePromise, rejectPromise) => {
    resolve = resolvePromise
    reject = rejectPromise
  })
  return { promise, resolve, reject }
}

beforeEach(() => {
  installFailClosedBrowserNetworkSentinels()
  Object.values(apiMocks).forEach((mock) => mock.mockReset())
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([OFFLINE_PROVIDER, LIVE_PROVIDER])
  apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: false, exists: false })
  apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue(LIVE_BATCH)
  apiMocks.getYouTubeOfficialApiMockCandidates.mockResolvedValue(OFFLINE_BATCH)
  apiMocks.attachSearchDiscoveryCandidates.mockResolvedValue(ATTACH_RESULT)
  apiMocks.getAnalysisCase.mockResolvedValue({ case_id: 'case_phase1', title: 'Phase-1 case' })

  window.matchMedia = vi.fn().mockImplementation((query) => ({
    matches: false,
    media: query,
    onchange: null,
    addListener: vi.fn(),
    removeListener: vi.fn(),
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    dispatchEvent: vi.fn(() => false),
  }))
  globalThis.ResizeObserver = class {
    observe() {}
    unobserve() {}
    disconnect() {}
  }
  HTMLElement.prototype.scrollIntoView = vi.fn()
})

afterEach(() => {
  try {
    expectNoBrowserNetworkAttempts()
  } finally {
    cleanup()
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  }
})

describe('SearchDiscovery offline YouTube official API Phase 1', () => {
  it('exposes the exact offline helper route without using other browser network primitives', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    expect(typeof actualApi.getYouTubeOfficialApiMockCandidates).toBe('function')

    const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get')
      .mockResolvedValue({ data: OFFLINE_BATCH })
    const result = await actualApi.getYouTubeOfficialApiMockCandidates('Synthetic launch', 3)

    expect(getSpy).toHaveBeenCalledTimes(1)
    expect(getSpy).toHaveBeenCalledWith(
      '/api/v1/search-discovery/youtube-official-api/mock-candidates',
      { params: { query: 'Synthetic launch', max_candidates: 3 } },
    )
    expect(result.candidates[0].provider).toBe('youtube_official_api')
    expect(result.safe_mode.offline_mocked_official_response).toBe(true)
  })

  it('reuses review, attach, and analysis controls without automatic side effects', async () => {
    const onRunCase = vi.fn()
    const onCaseReady = vi.fn()
    const onRefreshCases = vi.fn().mockResolvedValue(undefined)
    render(
      <SearchDiscovery
        cases={[{ case_id: 'case_phase1', title: 'Phase-1 case' }]}
        currentCase={{ case_id: 'case_phase1', title: 'Phase-1 case' }}
        onCaseReady={onCaseReady}
        onRefreshCases={onRefreshCases}
        onRunCase={onRunCase}
      />,
    )

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledTimes(0)
    expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(onRunCase).toHaveBeenCalledTimes(0)

    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic launch' } })
    fireEvent.click(screen.getByRole('button', { name: /Generate mock candidates/ }))

    await waitFor(() => {
      expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledWith('Synthetic launch', 5)
    })
    expect(apiMocks.getMockSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(await screen.findByText(OFFLINE_BATCH.candidates[0].title, { exact: true })).toBeTruthy()

    fireEvent.click(screen.getByRole('button', { name: '忽略' }))
    expect(screen.getByText('rejected', { exact: true })).toBeTruthy()
    expect(screen.getByRole('button', { name: /Attach accepted to case/ }).disabled).toBe(true)

    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    fireEvent.click(screen.getByRole('button', { name: /Attach accepted to case/ }))

    await waitFor(() => expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(1))
    expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledWith(
      'case_phase1',
      expect.objectContaining({
        candidates: [expect.objectContaining({ provider: 'youtube_official_api', status: 'accepted' })],
      }),
    )
    expect(apiMocks.getAnalysisCase).toHaveBeenCalledWith('case_phase1')
    expect(onCaseReady).toHaveBeenCalledTimes(1)
    expect(onRefreshCases).toHaveBeenCalledTimes(1)
    expect(onRunCase).toHaveBeenCalledTimes(0)

    fireEvent.click(screen.getByRole('button', { name: 'Run analysis after attach' }))
    expect(onRunCase).toHaveBeenCalledWith('case_phase1', 'analysis')

    for (const forbiddenControl of [/api key/i, /credential/i, /live provider/i, /auto.attach/i, /auto.analysis/i]) {
      expect(screen.queryByRole('textbox', { name: forbiddenControl })).toBeNull()
      expect(screen.queryByRole('button', { name: forbiddenControl })).toBeNull()
      expect(screen.queryByRole('switch', { name: forbiddenControl })).toBeNull()
    }
  })
})

describe('SearchDiscovery intentional guarded internal official API metadata', () => {
  it('uses the exact guarded live helper route and existing batch normalizer', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    expect(typeof actualApi.getYouTubeOfficialApiLiveCandidates).toBe('function')

    const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get')
      .mockResolvedValue({ data: LIVE_BATCH })
    const result = await actualApi.getYouTubeOfficialApiLiveCandidates('Current launch', 1)

    expect(getSpy).toHaveBeenCalledTimes(1)
    expect(getSpy).toHaveBeenCalledWith(
      '/api/v1/search-discovery/youtube-official-api/live-candidates',
      { params: { query: 'Current launch', max_candidates: 1 } },
    )
    expect(result.candidates[0]).toEqual(expect.objectContaining({
      provider: 'youtube_official_api_live',
      title: LIVE_BATCH.candidates[0].title,
    }))
    expect(result.safe_mode).toEqual(expect.objectContaining({
      human_review_required: true,
      url_fetching: false,
      evidence_write: false,
    }))
  })

  it('keeps the guarded live provider absent and unreachable by default', async () => {
    render(<SearchDiscovery />)

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    const providerCombobox = screen.getAllByRole('combobox')[0]
    fireEvent.mouseDown(providerCombobox)
    expect(screen.queryByText(LIVE_PROVIDER_LABEL, { exact: true })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(0)
  })

  it('exposes one guarded preview option while keeping a generated live batch local-only', async () => {
    const onRunCase = vi.fn()
    render(
      <SearchDiscovery
        cases={[{ case_id: 'case_phase1', title: 'Phase-1 case' }]}
        currentCase={{ case_id: 'case_phase1', title: 'Phase-1 case' }}
        onRunCase={onRunCase}
        liveRouteFrontendEnabled
      />,
    )

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))

    await waitFor(() => {
      expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledWith('Current launch', 5)
    })
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledTimes(0)
    expect(apiMocks.getMockSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeTruthy()

    for (const text of [
      'Internal real YouTube Official API metadata search',
      'Official API metadata only',
      'URL content not fetched',
      'Human review required',
      'Attachment disabled in this phase',
      'Backend route remains independently gated',
    ]) {
      expect(screen.getAllByText(text, { exact: true }).length).toBeGreaterThanOrEqual(1)
    }

    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    const attachButton = screen.getByRole('button', { name: /Attach accepted to case/ })
    expect(attachButton.disabled).toBe(true)
    fireEvent.click(attachButton)
    expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(onRunCase).toHaveBeenCalledTimes(0)

    for (const forbiddenControl of [/api key/i, /credential/i, /token/i, /cookie/i]) {
      expect(screen.queryByRole('textbox', { name: forbiddenControl })).toBeNull()
      expect(screen.queryByRole('button', { name: forbiddenControl })).toBeNull()
      expect(screen.queryByRole('switch', { name: forbiddenControl })).toBeNull()
    }
  })

  it('requires a fresh offline generation before attach resumes after a live batch', async () => {
    render(
      <SearchDiscovery
        cases={[{ case_id: 'case_phase1', title: 'Phase-1 case' }]}
        currentCase={{ case_id: 'case_phase1', title: 'Phase-1 case' }}
        liveRouteFrontendEnabled
      />,
    )

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))

    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    expect(screen.getByRole('button', { name: /Attach accepted to case/ }).disabled).toBe(true)

    fireEvent.click(screen.getByRole('button', { name: /Generate mock candidates/ }))
    await screen.findByText(OFFLINE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.getByRole('button', { name: /Attach accepted to case/ }).disabled).toBe(false)
    fireEvent.click(screen.getByRole('button', { name: /Attach accepted to case/ }))

    await waitFor(() => expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(1))
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getMockSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
  })
})

const COLLECTOR_LABEL = 'External Collector Handoff — already-produced local packages'
const COLLECTOR_FLAGS = {
  stored_validation_not_fresh: true,
  human_review_required: true,
  collector_job_run: false,
  package_validation_performed: false,
  evidence_content_read: false,
  url_fetching: false,
  scraping: false,
  full_web_coverage: false,
  full_platform_coverage: false,
}
const COLLECTOR_BATCH = {
  query: 'Synthetic launch',
  result_count: 1,
  results: [{
    package_name: 'synthetic_package_001',
    case_id: 'synthetic_case_001',
    case_title: 'Synthetic collector package summary',
    sample_labels: ['synthetic sample'],
    package_role: 'controlled_public_sample',
    validation_status: 'warn',
    exported_at: '2026-09-30T00:00:00Z',
    evidence_count: 3,
    source_count: 2,
    comment_count: 1,
    root_count: 1,
    recommended_for_sentigraph_demo: false,
    sample_quality_label: 'synthetic quality',
    recommended_next_action: 'needs_manual_review',
    matched_fields: ['case_title'],
    provenance: 'external_collector_handoff',
    ...COLLECTOR_FLAGS,
  }],
  safe_mode: { ...COLLECTOR_FLAGS, local_only: true, metadata_only: true, evidence_write: false, analysis_run: false },
}

describe('RDS1 external collector handoff query lane', () => {
  async function renderCollector(props = {}) {
    apiMocks.getExternalCollectorStatus.mockResolvedValue({
      configured: true, exists: true, exports_dir: 'synthetic-private-path', index_warning: 'synthetic-private-note',
    })
    apiMocks.getExternalCollectorDiscovery.mockResolvedValue(COLLECTOR_BATCH)
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled {...props} />)
    await waitFor(() => expect(apiMocks.getExternalCollectorStatus).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(COLLECTOR_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic launch' } })
  }

  function expectNoCollectorSideEffects() {
    for (const name of [
      'getYouTubeOfficialApiLiveCandidates', 'getYouTubeOfficialApiMockCandidates',
      'getMockSearchDiscoveryCandidates', 'getYouTubeOfficialApiLivePublicDiscussion',
      'attachSearchDiscoveryCandidates', 'attachYouTubeOfficialApiReviewedPublicDiscussion',
      'listExternalCollectorPackages', 'getExternalCollectorPackage', 'validateExternalCollectorPackage',
    ]) expect(apiMocks[name]).not.toHaveBeenCalled()
  }

  it.each([
    { configured: false, exists: false },
    { configured: true, exists: false },
  ])('does not offer discovery for an unavailable collector bridge %j', async (status) => {
    apiMocks.getExternalCollectorStatus.mockResolvedValue(status)
    render(<SearchDiscovery />)
    await waitFor(() => expect(apiMocks.getExternalCollectorStatus).toHaveBeenCalledTimes(1))
    fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
    expect(screen.queryByText(COLLECTOR_LABEL, { exact: true })).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).not.toHaveBeenCalled()
    expectNoCollectorSideEffects()
  })

  it('fails closed on an availability error without displaying private status fields', async () => {
    apiMocks.getExternalCollectorStatus.mockRejectedValue(new Error('synthetic-private-path'))
    render(<SearchDiscovery />)
    await waitFor(() => expect(apiMocks.getExternalCollectorStatus).toHaveBeenCalledTimes(1))
    fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
    expect(screen.queryByText(COLLECTOR_LABEL, { exact: true })).toBeNull()
    expect(screen.queryByText(/synthetic-private-path/)).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).not.toHaveBeenCalled()
    expectNoCollectorSideEffects()
  })

  it('requires one explicit action and keeps package metadata separate from candidate controls', async () => {
    const onRunCase = vi.fn()
    await renderCollector({ onRunCase })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: '  Synthetic   launch  ' } })
    expect(apiMocks.getExternalCollectorDiscovery).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledWith('Synthetic launch', 5)
    expect(screen.getByText('Current external collector package results for query: Synthetic launch')).toBeTruthy()
    expect(screen.getAllByTestId('external-collector-package-result')).toHaveLength(1)
    expect(screen.getByText('provenance=external_collector_handoff')).toBeTruthy()
    expect(screen.getByText('Stored validation: warn')).toBeTruthy()
    expect(screen.getByText(/Stored validation is not fresh/)).toBeTruthy()
    expect(screen.queryByText(/synthetic-private-path|synthetic-private-note/)).toBeNull()
    expect(screen.queryByText('Candidate review list')).toBeNull()
    for (const name of [/Attach accepted to case/, /Run analysis/, /Load.*discussion/, '接受', '拒绝']) {
      expect(screen.queryByRole('button', { name })).toBeNull()
    }
    expectNoCollectorSideEffects()
    expect(onRunCase).not.toHaveBeenCalled()
  })

  it('returns a valid explicit zero-result state without a fallback or retry', async () => {
    await renderCollector()
    apiMocks.getExternalCollectorDiscovery.mockResolvedValue({ ...COLLECTOR_BATCH, results: [], result_count: 0 })
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText('No matching external collector packages for query: Synthetic launch')
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expect(screen.queryByTestId('external-collector-package-result')).toBeNull()
    expectNoCollectorSideEffects()
  })

  it('rejects a blank query before any helper call and clears a previous batch', async () => {
    await renderCollector()
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })
    apiMocks.getExternalCollectorDiscovery.mockClear()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: '  \t ' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText('Enter a non-blank query before searching external collector packages.')
    expect(apiMocks.getExternalCollectorDiscovery).not.toHaveBeenCalled()
    expect(screen.queryByTestId('external-collector-package-result')).toBeNull()
    expectNoCollectorSideEffects()
  })

  it.each([
    ['not_configured', 'The external collector bridge is not configured.'],
    ['configured_root_missing', 'The configured external collector root is unavailable.'],
    ['query_invalid', 'Use a valid query of at most 120 characters.'],
    ['query_required', 'Enter a non-blank query before searching external collector packages.'],
    ['internal_failure', 'Unable to search the local external collector package summaries.'],
    ['unknown', 'Unable to search the local external collector package summaries.'],
  ])('renders bounded %s errors without raw paths or retries', async (suffix, message) => {
    await renderCollector()
    apiMocks.getExternalCollectorDiscovery.mockRejectedValue({
      message: 'synthetic-private-path',
      response: { data: { detail: suffix === 'configured_root_missing'
        ? 'external_collector_configured_root_missing' : `external_collector_${suffix === 'not_configured' ? 'bridge_not_configured' : suffix}`,
      raw: 'synthetic-private-backend-error' } },
    })
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText(message)
    expect(screen.queryByText(/synthetic-private-path|synthetic-private-backend-error/)).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expectNoCollectorSideEffects()
  })

  it('handles framework query bounds as a safe invalid-query error', async () => {
    await renderCollector()
    apiMocks.getExternalCollectorDiscovery.mockRejectedValue({ response: { status: 422, data: { detail: ['synthetic-private-path'] } } })
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText('Use a valid query of at most 120 characters.')
    expect(screen.queryByText(/synthetic-private-path/)).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expectNoCollectorSideEffects()
  })

  it('historicalizes a batch when the query changes without issuing another request', async () => {
    await renderCollector()
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Another event' } })
    expect(screen.getByText('Historical external collector package results for query: Synthetic launch')).toBeTruthy()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expectNoCollectorSideEffects()
  })

  it('discards an in-flight collector response after its submitted context is invalidated', async () => {
    await renderCollector()
    let resolveSearch
    apiMocks.getExternalCollectorDiscovery.mockImplementation(() => new Promise((resolve) => { resolveSearch = resolve }))
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Another event' } })
    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    await act(async () => { resolveSearch(COLLECTOR_BATCH); await Promise.resolve() })
    expect(screen.queryByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expectNoCollectorSideEffects()
  })

  it('rejects a response for another query without rendering package results', async () => {
    await renderCollector()
    apiMocks.getExternalCollectorDiscovery.mockResolvedValue({ ...COLLECTOR_BATCH, query: 'Different event' })
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText('The returned collector packages do not match the submitted query. Run a new explicit search.')
    expect(screen.queryByTestId('external-collector-package-result')).toBeNull()
    expectNoCollectorSideEffects()
  })

  it.each([['official', LIVE_PROVIDER_LABEL], ['offline', OFFLINE_PROVIDER.display_name]])(
    'clears collector state when a new %s candidate batch starts', async (kind, label) => {
      await renderCollector()
      fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
      await screen.findByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })
      await selectFirstComboboxOption(label)
      const official = kind === 'official'
      if (official) fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
      fireEvent.click(screen.getByRole('button', { name: official ? /Search YouTube Official API metadata/ : /Generate mock candidates/ }))
      await screen.findByText((official ? LIVE_BATCH : OFFLINE_BATCH).candidates[0].title, { exact: true })
      expect(screen.queryByTestId('external-collector-discovery-panel')).toBeNull()
      expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
      expect(apiMocks.getExternalCollectorPackage).not.toHaveBeenCalled()
      expect(apiMocks.validateExternalCollectorPackage).not.toHaveBeenCalled()
      expect(apiMocks.attachSearchDiscoveryCandidates).not.toHaveBeenCalled()
    },
  )

  it('clears candidate state when a new collector search starts', async () => {
    await renderCollector()
    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    fireEvent.click(screen.getByRole('button', { name: /Generate mock candidates/ }))
    await screen.findByText(OFFLINE_BATCH.candidates[0].title, { exact: true })
    await selectFirstComboboxOption(COLLECTOR_LABEL)
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await screen.findByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })
    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    expect(screen.queryByText(OFFLINE_BATCH.candidates[0].title, { exact: true })).toBeNull()
    expect(screen.queryByRole('button', { name: '接受' })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expect(apiMocks.attachSearchDiscoveryCandidates).not.toHaveBeenCalled()
  })

  it('projects only safe package metadata through the exact discovery client route', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const raw = { ...COLLECTOR_BATCH, results: [{
      ...COLLECTOR_BATCH.results[0], package_path: 'C:\\synthetic\\private',
      index_notes: 'synthetic private note', coverage_warnings: ['synthetic private note'],
      case_title: 'api_key=synthetic_not_a_real_secret',
      sample_labels: ['synthetic sample', 'authorization: synthetic', 'https://synthetic.invalid'],
      evidence_count: 2000000000, source_count: -1,
      candidate_id: 'must_not_exist', url: 'https://synthetic.invalid', snippet: 'must_not_exist', confidence: 1,
    }] }
    const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get').mockResolvedValue({ data: raw })
    const result = await actualApi.getExternalCollectorDiscovery('Synthetic launch', 5)
    expect(getSpy).toHaveBeenCalledTimes(1)
    expect(getSpy).toHaveBeenCalledWith('/api/v1/external-collector/discovery', { params: { query: 'Synthetic launch', max_results: 5 } })
    expect(result.results[0].case_title).toBe('')
    expect(result.results[0].sample_labels).toEqual(['synthetic sample'])
    expect(result.results[0].evidence_count).toBe(1000000000)
    expect(result.results[0].source_count).toBe(0)
    for (const field of ['package_path', 'index_notes', 'coverage_warnings', 'candidate_id', 'url', 'snippet', 'confidence']) {
      expect(result.results[0]).not.toHaveProperty(field)
    }
    expect(result.safe_mode.evidence_write).toBe(false)
    expect(result.safe_mode.analysis_run).toBe(false)
  })

  it.each(['provenance', 'evidence_content_read', 'analysis_run', 'count', 'package_name', 'blank_query'])(
    'rejects a malformed or unsafe %s client response without retry', async (field) => {
      const actualApi = await vi.importActual('../api/sentigraphApi.js')
      const raw = { ...COLLECTOR_BATCH, safe_mode: { ...COLLECTOR_BATCH.safe_mode }, results: [{ ...COLLECTOR_BATCH.results[0] }] }
      if (field === 'provenance') raw.results[0].provenance = 'youtube_official_api'
      if (field === 'evidence_content_read') raw.results[0].evidence_content_read = true
      if (field === 'analysis_run') raw.safe_mode.analysis_run = true
      if (field === 'count') raw.result_count = 2
      if (field === 'package_name') raw.results[0].package_name = '../synthetic'
      if (field === 'blank_query') raw.query = '  '
      const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get').mockResolvedValue({ data: raw })
      await expect(actualApi.getExternalCollectorDiscovery('Synthetic launch', 5)).rejects.toThrow('external_collector_response_invalid')
      expect(getSpy).toHaveBeenCalledTimes(1)
    },
  )
})

describe('RDS1 intentional live search boundaries', () => {
  async function renderLive(props = {}) {
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled {...props} />)
    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  }

  function expectNoDownstreamActions() {
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.attachSearchDiscoveryCandidates).not.toHaveBeenCalled()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.getMockSearchDiscoveryCandidates).not.toHaveBeenCalled()
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).not.toHaveBeenCalled()
  }

  it('fails closed when the backend live descriptor is missing', async () => {
    apiMocks.getSearchDiscoveryProviders.mockResolvedValue([OFFLINE_PROVIDER])
    render(<SearchDiscovery liveRouteFrontendEnabled />)
    await screen.findByText('Live search unavailable: backend capability descriptor is absent.')
    fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
    expect(screen.queryByText(LIVE_PROVIDER_LABEL, { exact: true })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).not.toHaveBeenCalled()
  })

  it('shows the backend-disabled descriptor as an unavailable lane', async () => {
    apiMocks.getSearchDiscoveryProviders.mockResolvedValue([OFFLINE_PROVIDER, { ...LIVE_PROVIDER, live_fetch_enabled: false }])
    render(<SearchDiscovery liveRouteFrontendEnabled />)
    await screen.findByText('Backend live search route is disabled; the live lane is unavailable.')
    fireEvent.mouseDown(screen.getAllByRole('combobox')[0])
    const option = (await screen.findByText(LIVE_PROVIDER_LABEL, { exact: true })).closest('.ant-select-item-option')
    expect(option.className).toContain('ant-select-item-option-disabled')
    fireEvent.click(option)
    expect(screen.queryByRole('button', { name: /Search YouTube Official API metadata/ })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).not.toHaveBeenCalled()
  })

  it('normalizes a submitted query, requests five once, and never auto invokes downstream actions', async () => {
    const onRunCase = vi.fn()
    await renderLive({ onRunCase })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: '  Current   launch  ' } })
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).not.toHaveBeenCalled()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledWith('Current launch', 5)
    expect(screen.queryByText('Mock/static only', { exact: true })).toBeNull()
    expect(screen.getByText('Current real official-API metadata batch for query: Current launch')).toBeTruthy()
    expectNoDownstreamActions()
    expect(onRunCase).not.toHaveBeenCalled()
  })

  it('rejects a blank explicit query without substituting Tesla or retaining an old current batch', async () => {
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.getByRole('button', { name: /Load provider-backed public discussion/ })).toBeTruthy()
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockClear()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: '   \t ' } })
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText('Enter a non-blank query before searching YouTube Official API metadata.')
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).not.toHaveBeenCalled()
    expect(screen.queryByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeNull()
    expectNoDownstreamActions()
  })

  it('shows successful zero results for the submitted query without fallback or retry', async () => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue({ ...LIVE_BATCH, candidates: [], candidate_count: 0 })
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText('No official API metadata candidates returned for query: Current launch')
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expectNoDownstreamActions()
  })

  it.each([
    ['route_disabled', 'The backend live search route is disabled.'],
    ['credential_missing', 'The backend live search credential is missing.'],
    ['quota_error', 'The official API reported a quota error.'],
    ['auth_error', 'The official API reported an authentication or authorization failure.'],
    ['network_error', 'The official API request failed at the network boundary.'],
    ['parsing_error', 'The official API response could not be parsed.'],
    ['provider_error', 'The official API reported a provider failure.'],
    ['unexpected', 'Unable to complete the official API metadata search.'],
  ])('renders safe %s failures once without exposing raw responses or falling back', async (suffix, message) => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockRejectedValue({
      message: 'synthetic-sensitive-raw-message',
      response: { data: { detail: 'youtube_live_search_discovery_' + suffix, raw: 'synthetic-private-response' } },
    })
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(message)
    expect(screen.queryByText(/synthetic-sensitive-raw-message|synthetic-private-response/)).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expectNoDownstreamActions()
  })

  it('discards an in-flight live result after query and lane drift', async () => {
    let resolveSearch
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockImplementation(() => new Promise((resolve) => { resolveSearch = resolve }))
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Another event' } })
    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    await act(async () => { resolveSearch(LIVE_BATCH); await Promise.resolve() })
    expect(screen.queryByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeNull()
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    expect(screen.getByRole('button', { name: /Attach accepted to case/ }).disabled).toBe(true)
    expectNoDownstreamActions()
  })

  it('rejects a response for another query without authorizing any selection', async () => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue({ ...LIVE_BATCH, query: 'Different event' })
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText('The returned metadata batch does not match the submitted query. Run a new explicit search.')
    expect(screen.queryByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeNull()
    expectNoDownstreamActions()
  })
})

describe('RIE1R2 exact-one live candidate and monotonic search context', () => {
  async function renderLiveSearch() {
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled />)
    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  }

  const searchName = /Search YouTube Official API metadata/
  const loadName = /Load provider-backed public discussion/
  const secondCandidate = {
    ...LIVE_BATCH.candidates[0], candidate_id: 'youtube_official_api_live_current_002',
    title: 'Second guarded live metadata candidate', url: 'https://www.youtube.com/watch?v=current_002',
  }

  it('requires exactly one accepted candidate without rewriting the other user decisions', async () => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue({
      ...LIVE_BATCH, candidate_count: 2, candidates: [LIVE_BATCH.candidates[0], secondCandidate],
    })
    await renderLiveSearch()
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    await screen.findByText(secondCandidate.title, { exact: true })
    const firstRow = screen.getByText(LIVE_BATCH.candidates[0].title, { exact: true }).closest('tr')
    const secondRow = screen.getByText(secondCandidate.title, { exact: true }).closest('tr')
    expect(screen.queryByRole('button', { name: loadName })).toBeNull()
    fireEvent.click(within(firstRow).getByRole('button', { name: '接受' }))
    expect(screen.getByRole('button', { name: loadName })).toBeTruthy()
    fireEvent.click(within(secondRow).getByRole('button', { name: '接受' }))
    expect(within(firstRow).getByText('accepted', { exact: true })).toBeTruthy()
    expect(within(secondRow).getByText('accepted', { exact: true })).toBeTruthy()
    expect(screen.queryByRole('button', { name: loadName })).toBeNull()
    fireEvent.click(within(firstRow).getByRole('button', { name: '忽略' }))
    expect(screen.getByRole('button', { name: loadName })).toBeTruthy()
    expect(within(secondRow).getByText('accepted', { exact: true })).toBeTruthy()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })

  it.each([
    ['missing candidate id', { candidate_id: '' }],
    ['another candidate query', { query: 'Different event' }],
  ])('does not grant discussion authority to %s', async (_, override) => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue({
      ...LIVE_BATCH, candidates: [{ ...LIVE_BATCH.candidates[0], ...override }],
    })
    await renderLiveSearch()
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.queryByRole('button', { name: loadName })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
  })

  it.each(['success', 'error'])('fences old search %s and loading completion across A-B-A', async (outcome) => {
    const oldA = deferred()
    const oldB = deferred()
    const currentA = deferred()
    apiMocks.getYouTubeOfficialApiLiveCandidates
      .mockReturnValueOnce(oldA.promise).mockReturnValueOnce(oldB.promise).mockReturnValueOnce(currentA.promise)
    await renderLiveSearch()
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Other event' } })
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(3)
    await act(async () => {
      if (outcome === 'success') oldA.resolve(LIVE_BATCH)
      else oldA.reject({ response: { data: { detail: 'youtube_live_search_discovery_quota_error' } } })
      oldB.resolve({ ...LIVE_BATCH, query: 'Other event' })
      await Promise.resolve()
    })
    expect(screen.queryByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeNull()
    expect(screen.queryByText('The official API reported a quota error.', { exact: true })).toBeNull()
    expect(screen.getByRole('button', { name: searchName }).classList.contains('ant-btn-loading')).toBe(true)
    const fresh = { ...LIVE_BATCH, candidates: [{ ...LIVE_BATCH.candidates[0], title: 'New A request candidate' }] }
    await act(async () => { currentA.resolve(fresh); await Promise.resolve() })
    expect(screen.getByText('New A request candidate', { exact: true })).toBeTruthy()
    expect(screen.getByRole('button', { name: searchName }).classList.contains('ant-btn-loading')).toBe(false)
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.getByRole('button', { name: loadName })).toBeTruthy()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
  })

  it('cannot revive an accepted historical batch merely by returning to the same query', async () => {
    await renderLiveSearch()
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Other event' } })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
    expect(screen.getByText('Historical real official-API metadata batch for query: Current launch')).toBeTruthy()
    expect(screen.queryByRole('button', { name: loadName })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
  })

  it('does not let a stale collector error or completion change a new live search', async () => {
    apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: true, exists: true })
    const oldCollector = deferred()
    const currentLive = deferred()
    apiMocks.getExternalCollectorDiscovery.mockReturnValueOnce(oldCollector.promise)
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockReturnValueOnce(currentLive.promise)
    await renderLiveSearch()
    await selectFirstComboboxOption(COLLECTOR_LABEL)
    fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.click(screen.getByRole('button', { name: searchName }))
    await act(async () => {
      oldCollector.reject({ response: { data: { detail: 'external_collector_configured_root_missing' } } })
      await Promise.resolve()
    })
    expect(screen.queryByText('The configured external collector root is unavailable.', { exact: true })).toBeNull()
    expect(screen.getByRole('button', { name: searchName }).classList.contains('ant-btn-loading')).toBe(true)
    await act(async () => { currentLive.resolve(LIVE_BATCH); await Promise.resolve() })
    expect(screen.getByText(LIVE_BATCH.candidates[0].title, { exact: true })).toBeTruthy()
    expect(screen.queryByTestId('external-collector-package-result')).toBeNull()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(1)
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
  })

  it('keeps only the newest collector package search across A-B-A', async () => {
    apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: true, exists: true })
    const oldA = deferred()
    const oldB = deferred()
    const currentA = deferred()
    apiMocks.getExternalCollectorDiscovery
      .mockReturnValueOnce(oldA.promise).mockReturnValueOnce(oldB.promise).mockReturnValueOnce(currentA.promise)
    await renderLiveSearch()
    await selectFirstComboboxOption(COLLECTOR_LABEL)
    const searchPackages = () => fireEvent.click(screen.getByRole('button', { name: 'Search external collector handoff packages' }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic launch' } })
    searchPackages()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Other event' } })
    searchPackages()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Synthetic launch' } })
    searchPackages()
    const currentBatch = { ...COLLECTOR_BATCH, results: [{ ...COLLECTOR_BATCH.results[0], case_title: 'Newest collector package' }] }
    await act(async () => { currentA.resolve(currentBatch); await Promise.resolve() })
    await act(async () => {
      oldA.resolve(COLLECTOR_BATCH)
      oldB.resolve({ ...COLLECTOR_BATCH, query: 'Other event' })
      await Promise.resolve()
    })
    expect(screen.getByText('Newest collector package', { exact: true })).toBeTruthy()
    expect(screen.queryByText(COLLECTOR_BATCH.results[0].case_title, { exact: true })).toBeNull()
    expect(screen.getByText('Current external collector package results for query: Synthetic launch')).toBeTruthy()
    expect(apiMocks.getExternalCollectorDiscovery).toHaveBeenCalledTimes(3)
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.attachSearchDiscoveryCandidates).not.toHaveBeenCalled()
  })
})
