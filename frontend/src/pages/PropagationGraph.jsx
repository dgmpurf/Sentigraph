import { Alert, Card, Col, Empty, List, Row, Skeleton, Space, Statistic, Tag, Typography } from 'antd'
import { GitBranch, Layers3, RadioTower, Route, Share2 } from 'lucide-react'

import { PropagationGraphChart } from '../components/charts/PropagationGraphChart.jsx'
import { formatPercent } from '../utils/formatters.js'

const { Paragraph, Text, Title } = Typography

function countBy(items, key) {
  return items.reduce((counts, item) => {
    const value = item?.[key] || 'unknown'
    counts.set(value, (counts.get(value) || 0) + 1)
    return counts
  }, new Map())
}

function formatSentiment(value) {
  const numericValue = Number(value || 0)
  return numericValue.toFixed(2)
}

function sentimentTone(value) {
  const numericValue = Number(value || 0)
  if (numericValue < -0.2) return 'error'
  if (numericValue > 0.2) return 'success'
  return 'default'
}

export function PropagationGraph({ error, loading, propagation, visualization }) {
  const graph = propagation?.nodes?.length ? propagation : visualization?.propagation_graph
  const metrics = propagation?.metrics || graph?.metrics || {}
  const nodes = graph?.nodes || []
  const edges = graph?.edges || []
  const sourceLabel = propagation?.nodes?.length ? 'propagation API' : 'visualization graph'
  const topNodes = [...nodes]
    .sort((left, right) => (right.influence_score || 0) - (left.influence_score || 0))
    .slice(0, 5)
  const platformStats = [...countBy(nodes, 'platform').entries()].sort((left, right) => right[1] - left[1])
  const typeStats = [...countBy(nodes, 'type').entries()].sort((left, right) => right[1] - left[1])
  const centralNode = nodes.find((node) => node.node_id === metrics?.central_node_id)
  const isSmallGraph = nodes.length > 0 && nodes.length <= 8

  if (!graph || !nodes.length) {
    return (
      <Card className="panel-card">
        {error ? <Alert message="Propagation graph failed to load" description={error} type="error" showIcon /> : null}
        <Alert
          message="Mock propagation graph boundary"
          description="当前为离线 mock 传播结构图，用于演示节点、边和传播结构读法；不代表真实 Reddit / Weibo 数据，也不代表真实跨平台因果传播链。"
          showIcon
          type="info"
          style={{ marginBottom: 16 }}
        />
        {loading ? (
          <Skeleton active paragraph={{ rows: 8 }} title />
        ) : (
          <Empty
            description="No propagation graph nodes returned by the mock pipeline yet"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        )}
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Mock Propagation Graph / 模拟传播结构图</Title>
          <Text>Read mock nodes, mock reply/spread relations, and sample propagation structure without claiming causal proof.</Text>
        </div>
        <Space direction="vertical" align="end" size={8}>
          <Tag color="cyan">{nodes.length} nodes</Tag>
          <Tag color="geekblue">{sourceLabel}</Tag>
          <Tag color="orange">mock platform labels</Tag>
        </Space>
      </div>

      <Alert
        message="传播图边界"
        description="当前为离线 mock 传播图。平台名如 reddit / weibo 是 mock platform label；边表示 mock reply / spread relation 或样例传播关系，不代表因果证明、真实跨平台链路或实时速度。"
        showIcon
        type="info"
      />

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Depth" value={metrics?.depth || 0} prefix={<Route size={18} />} />
            <Text>观察到的 mock 回复层级</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Breadth" value={metrics?.breadth || nodes.length} prefix={<Share2 size={18} />} />
            <Text>mock 扩散宽度</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Speed" value={formatPercent(metrics?.propagation_speed)} prefix={<RadioTower size={18} />} />
            <Text>mock propagation velocity，不是实时速度</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Relations" value={edges.length} prefix={<GitBranch size={18} />} />
            <Text>当前图中的 mock relation 数量</Text>
          </Card>
        </Col>
      </Row>

      {isSmallGraph ? (
        <Alert
          className="graph-guidance-alert"
          message="Small mock graph mode"
          description="The current offline fixture is intentionally compact. Node size reflects influence, color reflects platform, shape reflects node type, and edge thickness reflects relation weight."
          type="info"
          showIcon
        />
      ) : null}

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
            {centralNode ? (
              <div className="central-node-card">
                <Text type="secondary">Central node</Text>
                <Text strong>{centralNode.node_id}</Text>
                <Paragraph ellipsis={{ rows: 2 }} className="node-copy">
                  {centralNode.content || 'No node content'}
                </Paragraph>
              </div>
            ) : null}
            <List
              dataSource={topNodes}
              locale={{ emptyText: 'No graph nodes' }}
              renderItem={(node) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Space wrap>
                        <Text strong>{node.node_id}</Text>
                        <Tag>{node.type || 'node'}</Tag>
                        <Tag color="cyan">{node.platform}</Tag>
                        <Tag color="orange">mock platform label</Tag>
                        <Tag color={sentimentTone(node.sentiment_score)}>
                          sentiment {formatSentiment(node.sentiment_score)}
                        </Tag>
                        <Tag>influence {formatPercent(node.influence_score)}</Tag>
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
        <Col span={8}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <Layers3 size={18} />
                <Title level={4}>Node Breakdown</Title>
              </Space>
              <Tag color="cyan">{nodes.length}</Tag>
            </div>
            <Space direction="vertical" className="full-width" size={14}>
              <div className="graph-stat-block">
                <Text type="secondary">By platform</Text>
                <Space wrap>
                  {platformStats.map(([platform, count]) => (
                    <Tag color="geekblue" key={platform}>
                      {platform}: {count}
                    </Tag>
                  ))}
                </Space>
              </div>
              <div className="graph-stat-block">
                <Text type="secondary">By node type</Text>
                <Space wrap>
                  {typeStats.map(([type, count]) => (
                    <Tag key={type}>
                      {type}: {count}
                    </Tag>
                  ))}
                </Space>
              </div>
            </Space>
          </Card>
        </Col>
        <Col span={16}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Edge Details</Title>
              <Tag>{edges.length} links</Tag>
            </div>
            <Text type="secondary">
              Edges are mock reply / spread relations in the current graph. They are not causal proof.
            </Text>
            <List
              dataSource={edges}
              locale={{ emptyText: 'No graph edges' }}
              grid={{ gutter: 12, column: 2 }}
              renderItem={(edge) => (
                <List.Item>
                  <div className="edge-tile">
                    <Space direction="vertical" size={6}>
                      <Text strong>
                        {edge.source} {'->'} {edge.target}
                      </Text>
                      <Space wrap>
                        <Tag>{edge.relation || 'relation'}</Tag>
                        <Tag color="cyan">weight {formatPercent(edge.weight)}</Tag>
                      </Space>
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
