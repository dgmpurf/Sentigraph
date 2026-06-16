import { Button, Layout, Menu, Space, Tag, Tooltip, Typography } from 'antd'
import {
  Activity,
  BarChart3,
  Cable,
  ClipboardCheck,
  ClipboardList,
  Compass,
  FileText,
  FileSearch,
  FolderKanban,
  Globe2,
  Network,
  Newspaper,
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
  {
    key: 'consumer-demo-group',
    type: 'group',
    label: 'C端试玩',
    children: [
      { key: 'publicDemoGuide', label: 'Demo 试玩', icon: <Compass size={17} /> },
      { key: 'publicEventPlaza', label: '公开事件', icon: <Newspaper size={17} /> },
      {
        key: 'opinionEcosystem',
        label: (
          <Tooltip title="Opinion Ecosystem Sandbox / 舆论生态沙盒" placement="right">
            <span>生态沙盒</span>
          </Tooltip>
        ),
        icon: <Orbit size={17} />,
      },
    ],
  },
  {
    key: 'professional-analysis-group',
    type: 'group',
    label: '专业分析',
    children: [
      { key: 'dashboard', label: 'Dashboard', icon: <BarChart3 size={17} /> },
      { key: 'cases', label: 'Cases', icon: <FolderKanban size={17} /> },
      { key: 'keyword', label: 'Keyword Search', icon: <Search size={17} /> },
      { key: 'analysis', label: 'Analysis Result', icon: <Activity size={17} /> },
      { key: 'propagation', label: 'Propagation Graph', icon: <Network size={17} /> },
      { key: 'risk', label: 'Risk Monitor', icon: <ShieldAlert size={17} /> },
      { key: 'summary', label: 'Summary Report', icon: <FileText size={17} /> },
      { key: 'demoFlow', label: 'Demo Flow / 演示流程', icon: <ClipboardList size={17} /> },
      {
        key: 'simulationLab',
        label: (
          <Tooltip title="Simulation Lab / 舆情预演沙盘" placement="right">
            <span>Simulation / 沙盘</span>
          </Tooltip>
        ),
        icon: <Activity size={17} />,
      },
    ],
  },
  {
    key: 'data-dev-tools-group',
    type: 'group',
    label: '数据与开发工具',
    children: [
      { key: 'searchDiscovery', label: 'Search Discovery', icon: <FileSearch size={17} /> },
      { key: 'externalCollectorBridge', label: '外部采集桥接', icon: <Cable size={17} /> },
      { key: 'publicParsers', label: '公开页面解析', icon: <FileSearch size={17} /> },
      { key: 'platformIntegrations', label: '平台接入总览', icon: <Globe2 size={17} /> },
      { key: 'selectorRepair', label: 'Selector 修复工具', icon: <Wrench size={17} /> },
      { key: 'llmSafety', label: '大模型安全状态', icon: <ShieldCheck size={17} /> },
      { key: 'benchmarks', label: 'Benchmarks / 离线评测', icon: <ClipboardCheck size={17} /> },
    ],
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
  isPublicDemoPage = false,
}) {
  const refreshTooltip = isPublicDemoPage
    ? '仅重新加载本地 mock / selected sample 状态，不会联网抓取实时数据。'
    : 'Refresh analysis'
  const refreshLabel = isPublicDemoPage ? '刷新本地样本状态' : 'Refresh'

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
            {isPublicDemoPage ? (
              <>
                <Tag color="cyan">本地演示状态</Tag>
                <Tag color="default">Mock / selected sample</Tag>
                <Tag color="purple">LLM: Mock</Tag>
              </>
            ) : sourceStatus ? (
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
            <Text className="project-label">{isPublicDemoPage ? 'local demo' : projectId}</Text>
            {isPublicDemoPage ? (
              <>
                <Tag color="geekblue">No live fetch</Tag>
                <Tag color="default">not full-web coverage</Tag>
              </>
            ) : (
              <>
                <Tag color={riskTone(riskLevel)}>
                  风险 {riskScore} / {riskLevelLabels[riskLevel] || riskLevel}
                </Tag>
                <Tag color="volcano">{alertsCount} Alerts</Tag>
              </>
            )}
          </Space>
          <Tooltip title={refreshTooltip}>
            <Button
              icon={<RefreshCw size={16} />}
              loading={loading}
              onClick={onRefresh}
              type="primary"
            >
              {refreshLabel}
            </Button>
          </Tooltip>
        </Header>
        <Content className="app-content">{children}</Content>
      </Layout>
    </Layout>
  )
}
