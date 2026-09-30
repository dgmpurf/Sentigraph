import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  attachSearchDiscoveryCandidates: vi.fn(),
  attachYouTubeOfficialApiReviewedPublicDiscussion: vi.fn(),
  getAnalysisCase: vi.fn(),
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

beforeEach(() => {
  installFailClosedBrowserNetworkSentinels()
  Object.values(apiMocks).forEach((mock) => mock.mockReset())
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([OFFLINE_PROVIDER, LIVE_PROVIDER])
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

  it('keeps an in-flight result bound to its submitted query and lane after input drift', async () => {
    let resolveSearch
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockImplementation(() => new Promise((resolve) => { resolveSearch = resolve }))
    await renderLive()
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Another event' } })
    await selectFirstComboboxOption(OFFLINE_PROVIDER.display_name)
    resolveSearch(LIVE_BATCH)
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.getByText('Historical real official-API metadata batch for query: Current launch')).toBeTruthy()
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
