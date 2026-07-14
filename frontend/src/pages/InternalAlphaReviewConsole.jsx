import { useEffect, useState } from 'react'
import { Alert, Card, Col, Descriptions, List, Row, Space, Tag, Typography } from 'antd'
import { Eye, Lock, ShieldCheck, TriangleAlert } from 'lucide-react'

import {
  getInternalAlphaReviewConsoleProjection,
  INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID,
  INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS,
} from '../api/sentigraphApi.js'
import { INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE } from '../data/internalAlphaReviewConsoleStaticFixture.js'

const { Paragraph, Text, Title } = Typography
const GOVERNED_REVIEW_CONSOLE_PROJECTION_ID = INTERNAL_ALPHA_GOVERNED_RECORD_REVIEW_PROJECTION_ID
const SAFE_REVIEW_CONSOLE_PROJECTION_ID = GOVERNED_REVIEW_CONSOLE_PROJECTION_ID
const REVIEW_CONSOLE_PROJECTION_ALLOWLIST = INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS
const LEGACY_SYNTHETIC_SELECTION_REFERENCE = 'INTERNAL_ALPHA_REVIEW_CONSOLE_SAFE_PROJECTION_IDS[0]'
const STATIC_SOURCE_CHAIN_BOUNDARY_LABEL =
  'source_chain_boundary = evidence_layer_write_candidate_boundary'

const SAFE_METADATA_FIELDS = Object.freeze([
  'persisted_record_id',
  'attempt_reservation_id',
  'candidate_identity_digest',
  'input_safe_hash',
  'gate_contract_safe_hash',
  'activation_decision_safe_hash',
  'record_snapshot_digest',
  'reservation_snapshot_digest',
])

const GOVERNED_STATUS_DETAILS = Object.freeze({
  governed_record_review_ready: {
    statusLabel: 'governed record ready for human review',
    tagColor: 'cyan',
    description: 'The exact governed nonproduction record is available as bounded read-only metadata.',
  },
  governed_record_absent: {
    statusLabel: 'governed record absent',
    tagColor: 'default',
    description: 'No expected governed record or reservation is present.',
  },
  governed_record_missing_after_consumed_attempt: {
    statusLabel: 'record missing after consumed attempt',
    tagColor: 'orange',
    description: 'The expected reservation is present while the governed record is absent.',
  },
  governed_record_inconsistent: {
    statusLabel: 'governed record state inconsistent',
    tagColor: 'orange',
    description: 'The bounded reader could not safely classify the governed record state.',
  },
  governed_record_read_blocked_sidecar_present: {
    statusLabel: 'read blocked because a sidecar is present',
    tagColor: 'orange',
    description: 'Read-only review is blocked while a prohibited sidecar state is present.',
  },
  governed_record_target_unavailable: {
    statusLabel: 'governed target unavailable',
    tagColor: 'default',
    description: 'Target identity or metadata could not be safely verified.',
  },
  governed_record_read_only_audit_failed: {
    statusLabel: 'bounded read-only audit failed',
    tagColor: 'default',
    description: 'The bounded reader failed closed without exposing target details.',
  },
})

const STATIC_FALLBACK_ROUTE_STATE = {
  status: 'checking',
  statusLabel: 'checking disabled backend route',
  routeBackendConnection: 'static_fallback_active_not_connected',
  tagColor: 'default',
  description: 'static fallback active; backend route disabled / not connected state is handled safely.',
  detail: 'route_disabled and unsupported_projection responses remain safe not-connected state.',
  projection: null,
}

function staticRouteState({
  status,
  statusLabel,
  routeBackendConnection,
  description,
  detail,
}) {
  return {
    status,
    statusLabel,
    routeBackendConnection,
    tagColor: 'default',
    description,
    detail,
    projection: null,
  }
}

function describeRouteState(payload) {
  if (payload?.error === 'route_disabled') {
    return staticRouteState({
      status: 'disabled',
      statusLabel: 'backend route disabled',
      routeBackendConnection: 'backend_route_disabled_static_fallback',
      description: 'backend route disabled / not connected / static fallback active.',
      detail: 'route_disabled response keeps the page in safe not-connected state.',
    })
  }

  if (payload?.error === 'governed_record_projection_disabled') {
    return staticRouteState({
      status: 'governed_disabled',
      statusLabel: 'governed record projection disabled',
      routeBackendConnection: 'governed_record_projection_disabled_static_fallback',
      description: 'governed record projection disabled; static fallback remains active.',
      detail: 'The second read-only gate is disabled and no governed target reader was called.',
    })
  }

  if (payload?.error === 'unsupported_projection') {
    return staticRouteState({
      status: 'unsupported',
      statusLabel: 'unsupported projection',
      routeBackendConnection: 'unsupported_projection_static_fallback',
      description: 'unsupported_projection response keeps static fallback active.',
      detail: 'No alternate projection is loaded automatically.',
    })
  }

  const projectionStatus = payload?.projection_status
  const statusDetail = GOVERNED_STATUS_DETAILS[projectionStatus]
  const projection = payload?.projection
  if (
    payload?.projection_id === GOVERNED_REVIEW_CONSOLE_PROJECTION_ID &&
    projection &&
    statusDetail
  ) {
    return {
      status: projectionStatus,
      statusLabel: statusDetail.statusLabel,
      routeBackendConnection: 'governed_record_read_only_projection',
      tagColor: statusDetail.tagColor,
      description: statusDetail.description,
      detail: 'One internal GET returned the bounded governed-record projection; this is not operator runtime.',
      projection,
    }
  }

  return staticRouteState({
    status: 'unavailable',
    statusLabel: 'backend route unavailable',
    routeBackendConnection: 'backend_route_unavailable_static_fallback',
    description: 'backend route unavailable / not connected / static fallback active.',
    detail: 'Unexpected response shape is treated as safe not-connected state.',
  })
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

function displaySafeValue(value) {
  return typeof value === 'string' && value ? value : 'not available in this state'
}

export function InternalAlphaReviewConsole() {
  const fixture = INTERNAL_ALPHA_REVIEW_CONSOLE_STATIC_FIXTURE
  const [routeState, setRouteState] = useState(STATIC_FALLBACK_ROUTE_STATE)

  useEffect(() => {
    let isMounted = true

    getInternalAlphaReviewConsoleProjection(GOVERNED_REVIEW_CONSOLE_PROJECTION_ID)
      .then((payload) => {
        if (!isMounted) return
        setRouteState(describeRouteState(payload))
      })
      .catch(() => {
        if (!isMounted) return
        setRouteState(
          staticRouteState({
            status: 'unavailable',
            statusLabel: 'backend route unavailable',
            routeBackendConnection: 'backend_route_unavailable_static_fallback',
            description: 'backend route unavailable / not connected / static fallback active.',
            detail: 'Network or local backend absence keeps this shell in safe not-connected state.',
          }),
        )
      })

    return () => {
      isMounted = false
    }
  }, [])

  const projection = routeState.projection
  const allowedActions = projection?.allowed_actions ?? fixture.allowed_actions
  const blockedActions = projection?.blocked_actions ?? fixture.blocked_actions
  const sourceBoundary = projection?.source_chain_boundary ?? fixture.source_chain_boundary
  const humanReviewRequired = projection?.human_review_required ?? fixture.human_review_required
  const noAutomaticTrustUpgrade =
    projection?.no_automatic_trust_upgrade ?? fixture.no_automatic_trust_upgrade

  return (
    <div className="page-stack internal-alpha-review-shell-page">
      <section className="internal-alpha-review-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">internal alpha</Tag>
            <Tag color="cyan">governed nonproduction only</Tag>
            <Tag color="default">read-only route smoke</Tag>
            <Tag color="default">static fallback preserved</Tag>
            <Tag color="default">not operator runtime</Tag>
          </Space>
          <Title level={1}>Internal Alpha Review Console static preview</Title>
          <Paragraph>
            This static internal frontend shell presents bounded governance metadata for pending human review. It
            preserves the selected sample / no-write / no-production boundary and the safe static fallback when
            either backend gate is disabled or the backend is unavailable; this shell is not operator runtime.
          </Paragraph>
          <Alert
            className="internal-alpha-review-boundary-alert"
            showIcon
            type="info"
            message={
              projection
                ? 'source_chain_boundary = ' + sourceBoundary
                : STATIC_SOURCE_CHAIN_BOUNDARY_LABEL
            }
            description={
              'route_backend_connection = ' +
              routeState.routeBackendConnection +
              '; ' +
              routeState.description
            }
          />
        </div>
        <Card className="panel-card internal-alpha-review-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Shell status</Text>
            <Title level={2}>{routeState.status}</Title>
            <Text>{routeState.statusLabel}</Text>
            <Text>pending human review</Text>
            <Text>no automatic trust upgrade</Text>
            <Text>human_review_required = true</Text>
            <Text>no_automatic_trust_upgrade = true</Text>
            <Text>no Review Queue or operator runtime</Text>
            <Text>no production or public readiness</Text>
            <BooleanTag label="human_review_required" value={humanReviewRequired} />
            <BooleanTag label="no_automatic_trust_upgrade" value={noAutomaticTrustUpgrade} />
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
          <SummaryCard icon={<TriangleAlert size={18} />} title="Governed counts">
            <Descriptions column={1} size="small">
              <Descriptions.Item label="record_count_class">
                {projection?.record_count_class ?? 'not available in static fallback'}
              </Descriptions.Item>
              <Descriptions.Item label="reservation_count_class">
                {projection?.reservation_count_class ?? 'not available in static fallback'}
              </Descriptions.Item>
              <Descriptions.Item label="blocker_count">
                {projection?.blockers?.length ?? fixture.blocker_count}
              </Descriptions.Item>
            </Descriptions>
          </SummaryCard>
        </Col>
        <Col xs={24} lg={8}>
          <SummaryCard icon={<Lock size={18} />} title="Backend connection">
            <Tag color={routeState.tagColor}>{routeState.routeBackendConnection}</Tag>
            <Paragraph>{routeState.detail}</Paragraph>
            <Paragraph>
              Safe projection id: {SAFE_REVIEW_CONSOLE_PROJECTION_ID}. Allowlisted projection count:{' '}
              {REVIEW_CONSOLE_PROJECTION_ALLOWLIST.length}. The page calls no platform service, collector,
              provider, model, or write path. Legacy synthetic selection reference:{' '}
              {LEGACY_SYNTHETIC_SELECTION_REFERENCE}.
            </Paragraph>
          </SummaryCard>
        </Col>
      </Row>

      <Card className="panel-card internal-alpha-review-card">
        <Space direction="vertical" size={12} className="full-width">
          <Title level={4}>Approved opaque metadata only</Title>
          <Paragraph>
            Only the eight P1-approved opaque identifiers, hashes, and digests may appear here. Non-ready and
            fallback states display no values.
          </Paragraph>
          <Descriptions column={{ xs: 1, lg: 2 }} size="small">
            {SAFE_METADATA_FIELDS.map((field) => (
              <Descriptions.Item key={field} label={field}>
                <Text code>{displaySafeValue(projection?.[field])}</Text>
              </Descriptions.Item>
            ))}
          </Descriptions>
        </Space>
      </Card>

      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <SummaryCard icon={<Eye size={18} />} title="Allowed actions labels only">
            <List
              size="small"
              dataSource={allowedActions}
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
              dataSource={blockedActions}
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
