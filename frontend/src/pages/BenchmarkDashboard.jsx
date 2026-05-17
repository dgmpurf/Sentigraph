import { Alert, Button, Card, Col, Empty, Row, Skeleton, Space, Table, Tag, Typography } from 'antd'
import { AlertTriangle, BarChart3, CheckCircle2, RefreshCw, ShieldAlert, TimerReset } from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import { getLatestBenchmarkSummary } from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const SUITE_ORDER = [
  'sentiment',
  'topic_cluster',
  'topic_risk',
  'report_builder',
  'markdown_export',
  'selector_repair',
  'public_parser_fixtures',
  'platform_adapter_mocks',
]

const SUITE_LABELS = {
  sentiment: 'Sentiment',
  topic_cluster: 'Topic Cluster',
  topic_risk: 'V1.5 Topic Risk',
  report_builder: 'Report Builder',
  markdown_export: 'Markdown Export',
  selector_repair: 'Selector Repair',
  public_parser_fixtures: 'Public Parser Fixtures',
  platform_adapter_mocks: 'Platform Adapter Mocks',
}

const statusTone = {
  pass: 'green',
  fail: 'red',
  missing: 'default',
  unknown: 'default',
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

function getRegressionRisk(summary) {
  if (!summary?.available) return { label: '无结果', color: 'default', detail: '请先运行离线评测脚本。' }
  if (summary.total_failed > 0) {
    return { label: '高', color: 'red', detail: '存在失败项，需要优先排查。' }
  }
  if (summary.total_warnings > 0) {
    return { label: '中', color: 'gold', detail: '测试通过但存在警告，建议复核。' }
  }
  return { label: '低', color: 'green', detail: '当前离线评测全部通过。' }
}

function buildSuiteRows(summary) {
  const suites = Array.isArray(summary?.suites) ? summary.suites : []
  const suiteMap = new Map(suites.map((suite) => [suite.suite, suite]))
  const orderedRows = SUITE_ORDER.map((suiteName) => ({
    suite: suiteName,
    status: 'missing',
    passed: 0,
    failed: 0,
    warnings: [],
    ...suiteMap.get(suiteName),
  }))
  const extras = suites.filter((suite) => !SUITE_ORDER.includes(suite.suite))
  return [...orderedRows, ...extras]
}

function MetricCards({ summary }) {
  const regressionRisk = getRegressionRisk(summary)

  return (
    <Row gutter={[16, 16]}>
      <Col span={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <CheckCircle2 size={18} />
            <Text>总通过</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_passed)}</Title>
          <Text type="secondary">离线套件通过断言数。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <ShieldAlert size={18} />
            <Text>总失败</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_failed)}</Title>
          <Tag color={summary?.total_failed > 0 ? 'red' : 'green'}>
            {summary?.total_failed > 0 ? '需要处理' : '无失败'}
          </Tag>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <AlertTriangle size={18} />
            <Text>警告</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_warnings)}</Title>
          <Text type="secondary">仅展示套件级 warning，不展示 case payload。</Text>
        </Card>
      </Col>
      <Col span={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <BarChart3 size={18} />
            <Text>回归风险</Text>
          </Space>
          <Title level={2}>{regressionRisk.label}</Title>
          <Tag color={regressionRisk.color}>{regressionRisk.detail}</Tag>
        </Card>
      </Col>
    </Row>
  )
}

function EmptyBenchmarkState({ summary }) {
  return (
    <Card className="panel-card benchmark-empty-card">
      <Empty
        description={
          <Space direction="vertical" size={8}>
            <Text>{safeText(summary?.message, '尚未生成离线评测结果。')}</Text>
            <Text code>python scripts/run_offline_benchmarks.py</Text>
          </Space>
        }
        image={Empty.PRESENTED_IMAGE_SIMPLE}
      />
    </Card>
  )
}

function SuiteWarnings({ warnings = [] }) {
  if (!warnings.length) return <Text type="secondary">-</Text>
  return (
    <Space wrap size={4}>
      {warnings.map((warning) => (
        <Tag color="orange" key={warning}>
          {warning}
        </Tag>
      ))}
    </Space>
  )
}

export function BenchmarkDashboard() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadSummary = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const response = await getLatestBenchmarkSummary()
      setSummary(response)
    } catch (requestError) {
      setSummary(null)
      const status = requestError?.response?.status
      if (status === 404) {
        setError('后端尚未加载 /api/v1/benchmarks/latest。请重启 backend server 后再刷新；该接口不会自动运行 benchmark。')
      } else {
        setError(requestError?.message || '离线评测结果加载失败，请确认后端服务已启动。')
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadSummary()
  }, [loadSummary])

  const suiteRows = useMemo(() => buildSuiteRows(summary), [summary])
  const regressionRisk = useMemo(() => getRegressionRisk(summary), [summary])

  const columns = [
    {
      title: '评测套件',
      dataIndex: 'suite',
      key: 'suite',
      width: 260,
      render: (value) => (
        <Space direction="vertical" size={2}>
          <Text strong>{SUITE_LABELS[value] || safeText(value)}</Text>
          <Text type="secondary">{safeText(value)}</Text>
        </Space>
      ),
    },
    {
      title: '当前状态',
      dataIndex: 'status',
      key: 'status',
      width: 130,
      render: (value) => <Tag color={statusTone[value] || 'default'}>{safeText(value)}</Tag>,
    },
    {
      title: '通过',
      dataIndex: 'passed',
      key: 'passed',
      width: 120,
      render: (value) => <Text strong>{formatNumber(value)}</Text>,
    },
    {
      title: '失败',
      dataIndex: 'failed',
      key: 'failed',
      width: 120,
      render: (value) => <Tag color={value > 0 ? 'red' : 'green'}>{formatNumber(value)}</Tag>,
    },
    {
      title: '警告',
      key: 'warnings',
      render: (_, record) => <SuiteWarnings warnings={record.warnings || []} />,
    },
  ]

  return (
    <div className="page-stack benchmark-dashboard-page">
      <div className="page-heading">
        <div>
          <Title level={2}>离线评测</Title>
          <Text>展示 scripts/run_offline_benchmarks.py 最近生成的 benchmark summary；页面只读取结果，不会触发评测或外部调用。</Text>
        </div>
        <Space wrap>
          <Tag color="cyan" className="large-tag">Benchmarks</Tag>
          <Tag color="green" className="large-tag">Offline Only</Tag>
          <Button icon={<RefreshCw size={16} />} loading={loading} onClick={loadSummary}>
            刷新
          </Button>
        </Space>
      </div>

      {error ? <Alert message="离线评测加载失败" description={error} type="error" showIcon /> : null}

      {loading && !summary ? (
        <Card className="panel-card">
          <Skeleton active paragraph={{ rows: 10 }} title />
        </Card>
      ) : summary?.available ? (
        <>
          <Card className="panel-card benchmark-status-card">
            <div className="panel-heading">
              <Space>
                <TimerReset size={18} />
                <Title level={4}>最近结果</Title>
              </Space>
              <Space wrap>
                <Tag color="cyan">source: {safeText(summary.source)}</Tag>
                <Tag>{safeText(summary.benchmark_version)}</Tag>
                <Tag color={regressionRisk.color}>回归风险: {regressionRisk.label}</Tag>
              </Space>
            </div>
            <Paragraph className="benchmark-summary-copy">
              生成时间：{formatDate(summary.generated_at)}。该接口只读取 .benchmarks/offline_benchmark_summary.json
              的安全汇总字段，不返回 benchmark case 明细、原始文本、prompt 或凭证。
            </Paragraph>
          </Card>

          <MetricCards summary={summary} />

          <Card className="panel-card benchmark-suite-card">
            <div className="panel-heading">
              <Space>
                <BarChart3 size={18} />
                <Title level={4}>评测套件</Title>
              </Space>
              <Space wrap>
                <Tag color="green">{formatNumber(summary.total_passed)} passed</Tag>
                <Tag color={summary.total_failed > 0 ? 'red' : 'default'}>
                  {formatNumber(summary.total_failed)} failed
                </Tag>
                <Tag color={summary.total_warnings > 0 ? 'orange' : 'default'}>
                  {formatNumber(summary.total_warnings)} warnings
                </Tag>
              </Space>
            </div>
            <Table
              columns={columns}
              dataSource={suiteRows}
              pagination={false}
              rowKey="suite"
              scroll={{ x: 920 }}
            />
          </Card>
        </>
      ) : (
        <EmptyBenchmarkState summary={summary} />
      )}
    </div>
  )
}
