import {
  Alert,
  Button,
  Card,
  Col,
  Empty,
  List,
  Progress,
  Row,
  Skeleton,
  Space,
  Statistic,
  Tag,
  Timeline,
  Typography,
} from 'antd'
import {
  Activity,
  AlertTriangle,
  Bell,
  Bot,
  CheckCircle,
  Gauge,
  PlayCircle,
  RadioTower,
  Send,
  ShieldAlert,
} from 'lucide-react'

import { PlatformHeatmapChart } from '../components/charts/PlatformHeatmapChart.jsx'
import { RiskRadarChart } from '../components/charts/RiskRadarChart.jsx'
import { SentimentTrendChart } from '../components/charts/SentimentTrendChart.jsx'
import { formatPercent, riskTone } from '../utils/formatters.js'
import { buildPublicOpinionReportModel } from '../utils/reportModel.js'

const { Paragraph, Text, Title } = Typography

const riskLevelLabels = {
  low: '低风险',
  medium: '中等风险',
  high: '高风险',
  critical: '严重风险',
}

const alertLevelLabels = {
  info: '信息',
  warning: '预警',
  critical: '严重预警',
}

const alertTones = {
  info: 'blue',
  warning: 'warning',
  critical: 'error',
}

const scheduleStatusLabels = {
  disabled: '监控已暂停',
  scheduled: '监控已启用',
  due: '监控已到期',
}

const scheduleStatusTones = {
  disabled: 'default',
  scheduled: 'cyan',
  due: 'warning',
}

const notificationStatusLabels = {
  pending: '待模拟发送',
  simulated_sent: '已模拟发送',
  failed: '发送失败',
}

const notificationStatusTones = {
  pending: 'warning',
  simulated_sent: 'cyan',
  failed: 'error',
}

const channelTypeLabels = {
  in_app: '站内通知',
  email_placeholder: '邮件占位',
  webhook_placeholder: 'Webhook 占位',
  slack_placeholder: 'Slack 占位',
  enterprise_wechat_placeholder: '企业微信占位',
  feishu_placeholder: '飞书占位',
}

const radarLabels = [
  ['negative_sentiment', '负面情绪'],
  ['bot_impact', '疑似水军/重复话术'],
  ['propagation_speed', '扩散速度'],
  ['controversy', '争议程度'],
  ['trend_shift', '趋势突变'],
]

function scoreText(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '0.0'
}

function scorePercent(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? Math.max(0, Math.min(100, Math.round(numericValue))) : 0
}

function getAlertTone(level) {
  return alertTones[level] || riskTone(level)
}

function getSnapshotTime(snapshot) {
  if (!snapshot?.created_at) return '未生成'
  const date = new Date(snapshot.created_at)
  if (Number.isNaN(date.getTime())) return snapshot.created_at
  return date.toLocaleString('zh-CN', { hour12: false })
}

function getScheduleTime(value) {
  if (!value) return '未设置'
  return getSnapshotTime({ created_at: value })
}

function getNotificationTime(value) {
  if (!value) return '未生成'
  return getSnapshotTime({ created_at: value })
}

function normalizeTopic(topic, index = 0) {
  if (!topic || typeof topic !== 'object') {
    return {
      topicId: `topic_${index + 1}`,
      topic: '未命名话题',
      riskScore: 0,
      riskLevel: 'low',
      explanation: '暂无风险解释。',
      drivers: [],
    }
  }

  const riskScore = Number(topic.topic_risk_score ?? topic.risk_score ?? topic.riskScore ?? 0)
  return {
    topicId: String(topic.topic_id || topic.cluster_id || topic.topicId || `topic_${index + 1}`),
    topic: String(topic.topic || topic.name || '未命名话题'),
    riskScore,
    riskLevel: topic.topic_risk_level || topic.risk_level || topic.riskLevel || 'low',
    explanation: String(topic.risk_explanation || topic.explanation || '暂无风险解释。'),
    drivers: [
      ['负面严重度', topic.neg_severity ?? topic.negSeverity],
      ['扩散信号', topic.spread_signal ?? topic.spreadSignal],
      ['争议信号', topic.controversy_signal ?? topic.controversySignal],
      ['重复话术信号', topic.bot_signal ?? topic.botSignal],
      ['影响力代理', topic.influence_proxy ?? topic.influenceProxy],
    ].filter(([, value]) => Number.isFinite(Number(value))),
  }
}

function getLatestSnapshot(caseSnapshots = [], monitoringStatus) {
  if (monitoringStatus?.latest_snapshot) return monitoringStatus.latest_snapshot
  return caseSnapshots.length ? caseSnapshots[caseSnapshots.length - 1] : null
}

function getPreviousSnapshot(caseSnapshots = [], monitoringStatus) {
  if (monitoringStatus?.previous_snapshot) return monitoringStatus.previous_snapshot
  return caseSnapshots.length > 1 ? caseSnapshots[caseSnapshots.length - 2] : null
}

function buildSnapshotTrend(caseSnapshots = []) {
  return caseSnapshots.slice(-6).map((snapshot) => ({
    color: riskTone(snapshot.risk_level),
    children: (
      <Space direction="vertical" size={2}>
        <Text strong>{scoreText(snapshot.risk_score)}/100</Text>
        <Text type="secondary">
          {riskLevelLabels[snapshot.risk_level] || snapshot.risk_level} · {getSnapshotTime(snapshot)}
        </Text>
      </Space>
    ),
  }))
}

function buildTopDrivers(report, latestSnapshot, riskRadar) {
  const topicSource = latestSnapshot?.top_risk_topics?.length
    ? latestSnapshot.top_risk_topics
    : report.topRiskTopics
  const topicDrivers = topicSource.slice(0, 3).map((topic, index) => {
    const normalized = normalizeTopic(topic, index)
    return {
      title: normalized.topic,
      value: `${scoreText(normalized.riskScore)}/100`,
      level: normalized.riskLevel,
      description: normalized.explanation,
    }
  })

  const signalDrivers = [
    {
      title: '真实危机风险',
      value: `${scoreText(latestSnapshot?.real_crisis_risk ?? report.realCrisisRisk ?? 0)}/100`,
      level: (latestSnapshot?.real_crisis_risk ?? report.realCrisisRisk ?? 0) >= 70 ? 'high' : 'medium',
      description: '服务体验、事实争议、合规安全等信号的综合风险。',
    },
    {
      title: '操纵传播风险',
      value: `${scoreText(latestSnapshot?.manipulation_risk ?? report.manipulationRisk ?? 0)}/100`,
      level: (latestSnapshot?.manipulation_risk ?? report.manipulationRisk ?? 0) >= 70 ? 'high' : 'medium',
      description: '疑似水军、重复话术、异常协同传播的综合风险。',
    },
  ]

  if (riskRadar?.trend_shift) {
    signalDrivers.push({
      title: '趋势突变',
      value: formatPercent(riskRadar.trend_shift),
      level: riskRadar.trend_shift >= 0.65 ? 'high' : 'medium',
      description: '最近风险信号相对前一窗口的变化压力。',
    })
  }

  return [...topicDrivers, ...signalDrivers].slice(0, 5)
}

export function RiskMonitor({
  alerts = [],
  analysis,
  caseSnapshots = [],
  currentCase,
  error,
  loading,
  monitoringConfig,
  monitoringLoading = false,
  monitoringStatus,
  notificationLoading = false,
  notificationOutboxStatus,
  notifications = [],
  onDisableMonitoring,
  onEnableMonitoring,
  onMarkNotificationRead,
  onRunDueMonitoringJobs,
  onRunMonitoringCheck,
  onSimulateSendNotification,
  onSimulateSendPendingNotifications,
  recommendation,
  schedulerLoading = false,
  schedulerStatus,
  summary,
  visualization,
}) {
  const report = buildPublicOpinionReportModel({ analysis, recommendation, summary, visualization })
  const latestSnapshot = getLatestSnapshot(caseSnapshots, monitoringStatus)
  const previousSnapshot = getPreviousSnapshot(caseSnapshots, monitoringStatus)
  const riskRadar = visualization?.risk_radar
  const sentimentTrend = visualization?.sentiment_trend || []
  const visibleAlerts = alerts.length ? alerts : monitoringStatus?.alerts || []
  const riskScore = Number(
    latestSnapshot?.risk_score ?? report.overallRisk ?? report.riskScore ?? visualization?.risk_score ?? 0,
  )
  const riskLevel = latestSnapshot?.risk_level || report.riskLevel || visualization?.risk_level || 'low'
  const riskModelVersion =
    latestSnapshot?.risk_model_version || report.riskModelVersion || visualization?.risk_model_version || 'v1_static_mvp'
  const realCrisisRisk = Number(latestSnapshot?.real_crisis_risk ?? report.realCrisisRisk ?? 0)
  const manipulationRisk = Number(latestSnapshot?.manipulation_risk ?? report.manipulationRisk ?? 0)
  const riskDelta = Number(
    monitoringStatus?.latest_risk_delta ??
      (latestSnapshot && previousSnapshot ? latestSnapshot.risk_score - previousSnapshot.risk_score : 0),
  )
  const topDrivers = buildTopDrivers(report, latestSnapshot, riskRadar)
  const topReason =
    visibleAlerts[0]?.reason ||
    report.riskExplanation ||
    latestSnapshot?.summary ||
    '暂无触发原因。运行 mock 监控检查后，这里会显示最新预警解释。'
  const scheduleConfig = monitoringConfig || currentCase?.monitoring_config || {
    enabled: false,
    interval_minutes: 60,
    last_run_at: null,
    next_run_at: null,
    status: 'disabled',
  }
  const scheduleStatus = scheduleConfig.status || (scheduleConfig.enabled ? 'scheduled' : 'disabled')
  const scheduleLabel = scheduleStatusLabels[scheduleStatus] || scheduleStatus
  const schedulerDueCases = Number(schedulerStatus?.due_cases || 0)
  const schedulerEnabledCases = Number(schedulerStatus?.enabled_cases || 0)
  const visibleNotifications = notifications.slice(0, 6)
  const unreadNotifications = notifications.filter((item) => !item.read_at).length
  const pendingNotifications =
    notificationOutboxStatus?.pending ?? notifications.filter((item) => item.status === 'pending').length

  if (!visualization && !latestSnapshot) {
    return (
      <Card className="panel-card">
        {error ? <Alert message="风险监控数据加载失败" description={error} type="error" showIcon /> : null}
        {loading ? (
          <Skeleton active paragraph={{ rows: 8 }} title />
        ) : (
          <Empty description="暂无风险监控数据，请先创建并运行一个 mock 分析案例。" image={Empty.PRESENTED_IMAGE_SIMPLE} />
        )}
      </Card>
    )
  }

  return (
    <div className="page-stack">
      <div className="page-heading">
        <div>
          <Title level={2}>风险监控</Title>
          <Text>
            基于持久化案例快照，对总体风险、真实危机风险、操纵传播风险和高风险话题变化做离线 mock 预警。
          </Text>
        </div>
        <Space direction="vertical" align="end" size={8}>
          <Button
            icon={<PlayCircle size={16} />}
            loading={monitoringLoading}
            onClick={onRunMonitoringCheck}
            type="primary"
          >
            Run Mock Monitoring Check
          </Button>
          <Tag color={riskTone(riskLevel)} className="large-tag">
            {riskLevelLabels[riskLevel] || riskLevel}
          </Tag>
          <Tag color="geekblue">{riskModelVersion}</Tag>
        </Space>
      </div>

      <Row gutter={[16, 16]}>
        <Col span={24}>
          <Card className="panel-card trend-explanation-card">
            <div className="panel-heading">
              <Space>
                <RadioTower size={18} />
                <Title level={4}>监控配置</Title>
              </Space>
              <Tag color={scheduleStatusTones[scheduleStatus] || 'default'}>{scheduleLabel}</Tag>
            </div>
            <Row gutter={[16, 16]}>
              <Col span={5}>
                <Statistic title="检查间隔" value={scheduleConfig.interval_minutes || 60} suffix="分钟" />
              </Col>
              <Col span={6}>
                <Space direction="vertical" size={4}>
                  <Text type="secondary">上次检查</Text>
                  <Text>{getScheduleTime(scheduleConfig.last_run_at)}</Text>
                </Space>
              </Col>
              <Col span={6}>
                <Space direction="vertical" size={4}>
                  <Text type="secondary">下次检查</Text>
                  <Text>{getScheduleTime(scheduleConfig.next_run_at)}</Text>
                </Space>
              </Col>
              <Col span={7}>
                <Space direction="vertical" size={4}>
                  <Text type="secondary">手动调度器状态</Text>
                  <Text>
                    {schedulerEnabledCases} 个已启用 · {schedulerDueCases} 个到期 · 后台调度未运行
                  </Text>
                </Space>
              </Col>
            </Row>
            <Space wrap style={{ marginTop: 16 }}>
              <Button
                disabled={!currentCase?.case_id || scheduleConfig.enabled}
                loading={schedulerLoading}
                onClick={onEnableMonitoring}
                type="primary"
              >
                启用监控
              </Button>
              <Button
                disabled={!currentCase?.case_id || !scheduleConfig.enabled}
                loading={schedulerLoading}
                onClick={onDisableMonitoring}
              >
                暂停监控
              </Button>
              <Button loading={schedulerLoading} onClick={onRunDueMonitoringJobs}>
                运行到期监控任务
              </Button>
            </Space>
          </Card>
        </Col>

        <Col span={6}>
          <Card className={`panel-card risk-monitor-hero risk-${riskLevel}`}>
            <Space className="metric-heading">
              <AlertTriangle size={20} />
              <Text>监控状态</Text>
            </Space>
            <Statistic value={scoreText(riskScore)} suffix="/100" valueStyle={{ color: '#ff5d8f' }} />
            <Progress percent={scorePercent(riskScore)} showInfo={false} strokeColor="#ff5d8f" trailColor="#283043" />
            <Text type="secondary">
              {currentCase?.title || '默认 mock 项目'} · {riskLevelLabels[riskLevel] || riskLevel}
            </Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <Activity size={20} />
              <Text>风险变化</Text>
            </Space>
            <Statistic
              value={scoreText(riskDelta)}
              prefix={riskDelta > 0 ? '+' : ''}
              suffix="分"
              valueStyle={{ color: riskDelta >= 10 ? '#ff5d8f' : '#42f5d7' }}
            />
            <Text>{monitoringStatus?.message || '尚未运行本轮监控检查。'}</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <ShieldAlert size={20} />
              <Text>真实危机风险</Text>
            </Space>
            <Statistic value={scoreText(realCrisisRisk)} suffix="/100" />
            <Progress percent={scorePercent(realCrisisRisk)} showInfo={false} strokeColor="#f5c44b" trailColor="#283043" />
            <Text type="secondary">事实争议、服务体验、合规安全信号。</Text>
          </Card>
        </Col>
        <Col span={6}>
          <Card className="panel-card">
            <Space className="metric-heading">
              <Bot size={20} />
              <Text>操纵传播风险</Text>
            </Space>
            <Statistic value={scoreText(manipulationRisk)} suffix="/100" />
            <Progress
              percent={scorePercent(manipulationRisk)}
              showInfo={false}
              strokeColor="#42f5d7"
              trailColor="#283043"
            />
            <Text type="secondary">疑似水军、重复话术、协同扩散信号。</Text>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card className="panel-card trend-explanation-card">
            <div className="panel-heading">
              <Space>
                <RadioTower size={18} />
                <Title level={4}>预警事件</Title>
              </Space>
              <Tag color={visibleAlerts.length ? 'volcano' : 'cyan'}>{visibleAlerts.length}</Tag>
            </div>
            <Paragraph className="dashboard-summary-copy">{topReason}</Paragraph>
            <List
              className="monitor-alert-list"
              dataSource={visibleAlerts}
              locale={{ emptyText: '暂无预警事件。运行监控检查后，如阈值被触发会显示在这里。' }}
              renderItem={(item) => (
                <List.Item>
                  <div className={`alert-tile alert-${item.level}`}>
                    <Space direction="vertical" size={8} className="full-width">
                      <Space className="analysis-signal-line" wrap>
                        <Tag color={getAlertTone(item.level)}>{alertLevelLabels[item.level] || item.level}</Tag>
                        <Text type="secondary">{getSnapshotTime({ created_at: item.created_at })}</Text>
                      </Space>
                      <Text strong>{item.message}</Text>
                      <Text type="secondary">{item.reason}</Text>
                    </Space>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <Gauge size={18} />
                <Title level={4}>最新快照</Title>
              </Space>
              <Tag color="geekblue">{caseSnapshots.length}</Tag>
            </div>
            {caseSnapshots.length ? (
              <Timeline className="snapshot-timeline" items={buildSnapshotTrend(caseSnapshots)} />
            ) : (
              <Empty description="暂无监控快照" image={Empty.PRESENTED_IMAGE_SIMPLE} />
            )}
          </Card>
        </Col>

        <Col span={24}>
          <Card className="panel-card trend-explanation-card">
            <div className="panel-heading">
              <Space>
                <Bell size={18} />
                <Title level={4}>通知中心</Title>
              </Space>
              <Space wrap>
                <Tag color={unreadNotifications ? 'volcano' : 'cyan'}>{unreadNotifications} 未读通知</Tag>
                <Tag color={pendingNotifications ? 'warning' : 'cyan'}>{pendingNotifications} 待模拟发送</Tag>
                <Tag color="geekblue">{notificationOutboxStatus?.mock_only === false ? '外部通道' : '本地模拟出箱'}</Tag>
              </Space>
            </div>
            <Paragraph className="dashboard-summary-copy">
              当前 MVP 仅把预警事件写入本地通知出箱，可模拟发送状态，不会调用邮件、Slack、Webhook、企业微信或飞书接口。
            </Paragraph>
            <Space wrap style={{ marginBottom: 12 }}>
              <Button
                data-testid="notification-send-pending-button"
                icon={<Send size={15} />}
                loading={notificationLoading}
                onClick={onSimulateSendPendingNotifications}
              >
                模拟发送待处理通知
              </Button>
            </Space>
            <List
              className="monitor-alert-list"
              dataSource={visibleNotifications}
              locale={{ emptyText: '暂无通知。运行 mock 监控检查并触发预警后，通知会显示在这里。' }}
              renderItem={(item) => (
                <List.Item>
                  <div className={`alert-tile alert-${item.level}`}>
                    <Space direction="vertical" size={8} className="full-width">
                      <Space className="analysis-signal-line" wrap>
                        <Tag color={getAlertTone(item.level)}>{alertLevelLabels[item.level] || item.level}</Tag>
                        <Tag color={notificationStatusTones[item.status] || 'default'}>
                          发送状态：{notificationStatusLabels[item.status] || item.status}
                        </Tag>
                        <Tag color={item.read_at ? 'default' : 'gold'}>{item.read_at ? '已读' : '未读通知'}</Tag>
                        <Text type="secondary">关联案例：{item.case_id}</Text>
                      </Space>
                      <Text strong>{item.title}</Text>
                      <Text>{item.message}</Text>
                      <Text type="secondary">
                        {channelTypeLabels[item.channel_type] || item.channel_type} · {getNotificationTime(item.created_at)}
                      </Text>
                      <Space wrap>
                        <Button
                          data-testid="notification-mark-read-button"
                          disabled={Boolean(item.read_at)}
                          icon={<CheckCircle size={15} />}
                          loading={notificationLoading}
                          onClick={() => onMarkNotificationRead?.(item.notification_id)}
                          size="small"
                        >
                          标记已读
                        </Button>
                        <Button
                          data-testid="notification-simulate-send-button"
                          disabled={item.status === 'simulated_sent'}
                          icon={<Send size={15} />}
                          loading={notificationLoading}
                          onClick={() => onSimulateSendNotification?.(item.notification_id)}
                          size="small"
                        >
                          模拟发送
                        </Button>
                      </Space>
                    </Space>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col span={14}>
          <SentimentTrendChart data={sentimentTrend} focusNegative />
        </Col>
        <Col span={10}>
          <RiskRadarChart data={riskRadar} />
        </Col>

        <Col span={14}>
          <PlatformHeatmapChart data={visualization?.heatmap || []} />
        </Col>
        <Col span={10}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <ShieldAlert size={18} />
                <Title level={4}>Top 风险驱动因素</Title>
              </Space>
              <Tag color="geekblue">{riskModelVersion}</Tag>
            </div>
            <List
              dataSource={topDrivers}
              locale={{ emptyText: '暂无风险驱动因素' }}
              renderItem={(driver) => (
                <List.Item>
                  <Space direction="vertical" className="full-width" size={5}>
                    <Space className="analysis-signal-line" wrap>
                      <Text strong>{driver.title}</Text>
                      <Tag color={riskTone(driver.level)}>{driver.value}</Tag>
                    </Space>
                    <Text type="secondary">{driver.description}</Text>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>

        <Col span={24}>
          <Card className="panel-card">
            <div className="panel-heading">
              <Space>
                <Activity size={18} />
                <Title level={4}>高风险话题监控</Title>
              </Space>
              <Tag color="cyan">{(latestSnapshot?.top_risk_topics || report.topRiskTopics).length}</Tag>
            </div>
            <List
              grid={{ gutter: 16, column: 3 }}
              dataSource={(latestSnapshot?.top_risk_topics || report.topRiskTopics).slice(0, 3).map(normalizeTopic)}
              locale={{ emptyText: '暂无 V1.5 高风险话题数据' }}
              renderItem={(topic) => (
                <List.Item>
                  <div className={`topic-risk-card risk-${topic.riskLevel}`}>
                    <Space direction="vertical" className="full-width" size={10}>
                      <Space className="analysis-signal-line" wrap>
                        <Text strong>{topic.topic}</Text>
                        <Tag color={riskTone(topic.riskLevel)}>{riskLevelLabels[topic.riskLevel] || topic.riskLevel}</Tag>
                      </Space>
                      <Progress percent={scorePercent(topic.riskScore)} strokeColor="#ff5d8f" trailColor="#283043" />
                      <Paragraph className="topic-risk-explanation">{topic.explanation}</Paragraph>
                      <div className="topic-risk-meta-grid">
                        {topic.drivers.map(([label, value]) => (
                          <span key={`${topic.topicId}-${label}`}>
                            {label}: {formatPercent(Number(value))}
                          </span>
                        ))}
                      </div>
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
