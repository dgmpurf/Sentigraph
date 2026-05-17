import { Alert, Button, Card, Col, Empty, Row, Skeleton, Space, Table, Tag, Typography } from 'antd'
import {
  AlertTriangle,
  BarChart3,
  CheckCircle2,
  GitCompareArrows,
  History,
  RefreshCw,
  ShieldAlert,
  TimerReset,
} from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import {
  getBenchmarkHistory,
  getBenchmarkRegression,
  getLatestBenchmarkSummary,
} from '../api/sentigraphApi.js'

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

function formatDuration(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? `${numericValue.toFixed(2)}s` : '-'
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return String(value)
  return date.toLocaleString('zh-CN', { hour12: false })
}

function getRegressionDisplay(regression) {
  if (!regression || regression.status === 'no_history' || regression.available === false) {
    return {
      label: '无历史记录可比较',
      color: 'default',
      detail: '至少运行两次离线评测后，系统才会比较最近两次结果。',
    }
  }
  if (regression.regression_detected) {
    return {
      label: '发现回归风险',
      color: 'red',
      detail: '失败、警告或套件状态出现退化，请优先查看变化套件。',
    }
  }
  return {
    label: '无回归',
    color: 'green',
    detail: '最近一次离线评测相对上一轮没有发现退化。',
  }
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

function MetricCards({ regression, summary }) {
  const regressionDisplay = getRegressionDisplay(regression)

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} md={12} xl={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <CheckCircle2 size={18} />
            <Text>总通过</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_passed)}</Title>
          <Text type="secondary">离线套件通过断言数</Text>
        </Card>
      </Col>
      <Col xs={24} md={12} xl={6}>
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
      <Col xs={24} md={12} xl={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <AlertTriangle size={18} />
            <Text>警告</Text>
          </Space>
          <Title level={2}>{formatNumber(summary?.total_warnings)}</Title>
          <Text type="secondary">仅展示套件级 warning，不展示 case payload</Text>
        </Card>
      </Col>
      <Col xs={24} md={12} xl={6}>
        <Card className="metric-card benchmark-metric-card">
          <Space className="metric-heading">
            <GitCompareArrows size={18} />
            <Text>回归检测</Text>
          </Space>
          <Title level={2}>{regressionDisplay.label}</Title>
          <Tag color={regressionDisplay.color}>是否退化</Tag>
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

function RegressionPanel({ regression }) {
  const regressionDisplay = getRegressionDisplay(regression)
  const changedSuites = Array.isArray(regression?.changed_suites) ? regression.changed_suites : []
  const failedDelta =
    regression?.previous_total_failed === null || regression?.previous_total_failed === undefined
      ? null
      : regression.latest_total_failed - regression.previous_total_failed
  const warningDelta =
    regression?.previous_total_warnings === null || regression?.previous_total_warnings === undefined
      ? null
      : regression.latest_total_warnings - regression.previous_total_warnings

  return (
    <Card className="panel-card benchmark-regression-card">
      <div className="panel-heading">
        <Space>
          <GitCompareArrows size={18} />
          <Title level={4}>回归检测</Title>
        </Space>
        <Tag color={regressionDisplay.color}>{regressionDisplay.label}</Tag>
      </div>
      <Row gutter={[12, 12]} className="benchmark-regression-metrics">
        <Col xs={12} lg={6}>
          <div>
            <Text type="secondary">是否退化</Text>
            <Title level={5}>{regression?.regression_detected ? '是' : '否'}</Title>
          </div>
        </Col>
        <Col xs={12} lg={6}>
          <div>
            <Text type="secondary">新增失败</Text>
            <Title level={5}>{failedDelta === null ? '-' : formatNumber(Math.max(0, failedDelta))}</Title>
          </div>
        </Col>
        <Col xs={12} lg={6}>
          <div>
            <Text type="secondary">警告变化</Text>
            <Title level={5}>{warningDelta === null ? '-' : formatNumber(warningDelta)}</Title>
          </div>
        </Col>
        <Col xs={12} lg={6}>
          <div>
            <Text type="secondary">套件变化</Text>
            <Title level={5}>{formatNumber(changedSuites.length)}</Title>
          </div>
        </Col>
      </Row>
      <Paragraph className="benchmark-summary-copy">{regressionDisplay.detail}</Paragraph>
      {changedSuites.length ? (
        <div className="benchmark-change-list">
          {changedSuites.map((change) => (
            <Card size="small" className="benchmark-change-card" key={change.suite}>
              <Space direction="vertical" size={6}>
                <Space wrap>
                  <Text strong>{SUITE_LABELS[change.suite] || change.suite}</Text>
                  <Tag color="red">
                    {safeText(change.previous_status)}{' -> '}{safeText(change.latest_status)}
                  </Tag>
                </Space>
                <Space wrap size={6}>
                  {change.change_types.map((changeType) => (
                    <Tag color="orange" key={`${change.suite}-${changeType}`}>
                      {changeType}
                    </Tag>
                  ))}
                </Space>
                <Text type="secondary">
                  failed {formatNumber(change.previous_failed)}{' -> '}{formatNumber(change.latest_failed)} / warnings{' '}
                  {formatNumber(change.previous_warnings)}{' -> '}{formatNumber(change.latest_warnings)}
                </Text>
              </Space>
            </Card>
          ))}
        </div>
      ) : null}
    </Card>
  )
}

function HistoryTable({ history }) {
  const historyRows = Array.isArray(history?.entries) ? history.entries : []
  const columns = [
    {
      title: 'generated_at',
      dataIndex: 'generated_at',
      key: 'generated_at',
      width: 220,
      render: (value, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{formatDate(value)}</Text>
          <Text type="secondary">{safeText(record.benchmark_id)}</Text>
        </Space>
      ),
    },
    {
      title: '总通过',
      dataIndex: 'total_passed',
      key: 'total_passed',
      width: 110,
      render: (value) => <Text strong>{formatNumber(value)}</Text>,
    },
    {
      title: '总失败',
      dataIndex: 'total_failed',
      key: 'total_failed',
      width: 110,
      render: (value) => <Tag color={value > 0 ? 'red' : 'green'}>{formatNumber(value)}</Tag>,
    },
    {
      title: '警告',
      dataIndex: 'total_warnings',
      key: 'total_warnings',
      width: 110,
      render: (value) => <Tag color={value > 0 ? 'orange' : 'default'}>{formatNumber(value)}</Tag>,
    },
    {
      title: 'duration',
      dataIndex: 'duration_seconds',
      key: 'duration_seconds',
      width: 110,
      render: (value) => <Text>{formatDuration(value)}</Text>,
    },
    {
      title: '回归检测',
      dataIndex: 'regression_detected',
      key: 'regression_detected',
      width: 130,
      render: (value) => {
        if (value === null || value === undefined) return <Tag>未记录</Tag>
        return <Tag color={value ? 'red' : 'green'}>{value ? '发现回归风险' : '无回归'}</Tag>
      },
    },
  ]

  return (
    <Card className="panel-card benchmark-history-card">
      <div className="panel-heading">
        <Space>
          <History size={18} />
          <Title level={4}>历史记录</Title>
        </Space>
        <Space wrap>
          <Tag color="cyan">{formatNumber(history?.total_entries)} runs</Tag>
          {history?.malformed_entries ? <Tag color="orange">{history.malformed_entries} malformed skipped</Tag> : null}
        </Space>
      </div>
      {historyRows.length ? (
        <Table
          columns={columns}
          dataSource={historyRows}
          pagination={{ pageSize: 6, size: 'small' }}
          rowKey="benchmark_id"
          scroll={{ x: 900 }}
        />
      ) : (
        <Empty
          description="暂无历史记录。运行两次 python scripts/run_offline_benchmarks.py 后可查看趋势。"
          image={Empty.PRESENTED_IMAGE_SIMPLE}
        />
      )}
    </Card>
  )
}

export function BenchmarkDashboard() {
  const [summary, setSummary] = useState(null)
  const [history, setHistory] = useState(null)
  const [regression, setRegression] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  const loadBenchmarkState = useCallback(async () => {
    setLoading(true)
    setError('')
    try {
      const [summaryResponse, historyResponse, regressionResponse] = await Promise.all([
        getLatestBenchmarkSummary(),
        getBenchmarkHistory(),
        getBenchmarkRegression(),
      ])
      setSummary(summaryResponse)
      setHistory(historyResponse)
      setRegression(regressionResponse)
    } catch (requestError) {
      setSummary(null)
      setHistory(null)
      setRegression(null)
      const status = requestError?.response?.status
      if (status === 404) {
        setError(
          '后端尚未加载 benchmark history/regression API。请重启 backend server 后再刷新；这些接口不会自动运行 benchmark。',
        )
      } else {
        setError(requestError?.message || '离线评测结果加载失败，请确认后端服务已启动。')
      }
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    loadBenchmarkState()
  }, [loadBenchmarkState])

  const suiteRows = useMemo(() => buildSuiteRows(summary), [summary])
  const regressionDisplay = useMemo(() => getRegressionDisplay(regression), [regression])

  const suiteColumns = [
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
          <Text>
            展示 scripts/run_offline_benchmarks.py 最近生成的 benchmark summary、历史记录与回归检测；页面只读取结果，不会触发评测或外部调用。
          </Text>
        </div>
        <Space wrap>
          <Tag color="cyan" className="large-tag">Benchmarks</Tag>
          <Tag color="green" className="large-tag">Offline Only</Tag>
          <Button icon={<RefreshCw size={16} />} loading={loading} onClick={loadBenchmarkState}>
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
                <Tag color={regressionDisplay.color}>回归检测: {regressionDisplay.label}</Tag>
              </Space>
            </div>
            <Paragraph className="benchmark-summary-copy">
              生成时间：{formatDate(summary.generated_at)}。耗时：{formatDuration(summary.duration_seconds)}。
              该接口只读取 .benchmarks 下的安全汇总字段，不返回 benchmark case 明细、原始文本、prompt 或凭证。
            </Paragraph>
          </Card>

          <MetricCards regression={regression} summary={summary} />
          <RegressionPanel regression={regression} />

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
              columns={suiteColumns}
              dataSource={suiteRows}
              pagination={false}
              rowKey="suite"
              scroll={{ x: 920 }}
            />
          </Card>

          <HistoryTable history={history} />
        </>
      ) : (
        <EmptyBenchmarkState summary={summary} />
      )}
    </div>
  )
}
