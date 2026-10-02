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
  review_batch_safe_hash: 'a'.repeat(64),
  review_item_safe_hashes: {
    youtube_official_api_current_001_comment_001: 'b'.repeat(64),
    youtube_official_api_current_001_comment_002: 'c'.repeat(64),
  },
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

const TARGET_CASE = {
  case_id: 'case_001',
  title: 'Current launch case',
  keyword: 'Current launch',
}

const SECOND_TARGET_CASE = {
  case_id: 'case_002',
  title: 'Second target case',
  keyword: 'Second target',
}

const ATTACH_RESULT = {
  case_id: TARGET_CASE.case_id,
  video_id: LIVE_DISCUSSION_BATCH.video_id,
  status: 'attached',
  attached_discussion_count: 1,
  attached_evidence_items: [
    {
      evidence_id: 'evidence_youtube_official_api_current_001_comment_001',
      case_id: TARGET_CASE.case_id,
      platform: 'youtube',
      source_type: 'youtube',
      acquisition_mode: 'official_api_public',
      evidence_type: 'comment',
      comment_text: LIVE_DISCUSSION_BATCH.items[0].body_text,
      provenance_type: 'official_api',
      verification_status: 'verified_by_official_api',
    },
  ],
  evidence_result: {
    case_id: TARGET_CASE.case_id,
    status: 'attached',
    evidence_items: [],
    evidence_item_count: 1,
  },
  review_batch_safe_hash: LIVE_DISCUSSION_BATCH.review_batch_safe_hash,
  review_binding_mode: 'selected_item_v1',
  reviewed_batch_safe_hash: LIVE_DISCUSSION_BATCH.review_batch_safe_hash,
  // Unselected-item drift may change the fresh batch without invalidating the selected item.
  fresh_batch_safe_hash: 'd'.repeat(64),
  selected_discussion_safe_hashes: {
    [LIVE_DISCUSSION_BATCH.items[0].discussion_id]: 'b'.repeat(64),
  },
  safe_mode: {
    server_side_refetch: true,
    analysis_run: false,
    report_triggered: false,
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

function selectTargetCaseOption(targetCase) {
  const combobox = screen.getAllByRole('combobox')[1]
  const label = `${targetCase.title} · ${targetCase.case_id}`
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

async function renderAcceptedLiveCandidate(props = {}) {
  render(
    <SearchDiscovery
      liveRouteFrontendEnabled
      publicDiscussionReviewFrontendEnabled
      {...props}
    />,
  )
  await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
  await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
  // Live targets are deliberate; the legacy cases[0] implicit adoption is not authority.
  if (props.cases?.[0]) await selectTargetCaseOption(props.cases[0])
  fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
  await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
  fireEvent.click(screen.getByRole('button', { name: '接受' }))
  return screen.getByTestId('public-discussion-review-panel')
}

async function renderProviderDiscussion(props = {}) {
  const panel = await renderAcceptedLiveCandidate(props)
  fireEvent.click(within(panel).getByRole('button', { name: /Load provider-backed public discussion/ }))
  await waitFor(() => {
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
  })
  await within(panel).findByText(LIVE_DISCUSSION_BATCH.items[0].body_text, { exact: true })
  return panel
}

beforeEach(() => {
  installFailClosedBrowserNetworkSentinels()
  Object.values(apiMocks).forEach((mock) => mock.mockReset())
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([LIVE_PROVIDER])
  apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: false, exists: false })
  apiMocks.getYouTubeOfficialApiLiveCandidates.mockResolvedValue(LIVE_BATCH)
  apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockResolvedValue(LIVE_DISCUSSION_BATCH)
  apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mockResolvedValue(ATTACH_RESULT)
  apiMocks.getAnalysisCase.mockResolvedValue(TARGET_CASE)

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
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
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
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
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
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
  fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    fireEvent.click(screen.getByRole('button', { name: /Load provider-backed public discussion/ }))

    expect(await screen.findByText('Unable to load provider-backed public discussion.')).toBeTruthy()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
    expect(screen.queryByText(PUBLIC_DISCUSSION_REVIEW_FIXTURE.items[0].body_text)).toBeNull()
    expect(screen.queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
  })
})

describe('RDS1 current-query discussion eligibility', () => {
  it('revokes discussion loading after query drift, with no implicit provider action', async () => {
    render(<SearchDiscovery liveRouteFrontendEnabled publicDiscussionReviewFrontendEnabled />)
    await waitFor(() => expect(apiMocks.getSearchDiscoveryProviders).toHaveBeenCalledTimes(1))
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
    fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
    await screen.findByText(LIVE_BATCH.candidates[0].title, { exact: true })
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    expect(screen.getByRole('button', { name: /Load provider-backed public discussion/ })).toBeTruthy()
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'New event' } })
    expect(screen.queryByRole('button', { name: /Load provider-backed public discussion/ })).toBeNull()
    expect(screen.getByText('Historical real official-API metadata batch for query: Current launch')).toBeTruthy()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).not.toHaveBeenCalled()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })

  it('revokes reviewed-attach eligibility when the displayed search is no longer current', async () => {
    const panel = await renderProviderDiscussion({
      publicDiscussionAttachFrontendEnabled: true,
      cases: [TARGET_CASE], currentCase: TARGET_CASE,
    })
    fireEvent.click(within(panel).getByRole('button', { name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}` }))
    const attach = within(panel).getByRole('button', { name: 'Attach reviewed public discussion to case' })
    expect(attach.disabled).toBe(false)
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'New event' } })
    expect(within(panel).queryByRole('button', { name: 'Attach reviewed public discussion to case' })).toBeNull()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })
})

describe('SearchDiscovery reviewed public-discussion case evidence bridge', () => {
  it('uses the hidden attach endpoint with the exact two-field request body', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const postSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'post')
      .mockResolvedValue({ data: {
        ...ATTACH_RESULT, review_binding_mode: 'batch_v1', selected_discussion_safe_hashes: {},
      } })
    const payload = {
      review_batch_safe_hash: LIVE_DISCUSSION_BATCH.review_batch_safe_hash,
      selected_discussion_ids: [LIVE_DISCUSSION_BATCH.items[0].discussion_id],
    }

    const result = await actualApi.attachYouTubeOfficialApiReviewedPublicDiscussion(
      TARGET_CASE.case_id,
      LIVE_DISCUSSION_BATCH.video_id,
      payload,
    )

    expect(postSpy).toHaveBeenCalledTimes(1)
    expect(postSpy).toHaveBeenCalledWith(
      '/api/v1/cases/case_001/search-discovery/youtube-official-api/live-public-discussion/current_001/attach-reviewed',
      payload,
    )
    expect(result.attached_discussion_count).toBe(1)
    expect(result.review_batch_safe_hash).toBe(LIVE_DISCUSSION_BATCH.review_batch_safe_hash)
    expect(result.safe_mode).toEqual(expect.objectContaining({
      server_side_refetch: true,
      analysis_run: false,
      report_triggered: false,
    }))
  })

  it('keeps the attach control absent when the new frontend gate is off', async () => {
    const panel = await renderProviderDiscussion({ cases: [TARGET_CASE] })

    expect(
      within(panel).queryByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    ).toBeNull()
  })

  it('never exposes attach for the synthetic discussion fixture', () => {
    render(
      <SearchDiscovery
        cases={[TARGET_CASE]}
        publicDiscussionReviewFrontendEnabled
        publicDiscussionAttachFrontendEnabled
      />,
    )
    const panel = screen.getByTestId('public-discussion-review-panel')
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Load synthetic public discussion fixture / 加载模拟讨论',
      }),
    )

    expect(
      within(panel).queryByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    ).toBeNull()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledTimes(0)
  })

  it('keeps attach disabled for a provider batch with no accepted comments', async () => {
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
    })
    const attachButton = within(panel).getByRole('button', {
      name: 'Attach reviewed public discussion to case',
    })

    expect(attachButton.disabled).toBe(true)
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledTimes(0)
  })

  it('keeps attach disabled when a comment is accepted without a target case', async () => {
    const panel = await renderProviderDiscussion({
      publicDiscussionAttachFrontendEnabled: true,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )

    const attachButton = within(panel).getByRole('button', {
      name: 'Attach reviewed public discussion to case',
    })
    expect(attachButton.disabled).toBe(true)
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledTimes(0)
  })

  it('enables attach only for a provider batch, valid hash, target case, and accepted comment', async () => {
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )

    const attachButton = within(panel).getByRole('button', {
      name: 'Attach reviewed public discussion to case',
    })
    await waitFor(() => expect(attachButton.disabled).toBe(false))
  })

  it('posts exactly four selected-item fields using server hashes, never browser comment content', async () => {
    const onCaseReady = vi.fn()
    const onRefreshCases = vi.fn().mockResolvedValue(undefined)
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
      onCaseReady,
      onRefreshCases,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    )

    await waitFor(() => {
      expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledTimes(1)
    })
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledWith(
      TARGET_CASE.case_id,
      LIVE_DISCUSSION_BATCH.video_id,
      {
        review_batch_safe_hash: LIVE_DISCUSSION_BATCH.review_batch_safe_hash,
        selected_discussion_ids: [LIVE_DISCUSSION_BATCH.items[0].discussion_id],
        review_binding_mode: 'selected_item_v1',
        selected_discussion_safe_hashes: ATTACH_RESULT.selected_discussion_safe_hashes,
      },
    )
    const payload = apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mock.calls[0][2]
    expect(Object.keys(payload).sort()).toEqual([
      'review_batch_safe_hash',
      'review_binding_mode',
      'selected_discussion_ids',
      'selected_discussion_safe_hashes',
    ])
    expect(JSON.stringify(payload)).not.toContain(LIVE_DISCUSSION_BATCH.items[0].body_text)
    expect(JSON.stringify(payload).toLowerCase()).not.toMatch(/author|credential|raw/)
    await waitFor(() => expect(apiMocks.getAnalysisCase).toHaveBeenCalledWith(TARGET_CASE.case_id))
    expect(onCaseReady).toHaveBeenCalledWith(TARGET_CASE)
    expect(onRefreshCases).toHaveBeenCalledTimes(1)
  })

  it('requires persisted Evidence review after attach and exposes no immediate run shortcut', async () => {
    const onRunCase = vi.fn()
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
      onRunCase,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    )

    const result = await within(panel).findByTestId('public-discussion-attach-result')
    expect(within(result).getByText(`case=${TARGET_CASE.case_id}`, { exact: true })).toBeTruthy()
    expect(within(result).getByText('attached=1', { exact: true })).toBeTruthy()
    expect(within(result).getByText('analysis_run=false', { exact: true })).toBeTruthy()
    expect(onRunCase).toHaveBeenCalledTimes(0)

    expect(within(result).getByText('binding=selected_item_v1', { exact: true })).toBeTruthy()
    expect(within(result).getByText('server-side refetch; selected binding confirmed', { exact: true })).toBeTruthy()
    expect(within(result).getByText(/Review the persisted Evidence before any explicit analysis/)).toBeTruthy()
    expect(within(result).queryByRole('button', { name: /Run analysis/ })).toBeNull()
    expect(onRunCase).toHaveBeenCalledTimes(0)
  })

  it('binds a delayed attach receipt to its immutable case id without a run action', async () => {
    let resolveAttach
    apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mockImplementationOnce(
      () => new Promise((resolve) => {
        resolveAttach = resolve
      }),
    )
    const onRunCase = vi.fn()
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE, SECOND_TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
      onRunCase,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    )
    await waitFor(() => {
      expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledWith(
        TARGET_CASE.case_id,
        LIVE_DISCUSSION_BATCH.video_id,
        expect.any(Object),
      )
    })

    await selectTargetCaseOption(SECOND_TARGET_CASE)
    await act(async () => {
      resolveAttach(ATTACH_RESULT)
      await Promise.resolve()
    })

    const result = await within(panel).findByTestId('public-discussion-attach-result')
    expect(within(result).getByText(`case=${TARGET_CASE.case_id}`, { exact: true })).toBeTruthy()
    expect(within(result).queryByRole('button', { name: /Run analysis/ })).toBeNull()
    expect(onRunCase).not.toHaveBeenCalled()
  })

  it('clears a completed attach receipt when the target case changes', async () => {
    const onRunCase = vi.fn()
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE, SECOND_TARGET_CASE],
      publicDiscussionAttachFrontendEnabled: true,
      onRunCase,
    })
    fireEvent.click(
      within(panel).getByRole('button', {
        name: `Accept ${LIVE_DISCUSSION_BATCH.items[0].discussion_id}`,
      }),
    )
    fireEvent.click(
      within(panel).getByRole('button', {
        name: 'Attach reviewed public discussion to case',
      }),
    )

    const result = await within(panel).findByTestId('public-discussion-attach-result')
    expect(within(result).getByText(`case=${TARGET_CASE.case_id}`, { exact: true })).toBeTruthy()
    await selectTargetCaseOption(SECOND_TARGET_CASE)

    await waitFor(() => {
      expect(within(panel).queryByTestId('public-discussion-attach-result')).toBeNull()
    })
    expect(within(panel).queryByRole('button', { name: 'Run analysis after attach' })).toBeNull()
    expect(onRunCase).toHaveBeenCalledTimes(0)
  })
})

describe('RIE1R2 selected-item hash and receipt contracts', () => {
  const selectedId = LIVE_DISCUSSION_BATCH.items[0].discussion_id
  const selectedPayload = {
    review_batch_safe_hash: LIVE_DISCUSSION_BATCH.review_batch_safe_hash,
    selected_discussion_ids: [selectedId],
    review_binding_mode: 'selected_item_v1',
    selected_discussion_safe_hashes: { [selectedId]: 'b'.repeat(64) },
  }

  it('retains only safe server item hashes without reconstructing absent hashes', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const getSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'get')
      .mockResolvedValueOnce({ data: { ...LIVE_DISCUSSION_BATCH, raw_provider_payload: 'not retained' } })
      .mockResolvedValueOnce({ data: { ...LIVE_DISCUSSION_BATCH, review_item_safe_hashes: undefined } })
    const bound = await actualApi.getYouTubeOfficialApiLivePublicDiscussion('current_001', 3)
    const unbound = await actualApi.getYouTubeOfficialApiLivePublicDiscussion('current_001', 3)
    expect(bound.review_item_safe_hashes).toEqual(LIVE_DISCUSSION_BATCH.review_item_safe_hashes)
    expect(bound).not.toHaveProperty('raw_provider_payload')
    expect(unbound.review_item_safe_hashes).toEqual({})
    expect(getSpy).toHaveBeenCalledTimes(2)
  })

  it.each([
    ['array', []],
    ['malformed value', { [selectedId]: 'not-a-hash' }],
    ['uppercase', { [selectedId]: 'B'.repeat(64) }],
    ['non-string', { [selectedId]: 42 }],
    ['invalid key', { 'unsafe/id': 'b'.repeat(64) }],
  ])('does not retain attach authority from a %s hash map', async (_, hashes) => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    vi.spyOn((await import('../api/client.js')).apiClient, 'get')
      .mockResolvedValue({ data: { ...LIVE_DISCUSSION_BATCH, review_item_safe_hashes: hashes } })
    const result = await actualApi.getYouTubeOfficialApiLivePublicDiscussion('current_001', 3)
    expect(result.review_item_safe_hashes).toEqual({})
  })

  it.each([
    ['unknown mode', { review_binding_mode: 'unknown' }],
    ['missing hashes', { selected_discussion_safe_hashes: undefined }],
    ['missing key', { selected_discussion_safe_hashes: {} }],
    ['extra key', { selected_discussion_safe_hashes: { [selectedId]: 'b'.repeat(64), extra: 'c'.repeat(64) } }],
    ['uppercase hash', { selected_discussion_safe_hashes: { [selectedId]: 'B'.repeat(64) } }],
    ['array hashes', { selected_discussion_safe_hashes: ['b'.repeat(64)] }],
    ['empty selection', { selected_discussion_ids: [] }],
    ['non-string selection', { selected_discussion_ids: [42], selected_discussion_safe_hashes: { 42: 'b'.repeat(64) } }],
    ['duplicate selection', { selected_discussion_ids: [selectedId, selectedId] }],
    ['more than three', { selected_discussion_ids: ['one', 'two', 'three', 'four'] }],
  ])('rejects %s before any attach request, without a batch-mode fallback', async (_, override) => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const postSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'post')
    await expect(actualApi.attachYouTubeOfficialApiReviewedPublicDiscussion(
      TARGET_CASE.case_id, 'current_001', { ...selectedPayload, ...override },
    )).rejects.toThrow(/^youtube_reviewed_public_discussion_/)
    expect(postSpy).not.toHaveBeenCalled()
  })

  it('preserves selected binding and both batch hashes when only unselected items drift', async () => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const postSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'post')
      .mockResolvedValue({ data: { ...ATTACH_RESULT, raw_provider_payload: 'not retained' } })
    const result = await actualApi.attachYouTubeOfficialApiReviewedPublicDiscussion(
      TARGET_CASE.case_id, 'current_001', selectedPayload,
    )
    expect(postSpy).toHaveBeenCalledWith(expect.stringContaining('/attach-reviewed'), selectedPayload)
    expect(result.review_binding_mode).toBe('selected_item_v1')
    expect(result.reviewed_batch_safe_hash).toBe('a'.repeat(64))
    expect(result.fresh_batch_safe_hash).toBe('d'.repeat(64))
    expect(result.selected_discussion_safe_hashes).toEqual(selectedPayload.selected_discussion_safe_hashes)
    expect(result.safe_mode.server_side_refetch).toBe(true)
    expect(result).not.toHaveProperty('raw_provider_payload')
  })

  it.each([1, 2, 3])('accepts an exact server-selected hash set of %i items', async (count) => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const ids = ['one', 'two', 'three'].slice(0, count)
    const hashes = Object.fromEntries(ids.map((id) => [id, 'b'.repeat(64)]))
    const payload = { ...selectedPayload, selected_discussion_ids: ids, selected_discussion_safe_hashes: hashes }
    const postSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'post')
      .mockResolvedValue({ data: { ...ATTACH_RESULT, attached_discussion_count: count, selected_discussion_safe_hashes: hashes } })
    const result = await actualApi.attachYouTubeOfficialApiReviewedPublicDiscussion(TARGET_CASE.case_id, 'current_001', payload)
    expect(result.selected_discussion_safe_hashes).toEqual(hashes)
    expect(result.attached_discussion_count).toBe(count)
    expect(postSpy).toHaveBeenCalledTimes(1)
  })

  it.each([
    ['legacy mode', { review_binding_mode: 'batch_v1' }],
    ['missing reviewed hash', { reviewed_batch_safe_hash: undefined }],
    ['another reviewed batch', { reviewed_batch_safe_hash: 'e'.repeat(64) }],
    ['missing fresh hash', { fresh_batch_safe_hash: undefined }],
    ['invalid fresh hash', { fresh_batch_safe_hash: 'D'.repeat(64) }],
    ['missing selected map', { selected_discussion_safe_hashes: undefined }],
    ['another selected key', { selected_discussion_safe_hashes: { other: 'b'.repeat(64) } }],
    ['another selected hash', { selected_discussion_safe_hashes: { [selectedId]: 'f'.repeat(64) } }],
    ['no server refetch', { safe_mode: { server_side_refetch: false } }],
    ['another video', { video_id: 'current_002' }],
    ['another case', { case_id: 'case_002' }],
    ['invalid count', { attached_discussion_count: 0 }],
    ['not attached', { status: 'rejected' }],
  ])('does not expose a successful selected receipt for %s', async (_, override) => {
    const actualApi = await vi.importActual('../api/sentigraphApi.js')
    const postSpy = vi.spyOn((await import('../api/client.js')).apiClient, 'post')
      .mockResolvedValue({ data: { ...ATTACH_RESULT, ...override } })
    await expect(actualApi.attachYouTubeOfficialApiReviewedPublicDiscussion(
      TARGET_CASE.case_id, 'current_001', selectedPayload,
    )).rejects.toThrow('youtube_reviewed_public_discussion_attach_result_invalid')
    expect(postSpy).toHaveBeenCalledTimes(1)
  })

  it.each([undefined, {}, { [selectedId]: 'malformed' }])(
    'keeps the component attach disabled with missing or malformed selected hashes: %j', async (hashes) => {
      apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockResolvedValue({
        ...LIVE_DISCUSSION_BATCH, review_item_safe_hashes: hashes,
      })
      const panel = await renderProviderDiscussion({
        cases: [TARGET_CASE], publicDiscussionAttachFrontendEnabled: true,
      })
      fireEvent.click(within(panel).getByRole('button', { name: `Accept ${selectedId}` }))
      const attach = within(panel).getByRole('button', { name: 'Attach reviewed public discussion to case' })
      expect(attach.disabled).toBe(true)
      fireEvent.click(attach)
      expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
    },
  )
})

describe('RIE1R2 discussion context revocation and late-result fencing', () => {
  const loadName = /Load provider-backed public discussion/
  const firstId = LIVE_DISCUSSION_BATCH.items[0].discussion_id

  it.each(['query A-B-A', 'lane A-B-A', 'candidate rejection', 'new search', 'synthetic fixture'])(
    'clears provider batch, decisions and attach authority on %s without implicit discussion I/O', async (change) => {
      const panel = await renderProviderDiscussion({
        cases: [TARGET_CASE], publicDiscussionAttachFrontendEnabled: true,
      })
      fireEvent.click(within(panel).getByRole('button', { name: `Accept ${firstId}` }))
      expect(within(panel).getByRole('button', { name: 'Attach reviewed public discussion to case' }).disabled).toBe(false)
      if (change === 'query A-B-A') {
        fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Other event' } })
        fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
      } else if (change === 'lane A-B-A') {
        await selectFirstComboboxOption('Mock Static')
        await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
      } else if (change === 'candidate rejection') {
        fireEvent.click(screen.getByRole('button', { name: '忽略' }))
      } else if (change === 'new search') {
        fireEvent.click(screen.getByRole('button', { name: /Search YouTube Official API metadata/ }))
        await waitFor(() => expect(apiMocks.getYouTubeOfficialApiLiveCandidates).toHaveBeenCalledTimes(2))
      } else {
        fireEvent.click(within(panel).getByRole('button', { name: /Load synthetic public discussion fixture/ }))
      }
      expect(within(panel).queryByText(LIVE_DISCUSSION_BATCH.items[0].body_text, { exact: true })).toBeNull()
      expect(within(panel).queryByTestId(`public-discussion-decision-${firstId}`)).toBeNull()
      expect(within(panel).queryByRole('button', { name: 'Attach reviewed public discussion to case' })).toBeNull()
      expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
      expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
    },
  )

  it.each(['success', 'error'])('discards a late discussion %s even after query A-B-A', async (outcome) => {
    const pending = deferred()
    apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockReturnValueOnce(pending.promise)
    const panel = await renderAcceptedLiveCandidate()
    fireEvent.click(within(panel).getByRole('button', { name: loadName }))
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Other event' } })
    fireEvent.change(screen.getByPlaceholderText('Tesla'), { target: { value: 'Current launch' } })
    await act(async () => {
      if (outcome === 'success') pending.resolve(LIVE_DISCUSSION_BATCH)
      else pending.reject(new Error('stale private provider error'))
      await Promise.resolve()
    })
    expect(within(panel).queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
    expect(within(panel).queryByRole('button', { name: loadName })).toBeNull()
    expect(screen.queryByText('Unable to load provider-backed public discussion.')).toBeNull()
    expect(screen.queryByText(/stale private provider error/)).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
  })

  it('does not let an old discussion completion clear a newer load or replace its decisions', async () => {
    const old = deferred()
    const current = deferred()
    apiMocks.getYouTubeOfficialApiLivePublicDiscussion
      .mockReturnValueOnce(old.promise).mockReturnValueOnce(current.promise)
    const panel = await renderAcceptedLiveCandidate()
    fireEvent.click(within(panel).getByRole('button', { name: loadName }))
    fireEvent.click(screen.getByRole('button', { name: '忽略' }))
    fireEvent.click(screen.getByRole('button', { name: '接受' }))
    fireEvent.click(within(panel).getByRole('button', { name: loadName }))
    await act(async () => { old.resolve(LIVE_DISCUSSION_BATCH); await Promise.resolve() })
    expect(within(panel).getByRole('button', { name: loadName }).classList.contains('ant-btn-loading')).toBe(true)
    expect(within(panel).queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
    const newBatch = {
      ...LIVE_DISCUSSION_BATCH,
      items: LIVE_DISCUSSION_BATCH.items.map((item) => ({ ...item, body_text: `New request ${item.comment_id}` })),
    }
    await act(async () => { current.resolve(newBatch); await Promise.resolve() })
    expect(within(panel).getByText('New request comment_001', { exact: true })).toBeTruthy()
    expect(within(panel).queryByText(LIVE_DISCUSSION_BATCH.items[0].body_text, { exact: true })).toBeNull()
    expect(within(panel).getByTestId(`public-discussion-decision-${firstId}`).textContent).toBe('local decision=pending_review')
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(2)
  })

  it('rejects discussion from another video without falling back or attaching', async () => {
    apiMocks.getYouTubeOfficialApiLivePublicDiscussion.mockResolvedValue({ ...LIVE_DISCUSSION_BATCH, video_id: 'current_002' })
    const panel = await renderAcceptedLiveCandidate({ cases: [TARGET_CASE], publicDiscussionAttachFrontendEnabled: true })
    fireEvent.click(within(panel).getByRole('button', { name: loadName }))
    await screen.findByText('The returned public discussion does not match the selected video. Use a new explicit request.')
    expect(within(panel).queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })

  it('keeps the collector lane outside discussion and selected-item attach authority', async () => {
    apiMocks.getExternalCollectorStatus.mockResolvedValue({ configured: true, exists: true })
    const panel = await renderProviderDiscussion({ cases: [TARGET_CASE], publicDiscussionAttachFrontendEnabled: true })
    fireEvent.click(within(panel).getByRole('button', { name: `Accept ${firstId}` }))
    await selectFirstComboboxOption('External Collector Handoff — already-produced local packages')
    expect(screen.queryByTestId('public-discussion-review-panel')).toBeNull()
    await selectFirstComboboxOption(LIVE_PROVIDER_LABEL)
    expect(screen.queryAllByTestId('public-discussion-review-item')).toHaveLength(0)
    expect(screen.queryByRole('button', { name: loadName })).toBeNull()
    expect(apiMocks.getYouTubeOfficialApiLivePublicDiscussion).toHaveBeenCalledTimes(1)
    expect(apiMocks.getExternalCollectorDiscovery).not.toHaveBeenCalled()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).not.toHaveBeenCalled()
  })

  it.each(['success', 'error'])('discards a late attach %s after its context is revoked', async (outcome) => {
    const pending = deferred()
    apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion.mockReturnValueOnce(pending.promise)
    const onCaseReady = vi.fn()
    const onRefreshCases = vi.fn()
    const onRunCase = vi.fn()
    const panel = await renderProviderDiscussion({
      cases: [TARGET_CASE], publicDiscussionAttachFrontendEnabled: true, onCaseReady, onRefreshCases, onRunCase,
    })
    fireEvent.click(within(panel).getByRole('button', { name: `Accept ${firstId}` }))
    fireEvent.click(within(panel).getByRole('button', { name: 'Attach reviewed public discussion to case' }))
    fireEvent.click(screen.getByRole('button', { name: '忽略' }))
    await act(async () => {
      if (outcome === 'success') pending.resolve(ATTACH_RESULT)
      else pending.reject(new Error('stale attach error'))
      await Promise.resolve()
    })
    expect(within(panel).queryByTestId('public-discussion-attach-result')).toBeNull()
    expect(apiMocks.getAnalysisCase).not.toHaveBeenCalled()
    expect(onCaseReady).not.toHaveBeenCalled()
    expect(onRefreshCases).not.toHaveBeenCalled()
    expect(onRunCase).not.toHaveBeenCalled()
    expect(screen.queryByText('stale attach error', { exact: true })).toBeNull()
    expect(apiMocks.attachYouTubeOfficialApiReviewedPublicDiscussion).toHaveBeenCalledTimes(1)
  })
})
