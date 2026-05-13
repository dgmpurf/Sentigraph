import { Card, Col, Row, Statistic, Typography } from 'antd'

import { PropagationGraphChart } from '../components/charts/PropagationGraphChart.jsx'
import { formatPercent } from '../utils/formatters.js'

const { Text, Title } = Typography

export function PropagationGraph({ propagation, visualization }) {
  const graph = propagation || visualization?.propagation_graph
  const metrics = propagation?.metrics

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Propagation Graph</Title>
          <Text>Track core nodes, cross-platform spread, and propagation breadth.</Text>
        </div>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Depth" value={metrics?.depth || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Breadth" value={metrics?.breadth || 0} />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Speed" value={formatPercent(metrics?.propagation_speed)} />
          </Card>
        </Col>
        <Col span={6}>
          <Card className="metric-card">
            <Statistic title="Central Node" value={metrics?.central_node_id || '-'} />
          </Card>
        </Col>
      </Row>

      <PropagationGraphChart graph={graph} />
    </div>
  )
}
