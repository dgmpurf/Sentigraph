import { Alert, Card, Col, Empty, List, Progress, Row, Skeleton, Space, Statistic, Tag, Typography } from 'antd'
import { Activity, AlertTriangle, Bot, Gauge, RadioTower, ShieldAlert, TrendingDown } from 'lucide-react'

import { PlatformHeatmapChart } from '../components/charts/PlatformHeatmapChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'
import { buildPublicOpinionReportModel } from '../utils/reportModel.js'

const { Text, Title } = Typography

const radarLabels = [
  {
    key: 'negative_sentiment',
    label: '负面情绪',
    description: 'mock 管线中负面评论的占比与强度。',
  },
  {
    key: 'bot_impact',
    label: '疑似水军/重复话术',
    description: '重复表达、协同发布或异常账号行为带来的压力。',
  },
  {
    key: 'propagation_speed',
    label: '扩散速度',
    description: '讨论在传播图谱中扩散的速度和范围。',
  },
  {
    key: 'controversy',
    label: '争议程度',
    description: '讨论是否出现明显对立、分裂或高强度交锋。',
  },
  {
    key: 'trend_shift',
    label: '趋势突变',
    description: '近期风险信号相对前一时间段的变化压力。',
  },
]

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

function scoreText(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '0.0'
}

function getRiskLevelExplanation(level) {
  const messages = {
    low: '当前风险较低，可保持常规监测并继续积累趋势基线。',
    medium: '风险正在形成，建议将负面情绪、扩散速度和高风险话题一起观察。',
    high: '风险较高，建议明确回应负责人、事实口径和对外更新时间窗口。',
    critical: '风险严重，建议立即提升监测频率并协调统一回应。',
  }
  return messages[level] || messages.low
}

function buildTrendInsights(riskRadar, sentimentTrend = [], alerts = []) {
  const latest = sentimentTrend[sentimentTrend.length - 1]
  const previous = sentimentTrend[sentimentTrend.length - 2]
  const negativeDelta =
    latest && previous ? Number(latest.negative || 0) - Number(previous.negative || 0) : null
  const trendShift = riskRadar?.trend_shift ?? 0
  const propagationSpeed = riskRadar?.propagation_speed ?? 0
  const controversy = riskRadar?.controversy ?? 0

  const insights = [
    trendShift >= 0.65
      ? '趋势突变信号较高，应视为可能的加速窗口。'
      : trendShift >= 0.35
        ? '趋势突变信号中等，建议继续观察下一个时间段。'
        : '当前 mock 数据中的趋势突变信号较低。',
    propagationSpeed >= 0.7
      ? '扩散速度较强，即使图谱规模较小，也需要关注回应时机。'
      : '扩散速度尚未成为主导因素，当前更应关注话题质量与情绪结构。',
    controversy >= 0.65
      ? '争议信号明显，回应语言应保持事实化，避免放大未经证实的说法。'
      : '当前 mock 时间窗内争议信号相对可控。',
  ]

  if (negativeDelta !== null) {
    insights.push(
      negativeDelta > 0
        ? `最近两个时间段之间负面量增加 ${negativeDelta} 条。`
        : `最近两个时间段之间负面量未增加（变化 ${negativeDelta}）。`,
    )
  } else {
    insights.push('当前只有一个情绪时间段，真实趋势斜率需要更多时间窗支持。')
  }

  if (alerts.length) {
    insights.push(`当前有 ${alerts.length} 张预警卡片，发布回应前建议逐条核查。`)
  }

  return insights
}

function buildTopRiskDrivers(report, riskRadar) {
  const topicDrivers = report.topRiskTopics.slice(0, 3).map((topic) => ({
    title: topic.topic,
    value: `${scoreText(topic.riskScore)}/100`,
    description: topic.explanation || '暂无话题风险解释。',
    level: topic.riskLevel,
  }))
  const signalDrivers = [
    {
      title: '真实危机风险',
      value: `${scoreText(report.realCrisisRisk ?? 0)}/100`,
      description: '由高风险话题与负面严重度综合映射，仅基于 mock 管线。',
      level: report.realCrisisRisk >= 70 ? 'high' : report.realCrisisRisk >= 40 ? 'medium' : 'low',
    },
    {
      title: '操纵/重复话术风险',
      value: `${scoreText(report.manipulationRisk ?? 0)}/100`,
      description: '由疑似水军、重复脚本与协同表达信号综合映射。',
      level: report.manipulationRisk >= 70 ? 'high' : report.manipulationRisk >= 40 ? 'medium' : 'low',
    },
    riskRadar?.trend_shift
      ? {
          title: '趋势突变',
          value: formatPercent(riskRadar.trend_shift),
          description: '近期风险变化对监测节奏的影响。',
          level: riskRadar.trend_shift >= 0.65 ? 'high' : 'medium',
        }
      : null,
  ].filter(Boolean)

  return [...topicDrivers, ...signalDrivers].slice(0, 5)
}

export function RiskMonitor({ alerts = [], analysis, error, loading, recommendation, summary, visualization }) {
  const report = buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization })
  const riskRadar = visualization?.risk_radar
  const riskScore = Number(report.overallRisk ?? report.riskScore ?? visualization?.risk_score ?? 0)
  const riskLevel = report.riskLevel || visualization?.risk_level || 'low'
  const riskModelVersion = report.riskModelVersion || visualization?.risk_model_version || 'v1_static_mvp'
  const sentimentTrend = visualization?.sentiment_trend || []
  const trendInsights = buildTrendInsights(riskRadar, sentimentTrend, alerts)
  const topRiskDrivers = buildTopRiskDrivers(report, riskRadar)

  if (!visualization) {
    return (
      <Card className="panel-card">
        {error ? <Alert message="风险监控数据加载失败" description={error} type="error" showIcon /> : null}
        {loading ? (
          <Skeleton active paragraph={{ rows: 8 }} title />
        ) : (
          <Empty description="暂无风险可视化数据" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>风险监控</Title>
          <Text>监测小时级变化、预警阈值、平台热度和 V1.5 话题级风险。</Text>
        </div>
        <Space direction="vertical" align="end" size={8}>
          <Tag color={riskTone(riskLevel)} className="large-tag">
            {riskLevelLabels[riskLevel] || riskLevel}
          </Tag>
          <Tag color="geekblue">{riskModelVersion}</Tag>
        </Space>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className={`panel-card risk-monitor-hero risk-${riskLevel}`}>
            <Space className="metric-heading">
              <AlertTriangle size={20} />
              <Text>风险态势</Text>
            </Space>
            <Statistic value={scoreText(riskScore)} suffix="/100" valueStyle={{ color: '#ff5d8f' }} />
            <Progress percent={Math.round(riskScore)} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
            <Text>{getRiskLevelExplanation(riskLevel)}</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <TrendingDown size={20} />
              <Text>真实危机风险</Text>
            </Space>
            <Statistic value={scoreText(report.realCrisisRisk ?? 0)} suffix="/100" />
            <Progress
              percent={Math.round(report.realCrisisRisk ?? 0)}
              showInfo={false}
              strokeColor="#f5c44b"
              trailColor="#283043"
            />
            <Text>偏向真实事件、服务体验、合规安全等风险信号。</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <Bot size={20} />
              <Text>操纵/重复话术风险</Text>
            </Space>
            <Statistic value={scoreText(report.manipulationRisk ?? 0)} suffix="/100" />
            <Progress
              percent={Math.round(report.manipulationRisk ?? 0)}
              showInfo={false}
              strokeColor="#42f5d7"
              trailColor="#283043"
            />
            <Text>偏向疑似水军、重复脚本和异常协同信号。</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card className="panel-card trend-explanation-card">
            <div className="panel-heading">
              <Space>
                <Activity size={18} />
                <Title level={4}>趋势解释</Title>
              </Space>
              <Tag color={riskRadar?.trend_shift >= 0.65 ? 'volcano' : 'cyan'}>
                趋势突变 {formatPercent(riskRadar?.trend_shift)}
              </Tag>
            </div>
            <List
              className="trend-insight-list"
              dataSource={trendInsights}
              grid={{ gutter: 12, column: 2 }}
              renderItem={(item) => (
                <List.Item>
                  <div className="insight-tile">
                    <Text>{item}</Text>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={14}>
          <SentimentTrendChart data={sentimentTrend} focusNegative />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <ShieldAlert size={18} />
                <Title level={4}>Top 风险驱动因子</Title>
              </Space>
              <Tag color="geekblue">{riskModelVersion}</Tag>
            </div>
            <List
              dataSource={topRiskDrivers}
              locale={{ emptyText: '暂无 V1.5 风险驱动数据' }}
              renderItem={(driver) => (
                <List.Item>
                  <Space direction="vertical" className="full-width" size={5}>
                    <Space className="analysis-signal-line" wrap>
                      <Text strong>{driver.title}</Text>
                      <Tag color={riskTone(driver.level)}>{driver.value}</Tag>
                    </Space>
                    <Text type="secondary">{driver.description}</Text>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={14}>
          <PlatformHeatmapChart data={visualization.heatmap || []} />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <Gauge size={18} />
                <Title level={4}>风险因子读数</Title>
              </Space>
              <Tag color="cyan">{radarLabels.length}</Tag>
            </div>
            <List
              dataSource={radarLabels}
              renderItem={(factor) => {
                const value = riskRadar?.[factor.key] || 0
                return (
                  <List.Item>
                    <Space direction="vertical" className="full-width" size={4}>
                      <Space className="analysis-signal-line">
                        <Text>{factor.label}</Text>
                        <Tag color={value >= 0.5 ? 'volcano' : 'default'}>{formatPercent(value)}</Tag>
                      </Space>
                      <Text type="secondary">{factor.description}</Text>
                      <Progress percent={Math.round(value * 100)} showInfo={false} strokeColor="#42f5d7" />
                    </Space>
                  </List.Item>
                )
              }}
            />
          </Card>
        </Col>
        <Col span={24}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <RadioTower size={18} />
                <Title level={4}>阈值预警</Title>
              </Space>
              <Tag color="volcano">{alerts.length}</Tag>
            </div>
            <List
              dataSource={alerts}
              locale={{ emptyText: '暂无预警' }}
              grid={{ gutter: 16, column: 2 }}
              renderItem={(item) => (
                <List.Item>
                  <div className="alert-tile">
                    <Space direction="vertical" size={8}>
                      <Tag color={riskTone(item.level)}>{riskLevelLabels[item.level] || item.level}</Tag>
                      <Text strong>{item.created_at}</Text>
                      <Text>{item.message}</Text>
                    </Space>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}
