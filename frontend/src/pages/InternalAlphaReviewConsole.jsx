import { Alert, Card, Col, Descriptions, List, Row, Space, Tag, Typography } from 'antd'
import { Eye, Lock, ShieldCheck, TriangleAlert } from 'lucide-react'

import { INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE } from '../data/internalAlphaReviewConsoleStaticFixture.js'

const { Paragraph, Text, Title } = Typography

function BooleanTag({ label, value }) {
  return (
    <Tag color={value ? 'cyan' : 'default'}>
      {label} = {String(value)}
    </Tag>
  )
}

function SummaryCard({ icon, title, children }) {
  return (
    <Card className="panel-card internal-alpha-review-card">
      <Space direction="vertical" size={12} className="full-width">
        <Space>
          {icon}
          <Title level={4}>{title}</Title>
        </Space>
        {children}
      </Space>
    </Card>
  )
}

export function InternalAlphaReviewConsole() {
  const fixture = INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE

  return (
    <div className="page-stack internal-alpha-review-shell-page">
      <section className="internal-alpha-review-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">internal alpha</Tag>
            <Tag color="default">static shell only</Tag>
            <Tag color="default">not operator runtime</Tag>
          </Space>
          <Title level={1}>Internal Alpha Review Console static preview</Title>
          <Paragraph>
            this shell is not operator runtime. It is a local static preview for checking review-console layout,
            boundary copy, and selected sample / no-write / no-production boundary before any backend consumption is
            considered. It is a static internal frontend shell.
          </Paragraph>
          <Alert
            className="internal-alpha-review-boundary-alert"
            showIcon
            type="info"
            message="source_chain_boundary = evidence_layer_write_candidate_boundary"
            description="route_backend_connection = static_shell_only_not_connected; route/backend connection status: not connected / static shell only."
          />
        </div>
        <Card className="panel-card internal-alpha-review-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Shell status</Text>
            <Title level={2}>static</Title>
            <Text>human_review_required = true</Text>
            <Text>no_automatic_trust_upgrade = true</Text>
            <BooleanTag label="human_review_required" value={fixture.human_review_required} />
            <BooleanTag label="no_automatic_trust_upgrade" value={fixture.no_automatic_trust_upgrade} />
          </Space>
        </Card>
      </section>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<ShieldCheck size={18} />} title="Boundary flags">
            <Space wrap>
              <Tag color="cyan">no actual write</Tag>
              <Tag color="cyan">no production object</Tag>
              <Tag color="cyan">no Review Queue runtime</Tag>
              <Tag color="cyan">no Source 11 / FinalSummaryReport runtime</Tag>
            </Space>
            <Paragraph>{fixture.source_count_summary.note}</Paragraph>
          </SummaryCard>
        </Col>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<TriangleAlert size={18} />} title="Counts">
            <Descriptions column={1} size="small">
              <Descriptions.Item label="warning_count">{fixture.warning_count}</Descriptions.Item>
              <Descriptions.Item label="blocker_count">{fixture.blocker_count}</Descriptions.Item>
              <Descriptions.Item label="candidate_count">
                {fixture.evidence_count_summary.candidate_count}
              </Descriptions.Item>
            </Descriptions>
          </SummaryCard>
        </Col>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<Lock size={18} />} title="Backend connection">
            <Tag color="default">{fixture.route_backend_connection}</Tag>
            <Paragraph>This page does not call a route, platform service, collector, provider, or model.</Paragraph>
          </SummaryCard>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <SummaryCard icon={<Eye size={18} />} title="Allowed actions labels only">
            <List
              size="small"
              dataSource={fixture.allowed_actions}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
          </SummaryCard>
        </Col>
        <Col xs={24} lg={12}>
          <SummaryCard icon={<Lock size={18} />} title="Blocked actions labels only">
            <List
              size="small"
              dataSource={fixture.blocked_actions}
              renderItem={(item) => (
                <List.Item>
                  <Text>{item}</Text>
                </List.Item>
              )}
            />
          </SummaryCard>
        </Col>
      </Row>

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Coverage and validation summaries</Title>
          <Space wrap>
            {fixture.coverage_note_summary.map((item) => (
              <Tag key={item} color="default">
                {item}
              </Tag>
            ))}
          </Space>
          <List
            size="small"
            dataSource={fixture.validation_summary}
            renderItem={(item) => (
              <List.Item>
                <Text>{item}</Text>
              </List.Item>
            )}
          />
        </Space>
      </Card>
    </div>
  )
}
