import { Alert, Button, Card, Empty, Space, Table, Tag, Typography } from 'antd'
import { FileText, PlayCircle, RefreshCw } from 'lucide-react'

import { riskTone } from '../utils/formatters.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'

const { Text, Title } = Typography

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

const statusLabels = {
  draft: '待运行',
  running: '运行中',
  completed: '已完成',
  failed: '失败',
}

const statusColors = {
  draft: 'default',
  running: 'processing',
  completed: 'success',
  failed: 'error',
}

function formatScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '-'
}

function formatDate(value) {
  if (!value) return '-'
  const date = new Date(value)
  if (Number.isNaN(date.getTime())) return value
  return date.toLocaleString()
}

function buildEvidenceSummary(items = []) {
  const sourceDistribution = {}
  const typeCounts = {}
  const acquisitionModes = {}
  const titles = []
  const comments = []
  for (const item of Array.isArray(items) ? items : []) {
    const source = item.source_type || 'unknown'
    const type = item.evidence_type || 'unknown'
    const acquisitionMode = item.acquisition_mode || 'unknown'
    sourceDistribution[source] = (sourceDistribution[source] || 0) + 1
    typeCounts[type] = (typeCounts[type] || 0) + 1
    acquisitionModes[acquisitionMode] = (acquisitionModes[acquisitionMode] || 0) + 1
    if (item.title && !titles.includes(item.title)) titles.push(item.title)
    const comment = item.comment_text || item.body_text
    if (comment && !comments.includes(comment)) comments.push(comment)
  }
  return {
    acquisitionModes,
    comments: comments.slice(0, 3),
    sourceDistribution,
    titles: titles.slice(0, 3),
    typeCounts,
  }
}

function DistributionTags({ color = 'blue', values = {} }) {
  const entries = Object.entries(values)
  if (!entries.length) return <Text type="secondary">none</Text>
  return (
    <Space size={[4, 4]} wrap>
      {entries.map(([key, value]) => (
        <Tag color={color} key={key}>
          {key}: {value}
        </Tag>
      ))}
    </Space>
  )
}

export function Cases({
  cases = [],
  currentCase,
  error,
  loading,
  onNavigateToKeyword,
  onOpenCaseReport,
  onRefreshCases,
  onRunCase,
}) {
  const sourceStatus = getAnalysisSourceStatus({
    analysis: currentCase?.analysis_result,
    currentCase,
  })
  const evidenceSummary = buildEvidenceSummary(currentCase?.evidence_items || [])

  const columns = [
    {
      title: '案例',
      dataIndex: 'title',
      key: 'title',
      width: 230,
      render: (value, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{value || record.case_id}</Text>
          <Text type="secondary">{record.case_id}</Text>
        </Space>
      ),
    },
    {
      title: '关键词',
      dataIndex: 'keyword',
      key: 'keyword',
      width: 140,
      render: (value) => <Tag color="cyan">{value}</Tag>,
    },
    {
      title: '平台',
      dataIndex: 'platforms',
      key: 'platforms',
      render: (platforms = []) => (
        <Space wrap size={[4, 4]}>
          {platforms.length ? platforms.map((platform) => <Tag key={platform}>{platform}</Tag>) : <Text type="secondary">默认 mock 平台</Text>}
        </Space>
      ),
    },
    {
      title: '风险',
      key: 'risk',
      width: 150,
      render: (_, record) => (
        <Space direction="vertical" size={2}>
          <Text strong>{formatScore(record.risk_score)}/100</Text>
          {record.risk_level ? (
            <Tag color={riskTone(record.risk_level)}>{riskLevelLabels[record.risk_level] || record.risk_level}</Tag>
          ) : (
            <Tag>未生成</Tag>
          )}
        </Space>
      ),
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 110,
      render: (value) => <Tag color={statusColors[value] || 'default'}>{statusLabels[value] || value}</Tag>,
    },
    {
      title: '更新时间',
      dataIndex: 'updated_at',
      key: 'updated_at',
      width: 190,
      render: formatDate,
    },
    {
      title: '操作',
      key: 'actions',
      width: 210,
      render: (_, record) => (
        <Space>
          <Button
            icon={<PlayCircle size={15} />}
            loading={loading && currentCase?.case_id === record.case_id}
            onClick={() => onRunCase(record.case_id)}
            size="small"
            type="primary"
          >
            运行
          </Button>
          <Button
            disabled={record.status !== 'completed'}
            icon={<FileText size={15} />}
            onClick={() => onOpenCaseReport(record.case_id)}
            size="small"
          >
            报告
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>分析案例</Title>
          <Text>管理本地 mock 舆情分析案例，保存关键词、平台、V1.5 风险结果和中文报告上下文。</Text>
        </div>
        <Space>
          <Button icon={<RefreshCw size={16} />} onClick={onRefreshCases}>
            刷新
          </Button>
          <Button type="primary" onClick={onNavigateToKeyword}>
            新建案例
          </Button>
        </Space>
      </div>

      {error ? <Alert message="案例数据加载失败" description={error} type="error" showIcon /> : null}

      {currentCase ? (
        <Card className="panel-card">
          <div className="panel-heading">
            <div>
              <Title level={4}>Current Case Data Source</Title>
              <Text type="secondary">{sourceStatus.analysisDescription}</Text>
            </div>
          </div>
          <Space size={[8, 8]} wrap>
            <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
            <Tag color="green">{sourceStatus.analysisLabel}</Tag>
            <Tag color="purple">{sourceStatus.llmLabel}</Tag>
            <Tag color="geekblue">{sourceStatus.sourceDetail}</Tag>
            {sourceStatus.isYoutubeRealData ? (
              <Tag color="red">YouTube public video/comment data</Tag>
            ) : null}
          </Space>
          {currentCase.evidence_item_count ? (
            <Space direction="vertical" className="full-width" size={8} style={{ marginTop: 14 }}>
              <Text strong>Evidence summary</Text>
              <Space size={[8, 8]} wrap>
                <Tag color="cyan">evidence_items: {currentCase.evidence_item_count}</Tag>
                <DistributionTags color="geekblue" values={evidenceSummary.sourceDistribution} />
                <DistributionTags color="purple" values={evidenceSummary.typeCounts} />
                <DistributionTags color="gold" values={evidenceSummary.acquisitionModes} />
              </Space>
              <Text type="secondary">
                Evidence attachment normalizes already available public or user-provided material; it does not fetch external sources or expose credentials.
              </Text>
              {evidenceSummary.titles.length ? (
                <Text type="secondary">Top titles: {evidenceSummary.titles.join(' / ')}</Text>
              ) : null}
              {evidenceSummary.comments.length ? (
                <Text type="secondary">Representative evidence: {evidenceSummary.comments[0]}</Text>
              ) : null}
            </Space>
          ) : null}
        </Card>
      ) : null}

      <Card className="panel-card cases-panel">
        {cases.length ? (
          <Table
            columns={columns}
            dataSource={cases}
            loading={loading && !cases.length}
            pagination={false}
            rowClassName={(record) => (record.case_id === currentCase?.case_id ? 'active-case-row' : '')}
            rowKey="case_id"
          />
        ) : (
          <Empty
            description="暂无分析案例。请先在 Keyword Search 创建并运行一个 mock 案例。"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          >
            <Button type="primary" onClick={onNavigateToKeyword}>
              创建第一个案例
            </Button>
          </Empty>
        )}
      </Card>
    </div>
  )
}
