import { Card, Col, Empty, List, Row, Space, Statistic, Tag, Typography } from 'antd'

import { PropagationGraphChart } from '../components/charts/PropagationGraphChart.jsx'
import { formatPercent } from '../utils/formatters.js'

const { Paragraph, Text, Title } = Typography

export function PropagationGraph({ propagation, visualization }) {
  const graph = propagation || visualization?.propagation_graph
  const metrics = propagation?.metrics
  const nodes = graph?.nodes || []
  const edges = graph?.edges || []
  const topNodes = [...nodes]
    .sort((left, right) => (right.influence_score || 0) - (left.influence_score || 0))
    .slice(0, 5)

  if (!graph) {
    return (
      <Card className="panel-card">
        <Empty description="No propagation graph loaded" image={Empty.PRESENTED_IMAGE_SIMPLE} />
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Propagation Graph</Title>
          <Text>Track core nodes, cross-platform spread, and reply paths.</Text>
        </div>
        <Tag color="cyan">{nodes.length} nodes</Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Depth" value={metrics?.depth || 0} />
            <Text>Observed reply levels</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Breadth" value={metrics?.breadth || nodes.length} />
            <Text>Visible spread width</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Speed" value={formatPercent(metrics?.propagation_speed)} />
            <Text>Mock propagation velocity</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Relations" value={edges.length} />
            <Text>Reply or spread links</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={16}>
          <PropagationGraphChart graph={graph} />
        </Col>
        <Col span={8}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Key Nodes</Title>
              <Tag>{metrics?.central_node_id || 'mock graph'}</Tag>
            </div>
            <List
              dataSource={topNodes}
              locale={{ emptyText: 'No graph nodes' }}
              renderItem={(node) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Text strong>{node.node_id}</Text>
                        <Tag color="cyan">{node.platform}</Tag>
                        <Tag>{formatPercent(node.influence_score)}</Tag>
                      </Space>
                    }
                    description={
                      <Paragraph ellipsis={{ rows: 2 }} className="node-copy">
                        {node.content || 'No node content'}
                      </Paragraph>
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
