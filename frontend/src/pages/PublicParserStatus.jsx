import { Alert, Button, Card, Col, Empty, List, Row, Skeleton, Space, Table, Tag, Typography } from 'antd'
import { Database, Eye, FileSearch, MessageCircle, RefreshCw, ShieldCheck } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import { getPublicParserStatus, previewPublicParser } from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const parserStatusTone = {
  fixture_only: 'cyan',
  scaffolded: 'geekblue',
  disabled: 'default',
  live_public_enabled: 'green',
}

function booleanTag(value, trueText = '是', falseText = '否') {
  return <Tag color={value ? 'green' : 'default'}>{value ? trueText : falseText}</Tag>
}

function formatNumber(value, suffix = '') {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? `${numericValue}${suffix}` : '-'
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString('zh-CN', { hour12: false })
}

function safePreviewText(value, fallback = '-') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function schemaTag(valid) {
  return <Tag color={valid ? 'green' : 'red'}>{valid ? '通过' : '异常'}</Tag>
}

function getPreviewSummary(preview) {
  if (!preview) {
    return {
      postCount: 0,
      commentCount: 0,
      fallbackReason: '-',
      rawPostValid: false,
      rawCommentValid: false,
      warnings: [],
    }
  }

  return {
    postCount: Number(preview.post_count || 0),
    commentCount: Number(preview.comment_count || 0),
    fallbackReason: preview.fallback_reason_category || '-',
    rawPostValid: preview.raw_post_schema_valid !== false,
    rawCommentValid: preview.raw_comment_schema_valid !== false,
    warnings: Array.isArray(preview.warnings) ? preview.warnings : [],
  }
}

function ParserStatusCards({ status }) {
  const parsers = status?.parsers || []
  const fixtureCount = parsers.filter((parser) => parser.fixture_available).length
  const profileCount = parsers.filter((parser) => parser.profile_available).length
  const commentCount = parsers.filter((parser) => parser.comments_supported).length
  const liveCount = parsers.filter((parser) => parser.live_fetch_enabled).length

  return (
    <Row gutter={[16, 16]}>
      <Col span={6}>
        <Card className="metric-card parser-metric-card">
          <Space className="metric-heading">
            <Database size={18} />
            <Text>解析源数量</Text>
          </Space>
          <Title level={2}>{formatNumber(status?.total || parsers.length)}</Title>
          <Text type="secondary">当前注册的公开页面解析 scaffold。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card parser-metric-card">
          <Space className="metric-heading">
            <FileSearch size={18} />
            <Text>Fixture 可用</Text>
          </Space>
          <Title level={2}>{fixtureCount}</Title>
          <Text type="secondary">用于本地离线预览和测试。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card parser-metric-card">
          <Space className="metric-heading">
            <MessageCircle size={18} />
            <Text>评论支持</Text>
          </Space>
          <Title level={2}>{commentCount}</Title>
          <Text type="secondary">仅解析 fixture 中公开可见评论。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card parser-metric-card">
          <Space className="metric-heading">
            <ShieldCheck size={18} />
            <Text>Live Fetch 状态</Text>
          </Space>
          <Title level={2}>{liveCount}</Title>
          <Text type="secondary">
            默认：{status?.live_fetch_enabled_default ? '已启用' : '已关闭'}，前端预览固定使用 fixture。
          </Text>
        </Card>
      </Col>
    </Row>
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
                <Tag color="cyan">{safePreviewText(post.platform, 'unknown')}</Tag>
                <Text type="secondary">{safePreviewText(post.post_id)}</Text>
              </Space>
              <Text strong>{safePreviewText(post.title, 'Untitled public post')}</Text>
              <Paragraph ellipsis={{ rows: 3 }} className="parser-sample-content">
                {safePreviewText(post.content, '暂无正文预览')}
              </Paragraph>
              <Space wrap>
                <Text type="secondary">作者/来源：{safePreviewText(post.author_name || post.author_id)}</Text>
                <Text type="secondary">时间：{formatDate(post.created_at)}</Text>
                <Text type="secondary">互动：{formatNumber(post.like_count)} likes / {formatNumber(post.reply_count)} replies</Text>
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
    return <Empty description="暂无公开可见评论样本" image={Empty.PRESENTED_IMAGE_SIMPLE} />
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
                <Tag>{safePreviewText(comment.platform, 'unknown')}</Tag>
                <Text strong>{safePreviewText(comment.author_name || comment.author_id, 'anonymous')}</Text>
                <Text type="secondary">{formatDate(comment.created_at)}</Text>
              </Space>
              <Paragraph ellipsis={{ rows: 2 }} className="parser-sample-content">
                {safePreviewText(comment.content, '暂无评论内容')}
              </Paragraph>
              <Text type="secondary">
                comment_id: {safePreviewText(comment.comment_id)} · likes: {formatNumber(comment.like_count)}
              </Text>
            </Space>
          </div>
        </List.Item>
      )}
    />
  )
}

function PreviewPanel({ loading, preview }) {
  if (loading && !preview) {
    return <Skeleton active paragraph={{ rows: 8 }} title />
  }

  if (!preview) {
    return (
      <Empty
        description="选择一个解析源并点击预览。前端会固定发送 use_live_fetch=false。"
        image={Empty.PRESENTED_IMAGE_SIMPLE}
      />
    )
  }

  const summary = getPreviewSummary(preview)

  return (
    <Space direction="vertical" className="full-width" size={16}>
      <div className="parser-preview-summary">
        <div>
          <Text type="secondary">平台</Text>
          <Text strong>{preview.platform}</Text>
        </div>
        <div>
          <Text type="secondary">Post / Comment</Text>
          <Text strong>{summary.postCount} / {summary.commentCount}</Text>
        </div>
        <div>
          <Text type="secondary">回退状态</Text>
          <Space size={4} wrap>
            <Tag color={preview.fallback_used ? 'gold' : 'green'}>
              {preview.fallback_used ? 'fallback_used=true' : 'fallback_used=false'}
            </Tag>
            <Tag>{summary.fallbackReason}</Tag>
          </Space>
        </div>
        <div>
          <Text type="secondary">Schema 校验</Text>
          <Space size={4}>
            {schemaTag(summary.rawPostValid)}
            {schemaTag(summary.rawCommentValid)}
          </Space>
        </div>
      </div>

      {summary.warnings.length ? (
        <Alert
          type="warning"
          showIcon
          message="预览提示"
          description={
            <Space wrap>
              {summary.warnings.map((warning) => (
                <Tag color="orange" key={warning}>{warning}</Tag>
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

export function PublicParserStatus() {
  const [status, setStatus] = useState(null)
  const [selectedPlatform, setSelectedPlatform] = useState('')
  const [previewByPlatform, setPreviewByPlatform] = useState({})
  const [loading, setLoading] = useState(true)
  const [previewLoading, setPreviewLoading] = useState('')
  const [error, setError] = useState('')

  const parsers = useMemo(() => status?.parsers || [], [status])
  const selectedPreview = selectedPlatform ? previewByPlatform[selectedPlatform] : null

  const loadStatus = async () => {
    setLoading(true)
    setError('')
    try {
      const response = await getPublicParserStatus()
      setStatus(response)
      if (!selectedPlatform && response.parsers?.length) {
        setSelectedPlatform(response.parsers[0].platform_id)
      }
    } catch (requestError) {
      setError(requestError?.message || '公开页面解析状态加载失败')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadStatus()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

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

  const columns = [
    {
      title: '平台',
      dataIndex: 'display_name',
      key: 'display_name',
      width: 210,
      render: (value, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{value || record.platform_id}</Text>
          <Text type="secondary">{record.platform_id}</Text>
          <Tag color="geekblue">{record.source_type}</Tag>
        </Space>
      ),
    },
    {
      title: '解析状态',
      dataIndex: 'parser_status',
      key: 'parser_status',
      width: 135,
      render: (value) => <Tag color={parserStatusTone[value] || 'default'}>{value}</Tag>,
    },
    {
      title: 'Fixture 可用',
      dataIndex: 'fixture_available',
      key: 'fixture_available',
      width: 120,
      render: (value) => booleanTag(value),
    },
    {
      title: 'Profile 可用',
      dataIndex: 'profile_available',
      key: 'profile_available',
      width: 120,
      render: (value) => booleanTag(value),
    },
    {
      title: 'Live Fetch 状态',
      dataIndex: 'live_fetch_enabled',
      key: 'live_fetch_enabled',
      width: 145,
      render: (value) => (
        <Tag color={value ? 'warning' : 'default'}>{value ? '后端已启用' : '默认关闭'}</Tag>
      ),
    },
    {
      title: '评论支持',
      dataIndex: 'comments_supported',
      key: 'comments_supported',
      width: 110,
      render: (value) => booleanTag(value, '支持', '不支持'),
    },
    {
      title: '安全限制',
      dataIndex: 'safe_limit',
      key: 'safe_limit',
      width: 100,
      render: (value) => <Tag>{formatNumber(value, ' 条')}</Tag>,
    },
    {
      title: '请求间隔',
      dataIndex: 'rate_limit_seconds',
      key: 'rate_limit_seconds',
      width: 105,
      render: (value) => <Tag>{formatNumber(value, 's')}</Tag>,
    },
    {
      title: '备注',
      dataIndex: 'notes',
      key: 'notes',
      width: 260,
      render: (value) => (
        <Paragraph className="parser-table-note" ellipsis={{ rows: 2 }}>
          {safePreviewText(value, '暂无备注')}
        </Paragraph>
      ),
    },
    {
      title: '预览',
      key: 'preview',
      width: 110,
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
          <Title level={2}>公开页面解析</Title>
          <Text>查看 public-page parser 的 fixture 状态，并安全预览离线解析样本。</Text>
        </div>
        <Space>
          <Tag color="cyan" className="large-tag">Fixture Preview</Tag>
          <Tag color="default" className="large-tag">Live Fetch 不从前端启用</Tag>
          <Button icon={<RefreshCw size={16} />} loading={loading} onClick={loadStatus}>
            刷新
          </Button>
        </Space>
      </div>

      {error ? <Alert message="公开页面解析页面加载失败" description={error} type="error" showIcon /> : null}

      {loading && !status ? (
        <Card className="panel-card">
          <Skeleton active paragraph={{ rows: 8 }} title />
        </Card>
      ) : (
        <>
          <ParserStatusCards status={status} />

          <Card className="panel-card parser-status-card">
            <div className="panel-heading">
              <Space>
                <FileSearch size={18} />
                <Title level={4}>Parser Source Status</Title>
              </Space>
              <Tag color={status?.live_fetch_enabled_default ? 'warning' : 'green'}>
                默认 Live Fetch：{status?.live_fetch_enabled_default ? '开启' : '关闭'}
              </Tag>
            </div>
            {parsers.length ? (
              <Table
                columns={columns}
                dataSource={parsers}
                pagination={false}
                rowKey="platform_id"
                rowClassName={(record) => (record.platform_id === selectedPlatform ? 'active-parser-row' : '')}
                scroll={{ x: 1420 }}
              />
            ) : (
              <Empty description="暂无公开页面解析源状态" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            )}
          </Card>

          <Card className="panel-card parser-preview-shell">
            <div className="panel-heading">
              <Space>
                <Eye size={18} />
                <Title level={4}>预览</Title>
              </Space>
              <Space wrap>
                <Tag color="cyan">{selectedPlatform || '未选择'}</Tag>
                <Tag color="default">limit=3</Tag>
                <Tag color="green">use_live_fetch=false</Tag>
              </Space>
            </div>
            <PreviewPanel loading={Boolean(previewLoading)} preview={selectedPreview} />
          </Card>

          <Card className="panel-card parser-notes-card">
            <div className="panel-heading">
              <Space>
                <ShieldCheck size={18} />
                <Title level={4}>安全边界</Title>
              </Space>
              <Tag color="green">mock-first</Tag>
            </div>
            <List
              dataSource={parsers}
              locale={{ emptyText: '暂无 parser notes' }}
              renderItem={(parser) => (
                <List.Item>
                  <Space direction="vertical" size={4} className="full-width">
                    <Space wrap>
                      <Tag color="geekblue">{parser.platform_id}</Tag>
                      <Tag color={parser.comments_supported ? 'green' : 'default'}>
                        评论支持：{parser.comments_supported ? '是' : '否'}
                      </Tag>
                    </Space>
                    <Text type="secondary">{parser.notes || '暂无备注'}</Text>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </>
      )}
    </div>
  )
}
