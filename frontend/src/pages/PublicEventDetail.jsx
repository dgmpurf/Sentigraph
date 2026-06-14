import { Alert, Button, Card, Col, List, Progress, Row, Space, Statistic, Tag, Timeline, Typography } from 'antd'
import { ArrowRight, Boxes, CircleDot, FileCheck2, FlaskConical, ShieldCheck, Vote } from 'lucide-react'

import { HELLDIVERS_PUBLIC_EVENT } from '../data/publicEventSamples.js'

const { Paragraph, Text, Title } = Typography

const boundaryTags = [
  'frontend-only local demo',
  'selected public sample',
  'not full-web coverage',
  'not full-platform coverage',
  'not full-thread coverage',
  'not official verification',
  'not causal proof',
  'no real platform action',
  'no real API / no real LLM call',
  'PeopleCluster not real individuals',
]

function CompactMetric({ title, value, suffix }) {
  return (
    <Card className="metric-card public-event-metric-card">
      <Statistic title={title} value={value} suffix={suffix} />
    </Card>
  )
}

function SectionTitle({ kicker, title }) {
  return (
    <div className="public-event-section-title">
      <Text className="section-kicker">{kicker}</Text>
      <Title level={3}>{title}</Title>
    </div>
  )
}

export function PublicEventDetail({ onNavigate }) {
  const event = HELLDIVERS_PUBLIC_EVENT

  const openSandbox = () => {
    window.location.hash = '#/opinion-ecosystem'
    onNavigate?.('opinionEcosystem')
  }

  return (
    <div className="page-stack public-event-page">
      <section className="public-event-hero">
        <div className="public-event-hero-copy">
          <Space wrap>
            <Tag color="cyan">{event.event_type_label}</Tag>
            <Tag color="green">sample available</Tag>
            <Tag color="geekblue">sandbox available</Tag>
            <Tag color="default">not full-web</Tag>
            <Tag color="default">not causal proof</Tag>
          </Space>
          <Title level={1}>{event.title}</Title>
          <Paragraph>{event.subtitle}</Paragraph>
          <Space wrap>
            <Button type="primary" size="large" icon={<Boxes size={17} />} onClick={openSandbox}>
              {event.ctas.sandbox}
            </Button>
            <Button size="large" icon={<Vote size={17} />}>
              {event.ctas.requestSimilar}
            </Button>
            <Button size="large" icon={<ShieldCheck size={17} />}>
              {event.ctas.bEndInquiry}
            </Button>
          </Space>
        </div>
        <Card className="panel-card public-event-hero-card">
          <Space direction="vertical" size={12}>
            <Text type="secondary">样本状态</Text>
            <Title level={3}>Helldivers PSN selected public sample</Title>
            <Paragraph>
              这是一个面向公众解释的本地前端样本页。页面只展示整理后的样本状态和沙盒入口，不代表完整平台覆盖或官方核验。
            </Paragraph>
            <Space wrap>
              {event.labels.map((label) => (
                <Tag key={label}>{label}</Tag>
              ))}
            </Space>
          </Space>
        </Card>
      </section>

      <Row gutter={[16, 16]}>
        <Col span={6}>
          <CompactMetric title="Evidence items" value={event.sample_summary.evidence_items} />
        </Col>
        <Col span={6}>
          <CompactMetric title="Sources" value={event.sample_summary.sources} />
        </Col>
        <Col span={6}>
          <CompactMetric title="Comment samples" value={event.sample_summary.comment_samples} />
        </Col>
        <Col span={6}>
          <CompactMetric title="Root / InfluenceCore" value={event.sample_summary.root_candidates} />
        </Col>
      </Row>

      <Card className="panel-card public-event-sample-card" title="Sample status / 样本状态">
        <Row gutter={[16, 16]}>
          <Col span={14}>
            <Space direction="vertical" size={10}>
              <Space wrap>
                <Tag color="gold">{event.sample_summary.validator_status}</Tag>
                <Tag color="default">{event.sample_summary.sample_label}</Tag>
              </Space>
              <Paragraph>
                当前页面基于已整理的本地前端 fixture。它适合解释产品能力和样本阅读方式，不适合作为全网事实结论。
              </Paragraph>
              <Space wrap>
                {boundaryTags.map((tag) => (
                  <Tag key={tag}>{tag}</Tag>
                ))}
              </Space>
            </Space>
          </Col>
          <Col span={10}>
            <Alert
              type="warning"
              showIcon
              message="Validator warnings accepted"
              description={event.sample_summary.warnings.join('；')}
            />
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={13}>
          <Card className="panel-card" title="Event timeline / 事件时间线">
            <Timeline
              items={event.timeline.map((item) => ({
                color: item.tone === 'community' ? 'red' : item.tone === 'update' ? 'green' : 'blue',
                children: (
                  <div>
                    <Text strong>{item.title}</Text>
                    <Paragraph>{item.description}</Paragraph>
                  </div>
                ),
              }))}
            />
          </Card>
        </Col>
        <Col span={11}>
          <Card className="panel-card public-event-reading-card" title="How to read this page / 如何阅读本页">
            <List
              dataSource={[
                ['Evidence', '已收集或导入的样本材料，不等于全网全量材料。'],
                ['InfluenceCore', '官方、媒体、社区、梗或叙事核心，不是一个人群小球。'],
                ['EchoBox', '讨论容器或回音边界，用来解释讨论集中度。'],
                ['PeopleCluster', '匿名群组/观点簇，不代表真实个人用户。'],
                ['ResponseTempo', '情景化决策参考，不是因果证明。'],
              ]}
              renderItem={([label, description]) => (
                <List.Item>
                  <div className="ecosystem-reading-row">
                    <Text strong>{label}</Text>
                    <Paragraph>{description}</Paragraph>
                  </div>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      <section>
        <SectionTitle kicker="Narrative cores" title="InfluenceCore preview" />
        <Row gutter={[16, 16]}>
          {event.influence_cores.map((core) => (
            <Col span={core.type === 'community_memory' ? 24 : 12} key={core.title}>
              <Card className="panel-card public-event-core-card">
                <Space direction="vertical" size={8}>
                  <Space wrap>
                    <Tag color="cyan">{core.type}</Tag>
                    <Tag>{core.role}</Tag>
                  </Space>
                  <Title level={4}>{core.title}</Title>
                  <Paragraph>{core.why_it_matters}</Paragraph>
                  <Text type="secondary">{core.confidence_note}</Text>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      <section>
        <SectionTitle kicker="Discussion containers" title="EchoBox preview" />
        <Row gutter={[16, 16]}>
          {event.echo_boxes.map((box) => (
            <Col span={8} key={box.title}>
              <Card className="panel-card public-event-echo-card">
                <Space direction="vertical" size={12}>
                  <Title level={4}>{box.title}</Title>
                  <Progress percent={box.saturation} strokeColor="#42f5d7" trailColor="rgba(154,166,191,0.18)" />
                  <Progress percent={box.breakout_risk} strokeColor="#f5c44b" trailColor="rgba(154,166,191,0.18)" />
                  <Text type="secondary">{box.limitation}</Text>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="panel-card" title="PeopleCluster distribution / 人群簇分布">
            <List
              dataSource={event.people_clusters}
              renderItem={(cluster) => (
                <List.Item>
                  <div className="public-event-cluster-row">
                    <Space>
                      <span className="ecosystem-dot" style={{ background: cluster.color }} />
                      <div>
                        <Text strong>{cluster.label}</Text>
                        <Paragraph>{cluster.note}</Paragraph>
                      </div>
                    </Space>
                    <Tag color="default">{cluster.share}%</Tag>
                  </div>
                </List.Item>
              )}
            />
            <Alert type="info" showIcon message="小球代表匿名群组/观点簇，不代表真实个人。" />
          </Card>
        </Col>
        <Col span={12}>
          <Card className="panel-card" title="ResponseTempo / ReputationMemory">
            <Space direction="vertical" size={14}>
              <div className="public-event-note-tile">
                <Text strong>ResponseTempo</Text>
                <Paragraph>{event.response_tempo.summary}</Paragraph>
                <Text type="secondary">{event.response_tempo.note}</Text>
              </div>
              <div className="public-event-note-tile">
                <Text strong>ReputationMemory</Text>
                <Paragraph>{event.reputation_memory.summary}</Paragraph>
                <Text type="secondary">{event.reputation_memory.note}</Text>
              </div>
            </Space>
          </Card>
        </Col>
      </Row>

      <Card className="panel-card public-event-sandbox-entry">
        <Row gutter={[16, 16]} align="middle">
          <Col span={16}>
            <Space direction="vertical" size={8}>
              <Tag color="cyan">Opinion Ecosystem Sandbox</Tag>
              <Title level={3}>打开生态沙盒并切换到 Helldivers PSN sample</Title>
              <Paragraph>
                沙盒用于视觉化解释 EchoBox、PeopleCluster、InfluenceCore 和回应节奏。它仍是本地前端样本，不执行真实平台动作。
              </Paragraph>
            </Space>
          </Col>
          <Col span={8} className="public-event-action-col">
            <Button type="primary" size="large" icon={<ArrowRight size={17} />} onClick={openSandbox}>
              查看生态沙盒
            </Button>
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            className="panel-card public-event-mock-card"
            title={
              <Space>
                <CircleDot size={17} />
                <span>想看类似事件推演？</span>
              </Space>
            }
          >
            <Paragraph>
              当前为 mock 入口，不提交到后端。用户请求 / 赞助分析必须透明标注，不代表自然舆情热度。
            </Paragraph>
            <Space wrap>
              <Button>请求分析</Button>
              <Button>投票支持分析</Button>
              <Button>提交公开链接</Button>
            </Space>
          </Card>
        </Col>
        <Col span={12}>
          <Card
            className="panel-card public-event-mock-card"
            title={
              <Space>
                <FileCheck2 size={17} />
                <span>B端咨询 / 私有分析</span>
              </Space>
            }
          >
            <Paragraph>
              如果你是品牌、MCN、创作者团队、游戏社区运营或公关团队，可以申请私有分析。私有分析可包含更深证据复核、保密语境、丰富报告和场景对比。
            </Paragraph>
            <Button>申请私有分析（mock）</Button>
          </Card>
        </Col>
      </Row>

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        icon={<FlaskConical size={18} />}
        message="Boundary footer / 页面边界"
        description="本页是 frontend-only local demo，使用 selected public sample，不代表 full-web、full-platform、full-thread coverage，不是 official verification，不是 causal proof，不执行真实平台动作，不调用真实 API 或真实 LLM。PeopleCluster 不是个人画像，InfluenceCore 是内容/叙事/官方/媒体/梗核心。"
      />
    </div>
  )
}
