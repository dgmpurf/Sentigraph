import { Card, Col, List, Progress, Row, Space, Table, Tag, Typography } from 'antd'

import { formatPercent, riskTone } from '../utils/formatters.js'

const { Paragraph, Text, Title } = Typography

const topicColumns = [
  { title: 'Topic', dataIndex: 'topic', key: 'topic' },
  { title: 'Comments', dataIndex: 'comment_count', key: 'comment_count', width: 110 },
  {
    title: 'Sentiment',
    dataIndex: 'average_sentiment_score',
    key: 'average_sentiment_score',
    width: 120,
    render: (value) => value.toFixed(2),
  },
  { title: 'Summary', dataIndex: 'summary', key: 'summary' },
]

export function AnalysisResult({ analysis }) {
  const sentiment = analysis?.sentiment

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Analysis Result</Title>
          <Text>{analysis?.summary || 'No analysis loaded.'}</Text>
        </div>
        <Tag color={riskTone(analysis?.risk?.risk_level)} className="large-tag">
          {analysis?.risk?.risk_level || 'low'}
        </Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={8}>
          <Card className="panel-card">
            <Title level={4}>Sentiment Summary</Title>
            <Space direction="vertical" className="full-width" size={14}>
              <div>
                <Text>Positive</Text>
                <Progress percent={Math.round((sentiment?.positive_ratio || 0) * 100)} strokeColor="#54f5a8" />
              </div>
              <div>
                <Text>Neutral</Text>
                <Progress percent={Math.round((sentiment?.neutral_ratio || 0) * 100)} strokeColor="#f5c44b" />
              </div>
              <div>
                <Text>Negative</Text>
                <Progress percent={Math.round((sentiment?.negative_ratio || 0) * 100)} strokeColor="#ff5d8f" />
              </div>
              <Text>Average sentiment score: {sentiment?.average_sentiment_score ?? 0}</Text>
            </Space>
          </Card>
        </Col>
        <Col span={16}>
          <Card className="panel-card">
            <Title level={4}>Topic Clusters</Title>
            <Table
              columns={topicColumns}
              dataSource={analysis?.topics || []}
              pagination={false}
              rowKey="cluster_id"
              size="middle"
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="panel-card">
            <Title level={4}>Conflict Detection</Title>
            <List
              dataSource={analysis?.conflicts || []}
              locale={{ emptyText: 'No conflicts detected' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Tag color="red">Intensity {formatPercent(item.intensity)}</Tag>
                        <Text>{item.conflict_id}</Text>
                      </Space>
                    }
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
        <Col span={12}>
          <Card className="panel-card">
            <Title level={4}>Bot and AI Signals</Title>
            <List
              dataSource={analysis?.bot_accounts || []}
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
                    description={item.bot_reasons.join(' · ')}
                  />
                </List.Item>
              )}
            />
            <List
              dataSource={analysis?.ai_generated || []}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={<Tag color="purple">AI probability {formatPercent(item.ai_generated_probability)}</Tag>}
                    description={item.reason}
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
