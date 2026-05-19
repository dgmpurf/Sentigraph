import { useMemo, useState } from 'react'
import { Alert, Button, Card, DatePicker, Form, Input, InputNumber, List, Select, Space, Tag, Typography } from 'antd'
import { Database, PlayCircle, RadioTower, Search } from 'lucide-react'
import { createCase, crawlCaseRawData, getCase, runCase } from '../api/sentigraphApi.js'

const { RangePicker } = DatePicker
const { Text, Title } = Typography

const YOUTUBE_REAL_LIMIT_MAX = 5

const DEFAULT_PLATFORM_OPTIONS = [
  { label: 'Reddit', value: 'reddit' },
  { label: 'Weibo', value: 'weibo' },
]

const PLATFORM_GROUPS = [
  {
    key: 'mock_selectable',
    title: 'MVP mock-selectable platforms',
    description: 'Enabled for offline mock analysis only. These selections do not call real platform APIs.',
    color: 'cyan',
    filter: (platform) => platform.selectable_for_mock,
  },
  {
    key: 'official_api_planned',
    title: 'Official API planned platforms',
    description: 'Visible in the roadmap and selectable only for mock analysis until credentials are available.',
    color: 'blue',
    filter: (platform) => platform.category === 'official_api_planned',
  },
  {
    key: 'future_real_adapter_candidate',
    title: 'Future real adapter candidates',
    description: 'Potential future real adapters after compliance and API design review.',
    color: 'geekblue',
    filter: (platform) => platform.category === 'future_real_adapter_candidate',
  },
  {
    key: 'crawler_later',
    title: 'Crawler-later platforms',
    description: 'Future crawler integration',
    color: 'gold',
    filter: (platform) => platform.category === 'crawler_later',
  },
  {
    key: 'disabled_or_optional_future',
    title: 'Disabled or optional future platforms',
    description: 'Not active in the current MVP roadmap.',
    color: 'default',
    filter: (platform) => platform.category === 'disabled_or_optional_future',
  },
]

function getPlatformGroups(platformRegistry) {
  return PLATFORM_GROUPS.map((group) => ({
    ...group,
    platforms: platformRegistry.filter(group.filter),
  }))
}

function getPlatformStatusTags(platform, groupColor) {
  const tags = []
  if (platform.selectable_for_mock && platform.mock_available) {
    tags.push({ key: 'mock', color: 'green', label: 'Mock 可用' })
  }
  if (platform.api_pending || platform.api_approval_status === 'api_pending') {
    tags.push({ key: 'api_pending', color: 'orange', label: 'API 待审批' })
  }
  if (platform.category === 'official_api_planned') {
    tags.push({ key: 'official', color: 'blue', label: '官方 API 规划中' })
  }
  if (platform.category === 'crawler_later') {
    tags.push({ key: 'crawler_later', color: 'gold', label: '未来公开页面解析' })
  }
  if (platform.category === 'disabled_or_optional_future' || platform.real_mode_disabled) {
    tags.push({
      key: 'disabled',
      color: platform.selectable_for_mock ? 'default' : 'red',
      label: platform.selectable_for_mock ? '真实采集关闭' : '暂不启用',
    })
  }
  if (!tags.length) {
    tags.push({ key: 'status', color: groupColor, label: platform.status || '规划中' })
  }
  return tags
}

function getCredentialEntries(platform) {
  const credentialsPresent = platform.credentials_present
  if (!credentialsPresent || typeof credentialsPresent !== 'object') return []
  return Object.entries(credentialsPresent).map(([name, present]) => ({
    name,
    present: Boolean(present),
  }))
}

function PlatformRoadmap({ platformRegistry }) {
  if (!platformRegistry?.length) {
    return (
      <Card className="panel-card">
        <div className="panel-heading">
          <Title level={4}>Platform Roadmap</Title>
          <Text type="secondary">Backend platform registry is unavailable. Mock fallback choices are shown.</Text>
        </div>
      </Card>
    )
  }

  const mockSelectableCount = platformRegistry.filter((platform) => platform.selectable_for_mock && platform.mock_available).length
  const apiPendingCount = platformRegistry.filter((platform) => platform.api_pending || platform.api_approval_status === 'api_pending').length
  const realSelectableCount = platformRegistry.filter((platform) => platform.selectable_for_real && platform.real_mode_available).length

  return (
    <Card className="panel-card">
      <div className="panel-heading">
        <div>
          <Title level={4}>Data Sources / Platform Status</Title>
          <Text type="secondary">Selection is mock-first. No real crawler or third-party API call is triggered.</Text>
        </div>
      </div>
      <div className="platform-status-summary">
        <Tag color="green">Mock 可用 {mockSelectableCount}</Tag>
        <Tag color="orange">API 待审批 {apiPendingCount}</Tag>
        <Tag color={realSelectableCount ? 'cyan' : 'default'}>真实可选 {realSelectableCount}</Tag>
      </div>
      <div className="platform-roadmap-grid">
        {getPlatformGroups(platformRegistry).map((group) => (
          <div className="platform-group" key={group.key}>
            <div className="platform-group-header">
              <Text strong>{group.title}</Text>
              <Text type="secondary">{group.description}</Text>
            </div>
            <div className="platform-list">
              {group.platforms.length ? (
                group.platforms.map((platform) => (
                  <div className="platform-item" key={`${group.key}-${platform.platform_id}`}>
                    <Space size={6} wrap>
                      <Tag color={group.color}>{platform.display_name}</Tag>
                      {getPlatformStatusTags(platform, group.color).map((tag) => (
                        <Tag color={tag.color} key={tag.key}>{tag.label}</Tag>
                      ))}
                    </Space>
                    {getCredentialEntries(platform).length ? (
                      <div className="platform-credentials">
                        {getCredentialEntries(platform).map((credential) => (
                          <Text className="platform-credential" key={credential.name} type="secondary">
                            {credential.name}: {credential.present ? '已配置' : '缺失'}
                          </Text>
                        ))}
                      </div>
                    ) : null}
                    <Text className="platform-note" type="secondary">
                      {platform.notes}
                    </Text>
                  </div>
                ))
              ) : (
                <Text type="secondary">No platforms in this group.</Text>
              )}
            </div>
          </div>
        ))}
      </div>
    </Card>
  )
}

function normalizeDateRange(dateRange) {
  if (!dateRange?.length) return { start: '2026-05-01', end: '2026-05-13' }
  return {
    start: dateRange[0].format('YYYY-MM-DD'),
    end: dateRange[1].format('YYYY-MM-DD'),
  }
}

function normalizeSelectedPlatforms(platforms) {
  if (!Array.isArray(platforms)) return []
  return platforms.map((platform) => String(platform || '').toLowerCase()).filter(Boolean)
}

function getSafeYoutubeLimit(limit) {
  const numericLimit = Number(limit)
  if (!Number.isFinite(numericLimit)) return 3
  return Math.min(YOUTUBE_REAL_LIMIT_MAX, Math.max(1, Math.floor(numericLimit)))
}

function getYoutubeMetadata(caseDetail) {
  const crawlMetadata = Array.isArray(caseDetail?.crawl_metadata) ? caseDetail.crawl_metadata : []
  return crawlMetadata.find((item) => item?.platform === 'youtube') || crawlMetadata[0] || {}
}

function getDisplayValue(value) {
  if (value === true) return 'true'
  if (value === false) return 'false'
  if (value === null || value === undefined || value === '') return 'n/a'
  return String(value)
}

function getRepresentativeComments(caseDetail) {
  const candidateLists = [
    caseDetail?.report?.representative_comments,
    caseDetail?.analysis_result?.representative_comments,
    caseDetail?.report?.top_comments,
    caseDetail?.analysis_result?.top_comments,
  ]
  const comments = candidateLists.find((items) => Array.isArray(items) && items.length) || []
  return comments
    .map((comment) => {
      if (typeof comment === 'string') return comment
      if (!comment || typeof comment !== 'object') return ''
      return comment.content || comment.text || comment.comment || comment.summary || ''
    })
    .filter(Boolean)
    .slice(0, 3)
}

function MetadataGrid({ items }) {
  return (
    <div className="platform-status-summary">
      {items.map((item) => (
        <Tag color={item.color || 'geekblue'} key={item.label}>
          {item.label}: {getDisplayValue(item.value)}
        </Tag>
      ))}
    </div>
  )
}

export function KeywordSearch({
  expandedKeywords,
  initialPlatforms = ['reddit', 'weibo'],
  loading,
  onCaseReady,
  onNavigate,
  onStartAnalysis,
  platformOptions = DEFAULT_PLATFORM_OPTIONS,
  platformRegistry = [],
}) {
  const [form] = Form.useForm()
  const watchedPlatforms = Form.useWatch('platforms', form)
  const [youtubeFlow, setYoutubeFlow] = useState({
    loadingStep: '',
    error: '',
    createdCase: null,
    attachedCase: null,
    completedCase: null,
  })

  const selectOptions = [{ label: 'MVP mock-selectable platforms', options: platformOptions }]
  const selectedPlatforms = normalizeSelectedPlatforms(watchedPlatforms || initialPlatforms)
  const youtubeOnly = selectedPlatforms.length === 1 && selectedPlatforms[0] === 'youtube'
  const youtubeMixed = selectedPlatforms.includes('youtube') && !youtubeOnly
  const youtubeCase = youtubeFlow.completedCase || youtubeFlow.attachedCase || youtubeFlow.createdCase
  const youtubeMetadata = useMemo(() => getYoutubeMetadata(youtubeFlow.attachedCase || youtubeFlow.completedCase), [
    youtubeFlow.attachedCase,
    youtubeFlow.completedCase,
  ])
  const representativeComments = getRepresentativeComments(youtubeFlow.completedCase)

  const handleFinish = (values) => {
    onStartAnalysis({
      title: values.title,
      keyword: values.keyword,
      platforms: values.platforms,
      language: values.language,
      limit: values.limit,
      date_range: normalizeDateRange(values.date_range),
    })
  }

  const updateCaseState = async (caseDetail, patch = {}) => {
    if (caseDetail) {
      await onCaseReady?.(caseDetail)
    }
    setYoutubeFlow((current) => ({
      ...current,
      ...patch,
      loadingStep: '',
      error: '',
    }))
  }

  const handleYoutubeCreateCase = async () => {
    const values = form.getFieldsValue()
    setYoutubeFlow((current) => ({ ...current, loadingStep: 'create', error: '' }))
    try {
      const createdCase = await createCase({
        title: values.title || 'YouTube Real Data Case',
        keyword: values.keyword || 'Tesla',
        platforms: ['youtube'],
        report_language: 'zh-CN',
      })
      await updateCaseState(createdCase, {
        createdCase,
        attachedCase: null,
        completedCase: null,
      })
    } catch (requestError) {
      setYoutubeFlow((current) => ({
        ...current,
        loadingStep: '',
        error: requestError?.message || 'Unable to create the YouTube real-data case.',
      }))
    }
  }

  const handleYoutubeCrawlAttach = async () => {
    if (!youtubeFlow.createdCase?.case_id) {
      setYoutubeFlow((current) => ({ ...current, error: 'Create a YouTube case before crawling.' }))
      return
    }
    const values = form.getFieldsValue()
    setYoutubeFlow((current) => ({ ...current, loadingStep: 'crawl', error: '' }))
    try {
      const attachedCase = await crawlCaseRawData(youtubeFlow.createdCase.case_id, {
        limit: getSafeYoutubeLimit(values.limit),
      })
      await updateCaseState(attachedCase, {
        createdCase: attachedCase,
        attachedCase,
        completedCase: null,
      })
    } catch (requestError) {
      setYoutubeFlow((current) => ({
        ...current,
        loadingStep: '',
        error: requestError?.message || 'Unable to crawl and attach YouTube raw data.',
      }))
    }
  }

  const handleYoutubeRunCase = async () => {
    const caseId = youtubeFlow.attachedCase?.case_id || youtubeFlow.createdCase?.case_id
    if (!caseId) {
      setYoutubeFlow((current) => ({ ...current, error: 'Create and attach raw data before running analysis.' }))
      return
    }
    setYoutubeFlow((current) => ({ ...current, loadingStep: 'run', error: '' }))
    try {
      const completedCase = await runCase(caseId)
      const refreshedCase = await getCase(caseId).catch(() => completedCase)
      await updateCaseState(refreshedCase, {
        createdCase: refreshedCase,
        attachedCase: refreshedCase,
        completedCase: refreshedCase,
      })
    } catch (requestError) {
      setYoutubeFlow((current) => ({
        ...current,
        loadingStep: '',
        error: requestError?.message || 'Unable to run analysis for the YouTube real-data case.',
      }))
    }
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Keyword Search</Title>
          <Text>Start a mock monitoring project with selected public platforms.</Text>
        </div>
      </div>

      <Card className="panel-card form-panel">
        <Form
          form={form}
          layout="vertical"
          initialValues={{ keyword: 'Tesla', platforms: initialPlatforms, language: 'auto', limit: 100 }}
          onFinish={handleFinish}
        >
          <div className="form-grid">
            <Form.Item label="Case Title" name="title">
              <Input size="large" placeholder="Optional, for example Tesla product risk watch" />
            </Form.Item>
            <Form.Item
              label="Keyword"
              name="keyword"
              rules={[{ required: true, message: 'Enter one keyword to analyze.' }]}
            >
              <Input size="large" placeholder="Tesla, product name, public figure..." />
            </Form.Item>
            <Form.Item label="Platforms" name="platforms" rules={[{ required: true }]}>
              <Select
                mode="multiple"
                size="large"
                options={selectOptions}
                placeholder="Select mock-enabled MVP platforms"
              />
            </Form.Item>
            <Form.Item label="Date Range" name="date_range">
              <RangePicker size="large" className="full-width" />
            </Form.Item>
            <Form.Item label="Limit" name="limit">
              <InputNumber size="large" min={10} max={1000} step={10} className="full-width" />
            </Form.Item>
            <Form.Item label="Language" name="language">
              <Select
                size="large"
                options={[
                  { label: 'Auto', value: 'auto' },
                  { label: 'English', value: 'en' },
                  { label: 'Chinese', value: 'zh' },
                ]}
              />
            </Form.Item>
          </div>
          <Button type="primary" htmlType="submit" icon={<Search size={17} />} loading={loading} size="large">
            Create Case & Run Mock Analysis
          </Button>
        </Form>
      </Card>

      {youtubeMixed ? (
        <Alert
          showIcon
          type="warning"
          message="For YouTube real-data demo, select YouTube only."
          description="Multi-platform selections remain available for the offline mock flow. The real-data case flow is intentionally explicit so crawl, attach, and analysis steps are visible."
        />
      ) : null}

      {youtubeOnly ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <div>
              <Title level={4}>YouTube Real-Data Case Flow</Title>
              <Text type="secondary">
                Create a YouTube-only case, attach tiny-limit public YouTube data, then run offline deterministic analysis.
              </Text>
            </div>
          </div>
          <Space size={[8, 8]} wrap>
            <Tag color="red">Data: YouTube Real</Tag>
            <Tag color="green">Analysis: Offline</Tag>
            <Tag color="purple">LLM: Mock</Tag>
            <Tag color="default">API key values are never displayed</Tag>
          </Space>

          <Space className="section-actions" wrap>
            <Button
              icon={<Database size={16} />}
              loading={youtubeFlow.loadingStep === 'create'}
              onClick={handleYoutubeCreateCase}
              type="default"
            >
              Create YouTube Real Case
            </Button>
            <Button
              disabled={!youtubeFlow.createdCase?.case_id}
              icon={<RadioTower size={16} />}
              loading={youtubeFlow.loadingStep === 'crawl'}
              onClick={handleYoutubeCrawlAttach}
              type="default"
            >
              Crawl YouTube & Attach Raw Data
            </Button>
            <Button
              disabled={!youtubeFlow.attachedCase?.case_id}
              icon={<PlayCircle size={16} />}
              loading={youtubeFlow.loadingStep === 'run'}
              onClick={handleYoutubeRunCase}
              type="primary"
            >
              Run Case Analysis
            </Button>
          </Space>

          {youtubeFlow.error ? (
            <Alert className="app-alert" showIcon type="error" message={youtubeFlow.error} />
          ) : null}

          {youtubeCase ? (
            <div className="platform-group">
              <Text strong>Current YouTube case</Text>
              <MetadataGrid
                items={[
                  { label: 'case_id', value: youtubeCase.case_id, color: 'cyan' },
                  { label: 'raw_data_status', value: youtubeCase.raw_data_status, color: 'green' },
                  { label: 'raw_post_count', value: youtubeCase.raw_post_count ?? youtubeMetadata.post_count },
                  { label: 'raw_comment_count', value: youtubeCase.raw_comment_count ?? youtubeMetadata.comment_count },
                ]}
              />
            </div>
          ) : null}

          {youtubeFlow.attachedCase ? (
            <div className="platform-group">
              <Text strong>YouTube crawl attachment metadata</Text>
              <MetadataGrid
                items={[
                  { label: 'adapter_mode', value: youtubeMetadata.adapter_mode, color: 'blue' },
                  { label: 'fallback_used', value: youtubeMetadata.fallback_used, color: youtubeMetadata.fallback_used ? 'orange' : 'green' },
                  { label: 'fallback_reason_category', value: youtubeMetadata.fallback_reason_category, color: youtubeMetadata.fallback_used ? 'orange' : 'default' },
                  { label: 'cache_hit', value: youtubeMetadata.cache_hit, color: youtubeMetadata.cache_hit ? 'green' : 'default' },
                  { label: 'quota_guardrail_status', value: youtubeMetadata.quota_guardrail_status, color: 'geekblue' },
                ]}
              />
              {youtubeMetadata.fallback_used ? (
                <Alert
                  showIcon
                  type="warning"
                  message="YouTube crawl used a safe fallback."
                  description={`fallback_used=true; fallback_reason_category=${getDisplayValue(youtubeMetadata.fallback_reason_category)}. No credentials or secret values are shown.`}
                />
              ) : null}
            </div>
          ) : null}

          {youtubeFlow.completedCase ? (
            <div className="platform-group">
              <Text strong>Offline analysis result</Text>
              <MetadataGrid
                items={[
                  {
                    label: 'analysis_input_source',
                    value: youtubeFlow.completedCase.analysis_result?.analysis_input_source,
                    color: 'cyan',
                  },
                  {
                    label: 'raw_post_count',
                    value: youtubeFlow.completedCase.analysis_result?.raw_post_count ?? youtubeFlow.completedCase.raw_post_count,
                  },
                  {
                    label: 'raw_comment_count',
                    value: youtubeFlow.completedCase.analysis_result?.raw_comment_count ?? youtubeFlow.completedCase.raw_comment_count,
                  },
                ]}
              />
              <List
                bordered
                dataSource={representativeComments}
                header={<Text strong>Representative comments preview</Text>}
                locale={{ emptyText: 'No representative comments available yet.' }}
                renderItem={(comment) => (
                  <List.Item>
                    <Text>{comment}</Text>
                  </List.Item>
                )}
                size="small"
              />
              <Space className="section-actions" wrap>
                <Button onClick={() => onNavigate?.('analysis')} type="primary">
                  Open Analysis Result
                </Button>
                <Button onClick={() => onNavigate?.('summary')}>Open Summary Report</Button>
                <Button onClick={() => onNavigate?.('risk')}>Open Risk Monitor</Button>
                <Button onClick={() => onNavigate?.('simulationLab')}>Open Simulation Lab</Button>
              </Space>
            </div>
          ) : null}
        </Card>
      ) : null}

      <PlatformRoadmap platformRegistry={platformRegistry} />

      {expandedKeywords ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <Title level={4}>Expanded Keywords</Title>
            <Text>{expandedKeywords.original_keyword}</Text>
          </div>
          <Space wrap>
            {expandedKeywords.expanded_keywords.map((keyword) => (
              <Tag color="cyan" key={keyword}>
                {keyword}
              </Tag>
            ))}
          </Space>
          <div className="query-strip">
            {expandedKeywords.search_queries.map((query) => (
              <Text code key={query}>
                {query}
              </Text>
            ))}
          </div>
        </Card>
      ) : null}
    </div>
  )
}
