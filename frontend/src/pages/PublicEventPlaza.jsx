import { Alert, Button, Card, Col, Progress, Row, Space, Tag, Typography } from 'antd'
import { ArrowRight, Building2, Info, Sparkles, Vote } from 'lucide-react'
import { useState } from 'react'

import { PUBLIC_EVENT_PLAZA_EVENTS } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography

const STATUS_COLORS = {
  sample_available: 'green',
  sandbox_available: 'geekblue',
  mock_preview: 'default',
  pending_request: 'gold',
  user_requested: 'cyan',
  pending_analysis: 'orange',
  b_end_sample_preview: 'purple',
  private_demo_only: 'magenta',
}

const STATUS_LABELS = [
  ['selected public sample', '已整理公开样本。可展示，但仍需说明覆盖限制。'],
  ['mock preview', '仅为前端模拟卡片，不代表已有真实样本。'],
  ['user requested', '用户推动分析意向，不等于自然公众热度。'],
  ['sponsored/requested analysis', '必须透明标注，不能混入自然热度。'],
  ['sandbox available', '已有可进入的本地沙盒展示。'],
  ['pending analysis', '候选状态，尚未完成证据复核。'],
]

function StanceBar({ distribution }) {
  return (
    <div className="event-plaza-stance-bar" aria-label="support neutral oppose distribution">
      <span style={{ width: `${distribution.support}%`, background: '#54f5a8' }} />
      <span style={{ width: `${distribution.neutral}%`, background: '#9aa6bf' }} />
      <span style={{ width: `${distribution.oppose}%`, background: '#ff5d8f' }} />
    </div>
  )
}

function MetricLine({ label, value, color }) {
  return (
    <div className="event-plaza-metric-line">
      <Text>{label}</Text>
      <Progress percent={value} strokeColor={color} trailColor="rgba(154,166,191,0.18)" size="small" />
    </div>
  )
}

function EventCard({ event, onNavigate, onMockAction }) {
  const handleClick = () => {
    if (event.route) {
      window.location.hash = event.route
      onNavigate?.('publicEventDetail')
      return
    }
    onMockAction(event)
  }

  return (
    <Card className={`panel-card event-plaza-card ${event.is_sample_available ? 'sample-ready' : 'mock-only'}`}>
      <Space direction="vertical" size={12} className="full-width">
        <div className="event-plaza-card-header">
          <Space wrap>
            <Tag color="cyan">{event.event_type_label}</Tag>
            <Tag color={event.is_sample_available ? 'green' : 'default'}>{event.sample_label}</Tag>
            {event.is_sandbox_available ? <Tag color="geekblue">sandbox available</Tag> : null}
          </Space>
          <Text type="secondary">{event.event_id}</Text>
        </div>
        <div>
          <Title level={4}>{event.title}</Title>
          <Paragraph>{event.subtitle}</Paragraph>
        </div>
        <Space wrap>
          {event.status.map((status) => (
            <Tag key={status} color={STATUS_COLORS[status] || 'default'}>
              {status}
            </Tag>
          ))}
        </Space>
        <div className="event-plaza-metrics">
          <MetricLine label="mock heat" value={event.heat_score_mock} color="#42f5d7" />
          <MetricLine label="controversy" value={event.controversy_score_mock} color="#f5c44b" />
          <MetricLine label="breakout risk" value={event.breakout_risk_mock} color="#ff5d8f" />
        </div>
        <div>
          <div className="event-plaza-stance-labels">
            <Text>support</Text>
            <Text>neutral</Text>
            <Text>oppose</Text>
          </div>
          <StanceBar distribution={event.support_neutral_oppose_distribution} />
        </div>
        <div className="event-plaza-coverage-note">
          <Text strong>{event.source_label}</Text>
          <Paragraph>{event.coverage_label}</Paragraph>
          <Text type="secondary">{event.warning_note}</Text>
        </div>
        <Button
          type={event.route ? 'primary' : 'default'}
          icon={event.route ? <ArrowRight size={16} /> : <Vote size={16} />}
          onClick={handleClick}
        >
          {event.cta_label}
        </Button>
      </Space>
    </Card>
  )
}

export function PublicEventPlaza({ onNavigate }) {
  const [mockNotice, setMockNotice] = useState('')

  const handleMockAction = (event) => {
    setMockNotice(`${event.title}：当前为 mock 入口，尚未提交到后端。请求/投票/赞助意向不代表自然舆情热度。`)
  }

  return (
    <div className="page-stack public-event-page event-plaza-page">
      <section className="event-plaza-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">C-end public preview</Tag>
            <Tag color="default">frontend-only mock</Tag>
            <Tag color="default">not live ranking</Tag>
          </Space>
          <Title level={1}>公共事件广场 / Public Event Plaza</Title>
          <Paragraph>
            看懂公共事件如何发酵、分裂、降温与破圈。当前为本地前端 mock / selected sample 展示，不代表全网全量，也不是自然热榜。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<Sparkles size={16} />} onClick={() => setMockNotice('事件广场 v1 仅展示本地静态卡片，不提交任何后端请求。')}>
              了解当前边界
            </Button>
            <Button icon={<Building2 size={16} />} onClick={() => setMockNotice('B端咨询入口当前为 mock。私有分析可在后续接入更深证据复核、保密语境和场景对比。')}>
              B端咨询入口（mock）
            </Button>
          </Space>
        </div>
        <Card className="panel-card event-plaza-hero-card">
          <Title level={3}>广场不是热榜</Title>
          <Paragraph>
            卡片里的 mock heat、争议度和破圈风险只用于前端演示。用户请求、投票或赞助分析必须透明标注，不能混同为自然公众热度。
          </Paragraph>
          <Space wrap>
            <Tag>not full-web coverage</Tag>
            <Tag>not full-platform coverage</Tag>
            <Tag>not official verification</Tag>
            <Tag>not causal proof</Tag>
          </Space>
        </Card>
      </section>

      <Card className="panel-card event-plaza-status-card" title="Status labels / 状态标签">
        <Row gutter={[12, 12]}>
          {STATUS_LABELS.map(([label, description]) => (
            <Col span={8} key={label}>
              <div className="event-plaza-status-tile">
                <Text strong>{label}</Text>
                <Paragraph>{description}</Paragraph>
              </div>
            </Col>
          ))}
        </Row>
      </Card>

      {mockNotice ? (
        <Alert
          type="info"
          showIcon
          message="Mock action"
          description={mockNotice}
          closable
          onClose={() => setMockNotice('')}
        />
      ) : null}

      <section>
        <div className="public-event-section-title">
          <Text className="section-kicker">Event cards</Text>
          <Title level={3}>公开事件候选与样本</Title>
        </div>
        <Row gutter={[16, 16]}>
          {PUBLIC_EVENT_PLAZA_EVENTS.map((event) => (
            <Col span={event.is_sample_available ? 12 : 6} key={event.event_id}>
              <EventCard event={event} onNavigate={onNavigate} onMockAction={handleMockAction} />
            </Col>
          ))}
        </Row>
      </section>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            className="panel-card event-plaza-explainer-card"
            title={
              <Space>
                <Info size={17} />
                <span>如何请求分析一个事件？</span>
              </Space>
            }
          >
            <Paragraph>
              未来用户可以提交事件标题、公开链接和请求理由。请求/投票数量只是用户推动分析的信号，不是自然舆情热度，也不会被包装成公开排名。
            </Paragraph>
            <Paragraph>
              赞助分析必须显著标注；不做隐藏推广，不制造虚假公众热度。
            </Paragraph>
            <Space wrap>
              <Button onClick={() => handleMockAction(PUBLIC_EVENT_PLAZA_EVENTS[1])}>请求分析（mock）</Button>
              <Button onClick={() => handleMockAction(PUBLIC_EVENT_PLAZA_EVENTS[2])}>投票支持（mock）</Button>
              <Button onClick={() => handleMockAction(PUBLIC_EVENT_PLAZA_EVENTS[3])}>提交公开链接（mock）</Button>
            </Space>
          </Card>
        </Col>
        <Col span={12}>
          <Card className="panel-card event-plaza-explainer-card" title="需要私有分析？">
            <Paragraph>
              品牌、MCN、创作者团队、游戏社区运营或公关团队可以申请私有分析。私有分析可包含更深证据复核、保密语境、更丰富报告和场景对比。
            </Paragraph>
            <Paragraph>当前按钮只是 C 端 v1 mock，不提交后端，也不触发任何外部服务。</Paragraph>
            <Button onClick={() => handleMockAction(PUBLIC_EVENT_PLAZA_EVENTS[4])}>B端咨询（mock）</Button>
          </Card>
        </Col>
      </Row>

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        message="公共广场边界"
        description="本页是 frontend-only mock。只有明确标注 selected public sample 的事件才有公开样本；mock preview / pending analysis 不代表证据已完成。页面不代表 full-web、full-platform、official verification、causal proof，不执行真实平台动作，不调用真实 API 或 LLM。PeopleCluster 表示人群簇，不是个人；InfluenceCore 表示内容/叙事/官方/媒体/梗核心。"
      />
    </div>
  )
}
