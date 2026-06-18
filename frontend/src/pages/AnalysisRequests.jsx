import {
  Alert,
  App as AntApp,
  Button,
  Card,
  Checkbox,
  Col,
  Descriptions,
  Empty,
  Form,
  Input,
  InputNumber,
  Row,
  Select,
  Space,
  Statistic,
  Table,
  Tag,
  Typography,
} from 'antd'
import { ClipboardCopy, FileJson, RefreshCw, ShieldCheck, XCircle } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import {
  cancelAnalysisRequest,
  createAnalysisRequest,
  getAnalysisRequest,
  getAnalysisRequestConfig,
  listAnalysisRequests,
} from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography
const { TextArea } = Input

const STATUS_COLOR = {
  draft: 'default',
  queued: 'blue',
  accepted: 'blue',
  planning: 'geekblue',
  safety_check: 'purple',
  blocked_by_safety_gate: 'red',
  needs_manual_snapshot: 'gold',
  running_safe: 'cyan',
  cooldown: 'orange',
  partial_success: 'gold',
  package_generated: 'blue',
  validation_running: 'geekblue',
  validation_warn: 'gold',
  validation_failed: 'red',
  package_ready: 'green',
  canceled: 'default',
  expired: 'default',
}

const SAFETY_COLOR = {
  safe: 'green',
  medium: 'gold',
  hold: 'orange',
  cooldown: 'orange',
  blocked: 'red',
}

const DEFAULT_FORM_VALUES = {
  title: 'Helldivers PSN selected public sample request',
  description: 'Create a local file-based analysis request. Provider execution stays outside Sentigraph.',
  keywords: ['helldivers', 'psn'],
  negative_keywords: [],
  language: ['zh-CN'],
  event_type: 'public_opinion_event',
  sensitive_flags: [],
  platforms: ['reddit', 'news_site'],
  target_comment_count: 500,
  target_source_count: 30,
  max_runtime_minutes: 60,
  sample_strategy: 'stratified_public_sample',
  allow_manual_snapshot: true,
  allow_official_api: true,
  allow_vendor_api: true,
  allow_live_collection: false,
  allow_saved_profile: false,
  minor_sensitive_mode: true,
}

const BOUNDARY_TAGS = [
  'local file request only',
  'Evidence Package input',
  'provider execution outside Sentigraph',
  'no collector job',
  'no URL fetch',
  'no real API',
  'no real LLM',
  'not full-web coverage',
  'needs review',
]

function statusTag(status) {
  return <Tag color={STATUS_COLOR[status] || 'default'}>{status || 'no_result'}</Tag>
}

function safetyTag(status) {
  return <Tag color={SAFETY_COLOR[status] || 'default'}>{status || 'not_reported'}</Tag>
}

function splitTags(value) {
  if (Array.isArray(value)) return value
  return String(value || '')
    .split(',')
    .map((item) => item.trim())
    .filter(Boolean)
}

function buildPayload(values) {
  return {
    created_by: 'sentigraph_local_ui',
    case_seed: {
      title: values.title,
      description: values.description || '',
      keywords: splitTags(values.keywords),
      negative_keywords: splitTags(values.negative_keywords),
      language: splitTags(values.language).length ? splitTags(values.language) : ['zh-CN'],
      event_type: values.event_type || 'public_opinion_event',
      sensitive_flags: splitTags(values.sensitive_flags),
    },
    sampling_plan: {
      platforms: splitTags(values.platforms),
      time_range: {},
      target_comment_count: Number(values.target_comment_count || 500),
      target_source_count: Number(values.target_source_count || 30),
      max_runtime_minutes: Number(values.max_runtime_minutes || 60),
      sample_strategy: values.sample_strategy || 'stratified_public_sample',
    },
    safety_policy: {
      allow_live_collection: Boolean(values.allow_live_collection),
      allow_saved_profile: Boolean(values.allow_saved_profile),
      allow_manual_snapshot: values.allow_manual_snapshot !== false,
      allow_official_api: values.allow_official_api !== false,
      allow_vendor_api: values.allow_vendor_api !== false,
      forbid_proxy_pool: true,
      forbid_captcha_bypass: true,
      forbid_private_content: true,
    },
    privacy_policy: {
      remove_raw_author_id: true,
      remove_raw_author_name: true,
      remove_profile_url: true,
      remove_private_messages: true,
      minor_sensitive_mode: values.minor_sensitive_mode !== false,
    },
    output: {
      package_schema: 'sentigraph_evidence_export_v1',
      package_slug: '',
      package_index_required: true,
    },
  }
}

export function AnalysisRequests() {
  const { message } = AntApp.useApp()
  const [form] = Form.useForm()
  const [config, setConfig] = useState(null)
  const [requests, setRequests] = useState([])
  const [selectedRequestId, setSelectedRequestId] = useState('')
  const [detail, setDetail] = useState(null)
  const [loading, setLoading] = useState(false)
  const [creating, setCreating] = useState(false)
  const [canceling, setCanceling] = useState(false)
  const [error, setError] = useState('')

  const selectedRecord = useMemo(
    () => detail || requests.find((item) => item.request_id === selectedRequestId) || null,
    [detail, requests, selectedRequestId],
  )

  async function loadRequests(nextSelectedId = selectedRequestId) {
    setLoading(true)
    setError('')
    try {
      const [nextConfig, nextRequests] = await Promise.all([
        getAnalysisRequestConfig(),
        listAnalysisRequests(),
      ])
      setConfig(nextConfig)
      setRequests(nextRequests)
      const fallbackId = nextSelectedId || nextRequests[0]?.request_id || ''
      setSelectedRequestId(fallbackId)
      setDetail(fallbackId ? await getAnalysisRequest(fallbackId) : null)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load local analysis requests.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadRequests('')
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  async function handleCreate(values) {
    setCreating(true)
    setError('')
    try {
      const created = await createAnalysisRequest(buildPayload(values))
      message.success('已创建本地分析请求 JSON')
      await loadRequests(created.request_id)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to create local analysis request.')
    } finally {
      setCreating(false)
    }
  }

  async function handleOpen(record) {
    setSelectedRequestId(record.request_id)
    setError('')
    try {
      setDetail(await getAnalysisRequest(record.request_id))
    } catch (requestError) {
      setError(requestError?.message || 'Unable to open analysis request.')
    }
  }

  async function handleCancel() {
    if (!selectedRecord?.request_id) return
    setCanceling(true)
    setError('')
    try {
      const result = await cancelAnalysisRequest(selectedRecord.request_id)
      if (result.warning) {
        message.warning(result.warning)
      } else {
        message.success('已记录本地 canceled 状态；未调用 Provider')
      }
      await loadRequests(selectedRecord.request_id)
    } catch (requestError) {
      setError(requestError?.message || 'Unable to cancel local analysis request.')
    } finally {
      setCanceling(false)
    }
  }

  async function handleCopyRequestJson() {
    if (!selectedRecord?.request) return
    const text = JSON.stringify(selectedRecord.request, null, 2)
    try {
      await navigator.clipboard.writeText(text)
      message.success('Request JSON 已复制')
    } catch {
      message.warning('当前浏览器不允许复制，请在详情 JSON 区域手动选择。')
    }
  }

  const columns = [
    {
      title: 'Request',
      dataIndex: 'request_id',
      key: 'request_id',
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Text strong>{record.request?.case_seed?.title || record.request_id}</Text>
          <Text type="secondary">{record.request_id}</Text>
          <Space wrap size={4}>
            <Tag>{record.request?.sampling_plan?.sample_strategy || 'stratified_public_sample'}</Tag>
            {(record.request?.sampling_plan?.platforms || []).slice(0, 3).map((platform) => (
              <Tag key={platform} color="cyan">{platform}</Tag>
            ))}
          </Space>
        </Space>
      ),
    },
    {
      title: 'Created',
      dataIndex: 'created_at',
      key: 'created_at',
      width: 190,
      render: (value) => <Text>{value || '-'}</Text>,
    },
    {
      title: 'Provider result',
      key: 'provider',
      width: 260,
      render: (_, record) => (
        <Space direction="vertical" size={4}>
          <Space wrap size={4}>
            {statusTag(record.provider_status || record.request_status)}
            {safetyTag(record.safety_status)}
          </Space>
          <Text type="secondary">{record.package_name || record.result_warning || '等待手动放入 result JSON'}</Text>
        </Space>
      ),
    },
    {
      title: 'Action',
      key: 'action',
      width: 120,
      render: (_, record) => <Button onClick={() => handleOpen(record)}>查看</Button>,
    },
  ]

  const providerResult = selectedRecord?.provider_result
  const requestJson = selectedRecord?.request ? JSON.stringify(selectedRecord.request, null, 2) : ''
  const requestPath = selectedRecord?.request_file || 'runtime/analysis_requests/requests/<request_id>.json'

  return (
    <div className="page-stack analysis-requests-page">
      <section className="external-collector-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">file-based MVP</Tag>
            <Tag color="default">provider-agnostic</Tag>
            <Tag color="default">no provider execution</Tag>
          </Space>
          <Title level={1}>Analysis Requests / 分析任务请求</Title>
          <Paragraph>
            创建本地 <Text code>sentigraph_analysis_request_v1</Text> JSON，并读取手动放入的{' '}
            <Text code>sentigraph_provider_job_result_v1</Text>。外部 Provider 负责采样和生成 Evidence
            Package；当前页面不会运行 collector，不会抓取 URL，不会调用真实 API。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<RefreshCw size={16} />} loading={loading} onClick={() => loadRequests()}>
              刷新本地请求
            </Button>
            <Tag color={config?.configured_by_env ? 'blue' : 'default'}>
              {config?.configured_by_env ? 'custom local dir' : 'repo runtime dir'}
            </Tag>
            <Tag>{config?.root_label || 'runtime/analysis_requests'}</Tag>
          </Space>
        </div>
        <Card className="panel-card external-collector-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Local requests</Text>
            <Title level={2}>{config?.request_count ?? requests.length}</Title>
            <Text type="secondary">Provider results: {config?.result_count ?? 0}</Text>
            <Text type="secondary">Env: SENTIGRAPH_ANALYSIS_REQUESTS_DIR</Text>
          </Space>
        </Card>
      </section>

      <Alert
        type="info"
        showIcon
        message="Boundary / 边界"
        description={
          <Space wrap>
            {BOUNDARY_TAGS.map((item) => (
              <Tag key={item}>{item}</Tag>
            ))}
          </Space>
        }
      />
      <Alert
        type="warning"
        showIcon
        message="Provider execution is outside Sentigraph core"
        description="Sentigraph 只创建分析请求和接收 Evidence Package。平台访问、采样、安全门控、rate limit、snapshot/package 生成都属于外部 Provider；本页不会执行这些动作。"
      />
      {error ? <Alert type="error" showIcon message={error} /> : null}

      <Row gutter={[16, 16]}>
        <Col span={9}>
          <Card className="panel-card" title="创建分析请求">
            <Form
              form={form}
              layout="vertical"
              initialValues={DEFAULT_FORM_VALUES}
              onFinish={handleCreate}
            >
              <Form.Item name="title" label="事件标题" rules={[{ required: true, message: '请输入事件标题' }]}>
                <Input placeholder="例如：Helldivers PSN account linking controversy" />
              </Form.Item>
              <Form.Item name="description" label="事件描述">
                <TextArea rows={3} placeholder="简要说明事件背景和分析目的" />
              </Form.Item>
              <Form.Item name="keywords" label="关键词">
                <Select mode="tags" tokenSeparators={[',']} placeholder="helldivers, psn" />
              </Form.Item>
              <Form.Item name="negative_keywords" label="排除关键词">
                <Select mode="tags" tokenSeparators={[',']} placeholder="unrelated terms" />
              </Form.Item>
              <Form.Item name="language" label="语言">
                <Select mode="tags" tokenSeparators={[',']} options={[
                  { value: 'zh-CN', label: 'zh-CN' },
                  { value: 'en', label: 'en' },
                  { value: 'auto', label: 'auto' },
                ]} />
              </Form.Item>
              <Form.Item name="event_type" label="事件类型">
                <Select options={[
                  { value: 'public_opinion_event', label: 'public_opinion_event' },
                  { value: 'game_community_event', label: 'game_community_event' },
                  { value: 'brand_risk_event', label: 'brand_risk_event' },
                  { value: 'creator_community_event', label: 'creator_community_event' },
                ]} />
              </Form.Item>
              <Form.Item name="platforms" label="目标平台 / source hint">
                <Select mode="tags" tokenSeparators={[',']} placeholder="reddit, youtube, news_site" />
              </Form.Item>
              <Row gutter={10}>
                <Col span={8}>
                  <Form.Item name="target_comment_count" label="评论目标">
                    <InputNumber min={0} max={100000} className="full-width" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="target_source_count" label="来源目标">
                    <InputNumber min={0} max={10000} className="full-width" />
                  </Form.Item>
                </Col>
                <Col span={8}>
                  <Form.Item name="max_runtime_minutes" label="分钟预算">
                    <InputNumber min={1} max={1440} className="full-width" />
                  </Form.Item>
                </Col>
              </Row>
              <Form.Item name="sample_strategy" label="采样策略">
                <Select options={[
                  { value: 'stratified_public_sample', label: 'stratified_public_sample' },
                  { value: 'manual_snapshot', label: 'manual_snapshot' },
                  { value: 'provider_selected_sample', label: 'provider_selected_sample' },
                ]} />
              </Form.Item>
              <Card size="small" title="Safety policy">
                <Form.Item name="allow_manual_snapshot" valuePropName="checked">
                  <Checkbox>允许 manual snapshot</Checkbox>
                </Form.Item>
                <Form.Item name="allow_official_api" valuePropName="checked">
                  <Checkbox>允许已批准 official API</Checkbox>
                </Form.Item>
                <Form.Item name="allow_vendor_api" valuePropName="checked">
                  <Checkbox>允许已合规 vendor API</Checkbox>
                </Form.Item>
                <Form.Item name="allow_live_collection" valuePropName="checked">
                  <Checkbox>允许 live collection（默认关闭，仅作为请求字段）</Checkbox>
                </Form.Item>
                <Form.Item name="allow_saved_profile" valuePropName="checked">
                  <Checkbox>允许 saved profile（默认关闭，Sentigraph 不存储）</Checkbox>
                </Form.Item>
                <Form.Item name="minor_sensitive_mode" valuePropName="checked">
                  <Checkbox>minor_sensitive_mode</Checkbox>
                </Form.Item>
              </Card>
              <Space className="form-actions" wrap>
                <Button type="primary" htmlType="submit" loading={creating}>
                  创建分析请求
                </Button>
                <Button onClick={() => form.resetFields()}>重置</Button>
              </Space>
            </Form>
          </Card>
        </Col>

        <Col span={15}>
          <Card className="panel-card" title="本地请求列表">
            <Table
              rowKey="request_id"
              columns={columns}
              dataSource={requests}
              loading={loading}
              pagination={{ pageSize: 6 }}
              locale={{ emptyText: <Empty description="暂无本地 analysis request JSON" /> }}
            />
          </Card>

          <Card className="panel-card" title="Request / Provider result detail">
            {selectedRecord ? (
              <Space direction="vertical" size={14} className="full-width">
                <Space wrap>
                  <Tag color="cyan">{selectedRecord.request_id}</Tag>
                  {statusTag(selectedRecord.provider_status || selectedRecord.request_status)}
                  {safetyTag(selectedRecord.safety_status)}
                  {selectedRecord.package_name ? <Tag color="blue">{selectedRecord.package_name}</Tag> : null}
                </Space>
                <Row gutter={[12, 12]}>
                  <Col span={6}>
                    <Statistic title="Target comments" value={selectedRecord.request?.sampling_plan?.target_comment_count || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Target sources" value={selectedRecord.request?.sampling_plan?.target_source_count || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Result evidence" value={providerResult?.counts?.evidence || 0} />
                  </Col>
                  <Col span={6}>
                    <Statistic title="Result sources" value={providerResult?.counts?.sources || 0} />
                  </Col>
                </Row>
                <Descriptions column={1} size="small">
                  <Descriptions.Item label="title">{selectedRecord.request?.case_seed?.title || ''}</Descriptions.Item>
                  <Descriptions.Item label="request_file">{requestPath}</Descriptions.Item>
                  <Descriptions.Item label="result_file">
                    {selectedRecord.result_file || 'runtime/analysis_requests/results/<request_id>.json'}
                  </Descriptions.Item>
                  <Descriptions.Item label="provider execution">outside Sentigraph core</Descriptions.Item>
                  <Descriptions.Item label="privacy">
                    raw identity fields removed: {String(selectedRecord.request?.privacy_policy?.remove_raw_author_id !== false)}
                  </Descriptions.Item>
                </Descriptions>
                {selectedRecord.result_warning ? (
                  <Alert type="warning" showIcon message="Provider result warning" description={selectedRecord.result_warning} />
                ) : null}
                {providerResult ? (
                  <Alert
                    type={providerResult.status === 'package_ready' ? 'success' : 'info'}
                    showIcon
                    message={`Provider result: ${providerResult.status}`}
                    description={
                      <Space direction="vertical" size={4}>
                        <Text>package: {providerResult.package_name || 'not provided'}</Text>
                        <Text>coverage: {providerResult.coverage?.coverage_level || 'selected_public_sample'}</Text>
                        <Text>
                          validation: {providerResult.validation?.status || 'unknown'} /
                          errors {providerResult.validation?.errors || 0} /
                          warnings {providerResult.validation?.warnings || 0}
                        </Text>
                      </Space>
                    }
                  />
                ) : (
                  <Alert
                    type="info"
                    showIcon
                    message="等待外部 Provider result JSON"
                    description="如果外部 Provider 手动写入 runtime/analysis_requests/results/<request_id>.json，本页会读取并展示状态；不会启动 Provider。"
                  />
                )}
                <Alert
                  type="info"
                  showIcon
                  message="Coverage / trust note"
                  description="Provider 输出仍是 evidence，不是 official truth。导入 case 前仍需 validation、trust/provenance、review、dedup、coverage 和 audit。"
                />
                <Space wrap>
                  <Button icon={<ClipboardCopy size={16} />} onClick={handleCopyRequestJson}>
                    复制 request JSON
                  </Button>
                  <Button icon={<XCircle size={16} />} loading={canceling} onClick={handleCancel}>
                    本地取消请求
                  </Button>
                  <Button icon={<RefreshCw size={16} />} onClick={() => handleOpen(selectedRecord)}>
                    刷新详情
                  </Button>
                </Space>
                <Card size="small" title={<Space><FileJson size={16} />Request JSON preview</Space>}>
                  <pre className="code-preview">{requestJson}</pre>
                </Card>
              </Space>
            ) : (
              <Empty description="创建或选择一个本地分析请求" />
            )}
          </Card>
        </Col>
      </Row>

      <Card className="panel-card" title={<Space><ShieldCheck size={17} />Intentional non-goals</Space>}>
        <Space wrap>
          <Tag>no provider execution</Tag>
          <Tag>no collector jobs</Tag>
          <Tag>no subprocess provider execution</Tag>
          <Tag>no live collection</Tag>
          <Tag>no URL fetching</Tag>
          <Tag>no scraping</Tag>
          <Tag>no real API calls</Tag>
          <Tag>no real LLM</Tag>
          <Tag>no Project Source changes</Tag>
        </Space>
      </Card>
    </div>
  )
}
