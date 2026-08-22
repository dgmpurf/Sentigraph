import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  attachSearchDiscoveryCandidates: vi.fn(),
  getAnalysisCase: vi.fn(),
  getMockSearchDiscoveryCandidates: vi.fn(),
  getSearchDiscoveryProviders: vi.fn(),
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
    getAnalysisCase: apiMocks.getAnalysisCase,
    getMockSearchDiscoveryCandidates: apiMocks.getMockSearchDiscoveryCandidates,
    getSearchDiscoveryProviders: apiMocks.getSearchDiscoveryProviders,
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
  return screen.findByText(label, { exact: true }).then((option) => {
    fireEvent.click(option)
  })
}

beforeEach(() => {
  installFailClosedBrowserNetworkSentinels()
  Object.values(apiMocks).forEach((mock) => mock.mockReset())
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([OFFLINE_PROVIDER])
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
