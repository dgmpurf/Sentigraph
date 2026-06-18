import { Alert, Button, Card, Col, List, Progress, Row, Space, Tag, Timeline, Typography } from 'antd'
import {
  ArrowLeft,
  BarChart3,
  Boxes,
  FileText,
  FlaskConical,
  Scale,
  ShieldCheck,
  TriangleAlert,
} from 'lucide-react'

import { DONGLU_SUNJIHAI_PUBLIC_EVENT } from '../data/publicEventSamples.js'
import { DONGLU_SUNJIHAI_TIMELINE_PRESETS } from '../data/dongluSunjihaiTimelinePresets.js'

const { Paragraph, Text, Title } = Typography

const SAMPLE_SUMMARY = DONGLU_SUNJIHAI_PUBLIC_EVENT.sample_summary
const PLATFORM_DISTRIBUTION = DONGLU_SUNJIHAI_PUBLIC_EVENT.platform_distribution || {}

const COVERAGE_STATS = [
  ['Evidence', SAMPLE_SUMMARY.evidence_items, 'controlled candidate public sample'],
  ['Comments', SAMPLE_SUMMARY.comment_samples, 'comment samples only'],
  ['Sources', SAMPLE_SUMMARY.sources, 'source categories reviewed locally'],
  ['Roots', SAMPLE_SUMMARY.root_candidates, 'InfluenceCore candidates'],
]

const ECOSYSTEM_DIRECTIONS = [
  {
    title: '支持董路路线 / 经验派讨论',
    copy: '样本中可以观察到围绕训练实践、长期投入、项目经验与中国足球青训路径的支持性讨论。它只代表样本内的表达方向，不代表全平台比例。',
  },
  {
    title: '支持孙继海 / 精英青训路线讨论',
    copy: '样本中也存在围绕嗨球少年、精英青训、专业体系和长期路径的支持性讨论。该方向需要后续人工复核，不应被简化为个人对立。',
  },
  {
    title: '中立流程与制度关注',
    copy: '一部分讨论关注时间线、项目责任、青训制度、公共表达边界和信息缺口，更适合作为事实边界澄清与 FAQ 的素材入口。',
  },
  {
    title: '反感争吵 / 舆论疲劳',
    copy: '样本中可观察到对持续争吵、平台扩散和重复对立的疲劳表达。沉默或退出不等于问题解决，也不等于真实信任恢复。',
  },
  {
    title: '媒体转述与社区二次解释',
    copy: '媒体、视频和社区讨论会二次组织事件叙事。报告应区分原始证据、转述内容和分析解释，避免把转述当作官方验证。',
  },
  {
    title: '极端表达簇 / trolling-like behavior',
    copy: '高强度表达只作为聚合讨论行为观察，不作为个人标签，不用于个体指认，也不能被当作全平台共识或事实裁定。',
  },
]

const RESPONSE_TEMPO_ITEMS = [
  ['事实边界澄清', '当讨论从单点争议扩散到青训制度和项目责任时，优先建立公开时间线、样本边界和可复核事实来源。'],
  ['证据包 / 时间线补充', '将公开材料、样本范围、平台来源和未验证状态分开说明，避免把受控样本误读成全网全量结论。'],
  ['第三方解释窗口', '当讨论进入制度、历史和专业训练背景时，可信第三方说明可能帮助中立用户理解复杂背景，但仍需标注来源。'],
  ['极端表达降放大', '高情绪和攻击性表达应作为风险边界处理，不宜直接放大、复述或作为回应主轴。'],
  ['疲劳期声誉修复', '讨论退潮后适合沉淀长期项目成果和透明材料，而不是反复点燃争议或制造新的对立焦点。'],
]

const RISK_OPPORTUNITY_ITEMS = [
  ['阵营化风险', '讨论可能从路线差异滑向身份化和阵营化表达。', '样本内可观察方向；仍需人工复核。'],
  ['极端表达放大风险', '少量高强度内容可能带动关注，但不代表主流态度。', '需要隔离处理，避免二次扩散。'],
  ['中立用户疲劳', '普通用户可能因持续争吵退出讨论。', '退出讨论不等于信任恢复。'],
  ['长期声誉记忆', '青训路线和中国足球信任议题可能沉淀为长期记忆。', '不是因果证明，也不是未来预测。'],
  ['媒体转述窗口', '媒体或创作者二次解释可帮助梳理背景。', '必须区分转述、事实和判断。'],
  ['第三方解释空间', '第三方材料可能降低误读和信息缺口。', '需要自愿、可复核、保护隐私。'],
  ['未成年人 / 家庭边界', '涉及青训和青少年时必须提高隐私保护标准。', '不展示敏感个人细节。'],
]

const SAMPLE_ACTIONS = [
  '建立公开时间线与事实边界，明确哪些内容来自受控样本、哪些仍需复核。',
  '区分青训模式争议、项目责任讨论与个人攻击内容，不把复杂议题压缩成个人对错。',
  '补充可复核的项目背景、公开证据和样本范围说明。',
  '使用第三方解释材料梳理复杂青训背景，但必须清楚标注来源和限制。',
  '避免直接放大极端攻击内容，不把高情绪表达作为报告主轴。',
  '保护未成年人、家庭和敏感个人信息，避免将未成年人推入争议中心。',
  '在疲劳期沉淀长期项目成果和复盘材料，而不是反复点燃争议。',
]

const BOUNDARY_TAGS = [
  'fixed sample report',
  'controlled candidate public sample',
  'frontend-only local demo',
  'not production data',
  'not full-web',
  'not full-platform',
  'not official verification',
  'not causal proof',
  'not a judgment of who is right or wrong',
]

function goToHash(hash) {
  window.location.hash = hash
}

function ReportMetric({ label, note, value }) {
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

export function BusinessReportDongluSunjihaiSample() {
  const timelineItems = DONGLU_SUNJIHAI_TIMELINE_PRESETS.map((phase) => ({
    color: phase.phase_id === 't2' || phase.phase_id === 't4' ? 'red' : phase.phase_id === 't3' ? 'blue' : 'green',
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
            {BOUNDARY_TAGS.map((tag) => (
              <Tag key={tag} color={tag.includes('fixed') ? 'gold' : tag.includes('frontend') ? 'cyan' : 'default'}>
                {tag}
              </Tag>
            ))}
          </Space>
          <Title level={1}>B端报告样例：中国足球青训路线争议</Title>
          <Paragraph>
            基于 Dong Lu / Sun Jihai controlled candidate public sample 的本地报告样例，用于展示未来 B
            端舆情证据分析、舆论生态复盘和回应节奏评估形态。
          </Paragraph>
          <Alert
            type="info"
            showIcon
            message="固定前端报告样例 / 不是动态报告生成器"
            description="本页用于展示专业报告的表达形态，不生成 PDF、Markdown 或 briefing deck，不调用后端，不运行采集任务，也不是正式客户报告。"
          />
          <Space wrap>
            <Button
              type="primary"
              icon={<Boxes size={17} />}
              onClick={() => goToHash('#/opinion-ecosystem?sample=donglu-sunjihai-youth-football')}
            >
              查看本地历史复盘沙盒
            </Button>
            <Button
              icon={<ArrowLeft size={17} />}
              onClick={() => goToHash('#/public-events/donglu-sunjihai-youth-football')}
            >
              查看公开事件样本
            </Button>
          </Space>
        </div>
        <Card className="panel-card business-report-hero-card">
          <Space direction="vertical" size={12}>
            <Tag color="gold">Report sample / professional value preview</Tag>
            <Title level={3}>边界先行</Title>
            <Paragraph>
              该报告样例只说明 Sentigraph 如何组织证据、区分讨论方向、解释圈层结构和呈现复盘结果。它不是事实裁定，不代表全网共识，不代表官方验证，也不判断谁对谁错。
            </Paragraph>
          </Space>
        </Card>
      </section>

      <Card className="panel-card business-report-summary-card" title="管理层摘要 / Executive Summary">
        <Row gutter={[16, 16]}>
          <Col span={12}>
            <Space direction="vertical" size={12}>
              <div className="business-report-summary-line">
                <Text strong>样本显示</Text>
                <Paragraph>
                  当前受控样本聚焦中国足球青训路线争议中的公开讨论分化，可观察到围绕路线、责任、信任、媒体转述和社区情绪的多方向表达。
                </Paragraph>
              </div>
              <div className="business-report-summary-line">
                <Text strong>讨论不只围绕个人冲突</Text>
                <Paragraph>
                  样本中的讨论延伸到青训模式、项目责任、足球信任、媒体叙事和社区疲劳。报告应避免将复杂议题简化为个人对错。
                </Paragraph>
              </div>
            </Space>
          </Col>
          <Col span={12}>
            <Space direction="vertical" size={12}>
              <div className="business-report-summary-line">
                <Text strong>报告价值</Text>
                <Paragraph>
                  当前样本适合展示 Sentigraph 如何组织证据、区分阵营表达、解释讨论圈层，并形成谨慎的 B 端报告样例。
                </Paragraph>
              </div>
              <div className="business-report-summary-line">
                <Text strong>不适合用途</Text>
                <Paragraph>
                  当前页面不适合作为完整舆情覆盖、官方验证、事实裁定或因果证明。所有结论都需要后续人工复核。
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
                <Tag color="gold">{SAMPLE_SUMMARY.validator_status}</Tag>
                <Tag color="orange">all review_needed</Tag>
                <Tag color="orange">all source_url_provided_unverified</Tag>
                <Tag>roots trust_label medium</Tag>
                <Tag>comments trust_label medium_low</Tag>
              </Space>
              <Paragraph>
                source_url_provided_unverified 表示来源 URL 已被保留为线索，但仍需要人工复核；它不等于官方验证。当前覆盖是样本覆盖，不是全网覆盖、全平台覆盖或全线程覆盖。
              </Paragraph>
            </Col>
            <Col span={10}>
              <Alert
                type="warning"
                showIcon
                message="覆盖不等于全量"
                description="581 evidence / 546 comments / 37 sources / 35 roots 只代表已整理的受控候选公开样本。Sentigraph 没有为本页运行实时平台采集或 collector job。"
              />
            </Col>
          </Row>
        </Card>
      </section>

      <section>
        <ReportSectionTitle kicker="Source map" title="来源与平台结构" />
        <Row gutter={[16, 16]}>
          {Object.entries(PLATFORM_DISTRIBUTION).map(([platform, count]) => (
            <Col span={8} key={platform}>
              <Card className="panel-card business-report-tempo-card">
                <Text strong>{platform}</Text>
                <Progress
                  percent={Math.round((Number(count) / SAMPLE_SUMMARY.evidence_items) * 100)}
                  strokeColor="#42f5d7"
                  trailColor="rgba(154,166,191,0.18)"
                />
                <Paragraph>{count} evidence items in the selected sample.</Paragraph>
              </Card>
            </Col>
          ))}
        </Row>
        <Alert
          className="business-report-section-alert"
          type="info"
          showIcon
          message="平台名称只描述样本来源类别"
          description="这些平台分布不表示 Sentigraph 运行了实时平台采集，也不表示覆盖了平台全量内容。样本来自已导出的 Evidence Export v1 package。"
        />
      </section>

      <section>
        <ReportSectionTitle kicker="Opinion Ecosystem" title="舆论生态摘要" />
        <Row gutter={[16, 16]}>
          {ECOSYSTEM_DIRECTIONS.map((item) => (
            <Col span={8} key={item.title}>
              <Card className="panel-card business-report-ecosystem-card">
                <Space direction="vertical" size={8}>
                  <Tag color="cyan">{item.title}</Tag>
                  <Paragraph>{item.copy}</Paragraph>
                </Space>
              </Card>
            </Col>
          ))}
        </Row>
        <Alert
          className="business-report-section-alert"
          type="info"
          showIcon
          message="样本内可观察讨论方向"
          description="这些方向不是全平台比例，不是个人标签，也不是官方事实裁定。PeopleCluster 表示匿名群体簇，InfluenceCore 表示内容 / 叙事 / 媒体 / 社区核心。"
        />
      </section>

      <section>
        <ReportSectionTitle kicker="Historical replay" title="T0-T6 历史复盘" />
        <Card className="panel-card business-report-timeline-card">
          <Alert
            type="info"
            showIcon
            message="本地 historical replay"
            description="T0-T6 是基于当前样本的本地历史复盘 preset，不是完整历史重建，也不是未来预测。"
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
          message="复盘价值，不是策略保证"
          description="本节展示报告如何阅读阶段节奏和风险窗口，不保证任何回应方案的实际结果，也不输出自动决策。"
        />
      </section>

      <section>
        <ReportSectionTitle kicker="Risk and opportunity" title="风险与机会" />
        <Row gutter={[16, 16]}>
          {RISK_OPPORTUNITY_ITEMS.map(([title, meaning, limitation]) => (
            <Col span={8} key={title}>
              <Card className="panel-card business-report-risk-card">
                <Space direction="vertical" size={10}>
                  <TriangleAlert size={18} />
                  <Text strong>{title}</Text>
                  <Paragraph>{meaning}</Paragraph>
                  <Tag>{limitation}</Tag>
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
              message="建议动作样例，不是自动决策"
              description="如未来使用受益者、家长、成年学员或第三方观察者材料，必须自愿、可复核、保护隐私，并避免将未成年人推入争议中心。"
            />
          </Card>
        </Col>
        <Col span={10}>
          <Card
            className="panel-card business-report-export-card"
            title={
              <Space>
                <Scale size={17} />
                <span>Response Strategy Lab（规划中）</span>
              </Space>
            }
          >
            <Paragraph>
              未来 Response Strategy Lab 可以比较透明事实澄清、证据支持的语境补充、第三方解释、低放大回应、疲劳期声誉修复等方案的可能影响。
            </Paragraph>
            <Paragraph>
              当前页面不进行真实策略推演，不预测未来，不输出自动决策，不是操控工具，不做个人定向，也不制造虚假共识。
            </Paragraph>
            <Space wrap>
              <Tag>planned only</Tag>
              <Tag>not active</Tag>
              <Tag>not real prediction</Tag>
              <Tag>no individual targeting</Tag>
            </Space>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card
            className="panel-card business-report-export-card"
            title={
              <Space>
                <FileText size={17} />
                <span>报告导出（规划中）</span>
              </Space>
            }
          >
            <Paragraph>
              未来可能支持 PDF、Markdown、briefing deck 和 evidence appendix。当前页面不生成文件，没有导出 runtime，也没有后端 job。
            </Paragraph>
            <Progress percent={20} strokeColor="#42f5d7" trailColor="rgba(154,166,191,0.18)" />
          </Card>
        </Col>
        <Col span={12}>
          <Card
            className="panel-card business-report-export-card"
            title={
              <Space>
                <ShieldCheck size={17} />
                <span>Human Review / Audit Status</span>
              </Space>
            }
          >
            <Space wrap>
              <Tag color="orange">581 review_needed</Tag>
              <Tag color="orange">581 source_url_provided_unverified</Tag>
              <Tag>no raw author identifiers</Tag>
              <Tag>minors / family sensitive details not exposed</Tag>
            </Space>
            <Paragraph>
              面向真实客户使用前，需要完成人工复核、来源可信度复核、敏感信息边界确认和报告措辞审查。
            </Paragraph>
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
                先阅读本页报告结构，再打开 Sandbox V2 查看 EchoBox、PeopleCluster、InfluenceCore 和 T0-T6 历史复盘如何被可视化。
              </Paragraph>
            </Space>
          </Col>
          <Col span={8} className="public-event-action-col">
            <Space direction="vertical" size={10}>
              <Button
                type="primary"
                size="large"
                icon={<BarChart3 size={17} />}
                onClick={() => goToHash('#/opinion-ecosystem?sample=donglu-sunjihai-youth-football')}
              >
                打开本地历史复盘沙盒
              </Button>
              <Button
                size="large"
                icon={<ArrowLeft size={17} />}
                onClick={() => goToHash('#/public-events/donglu-sunjihai-youth-football')}
              >
                返回公开事件样本
              </Button>
            </Space>
          </Col>
        </Row>
      </Card>

      <Alert
        className="public-event-boundary-alert"
        type="info"
        showIcon
        icon={<FlaskConical size={18} />}
        message="B端报告样例边界"
        description="本页是 frontend-only local demo。Dong Lu / Sun Jihai 样本是 controlled candidate public sample，不是 full-web coverage、不是 full-platform coverage、不是 official verification、不是 causal proof。没有真实 API、没有真实 LLM、没有实时采集、没有报告导出、没有真实平台动作，也不展示原始作者身份字段。"
      />
    </div>
  )
}
