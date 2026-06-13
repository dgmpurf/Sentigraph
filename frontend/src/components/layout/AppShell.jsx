import { Button, Layout, Menu, Space, Tag, Tooltip, Typography } from 'antd'
import {
  Activity,
  BarChart3,
  ClipboardCheck,
  ClipboardList,
  FileText,
  FileSearch,
  FolderKanban,
  Globe2,
  Network,
  Orbit,
  RefreshCw,
  Search,
  ShieldAlert,
  ShieldCheck,
  Sparkles,
  Wrench,
} from 'lucide-react'

import { riskTone } from '../../utils/formatters.js'

const { Content, Header, Sider } = Layout
const { Text, Title } = Typography

const navItems = [
  { key: 'dashboard', label: 'Dashboard', icon: <BarChart3 size={17} /> },
  { key: 'searchDiscovery', label: 'Search Discovery', icon: <FileSearch size={17} /> },
  { key: 'demoFlow', label: 'Demo Flow / 演示流程', icon: <ClipboardList size={17} /> },
  { key: 'cases', label: 'Cases', icon: <FolderKanban size={17} /> },
  { key: 'keyword', label: 'Keyword Search', icon: <Search size={17} /> },
  { key: 'analysis', label: 'Analysis Result', icon: <Activity size={17} /> },
  { key: 'propagation', label: 'Propagation Graph', icon: <Network size={17} /> },
  { key: 'risk', label: 'Risk Monitor', icon: <ShieldAlert size={17} /> },
  { key: 'summary', label: 'Summary Report', icon: <FileText size={17} /> },
  { key: 'publicParsers', label: '公开页面解析', icon: <FileSearch size={17} /> },
  { key: 'platformIntegrations', label: '平台接入总览', icon: <Globe2 size={17} /> },
  { key: 'selectorRepair', label: 'Selector 修复工具', icon: <Wrench size={17} /> },
  { key: 'llmSafety', label: '大模型安全状态', icon: <ShieldCheck size={17} /> },
  { key: 'benchmarks', label: 'Benchmarks / 离线评测', icon: <ClipboardCheck size={17} /> },
  {
    key: 'simulationLab',
    label: (
      <Tooltip title="Simulation Lab / 舆情预演沙盘" placement="right">
        <span>Simulation / 沙盘</span>
      </Tooltip>
    ),
    icon: <Activity size={17} />,
  },
  {
    key: 'opinionEcosystem',
    label: (
      <Tooltip title="Opinion Ecosystem Sandbox / 舆论生态沙盒" placement="right">
        <span>生态沙盒</span>
      </Tooltip>
    ),
    icon: <Orbit size={17} />,
  },
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
  sourceStatus,
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
            {sourceStatus ? (
              <>
                <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
                <Tag color="green">{sourceStatus.analysisLabel}</Tag>
                <Tag color="purple">{sourceStatus.llmLabel}</Tag>
              </>
            ) : (
              <>
                <Tag color="default">Data: Mock</Tag>
                <Tag color="green">Analysis: Offline</Tag>
                <Tag color="purple">LLM: Mock</Tag>
              </>
            )}
            {caseTitle ? <Tag color="geekblue">{caseTitle}</Tag> : null}
            <Text className="project-label">{projectId}</Text>
            <Tag color={riskTone(riskLevel)}>
              风险 {riskScore} / {riskLevelLabels[riskLevel] || riskLevel}
            </Tag>
            <Tag color="volcano">{alertsCount} Alerts</Tag>
          </Space>
          <Tooltip title="Refresh analysis">
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
