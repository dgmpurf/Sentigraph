import { Card, Col, List, Progress, Row, Space, Statistic, Tag, Typography } from 'antd'
import { AlertTriangle, Bot, RadioTower, TrendingDown } from 'lucide-react'

import { BotImpactChart } from '../components/charts/BotImpactChart.jsx'
import { PropagationGraphChart } from '../components/charts/PropagationGraphChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { TopicClusterChart } from '../components/charts/TopicClusterChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'

const { Text, Title } = Typography

export function Dashboard({ alerts, analysis, keyword, visualization }) {
  const sentiment = analysis?.sentiment
  const riskScore = visualization?.risk_score || 0
  const graph = visualization?.propagation_graph

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Sentigraph Command Center</Title>
          <Text>Monitoring keyword: {keyword}</Text>
        </div>
        <Tag color={riskTone(visualization?.risk_level)} className="large-tag">
          {visualization?.risk_level || 'low'} risk
        </Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className="metric-card risk-card">
            <Space align="start" className="metric-heading">
              <AlertTriangle size={20} />
              <Text>Risk Score</Text>
            </Space>
            <Statistic value={riskScore} suffix="/100" valueStyle={{ color: '#ff5d8f' }} />
            <Progress percent={riskScore} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Space align="start" className="metric-heading">
              <TrendingDown size={20} />
              <Text>Negative Ratio</Text>
            </Space>
            <Statistic value={formatPercent(sentiment?.negative_ratio)} valueStyle={{ color: '#f5c44b' }} />
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
            <Text>Suspected accounts {formatPercent(visualization?.bot_impact?.suspected_bot_ratio)}</Text>
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
            <Text>{graph?.edges?.length || 0} active relations</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
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
      </Row>
    </div>
  )
}
