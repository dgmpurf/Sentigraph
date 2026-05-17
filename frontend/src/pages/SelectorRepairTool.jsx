import {
  Alert,
  Button,
  Card,
  Col,
  Collapse,
  Empty,
  Form,
  Input,
  List,
  Row,
  Select,
  Skeleton,
  Space,
  Tag,
  Typography,
} from 'antd'
import { ClipboardCopy, Eye, FileSearch, ShieldCheck, Wand2 } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import {
  getPublicParserStatus,
  previewSelectorRepair,
  suggestSelectorRepair,
} from '../api/sentigraphApi.js'
import { copyTextToClipboard } from '../utils/clipboard.js'

const { Paragraph, Text, Title } = Typography
const { TextArea } = Input

const PUBLIC_PARSER_OPTIONS = [
  { label: 'The Paper / 澎湃新闻', value: 'the_paper' },
  { label: 'Jiemian / 界面新闻', value: 'jiemian' },
  { label: 'Hupu / 虎扑', value: 'hupu' },
  { label: 'Baidu Tieba / 百度贴吧', value: 'tieba' },
  { label: 'NGA', value: 'nga' },
  { label: 'Maimai / 脉脉', value: 'maimai' },
]

const DEFAULT_HTML = `<article class="thread">
  <h1 class="thread-title">Fixture title for selector repair</h1>
  <div class="thread-content">Visible public fixture content for parser maintenance.</div>
  <div class="reply">
    <span class="reply-author">fixture_user</span>
    <p class="reply-content">Visible public reply.</p>
  </div>
</article>`

const DEFAULT_TARGETS = 'title, content, author, created_at, comment_content'

function safeText(value, fallback = '-') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function getErrorMessage(error, fallback) {
  const detail = error?.response?.data?.detail
  if (typeof detail === 'string') return detail
  if (Array.isArray(detail) && detail.length) {
    return detail.map((item) => item?.msg || 'validation error').join('; ')
  }
  return error?.message || fallback
}

function splitTargets(value) {
  return String(value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
}

function warningTags(warnings = []) {
  if (!warnings.length) return <Text type="secondary">暂无警告</Text>
  return (
    <Space wrap>
      {warnings.map((warning) => (
        <Tag color="orange" key={warning}>
          {warning}
        </Tag>
      ))}
    </Space>
  )
}

function CandidateList({ candidates = [] }) {
  if (!candidates.length) {
    return <Empty description="暂无候选 Selector" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <List
      className="selector-candidate-list"
      dataSource={candidates}
      renderItem={(candidate) => (
        <List.Item>
          <div className="selector-candidate-card">
            <Space direction="vertical" size={8} className="full-width">
              <Space wrap>
                <Tag color="cyan">{safeText(candidate.target)}</Tag>
                <Tag>{safeText(candidate.selector_type, 'css')}</Tag>
                <Tag color="geekblue">confidence {Math.round(Number(candidate.confidence || 0) * 100)}%</Tag>
              </Space>
              <Text code className="selector-code-line">
                {safeText(candidate.selector)}
              </Text>
              <Paragraph className="selector-rationale">
                {safeText(candidate.rationale, '暂无 rationale')}
              </Paragraph>
              {candidate.warning ? <Tag color="orange">{candidate.warning}</Tag> : null}
              <Text type="secondary">source: {safeText(candidate.source)}</Text>
            </Space>
          </div>
        </List.Item>
      )}
    />
  )
}

function PreviewSummary({ preview }) {
  if (!preview) {
    return <Empty description="生成建议后可预览候选 Selector" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  const sampleValues = preview.sample_values || {}
  const matchedEntries = Object.entries(preview.matched_targets || {})
  const commentCount = Object.keys(sampleValues).filter((key) => key.includes('comment')).length
  const contentPreview = sampleValues.content || sampleValues.main_content || sampleValues.body || ''

  return (
    <Space direction="vertical" size={16} className="full-width">
      <div className="selector-preview-summary">
        <div>
          <Text type="secondary">状态</Text>
          <Tag color={preview.status === 'preview_ok' ? 'green' : 'orange'}>{safeText(preview.status)}</Tag>
        </div>
        <div>
          <Text type="secondary">Profile 修改</Text>
          <Tag color={preview.profile_modified ? 'red' : 'green'}>
            {preview.profile_modified ? 'true' : 'false'}
          </Tag>
        </div>
        <div>
          <Text type="secondary">Schema 校验</Text>
          <Text strong>-</Text>
        </div>
        <div>
          <Text type="secondary">评论提取数</Text>
          <Text strong>{commentCount}</Text>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="selector-preview-card" title="提取标题">
            <Paragraph className="selector-preview-copy">
              {safeText(sampleValues.title, '未提取到 title')}
            </Paragraph>
          </Card>
        </Col>
        <Col span={12}>
          <Card className="selector-preview-card" title="内容预览">
            <Paragraph ellipsis={{ rows: 4 }} className="selector-preview-copy">
              {safeText(contentPreview, '未提取到 content')}
            </Paragraph>
          </Card>
        </Col>
      </Row>

      <Card className="selector-preview-card" title="匹配结果">
        {matchedEntries.length ? (
          <Space wrap>
            {matchedEntries.map(([target, matched]) => (
              <Tag color={matched ? 'green' : 'red'} key={target}>
                {target}: {matched ? 'matched' : 'missing'}
              </Tag>
            ))}
          </Space>
        ) : (
          <Empty description="暂无 matched_targets" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </Card>
    </Space>
  )
}

function SafetyNotice() {
  const items = [
    '当前工具只使用 MockProvider',
    '不调用真实大模型',
    '不抓取真实网页',
    '不自动修改 parser profile',
    '只用于 fixture / sanitized HTML 维护',
  ]

  return (
    <Card className="panel-card selector-safety-card">
      <div className="panel-heading">
        <Space>
          <ShieldCheck size={18} />
          <Title level={4}>安全边界</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">MockProvider 模式</Tag>
          <Tag color="green">不会自动修改 Profile</Tag>
        </Space>
      </div>
      <Space wrap>
        {items.map((item) => (
          <Tag color="geekblue" key={item}>
            {item}
          </Tag>
        ))}
      </Space>
    </Card>
  )
}

export function SelectorRepairTool() {
  const [form] = Form.useForm()
  const [parserStatus, setParserStatus] = useState(null)
  const [statusLoading, setStatusLoading] = useState(true)
  const [suggestion, setSuggestion] = useState(null)
  const [preview, setPreview] = useState(null)
  const [suggestLoading, setSuggestLoading] = useState(false)
  const [previewLoading, setPreviewLoading] = useState(false)
  const [error, setError] = useState('')
  const [notice, setNotice] = useState('')

  useEffect(() => {
    let mounted = true
    getPublicParserStatus()
      .then((status) => {
        if (mounted) setParserStatus(status)
      })
      .catch(() => {
        if (mounted) setParserStatus(null)
      })
      .finally(() => {
        if (mounted) setStatusLoading(false)
      })
    return () => {
      mounted = false
    }
  }, [])

  const platformOptions = useMemo(() => {
    const statusOptions = (parserStatus?.parsers || [])
      .filter((parser) => PUBLIC_PARSER_OPTIONS.some((option) => option.value === parser.platform_id))
      .map((parser) => ({
        label: `${parser.display_name || parser.platform_id} (${parser.platform_id})`,
        value: parser.platform_id,
      }))
    return statusOptions.length ? statusOptions : PUBLIC_PARSER_OPTIONS
  }, [parserStatus])

  const allWarnings = useMemo(() => {
    const values = [...(suggestion?.warnings || []), ...(preview?.warnings || [])]
    return [...new Set(values)]
  }, [preview, suggestion])

  const handleSuggest = async () => {
    setError('')
    setNotice('')
    setPreview(null)
    const values = form.getFieldsValue()
    const html = values.html || ''
    if (!html.trim()) {
      setError('请先粘贴 fixture / sanitized HTML。')
      return
    }

    setSuggestLoading(true)
    try {
      const response = await suggestSelectorRepair({
        platform_id: values.platform_id,
        html,
        extraction_targets: splitTargets(values.extraction_targets),
        error_summary: values.error_summary || '',
      })
      setSuggestion(response)
    } catch (requestError) {
      setSuggestion(null)
      setError(getErrorMessage(requestError, 'Selector 建议生成失败。'))
    } finally {
      setSuggestLoading(false)
    }
  }

  const handlePreview = async () => {
    setError('')
    setNotice('')
    const values = form.getFieldsValue()
    const html = values.html || ''
    if (!html.trim()) {
      setError('请先提供用于预览的 fixture / sanitized HTML。')
      return
    }
    if (!suggestion) {
      setError('请先生成 Selector 建议。')
      return
    }

    setPreviewLoading(true)
    try {
      const response = await previewSelectorRepair({
        platform_id: values.platform_id,
        suggestion,
        fixture_html: html,
      })
      setPreview(response)
    } catch (requestError) {
      setPreview(null)
      setError(getErrorMessage(requestError, 'Selector 预览失败。'))
    } finally {
      setPreviewLoading(false)
    }
  }

  const handleCopyDraft = async () => {
    if (!suggestion) return
    const copied = await copyTextToClipboard(JSON.stringify(suggestion, null, 2))
    setNotice(copied ? '候选 Selector JSON 已复制为草稿。' : '复制失败，请手动展开 debug JSON。')
  }

  return (
    <div className="page-stack selector-repair-page">
      <div className="page-heading">
        <div>
          <Title level={2}>Selector 修复工具</Title>
          <Text>使用 fixture / sanitized HTML 生成和预览候选 Selector；不会抓取真实网页，也不会写入 profile。</Text>
        </div>
        <Space wrap>
          <Tag color="cyan" className="large-tag">MockProvider 模式</Tag>
          <Tag color="green" className="large-tag">不会自动修改 Profile</Tag>
        </Space>
      </div>

      <SafetyNotice />

      {error ? <Alert message="Selector 修复工具提示" description={error} type="error" showIcon /> : null}
      {notice ? <Alert message={notice} type="success" showIcon /> : null}

      <Row gutter={[16, 16]}>
        <Col span={10}>
          <Card className="panel-card selector-input-card">
            <div className="panel-heading">
              <Space>
                <FileSearch size={18} />
                <Title level={4}>输入</Title>
              </Space>
              {statusLoading ? <Tag>加载平台中</Tag> : <Tag color="cyan">{platformOptions.length} platforms</Tag>}
            </div>

            {statusLoading ? (
              <Skeleton active paragraph={{ rows: 8 }} title />
            ) : (
              <Form
                form={form}
                layout="vertical"
                initialValues={{
                  platform_id: 'hupu',
                  html: DEFAULT_HTML,
                  extraction_targets: DEFAULT_TARGETS,
                  error_summary: 'title/content selectors did not match fixture HTML',
                }}
              >
                <Form.Item label="平台" name="platform_id">
                  <Select
                    options={platformOptions}
                    onChange={() => {
                      setSuggestion(null)
                      setPreview(null)
                      setError('')
                      setNotice('')
                    }}
                  />
                </Form.Item>
                <Form.Item label="Sanitized HTML" name="html">
                  <TextArea
                    autoSize={{ minRows: 14, maxRows: 22 }}
                    placeholder="粘贴公开 fixture / sanitized HTML。不要粘贴 cookies、token、私有页面或登录后内容。"
                  />
                </Form.Item>
                <Form.Item label="错误摘要" name="error_summary">
                  <Input placeholder="例如：title/content selectors did not match fixture HTML" />
                </Form.Item>
                <Form.Item label="Extraction targets" name="extraction_targets">
                  <Input placeholder="title, content, author, created_at, comment_content" />
                </Form.Item>
                <Space wrap>
                  <Button
                    icon={<Wand2 size={16} />}
                    loading={suggestLoading}
                    onClick={handleSuggest}
                    type="primary"
                  >
                    生成 Selector 建议
                  </Button>
                  <Button
                    icon={<Eye size={16} />}
                    disabled={!suggestion}
                    loading={previewLoading}
                    onClick={handlePreview}
                  >
                    预览建议
                  </Button>
                  <Button
                    icon={<ClipboardCopy size={16} />}
                    disabled={!suggestion}
                    onClick={handleCopyDraft}
                  >
                    复制草稿 JSON
                  </Button>
                </Space>
              </Form>
            )}
          </Card>
        </Col>

        <Col span={14}>
          <Space direction="vertical" size={16} className="full-width">
            <Card className="panel-card selector-result-card">
              <div className="panel-heading">
                <Space>
                  <Wand2 size={18} />
                  <Title level={4}>候选 Selector</Title>
                </Space>
                <Space wrap>
                  <Tag color={suggestion?.generated_by_mock ? 'green' : 'default'}>
                    generated_by_mock={suggestion?.generated_by_mock ? 'true' : 'false'}
                  </Tag>
                  <Tag>{safeText(suggestion?.status, '未生成')}</Tag>
                </Space>
              </div>
              {suggestLoading ? (
                <Skeleton active paragraph={{ rows: 8 }} title />
              ) : suggestion ? (
                <CandidateList candidates={suggestion.candidates || []} />
              ) : (
                <Empty description="点击生成建议后显示候选 Selector" image={Empty.PRESENTED_IMAGE_SIMPLE} />
              )}
            </Card>

            <Card className="panel-card selector-result-card">
              <div className="panel-heading">
                <Space>
                  <Eye size={18} />
                  <Title level={4}>预览结果</Title>
                </Space>
                <Tag color="green">profile_modified=false</Tag>
              </div>
              {previewLoading ? <Skeleton active paragraph={{ rows: 8 }} title /> : <PreviewSummary preview={preview} />}
            </Card>
          </Space>
        </Col>
      </Row>

      <Card className="panel-card selector-warning-card">
        <div className="panel-heading">
          <Space>
            <ShieldCheck size={18} />
            <Title level={4}>警告</Title>
          </Space>
          <Tag color="default">review required</Tag>
        </div>
        {warningTags(allWarnings)}
      </Card>

      <Collapse
        className="selector-debug-collapse"
        items={[
          {
            key: 'debug',
            label: 'Debug JSON',
            children: (
              <pre className="selector-debug-json">
                {JSON.stringify({ suggestion, preview }, null, 2)}
              </pre>
            ),
          },
        ]}
      />
    </div>
  )
}
