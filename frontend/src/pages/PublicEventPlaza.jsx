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
  candidate_demo_sample: 'cyan',
  review_needed: 'gold',
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

function EventCard({ event, guided, onNavigate }) {
  const isGuidedSample = guided && event.guided_recommended
  const handleClick = () => {
    if (event.route) {
      window.location.hash = event.route
      return
    }
    window.location.hash = '#/public-events/request'
    onNavigate?.('publicEventRequest')
  }

  return (
    <Card className={`panel-card event-plaza-card ${event.is_sample_available ? 'sample-ready' : 'mock-only'} ${isGuidedSample ? 'guided-highlight' : ''}`}>
      <Space direction="vertical" size={12} className="full-width">
        <div className="event-plaza-card-header">
          <Space wrap>
            <Tag color="cyan">{event.event_type_label}</Tag>
            <Tag color={event.is_sample_available ? 'green' : 'default'}>{event.sample_label}</Tag>
            {event.is_sandbox_available ? <Tag color="geekblue">sandbox available</Tag> : null}
            {isGuidedSample ? <Tag color="gold">推荐试玩样本</Tag> : null}
            {isGuidedSample ? <Tag color="green">当前唯一完整体验样本</Tag> : null}
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
          {isGuidedSample ? '继续试玩：查看 Helldivers 分析' : event.cta_label}
        </Button>
      </Space>
    </Card>
  )
}

export function PublicEventPlaza({ guided = false, onNavigate }) {
  const [activeInfoPanel, setActiveInfoPanel] = useState('')

  const openRequestPage = () => {
    window.location.hash = '#/public-events/request'
    onNavigate?.('publicEventRequest')
  }

  const closeInfoPanel = () => setActiveInfoPanel('')

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
            <Button type="primary" icon={<Sparkles size={16} />} onClick={() => setActiveInfoPanel('boundary')}>
              数据来源与限制
            </Button>
            <Button icon={<Vote size={16} />} onClick={openRequestPage}>
              请求分析一个事件
            </Button>
            <Button icon={<Building2 size={16} />} onClick={() => setActiveInfoPanel('private')}>
              企业 / 团队私有分析咨询
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

      {guided ? (
        <Alert
          className="event-plaza-guided-banner"
          type="success"
          showIcon
          message="试玩引导：请选择 Helldivers 推荐样本"
          description="你正在从 Demo 试玩页进入公共事件广场。建议点击标记为“推荐试玩样本 / 当前唯一完整体验样本”的 Helldivers 2 / PSN 账号绑定争议卡片，继续查看公开事件详情和生态沙盒。"
        />
      ) : null}

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

      {activeInfoPanel === 'boundary' ? (
        <Alert
          className="event-plaza-info-panel"
          type="info"
          showIcon
          message="数据来源与限制"
          description="当前广场只展示本地 demo 事件和 selected public sample。它不是实时榜单，不进行全网搜索，不抓取 URL，不调用真实平台 API 或 LLM；只有明确标记为 selected public sample 的事件才有已整理样本。"
          closable
          onClose={closeInfoPanel}
        />
      ) : null}
      {activeInfoPanel === 'private' ? (
        <Alert
          className="event-plaza-info-panel"
          type="info"
          showIcon
          message="企业 / 团队私有分析咨询"
          description="当前只是前端入口演示，不提交信息。未来私有分析可面向品牌、MCN、创作者团队、公关团队或游戏社区运营，提供更深证据复核、保密语境、报告和场景对比，并且必须透明标注来源和关系。"
          closable
          onClose={closeInfoPanel}
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
              <EventCard event={event} guided={guided} onNavigate={onNavigate} />
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
              <Button onClick={openRequestPage}>请求分析（mock）</Button>
              <Button onClick={openRequestPage}>投票支持（mock）</Button>
              <Button onClick={openRequestPage}>提交公开链接（mock）</Button>
            </Space>
          </Card>
        </Col>
        <Col span={12}>
          <Card className="panel-card event-plaza-explainer-card" title="需要私有分析？">
            <Paragraph>
              品牌、MCN、创作者团队、游戏社区运营或公关团队可以申请私有分析。私有分析可包含更深证据复核、保密语境、更丰富报告和场景对比。
            </Paragraph>
            <Paragraph>当前按钮只是 C 端 v1 mock，不提交后端，也不触发任何外部服务。</Paragraph>
            <Button onClick={() => setActiveInfoPanel('private')}>企业 / 团队私有分析咨询</Button>
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
