import { Alert, Button, Card, Empty, Form, Input, Select, Space, Statistic, Table, Tag, Typography } from 'antd'
import { CheckCircle2, FileSearch, LinkIcon, PlayCircle, RefreshCw, ShieldCheck, XCircle } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import {
  attachSearchDiscoveryCandidates,
  getAnalysisCase,
  getMockSearchDiscoveryCandidates,
  getSearchDiscoveryProviders,
  getYouTubeOfficialApiLiveCandidates,
  getYouTubeOfficialApiLivePublicDiscussion,
  getYouTubeOfficialApiMockCandidates,
} from '../api/sentigraphApi.js'
import { PUBLIC_DISCUSSION_REVIEW_FIXTURE } from '../fixtures/publicDiscussionReviewFixture.js'

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
const LIVE_PROVIDER_OPTION = Object.freeze({
  value: LIVE_PROVIDER_ID,
  label: 'YouTube Official API — guarded live preview',
})
const LIVE_PROVIDER_STATUS = Object.freeze({
  provider_id: LIVE_PROVIDER_ID,
  provider_type: LIVE_PROVIDER_ID,
  display_name: LIVE_PROVIDER_OPTION.label,
  status: 'guarded_live_preview',
  safety_notes: Object.freeze([
    'Official API metadata only',
    'URL content not fetched',
    'Human review required',
    'Attachment disabled in this phase',
  ]),
})

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
  liveRouteFrontendEnabled =
    import.meta.env.VITE_SENTIGRAPH_SEARCH_DISCOVERY_YOUTUBE_LIVE_ENABLED === '1',
  publicDiscussionReviewFrontendEnabled =
    import.meta.env.VITE_SENTIGRAPH_SEARCH_DISCOVERY_PUBLIC_DISCUSSION_REVIEW_ENABLED === '1',
}) {
  const [query, setQuery] = useState('Tesla')
  const [provider, setProvider] = useState('mock_static')
  const [providers, setProviders] = useState([])
  const [targetCaseId, setTargetCaseId] = useState(currentCase?.case_id || '')
  const [batch, setBatch] = useState(null)
  const [generatedProvider, setGeneratedProvider] = useState(null)
  const [candidateStatusById, setCandidateStatusById] = useState({})
  const [loading, setLoading] = useState(false)
  const [attaching, setAttaching] = useState(false)
  const [attachResult, setAttachResult] = useState(null)
  const [publicDiscussionBatch, setPublicDiscussionBatch] = useState(null)
  const [publicDiscussionDecisionById, setPublicDiscussionDecisionById] = useState({})
  const [publicDiscussionLoading, setPublicDiscussionLoading] = useState(false)
  const [publicDiscussionSource, setPublicDiscussionSource] = useState(null)
  const [error, setError] = useState('')

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
    if (targetCaseId) return
    if (currentCase?.case_id) {
      setTargetCaseId(currentCase.case_id)
    } else if (!targetCaseId && cases[0]?.case_id) {
      setTargetCaseId(cases[0].case_id)
    }
  }, [cases, currentCase, targetCaseId])

  const caseOptions = useMemo(
    () =>
      cases.map((item) => ({
        value: item.case_id,
        label: `${item.title || item.keyword || item.case_id} · ${item.case_id}`,
      })),
    [cases],
  )

  const providerOptions = useMemo(() => {
    const options = providers
      .filter((item) => MOCK_PROVIDER_TYPES.includes(item.provider_type || item.provider_id))
      .map((item) => ({
        value: item.provider_id,
        label: item.display_name || item.provider_id,
      }))
    const offlineOptions = options.length ? options : FALLBACK_PROVIDER_OPTIONS
    return liveRouteFrontendEnabled
      ? [...offlineOptions, LIVE_PROVIDER_OPTION]
      : offlineOptions
  }, [liveRouteFrontendEnabled, providers])

  const selectedProviderStatus = useMemo(() => {
    if (provider === LIVE_PROVIDER_ID) return LIVE_PROVIDER_STATUS
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
  const generatedBatchMatchesProvider = Boolean(generatedProvider) && generatedProvider === provider
  const acceptedLiveCandidate = liveBatchPreviewOnly && generatedBatchMatchesProvider
    ? acceptedCandidates[0] || null
    : null
  const acceptedLiveVideoId = getYouTubeWatchVideoId(acceptedLiveCandidate?.url)
  const providerDiscussionLoadAvailable = Boolean(
    liveRouteFrontendEnabled &&
    publicDiscussionReviewFrontendEnabled &&
    acceptedLiveCandidate &&
    acceptedLiveVideoId,
  )

  async function handleGenerateCandidates() {
    setLoading(true)
    setError('')
    setAttachResult(null)
    setPublicDiscussionBatch(null)
    setPublicDiscussionDecisionById({})
    setPublicDiscussionSource(null)
    try {
      const result = provider === LIVE_PROVIDER_ID
        ? await getYouTubeOfficialApiLiveCandidates(query, 1)
        : provider === 'youtube_official_api'
          ? await getYouTubeOfficialApiMockCandidates(query, 5)
          : await getMockSearchDiscoveryCandidates(query, provider)
      setBatch(result)
      setGeneratedProvider(provider)
      setCandidateStatusById(
        Object.fromEntries((result.candidates || []).map((candidate) => [candidate.candidate_id, 'pending_review'])),
      )
    } catch (requestError) {
      setError(requestError?.message || 'Unable to generate mock Search Discovery candidates.')
    } finally {
      setLoading(false)
    }
  }

  function setCandidateStatus(candidateId, status) {
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
    setError('')
    setPublicDiscussionBatch(PUBLIC_DISCUSSION_REVIEW_FIXTURE)
    setPublicDiscussionSource('synthetic')
    setPublicDiscussionDecisionById(
      Object.fromEntries(
        PUBLIC_DISCUSSION_REVIEW_FIXTURE.items.map((item) => [item.discussion_id, 'pending_review']),
      ),
    )
  }

  async function handleLoadProviderPublicDiscussion() {
    if (!providerDiscussionLoadAvailable || !acceptedLiveVideoId) {
      setError('Accepted live candidate does not contain a valid YouTube watch URL.')
      return
    }

    setPublicDiscussionLoading(true)
    setError('')
    setPublicDiscussionBatch(null)
    setPublicDiscussionDecisionById({})
    setPublicDiscussionSource(null)
    try {
      const result = await getYouTubeOfficialApiLivePublicDiscussion(acceptedLiveVideoId, 3)
      setPublicDiscussionBatch(result)
      setPublicDiscussionSource('provider-backed')
      setPublicDiscussionDecisionById(
        Object.fromEntries(
          (result.items || []).map((item) => [item.discussion_id, 'pending_review']),
        ),
      )
    } catch {
      setError('Unable to load provider-backed public discussion.')
    } finally {
      setPublicDiscussionLoading(false)
    }
  }

  function setPublicDiscussionDecision(discussionId, decision) {
    setPublicDiscussionDecisionById((current) => ({ ...current, [discussionId]: decision }))
  }

  async function handleAttachAcceptedCandidates() {
    if (liveBatchPreviewOnly) {
      setError('Guarded live candidates are preview-only and cannot be attached in this phase.')
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
      render: (status, record) => (
        <Space direction="vertical" size={6}>
          <Tag color={STATUS_COLORS[status] || 'default'}>{status}</Tag>
          <Space>
            <Button
              size="small"
              icon={<CheckCircle2 size={14} />}
              onClick={() => setCandidateStatus(record.candidate_id, 'accepted')}
              disabled={status === 'attached'}
            >
              接受
            </Button>
            <Button
              size="small"
              danger
              icon={<XCircle size={14} />}
              onClick={() => setCandidateStatus(record.candidate_id, 'rejected')}
              disabled={status === 'attached'}
            >
              忽略
            </Button>
          </Space>
        </Space>
      ),
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
                {liveRouteFrontendEnabled
                  ? 'Offline review with a disabled-by-default guarded live metadata preview.'
                  : 'Mock-only candidate review for future all-web discovery workflows.'}
              </Text>
            </div>
          </Space>
          <Space wrap>
            <Tag color="purple">Mock/static only</Tag>
            <Tag color="purple">RSS/GDELT fixtures</Tag>
            <Tag color="purple">YouTube official-shaped offline fixture</Tag>
            {liveRouteFrontendEnabled ? (
              <Tag color="cyan">Guarded live preview option exposed</Tag>
            ) : (
              <Tag color="green">No real search API</Tag>
            )}
            <Tag color="green">No URL fetch</Tag>
            <Tag color="green">No scraping</Tag>
            <Tag color="blue">Evidence metadata only</Tag>
          </Space>
        </div>
        {provider === LIVE_PROVIDER_ID ? (
          <Alert
            type="warning"
            showIcon
            message="Guarded live metadata preview"
            description={(
              <Space wrap size={6}>
                <Tag>Official API metadata only</Tag>
                <Tag>URL content not fetched</Tag>
                <Tag>Human review required</Tag>
                <Tag>Attachment disabled in this phase</Tag>
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

      <Card className="panel-card">
        <Form layout="vertical">
          <Form.Item label="Discovery provider / 发现来源">
            <Select
              value={provider}
              onChange={setProvider}
              options={providerOptions}
              placeholder="Select a mock provider"
            />
          </Form.Item>
          <Form.Item label="Keyword / Event query">
            <Input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              maxLength={120}
              placeholder="Tesla"
            />
          </Form.Item>
          <Form.Item label="Target case">
            <Select
              showSearch
              value={targetCaseId || undefined}
              onChange={setTargetCaseId}
              options={caseOptions}
              placeholder="Select a case"
              optionFilterProp="label"
            />
          </Form.Item>
          <Space wrap>
            <Button
              type="primary"
              icon={<RefreshCw size={16} />}
              loading={loading}
              onClick={handleGenerateCandidates}
            >
              {provider === LIVE_PROVIDER_ID
                ? 'Generate guarded live preview / 生成受控实时预览'
                : 'Generate mock candidates / 生成模拟候选'}
            </Button>
            <Button
              icon={<ShieldCheck size={16} />}
              loading={attaching}
              disabled={
                liveBatchPreviewOnly ||
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
                liveBatchPreviewOnly ||
                !attachResult?.attached_candidate_count ||
                !targetCaseId
              }
              onClick={() => onRunCase?.(targetCaseId, 'analysis')}
            >
              Run analysis after attach
            </Button>
          </Space>
        </Form>
        {error ? <Alert className="section-alert" type="error" showIcon message={error} /> : null}
      </Card>

      <Card className="panel-card">
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
                <Tag color="cyan">frontend_preview_option=true</Tag>
                <Tag color="gold">backend_route_independently_gated=true</Tag>
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
            ? `${selectedProviderStatus.display_name} · This local UI choice can request one guarded metadata preview only when the independently gated backend route is available. It does not fetch URL content, attach Evidence, or start analysis.`
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
      </Card>

      {publicDiscussionReviewFrontendEnabled ? (
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
                  <Tag>No Evidence persistence</Tag>
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
            <Space direction="vertical" size={12} className="full-width">
              <Space wrap>
                <Tag color="purple">items={publicDiscussionBatch.item_count}</Tag>
                <Tag color="blue">video_id={publicDiscussionBatch.video_id}</Tag>
                <Tag>generated_at={publicDiscussionBatch.generated_at}</Tag>
                <Tag color="green">reply_content_acquired=false</Tag>
              </Space>
              {publicDiscussionBatch.items.map((item) => {
                const localDecision = publicDiscussionDecisionById[item.discussion_id] || 'pending_review'
                return (
                  <Card
                    key={item.discussion_id}
                    size="small"
                    data-testid="public-discussion-review-item"
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
                  </Card>
                )
              })}
            </Space>
          ) : (
            <Empty description="Use one explicit load action to begin local review." />
          )}
        </Card>
      ) : null}

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
          <Statistic title="Attached evidence" value={attachResult?.attached_candidate_count || 0} />
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
        {candidates.length ? (
          <Table
            rowKey="candidate_id"
            dataSource={candidates}
            columns={columns}
            pagination={false}
          />
        ) : (
          <Empty description="Generate mock candidates to start the review flow." />
        )}
      </Card>

      {attachResult ? (
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
