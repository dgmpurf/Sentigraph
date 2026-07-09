import { useEffect, useState } from 'react'
import { Alert, Card, Col, Descriptions, List, Row, Space, Tag, Typography } from 'antd'
import { Eye, Lock, ShieldCheck, TriangleAlert } from 'lucide-react'

import {
  getInternalAlphaReviewConsoleProjection,
  INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS,
} from '../api/sentigraphApi.js'
import { INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE } from '../data/internalAlphaReviewConsoleStaticFixture.js'

const { Paragraph, Text, Title } = Typography
const SAFE_REVIEW_CONSOLE_PROJECTION_ID = INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]

const STATIC_FALLBACK_ROUTE_STATE = {
  status: 'checking',
  statusLabel: 'checking disabled backend route',
  routeBackendConnection: 'static_fallback_active_not_connected',
  tagColor: 'default',
  description: 'static fallback active; backend route disabled / not connected state is handled safely.',
  detail: 'route_disabled and unsupported_projection responses remain safe not-connected state.',
}

function describeRouteState(payload) {
  if (payload?.error === 'route_disabled') {
    return {
      status: 'disabled',
      statusLabel: 'backend route disabled',
      routeBackendConnection: 'backend_route_disabled_static_fallback',
      tagColor: 'default',
      description: 'backend route disabled / not connected / static fallback active.',
      detail: 'route_disabled response keeps the page in safe not-connected state.',
    }
  }

  if (payload?.error === 'unsupported_projection') {
    return {
      status: 'unsupported',
      statusLabel: 'unsupported projection',
      routeBackendConnection: 'unsupported_projection_static_fallback',
      tagColor: 'default',
      description: 'unsupported_projection response keeps static fallback active.',
      detail: 'No alternate projection is loaded automatically.',
    }
  }

  if (payload?.route_mode === 'disabled_by_default_internal_safe_projection_route_skeleton') {
    return {
      status: 'local_synthetic',
      statusLabel: 'local/synthetic enabled mode',
      routeBackendConnection: 'local_synthetic_enabled_response',
      tagColor: 'cyan',
      description: 'existing disabled-by-default internal GET route returned a safe local/synthetic projection.',
      detail: 'Static fallback remains available; this is not operator runtime.',
    }
  }

  return {
    status: 'unavailable',
    statusLabel: 'backend route unavailable',
    routeBackendConnection: 'backend_route_unavailable_static_fallback',
    tagColor: 'default',
    description: 'backend route unavailable / not connected / static fallback active.',
    detail: 'Unexpected response shape is treated as safe not-connected state.',
  }
}

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
  const [routeState, setRouteState] = useState(STATIC_FALLBACK_ROUTE_STATE)

  useEffect(() => {
    let isMounted = true

    getInternalAlphaReviewConsoleProjection(SAFE_REVIEW_CONSOLE_PROJECTION_ID)
      .then((payload) => {
        if (!isMounted) return
        setRouteState(describeRouteState(payload))
      })
      .catch(() => {
        if (!isMounted) return
        setRouteState({
          status: 'unavailable',
          statusLabel: 'backend route unavailable',
          routeBackendConnection: 'backend_route_unavailable_static_fallback',
          tagColor: 'default',
          description: 'backend route unavailable / not connected / static fallback active.',
          detail: 'Network or local backend absence keeps this shell in safe not-connected state.',
        })
      })

    return () => {
      isMounted = false
    }
  }, [])

  return (
    <div className="page-stack internal-alpha-review-shell-page">
      <section className="internal-alpha-review-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">internal alpha</Tag>
            <Tag color="default">read-only route smoke</Tag>
            <Tag color="default">static fallback preserved</Tag>
            <Tag color="default">not operator runtime</Tag>
          </Space>
          <Title level={1}>Internal Alpha Review Console static preview</Title>
          <Paragraph>
            this shell is not operator runtime. It is a local internal preview for checking review-console layout,
            boundary copy, selected sample / no-write / no-production boundary, and safe disabled-route handling.
            static internal frontend shell fallback remains active when the backend route is disabled or not connected.
          </Paragraph>
          <Alert
            className="internal-alpha-review-boundary-alert"
            showIcon
            type="info"
            message="source_chain_boundary = evidence_layer_write_candidate_boundary"
            description={`route_backend_connection = ${routeState.routeBackendConnection}; ${routeState.description}`}
          />
        </div>
        <Card className="panel-card internal-alpha-review-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Shell status</Text>
            <Title level={2}>{routeState.status}</Title>
            <Text>{routeState.statusLabel}</Text>
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
            <Tag color={routeState.tagColor}>{routeState.routeBackendConnection}</Tag>
            <Paragraph>{routeState.detail}</Paragraph>
            <Paragraph>
              Safe projection id: {SAFE_REVIEW_CONSOLE_PROJECTION_ID}. The page does not call a platform service,
              collector, provider, model, or write path.
            </Paragraph>
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
