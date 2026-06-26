import { Alert, Card, Col, List, Row, Space, Tag, Tooltip, Typography } from 'antd'
import { AlertTriangle, BadgeCheck, BookOpen, Eye, GitCompare, ShieldCheck } from 'lucide-react'

import {
  OPINION_ECOSYSTEM_DEFERRED_NOTICES,
  OPINION_ECOSYSTEM_EXPLANATION_STATUS,
  OPINION_ECOSYSTEM_MODULE_EXPLANATIONS,
  OPINION_ECOSYSTEM_UI_COPY_GUARDRAILS,
} from '../../data/opinionEcosystemCalculatorOutputFixture.js'

const { Paragraph, Text, Title } = Typography

const TAG_COLOR_BY_STATUS = {
  mock_default: 'cyan',
  uncalibrated: 'gold',
  not_started: 'default',
  selected_sample_or_local_fixture_only: 'purple',
}

function StatusTag({ label, value }) {
  return (
    <Tooltip title={label}>
      <Tag color={TAG_COLOR_BY_STATUS[value] || 'default'}>{value}</Tag>
    </Tooltip>
  )
}

function CompactTagList({ items, color = 'default', limit = 5 }) {
  const visible = items.slice(0, limit)
  const remaining = items.length - visible.length
  return (
    <Space size={[6, 6]} wrap>
      {visible.map((item) => (
        <Tag key={item} color={color}>
          {item}
        </Tag>
      ))}
      {remaining > 0 && <Tag color="default">+{remaining} more</Tag>}
    </Space>
  )
}

function ScoreSummary({ scores }) {
  return (
    <List
      size="small"
      className="ecosystem-model-score-list"
      dataSource={scores}
      renderItem={(item) => (
        <List.Item>
          <div className="ecosystem-model-score-row">
            <Text strong>{item.label}</Text>
            <Text type="secondary">{item.value}</Text>
          </div>
        </List.Item>
      )}
    />
  )
}

function ModuleExplanationCard({ module }) {
  const isResponseStrategy = module.module_name === 'ResponseStrategyComparisonV01'
  return (
    <Card
      className={`panel-card ecosystem-model-module-card ${isResponseStrategy ? 'response-strategy' : ''}`}
      title={
        <Space>
          {isResponseStrategy ? <GitCompare size={17} /> : <BookOpen size={17} />}
          <span>{module.title}</span>
        </Space>
      }
      extra={<Tag color={isResponseStrategy ? 'gold' : 'cyan'}>{module.model_status}</Tag>}
    >
      <Space direction="vertical" size={12}>
        <div>
          <Text strong>{module.plain_title}</Text>
          <Paragraph>{module.means}</Paragraph>
        </div>
        <Alert
          type="warning"
          showIcon
          message="这不代表什么"
          description={module.does_not_mean}
          className="ecosystem-model-inline-alert"
        />
        {isResponseStrategy && (
          <Alert
            type="info"
            showIcon
            message="透明回应候选比较 / human-review-only"
            description="不是回应文案生成，不是 Strategy Lab runtime，不自动执行。Blockers come before score; high score cannot override privacy, evidence, overclaim, or implementation blockers."
            className="ecosystem-model-inline-alert"
          />
        )}
        <ScoreSummary scores={module.scores_summary} />
        <div className="ecosystem-model-card-section">
          <Text type="secondary">Warnings</Text>
          <CompactTagList items={module.warnings_summary} color="gold" />
        </div>
        {module.blockers_summary.length > 0 && (
          <div className="ecosystem-model-card-section">
            <Text type="secondary">Blockers before score</Text>
            <CompactTagList items={module.blockers_summary} color="red" />
          </div>
        )}
        <div className="ecosystem-model-card-section">
          <Text type="secondary">Boundary flags</Text>
          <CompactTagList items={module.boundary_flags} color="default" />
        </div>
        <div className="ecosystem-model-card-section">
          <Text type="secondary">Recommended audience</Text>
          <CompactTagList items={module.audience} color="blue" />
        </div>
      </Space>
    </Card>
  )
}

function DeferredNotice() {
  return (
    <Card
      className="panel-card ecosystem-model-deferred-card"
      title={
        <Space>
          <AlertTriangle size={17} />
          <span>未计算 / deferred</span>
        </Space>
      }
    >
      <Paragraph>
        这些模块或集成在 8Q-2 中没有实现。本页只解释安全的本地快照，不把 deferred 项伪装成可用能力。
      </Paragraph>
      <CompactTagList items={OPINION_ECOSYSTEM_DEFERRED_NOTICES} color="default" limit={10} />
    </Card>
  )
}

function CopyGuardrails() {
  return (
    <Card
      className="panel-card ecosystem-model-copy-card"
      title={
        <Space>
          <Eye size={17} />
          <span>文案护栏</span>
        </Space>
      }
    >
      <Row gutter={[12, 12]}>
        <Col xs={24} md={12}>
          <Text strong>适合展示</Text>
          <CompactTagList items={OPINION_ECOSYSTEM_UI_COPY_GUARDRAILS.use} color="green" limit={8} />
        </Col>
        <Col xs={24} md={12}>
          <Text strong>避免作为能力宣称</Text>
          <CompactTagList items={OPINION_ECOSYSTEM_UI_COPY_GUARDRAILS.avoid_as_capability} color="red" limit={8} />
        </Col>
      </Row>
    </Card>
  )
}

export function OpinionEcosystemModelExplanation() {
  const status = OPINION_ECOSYSTEM_EXPLANATION_STATUS

  return (
    <section className="ecosystem-model-explanation" aria-label="Local model explanation">
      <Card
        className="panel-card ecosystem-model-boundary-card"
        title={
          <Space>
            <ShieldCheck size={18} />
            <span>模型解释 / 本地分数说明</span>
          </Space>
        }
      >
        <Row gutter={[16, 16]} align="middle">
          <Col xs={24} lg={15}>
            <Space direction="vertical" size={10}>
              <Space wrap>
                <Tag color="cyan">本地解释快照</Tag>
                <StatusTag label="coefficient source" value={status.coefficient_source} />
                <StatusTag label="calibration status" value={status.calibration_status} />
                <StatusTag label="empirical validation" value={status.empirical_validation} />
                <StatusTag label="sample scope" value={status.sample_scope} />
              </Space>
              <Title level={4}>Selected-sample score explanation, not production runtime</Title>
              <Paragraph>当前为本地解释快照，不是生产分数；本页只展示安全解释，不调用 calculator API。</Paragraph>
              <Paragraph>
                分数只用于理解 selected sample 的结构，不代表全网、全平台、完整讨论串、官方验证、因果证明或预测。
                ResponseStrategyComparison 只做人工复核前的候选比较，不生成回应文案，也不自动执行。
              </Paragraph>
            </Space>
          </Col>
          <Col xs={24} lg={9}>
            <Alert
              type="success"
              showIcon
              icon={<BadgeCheck size={18} />}
              message="Human review required"
              description="Evidence is not truth. Scores are mock-default, uncalibrated, selected-sample-only explanations with no automatic action."
              className="ecosystem-model-human-review-alert"
            />
          </Col>
        </Row>
      </Card>

      <Row gutter={[16, 16]}>
        {OPINION_ECOSYSTEM_MODULE_EXPLANATIONS.map((module) => (
          <Col xs={24} xl={module.module_name === 'ResponseStrategyComparisonV01' ? 24 : 12} key={module.module_name}>
            <ModuleExplanationCard module={module} />
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={14}>
          <DeferredNotice />
        </Col>
        <Col xs={24} lg={10}>
          <CopyGuardrails />
        </Col>
      </Row>
    </section>
  )
}
