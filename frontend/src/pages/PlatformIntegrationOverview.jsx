import { Alert, Button, Card, Col, Empty, List, Row, Skeleton, Space, Table, Tag, Typography } from 'antd'
import { Database, Eye, FileSearch, Globe2, RefreshCw, ShieldCheck } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  getPlatforms,
  getPlatformReadiness,
  getPlatformStatus,
  getPublicParserStatus,
  getSearchDiscoveryStatus,
  getSourceCatalog,
  previewPublicParser,
} from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const groupLabels = {
  realReady: 'Real Ready',
  configuredGuarded: 'Configured but Guarded',
  permissionPending: 'Permission Pending',
  oauthPending: 'OAuth Pending',
  mockScaffoldOnly: 'Mock / Scaffold Only',
  official: '官方 API 规划平台',
  publicParser: '公开页面解析平台',
  reddit: 'Reddit 状态',
  future: '暂不启用 / 未来可选',
}

const statusTone = {
  api_pending: 'orange',
  official_api_planned: 'blue',
  fixture_only: 'cyan',
  future_crawler_integration: 'gold',
  disabled_optional_future: 'default',
  disabled_or_optional_future: 'default',
  real_api_available_when_configured: 'green',
  approval_pending: 'orange',
  oauth_pending: 'purple',
  credential_missing: 'gold',
  adapter_mode_mock: 'blue',
  item_comment_not_verified: 'purple',
  company_age_requirement_pending: 'orange',
  comment_api_unknown_or_not_confirmed: 'orange',
}

const feasibilityTone = {
  green: 'green',
  yellow: 'gold',
  red: 'red',
}

function safeText(value, fallback = '-') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function boolTag(value, trueText = '是', falseText = '否') {
  return <Tag color={value ? 'green' : 'default'}>{value ? trueText : falseText}</Tag>
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString('zh-CN', { hour12: false })
}

function formatNumber(value, suffix = '') {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? `${numericValue}${suffix}` : '-'
}

function formatList(values, fallback = '-') {
  if (!Array.isArray(values) || values.length === 0) return fallback
  return values.map((value) => String(value)).join(', ')
}

function schemaTag(valid) {
  return <Tag color={valid ? 'green' : 'red'}>{valid ? '通过' : '异常'}</Tag>
}

function getCredentialEntries(platform) {
  const credentialsPresent = platform?.credentials_present
  if (!credentialsPresent || typeof credentialsPresent !== 'object') return []
  return Object.entries(credentialsPresent).map(([name, present]) => ({
    name,
    present: Boolean(present),
  }))
}

function getStatusBadges(platform = {}, parser = null) {
  const badges = []
  if (platform.mock_available) {
    badges.push({ key: 'mock_available', color: 'green', label: 'Mock 可用' })
  }
  if (platform.real_mode_configured && platform.selectable_for_real) {
    badges.push({ key: 'real_ready', color: 'green', label: 'Real Ready' })
  }
  if (platform.platform_id === 'youtube' && platform.real_mode_available && !platform.real_mode_configured) {
    badges.push({ key: 'configured_guarded', color: 'blue', label: 'Real-capable / Guarded' })
  }
  if (platform.oauth_required || platform.oauth_status === 'oauth_pending') {
    badges.push({ key: 'oauth_pending', color: 'purple', label: 'OAuth Pending' })
  }
  if (platform.real_mode_blocker === 'approval_pending' || platform.scope_status === 'approval_pending') {
    badges.push({ key: 'approval_pending', color: 'orange', label: 'Permission Pending' })
  }
  if (platform.status === 'api_pending' || platform.api_approval_status === 'api_pending') {
    badges.push({ key: 'api_pending', color: 'orange', label: 'API 待接入' })
  }
  if (platform.status === 'official_api_planned' || platform.category === 'official_api_planned') {
    badges.push({ key: 'official_api_planned', color: 'blue', label: 'API 待接入' })
  }
  if (parser?.parser_status === 'fixture_only' || platform.status === 'fixture_only') {
    badges.push({ key: 'fixture_only', color: 'cyan', label: 'Fixture Only' })
  }
  if (parser && !parser.live_fetch_enabled) {
    badges.push({ key: 'live_fetch_disabled', color: 'default', label: 'Live 关闭' })
  }
  if (platform.category === 'disabled_or_optional_future') {
    badges.push({ key: 'disabled_or_optional_future', color: 'default', label: '暂不启用' })
  }
  if (platform.real_mode_available === false) {
    badges.push({ key: 'real_mode_unavailable', color: 'default', label: '真实模式未启用' })
  }
  if (!badges.length && platform.status) {
    badges.push({
      key: 'status',
      color: statusTone[platform.status] || 'default',
      label: platform.status,
    })
  }

  const seen = new Set()
  return badges.filter((badge) => {
    if (seen.has(badge.key)) return false
    seen.add(badge.key)
    return true
  })
}

function PlatformNameCell({ record }) {
  return (
    <Space direction="vertical" size={3} className="full-width">
      <Text strong>{safeText(record.display_name || record.platform_id)}</Text>
      <Text type="secondary">{safeText(record.platform_id)}</Text>
      <Space size={4} wrap>
        <Tag color="geekblue">{safeText(record.category)}</Tag>
        <Tag>{safeText(record.source_type)}</Tag>
      </Space>
    </Space>
  )
}

function StatusBadgeRow({ platform, parser }) {
  return (
    <Space wrap size={4}>
      {getStatusBadges(platform, parser).map((badge) => (
        <Tag color={badge.color} key={badge.key}>
          {badge.label}
        </Tag>
      ))}
    </Space>
  )
}

function CredentialStatus({ platform }) {
  const entries = getCredentialEntries(platform)
  if (!entries.length) {
    return <Tag color="default">无需凭证</Tag>
  }

  return (
    <div className="integration-credential-list">
      {entries.map((credential) => (
        <Text className="integration-credential" key={credential.name} type="secondary">
          {credential.name}: {credential.present ? '已配置' : '缺失'}
        </Text>
      ))}
    </div>
  )
}

function RegistrySafetyFields({ platform }) {
  return (
    <Space wrap size={4} className="integration-safe-field-tags">
      <Tag color="geekblue">integration: {safeText(platform.integration_type)}</Tag>
      <Tag color={statusTone[platform.status] || 'default'}>status: {safeText(platform.status)}</Tag>
      <Tag color={platform.mock_available ? 'green' : 'default'}>
        {platform.mock_available ? 'Mock 可用' : 'Mock 不可用'}
      </Tag>
      <Tag color={platform.real_mode_available ? 'green' : 'default'}>
        {platform.real_mode_available ? '真实模式可用' : '真实模式未启用'}
      </Tag>
      <Tag color={platform.real_mode_configured ? 'green' : 'default'}>
        configured: {platform.real_mode_configured ? 'yes' : 'no'}
      </Tag>
      <Tag color={platform.api_approval_required ? 'orange' : 'default'}>
        API 审批: {platform.api_approval_required ? '需要' : '不需要'}
      </Tag>
      <Tag>{safeText(platform.api_approval_status, 'not_applicable')}</Tag>
      <Tag color={statusTone[platform.scope_status] || 'default'}>
        scope: {safeText(platform.scope_status)}
      </Tag>
      <Tag color={platform.oauth_required ? 'purple' : 'default'}>
        OAuth: {platform.oauth_required ? safeText(platform.oauth_status, 'required') : 'not_required'}
      </Tag>
      {platform.real_mode_blocker ? (
        <Tag color={statusTone[platform.real_mode_blocker] || 'orange'}>
          blocker: {platform.real_mode_blocker}
        </Tag>
      ) : null}
      <Tag color={platform.enabled_in_mvp ? 'green' : 'default'}>
        MVP: {platform.enabled_in_mvp ? '启用' : '未启用'}
      </Tag>
      <Tag color={platform.selectable_for_mock ? 'green' : 'default'}>
        Mock: {platform.selectable_for_mock ? '可选' : '不可选'}
      </Tag>
      <Tag color={platform.selectable_for_real ? 'green' : 'default'}>
        Real: {platform.selectable_for_real ? '可选' : '不可选'}
      </Tag>
      <Tag>{safeText(platform.data_access_level)}</Tag>
      {platform.quota_cache_protected ? <Tag color="cyan">quota/cache protected</Tag> : null}
    </Space>
  )
}

function ReadinessDetails({ platform }) {
  return (
    <Space direction="vertical" size={4} className="full-width">
      <Text type="secondary">凭证：{platform.credential_present ? '已配置必要凭证' : '未完整配置必要凭证'}</Text>
      <Text type="secondary">Required credentials: {formatList(platform.required_credentials || platform.credentials_required)}</Text>
      <Text type="secondary">Required scopes: {formatList(platform.required_scopes, 'not_required')}</Text>
      <Text type="secondary">Blocker: {safeText(platform.real_mode_blocker, 'none')}</Text>
      <Text type="secondary">Next: {safeText(platform.next_user_action)}</Text>
    </Space>
  )
}

function SamplePostList({ posts = [] }) {
  if (!posts.length) {
    return <Empty description="暂无 sample_posts" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <List
      className="parser-sample-list"
      dataSource={posts}
      renderItem={(post) => (
        <List.Item>
          <div className="parser-sample-card">
            <Space direction="vertical" size={8} className="full-width">
              <Space wrap>
                <Tag color="cyan">{safeText(post.platform, 'unknown')}</Tag>
                <Text type="secondary">{safeText(post.post_id)}</Text>
              </Space>
              <Text strong>{safeText(post.title, 'Untitled public post')}</Text>
              <Paragraph ellipsis={{ rows: 3 }} className="parser-sample-content">
                {safeText(post.content, '暂无正文预览')}
              </Paragraph>
              <Space wrap>
                <Text type="secondary">作者/来源：{safeText(post.author_name || post.author_id)}</Text>
                <Text type="secondary">时间：{formatDate(post.created_at)}</Text>
                <Text type="secondary">
                  互动：{formatNumber(post.like_count)} likes / {formatNumber(post.reply_count)} replies
                </Text>
              </Space>
            </Space>
          </div>
        </List.Item>
      )}
    />
  )
}

function SampleCommentList({ comments = [] }) {
  if (!comments.length) {
    return <Empty description="暂无 sample_comments" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <List
      className="parser-sample-list"
      dataSource={comments}
      renderItem={(comment) => (
        <List.Item>
          <div className="parser-comment-card">
            <Space direction="vertical" size={7} className="full-width">
              <Space wrap>
                <Tag>{safeText(comment.platform, 'unknown')}</Tag>
                <Text strong>{safeText(comment.author_name || comment.author_id, 'anonymous')}</Text>
                <Text type="secondary">{formatDate(comment.created_at)}</Text>
              </Space>
              <Paragraph ellipsis={{ rows: 2 }} className="parser-sample-content">
                {safeText(comment.content, '暂无评论内容')}
              </Paragraph>
              <Text type="secondary">
                comment_id: {safeText(comment.comment_id)} · likes: {formatNumber(comment.like_count)}
              </Text>
            </Space>
          </div>
        </List.Item>
      )}
    />
  )
}

function PreviewPanel({ loading, preview, selectedPlatform }) {
  if (loading && !preview) {
    return <Skeleton active paragraph={{ rows: 8 }} title />
  }

  if (!preview) {
    return (
      <Empty
        description="点击公开页面解析平台的预览按钮。前端固定发送 use_live_fetch=false。"
        image={Empty.PRESENTED_IMAGE_SIMPLE}
      />
    )
  }

  const warnings = Array.isArray(preview.warnings) ? preview.warnings : []

  return (
    <Space direction="vertical" className="full-width" size={16}>
      <div className="parser-preview-summary integration-preview-summary">
        <div>
          <Text type="secondary">平台</Text>
          <Text strong>{safeText(preview.platform || selectedPlatform)}</Text>
        </div>
        <div>
          <Text type="secondary">Post / Comment</Text>
          <Text strong>{formatNumber(preview.post_count)} / {formatNumber(preview.comment_count)}</Text>
        </div>
        <div>
          <Text type="secondary">回退原因</Text>
          <Space size={4} wrap>
            <Tag color={preview.fallback_used ? 'gold' : 'green'}>
              {preview.fallback_used ? 'fallback_used=true' : 'fallback_used=false'}
            </Tag>
            <Tag>{safeText(preview.fallback_reason_category)}</Tag>
          </Space>
        </div>
        <div>
          <Text type="secondary">Schema 校验</Text>
          <Space size={4} wrap>
            {schemaTag(preview.raw_post_schema_valid !== false)}
            {schemaTag(preview.raw_comment_schema_valid !== false)}
          </Space>
        </div>
      </div>

      {warnings.length ? (
        <Alert
          type="warning"
          showIcon
          message="预览提示"
          description={
            <Space wrap>
              {warnings.map((warning) => (
                <Tag color="orange" key={warning}>
                  {warning}
                </Tag>
              ))}
            </Space>
          }
        />
      ) : null}

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card parser-preview-card" title="sample_posts">
            <SamplePostList posts={preview.sample_posts || []} />
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card parser-preview-card" title="sample_comments">
            <SampleCommentList comments={preview.sample_comments || []} />
          </Card>
        </Col>
      </Row>
    </Space>
  )
}

function MetricCards({ platforms, publicParsers, summary }) {
  const officialCount = platforms.filter((platform) => platform.category === 'official_api_planned').length
  const oauthPendingCount = platforms.filter((platform) => platform.oauth_required || platform.oauth_status === 'oauth_pending').length
  const realSelectableCount = summary?.real_selectable_count ?? platforms.filter((platform) => platform.selectable_for_real).length

  return (
    <Row gutter={[16, 16]}>
      <Col span={6}>
        <Card className="metric-card integration-metric-card">
          <Space className="metric-heading">
            <Globe2 size={18} />
            <Text>总平台数</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_platforms || platforms.length)}</Title>
          <Text type="secondary">来自平台 readiness/status 的安全展示字段。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card integration-metric-card">
          <Space className="metric-heading">
            <FileSearch size={18} />
            <Text>官方 API 规划</Text>
          </Space>
          <Title level={2}>{officialCount}</Title>
          <Text type="secondary">YouTube real-capable；其他官方源仍为权限/实现待验证。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card integration-metric-card">
          <Space className="metric-heading">
            <Database size={18} />
            <Text>公开页面解析</Text>
          </Space>
          <Title level={2}>{publicParsers.length}</Title>
          <Text type="secondary">Fixture-first，前端不启用 live fetch。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card integration-metric-card">
          <Space className="metric-heading">
            <ShieldCheck size={18} />
            <Text>真实可选</Text>
          </Space>
          <Title level={2}>{formatNumber(realSelectableCount)}</Title>
          <Text type="secondary">OAuth pending：{oauthPendingCount}；所有凭证只显示布尔状态。</Text>
        </Card>
      </Col>
    </Row>
  )
}

function ExplanationCards() {
  const items = [
    {
      key: 'youtube',
      title: 'YouTube',
      color: 'green',
      text: '官方 Data API v3 已接入为 real-capable，只有本地 .env 同时配置 real mode 和 API key 时才可真实调用，并受缓存/配额保护。',
    },
    {
      key: 'douyin',
      title: 'Douyin',
      color: 'purple',
      text: 'Web App 开发者访问已记录，但 OAuth、item.comment、redirect URI、白名单和 item_id 来源仍待控制台验证。',
    },
    {
      key: 'safety',
      title: 'Safety',
      color: 'cyan',
      text: '页面只展示非秘密 readiness 字段；不展示 API key、token、.env 值，不启用抓取或真实 LLM。',
    },
  ]

  return (
    <Row gutter={[16, 16]}>
      {items.map((item) => (
        <Col span={8} key={item.key}>
          <Card className="panel-card integration-explanation-card">
            <Space direction="vertical" size={9} className="full-width">
              <Tag color={item.color}>{item.title}</Tag>
              <Text>{item.text}</Text>
            </Space>
          </Card>
        </Col>
      ))}
    </Row>
  )
}

function SourceCatalogPanel({ catalog }) {
  const categories = Array.isArray(catalog?.categories) ? catalog.categories : []
  const safeMode = catalog?.safe_mode || {}
  const thirdPartyCrawlerName = ['Media', 'Crawler'].join('')

  return (
    <Card className="panel-card integration-section-card">
      <div className="panel-heading">
        <Space>
          <FileSearch size={18} />
          <Title level={4}>Source Catalog / Evidence Sources</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">{formatNumber(catalog?.total_categories || categories.length)} categories</Tag>
          <Tag color="geekblue">{formatNumber(catalog?.total_sources || 0)} sources</Tag>
          <Tag color={safeMode.static_metadata_only ? 'green' : 'red'}>static metadata only</Tag>
          <Tag color={safeMode.real_api_calls ? 'red' : 'green'}>no real API calls</Tag>
          <Tag color={safeMode.secrets_exposed ? 'red' : 'green'}>no secrets</Tag>
          <Tag color={safeMode.third_party_crawler_integrated ? 'red' : 'green'}>
            {thirdPartyCrawlerName} not integrated
          </Tag>
        </Space>
      </div>
      <Paragraph type="secondary" className="integration-table-note">
        Source Catalog is a planning layer for event-centered evidence. It shows what can become normalized
        EvidenceItem records; it does not crawl, use cookies, bypass captcha or anti-bot systems, fetch URLs,
        read credentials, or call real LLMs.
      </Paragraph>
      {categories.length ? (
        <div className="integration-tile-grid">
          {categories.map((category) => (
            <div className="integration-tile" key={category.category_id}>
              <Space direction="vertical" size={8} className="full-width">
                <div className="integration-tile-header">
                  <Space direction="vertical" size={2}>
                    <Text strong>{category.display_name}</Text>
                    <Text type="secondary">{category.category_id}</Text>
                  </Space>
                  <Tag>{category.sources.length}</Tag>
                </div>
                <Paragraph className="integration-note" ellipsis={{ rows: 2 }}>
                  {category.description}
                </Paragraph>
                <Space wrap size={[4, 4]}>
                  {category.sources.map((source) => (
                    <Tag color={feasibilityTone[source.feasibility_status] || 'default'} key={source.source_id}>
                      {source.display_name}: {source.feasibility_status} / {source.current_status}
                    </Tag>
                  ))}
                </Space>
                <Space wrap size={[4, 4]}>
                  {[...new Set(category.sources.flatMap((source) => source.acquisition_modes || []))]
                    .slice(0, 5)
                    .map((mode) => (
                      <Tag color="blue" key={mode}>
                        {mode}
                      </Tag>
                    ))}
                </Space>
              </Space>
            </div>
          ))}
        </div>
      ) : (
        <Empty description="Source Catalog metadata is unavailable." image={Empty.PRESENTED_IMAGE_SIMPLE} />
      )}
    </Card>
  )
}

function SearchDiscoveryStatusPanel({ status }) {
  const providers = Array.isArray(status?.provider_statuses) ? status.provider_statuses : []
  const safeMode = status?.safe_mode || {}

  return (
    <Card className="panel-card integration-section-card">
      <div className="panel-heading">
        <Space>
          <FileSearch size={18} />
          <Title level={4}>Search Discovery / URL Candidate Planning</Title>
        </Space>
        <Space wrap>
          <Tag color="purple">{safeText(status?.status, 'planning_mock_only')}</Tag>
          <Tag color="cyan">{providers.length} providers</Tag>
          <Tag color={safeMode.mock_candidates_only ? 'green' : 'default'}>mock/static only</Tag>
          <Tag color={safeMode.real_search_api_calls ? 'red' : 'green'}>no real search API</Tag>
          <Tag color={safeMode.url_fetching ? 'red' : 'green'}>no URL fetch</Tag>
          <Tag color={safeMode.scraping ? 'red' : 'green'}>no scraping</Tag>
        </Space>
      </div>
      <Paragraph type="secondary" className="integration-table-note">
        Search Discovery is planned as candidate URL/title/snippet discovery. It is not crawling: users must
        review candidates before attaching text as Manual URL evidence or routing a source to a reviewed public parser.
      </Paragraph>
      <Row gutter={[16, 16]}>
        <Col span={15}>
          {providers.length ? (
            <div className="integration-tile-grid">
              {providers.map((provider) => (
                <div className="integration-tile" key={provider.provider_id}>
                  <Space direction="vertical" size={7} className="full-width">
                    <div className="integration-tile-header">
                      <Space direction="vertical" size={2}>
                        <Text strong>{provider.display_name}</Text>
                        <Text type="secondary">{provider.provider_class}</Text>
                      </Space>
                      <Tag color={provider.status === 'available_now' ? 'green' : 'gold'}>
                        {provider.status}
                      </Tag>
                    </div>
                    <Space wrap size={4}>
                      <Tag>{provider.requires_api_key ? 'API key later' : 'No key required'}</Tag>
                      <Tag color={provider.credential_present ? 'green' : 'default'}>
                        credential_present={String(provider.credential_present)}
                      </Tag>
                      <Tag color={provider.user_review_required ? 'purple' : 'default'}>
                        review_required={String(provider.user_review_required)}
                      </Tag>
                      <Tag color={provider.full_content_available ? 'orange' : 'default'}>
                        full_content={String(provider.full_content_available)}
                      </Tag>
                    </Space>
                    <Text type="secondary">Data: {formatList(provider.data_returned)}</Text>
                    <Paragraph className="integration-note" ellipsis={{ rows: 2 }}>
                      {provider.next_action}
                    </Paragraph>
                  </Space>
                </div>
              ))}
            </div>
          ) : (
            <Empty description="Search Discovery status is unavailable." image={Empty.PRESENTED_IMAGE_SIMPLE} />
          )}
        </Col>
        <Col span={9}>
          <Card className="panel-card integration-explanation-card">
            <Space direction="vertical" size={10} className="full-width">
              <Text strong>Review flow</Text>
              {(status?.review_flow || []).slice(0, 5).map((step, index) => (
                <Text type="secondary" key={step}>
                  {index + 1}. {step}
                </Text>
              ))}
              <Alert
                type="info"
                showIcon
                message="Boundary"
                description="No automatic page fetching, no website scraping, no cookies, no real search provider, and no real LLM call in the current status design."
              />
            </Space>
          </Card>
        </Col>
      </Row>
    </Card>
  )
}

function PlatformTileList({ platforms, emptyText }) {
  if (!platforms.length) {
    return <Empty description={emptyText} image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <div className="integration-tile-grid">
      {platforms.map((platform) => (
        <div className="integration-tile" key={platform.platform_id}>
          <div className="integration-tile-header">
            <Space direction="vertical" size={2}>
              <Text strong>{platform.display_name || platform.platform_id}</Text>
              <Text type="secondary">{platform.platform_id}</Text>
            </Space>
            <StatusBadgeRow platform={platform} />
          </div>
          <Space wrap size={4}>
            <Tag>{safeText(platform.category)}</Tag>
            <Tag>{safeText(platform.source_type)}</Tag>
            <Tag color={statusTone[platform.status] || 'default'}>{safeText(platform.status)}</Tag>
          </Space>
          <RegistrySafetyFields platform={platform} />
          <ReadinessDetails platform={platform} />
          <CredentialStatus platform={platform} />
          <Paragraph className="integration-note" ellipsis={{ rows: 3 }}>
            {safeText(platform.notes, '暂无备注')}
          </Paragraph>
        </div>
      ))}
    </div>
  )
}

function classifyReadiness(platform = {}) {
  if (platform.real_mode_configured && platform.selectable_for_real) return 'realReady'
  if (platform.platform_id === 'youtube' && platform.real_mode_available) return 'configuredGuarded'
  if (platform.oauth_required || platform.oauth_status === 'oauth_pending') return 'oauthPending'
  if (
    platform.real_mode_blocker === 'approval_pending' ||
    platform.scope_status === 'approval_pending' ||
    platform.scope_status === 'company_age_requirement_pending' ||
    platform.scope_status === 'comment_api_unknown_or_not_confirmed' ||
    platform.comment_api_status === 'unknown_or_not_confirmed'
  ) {
    return 'permissionPending'
  }
  return 'mockScaffoldOnly'
}

function ReadinessGroupSection({ title, color, description, platforms }) {
  return (
    <Card className="panel-card integration-section-card">
      <div className="panel-heading">
        <Space>
          <ShieldCheck size={18} />
          <Title level={4}>{title}</Title>
        </Space>
        <Tag color={color}>{platforms.length}</Tag>
      </div>
      <Paragraph type="secondary" className="integration-table-note">
        {description}
      </Paragraph>
      <PlatformTileList platforms={platforms} emptyText={`${title} 暂无平台`} />
    </Card>
  )
}

export function PlatformIntegrationOverview() {
  const [platformStatus, setPlatformStatus] = useState(null)
  const [platformRegistry, setPlatformRegistry] = useState(null)
  const [parserStatus, setParserStatus] = useState(null)
  const [sourceCatalog, setSourceCatalog] = useState(null)
  const [searchDiscoveryStatus, setSearchDiscoveryStatus] = useState(null)
  const [previewByPlatform, setPreviewByPlatform] = useState({})
  const [selectedPlatform, setSelectedPlatform] = useState('')
  const [loading, setLoading] = useState(true)
  const [previewLoading, setPreviewLoading] = useState('')
  const [error, setError] = useState('')
  const [warning, setWarning] = useState('')

  const loadOverview = useCallback(async () => {
    setLoading(true)
    setError('')
    setWarning('')
    const readinessRequest = getPlatformReadiness().catch(async () => {
      const fallback = await getPlatformStatus()
      return { ...fallback, readiness_fallback_used: true }
    })
    const [platformsResult, statusResult, parsersResult, catalogResult, searchDiscoveryResult] = await Promise.allSettled([
      getPlatforms(),
      readinessRequest,
      getPublicParserStatus(),
      getSourceCatalog(),
      getSearchDiscoveryStatus(),
    ])

    const nextPlatformRegistry = platformsResult.status === 'fulfilled' ? platformsResult.value : null
    const nextPlatformStatus = statusResult.status === 'fulfilled' ? statusResult.value : null
    const nextParserStatus = parsersResult.status === 'fulfilled' ? parsersResult.value : null
    const nextSourceCatalog = catalogResult.status === 'fulfilled' ? catalogResult.value : null
    const nextSearchDiscoveryStatus = searchDiscoveryResult.status === 'fulfilled' ? searchDiscoveryResult.value : null

    setPlatformRegistry(nextPlatformRegistry)
    setPlatformStatus(nextPlatformStatus)
    setParserStatus(nextParserStatus)
    setSourceCatalog(nextSourceCatalog)
    setSearchDiscoveryStatus(nextSearchDiscoveryStatus)

    const partialWarnings = []
    if (platformsResult.status === 'rejected') partialWarnings.push('GET /api/v1/platforms 加载失败')
    if (statusResult.status === 'rejected') partialWarnings.push('GET /api/v1/platforms/readiness 加载失败')
    if (nextPlatformStatus?.readiness_fallback_used) {
      partialWarnings.push('GET /api/v1/platforms/readiness 不可用，已回退到 /platforms/status')
    }
    if (parsersResult.status === 'rejected') partialWarnings.push('GET /api/v1/public-parsers/status 加载失败')
    setWarning(partialWarnings.join('；'))

    const hasPlatforms = Boolean(nextPlatformStatus?.platforms?.length || nextPlatformRegistry?.platforms?.length)
    const hasParsers = Boolean(nextParserStatus?.parsers?.length)
    if (!hasPlatforms && !hasParsers) {
      setError('平台接入状态加载失败，请确认后端服务已启动。')
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    loadOverview()
  }, [loadOverview])

  const platforms = useMemo(() => {
    const source = platformStatus?.platforms?.length ? platformStatus.platforms : platformRegistry?.platforms
    return Array.isArray(source) ? source : []
  }, [platformRegistry, platformStatus])

  const publicParsers = useMemo(
    () => (Array.isArray(parserStatus?.parsers) ? parserStatus.parsers : []),
    [parserStatus],
  )

  const platformById = useMemo(() => {
    const map = new Map()
    platforms.forEach((platform) => {
      if (platform?.platform_id) map.set(platform.platform_id, platform)
    })
    return map
  }, [platforms])

  const officialPlatforms = useMemo(
    () => platforms.filter((platform) => platform.category === 'official_api_planned'),
    [platforms],
  )

  const publicParserRows = useMemo(() => {
    const parserIds = new Set([
      ...publicParsers.map((parser) => parser.platform_id),
      ...platforms
        .filter((platform) => platform.source_type === 'public_page_parser')
        .map((platform) => platform.platform_id),
    ])

    return [...parserIds].sort().map((platformId) => {
      const platform = platformById.get(platformId) || { platform_id: platformId }
      const parser = publicParsers.find((item) => item.platform_id === platformId) || {}
      return {
        ...platform,
        ...parser,
        platform_id: platformId,
        display_name: parser.display_name || platform.display_name || platformId,
        platform_notes: platform.notes || '',
        parser_notes: parser.notes || '',
      }
    })
  }, [platformById, platforms, publicParsers])

  const redditPlatforms = useMemo(
    () => platforms.filter((platform) => platform.platform_id === 'reddit'),
    [platforms],
  )

  const futurePlatforms = useMemo(
    () =>
      platforms.filter(
        (platform) =>
          platform.category === 'disabled_or_optional_future' ||
          (platform.category === 'crawler_later' && platform.source_type !== 'public_page_parser'),
      ),
    [platforms],
  )

  const readinessGroups = useMemo(() => {
    const groups = {
      realReady: [],
      configuredGuarded: [],
      permissionPending: [],
      oauthPending: [],
      mockScaffoldOnly: [],
    }
    platforms.forEach((platform) => {
      groups[classifyReadiness(platform)].push(platform)
    })
    return groups
  }, [platforms])

  const selectedPreview = selectedPlatform ? previewByPlatform[selectedPlatform] : null

  const handlePreview = async (platformId) => {
    setPreviewLoading(platformId)
    setError('')
    try {
      const preview = await previewPublicParser(platformId, 3, false)
      setPreviewByPlatform((current) => ({
        ...current,
        [platformId]: preview,
      }))
      setSelectedPlatform(platformId)
    } catch (requestError) {
      setError(requestError?.message || `无法预览解析源 ${platformId}`)
    } finally {
      setPreviewLoading('')
    }
  }

  const officialColumns = [
    {
      title: '平台',
      key: 'platform',
      width: 225,
      render: (_, record) => <PlatformNameCell record={record} />,
    },
    {
      title: '当前状态',
      key: 'status',
      width: 215,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <StatusBadgeRow platform={record} />
          <Tag color={statusTone[record.status] || 'default'}>{safeText(record.status)}</Tag>
        </Space>
      ),
    },
    {
      title: 'Mock 可用',
      dataIndex: 'mock_available',
      key: 'mock_available',
      width: 100,
      render: (value) => boolTag(value),
    },
    {
      title: '真实模式',
      dataIndex: 'real_mode_available',
      key: 'real_mode_available',
      width: 120,
      render: (value) => <Tag color={value ? 'green' : 'default'}>{value ? '可用' : '未启用'}</Tag>,
    },
    {
      title: 'API 审批',
      key: 'api_approval',
      width: 140,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          {boolTag(record.api_approval_required, '需要', '不需要')}
          <Tag color={statusTone[record.api_approval_status] || 'orange'}>
            {safeText(record.api_approval_status)}
          </Tag>
        </Space>
      ),
    },
    {
      title: '凭证状态',
      key: 'credentials',
      width: 245,
      render: (_, record) => <CredentialStatus platform={record} />,
    },
    {
      title: '选择状态',
      key: 'selectable',
      width: 180,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Text type="secondary">mock: {record.selectable_for_mock ? '可选' : '不可选'}</Text>
          <Text type="secondary">real: {record.selectable_for_real ? '可选' : '不可选'}</Text>
          <Text type="secondary">MVP: {record.enabled_in_mvp ? '启用' : '未启用'}</Text>
        </Space>
      ),
    },
    {
      title: '备注',
      dataIndex: 'notes',
      key: 'notes',
      width: 340,
      render: (value) => (
        <Paragraph className="integration-table-note" ellipsis={{ rows: 3 }}>
          {safeText(value, '暂无备注')}
        </Paragraph>
      ),
    },
  ]

  const parserColumns = [
    {
      title: '平台',
      key: 'platform',
      width: 220,
      render: (_, record) => <PlatformNameCell record={record} />,
    },
    {
      title: '解析状态',
      key: 'parser_status',
      width: 155,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <StatusBadgeRow platform={record} parser={record} />
          <Tag color={statusTone[record.parser_status] || 'default'}>{safeText(record.parser_status)}</Tag>
        </Space>
      ),
    },
    {
      title: 'Fixture 可用',
      dataIndex: 'fixture_available',
      key: 'fixture_available',
      width: 110,
      render: (value) => boolTag(value),
    },
    {
      title: 'Profile 可用',
      dataIndex: 'profile_available',
      key: 'profile_available',
      width: 110,
      render: (value) => boolTag(value),
    },
    {
      title: 'Live Fetch',
      dataIndex: 'live_fetch_enabled',
      key: 'live_fetch_enabled',
      width: 120,
      render: (value) => (
        <Tag color={value ? 'warning' : 'default'}>{value ? '后端启用' : 'Live 关闭'}</Tag>
      ),
    },
    {
      title: 'Registry 字段',
      key: 'registry_fields',
      width: 280,
      render: (_, record) => <RegistrySafetyFields platform={record} />,
    },
    {
      title: '凭证状态',
      key: 'credentials',
      width: 140,
      render: (_, record) => <CredentialStatus platform={record} />,
    },
    {
      title: '评论支持',
      dataIndex: 'comments_supported',
      key: 'comments_supported',
      width: 105,
      render: (value) => boolTag(value, '支持', '不支持'),
    },
    {
      title: '安全限制',
      key: 'safe_limit',
      width: 135,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Tag>{formatNumber(record.safe_limit, ' 条')}</Tag>
          <Text type="secondary">{formatNumber(record.rate_limit_seconds, 's')}</Text>
        </Space>
      ),
    },
    {
      title: '备注',
      key: 'notes',
      width: 330,
      render: (_, record) => (
        <Paragraph className="integration-table-note" ellipsis={{ rows: 3 }}>
          {safeText(record.parser_notes || record.platform_notes, '暂无备注')}
        </Paragraph>
      ),
    },
    {
      title: '预览',
      key: 'preview',
      width: 105,
      render: (_, record) => (
        <Button
          icon={<Eye size={15} />}
          loading={previewLoading === record.platform_id}
          onClick={() => handlePreview(record.platform_id)}
          size="small"
          type={selectedPlatform === record.platform_id ? 'primary' : 'default'}
        >
          预览
        </Button>
      ),
    },
  ]

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>平台接入总览</Title>
          <Text>集中查看官方 API scaffold、公开页面解析、Reddit 审批状态和未来可选数据源。</Text>
        </div>
        <Space>
          <Tag color="cyan" className="large-tag">Mock-first</Tag>
          <Tag color="default" className="large-tag">Live Fetch 不从前端启用</Tag>
          <Button icon={<RefreshCw size={16} />} loading={loading} onClick={loadOverview}>
            刷新
          </Button>
        </Space>
      </div>

      {error ? <Alert message="平台接入总览加载失败" description={error} type="error" showIcon /> : null}
      {warning ? <Alert message="部分状态接口加载失败" description={warning} type="warning" showIcon /> : null}

      {loading ? (
        <Card className="panel-card">
          <Skeleton active paragraph={{ rows: 10 }} title />
        </Card>
      ) : (
        <>
          <MetricCards platforms={platforms} publicParsers={publicParsers} summary={platformStatus?.summary} />
          <ExplanationCards />
          <SourceCatalogPanel catalog={sourceCatalog} />
          <SearchDiscoveryStatusPanel status={searchDiscoveryStatus} />

          <Row gutter={[16, 16]}>
            <Col span={12}>
              <ReadinessGroupSection
                title={groupLabels.realReady}
                color="green"
                description="可真实调用的官方 API 源；仍只显示安全元数据和凭证布尔状态。"
                platforms={readinessGroups.realReady}
              />
            </Col>
            <Col span={12}>
              <ReadinessGroupSection
                title={groupLabels.configuredGuarded}
                color="blue"
                description="具备真实模式能力但仍受本地配置、缓存、配额和手动 demo 边界保护。"
                platforms={readinessGroups.configuredGuarded}
              />
            </Col>
            <Col span={12}>
              <ReadinessGroupSection
                title={groupLabels.oauthPending}
                color="purple"
                description="需要 OAuth、scope、redirect URI、白名单、token 或授权账号验证。"
                platforms={readinessGroups.oauthPending}
              />
            </Col>
            <Col span={12}>
              <ReadinessGroupSection
                title={groupLabels.permissionPending}
                color="orange"
                description="开发者权限、审批、评论接口、公司资质或数据范围仍未确认。"
                platforms={readinessGroups.permissionPending}
              />
            </Col>
          </Row>

          <ReadinessGroupSection
            title={groupLabels.mockScaffoldOnly}
            color="default"
            description="仅用于 mock、fixture 或未来规划；不触发真实 API、抓取、cookies 或 live fetch。"
            platforms={readinessGroups.mockScaffoldOnly}
          />

          <Card className="panel-card integration-section-card">
            <div className="panel-heading">
              <Space>
                <FileSearch size={18} />
                <Title level={4}>{groupLabels.official}</Title>
              </Space>
              <Tag color="blue">{officialPlatforms.length}</Tag>
            </div>
            {officialPlatforms.length ? (
              <Table
                columns={officialColumns}
                dataSource={officialPlatforms}
                pagination={false}
                rowKey="platform_id"
                scroll={{ x: 1660 }}
              />
            ) : (
              <Empty description="暂无官方 API 规划平台状态" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            )}
          </Card>

          <Card className="panel-card integration-section-card">
            <div className="panel-heading">
              <Space>
                <Database size={18} />
                <Title level={4}>{groupLabels.publicParser}</Title>
              </Space>
              <Space wrap>
                <Tag color="cyan">{publicParserRows.length}</Tag>
                <Tag color="green">preview use_live_fetch=false</Tag>
              </Space>
            </div>
            {publicParserRows.length ? (
              <Table
                columns={parserColumns}
                dataSource={publicParserRows}
                pagination={false}
                rowKey="platform_id"
                rowClassName={(record) => (record.platform_id === selectedPlatform ? 'active-parser-row' : '')}
                scroll={{ x: 1830 }}
              />
            ) : (
              <Empty description="暂无公开页面解析平台状态" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            )}
          </Card>

          <Row gutter={[16, 16]}>
            <Col span={12}>
              <Card className="panel-card integration-section-card">
                <div className="panel-heading">
                  <Space>
                    <ShieldCheck size={18} />
                    <Title level={4}>{groupLabels.reddit}</Title>
                  </Space>
                  <Tag color="orange">API 待接入</Tag>
                </div>
                <PlatformTileList platforms={redditPlatforms} emptyText="暂无 Reddit 状态" />
              </Card>
            </Col>
            <Col span={12}>
              <Card className="panel-card integration-section-card">
                <div className="panel-heading">
                  <Space>
                    <Globe2 size={18} />
                    <Title level={4}>{groupLabels.future}</Title>
                  </Space>
                  <Tag>{futurePlatforms.length}</Tag>
                </div>
                <PlatformTileList platforms={futurePlatforms} emptyText="暂无未来可选平台" />
              </Card>
            </Col>
          </Row>

          <Card className="panel-card parser-preview-shell">
            <div className="panel-heading">
              <Space>
                <Eye size={18} />
                <Title level={4}>公开页面解析预览</Title>
              </Space>
              <Space wrap>
                <Tag color="cyan">{selectedPlatform || '未选择'}</Tag>
                <Tag color="default">limit=3</Tag>
                <Tag color="green">use_live_fetch=false</Tag>
              </Space>
            </div>
            <PreviewPanel
              loading={Boolean(previewLoading)}
              preview={selectedPreview}
              selectedPlatform={selectedPlatform}
            />
          </Card>
        </>
      )}
    </div>
  )
}
