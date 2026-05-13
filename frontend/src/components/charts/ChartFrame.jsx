import { Card, Empty, Typography } from 'antd'

const { Text, Title } = Typography

export function ChartFrame({ children, description, empty, title }) {
  return (
    <Card className="panel-card chart-card">
      <div className="panel-heading">
        <div>
          <Title level={4}>{title}</Title>
          {description ? <Text>{description}</Text> : null}
        </div>
      </div>
      {empty ? <Empty image={Empty.PRESENTED_IMAGE_SIMPLE} /> : children}
    </Card>
  )
}

