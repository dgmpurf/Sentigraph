import { Alert, Button, Card, Col, Empty, Row, Skeleton, Space, Tag, Typography } from 'antd'
import {
  BarChart3,
  Bot,
  CheckCircle2,
  ClipboardCheck,
  Download,
  FileText,
  FlaskConical,
  PlayCircle,
  Rocket,
  ShieldCheck,
  Workflow,
} from 'lucide-react'
import { useCallback, useEffect, useMemo, useState } from 'react'

import { getLatestBenchmarkSummary, getLlmStatus } from '../api/sentigraphApi.js'
import { getAnalysisSourceStatus } from '../utils/dataSourceStatus.js'

const { Paragraph, Text, Title } = Typography

const DEMO_KEYWORD = 'Tesla'
const DEMO_CASE_TITLE = 'Tesla Demo Case'
const DEMO_CASE_PLATFORMS = ['reddit', 'weibo', 'bilibili']

const stepTone = {
  ready: 'green',
  active: 'cyan',
  pending: 'default',
  warning: 'orange',
}

const stepLabels = {
  ready: '已就绪',
  active: '可执行',
  pending: '待准备',
  warning: '需检查',
}

function isDemoCase(caseItem) {
  if (!caseItem) return false
  const title = String(caseItem.title || '').toLowerCase()
  const keyword = String(caseItem.keyword || '').toLowerCase()
  return title === DEMO_CASE_TITLE.toLowerCase() || keyword === DEMO_KEYWORD.toLowerCase()
}

function formatScore(value) {
  const numericValue = Number(value)
  return Number.isFinite(numericValue) ? numericValue.toFixed(1) : '-'
}

function getStatus(ready, active = true) {
  if (ready) return 'ready'
  return active ? 'active' : 'pending'
}

function StepCard({ action, description, icon, mockLabel = 'mock/offline', status, title }) {
  return (
    <Card className={`panel-card demo-step-card demo-step-${status}`}>
      <div className="demo-step-header">
        <Space>
          <span className="demo-step-icon">{icon}</span>
          <Title level={4}>{title}</Title>
        </Space>
        <Tag color={stepTone[status] || 'default'}>{stepLabels[status] || status}</Tag>
      </div>
      <Paragraph>{description}</Paragraph>
      <div className="demo-step-footer">
        <Tag color="cyan">{mockLabel}</Tag>
        {action}
      </div>
    </Card>
  )
}

function DemoReadinessCard({ benchmarkSummary, demoCase, llmStatus, loading, sourceStatus }) {
  return (
    <Card className="panel-card demo-readiness-card">
      <div className="panel-heading">
        <Space>
          <ClipboardCheck size={18} />
          <Title level={4}>演示就绪度</Title>
        </Space>
        <Tag color="green">Offline Only</Tag>
      </div>
      {loading ? (
        <Skeleton active paragraph={{ rows: 5 }} title={false} />
      ) : (
        <Space direction="vertical" size={10} className="full-width">
          <div className="demo-readiness-row">
            <Text type="secondary">演示案例</Text>
            <Tag color={demoCase ? 'green' : 'default'}>{demoCase ? demoCase.case_id : '待创建'}</Tag>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">案例风险</Text>
            <Text>{formatScore(demoCase?.risk_score)}/100</Text>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">Data</Text>
            <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">Analysis</Text>
            <Tag color="green">Offline</Tag>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">LLM</Text>
            <Tag color="purple">Mock</Tag>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">离线评测</Text>
            <Tag color={benchmarkSummary?.total_failed > 0 ? 'red' : 'green'}>
              {benchmarkSummary ? `${benchmarkSummary.total_passed || 0} passed` : '未读取'}
            </Tag>
          </div>
          <div className="demo-readiness-row">
            <Text type="secondary">大模型状态</Text>
            <Tag color={llmStatus?.real_calls_enabled ? 'red' : 'green'}>
              {llmStatus ? (llmStatus.real_calls_enabled ? '真实调用已开' : '真实调用关闭') : '未读取'}
            </Tag>
          </div>
        </Space>
      )}
    </Card>
  )
}

function DemoCommandCard() {
  return (
    <Card className="panel-card demo-command-card">
      <div className="panel-heading">
        <Space>
          <Rocket size={18} />
          <Title level={4}>Windows 本地演示命令</Title>
        </Space>
      </div>
      <Space direction="vertical" size={8} className="full-width">
        <Text code>cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph"</Text>
        <Text code>python scripts\reset_local_data.py --yes</Text>
        <Text code>python scripts\seed_demo_cases.py --reset-first</Text>
        <Text code>python -m uvicorn app.main:app --reload --app-dir backend --host 127.0.0.1 --port 8000</Text>
        <Text code>cd /d "G:\AICODING\Sentigraph 舆情图谱系统\Sentigraph\frontend"</Text>
        <Text code>npm run dev</Text>
        <Text code>python scripts\api_smoke_check.py --base-url http://127.0.0.1:8000</Text>
      </Space>
    </Card>
  )
}

export function DemoFlow({
  analysis,
  cases = [],
  currentCase,
  error,
  loading,
  markdownLoading,
  markdownReport,
  onGetMarkdownReport,
  onLoadDemoCase,
  onNavigate,
  onOpenCaseReport,
  onRunCase,
  summary,
}) {
  const [readiness, setReadiness] = useState({
    benchmarkSummary: null,
    llmStatus: null,
    loading: true,
    error: '',
  })
  const [markdownStatus, setMarkdownStatus] = useState('')

  const demoCase = useMemo(() => {
    if (isDemoCase(currentCase)) return currentCase
    return cases.find(isDemoCase) || null
  }, [cases, currentCase])

  const selectedDemoCase = currentCase?.case_id && currentCase.case_id === demoCase?.case_id ? currentCase : null
  const sourceCase = selectedDemoCase || demoCase || currentCase
  const sourceStatus = getAnalysisSourceStatus({
    analysis: analysis || sourceCase?.analysis_result,
    currentCase: sourceCase,
  })
  const completed = demoCase?.status === 'completed' || selectedDemoCase?.status === 'completed'
  const topicRisks = analysis?.topic_risks || selectedDemoCase?.analysis_result?.topic_risks || []
  const riskReady = completed && topicRisks.length > 0
  const reportReady = completed && Boolean(summary || selectedDemoCase?.report)
  const markdownReady = Boolean(markdownReport?.markdown)

  useEffect(() => {
    let isMounted = true
    setReadiness((current) => ({ ...current, loading: true, error: '' }))
    Promise.all([getLatestBenchmarkSummary(), getLlmStatus()])
      .then(([benchmarkSummary, llmStatus]) => {
        if (isMounted) {
          setReadiness({ benchmarkSummary, llmStatus, loading: false, error: '' })
        }
      })
      .catch((requestError) => {
        if (isMounted) {
          setReadiness({
            benchmarkSummary: null,
            llmStatus: null,
            loading: false,
            error: requestError?.message || '无法读取离线评测或大模型安全状态。',
          })
        }
      })
    return () => {
      isMounted = false
    }
  }, [])

  const handleLoadDemo = useCallback(async () => {
    setMarkdownStatus('')
    await onLoadDemoCase?.()
  }, [onLoadDemoCase])

  const handleRunDemo = useCallback(async () => {
    if (!demoCase?.case_id) return
    setMarkdownStatus('')
    await onRunCase?.(demoCase.case_id, 'demoFlow')
  }, [demoCase, onRunCase])

  const handleMarkdownExport = useCallback(async () => {
    setMarkdownStatus('')
    try {
      const report = await onGetMarkdownReport?.()
      setMarkdownStatus(report?.markdown ? 'Markdown 报告已生成，可在舆情报告页复制或下载。' : '暂无可用 Markdown。')
    } catch (requestError) {
      setMarkdownStatus(requestError?.message || '暂时无法生成 Markdown 报告。')
    }
  }, [onGetMarkdownReport])

  const runAnalysisTitle = sourceStatus.isCaseRawData ? '2 运行离线确定性分析' : '2 运行 mock 分析'
  const runAnalysisDescription = sourceStatus.isCaseRawData
    ? '使用已附加的案例原始数据运行离线确定性分析，生成 V1.5 风险、中文报告、监控快照、告警和本地通知。'
    : '运行离线 mock pipeline，生成 V1.5 风险、中文报告、监控快照、告警和本地通知。'
  const runAnalysisButton = sourceStatus.isCaseRawData ? '运行离线分析' : '运行 mock 分析'
  const demoNotice = sourceStatus.isYoutubeRealData
    ? '当前案例的数据来源为 YouTube public video/comment data；分析、报告、预测、Simulation Lab 和 LLM 仍保持离线确定性/Mock，不调用真实大模型。'
    : '当前演示使用 mock/offline 数据，不调用真实平台 API 或真实大模型。Simulation Lab 输出仅用于聚合级人工复核。'

  const steps = [
    {
      title: '1 创建/加载演示案例',
      status: getStatus(Boolean(demoCase)),
      icon: <Rocket size={18} />,
      description: sourceStatus.isYoutubeRealData
        ? '加载已附加 YouTube public video/comment data 的 Tesla / 特斯拉演示案例。'
        : '准备 Tesla / 特斯拉本地 mock 案例，平台固定为 reddit、weibo、bilibili。',
      action: (
        <Button icon={<PlayCircle size={15} />} loading={loading} onClick={handleLoadDemo} type="primary">
          一键准备演示数据
        </Button>
      ),
      mockLabel: sourceStatus.isYoutubeRealData ? 'youtube-real/offline' : 'mock/offline',
    },
    {
      title: runAnalysisTitle,
      status: getStatus(completed, Boolean(demoCase)),
      icon: <FlaskConical size={18} />,
      description: runAnalysisDescription,
      action: (
        <Button disabled={!demoCase?.case_id} loading={loading} onClick={handleRunDemo}>
          {runAnalysisButton}
        </Button>
      ),
      mockLabel: sourceStatus.isCaseRawData ? 'offline/raw-data' : 'mock/offline',
    },
    {
      title: '3 查看风险结果',
      status: getStatus(riskReady, completed),
      icon: <BarChart3 size={18} />,
      description: '展示 V1.5 topic risk、总体风险、真实危机风险和操纵传播风险。',
      action: (
        <Button disabled={!completed} onClick={() => onNavigate?.('analysis')}>
          打开风险结果
        </Button>
      ),
    },
    {
      title: '4 查看中文报告并导出 Markdown',
      status: getStatus(reportReady || markdownReady, completed),
      icon: <FileText size={18} />,
      description: '查看结构化中文舆情报告，并生成可复制或下载的 Markdown 报告。',
      action: (
        <Space>
          <Button disabled={!completed || !demoCase?.case_id} onClick={() => onOpenCaseReport?.(demoCase.case_id)}>
            打开中文报告
          </Button>
          <Button disabled={!completed || !currentCase?.case_id} icon={<Download size={15} />} loading={markdownLoading} onClick={handleMarkdownExport}>
            生成 Markdown
          </Button>
        </Space>
      ),
    },
    {
      title: '5 初始化沙盘',
      status: getStatus(completed, completed),
      icon: <Workflow size={18} />,
      description: '使用聚合案例数据初始化 Simulation Lab，不生成个体操控建议。',
      action: (
        <Button disabled={!completed} onClick={() => onNavigate?.('simulationLab')}>
          打开 Simulation Lab
        </Button>
      ),
    },
    {
      title: '6 A/B 策略对比',
      status: getStatus(completed, completed),
      icon: <Workflow size={18} />,
      description: '在沙盘中比较 no_response、clarification、apology 或透明内容治理方案。',
      action: (
        <Button disabled={!completed} onClick={() => onNavigate?.('simulationLab')}>
          进入 A/B 对比
        </Button>
      ),
    },
    {
      title: '7 导出策略预演报告',
      status: getStatus(completed, completed),
      icon: <ClipboardCheck size={18} />,
      description: '导出 Simulation Lab Markdown 策略报告，结论保持人工复核导向。',
      action: (
        <Button disabled={!completed} onClick={() => onNavigate?.('simulationLab')}>
          打开报告导出
        </Button>
      ),
    },
    {
      title: '8 查看离线评测与安全状态',
      status: getStatus(Boolean(readiness.benchmarkSummary && readiness.llmStatus)),
      icon: <ShieldCheck size={18} />,
      description: '确认离线评测通过、大模型真实调用关闭、API key 只显示布尔状态。',
      action: (
        <Space>
          <Button onClick={() => onNavigate?.('benchmarks')}>离线评测</Button>
          <Button onClick={() => onNavigate?.('llmSafety')}>大模型安全</Button>
        </Space>
      ),
    },
  ]

  return (
    <div className="page-stack demo-flow-page">
      <div className="page-heading">
        <div>
          <Title level={2}>演示流程</Title>
          <Text>一页串起 Sentigraph 的本地演示路径，并区分真实数据来源、离线分析和 Mock LLM。</Text>
        </div>
        <Space>
          <Tag color="cyan">Demo Flow</Tag>
          <Tag color={sourceStatus.dataTagColor}>{sourceStatus.dataLabel}</Tag>
          <Tag color="green">{sourceStatus.analysisLabel}</Tag>
          <Tag color="purple">{sourceStatus.llmLabel}</Tag>
          <Tag color="geekblue">{sourceStatus.sourceDetail}</Tag>
          {sourceStatus.isYoutubeRealData ? <Tag color="red">YouTube public comments</Tag> : null}
          <Tag color="orange">{sourceStatus.isYoutubeRealData ? 'Manual YouTube API data' : 'No Real APIs'}</Tag>
          <Tag color="volcano">No Real LLMs</Tag>
        </Space>
      </div>

      <Alert
        message={demoNotice}
        type="info"
        showIcon
      />
      {error ? <Alert message="演示流程状态提示" description={error} type="error" showIcon /> : null}
      {readiness.error ? <Alert message="安全状态读取失败" description={readiness.error} type="warning" showIcon /> : null}
      {markdownStatus ? <Alert message={markdownStatus} type={markdownStatus.includes('已生成') ? 'success' : 'warning'} showIcon /> : null}

      <Row gutter={[16, 16]}>
        <Col span={16}>
          <Row gutter={[16, 16]}>
            {steps.map((step) => (
              <Col span={12} key={step.title}>
                <StepCard {...step} />
              </Col>
            ))}
          </Row>
        </Col>
        <Col span={8}>
          <Space direction="vertical" size={16} className="full-width">
            <DemoReadinessCard
              benchmarkSummary={readiness.benchmarkSummary}
              demoCase={demoCase}
              llmStatus={readiness.llmStatus}
              loading={readiness.loading}
              sourceStatus={sourceStatus}
            />
            <Card className="panel-card demo-scope-card">
              <div className="panel-heading">
                <Space>
                  <Bot size={18} />
                  <Title level={4}>演示边界</Title>
                </Space>
              </div>
              <Space direction="vertical" size={8}>
                <Text>
                  {sourceStatus.isCaseRawData
                    ? `${sourceStatus.analysisDescription} ${sourceStatus.dataDescription}`
                    : '只使用确定性 mock pipeline 和本地 JSON 运行数据。'}
                </Text>
                <Text>
                  {sourceStatus.isYoutubeRealData
                    ? '本页不会自动调用真实平台 API；YouTube public video/comment data 来自用户手动附加的本地案例原始数据，不启用真实 LLM、真实通知或 live public fetching。'
                    : '不启用真实平台 API、真实 LLM、真实通知或 live public fetching。'}
                </Text>
                <Text>不提供虚假共识、机器人放大、伪造事件、隐蔽引导或个体定向建议。</Text>
              </Space>
            </Card>
            <DemoCommandCard />
          </Space>
        </Col>
      </Row>

      {!demoCase && !loading ? (
        <Card className="panel-card">
          <Empty
            description="尚未发现 Tesla 演示案例。点击“一键准备演示数据”即可创建并运行本地 mock 演示。"
            image={Empty.PRESENTED_IMAGE_SIMPLE}
          />
        </Card>
      ) : null}
    </div>
  )
}
