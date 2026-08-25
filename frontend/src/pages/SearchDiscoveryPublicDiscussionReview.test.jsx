import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  attachSearchDiscoveryCandidates: vi.fn(),
  getAnalysisCase: vi.fn(),
  getMockSearchDiscoveryCandidates: vi.fn(),
  getSearchDiscoveryProviders: vi.fn(),
  getYouTubeOfficialApiLiveCandidates: vi.fn(),
  getYouTubeOfficialApiLivePublicDiscussion: vi.fn(),
  getYouTubeOfficialApiMockCandidates: vi.fn(),
}))

const browserNetworkAttempts = {
  fetch: 0,
  XMLHttpRequest: 0,
  WebSocket: 0,
  EventSource: 0,
}

function installFailClosedBrowserNetworkSentinels() {
  for (const name of Object.keys(browserNetworkAttempts)) {
    browserNetworkAttempts[name] = 0
    if (!(name in globalThis)) continue
    vi.stubGlobal(name, function failClosedBrowserNetworkPrimitive() {
      browserNetworkAttempts[name] += 1
      throw new Error(`Unexpected browser network primitive: ${name}`)
    })
  }
}

vi.mock('../api/sentigraphApi.js', () => apiMocks)

import { SearchDiscovery } from './SearchDiscovery.jsx'
import { PUBLIC_DISCUSSION_REVIEW_FIXTURE } from '../fixtures/publicDiscussionReviewFixture.js'

const LIVE_PROVIDER_LABEL = 'YouTube Official API — guarded live preview'

const LIVE_BATCH = {
  query: 'Current launch',
  generated_at: '2026-08-25T00:00:00Z',
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
      published_at: '2026-08-25T00:00:00Z',
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

const LIVE_DISCUSSION_BATCH = {
  video_id: 'current_001',
  generated_at: '2026-08-25T00:01:00Z',
  item_count: 2,
  items: [
    {
      discussion_id: 'youtube_official_api_current_001_comment_001',
      provider: 'youtube_official_api',
      platform_hint: 'youtube',
      video_id: 'current_001',
      comment_id: 'comment_001',
      body_text: 'Provider-backed comment one requires human review.',
      published_at: '2026-08-25T00:01:00Z',
      like_count: 7,
      reply_count: 2,
      source_url: 'https://www.youtube.com/watch?v=current_001&lc=comment_001',
      content_type_hint: 'comment',
      acquisition_mode: 'search_discovery_public_discussion',
      status: 'pending_review',
      safety_notes: ['Author identity omitted', 'Reply content not acquired'],
    },
    {
      discussion_id: 'youtube_official_api_current_001_comment_002',
      provider: 'youtube_official_api',
      platform_hint: 'youtube',
      video_id: 'current_001',
      comment_id: 'comment_002',
      body_text: 'Provider-backed comment two remains pending review.',
      published_at: '2026-08-25T00:02:00Z',
      like_count: 3,
      reply_count: 0,
      source_url: 'https://www.youtube.com/watch?v=current_001&lc=comment_002',
      content_type_hint: 'comment',
      acquisition_mode: 'search_discovery_public_discussion',
      status: 'pending_review',
      safety_notes: ['Author identity omitted', 'Reply content not acquired'],
    },
  ],
  safe_mode: {
    public_discussion_text: true,
    top_level_comments_only: true,
    reply_content_acquired: false,
    pagination: false,
    url_fetching: false,
    scraping: false,
    cookies_used: false,
    secrets_exposed: false,
    evidence_write: false,
    analysis_run: false,
    human_review_required: true,
  },
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
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([])
  apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue(LIVE_BATCH)
  apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockResolvedValue(LIVE_DISCUSSION_BATCH)

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
    expect(browserNetworkAttempts).toEqual({
      fetch: 0,
      XMLHttpRequest: 0,
      WebSocket: 0,
      EventSource: 0,
    })
  } finally {
    cleanup()
    vi.unstubAllGlobals()
    vi.restoreAllMocks()
  }
})

describe('SearchDiscovery offline public-discussion review lane Phase 2E3B', () => {
  it('keeps the review lane absent under the default-disabled gate', async () => {
    render(<SearchDiscovery />)

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    expect(
      screen.queryByRole('heading', { name: 'Public Discussion Review / 公开讨论复核' }),
    ).toBeNull()
    expect(
      screen.queryByRole('button', {
        name: 'Load synthetic public discussion fixture / 加载模拟讨论',
      }),
    ).toBeNull()
  })

  it('loads exactly three synthetic items only after the explicit local action', async () => {
    render(<SearchDiscovery publicDiscussionReviewFrontendEnabled />)

    const heading = screen.getByRole('heading', {
      name: 'Public Discussion Review / 公开讨论复核',
    })
    expect(heading).toBeTruthy()
    const panel = screen.getByTestId('public-discussion-review-panel')
    const loadButton = within(panel).getByRole('button', {
      name: 'Load synthetic public discussion fixture / 加载模拟讨论',
    })
    expect(loadButton).toBeTruthy()
    expect(screen.queryByText(PUBLIC_DISCUSSION_REVIEW_FIXTURE.items[0].body_text)).toBeNull()

    fireEvent.click(loadButton)

    expect(within(panel).getAllByTestId('public-discussion-review-item')).toHaveLength(3)
    for (const item of PUBLIC_DISCUSSION_REVIEW_FIXTURE.items) {
      expect(within(panel).getByText(item.body_text, { exact: true })).toBeTruthy()
      expect(within(panel).getByText(item.comment_id, { exact: true })).toBeTruthy()
      expect(within(panel).getByText(item.published_at, { exact: true })).toBeTruthy()
    }

    for (const safetyText of [
      'Synthetic fixture only',
      'No provider request',
      'Human review required',
      'No Evidence persistence',
      'No analysis run',
    ]) {
      expect(within(panel).getAllByText(safetyText, { exact: true }).length).toBeGreaterThanOrEqual(1)
    }

    expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(0)
    expect(apiMocks.getYouTubeOfficialApiMockCandidates).toHaveBeenCalledTimes(0)
    expect(apiMocks.getMockSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
    expect(within(panel).queryByRole('button', { name: /attach/i })).toBeNull()
    expect(within(panel).queryByRole('button', { name: /analysis/i })).toBeNull()
  })

  it('keeps review decisions local while preserving every underlying pending status', () => {
    render(<SearchDiscovery publicDiscussionReviewFrontendEnabled />)
    const panel = screen.getByTestId('public-discussion-review-panel')
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Load synthetic public discussion fixture / 加载模拟讨论',
      }),
    )

    const [acceptedItem, rejectedItem] = PUBLIC_DISCUSSION_REVIEW_FIXTURE.items
    fireEvent.click(within(panel).getByRole('button', { name: `Accept ${acceptedItem.discussion_id}` }))
    fireEvent.click(within(panel).getByRole('button', { name: `Reject ${rejectedItem.discussion_id}` }))

    expect(
      screen.getByTestId(`public-discussion-decision-${acceptedItem.discussion_id}`).textContent,
    ).toBe('local decision=accepted')
    expect(
      screen.getByTestId(`public-discussion-decision-${rejectedItem.discussion_id}`).textContent,
    ).toBe('local decision=rejected')
    expect(PUBLIC_DISCUSSION_REVIEW_FIXTURE.items.map((item) => item.status)).toEqual([
      'pending_review',
      'pending_review',
      'pending_review',
    ])
    expect(apiMocks.attachSearchDiscoveryCandidates).toHaveBeenCalledTimes(0)
  })

  it('matches the frozen safe-mode fixture contract without identity or credential fields', () => {
    expect(PUBLIC_DISCUSSION_REVIEW_FIXTURE.item_count).toBe(3)
    expect(PUBLIC_DISCUSSION_REVIEW_FIXTURE.safe_mode).toEqual({
      public_discussion_text: true,
      top_level_comments_only: true,
      reply_content_acquired: false,
      pagination: false,
      url_fetching: false,
      scraping: false,
      cookies_used: false,
      secrets_exposed: false,
      evidence_write: false,
      analysis_run: false,
      human_review_required: true,
    })

    const serializedFixture = JSON.stringify(PUBLIC_DISCUSSION_REVIEW_FIXTURE)
    for (const forbiddenField of [
      /author(?:_|\")/i,
      /credential/i,
      /api[_-]?key/i,
      /token/i,
      /cookie(?:_|\")/i,
      /raw[_-]?(?:body|text|metadata)/i,
    ]) {
      expect(serializedFixture).not.toMatch(forbiddenField)
    }
  })
})

describe('SearchDiscovery provider-backed public-discussion bridge Phase 2E3D', () => {
  it('uses the existing hidden route through apiClient with a bounded normalized response', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    expect(typeof actualApi.getYouTubeOfficialApiLivePublicDiscussion).toBe('function')

    const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get')
      .mockResolvedValue({ data: LIVE_DISCUSSION_BATCH })
    const result = await actualApi.getYouTubeOfficialApiLivePublicDiscussion('current_001')

    expect(getSpy).toHaveBeenCalledTimes(1)
    expect(getSpy).toHaveBeenCalledWith(
      '/api/v1/search-discovery/youtube-official-api/live-public-discussion/current_001',
      { params: { max_items: 3 } },
    )
    expect(result.video_id).toBe('current_001')
    expect(result.item_count).toBe(2)
    expect(result.items).toHaveLength(2)
    expect(result.items.every((item) => item.status === 'pending_review')).toBe(true)
    expect(result.safe_mode).toEqual(expect.objectContaining({
      top_level_comments_only: true,
      reply_content_acquired: false,
      evidence_write: false,
      analysis_run: false,
      human_review_required: true,
    }))
  })

  it('keeps the provider-backed load control absent when either frontend gate is false', async () => {
    render(<SearchDiscovery publicDiscussionReviewFrontendEnabled />)
    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()

    cleanup()
    apiMocks.getSearchDiscoveryProviders.mockClear()
    render(<SearchDiscovery liveRouteFrontendEnabled />)
    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(0)
  })

  it('requires explicit accept and then a second explicit action for exactly one bounded request', async () => {
    render(
      <SearchDiscovery
        liveRouteFrontendEnabled
        publicDiscussionReviewFrontendEnabled
      />,
    )

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
    fireEvent.click(screen.getByRole('button', { name: /Generate guarded live preview/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })

    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(0)
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(0)

    const panel = screen.getByTestId('public-discussion-review-panel')
    const loadButton = within(panel).getByRole('button', {
      name: 'Load provider-backed public discussion / 加载官方 API 公开讨论',
    })
    fireEvent.click(loadButton)

    await waitFor(() => {
      expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledWith('current_001', 3)
    })
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
    expect(within(panel).getAllByTestId('public-discussion-review-item')).toHaveLength(2)
    for (const item of LIVE_DISCUSSION_BATCH.items) {
      expect(within(panel).getByText(item.body_text, { exact: true })).toBeTruthy()
    }
    expect(within(panel).getAllByText('schema status=pending_review', { exact: true })).toHaveLength(2)
    for (const safetyText of [
      'Official API public comments / provider-backed review',
      'Top-level comments only',
      'Author identity omitted',
      'Reply content not acquired',
      'Human review required',
      'No Evidence persistence',
      'No analysis run',
      'Provider transport is not truth verification',
    ]) {
      expect(within(panel).getAllByText(safetyText, { exact: true }).length).toBeGreaterThanOrEqual(1)
    }
    expect(within(panel).queryByRole('button', { name: /attach/i })).toBeNull()
    expect(within(panel).queryByRole('button', { name: /analysis/i })).toBeNull()
    expect(within(panel).getByRole('button', {
      name: 'Load synthetic public discussion fixture / 加载模拟讨论',
    })).toBeTruthy()

    const acceptedItem = LIVE_DISCUSSION_BATCH.items[0]
    fireEvent.click(within(panel).getByRole('button', { name: `Accept ${acceptedItem.discussion_id}` }))
    expect(
      within(panel).getByTestId(`public-discussion-decision-${acceptedItem.discussion_id}`).textContent,
    ).toBe('local decision=accepted')
    expect(LIVE_DISCUSSION_BATCH.items.every((item) => item.status === 'pending_review')).toBe(true)
  })

  it('fails an invalid non-YouTube candidate locally without exposing a load action', async () => {
    apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue({
      ...LIVE_BATCH,
      candidates: [{ ...LIVE_BATCH.candidates[0], url: 'https://example.com/watch?v=current_001' }],
    })
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled />)

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.click(screen.getByRole('button', { name: /Generate guarded live preview/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))

    expect(await screen.findByText('Accepted live candidate does not contain a valid YouTube watch URL.')).toBeTruthy()
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(0)
  })

  it('shows a bounded helper failure without retry or synthetic fallback', async () => {
    apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockRejectedValue(
      new Error('provider route unavailable'),
    )
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled />)

    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.click(screen.getByRole('button', { name: /Generate guarded live preview/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    fireEvent.click(screen.getByRole('button', { name: /Load provider-backed public discussion/ }))

    expect(await screen.findByText('Unable to load provider-backed public discussion.')).toBeTruthy()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
    expect(screen.queryByText(PUBLIC_DISCUSSION_REVIEW_FIXTURE.items[0].body_text)).toBeNull()
    expect(screen.queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
  })
})
