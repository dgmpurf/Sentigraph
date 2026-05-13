import { Card, Col, Empty, List, Progress, Row, Space, Table, Tag, Typography } from 'antd'
import { AlertTriangle, Bot, MessageCircleWarning, TrendingDown } from 'lucide-react'

import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'

const { Paragraph, Text, Title } = Typography

const topicColumns = [
  {
    title: 'Topic',
    dataIndex: 'topic',
    key: 'topic',
    width: 220,
    render: (value, record) => (
      <Space direction="vertical" size={2}>
        <Text strong>{value}</Text>
        <Text type="secondary">{record.cluster_id}</Text>
      </Space>
    ),
  },
  { title: 'Comments', dataIndex: 'comment_count', key: 'comment_count', width: 110 },
  {
    title: 'Sentiment',
    dataIndex: 'average_sentiment_score',
    key: 'average_sentiment_score',
    width: 130,
    render: (value) => {
      const numericValue = typeof value === 'number' ? value : 0
      return <Tag color={numericValue < 0 ? 'error' : numericValue > 0 ? 'success' : 'default'}>{numericValue.toFixed(2)}</Tag>
    },
  },
  { title: 'Summary', dataIndex: 'summary', key: 'summary' },
]

function SentimentBar({ color, label, value }) {
  return (
    <div className="sentiment-bar-row">
      <Space className="full-width" direction="vertical" size={4}>
        <Space className="sentiment-bar-label">
          <Text>{label}</Text>
          <Text strong>{formatPercent(value)}</Text>
        </Space>
        <Progress percent={Math.round((value || 0) * 100)} showInfo={false} strokeColor={color} trailColor="#283043" />
      </Space>
    </div>
  )
}

export function AnalysisResult({ analysis, visualization }) {
  const sentiment = analysis?.sentiment
  const riskScore = visualization?.risk_score ?? analysis?.risk?.risk_score ?? 0
  const riskLevel = visualization?.risk_level ?? analysis?.risk?.risk_level ?? 'low'
  const topics = analysis?.topics || []
  const botAccounts = analysis?.bot_accounts || []
  const conflicts = analysis?.conflicts || []

  if (!analysis) {
    return (
      <Card className="panel-card">
        <Empty description="No analysis result loaded" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Analysis Result</Title>
          <Text>{analysis.summary}</Text>
        </div>
        <div className={`risk-score-lockup risk-${riskLevel}`}>
          <span>{riskScore}</span>
          <Tag color={riskTone(riskLevel)}>{riskLevel} risk</Tag>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card risk-readout-card">
            <Space className="metric-heading">
              <AlertTriangle size={20} />
              <Text>Current Risk</Text>
            </Space>
            <Title level={1}>{riskScore}</Title>
            <Tag color={riskTone(riskLevel)}>{riskLevel}</Tag>
            <Paragraph>
              Risk combines sentiment, bot-like amplification, controversy, propagation speed, and trend shift.
            </Paragraph>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Title level={4}>Sentiment Mix</Title>
            <Space direction="vertical" className="full-width" size={14}>
              <SentimentBar color="#54f5a8" label="Positive" value={sentiment?.positive_ratio || 0} />
              <SentimentBar color="#f5c44b" label="Neutral" value={sentiment?.neutral_ratio || 0} />
              <SentimentBar color="#ff5d8f" label="Negative" value={sentiment?.negative_ratio || 0} />
              <Text>Average sentiment score: {sentiment?.average_sentiment_score ?? 0}</Text>
            </Space>
          </Card>
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <Title level={4}>Bot Impact</Title>
            <Space direction="vertical" className="full-width" size={14}>
              <Space className="analysis-signal-line">
                <Bot size={18} />
                <Text>Suspected accounts</Text>
                <Tag color="cyan">{formatPercent(analysis.bot_score?.suspected_bot_ratio)}</Tag>
              </Space>
              <Space className="analysis-signal-line">
                <MessageCircleWarning size={18} />
                <Text>Suspected comment share</Text>
                <Tag color="volcano">{formatPercent(analysis.bot_score?.suspected_bot_comment_ratio)}</Tag>
              </Space>
              <Text>Use this as an early triage signal, not a final identity judgment.</Text>
            </Space>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <SentimentTrendChart data={visualization?.sentiment_trend || []} focusNegative />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <Title level={4}>Negative Topic Priority</Title>
            <List
              dataSource={[...topics].sort((left, right) => left.average_sentiment_score - right.average_sentiment_score)}
              locale={{ emptyText: 'No topic clusters loaded' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Text strong>{item.topic}</Text>
                        <Tag color={item.average_sentiment_score < 0 ? 'error' : 'default'}>
                          {item.average_sentiment_score.toFixed(2)}
                        </Tag>
                        <Tag>{item.comment_count} comments</Tag>
                      </Space>
                    }
                    description={item.summary}
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Topic Clusters</Title>
              <Tag color="cyan">{topics.length}</Tag>
            </div>
            <Table
              columns={topicColumns}
              dataSource={topics}
              pagination={false}
              rowKey="cluster_id"
              size="middle"
            />
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <Title level={4}>Bot and Conflict Signals</Title>
            <List
              dataSource={botAccounts}
              locale={{ emptyText: 'No suspicious accounts in mock result' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Text>{item.author_id}</Text>
                        <Tag color="volcano">{formatPercent(item.bot_probability)}</Tag>
                      </Space>
                    }
                    description={(item.bot_reasons || []).join(' / ')}
                  />
                </List.Item>
              )}
            />
            <List
              dataSource={conflicts}
              locale={{ emptyText: 'No conflict signal detected' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={<Tag color="red">Conflict intensity {formatPercent(item.intensity)}</Tag>}
                    description={
                      <div className="conflict-copy">
                        <Paragraph>{item.side_a}</Paragraph>
                        <Paragraph>{item.side_b}</Paragraph>
                      </div>
                    }
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
