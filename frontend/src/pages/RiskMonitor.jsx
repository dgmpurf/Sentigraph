import { Card, Col, List, Row, Tag, Typography } from 'antd'

import { PlatformHeatmapChart } from '../components/charts/PlatformHeatmapChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { riskTone } from '../utils/formatters.js'

const { Text, Title } = Typography

export function RiskMonitor({ alerts, visualization }) {
  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>Risk Monitor</Title>
          <Text>Watch hourly shifts, alert thresholds, and platform intensity.</Text>
        </div>
        <Tag color={riskTone(visualization?.risk_level)} className="large-tag">
          Score {visualization?.risk_score || 0}
        </Tag>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <SentimentTrendChart data={visualization?.sentiment_trend} />
        </Col>
        <Col span={10}>
          <RiskRadarChart data={visualization?.risk_radar} />
        </Col>
        <Col span={14}>
          <PlatformHeatmapChart data={visualization?.heatmap} />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Title level={4}>Threshold Alerts</Title>
              <Tag color="volcano">{alerts.length}</Tag>
            </div>
            <List
              dataSource={alerts}
              locale={{ emptyText: 'No alerts' }}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={
                      <Tag color={riskTone(item.level)}>
                        {item.level} · {item.created_at}
                      </Tag>
                    }
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
