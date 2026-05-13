import { Card, Col, Empty, List, Progress, Row, Space, Statistic, Tag, Typography } from 'antd'
import { AlertTriangle, Bot, RadioTower, TrendingDown } from 'lucide-react'

import { PlatformHeatmapChart } from '../components/charts/PlatformHeatmapChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'

const { Text, Title } = Typography

const radarLabels = [
  ['negative_sentiment', 'Negative sentiment'],
  ['bot_impact', 'Bot impact'],
  ['propagation_speed', 'Propagation speed'],
  ['controversy', 'Controversy'],
  ['trend_shift', 'Trend shift'],
]

export function RiskMonitor({ alerts, visualization }) {
  const riskRadar = visualization?.risk_radar
  const riskScore = visualization?.risk_score || 0
  const riskLevel = visualization?.risk_level || 'low'

  if (!visualization) {
    return (
      <Card className="panel-card">
        <Empty description="No risk visualization data loaded" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Risk Monitor</Title>
          <Text>Watch hourly shifts, alert thresholds, and platform intensity.</Text>
        </div>
        <Tag color={riskTone(riskLevel)} className="large-tag">
          {riskLevel} risk
        </Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className={`panel-card risk-monitor-hero risk-${riskLevel}`}>
            <Space className="metric-heading">
              <AlertTriangle size={20} />
              <Text>Risk posture</Text>
            </Space>
            <Statistic value={riskScore} suffix="/100" valueStyle={{ color: '#ff5d8f' }} />
            <Progress percent={riskScore} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
            <Text>Risk level is intentionally prominent for command-center scanning.</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <TrendingDown size={20} />
              <Text>Negative Trend</Text>
            </Space>
            <Statistic value={formatPercent(riskRadar?.negative_sentiment)} />
            <Text>Negative line is emphasized in trend charts.</Text>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <Bot size={20} />
              <Text>Bot Impact</Text>
            </Space>
            <Statistic value={formatPercent(visualization.bot_impact?.suspected_bot_comment_ratio)} />
            <Text>Suspected repeated-script comment share.</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <SentimentTrendChart data={visualization.sentiment_trend || []} focusNegative />
        </Col>
        <Col span={10}>
          <RiskRadarChart data={riskRadar} />
        </Col>
        <Col span={14}>
          <PlatformHeatmapChart data={visualization.heatmap || []} />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Risk Factor Readout</Title>
              <Tag color="cyan">{radarLabels.length}</Tag>
            </div>
            <List
              dataSource={radarLabels}
              renderItem={([key, label]) => {
                const value = riskRadar?.[key] || 0
                return (
                  <List.Item>
                    <Space direction="vertical" className="full-width" size={4}>
                      <Space className="analysis-signal-line">
                        <Text>{label}</Text>
                        <Tag color={value >= 0.5 ? 'volcano' : 'default'}>{formatPercent(value)}</Tag>
                      </Space>
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
                <Title level={4}>Threshold Alerts</Title>
              </Space>
              <Tag color="volcano">{alerts.length}</Tag>
            </div>
            <List
              dataSource={alerts}
              locale={{ emptyText: 'No alerts' }}
              grid={{ gutter: 16, column: 2 }}
              renderItem={(item) => (
                <List.Item>
                  <Card className="alert-tile">
                    <Space direction="vertical" size={8}>
                      <Tag color={riskTone(item.level)}>{item.level}</Tag>
                      <Text strong>{item.created_at}</Text>
                      <Text>{item.message}</Text>
                    </Space>
                  </Card>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>
    </div>
  )
}
