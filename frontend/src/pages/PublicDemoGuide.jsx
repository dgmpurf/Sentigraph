import { Alert, Button, Card, Col, Empty, Input, Progress, Row, Space, Tag, Typography } from 'antd'
import {
  Building2,
  CheckCircle2,
  Compass,
  ExternalLink,
  RotateCcw,
  Search,
  ShieldCheck,
  Vote,
} from 'lucide-react'
import { useMemo, useState } from 'react'

import { PUBLIC_EVENT_PLAZA_EVENTS } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography

const STORAGE_KEY = 'sentigraph-public-demo-progress-v1'

const DEMO_STEPS = [
  {
    key: 'plaza',
    title: 'Step 1：浏览公共事件广场',
    buttonLabel: '打开事件广场',
    targetHash: '#/public-events',
    description: '查看多个公共事件卡片。当前不是真实热榜，而是本地 demo 事件列表。',
  },
  {
    key: 'helldivers',
    title: 'Step 2：查看 Helldivers 公开事件页',
    buttonLabel: '打开 Helldivers 事件页',
    targetHash: '#/public-events/helldivers-psn',
    description: '查看 selected public sample、事件时间线、样本边界和生态沙盒入口。',
  },
  {
    key: 'sandbox',
    title: 'Step 3：进入生态沙盒 V2',
    buttonLabel: '打开生态沙盒 V2',
    targetHash: '#/opinion-ecosystem',
    description: '进入页面后请选择 V2 ecology view + Helldivers PSN sample。这里不做 URL 抓取，也不连接真实平台。',
  },
  {
    key: 'timeline',
    title: 'Step 4：体验 T0-T6 时间线',
    buttonLabel: '打开沙盒并体验时间线',
    targetHash: '#/opinion-ecosystem',
    description: '依次点击 T0 公告、T1 社区反弹、T2 官方回应、T3 第三方解释、T4 社区解构、T5 疲劳衰减、T6 声誉记忆。',
  },
  {
    key: 'request',
    title: 'Step 5：请求分析一个事件 mock',
    buttonLabel: '打开请求分析页',
    targetHash: '#/public-events/request',
    description: '填写事件标题和理由，生成本地请求预览。不会提交后端。',
  },
  {
    key: 'vote',
    title: 'Step 6：投票支持分析 mock',
    buttonLabel: '打开投票区',
    targetHash: '#/public-events/request',
    description: '点击投票支持，只改变本地 UI，不代表真实热度。',
  },
  {
    key: 'bEnd',
    title: 'Step 7：B 端咨询 mock',
    buttonLabel: '查看 B 端咨询 mock',
    targetHash: '#/public-events/request',
    description: '当前只是入口演示，不提交信息。赞助或商业分析必须透明标注。',
  },
]

const BOUNDARY_ITEMS = [
  'frontend-only local demo',
  'selected public sample where labeled',
  'request / vote mock only',
  'not full-web coverage',
  'not full-platform coverage',
  'not official verification',
  'not causal proof',
  'no real platform action',
  'no real API / no real LLM call',
  'PeopleCluster = anonymous groups/clusters, not real individuals',
  'InfluenceCore = content / narrative / official / media / meme cores, not people balls',
  'request/vote count does not represent natural public-opinion heat',
  'sponsored analysis must be transparently labeled',
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
            用 5 分钟体验公共事件舆论生态推演。当前为本地前端 demo，不连接真实平台，不抓取网页，不提交后端。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<Compass size={16} />} onClick={() => openStep(DEMO_STEPS[0])}>
              开始试玩
            </Button>
            <Button icon={<Vote size={16} />} onClick={() => openEvent('#/public-events/request')}>
              直接打开请求 / 投票 mock
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
                <span>请求 / 投票 / B 端咨询说明</span>
              </Space>
            }
          >
            <Paragraph>
              请求分析、投票支持分析和 B 端咨询都是本地 mock。它们不会提交后端，不代表自然公众热度，也不会触发真实平台动作。
            </Paragraph>
            <Paragraph>
              如果未来出现赞助分析或商业分析入口，必须透明标注来源与关系，不能和自然讨论热度混合展示。
            </Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  )
}
