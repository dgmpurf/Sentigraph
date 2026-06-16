import { Alert, Button, Card, Col, List, Progress, Row, Space, Tag, Timeline, Typography } from 'antd'
import {
  ArrowLeft,
  ArrowRight,
  BarChart3,
  Boxes,
  FileText,
  FlaskConical,
  ShieldCheck,
  TriangleAlert,
} from 'lucide-react'

import { HELLDIVERS_PUBLIC_EVENT } from '../data/publicEventSamples.js'
import { HELLDIVERS_TIMELINE_PRESETS } from '../data/helldivers2PsnTimelinePresets.js'

const { Paragraph, Text, Title } = Typography

const COVERAGE_STATS = [
  ['Evidence', HELLDIVERS_PUBLIC_EVENT.sample_summary.evidence_items, 'selected public sample'],
  ['Sources', HELLDIVERS_PUBLIC_EVENT.sample_summary.sources, 'source list reviewed locally'],
  ['Comments', HELLDIVERS_PUBLIC_EVENT.sample_summary.comment_samples, 'comment samples only'],
  ['Roots', HELLDIVERS_PUBLIC_EVENT.sample_summary.root_candidates, 'InfluenceCore candidates'],
]

const ECOSYSTEM_ITEMS = [
  {
    title: 'InfluenceCore',
    copy: '样本呈现社区反弹、官方回应、FAQ / 媒体解释、社区解构等核心叙事。InfluenceCore 是内容、叙事、官方、媒体或 meme 核心，不是人群小球。',
  },
  {
    title: 'EchoBox',
    copy: '主要讨论圈层包括官方公告区、玩家社区、媒体解释区和梗化记忆区。它们帮助解释讨论聚集、扩散压力和降温窗口。',
  },
  {
    title: 'PeopleCluster',
    copy: 'PeopleCluster 表示匿名人群簇或观点簇，不代表真实个人用户，也不用于个人影响力画像。',
  },
  {
    title: 'Camp Dynamics',
    copy: '报告用反弹、解释、中立化、疲劳、声誉记忆和再激活风险来描述公开讨论结构变化。',
  },
]

const RESPONSE_TEMPO_ITEMS = [
  ['官方澄清', '判断什么阶段适合透明说明规则变化原因、影响范围和后续安排。'],
  ['FAQ / 长文解释', '判断复杂背景是否需要被结构化解释，降低误读和信息缺口。'],
  ['第三方说明', '判断可信第三方或社区语言是否有桥接价值。'],
  ['社区解构', '判断社区符号、梗和二创是否有助于降温，或是否留下长期记忆。'],
  ['延迟 / 无回应', '判断沉默是否可能留下长期声誉记忆或再激活风险。'],
]

const RISK_OPPORTUNITY_ITEMS = [
  ['破圈风险', '讨论压力可能从核心社区外溢到更广泛受众。', 'local heuristic / not a guaranteed forecast'],
  ['反噬风险', '回应措辞、时机或解释不足可能重新激活不满。', 'requires human review'],
  ['长尾声誉记忆', '事件可能沉淀为梗、截图、纪念物或后续讨论触发点。', 'selected sample only'],
  ['社区解构窗口', '社区语言可能把高压冲突转为可讨论的符号和复盘。', 'not automatic success'],
  ['第三方解释空间', '媒体或第三方整理可能帮助中立用户理解事件脉络。', 'not official verification'],
  ['样本不确定性', '小样本和来源覆盖限制会影响结论表达。', 'model-card TBD'],
]

const SAMPLE_ACTIONS = [
  '透明说明政策变更原因和影响范围。',
  '明确哪些地区、平台或用户群体受影响。',
  '提供 FAQ / 长文解释，降低信息缺口。',
  '通过可信第三方或社区语言解释复杂背景。',
  '承认沟通节奏问题，避免把低响应误读为问题消失。',
  '持续监测声誉记忆和再激活风险。',
]

function goToHash(hash) {
  window.location.hash = hash
}

function ReportMetric({ label, value, note }) {
  return (
    <Card className="panel-card business-report-stat-card">
      <Text type="secondary">{label}</Text>
      <Title level={2}>{value}</Title>
      <Paragraph>{note}</Paragraph>
    </Card>
  )
}

function ReportSectionTitle({ kicker, title }) {
  return (
    <div className="business-report-section-title">
      <Text className="section-kicker">{kicker}</Text>
      <Title level={3}>{title}</Title>
    </div>
  )
}

export function BusinessReportSample() {
  const timelineItems = HELLDIVERS_TIMELINE_PRESETS.map((phase) => ({
    color: phase.phase_id === 't1' ? 'red' : phase.phase_id === 't2' ? 'green' : 'blue',
    children: (
      <div className="business-report-timeline-item">
        <Text strong>{phase.label_zh}</Text>
        <Paragraph>{phase.short_explanation_zh}</Paragraph>
        <Text type="secondary">{phase.label_en}</Text>
      </div>
    ),
  }))

  return (
    <div className="page-stack business-report-page">
      <section className="business-report-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">selected public sample</Tag>
            <Tag>local demo</Tag>
            <Tag>not full-web</Tag>
            <Tag>not official verification</Tag>
            <Tag>not causal proof</Tag>
          </Space>
          <Title level={1}>B端报告样例：Helldivers 2 / PSN 账号绑定争议</Title>
          <Paragraph>
            面向品牌、公关、MCN、创作者、游戏社区或团队内部复盘的专业报告样例。页面展示报告表达方式和分析框架，不代表生产级交付或完整验证。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<Boxes size={17} />} onClick={() => goToHash('#/opinion-ecosystem')}>
              打开生态沙盒
            </Button>
            <Button icon={<ArrowLeft size={17} />} onClick={() => goToHash('#/public-events/helldivers-psn')}>
              查看公开事件页
            </Button>
            <Button icon={<ArrowRight size={17} />} onClick={() => goToHash('#/public-events/request')}>
              请求分析类似事件
            </Button>
          </Space>
        </div>
        <Card className="panel-card business-report-hero-card">
          <Space direction="vertical" size={12}>
            <Tag color="gold">Report sample / not production delivery</Tag>
            <Title level={3}>边界先行</Title>
            <Paragraph>
              本页使用 Helldivers selected public sample。它不是全网覆盖、不是全平台覆盖、不是官方验证，也不是因果证明；Sandbox V2 是前端视觉原型，T0-T6 是本地历史复盘 preset。
            </Paragraph>
          </Space>
        </Card>
      </section>

      <Card className="panel-card business-report-summary-card" title="管理层摘要 / Executive Summary">
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Space direction="vertical" size={12}>
              <div className="business-report-summary-line">
                <Text strong>事件核心</Text>
                <Paragraph>
                  本地样本显示，PSN 账号绑定要求引发玩家对购买预期、平台限制和信任边界的反弹。
                </Paragraph>
              </div>
              <div className="business-report-summary-line">
                <Text strong>舆论结构</Text>
                <Paragraph>
                  反对核心集中在玩家社区与评价系统；官方回应后，讨论进入解释、社区解构与长期声誉记忆阶段。
                </Paragraph>
              </div>
            </Space>
          </Col>
          <Col span={12}>
            <Space direction="vertical" size={12}>
              <div className="business-report-summary-line">
                <Text strong>样本限制</Text>
                <Paragraph>
                  当前仅基于 selected public sample，不代表全网全量、全平台全量或完整历史重建。
                </Paragraph>
              </div>
              <div className="business-report-summary-line">
                <Text strong>决策用途</Text>
                <Paragraph>
                  用于展示证据治理、讨论结构解释、回应节奏复盘和报告表达方式，不用于自动决策。
                </Paragraph>
              </div>
            </Space>
          </Col>
        </Row>
      </Card>

      <section>
        <ReportSectionTitle kicker="Coverage" title="证据覆盖与可信度" />
        <Row gutter={[16, 16]}>
          {COVERAGE_STATS.map(([label, value, note]) => (
            <Col span={6} key={label}>
              <ReportMetric label={label} value={value} note={note} />
            </Col>
          ))}
        </Row>
        <Card className="panel-card business-report-coverage-card">
          <Row gutter={[16, 16]} align="middle">
            <Col span={14}>
              <Space wrap>
                <Tag color="gold">validation: warn</Tag>
                <Tag color="green">errors: 0</Tag>
                <Tag color="orange">warnings: 2</Tag>
                <Tag>privacy checked</Tag>
                <Tag>coverage limitation</Tag>
              </Space>
              <Paragraph>
                warn 对 demo 可接受，但不等于生产级交付。当前警告包括样本规模低于目标和跳过部分来源；面向真实客户前仍需来源可信度、验证状态和样本覆盖复核。
              </Paragraph>
            </Col>
            <Col span={10}>
              <Alert
                type="warning"
                showIcon
                message="覆盖不等于全量"
                description="Evidence Coverage 只表示已导入或可用证据覆盖，不代表 full-web、full-platform 或官方验证。"
              />
            </Col>
          </Row>
        </Card>
      </section>

      <section>
        <ReportSectionTitle kicker="Opinion Ecosystem" title="舆论生态摘要" />
        <Row gutter={[16, 16]}>
          {ECOSYSTEM_ITEMS.map((item) => (
            <Col span={12} key={item.title}>
              <Card className="panel-card business-report-ecosystem-card">
                <Space direction="vertical" size={8}>
                  <Tag color="cyan">{item.title}</Tag>
                  <Paragraph>{item.copy}</Paragraph>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      <section>
        <ReportSectionTitle kicker="Historical replay" title="T0-T6 历史复盘" />
        <Card className="panel-card business-report-timeline-card">
          <Alert
            type="info"
            showIcon
            message="本地历史复盘 preset"
            description="T0-T6 是本地历史复盘 preset，不是完整历史重建，也不是未来预测。"
          />
          <Timeline items={timelineItems} />
        </Card>
      </section>

      <section>
        <ReportSectionTitle kicker="Response Tempo" title="回应节奏复盘" />
        <Row gutter={[16, 16]}>
          {RESPONSE_TEMPO_ITEMS.map(([title, copy]) => (
            <Col span={8} key={title}>
              <Card className="panel-card business-report-tempo-card">
                <Text strong>{title}</Text>
                <Paragraph>{copy}</Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
        <Alert
          className="business-report-section-alert"
          type="info"
          showIcon
          message="比较性复盘，不是保证最优策略"
          description="本页只展示 B 端报告如何描述回应节奏、降压窗口和再激活风险，不提供自动化最佳策略或法律、公关保证。"
        />
      </section>

      <section>
        <ReportSectionTitle kicker="Risk and opportunity" title="风险与机会" />
        <Row gutter={[16, 16]}>
          {RISK_OPPORTUNITY_ITEMS.map(([title, copy, status]) => (
            <Col span={8} key={title}>
              <Card className="panel-card business-report-risk-card">
                <Space direction="vertical" size={10}>
                  <TriangleAlert size={18} />
                  <Text strong>{title}</Text>
                  <Paragraph>{copy}</Paragraph>
                  <Tag>{status}</Tag>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
      </section>

      <Row gutter={[16, 16]}>
        <Col span={14}>
          <Card
            className="panel-card business-report-actions-card"
            title={
              <Space>
                <ShieldCheck size={17} />
                <span>样例建议：不是自动决策</span>
              </Space>
            }
          >
            <List
              dataSource={SAMPLE_ACTIONS}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
            <Alert
              type="warning"
              showIcon
              message="报告格式样例"
              description="这些是报告表达示例，不是真实客户建议，不是法律意见，也不保证公关结果。"
            />
          </Card>
        </Col>
        <Col span={10}>
          <Card
            className="panel-card business-report-export-card"
            title={
              <Space>
                <FileText size={17} />
                <span>报告导出 / Export（规划中）</span>
              </Space>
            }
          >
            <Paragraph>
              未来 B 端版本可导出 PDF、Markdown 或 briefing deck，包含 evidence coverage、Opinion Ecosystem summary、response tempo、uncertainty 和 suggested actions。
            </Paragraph>
            <Paragraph>当前仅为前端样例页，不生成真实报告文件。</Paragraph>
            <Progress percent={35} strokeColor="#42f5d7" trailColor="rgba(154,166,191,0.18)" />
          </Card>
        </Col>
      </Row>

      <Card className="panel-card business-report-next-card">
        <Row gutter={[16, 16]} align="middle">
          <Col span={16}>
            <Space direction="vertical" size={8}>
              <Tag color="cyan">Next view</Tag>
              <Title level={3}>把报告摘要和生态沙盒连起来看</Title>
              <Paragraph>
                先阅读本页报告结构，再打开 Sandbox V2 查看 EchoBox、PeopleCluster、InfluenceCore 和 T0-T6 历史复盘如何被视觉化。
              </Paragraph>
            </Space>
          </Col>
          <Col span={8} className="public-event-action-col">
            <Button type="primary" size="large" icon={<BarChart3 size={17} />} onClick={() => goToHash('#/opinion-ecosystem')}>
              打开生态沙盒
            </Button>
          </Col>
        </Row>
      </Card>

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        icon={<FlaskConical size={18} />}
        message="B端报告样例边界"
        description="本页是 frontend-only local demo。Helldivers PSN 是 selected public sample；不是 full-web coverage、不是 full-platform coverage、不是 official verification、不是 causal proof。没有真实 API、没有真实 LLM、没有真实爬取、没有真实客户报告导出或真实平台动作。"
      />
    </div>
  )
}
