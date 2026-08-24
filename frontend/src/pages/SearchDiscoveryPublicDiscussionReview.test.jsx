import React from 'react'
import { cleanup, fireEvent, render, screen, waitFor, within } from '@testing-library/react'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'

const apiMocks = vi.hoisted(() => ({
  attachSearchDiscoveryCandidates: vi.fn(),
  getAnalysisCase: vi.fn(),
  getMockSearchDiscoveryCandidates: vi.fn(),
  getSearchDiscoveryProviders: vi.fn(),
  getYouTubeOfficialApiLiveCandidates: vi.fn(),
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

beforeEach(() => {
  installFailClosedBrowserNetworkSentinels()
  Object.values(apiMocks).forEach((mock) => mock.mockReset())
  apiMocks.getSearchDiscoveryProviders.mockResolvedValue([])

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
