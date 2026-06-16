import { Alert, Button, Card, Col, Empty, Input, Progress, Row, Space, Tag, Typography } from 'antd'
import {
  Building2,
  CheckCircle2,
  Compass,
  Database,
  ExternalLink,
  FileText,
  RotateCcw,
  Search,
  ShieldCheck,
  ThumbsUp,
} from 'lucide-react'
import { useMemo, useState } from 'react'

import { PUBLIC_EVENT_PLAZA_EVENTS } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography

const STORAGE_KEY = 'sentigraph-public-demo-progress-v1'

const DEMO_STEPS = [
  {
    key: 'plaza',
    title: 'Step 1：打开事件广场',
    buttonLabel: '打开事件广场',
    targetHash: '#/public-events?guided=1',
    description: '查看多个公共事件卡片。当前不是真实热榜，而是本地 demo 事件列表。',
  },
  {
    key: 'collector',
    title: 'Step 2：查看外部采集桥接',
    buttonLabel: '打开外部采集桥接',
    targetHash: '#/external-collector',
    description:
      '这里读取私人 collector 项目已经导出的本地 Evidence Export package，不运行爬虫、不搜索全网、不抓取 URL、不调用真实 API。推荐演示样本是 helldivers2-psn-demo_20260614_055754。',
  },
  {
    key: 'helldivers',
    title: 'Step 3：查看 Helldivers 公开事件页',
    buttonLabel: '打开 Helldivers 事件页',
    targetHash: '#/public-events/helldivers-psn',
    description: '查看 selected public sample、事件时间线、样本边界和生态沙盒入口。',
  },
  {
    key: 'sandbox',
    title: 'Step 4：进入生态沙盒 V2',
    buttonLabel: '打开生态沙盒 V2',
    targetHash: '#/opinion-ecosystem',
    description: '进入页面后请选择 V2 ecology view + Helldivers PSN sample。这里不做 URL 抓取，也不连接真实平台。',
  },
  {
    key: 'timeline',
    title: 'Step 5：体验 T0-T6 时间线',
    buttonLabel: '打开沙盒并体验时间线',
    targetHash: '#/opinion-ecosystem',
    description: '依次点击 T0 公告、T1 社区反弹、T2 官方回应、T3 第三方解释、T4 社区解构、T5 疲劳衰减、T6 声誉记忆。',
  },
  {
    key: 'request',
    title: 'Step 6：请求分析一个事件',
    buttonLabel: '打开请求分析页',
    targetHash: '#/public-events/request',
    description: '填写事件名称、公开线索和请求理由，生成本地演示预览。不会提交后端，也不会触发抓取。',
  },
  {
    key: 'vote',
    title: 'Step 7：支持候选事件',
    buttonLabel: '打开支持候选区',
    targetHash: '#/public-events/request',
    description: '支持我们优先做某个公开样本，只改变本地 UI，不代表自然舆情热度或真实排序。',
  },
  {
    key: 'bEnd',
    title: 'Step 8：查看企业 / 团队私有分析说明',
    buttonLabel: '查看私有分析说明',
    targetHash: '#/public-events/request',
    description: '当前只是入口演示，不提交信息、不创建私有 case。优先分析或商业分析必须透明标注。',
  },
  {
    key: 'bEndReport',
    title: 'Step 9：查看 B端报告样例',
    buttonLabel: '查看 B端报告样例',
    targetHash: '#/reports/helldivers-psn-sample',
    description: '查看同一个 Helldivers selected public sample 如何被组织成专业报告样例。它不是生产级报告、官方验证或因果证明。',
  },
]

const BOUNDARY_ITEMS = [
  'frontend-only local demo',
  'selected public sample where labeled',
  'request / support mock only',
  'not full-web coverage',
  'not full-platform coverage',
  'not official verification',
  'not causal proof',
  'no real platform action',
  'no real API / no real LLM call',
  'local exported package only',
  'no crawler job',
  'no live search',
  'no URL fetch',
  'PeopleCluster = anonymous groups/clusters, not real individuals',
  'InfluenceCore = content / narrative / official / media / meme cores, not people balls',
  'request/support count does not represent natural public-opinion heat',
  'priority or commercial analysis must be transparently labeled',
]

function readProgress() {
  try {
    const raw = window.localStorage.getItem(STORAGE_KEY)
    const parsed = raw ? JSON.parse(raw) : []
    return Array.isArray(parsed) ? parsed : []
  } catch {
    return []
  }
}

function DemoStepCard({ completed, onOpen, onToggle, step }) {
  return (
    <Card className={`panel-card public-demo-step-card ${completed ? 'complete' : ''}`}>
      <Space direction="vertical" size={12} className="full-width">
        <div className="public-demo-step-header">
          <Tag color={completed ? 'green' : 'cyan'}>{completed ? '已完成' : '待体验'}</Tag>
          {completed ? <CheckCircle2 size={18} /> : <Compass size={18} />}
        </div>
        <div>
          <Title level={4}>{step.title}</Title>
          <Paragraph>{step.description}</Paragraph>
        </div>
        <Space wrap>
          <Button type="primary" icon={<ExternalLink size={16} />} onClick={() => onOpen(step)}>
            {step.buttonLabel}
          </Button>
          <Button onClick={() => onToggle(step.key)}>
            {completed ? '标记为未完成' : '我已试过'}
          </Button>
        </Space>
      </Space>
    </Card>
  )
}

function EventResultCard({ event, onOpen }) {
  const targetHash = event.route || '#/public-events/request'
  return (
    <Card className="panel-card public-demo-result-card">
      <Space direction="vertical" size={10} className="full-width">
        <Space wrap>
          <Tag color={event.is_sample_available ? 'green' : 'default'}>{event.sample_label}</Tag>
          <Tag color={event.is_sandbox_available ? 'geekblue' : 'gold'}>{event.event_type_label}</Tag>
          <Tag>{event.status?.[0] || 'demo'}</Tag>
        </Space>
        <div>
          <Title level={4}>{event.title}</Title>
          <Paragraph>{event.subtitle}</Paragraph>
        </div>
        <Text type="secondary">{event.coverage_label}</Text>
        <Button onClick={() => onOpen(targetHash)}>{event.route ? '查看事件页' : '去请求分析 mock'}</Button>
      </Space>
    </Card>
  )
}

export function PublicDemoGuide() {
  const [completedSteps, setCompletedSteps] = useState(readProgress)
  const [query, setQuery] = useState('')

  const completedCount = completedSteps.length
  const progressPercent = Math.round((completedCount / DEMO_STEPS.length) * 100)

  const persistProgress = (nextSteps) => {
    setCompletedSteps(nextSteps)
    try {
      window.localStorage.setItem(STORAGE_KEY, JSON.stringify(nextSteps))
    } catch {
      // Local demo remains usable when storage is unavailable.
    }
  }

  const markComplete = (stepKey) => {
    if (completedSteps.includes(stepKey)) return
    persistProgress([...completedSteps, stepKey])
  }

  const toggleStep = (stepKey) => {
    if (completedSteps.includes(stepKey)) {
      persistProgress(completedSteps.filter((key) => key !== stepKey))
      return
    }
    persistProgress([...completedSteps, stepKey])
  }

  const openStep = (step) => {
    markComplete(step.key)
    window.location.hash = step.targetHash
  }

  const resetProgress = () => {
    persistProgress([])
  }

  const filteredEvents = useMemo(() => {
    const normalizedQuery = query.trim().toLowerCase()
    if (!normalizedQuery) return PUBLIC_EVENT_PLAZA_EVENTS
    return PUBLIC_EVENT_PLAZA_EVENTS.filter((event) => {
      const searchable = [event.title, event.subtitle, event.event_type_label, event.event_type, event.sample_label]
        .filter(Boolean)
        .join(' ')
        .toLowerCase()
      return searchable.includes(normalizedQuery)
    })
  }, [query])

  const openEvent = (targetHash) => {
    window.location.hash = targetHash
  }

  return (
    <div className="page-stack public-demo-guide-page">
      <section className="public-demo-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">C-end guided demo</Tag>
            <Tag color="default">frontend-only</Tag>
            <Tag color="default">no real API</Tag>
          </Space>
          <Title level={1}>Sentigraph 试玩演示 / Guided Demo</Title>
          <Paragraph>
            用 5 分钟体验公共事件舆论生态推演。当前为本地前端 demo，不连接真实平台，不抓取网页，不执行真实平台动作。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<Compass size={16} />} onClick={() => openStep(DEMO_STEPS[0])}>
              开始试玩
            </Button>
            <Button icon={<ThumbsUp size={16} />} onClick={() => openEvent('#/public-events/request')}>
              直接打开请求 / 支持演示
            </Button>
          </Space>
        </div>
        <Card className="panel-card public-demo-progress-card">
          <Space direction="vertical" size={14} className="full-width">
            <Text type="secondary">试玩进度</Text>
            <Title level={2}>
              {completedCount} / {DEMO_STEPS.length}
            </Title>
            <Progress percent={progressPercent} strokeColor="#42f5d7" trailColor="rgba(154,166,191,0.18)" />
            <Button icon={<RotateCcw size={16} />} onClick={resetProgress}>
              重置试玩进度
            </Button>
          </Space>
        </Card>
      </section>

      <Alert
        className="public-demo-boundary-alert"
        type="info"
        showIcon
        message="试玩边界"
        description={
          <Space wrap>
            {BOUNDARY_ITEMS.map((item) => (
              <Tag key={item}>{item}</Tag>
            ))}
          </Space>
        }
      />

      <Card
        className="panel-card public-demo-origin-card"
        title={
          <Space>
            <Database size={17} />
            <span>样本从哪里来？</span>
          </Space>
        }
      >
        <Row gutter={[14, 14]}>
          <Col span={12}>
            <div className="public-demo-origin-tile">
              <Text strong>外部采集桥接</Text>
              <Paragraph>
                抓取项目 / 私人 collector 负责生成本地 Evidence Export package。Sentigraph 只读取 package、验证 package，并把安全样本进入 Evidence / Opinion Ecosystem 展示。
              </Paragraph>
              <Space wrap>
                <Tag color="cyan">local exported package only</Tag>
                <Tag>no crawler job</Tag>
                <Tag>no live search</Tag>
                <Tag>no URL fetch</Tag>
                <Tag>no real platform API</Tag>
                <Tag>no real LLM</Tag>
              </Space>
            </div>
          </Col>
          <Col span={12}>
            <div className="public-demo-origin-tile recommended">
              <Text strong>推荐演示样本</Text>
              <Paragraph>
                当前演示推荐使用 <Text code>helldivers2-psn-demo_20260614_055754</Text>：34 evidence / 7 sources / 28 comments / 6 roots 的 Helldivers selected public sample。
              </Paragraph>
              <Paragraph>
                validation passed / warn 只代表结构、安全、覆盖说明等本地检查通过，不代表全网全量、官方验证或因果证明。
              </Paragraph>
            </div>
          </Col>
          <Col span={24}>
            <Alert
              type="warning"
              showIcon
              message="历史测试包不是主演示样本"
              description="历史 smoke、seed 相关性、local snapshot 包只用于流程测试，不建议作为第一次朋友演示的主样本。Evidence Scale / Coverage 只代表已导入或可用证据覆盖，不代表全网或全平台覆盖。"
            />
          </Col>
        </Row>
      </Card>

      <section>
        <div className="public-event-section-title">
          <Text className="section-kicker">Hands-on path</Text>
          <Title level={3}>第一次来，按这个顺序点</Title>
        </div>
        <Row gutter={[16, 16]}>
          {DEMO_STEPS.map((step) => (
            <Col span={8} key={step.key}>
              <DemoStepCard
                completed={completedSteps.includes(step.key)}
                onOpen={openStep}
                onToggle={toggleStep}
                step={step}
              />
            </Col>
          ))}
        </Row>
      </section>

      <Card
        className="panel-card public-demo-search-card"
        title={
          <Space>
            <Search size={17} />
            <span>搜索本地 demo 事件</span>
          </Space>
        }
      >
        <Space direction="vertical" size={14} className="full-width">
          <Input
            allowClear
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder="搜索本地 demo 事件，例如：游戏 / 品牌 / UP主 / Helldivers"
            prefix={<Search size={16} />}
          />
          <Text type="secondary">此搜索仅筛选本地 demo 事件，不进行全网搜索或抓取。</Text>
          {filteredEvents.length ? (
            <Row gutter={[16, 16]}>
              {filteredEvents.map((event) => (
                <Col span={8} key={event.event_id}>
                  <EventResultCard event={event} onOpen={openEvent} />
                </Col>
              ))}
            </Row>
          ) : (
            <Empty description="没有匹配的本地 demo 事件" />
          )}
        </Space>
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            className="panel-card public-demo-note-card"
            title={
              <Space>
                <ShieldCheck size={17} />
                <span>生态沙盒说明</span>
              </Space>
            }
          >
            <Paragraph>
              进入生态沙盒后，请选择 V2 ecology view 和 Helldivers PSN sample。PeopleCluster 小球代表匿名人群簇，不代表真实个人；InfluenceCore 代表内容、叙事、官方、媒体或 meme 核心，不是人群小球。
            </Paragraph>
            <Paragraph>
              T0-T6 是本地 timeline preset，用于展示事件节奏与风险结构变化，不代表完整历史重建或因果证明。
            </Paragraph>
          </Card>
        </Col>
        <Col span={12}>
          <Card
            className="panel-card public-demo-note-card"
            title={
              <Space>
                <Building2 size={17} />
                <span>请求 / 支持 / B 端咨询说明</span>
              </Space>
            }
          >
            <Paragraph>
              请求分析、支持候选事件和 B 端咨询都是本地演示。它们不会提交后端，不代表自然公众热度，也不会触发真实平台动作。
            </Paragraph>
            <Paragraph>
              如果未来出现赞助分析或商业分析入口，必须透明标注来源与关系，不能和自然讨论热度混合展示。
            </Paragraph>
            <Button icon={<FileText size={16} />} onClick={() => openEvent('#/reports/helldivers-psn-sample')}>
              查看 B端报告样例
            </Button>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
