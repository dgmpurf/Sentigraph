import { Alert, Card, Col, Empty, List, Progress, Row, Skeleton, Space, Statistic, Tag, Typography } from 'antd'
import { AlertTriangle, Bot, FileText, Globe2, RadioTower, ShieldAlert, TrendingDown } from 'lucide-react'

import { BotImpactChart } from '../components/charts/BotImpactChart.jsx'
import { PlatformHeatmapChart } from '../components/charts/PlatformHeatmapChart.jsx'
import { PropagationGraphChart } from '../components/charts/PropagationGraphChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { TopicClusterChart } from '../components/charts/TopicClusterChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'
import { buildPublicOpinionReportModel } from '../utils/reportModel.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'

const { Paragraph, Text, Title } = Typography

const riskCopy = {
  low: '信号较平稳，保持常规观察并继续积累基线。',
  medium: '风险正在形成，重点观察负面情绪、扩散速度与话题集中度。',
  high: '已出现较高舆情压力，建议准备统一回应并盯紧快速扩散话题。',
  critical: '存在严重升级风险，应优先组织事实核查、统一口径和关键渠道回应。',
}

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

function toScore(value) {
  const numericValue = Number(value)
  if (!Number.isFinite(numericValue)) return 0
  return Math.max(0, Math.min(100, numericValue))
}

function buildPlatformDistribution(heatmap = [], graph) {
  const totals = new Map()

  heatmap.forEach((item) => {
    const platform = item?.platform
    if (!platform) return
    totals.set(platform, (totals.get(platform) || 0) + Number(item.intensity || 0))
  })

  if (!totals.size) {
    ;(graph?.nodes || []).forEach((node) => {
      const platform = node?.platform
      if (!platform) return
      totals.set(platform, (totals.get(platform) || 0) + 1)
    })
  }

  const total = [...totals.values()].reduce((sum, value) => sum + value, 0) || 1
  return [...totals.entries()]
    .map(([platform, value]) => ({
      platform,
      value,
      ratio: value / total,
    }))
    .sort((left, right) => right.value - left.value)
}

function getLatestSummary(summary, analysis, sourceStatus) {
  return (
    summary?.overall_summary ||
    summary?.summary ||
    analysis?.summary ||
    (sourceStatus?.isCaseRawData
      ? 'Offline deterministic analysis from attached case raw data has not returned a public opinion summary yet.'
      : 'Mock pipeline has not returned a public opinion summary yet.')
  )
}

export function Dashboard({ alerts = [], analysis, currentCase, error, keyword, loading, recommendation, summary, visualization }) {
  const sourceStatus = getAnalysisSourceStatus({ analysis, currentCase })
  const sentiment = analysis?.sentiment
  const report = buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization })
  const riskScore = Number(report.overallRisk ?? report.riskScore ?? visualization?.risk_score ?? 0)
  const riskLevel = report.riskLevel || visualization?.risk_level || analysis?.risk_level || analysis?.risk?.risk_level || 'low'
  const riskModelVersion = report.riskModelVersion || visualization?.risk_model_version || 'v1_static_mvp'
  const realCrisisRisk = toScore(report.realCrisisRisk)
  const manipulationRisk = toScore(report.manipulationRisk)
  const topRiskTopics = report.topRiskTopics.slice(0, 3)
  const graph = visualization?.propagation_graph
  const heatmap = visualization?.heatmap || []
  const topics = visualization?.topic_clusters || []
  const riskRadar = visualization?.risk_radar
  const platformDistribution = buildPlatformDistribution(heatmap, graph)
  const summaryText = getLatestSummary(summary, analysis, sourceStatus)
  const headingSourceLabel = sourceStatus.isCaseRawData
    ? 'offline deterministic analysis from attached case raw data'
    : 'mock pipeline visualization'
  const botSignalCopy = sourceStatus.isCaseRawData
    ? 'Repeated-script impact from attached public comment signals.'
    : 'Repeated-script impact from mock behavior signals.'

  if (!visualization) {
    return (
      <Card className="panel-card">
        {error ? <Alert message="Dashboard data failed to load" description={error} type="error" showIcon /> : null}
        <Alert
          message="风险口径说明"
          description="Dashboard 展示 demo / mock / selected case summary；不是实时全网监控。基础分析风险、当前监控风险和预测风险来自不同阶段，监控检查不会自动改写 Dashboard。"
          showIcon
          type="info"
          style={{ marginBottom: 16 }}
        />
        {loading ? (
          <Skeleton active paragraph={{ rows: 8 }} title />
        ) : (
          <Empty description="No visualization data loaded from the mock backend" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Sentigraph Command Center</Title>
          <Text>Monitoring keyword: {keyword} · {headingSourceLabel}</Text>
        </div>
        <Space>
          <Tag color="geekblue" className="large-tag">
            {riskModelVersion}
          </Tag>
          <Tag color={riskTone(riskLevel)} className="large-tag">
            {riskLevelLabels[riskLevel] || riskLevel}
          </Tag>
        </Space>
      </div>

      <Alert
        message="风险口径说明"
        description={
          <Space direction="vertical" size={2}>
            <Text>Dashboard 当前展示的是 demo / mock / selected case summary，不是实时全网监控。</Text>
            <Text>顶部风险为基础分析风险或 demo risk score；Risk Monitor 的当前监控风险和预测风险来自本地 mock 检查 / deterministic forecast，不会自动改写 Dashboard。</Text>
            <Text>如果当前样例来自 Tesla mock case，它不是 Helldivers selected public sample，也不是实时平台刷新。</Text>
          </Space>
        }
        showIcon
        type="info"
      />

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className={`metric-card risk-card risk-${riskLevel}`}>
            <Space align="start" className="metric-heading">
              <AlertTriangle size={20} />
              <Text>基础分析风险 / Demo risk score</Text>
            </Space>
            <Statistic value={riskScore} suffix="/100" valueStyle={{ color: '#ff5d8f' }} />
            <Progress percent={riskScore} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
            <Text>{riskCopy[riskLevel] || riskCopy.low}</Text>
            <Tag color="geekblue">{riskModelVersion}</Tag>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <TrendingDown size={20} />
              <Text>Negative Ratio</Text>
            </Space>
            <Statistic
              value={formatPercent(sentiment?.negative_ratio ?? riskRadar?.negative_sentiment)}
              valueStyle={{ color: '#f5c44b' }}
            />
            <Text>Average score {sentiment?.average_sentiment_score ?? 0}</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <Bot size={20} />
              <Text>Bot Comment Share</Text>
            </Space>
            <Statistic
              value={formatPercent(visualization?.bot_impact?.suspected_bot_comment_ratio)}
              valueStyle={{ color: '#42f5d7' }}
            />
            <Text>{botSignalCopy}</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <RadioTower size={20} />
              <Text>Propagation Speed</Text>
            </Space>
            <Statistic
              value={formatPercent(visualization?.risk_radar?.propagation_speed)}
              valueStyle={{ color: '#8bff72' }}
            />
            <Text>{graph?.nodes?.length || 0} nodes · {graph?.edges?.length || 0} active relations</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <ShieldAlert size={20} />
              <Text>真实危机风险</Text>
            </Space>
            <Statistic value={realCrisisRisk.toFixed(1)} suffix="/100" valueStyle={{ color: '#ffb057' }} />
            <Progress percent={Math.round(realCrisisRisk)} showInfo={false} strokeColor="#ffb057" trailColor="#283043" />
            <Text>衡量高风险话题中的真实投诉、事实核查压力和自然扩散迹象。</Text>
          </Card>
        </Col>
        <Col span={12}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <Bot size={20} />
              <Text>操纵传播风险</Text>
            </Space>
            <Statistic value={manipulationRisk.toFixed(1)} suffix="/100" valueStyle={{ color: '#42f5d7' }} />
            <Progress percent={Math.round(manipulationRisk)} showInfo={false} strokeColor="#42f5d7" trailColor="#283043" />
            <Text>衡量重复话术、疑似协同账号和异常集中传播对舆情判断的影响。</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card summary-signal-card">
            <div className="panel-heading">
              <Space>
                <FileText size={18} />
                <Title level={4}>Latest Public Opinion Summary</Title>
              </Space>
              <Tag color={summary ? 'cyan' : 'default'}>{summary ? 'summary API' : 'analysis fallback'}</Tag>
            </div>
            <Paragraph className="dashboard-summary-copy" ellipsis={{ rows: 4, expandable: true }}>
              {summaryText}
            </Paragraph>
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <ShieldAlert size={18} />
                <Title level={4}>V1.5 高风险话题 Top 3</Title>
              </Space>
              <Tag color="geekblue">{riskModelVersion}</Tag>
            </div>
            <List
              className="topic-risk-list"
              dataSource={topRiskTopics}
              locale={{ emptyText: '暂无 V1.5 话题风险数据' }}
              renderItem={(item, index) => {
                const score = Number(item.riskScore || 0)
                return (
                  <List.Item>
                    <Space direction="vertical" className="full-width" size={6}>
                      <Space className="analysis-signal-line">
                        <Text strong>{index + 1}. {item.topic}</Text>
                        <Tag color={riskTone(item.riskLevel)}>{riskLevelLabels[item.riskLevel] || item.riskLevel}</Tag>
                        <Tag color="volcano">{score.toFixed(1)}/100</Tag>
                      </Space>
                      <Progress percent={Math.round(score)} showInfo={false} strokeColor="#ff5d8f" />
                      <Text type="secondary">
                        评论 {item.commentCount || 0} 条 · 负面占比 {formatPercent(item.negativeRatio || 0)}
                      </Text>
                      <Paragraph className="topic-risk-explanation" ellipsis={{ rows: 2 }}>
                        {item.explanation || '暂无风险解释。'}
                      </Paragraph>
                    </Space>
                  </List.Item>
                )
              }}
            />
          </Card>
        </Col>
        <Col span={14}>
          <SentimentTrendChart data={visualization?.sentiment_trend} />
        </Col>
        <Col span={10}>
          <RiskRadarChart data={visualization?.risk_radar} />
        </Col>
        <Col span={12}>
          <TopicClusterChart data={visualization?.topic_clusters} />
        </Col>
        <Col span={12}>
          <BotImpactChart data={visualization?.bot_impact} />
        </Col>
        <Col span={16}>
          <PropagationGraphChart graph={graph} />
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Active Alerts</Title>
              <Tag color="volcano">{alerts.length}</Tag>
            </div>
            <List
              dataSource={alerts}
              locale={{ emptyText: 'No alerts' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={<Tag color={riskTone(item.level)}>{item.level}</Tag>}
                    description={item.message}
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={14}>
          <PlatformHeatmapChart data={heatmap} />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <Globe2 size={18} />
                <Title level={4}>Platform Distribution</Title>
              </Space>
              <Tag color="cyan">{platformDistribution.length}</Tag>
            </div>
            <List
              className="platform-distribution-list"
              dataSource={platformDistribution}
              locale={{ emptyText: 'No platform distribution data' }}
              renderItem={(item) => (
                <List.Item>
                  <Space direction="vertical" className="full-width" size={5}>
                    <Space className="analysis-signal-line">
                      <Text strong>{item.platform}</Text>
                      <Tag>{formatPercent(item.ratio)}</Tag>
                    </Space>
                    <Progress percent={Math.round(item.ratio * 100)} showInfo={false} strokeColor="#8bff72" />
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}
