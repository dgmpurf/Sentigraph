import { Alert, Button, Card, Col, Empty, List, Row, Skeleton, Space, Table, Tag, Typography } from 'antd'
import { BrainCircuit, KeyRound, RefreshCw, ShieldCheck, ShieldOff, TimerReset } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import { getLlmStatus, getLlmUsage } from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const providerTone = {
  mock_ready: 'green',
  provider_not_enabled: 'default',
  not_configured: 'orange',
  unknown_provider: 'red',
}

function safeText(value, fallback = '-') {
  if (value === null || value === undefined || value === '') return fallback
  return String(value)
}

function formatNumber(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toLocaleString('zh-CN') : '0'
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString('zh-CN', { hour12: false })
}

function booleanTag(value, trueText, falseText) {
  return <Tag color={value ? 'green' : 'default'}>{value ? trueText : falseText}</Tag>
}

function statusTag(status) {
  return <Tag color={providerTone[status] || 'default'}>{safeText(status)}</Tag>
}

function SafetyNotice() {
  const notices = [
    '当前默认使用 MockProvider',
    '不调用真实大模型',
    '不显示 API key',
    '不记录原始 prompt',
    '真实调用需要未来显式开启',
  ]

  return (
    <Card className="panel-card llm-safety-card">
      <div className="panel-heading">
        <Space>
          <ShieldCheck size={18} />
          <Title level={4}>安全边界</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">Mock 模式</Tag>
          <Tag color="green">不记录原始 Prompt</Tag>
        </Space>
      </div>
      <Space wrap>
        {notices.map((notice) => (
          <Tag color="geekblue" key={notice}>
            {notice}
          </Tag>
        ))}
      </Space>
    </Card>
  )
}

function MetricCards({ status, usage }) {
  const realCallsEnabled = Boolean(status?.real_calls_enabled)
  const trackingEnabled = status?.tracking_enabled ?? usage?.tracking_enabled

  return (
    <Row gutter={[16, 16]}>
      <Col span={6}>
        <Card className="metric-card llm-metric-card">
          <Space className="metric-heading">
            <BrainCircuit size={18} />
            <Text>当前 Provider</Text>
          </Space>
          <Title level={2}>{safeText(status?.provider_name, 'mock')}</Title>
          <Space wrap>
            {statusTag(status?.provider_status || 'unknown')}
            <Tag color={status?.provider_name === 'mock' ? 'cyan' : 'default'}>Mock 模式</Tag>
          </Space>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card llm-metric-card">
          <Space className="metric-heading">
            {realCallsEnabled ? <ShieldOff size={18} /> : <ShieldCheck size={18} />}
            <Text>真实调用</Text>
          </Space>
          <Title level={2}>{realCallsEnabled ? 'Enabled' : 'Disabled'}</Title>
          {booleanTag(realCallsEnabled, '真实调用已启用', '安全关闭')}
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card llm-metric-card">
          <Space className="metric-heading">
            <TimerReset size={18} />
            <Text>调用次数</Text>
          </Space>
          <Title level={2}>{formatNumber(usage?.daily_calls)}</Title>
          <Text type="secondary">
            今日限制 {formatNumber(status?.daily_call_limit ?? usage?.daily_call_limit)}
          </Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card llm-metric-card">
          <Space className="metric-heading">
            <KeyRound size={18} />
            <Text>API Key 状态</Text>
          </Space>
          <Title level={2}>{status?.api_key_present ? 'Present' : 'Missing'}</Title>
          <Space wrap>
            {booleanTag(status?.api_key_present, '存在', '未配置 / 不需要')}
            {booleanTag(trackingEnabled, '追踪开启', '追踪关闭')}
          </Space>
        </Card>
      </Col>
    </Row>
  )
}

function ProviderCards({ providers = [], currentProvider }) {
  if (!providers.length) {
    return <Empty description="暂无 Provider 状态" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  return (
    <div className="llm-provider-grid">
      {providers.map((provider) => (
        <div
          className={provider.provider_name === currentProvider ? 'llm-provider-card active' : 'llm-provider-card'}
          key={provider.provider_name}
        >
          <div className="llm-provider-card-header">
            <Space direction="vertical" size={2}>
              <Text strong>{safeText(provider.provider_name)}</Text>
              <Text type="secondary">Provider status</Text>
            </Space>
            {statusTag(provider.provider_status)}
          </div>
          <Space wrap size={6}>
            {booleanTag(provider.real_calls_enabled, '真实调用开启', '真实调用关闭')}
            {booleanTag(provider.api_key_present, 'API Key 存在', provider.api_key_required ? 'API Key 缺失' : '无需 API Key')}
            {booleanTag(provider.available, '可用', '未启用')}
          </Space>
          <Paragraph className="llm-provider-note">
            {provider.provider_name === 'mock'
              ? '离线确定性 MockProvider，当前 MVP 默认使用。'
              : '真实 provider 仍是未来占位；未显式开启前不会调用外部服务。'}
          </Paragraph>
        </div>
      ))}
    </div>
  )
}

function UsageSummary({ status, usage }) {
  const callLimit = status?.daily_call_limit ?? usage?.daily_call_limit
  const tokenLimit = status?.daily_token_limit ?? usage?.daily_token_limit
  const maxInputChars = status?.max_input_chars ?? usage?.max_input_chars

  return (
    <div className="llm-usage-summary">
      <div>
        <Text type="secondary">调用次数</Text>
        <Text strong>{formatNumber(usage?.daily_calls)} / {formatNumber(callLimit)}</Text>
      </div>
      <div>
        <Text type="secondary">Token 估算</Text>
        <Text strong>{formatNumber(usage?.daily_total_tokens)} / {formatNumber(tokenLimit)}</Text>
      </div>
      <div>
        <Text type="secondary">输入 Token</Text>
        <Text strong>{formatNumber(usage?.daily_input_tokens)}</Text>
      </div>
      <div>
        <Text type="secondary">输出 Token</Text>
        <Text strong>{formatNumber(usage?.daily_output_tokens)}</Text>
      </div>
      <div>
        <Text type="secondary">最大输入字符</Text>
        <Text strong>{formatNumber(maxInputChars)}</Text>
      </div>
      <div>
        <Text type="secondary">Guardrail</Text>
        <Tag color="cyan">{safeText(status?.guardrail_mode ?? usage?.guardrail_mode, 'mock')}</Tag>
      </div>
    </div>
  )
}

function UsageRecords({ records = [] }) {
  if (!records.length) {
    return <Empty description="暂无 LLM mock usage 记录" image={Empty.PRESENTED_IMAGE_SIMPLE} />
  }

  const columns = [
    {
      title: 'Provider',
      dataIndex: 'provider',
      key: 'provider',
      width: 120,
      render: (value) => <Tag color="cyan">{safeText(value)}</Tag>,
    },
    {
      title: 'Operation',
      dataIndex: 'operation',
      key: 'operation',
      width: 210,
      render: (value) => <Text>{safeText(value)}</Text>,
    },
    {
      title: '字符数',
      key: 'chars',
      width: 160,
      render: (_, record) => (
        <Text type="secondary">
          in {formatNumber(record.input_chars)} / out {formatNumber(record.output_chars)}
        </Text>
      ),
    },
    {
      title: 'Token 估算',
      key: 'tokens',
      width: 180,
      render: (_, record) => (
        <Text type="secondary">
          {formatNumber(record.estimated_input_tokens + record.estimated_output_tokens)}
        </Text>
      ),
    },
    {
      title: '结果',
      key: 'success',
      width: 130,
      render: (_, record) => (
        <Space wrap size={4}>
          {booleanTag(record.success, 'success', 'failure')}
          {record.failure_category ? <Tag color="orange">{record.failure_category}</Tag> : null}
        </Space>
      ),
    },
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 210,
      render: (value) => <Text type="secondary">{formatDate(value)}</Text>,
    },
  ]

  return (
    <Table
      columns={columns}
      dataSource={records}
      pagination={false}
      rowKey="record_key"
      scroll={{ x: 1010 }}
    />
  )
}

function SafetyFlags({ flags = {} }) {
  const items = [
    ['mock_default', 'Mock 默认'],
    ['real_calls_disabled_by_default', '真实调用默认关闭'],
    ['api_key_values_exposed', 'API key 值暴露'],
    ['raw_prompt_logging', '原始 Prompt 记录'],
    ['raw_user_content_logging', '原始用户内容记录'],
  ]

  return (
    <List
      className="llm-safety-list"
      dataSource={items}
      renderItem={([key, label]) => {
        const value = Boolean(flags[key])
        const safeNegative = key.includes('exposed') || key.includes('logging')
        const ok = safeNegative ? !value : value
        return (
          <List.Item>
            <Space className="full-width" align="center">
              <Text>{label}</Text>
              <Tag color={ok ? 'green' : 'red'}>{ok ? '安全' : '需检查'}</Tag>
            </Space>
          </List.Item>
        )
      }}
    />
  )
}

export function LlmAdminStatus() {
  const [status, setStatus] = useState(null)
  const [usage, setUsage] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [warning, setWarning] = useState('')

  const loadStatus = useCallback(async () => {
    setLoading(true)
    setError('')
    setWarning('')

    const [statusResult, usageResult] = await Promise.allSettled([getLlmStatus(), getLlmUsage()])
    const nextStatus = statusResult.status === 'fulfilled' ? statusResult.value : null
    const nextUsage = usageResult.status === 'fulfilled' ? usageResult.value : null

    setStatus(nextStatus)
    setUsage(nextUsage)

    const warnings = []
    if (statusResult.status === 'rejected') warnings.push('GET /api/v1/llm/status 加载失败')
    if (usageResult.status === 'rejected') warnings.push('GET /api/v1/llm/usage 加载失败')
    setWarning(warnings.join('；'))

    if (!nextStatus && !nextUsage) {
      setError('大模型安全状态加载失败，请确认后端服务已启动。')
    }
    setLoading(false)
  }, [])

  useEffect(() => {
    loadStatus()
  }, [loadStatus])

  const providers = useMemo(() => status?.providers || [], [status])
  const records = useMemo(() => usage?.recent_records || [], [usage])

  return (
    <div className="page-stack llm-admin-page">
      <div className="page-heading">
        <div>
          <Title level={2}>大模型安全状态</Title>
          <Text>查看 MockProvider、未来真实 Provider 占位状态与 metadata-only 使用量；此页面不会开启真实调用。</Text>
        </div>
        <Space wrap>
          <Tag color="cyan" className="large-tag">LLM Safety</Tag>
          <Tag color="green" className="large-tag">不显示 API key</Tag>
          <Button icon={<RefreshCw size={16} />} loading={loading} onClick={loadStatus}>
            刷新
          </Button>
        </Space>
      </div>

      <SafetyNotice />

      {error ? <Alert message="大模型安全状态加载失败" description={error} type="error" showIcon /> : null}
      {warning ? <Alert message="部分 LLM 状态接口加载失败" description={warning} type="warning" showIcon /> : null}

      {loading && !status && !usage ? (
        <Card className="panel-card">
          <Skeleton active paragraph={{ rows: 10 }} title />
        </Card>
      ) : (
        <>
          <MetricCards status={status} usage={usage} />

          <Row gutter={[16, 16]}>
            <Col span={16}>
              <Card className="panel-card llm-provider-section">
                <div className="panel-heading">
                  <Space>
                    <BrainCircuit size={18} />
                    <Title level={4}>Provider 状态</Title>
                  </Space>
                  <Space wrap>
                    <Tag color="cyan">available: {(status?.available_providers || []).join(', ') || '-'}</Tag>
                    <Tag color={status?.real_calls_enabled ? 'red' : 'green'}>
                      {status?.real_calls_enabled ? '真实调用开启' : '安全关闭'}
                    </Tag>
                  </Space>
                </div>
                <ProviderCards providers={providers} currentProvider={status?.provider_name} />
              </Card>
            </Col>
            <Col span={8}>
              <Card className="panel-card llm-safety-flags-card">
                <div className="panel-heading">
                  <Space>
                    <ShieldCheck size={18} />
                    <Title level={4}>安全检查</Title>
                  </Space>
                  <Tag color="green">no raw prompt</Tag>
                </div>
                <SafetyFlags flags={status?.safety_flags || {}} />
              </Card>
            </Col>
          </Row>

          <Card className="panel-card llm-usage-card">
            <div className="panel-heading">
              <Space>
                <TimerReset size={18} />
                <Title level={4}>调用次数 / Token 估算</Title>
              </Space>
              <Space wrap>
                {booleanTag(usage?.tracking_enabled ?? status?.tracking_enabled, 'usage tracking enabled', 'usage tracking disabled')}
                <Tag color="default">不记录原始 Prompt</Tag>
              </Space>
            </div>
            <UsageSummary status={status} usage={usage} />
          </Card>

          <Card className="panel-card llm-usage-card">
            <div className="panel-heading">
              <Space>
                <TimerReset size={18} />
                <Title level={4}>最近 mock usage 记录</Title>
              </Space>
              <Tag>{records.length} records</Tag>
            </div>
            <UsageRecords records={records} />
          </Card>
        </>
      )}
    </div>
  )
}
