import { Alert, Button, Card, Empty, Form, Input, Select, Space, Statistic, Table, Tag, Typography } from 'antd'
import { CheckCircle2, FileSearch, LinkIcon, PlayCircle, RefreshCw, ShieldCheck, XCircle } from 'lucide-react'
import React, { useEffect, useMemo, useRef, useState } from 'react'

import {
  attachSearchDiscoveryCandidates,
  attachYouTubeOfficialApiReviewedPublicDiscussion,
  createAnalysisCase,
  getAnalysisCase,
  getExternalCollectorDiscovery,
  getExternalCollectorStatus,
  getMockSearchDiscoveryCandidates,
  getSearchDiscoveryProviders,
  getYouTubeOfficialApiLiveCandidates,
  getYouTubeOfficialApiLivePublicDiscussion,
  getYouTubeOfficialApiMockCandidates,
} from '../api/sentigraphApi.js'
import { PUBLIC_DISCUSSION_REVIEW_FIXTURE } from '../fixtures/publicDiscussionReviewFixture.js'
import { buildGuidedCaseCreatePayload, scopeFromReviewedAttach } from '../utils/guidedCaseFlow.js'

const { Paragraph, Text, Title } = Typography

const STATUS_COLORS = {
  accepted: 'green',
  rejected: 'red',
  attached: 'blue',
  pending_review: 'gold',
}

const MOCK_PROVIDER_TYPES = ['mock_static', 'rss_mock', 'gdelt_mock', 'youtube_official_api']
const FALLBACK_PROVIDER_OPTIONS = [
  { value: 'mock_static', label: 'Mock Static' },
  { value: 'rss_mock', label: 'RSS Mock' },
  { value: 'gdelt_mock', label: 'GDELT Mock' },
  { value: 'youtube_official_api', label: 'YouTube Official API — offline mocked response (Phase 1)' },
]
const LIVE_PROVIDER_ID = 'youtube_official_api_live'
const COLLECTOR_LANE_ID = 'external_collector_handoff'
const COLLECTOR_LANE_LABEL = 'External Collector Handoff — already-produced local packages'
const COLLECTOR_SEARCH_ERRORS = Object.freeze({
  external_collector_bridge_not_configured: 'The external collector bridge is not configured.',
  external_collector_configured_root_missing: 'The configured external collector root is unavailable.',
  external_collector_query_required: 'Enter a non-blank query before searching external collector packages.',
  external_collector_query_invalid: 'Use a valid query of at most 120 characters.',
  external_collector_internal_failure: 'Unable to search the local external collector package summaries.',
})
const LIVE_SEARCH_ERRORS = Object.freeze({
  youtube_live_search_discovery_route_disabled: 'The backend live search route is disabled.',
  youtube_live_search_discovery_credential_missing: 'The backend live search credential is missing.',
  youtube_live_search_discovery_quota_error: 'The official API reported a quota error.',
  youtube_live_search_discovery_auth_error: 'The official API reported an authentication or authorization failure.',
  youtube_live_search_discovery_network_error: 'The official API request failed at the network boundary.',
  youtube_live_search_discovery_parsing_error: 'The official API response could not be parsed.',
  youtube_live_search_discovery_provider_error: 'The official API reported a provider failure.',
})

function normalizeDiscoveryQuery(value) {
  return String(value || '').replace(/\s+/g, ' ').trim()
}

function safeLiveSearchError(error) {
  const code = error?.response?.data?.detail
  return typeof code === 'string' && Object.hasOwn(LIVE_SEARCH_ERRORS, code)
    ? LIVE_SEARCH_ERRORS[code]
    : 'Unable to complete the official API metadata search.'
}

function safeCollectorSearchError(error) {
  const code = error?.response?.data?.detail
  if (error?.response?.status === 422) return COLLECTOR_SEARCH_ERRORS.external_collector_query_invalid
  return typeof code === 'string' && Object.hasOwn(COLLECTOR_SEARCH_ERRORS, code)
    ? COLLECTOR_SEARCH_ERRORS[code]
    : 'Unable to search the local external collector package summaries.'
}

function getYouTubeWatchVideoId(candidateUrl) {
  try {
    const parsed = new URL(String(candidateUrl || ''))
    const host = parsed.hostname.toLowerCase()
    if (
      parsed.protocol !== 'https:' ||
      !['youtube.com', 'www.youtube.com', 'm.youtube.com'].includes(host) ||
      parsed.pathname !== '/watch'
    ) {
      return null
    }
    const videoId = parsed.searchParams.get('v') || ''
    return /^[A-Za-z0-9_-]{11}$/.test(videoId) ? videoId : null
  } catch {
    return null
  }
}

export function SearchDiscovery({
  cases = [],
  currentCase,
  onCaseReady,
  onRefreshCases,
  onRunCase,
  onOpenGuidedEvidenceReview,
  liveRouteFrontendEnabled =
    import.meta.env.VITE_SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_ENABLED === '1',
  publicDiscussionReviewFrontendEnabled =
    import.meta.env.VITE_SENTIGRAPH_SEARCH_DISCOVERY_PUBLIC_DISCUSSION_REVIEW_ENABLED === '1',
  publicDiscussionAttachFrontendEnabled =
    import.meta.env.VITE_SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_REVIEWED_EVIDENCE_ATTACH_ENABLED === '1',
}) {
  const [query, setQuery] = useState('Tesla')
  const [provider, setProvider] = useState('mock_static')
  const [providers, setProviders] = useState([])
  const [collectorStatus, setCollectorStatus] = useState({ configured: false, exists: false })
  const [collectorBatch, setCollectorBatch] = useState(null)
  const [generatedCollectorQuery, setGeneratedCollectorQuery] = useState(null)
  const [generatedCollectorLane, setGeneratedCollectorLane] = useState(null)
  const [targetCaseId, setTargetCaseId] = useState(currentCase?.case_id || '')
  const [liveTargetCaseId, setLiveTargetCaseId] = useState('')
  const [createdCaseOption, setCreatedCaseOption] = useState(null)
  const [creatingCase, setCreatingCase] = useState(false)
  const [createNotice, setCreateNotice] = useState('')
  const [batch, setBatch] = useState(null)
  const [generatedProvider, setGeneratedProvider] = useState(null)
  const [generatedQuery, setGeneratedQuery] = useState(null)
  const [generatedSearchEpoch, setGeneratedSearchEpoch] = useState(null)
  const [candidateStatusById, setCandidateStatusById] = useState({})
  const [loading, setLoading] = useState(false)
  const [attaching, setAttaching] = useState(false)
  const [attachResult, setAttachResult] = useState(null)
  const [publicDiscussionBatch, setPublicDiscussionBatch] = useState(null)
  const [publicDiscussionDecisionById, setPublicDiscussionDecisionById] = useState({})
  const [publicDiscussionLoading, setPublicDiscussionLoading] = useState(false)
  const [publicDiscussionSource, setPublicDiscussionSource] = useState(null)
  const [publicDiscussionContextKey, setPublicDiscussionContextKey] = useState(null)
  const [publicDiscussionAttaching, setPublicDiscussionAttaching] = useState(false)
  const [publicDiscussionAttachResult, setPublicDiscussionAttachResult] = useState(null)
  const [guidedAttachScope, setGuidedAttachScope] = useState(null)
  const [error, setError] = useState('')
  const searchRequestEpochRef = useRef(0)
  const discussionRequestEpochRef = useRef(0)
  const reviewedAttachRequestEpochRef = useRef(0)
  const discussionContextKeyRef = useRef(null)
  const createContextEpochRef = useRef(0)
  const createPendingRef = useRef(false)
  const mountedRef = useRef(true)
  const reviewedAttachPendingRef = useRef(false)
  const [reviewedAttachPending, setReviewedAttachPending] = useState(false)

  useEffect(() => {
    mountedRef.current = true
    return () => {
      mountedRef.current = false
      createContextEpochRef.current += 1
      searchRequestEpochRef.current += 1
      discussionRequestEpochRef.current += 1
      reviewedAttachRequestEpochRef.current += 1
      discussionContextKeyRef.current = null
    }
  }, [])

  function invalidateCreateContext() {
    createContextEpochRef.current += 1
    setCreateNotice('')
  }

  useEffect(() => { createContextEpochRef.current += 1 }, [currentCase?.case_id])

  // Revoke authority in the user event, before a pending promise can resolve.
  function invalidatePublicDiscussion() {
    discussionRequestEpochRef.current += 1
    reviewedAttachRequestEpochRef.current += 1
    discussionContextKeyRef.current = null
    setPublicDiscussionContextKey(null)
    setPublicDiscussionBatch(null)
    setPublicDiscussionDecisionById({})
    setPublicDiscussionSource(null)
    setPublicDiscussionAttachResult(null)
    setPublicDiscussionLoading(false)
    setPublicDiscussionAttaching(false)
  }

  function invalidateSearchContext() {
    searchRequestEpochRef.current += 1
    setGeneratedSearchEpoch(null)
    setLoading(false)
    invalidatePublicDiscussion()
  }

  function handleQueryChange(nextQuery) {
    if (nextQuery !== query) {
      invalidateSearchContext()
      invalidateCreateContext()
    }
    setQuery(nextQuery)
  }

  function handleProviderChange(nextProvider) {
    if (nextProvider !== provider) {
      invalidateSearchContext()
      invalidateCreateContext()
    }
    setProvider(nextProvider)
  }

  useEffect(() => {
    let isMounted = true
    getSearchDiscoveryProviders()
      .then((items) => {
        if (isMounted) setProviders(items)
      })
      .catch(() => {
        if (isMounted) setProviders([])
      })
    return () => {
      isMounted = false
    }
  }, [])

  useEffect(() => {
    let isMounted = true
    // Only the two availability booleans are retained; no paths/notes enter page state.
    const unavailable = () => {
      if (isMounted) setCollectorStatus({ configured: false, exists: false })
    }
    try {
      Promise.resolve(getExternalCollectorStatus())
        .then((status) => {
          if (isMounted) setCollectorStatus({
            configured: status?.configured === true,
            exists: status?.exists === true,
          })
        })
        .catch(unavailable)
    } catch {
      unavailable()
    }
    return () => { isMounted = false }
  }, [])

  useEffect(() => {
    if (provider === LIVE_PROVIDER_ID) return
    if (targetCaseId) return
    if (currentCase?.case_id) {
      setTargetCaseId(currentCase.case_id)
    } else if (!targetCaseId && cases[0]?.case_id) {
      setTargetCaseId(cases[0].case_id)
    }
  }, [cases, currentCase, targetCaseId, provider])

  function handleTargetCaseChange(nextCaseId) {
    invalidateCreateContext()
    if (provider === LIVE_PROVIDER_ID) setLiveTargetCaseId(nextCaseId)
    else setTargetCaseId(nextCaseId)
    setPublicDiscussionAttachResult(null)
  }

  async function handleCreateCaseFromQuery() {
    if (createPendingRef.current) return
    const payload = buildGuidedCaseCreatePayload(query, provider === LIVE_PROVIDER_ID)
    if (!payload) {
      setError('Enter a non-blank query of at most 120 characters before creating a case.')
      return
    }
    createPendingRef.current = true
    const epoch = ++createContextEpochRef.current
    const live = provider === LIVE_PROVIDER_ID
    const isCurrent = () => mountedRef.current && createContextEpochRef.current === epoch
    setCreatingCase(true)
    setCreateNotice('')
    setError('')
    try {
      const created = await createAnalysisCase(payload)
      if (!isCurrent()) return
      if (!/^[A-Za-z0-9_-]{1,200}$/.test(created?.case_id || '') ||
          normalizeDiscoveryQuery(created.keyword) !== payload.keyword || created.status !== 'draft') {
        setError('The create receipt is invalid. Any server-side draft is retained; no automatic retry or deletion.')
        return
      }
      const option = { case_id: created.case_id, title: created.title || payload.title }
      setCreatedCaseOption(option)
      if (live) setLiveTargetCaseId(created.case_id)
      else setTargetCaseId(created.case_id)
      setPublicDiscussionAttachResult(null)
      setCreateNotice(`Created draft case=${created.case_id}. Creation does not run analysis.`)
      await onCaseReady?.(created)
      if (!isCurrent()) return
      await onRefreshCases?.()
    } catch {
      if (isCurrent()) setError('Unable to create the case. No automatic retry; any server-side draft remains intact.')
    } finally {
      createPendingRef.current = false
      if (mountedRef.current) setCreatingCase(false)
    }
  }

  const caseOptions = useMemo(
    () =>
      [...cases, ...(createdCaseOption && !cases.some((item) => item.case_id === createdCaseOption.case_id)
        ? [createdCaseOption] : [])].map((item) => ({
        value: item.case_id,
        label: `${item.title || item.keyword || item.case_id} · ${item.case_id}`,
      })),
    [cases, createdCaseOption],
  )

  const providerOptions = useMemo(() => {
    const options = providers
      .filter((item) => item.provider_id !== LIVE_PROVIDER_ID && MOCK_PROVIDER_TYPES.includes(item.provider_type || item.provider_id))
      .map((item) => ({
        value: item.provider_id,
        label: item.display_name || item.provider_id,
      }))
    const offlineOptions = options.length ? options : FALLBACK_PROVIDER_OPTIONS
    const liveDescriptor = providers.find(
      (item) => item.provider_id === LIVE_PROVIDER_ID && item.provider_type === 'youtube_official_api',
    )
    const candidateOptions = liveRouteFrontendEnabled && liveDescriptor
      ? [...offlineOptions, {
        value: LIVE_PROVIDER_ID,
        label: liveDescriptor.display_name,
        disabled: liveDescriptor.live_fetch_enabled !== true,
      }]
      : offlineOptions
    return collectorStatus.configured && collectorStatus.exists
      ? [...candidateOptions, { value: COLLECTOR_LANE_ID, label: COLLECTOR_LANE_LABEL }]
      : candidateOptions
  }, [liveRouteFrontendEnabled, providers, collectorStatus.configured, collectorStatus.exists])

  const selectedProviderStatus = useMemo(() => {
    return providers.find((item) => item.provider_id === provider) || null
  }, [provider, providers])

  const candidates = useMemo(() => {
    const rawCandidates = Array.isArray(batch?.candidates) ? batch.candidates : []
    return rawCandidates.map((candidate) => ({
      ...candidate,
      status: candidateStatusById[candidate.candidate_id] || candidate.status || 'pending_review',
    }))
  }, [batch, candidateStatusById])

  const acceptedCandidates = useMemo(
    () => candidates.filter((candidate) => candidate.status === 'accepted'),
    [candidates],
  )

  const acceptedCount = acceptedCandidates.length
  const rejectedCount = candidates.filter((candidate) => candidate.status === 'rejected').length
  const liveBatchPreviewOnly = generatedProvider === LIVE_PROVIDER_ID
  const liveSelected = provider === LIVE_PROVIDER_ID
  const effectiveTargetCaseId = liveSelected ? liveTargetCaseId : targetCaseId
  const collectorSelected = provider === COLLECTOR_LANE_ID
  const collectorAvailable = collectorStatus.configured && collectorStatus.exists
  const generatedSearchCurrent = generatedSearchEpoch !== null &&
    generatedSearchEpoch === searchRequestEpochRef.current
  const collectorBatchCurrent = Boolean(collectorBatch) && generatedCollectorLane === provider &&
    generatedCollectorQuery === normalizeDiscoveryQuery(query) && generatedSearchCurrent
  const backendLiveDescriptor = providers.find(
    (item) => item.provider_id === LIVE_PROVIDER_ID && item.provider_type === 'youtube_official_api',
  )
  const liveSearchAvailable = liveRouteFrontendEnabled && backendLiveDescriptor?.live_fetch_enabled === true
  const generatedBatchMatchesProvider = Boolean(generatedProvider) && generatedProvider === provider
  const generatedBatchMatchesQuery = generatedQuery !== null && generatedQuery === normalizeDiscoveryQuery(query)
  const generatedLiveBatchCurrent = liveBatchPreviewOnly && generatedBatchMatchesProvider &&
    generatedBatchMatchesQuery && generatedSearchCurrent
  const acceptedLiveCandidate = generatedLiveBatchCurrent && acceptedCandidates.length === 1
    ? acceptedCandidates[0] || null
    : null
  const acceptedLiveVideoId = getYouTubeWatchVideoId(acceptedLiveCandidate?.url)
  const liveCandidateContextKey = acceptedLiveCandidate?.candidate_id?.trim() && acceptedLiveVideoId &&
    normalizeDiscoveryQuery(acceptedLiveCandidate.query) === generatedQuery
    ? JSON.stringify({
      search_epoch: generatedSearchEpoch,
      submitted_query: generatedQuery,
      lane: generatedProvider,
      candidate_id: acceptedLiveCandidate.candidate_id,
      video_id: acceptedLiveVideoId,
    })
    : null
  const providerDiscussionLoadAvailable = Boolean(
    liveSearchAvailable &&
    publicDiscussionReviewFrontendEnabled &&
    acceptedLiveCandidate &&
    liveCandidateContextKey,
  )
  const acceptedPublicDiscussionIds = useMemo(
    () => (publicDiscussionBatch?.items || [])
      .filter((item) => publicDiscussionDecisionById[item.discussion_id] === 'accepted')
      .map((item) => item.discussion_id),
    [publicDiscussionBatch, publicDiscussionDecisionById],
  )
  const selectedDiscussionSafeHashes = Object.fromEntries(acceptedPublicDiscussionIds.map((id) => [
    id, Object.hasOwn(publicDiscussionBatch?.review_item_safe_hashes || {}, id)
      ? publicDiscussionBatch.review_item_safe_hashes[id] : undefined,
  ]))
  const publicDiscussionAttachAvailable = Boolean(
    publicDiscussionAttachFrontendEnabled &&
    providerDiscussionLoadAvailable &&
    publicDiscussionBatch?.video_id === acceptedLiveVideoId &&
    publicDiscussionSource === 'provider-backed' &&
    publicDiscussionContextKey === liveCandidateContextKey &&
    discussionContextKeyRef.current === liveCandidateContextKey &&
    liveTargetCaseId &&
    /^[0-9a-f]{64}$/.test(publicDiscussionBatch?.review_batch_safe_hash || '') &&
    acceptedPublicDiscussionIds.length >= 1 &&
    acceptedPublicDiscussionIds.length <= 3 &&
    new Set(acceptedPublicDiscussionIds).size === acceptedPublicDiscussionIds.length &&
    acceptedPublicDiscussionIds.every((id) => typeof selectedDiscussionSafeHashes[id] === 'string' &&
      /^[0-9a-f]{64}$/.test(selectedDiscussionSafeHashes[id])) &&
    !publicDiscussionAttaching && !reviewedAttachPending,
  )

  async function handleGenerateCandidates() {
    if (loading) return
    const submittedProvider = provider
    const submittedQuery = normalizeDiscoveryQuery(query)
    const requestEpoch = ++searchRequestEpochRef.current
    const isCurrentRequest = () => searchRequestEpochRef.current === requestEpoch
    invalidatePublicDiscussion()
    setGeneratedSearchEpoch(null)
    setLoading(true)
    setError('')
    setAttachResult(null)
    setBatch(null)
    setGeneratedProvider(null)
    setGeneratedQuery(null)
    setCandidateStatusById({})
    setCollectorBatch(null)
    setGeneratedCollectorQuery(null)
    setGeneratedCollectorLane(null)
    try {
      if (submittedProvider === COLLECTOR_LANE_ID) {
        if (!collectorAvailable) {
          setError('External Collector Handoff is unavailable: the local bridge must be configured and available.')
          return
        }
        if (!submittedQuery) {
          setError(COLLECTOR_SEARCH_ERRORS.external_collector_query_required)
          return
        }
        const result = await getExternalCollectorDiscovery(submittedQuery, 5)
        if (!isCurrentRequest()) return
        if (normalizeDiscoveryQuery(result.query) !== submittedQuery) {
          setError('The returned collector packages do not match the submitted query. Run a new explicit search.')
          return
        }
        setCollectorBatch(result)
        setGeneratedCollectorQuery(submittedQuery)
        setGeneratedCollectorLane(submittedProvider)
        setGeneratedSearchEpoch(requestEpoch)
        return
      }
      if (submittedProvider === LIVE_PROVIDER_ID) {
        if (!liveSearchAvailable) {
          setError('Live search is unavailable: a backend-enabled descriptor and the frontend gate are required.')
          return
        }
        if (!submittedQuery) {
          setError('Enter a non-blank query before searching YouTube Official API metadata.')
          return
        }
      }
      const result = submittedProvider === LIVE_PROVIDER_ID
        ? await getYouTubeOfficialApiLiveCandidates(submittedQuery, 5)
        : submittedProvider === 'youtube_official_api'
          ? await getYouTubeOfficialApiMockCandidates(query, 5)
          : await getMockSearchDiscoveryCandidates(query, submittedProvider)
      if (!isCurrentRequest()) return
      if (submittedProvider === LIVE_PROVIDER_ID && normalizeDiscoveryQuery(result.query) !== submittedQuery) {
        setError('The returned metadata batch does not match the submitted query. Run a new explicit search.')
        return
      }
      setBatch(result)
      setGeneratedProvider(submittedProvider)
      setGeneratedQuery(submittedQuery)
      setGeneratedSearchEpoch(requestEpoch)
      setCandidateStatusById(
        Object.fromEntries((result.candidates || []).map((candidate) => [candidate.candidate_id, 'pending_review'])),
      )
    } catch (requestError) {
      if (!isCurrentRequest()) return
      setError(submittedProvider === COLLECTOR_LANE_ID
        ? safeCollectorSearchError(requestError)
        : submittedProvider === LIVE_PROVIDER_ID
        ? safeLiveSearchError(requestError)
        : requestError?.message || 'Unable to generate mock Search Discovery candidates.')
    } finally {
      if (isCurrentRequest()) setLoading(false)
    }
  }

  function setCandidateStatus(candidateId, status) {
    if (generatedProvider === LIVE_PROVIDER_ID &&
      candidates.find((item) => item.candidate_id === candidateId)?.status !== status) {
      invalidatePublicDiscussion()
    }
    if (status === 'accepted' && generatedProvider === LIVE_PROVIDER_ID) {
      const candidate = candidates.find((item) => item.candidate_id === candidateId)
      if (!getYouTubeWatchVideoId(candidate?.url)) {
        setError('Accepted live candidate does not contain a valid YouTube watch URL.')
      } else {
        setError('')
      }
    }
    setCandidateStatusById((current) => ({ ...current, [candidateId]: status }))
  }

  function handleLoadPublicDiscussionFixture() {
    invalidatePublicDiscussion()
    setError('')
    setPublicDiscussionAttachResult(null)
    setPublicDiscussionBatch(PUBLIC_DISCUSSION_REVIEW_FIXTURE)
    setPublicDiscussionSource('synthetic')
    setPublicDiscussionDecisionById(
      Object.fromEntries(
        PUBLIC_DISCUSSION_REVIEW_FIXTURE.items.map((item) => [item.discussion_id, 'pending_review']),
      ),
    )
  }

  async function handleLoadProviderPublicDiscussion() {
    if (!providerDiscussionLoadAvailable || !liveCandidateContextKey) {
      setError('Accepted live candidate does not contain a valid YouTube watch URL.')
      return
    }

    invalidatePublicDiscussion()
    const requestEpoch = ++discussionRequestEpochRef.current
    const requestSearchEpoch = generatedSearchEpoch
    const requestContextKey = liveCandidateContextKey
    discussionContextKeyRef.current = requestContextKey
    const isCurrentRequest = () => discussionRequestEpochRef.current === requestEpoch &&
      searchRequestEpochRef.current === requestSearchEpoch &&
      discussionContextKeyRef.current === requestContextKey
    setPublicDiscussionLoading(true)
    setError('')
    setPublicDiscussionBatch(null)
    setPublicDiscussionDecisionById({})
    setPublicDiscussionSource(null)
    setPublicDiscussionAttachResult(null)
    try {
      const result = await getYouTubeOfficialApiLivePublicDiscussion(acceptedLiveVideoId, 3)
      if (!isCurrentRequest()) return
      if (result?.video_id !== acceptedLiveVideoId) {
        setError('The returned public discussion does not match the selected video. Use a new explicit request.')
        return
      }
      setPublicDiscussionBatch(result)
      setPublicDiscussionContextKey(requestContextKey)
      setPublicDiscussionSource('provider-backed')
      setPublicDiscussionDecisionById(
        Object.fromEntries(
          (result.items || []).map((item) => [item.discussion_id, 'pending_review']),
        ),
      )
    } catch {
      if (!isCurrentRequest()) return
      setError('Unable to load provider-backed public discussion.')
    } finally {
      if (isCurrentRequest()) setPublicDiscussionLoading(false)
    }
  }

  function setPublicDiscussionDecision(discussionId, decision) {
    reviewedAttachRequestEpochRef.current += 1
    setPublicDiscussionAttaching(false)
    setPublicDiscussionAttachResult(null)
    setPublicDiscussionDecisionById((current) => ({ ...current, [discussionId]: decision }))
  }

  async function handleAttachReviewedPublicDiscussion() {
    if (reviewedAttachPendingRef.current) return
    if (!publicDiscussionAttachAvailable || !acceptedLiveVideoId) {
      setError('Select a target case and accept one to three provider-backed comments before attaching.')
      return
    }

    setPublicDiscussionAttaching(true)
    reviewedAttachPendingRef.current = true
    setReviewedAttachPending(true)
    const requestEpoch = ++reviewedAttachRequestEpochRef.current
    const requestSearchEpoch = generatedSearchEpoch
    const requestDiscussionEpoch = discussionRequestEpochRef.current
    const requestContextKey = publicDiscussionContextKey
    const requestCaseId = liveTargetCaseId
    const requestQuery = generatedQuery
    const isCurrentRequest = () => reviewedAttachRequestEpochRef.current === requestEpoch &&
      searchRequestEpochRef.current === requestSearchEpoch &&
      discussionRequestEpochRef.current === requestDiscussionEpoch &&
      discussionContextKeyRef.current === requestContextKey
    setPublicDiscussionAttachResult(null)
    setError('')
    try {
      const result = await attachYouTubeOfficialApiReviewedPublicDiscussion(
        requestCaseId,
        acceptedLiveVideoId,
        {
          review_batch_safe_hash: publicDiscussionBatch.review_batch_safe_hash,
          selected_discussion_ids: acceptedPublicDiscussionIds,
          review_binding_mode: 'selected_item_v1',
          selected_discussion_safe_hashes: selectedDiscussionSafeHashes,
        },
      )
      if (!isCurrentRequest()) return
      if (result?.case_id !== requestCaseId || result?.video_id !== acceptedLiveVideoId) {
        setError('The attach receipt does not match its captured case and video. No retry or navigation.')
        return
      }
      const scope = scopeFromReviewedAttach(result, requestQuery, requestCaseId)
      if (scope) setGuidedAttachScope(scope)
      // Keep a safe immutable receipt for navigation, not the provider/Evidence body.
      setPublicDiscussionAttachResult(Object.freeze({
        case_id: requestCaseId, attached_discussion_count: result.attached_discussion_count,
        review_binding_mode: result.review_binding_mode,
        safe_mode: Object.freeze({ server_side_refetch: result.safe_mode?.server_side_refetch === true }),
        guided_scope: scope,
      }))
      const refreshedCase = await getAnalysisCase(requestCaseId)
      if (!isCurrentRequest()) return
      if (refreshedCase?.case_id !== requestCaseId) {
        setError('The persisted case readback does not match the attach receipt.')
        return
      }
      onCaseReady?.(refreshedCase)
      await onRefreshCases?.()
    } catch (requestError) {
      if (!isCurrentRequest()) return
      setError(requestError?.message || 'Unable to attach reviewed public discussion.')
    } finally {
      reviewedAttachPendingRef.current = false
      if (mountedRef.current) setReviewedAttachPending(false)
      if (isCurrentRequest()) setPublicDiscussionAttaching(false)
    }
  }

  async function handleAttachAcceptedCandidates() {
    if (liveBatchPreviewOnly) {
      setError('Live metadata leads cannot be attached through the generic candidate action.')
      return
    }
    if (!generatedBatchMatchesProvider) {
      setError('Generate a fresh offline candidate batch before attaching.')
      return
    }
    if (!targetCaseId) {
      setError('Select a target case before attaching candidates.')
      return
    }
    if (!acceptedCandidates.length) {
      setError('Accept at least one mock candidate before attaching.')
      return
    }
    setAttaching(true)
    setError('')
    try {
      const result = await attachSearchDiscoveryCandidates(targetCaseId, {
        candidates: acceptedCandidates,
        reviewer_label: 'local_demo_reviewer',
      })
      setAttachResult(result)
      setCandidateStatusById((current) => {
        const next = { ...current }
        acceptedCandidates.forEach((candidate) => {
          next[candidate.candidate_id] = 'attached'
        })
        return next
      })
      const refreshedCase = await getAnalysisCase(targetCaseId)
      onCaseReady?.(refreshedCase)
      await onRefreshCases?.()
    } catch (requestError) {
      setError(requestError?.message || 'Unable to attach Search Discovery candidates.')
    } finally {
      setAttaching(false)
    }
  }

  const columns = [
    {
      title: 'Candidate',
      dataIndex: 'title',
      key: 'title',
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Text strong>{record.title}</Text>
          <Text type="secondary">{record.snippet}</Text>
          <Space wrap size={4}>
            <Tag>{record.source_name}</Tag>
            <Tag color="cyan">{record.platform_hint}</Tag>
            <Tag color="blue">{record.content_type_hint}</Tag>
            <Tag>{Math.round(record.confidence * 100)}% confidence</Tag>
          </Space>
        </Space>
      ),
    },
    {
      title: 'URL metadata',
      dataIndex: 'url',
      key: 'url',
      width: 260,
      render: (url, record) => (
        <Space direction="vertical" size={4}>
          <Text copyable={{ text: url }} ellipsis>
            <LinkIcon size={13} /> {url}
          </Text>
          <Text type="secondary">{record.published_at || 'published_at unavailable'}</Text>
        </Space>
      ),
    },
    {
      title: 'Safety notes',
      dataIndex: 'safety_notes',
      key: 'safety_notes',
      width: 230,
      render: (notes) => (
        <Space wrap size={4}>
          {(notes || []).map((note) => (
            <Tag key={note} color={note.includes('not fetched') ? 'green' : 'default'}>
              {note}
            </Tag>
          ))}
        </Space>
      ),
    },
    {
      title: 'Review',
      dataIndex: 'status',
      key: 'status',
      width: 190,
      render: (status, record, candidateOrderIndex) => {
        const safeCandidateId = typeof record.candidate_id === 'string' &&
          /^[A-Za-z0-9_.:-]{1,256}$/.test(record.candidate_id) ? record.candidate_id : ''
        const safeVideoId = getYouTubeWatchVideoId(record.url) || ''
        const safeLocalStatus = ['pending_review', 'accepted', 'rejected'].includes(status) ? status : ''
        const currentContextValid = Boolean(
          generatedLiveBatchCurrent &&
          generatedProvider === LIVE_PROVIDER_ID &&
          normalizeDiscoveryQuery(record.query) === generatedQuery &&
          safeCandidateId &&
          safeVideoId,
        )
        return (
          <div
            data-testid="search-discovery-candidate-safe-binding"
            data-sentigraph-candidate-order-index={Number.isInteger(candidateOrderIndex) &&
              candidateOrderIndex >= 0 && candidateOrderIndex <= 4 ? candidateOrderIndex : ''}
            data-sentigraph-candidate-id={safeCandidateId}
            data-sentigraph-video-id={safeVideoId}
            data-sentigraph-local-status={safeLocalStatus}
            data-sentigraph-current-context-valid={currentContextValid ? 'true' : 'false'}
          >
        <Space direction="vertical" size={6}>
          <Tag color={STATUS_COLORS[status] || 'default'}>{status}</Tag>
          <Space>
            <Button
              size="small"
              icon={<CheckCircle2 size={14} />}
              data-testid="search-discovery-candidate-accept"
              onClick={() => setCandidateStatus(record.candidate_id, 'accepted')}
              disabled={status === 'attached'}
            >
              接受
            </Button>
            <Button
              size="small"
              danger
              icon={<XCircle size={14} />}
              data-testid="search-discovery-candidate-reject"
              onClick={() => setCandidateStatus(record.candidate_id, 'rejected')}
              disabled={status === 'attached'}
            >
              忽略
            </Button>
          </Space>
        </Space>
          </div>
        )
      },
    },
  ]

  return (
    <Space direction="vertical" size={18} className="full-width">
      <Card className="panel-card">
        <div className="panel-heading">
          <Space>
            <FileSearch size={20} />
            <div>
              <Title level={2}>Search Discovery / 搜索发现</Title>
              <Text type="secondary">
                {collectorSelected
                  ? 'Search already-produced local external collector export package summaries.'
                  : liveSelected
                  ? 'Intentional internal real YouTube Official API metadata search.'
                  : 'Mock-only candidate review for future all-web discovery workflows.'}
              </Text>
            </div>
          </Space>
          <Space wrap>
            <Tag color={collectorSelected ? 'gold' : liveSelected ? 'cyan' : 'purple'}>
              {collectorSelected ? 'External collector handoff lane' : liveSelected ? 'Real official-API metadata lane' : 'Offline/mock fixtures'}
            </Tag>
            {!collectorSelected ? <>
            <Tag color="purple">RSS/GDELT fixtures</Tag>
            <Tag color="purple">YouTube official-shaped offline fixture</Tag>
            {liveRouteFrontendEnabled ? (
              <Tag color="cyan">Guarded internal capability; readiness not established</Tag>
            ) : (
              <Tag color="green">No real search API</Tag>
            )}
            <Tag color="green">No URL fetch</Tag>
            <Tag color="green">No scraping</Tag>
            <Tag color="blue">Evidence metadata only</Tag>
            </> : <>
              <Tag>No collector job</Tag><Tag>No fresh package validation</Tag>
              <Tag>No Evidence ingestion</Tag><Tag>No full-web/full-platform coverage</Tag>
            </>}
          </Space>
        </div>
        {collectorSelected ? (
          <Alert
            type="warning"
            showIcon
            message="External collector handoff packages"
            description="Already-produced local exports only. Stored validation is not a fresh validation. Selected/available samples are not full-web/full-platform coverage or official truth verification. Human review required."
          />
        ) : provider === LIVE_PROVIDER_ID ? (
          <Alert
            type="warning"
            showIcon
            message="Internal real YouTube Official API metadata search"
            description={(
              <Space wrap size={6}>
                <Tag>Official API metadata only</Tag>
                <Tag>URL content not fetched</Tag>
                <Tag>Human review required</Tag>
                <Tag>Metadata lead only; official API provenance is not truth verification</Tag>
                <Tag>
                  {publicDiscussionAttachFrontendEnabled
                    ? 'Reviewed public comments may be attached through a separate guarded action'
                    : 'Attachment disabled in this phase'}
                </Tag>
                <Tag>Backend route remains independently gated</Tag>
              </Space>
            )}
          />
        ) : (
          <Alert
            type="info"
            showIcon
            message="Safe candidate-review scaffold"
            description="当前为模拟搜索发现，不调用真实搜索 API。系统不会自动抓取候选 URL 内容；接受候选只会保存 URL、标题、摘要等元数据，候选证据默认需要人工复核。"
          />
        )}
      </Card>

      {liveRouteFrontendEnabled && !backendLiveDescriptor ? (
        <Alert type="warning" showIcon message="Live search unavailable: backend capability descriptor is absent." />
      ) : null}
      {liveRouteFrontendEnabled && backendLiveDescriptor?.live_fetch_enabled !== true && backendLiveDescriptor ? (
        <Alert type="warning" showIcon message="Backend live search route is disabled; the live lane is unavailable." />
      ) : null}

      <Card className="panel-card">
        <Form layout="vertical">
          <Form.Item label="Discovery lane / 发现入口">
            <Select
              value={provider}
              onChange={handleProviderChange}
              options={providerOptions}
              placeholder="Select a discovery lane"
            />
          </Form.Item>
          <Form.Item label="Keyword / Event query">
            <Input
              value={query}
              onChange={(event) => handleQueryChange(event.target.value)}
              maxLength={120}
              placeholder="Tesla"
            />
          </Form.Item>
          {!collectorSelected ? <Form.Item label="Target case">
            <Select
              showSearch
              value={effectiveTargetCaseId || undefined}
              onChange={handleTargetCaseChange}
              options={caseOptions}
              placeholder="Select a case"
              optionFilterProp="label"
            />
          </Form.Item> : null}
          <Space wrap>
            {!collectorSelected ? <Button
              loading={creatingCase}
              disabled={creatingCase || !buildGuidedCaseCreatePayload(query, liveSelected)}
              onClick={handleCreateCaseFromQuery}
            >Create case from query</Button> : null}
            {liveSelected && currentCase?.case_id ? <Button
              onClick={() => handleTargetCaseChange(currentCase.case_id)}
            >Use opened current case</Button> : null}
            <Button
              type="primary"
              icon={<RefreshCw size={16} />}
              loading={loading}
              disabled={(liveSelected && !liveSearchAvailable) || (collectorSelected && !collectorAvailable)}
              onClick={handleGenerateCandidates}
            >
              {collectorSelected
                ? 'Search external collector handoff packages'
                : provider === LIVE_PROVIDER_ID
                ? 'Search YouTube Official API metadata / 搜索官方 API 元数据'
                : 'Generate mock candidates / 生成模拟候选'}
            </Button>
            {!collectorSelected ? <>
            <Button
              icon={<ShieldCheck size={16} />}
              loading={attaching}
              disabled={
                liveSelected || liveBatchPreviewOnly ||
                !generatedBatchMatchesProvider ||
                !acceptedCount ||
                !targetCaseId
              }
              onClick={handleAttachAcceptedCandidates}
            >
              Attach accepted to case / 附加到案例
            </Button>
            <Button
              icon={<PlayCircle size={16} />}
              disabled={
                liveSelected || liveBatchPreviewOnly ||
                !attachResult?.attached_candidate_count ||
                !targetCaseId
              }
              onClick={() => onRunCase?.(targetCaseId, 'analysis')}
            >
              Run analysis after attach
            </Button>
            </> : null}
          </Space>
        </Form>
        {error ? <Alert className="section-alert" type="error" showIcon message={error} /> : null}
        {createNotice ? <Alert type="success" showIcon message={createNotice} /> : null}
        {liveSelected && !liveTargetCaseId ? <Alert type="info"
          message="Choose an existing case explicitly, adopt the opened current case, or create a draft from this query. No case is selected automatically for live attachment." /> : null}
      </Card>

      {guidedAttachScope && publicDiscussionAttachResult?.guided_scope !== guidedAttachScope ? (
        <Card size="small" className="panel-card" data-testid="last-guided-attach-scope">
          <Space direction="vertical">
            <Text>Last completed attach receipt: case={guidedAttachScope.case_id} · query={guidedAttachScope.query}</Text>
            <Text type="secondary">This receipt remains bound to its original case and Evidence IDs despite current query/target changes.</Text>
            <Button disabled={!onOpenGuidedEvidenceReview}
              onClick={() => onOpenGuidedEvidenceReview?.(guidedAttachScope)}>Open Evidence review</Button>
          </Space>
        </Card>
      ) : null}

      {!collectorSelected ? <Card className="panel-card">
        <div className="panel-heading">
          <Space>
            <ShieldCheck size={18} />
            <Title level={4}>Provider status</Title>
          </Space>
          <Space wrap>
            <Tag color="purple">{selectedProviderStatus?.provider_type || provider}</Tag>
            <Tag color="blue">{selectedProviderStatus?.status || 'mock_only'}</Tag>
            {provider === LIVE_PROVIDER_ID ? (
              <>
                <Tag color="cyan">frontend_gate={String(liveRouteFrontendEnabled)}</Tag>
                <Tag color="gold">backend_route_enabled={String(backendLiveDescriptor?.live_fetch_enabled === true)}</Tag>
                <Tag>Credentials not checked; provider availability not established</Tag>
              </>
            ) : (
              <Tag color="green">live_fetch_enabled=false</Tag>
            )}
            <Tag color="green">candidate metadata only</Tag>
            <Tag color="green">No URL content extraction</Tag>
            <Tag color="gold">full_content=false</Tag>
          </Space>
        </div>
        <Paragraph type="secondary">
          {provider === LIVE_PROVIDER_ID
            ? `${selectedProviderStatus?.display_name || 'Unavailable live lane'} · One explicit internal metadata search requests at most five candidates. Enablement is not credential/provider readiness. URL content is not fetched. Generic metadata attachment is disabled; public discussion review requires its separate gates and a current query/lane selection.`
            : `${selectedProviderStatus?.display_name || 'Selected provider'} · RSS/GDELT and the Phase-1 YouTube official-shaped response are offline fixtures. Future real providers may return URL/title/snippet metadata only; full content extraction requires a separate reviewed public parser, official API route, licensed vendor payload, or user-provided text.`}
        </Paragraph>
        <Space wrap size={6}>
          {(selectedProviderStatus?.safety_notes || [
            'Mock/static only',
            'No live fetching',
            'No URL content extraction',
            'Candidate metadata requires review',
          ]).map((note) => (
            <Tag key={note}>{note}</Tag>
          ))}
        </Space>
      </Card> : null}

      {collectorSelected || collectorBatch ? (
        <Card className="panel-card" data-testid="external-collector-discovery-panel">
          <Title level={4}>External Collector Handoff / 外部抓取包交接</Title>
          <Paragraph>Package-level metadata results, not Search Discovery candidates. No Evidence attach or analysis action.</Paragraph>
          <Alert
            type={collectorBatch && !collectorBatchCurrent ? 'warning' : 'info'}
            message={collectorBatch
              ? `${collectorBatchCurrent ? 'Current' : 'Historical'} external collector package results for query: ${generatedCollectorQuery}`
              : 'Use one explicit collector package search to begin.'}
            description="Stored validation is not fresh. Already-produced local export; selected/available sample only, not full-web/full-platform coverage, not official truth verification. Human review required."
          />
          {collectorBatch?.results?.length ? collectorBatch.results.map((item) => (
            <Card key={item.package_name} size="small" data-testid="external-collector-package-result">
              <Space direction="vertical" size={6}>
                <Text strong>{item.case_title || item.package_name}</Text>
                <Text>{item.package_name}</Text>
                <Text>Case: {item.case_id || 'unavailable'}</Text>
                <Space wrap>
                  <Tag>provenance=external_collector_handoff</Tag>
                  <Tag>role={item.package_role || 'unknown'}</Tag>
                  <Tag>Stored validation: {item.validation_status}</Tag>
                  <Tag>exported={item.exported_at || 'unavailable'}</Tag>
                  <Tag>evidence={item.evidence_count}</Tag><Tag>sources={item.source_count}</Tag>
                  <Tag>comments={item.comment_count}</Tag><Tag>roots={item.root_count}</Tag>
                  <Tag>{item.sample_quality_label || 'sample quality not established'}</Tag>
                  <Tag>next={item.recommended_next_action}</Tag>
                  <Tag>recommended demo={String(item.recommended_for_sentigraph_demo)}</Tag>
                  <Tag>matched fields: {(item.matched_fields || []).join(', ')}</Tag>
                  {(item.sample_labels || []).map((label) => <Tag key={label}>{label}</Tag>)}
                </Space>
              </Space>
            </Card>
          )) : <Empty description={collectorBatch
            ? `No matching external collector packages for query: ${generatedCollectorQuery}`
            : 'No collector discovery has been requested.'} />}
        </Card>
      ) : null}

      {publicDiscussionReviewFrontendEnabled && !collectorSelected ? (
        <Card className="panel-card" data-testid="public-discussion-review-panel">
          <div className="panel-heading">
            <Space>
              <FileSearch size={18} />
              <div>
                <Title level={4}>Public Discussion Review / 公开讨论复核</Title>
                <Text type="secondary">
                  Synthetic fixtures and gated provider-backed comments for transient human review only.
                </Text>
              </div>
            </Space>
            <Space wrap>
              <Button type="primary" onClick={handleLoadPublicDiscussionFixture}>
                Load synthetic public discussion fixture / 加载模拟讨论
              </Button>
              {providerDiscussionLoadAvailable ? (
                <Button
                  data-testid="search-discovery-provider-discussion-load"
                  loading={publicDiscussionLoading}
                  onClick={handleLoadProviderPublicDiscussion}
                >
                  Load provider-backed public discussion / 加载官方 API 公开讨论
                </Button>
              ) : null}
            </Space>
          </div>

          {publicDiscussionSource === 'provider-backed' ? (
            <Alert
              className="section-alert"
              type="warning"
              showIcon
              message="Official API public comments / provider-backed review"
              description={(
                <Space wrap size={6}>
                  <Tag>Top-level comments only</Tag>
                  <Tag>Author identity omitted</Tag>
                  <Tag>Reply content not acquired</Tag>
                  <Tag>Human review required</Tag>
                  <Tag>
                    {publicDiscussionAttachFrontendEnabled
                      ? 'Human-selected comments may become case Evidence'
                      : 'No Evidence persistence'}
                  </Tag>
                  <Tag>No analysis run</Tag>
                  <Tag>Provider transport is not truth verification</Tag>
                </Space>
              )}
            />
          ) : (
            <Alert
              className="section-alert"
              type="warning"
              showIcon
              message="Synthetic fixture only"
              description={(
                <Space wrap size={6}>
                  <Tag>No provider request</Tag>
                  <Tag>Human review required</Tag>
                  <Tag>No Evidence persistence</Tag>
                  <Tag>No analysis run</Tag>
                </Space>
              )}
            />
          )}

          {publicDiscussionBatch ? (
            <div
              data-testid="public-discussion-safe-batch-binding"
              data-sentigraph-video-id={typeof publicDiscussionBatch.video_id === 'string' &&
                /^[A-Za-z0-9_-]{11}$/.test(publicDiscussionBatch.video_id) ? publicDiscussionBatch.video_id : ''}
              data-sentigraph-review-batch-safe-hash={typeof publicDiscussionBatch.review_batch_safe_hash === 'string' &&
                /^[0-9a-f]{64}$/.test(publicDiscussionBatch.review_batch_safe_hash) ?
                publicDiscussionBatch.review_batch_safe_hash : ''}
              data-sentigraph-provider-backed={publicDiscussionSource === 'provider-backed' ? 'true' : 'false'}
            >
            <Space direction="vertical" size={12} className="full-width">
              <Space wrap>
                <Tag color="purple">items={publicDiscussionBatch.item_count}</Tag>
                <Tag color="blue">video_id={publicDiscussionBatch.video_id}</Tag>
                <Tag>generated_at={publicDiscussionBatch.generated_at}</Tag>
                <Tag color="green">reply_content_acquired=false</Tag>
                {publicDiscussionBatch.review_batch_safe_hash ? (
                  <Tag color="cyan">review batch bound</Tag>
                ) : null}
              </Space>
              {publicDiscussionBatch.items.map((item) => {
                const localDecision = publicDiscussionDecisionById[item.discussion_id] || 'pending_review'
                const safeDiscussionId = typeof item.discussion_id === 'string' &&
                  /^[A-Za-z0-9_.:-]{1,256}$/.test(item.discussion_id) ? item.discussion_id : ''
                const safeCommentId = typeof item.comment_id === 'string' &&
                  /^[A-Za-z0-9_.:-]{1,256}$/.exec(item.comment_id)?.[0] === item.comment_id ? item.comment_id : ''
                const selectedItemSafeHash = publicDiscussionBatch.review_item_safe_hashes?.[item.discussion_id]
                const safeSelectedItemHash = typeof selectedItemSafeHash === 'string' &&
                  /^[0-9a-f]{64}$/.test(selectedItemSafeHash) ? selectedItemSafeHash : ''
                const safeLocalDecision = ['pending_review', 'accepted', 'rejected'].includes(localDecision) ?
                  localDecision : ''
                return (
                  <Card
                    key={item.discussion_id}
                    size="small"
                    data-testid="public-discussion-review-item"
                  >
                    <div
                      data-testid="public-discussion-safe-item-binding"
                      data-sentigraph-discussion-id={safeDiscussionId}
                      data-sentigraph-comment-id={safeCommentId}
                      data-sentigraph-selected-item-safe-hash={safeSelectedItemHash}
                      data-sentigraph-local-decision={safeLocalDecision}
                    >
                    <Space direction="vertical" size={8} className="full-width">
                      <Text>{item.body_text}</Text>
                      <Space wrap size={4}>
                        <Tag>{item.provider}</Tag>
                        <Tag color="cyan">{item.platform_hint}</Tag>
                        <Tag>{item.comment_id}</Tag>
                        <Tag>{item.published_at}</Tag>
                        <Tag>likes={item.like_count}</Tag>
                        <Tag>replies={item.reply_count}</Tag>
                        <Tag color="gold">schema status={item.status}</Tag>
                        <Tag
                          color={STATUS_COLORS[localDecision] || 'default'}
                          data-testid={`public-discussion-decision-${item.discussion_id}`}
                        >
                          local decision={localDecision}
                        </Tag>
                      </Space>
                      <Space wrap size={4}>
                        {item.safety_notes.map((note) => (
                          <Tag key={note}>{note}</Tag>
                        ))}
                      </Space>
                      <Space>
                        <Button
                          size="small"
                          icon={<CheckCircle2 size={14} />}
                          aria-label={`Accept ${item.discussion_id}`}
                          onClick={() => setPublicDiscussionDecision(item.discussion_id, 'accepted')}
                        >
                          Accept / 接受
                        </Button>
                        <Button
                          size="small"
                          danger
                          icon={<XCircle size={14} />}
                          aria-label={`Reject ${item.discussion_id}`}
                          onClick={() => setPublicDiscussionDecision(item.discussion_id, 'rejected')}
                        >
                          Reject / 拒绝
                        </Button>
                      </Space>
                    </Space>
                    </div>
                  </Card>
                )
              })}
              {publicDiscussionAttachFrontendEnabled && publicDiscussionSource === 'provider-backed' ? (
                <Space wrap>
                  <Button
                    type="primary"
                    icon={<ShieldCheck size={16} />}
                    data-testid="public-discussion-attach-reviewed"
                    loading={publicDiscussionAttaching}
                    disabled={!publicDiscussionAttachAvailable}
                    onClick={handleAttachReviewedPublicDiscussion}
                  >
                    Attach reviewed public discussion to case
                  </Button>
                  <Text type="secondary">
                    Select one to three accepted comments and a target case. The server refetches the bounded batch;
                    browser text is not authoritative.
                  </Text>
                </Space>
              ) : null}
              {publicDiscussionAttachResult ? (
                <Card size="small" data-testid="public-discussion-attach-result">
                  <Space direction="vertical" size={8} className="full-width">
                    <Space wrap>
                      <Tag color="cyan">case={publicDiscussionAttachResult.case_id}</Tag>
                      <Tag color="green">
                        attached={publicDiscussionAttachResult.attached_discussion_count}
                      </Tag>
                      <Tag color="purple">acquisition_mode=official_api_public</Tag>
                      <Tag color="blue">provenance=official_api</Tag>
                      <Tag color="gold">analysis_run=false</Tag>
                      <Tag color="cyan">binding={publicDiscussionAttachResult.review_binding_mode}</Tag>
                      {publicDiscussionAttachResult.safe_mode?.server_side_refetch === true ? (
                        <Tag color="green">server-side refetch; selected binding confirmed</Tag>
                      ) : null}
                    </Space>
                    <Text type="secondary">
                      Human-selected public comments are attached to the existing case. Official API provenance is
                      transport provenance, not truth verification.
                    </Text>
                    <Text strong>
                      Attached to case-local Evidence. Review the persisted Evidence before any explicit analysis.
                    </Text>
                    <Button
                      disabled={!publicDiscussionAttachResult.guided_scope || !onOpenGuidedEvidenceReview || reviewedAttachPending}
                      onClick={() => onOpenGuidedEvidenceReview?.(publicDiscussionAttachResult.guided_scope)}
                    >Open Evidence review</Button>
                  </Space>
                </Card>
              ) : null}
            </Space>
            </div>
          ) : (
            <Empty description="Use one explicit load action to begin local review." />
          )}
        </Card>
      ) : null}

      {!collectorSelected ? <>
      <div className="metric-grid">
        <Card className="metric-card">
          <Statistic title="Candidates" value={candidates.length} />
        </Card>
        <Card className="metric-card">
          <Statistic title="Accepted" value={acceptedCount} />
        </Card>
        <Card className="metric-card">
          <Statistic title="Rejected" value={rejectedCount} />
        </Card>
        <Card className="metric-card">
          <Statistic
            title="Attached evidence"
            value={
              publicDiscussionAttachResult?.attached_discussion_count ||
              attachResult?.attached_candidate_count ||
              0
            }
          />
        </Card>
      </div>

      <Card className="panel-card">
        <div className="panel-heading">
          <Space>
            <FileSearch size={18} />
            <Title level={4}>Candidate review list</Title>
          </Space>
          <Text type="secondary">Users must later supplement full text/comments or route sources through a compliant parser.</Text>
        </div>
        {liveBatchPreviewOnly ? (
          <Alert
            type={generatedLiveBatchCurrent ? 'info' : 'warning'}
            message={`${generatedLiveBatchCurrent ? 'Current' : 'Historical'} real official-API metadata batch for query: ${generatedQuery}`}
            description="Metadata leads only; human review required. URL content not fetched; API transport provenance is not claim-truth verification. Historical results cannot load discussion for a changed query/lane."
          />
        ) : null}
        {candidates.length ? (
          <Table
            rowKey="candidate_id"
            dataSource={candidates}
            columns={columns}
            pagination={false}
          />
        ) : (
          <Empty description={liveBatchPreviewOnly
            ? `No official API metadata candidates returned for query: ${generatedQuery}`
            : liveSelected
              ? 'Click the explicit official API search action to begin.'
              : 'Generate offline/mock candidates to start the review flow.'} />
        )}
      </Card>
      </> : null}

      {!collectorSelected && attachResult ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <Title level={4}>Attach result</Title>
            <Space wrap>
              <Tag color="green">attached={attachResult.attached_candidate_count}</Tag>
              <Tag color="gold">skipped={attachResult.skipped_candidate_count}</Tag>
              <Tag color="red">rejected={attachResult.rejected_candidate_count}</Tag>
              <Tag color="purple">acquisition_mode=search_discovery</Tag>
              <Tag color="blue">provenance=search_discovery_candidate</Tag>
            </Space>
          </div>
          <Paragraph type="secondary">
            Accepted candidates are stored as normalized EvidenceItems with conservative trust labels and review-needed
            warnings. URL content was not fetched.
          </Paragraph>
          <Space direction="vertical" className="full-width">
            {(attachResult.attached_evidence_items || []).map((item) => (
              <div className="evidence-preview-row" key={item.evidence_id}>
                <Space direction="vertical" size={4}>
                  <Text strong>{item.title || item.evidence_id}</Text>
                  <Text type="secondary">{item.body_text || item.comment_text || item.url}</Text>
                  <Space wrap size={4}>
                    <Tag>{item.acquisition_mode}</Tag>
                    <Tag>{item.provenance_type}</Tag>
                    <Tag color="gold">{item.verification_status}</Tag>
                    <Tag color="purple">{item.review_status}</Tag>
                  </Space>
                </Space>
              </div>
            ))}
          </Space>
        </Card>
      ) : null}
    </Space>
  )
}
