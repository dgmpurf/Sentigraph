import { Button, Empty, Typography } from 'antd'

const { Text, Title } = Typography

export function NotFound({ activePage, onNavigate }) {
  return (
    <div className="page-stack">
      <div className="panel-card not-found-panel">
        <Empty
          description={
            <div>
              <Title level={3}>未找到页面</Title>
              <Text type="secondary">当前页面键 `{activePage || 'unknown'}` 不存在。</Text>
            </div>
          }
        >
          <Button type="primary" onClick={() => onNavigate?.('dashboard')}>
            返回仪表盘
          </Button>
        </Empty>
      </div>
    </div>
  )
}
