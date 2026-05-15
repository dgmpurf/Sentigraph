import { Button, Layout, Menu, Space, Tag, Tooltip, Typography } from 'antd'
import {
  Activity,
  BarChart3,
  FileText,
  FolderKanban,
  Network,
  RefreshCw,
  Search,
  ShieldAlert,
  Sparkles,
} from 'lucide-react'

import { riskTone } from '../../utils/formatters.js'

const { Content, Header, Sider } = Layout
const { Text, Title } = Typography

const navItems = [
  { key: 'dashboard', label: 'Dashboard', icon: <BarChart3 size={17} /> },
  { key: 'cases', label: 'Cases', icon: <FolderKanban size={17} /> },
  { key: 'keyword', label: 'Keyword Search', icon: <Search size={17} /> },
  { key: 'analysis', label: 'Analysis Result', icon: <Activity size={17} /> },
  { key: 'propagation', label: 'Propagation Graph', icon: <Network size={17} /> },
  { key: 'risk', label: 'Risk Monitor', icon: <ShieldAlert size={17} /> },
  { key: 'summary', label: 'Summary Report', icon: <FileText size={17} /> },
]

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

export function AppShell({
  activePage,
  alertsCount,
  children,
  loading,
  onNavigate,
  onRefresh,
  caseTitle,
  projectId,
  riskLevel,
  riskScore,
}) {
  return (
    <Layout className="app-shell">
      <Sider width={256} className="app-sider">
        <div className="brand-lockup">
          <div className="brand-mark">
            <Sparkles size={21} />
          </div>
          <div>
            <Title level={4}>Sentigraph</Title>
            <Text>Public opinion intelligence</Text>
          </div>
        </div>
        <Menu
          mode="inline"
          selectedKeys={[activePage]}
          items={navItems}
          onClick={({ key }) => onNavigate(key)}
          className="app-menu"
        />
      </Sider>
      <Layout>
        <Header className="app-header">
          <Space size={14} wrap>
            <Tag color="cyan">Mock Mode</Tag>
            {caseTitle ? <Tag color="geekblue">{caseTitle}</Tag> : null}
            <Text className="project-label">{projectId}</Text>
            <Tag color={riskTone(riskLevel)}>
              风险 {riskScore} · {riskLevelLabels[riskLevel] || riskLevel}
            </Tag>
            <Tag color="volcano">{alertsCount} Alerts</Tag>
          </Space>
          <Tooltip title="Refresh mock analysis">
            <Button
              icon={<RefreshCw size={16} />}
              loading={loading}
              onClick={onRefresh}
              type="primary"
            >
              Refresh
            </Button>
          </Tooltip>
        </Header>
        <Content className="app-content">{children}</Content>
      </Layout>
    </Layout>
  )
}
