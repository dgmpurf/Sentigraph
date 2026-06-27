import { Alert, Button, Card, Col, Descriptions, List, Row, Space, Tag, Typography } from 'antd'
import { DatabaseZap, ShieldCheck, Sparkles } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import { createOpinionEcosystemGeneratedRunLocalFixture } from '../../api/sentigraphApi.js'

const { Paragraph, Text } = Typography

const MODULE_KEYS = [
  'ContentAggregate',
  'InfluenceCore',
  'EchoBox',
  'PeopleCluster',
  'ResponseStrategyComparisonV01',
]

const BOUNDARY_LABELS = {
  selected_sample_only: 'selected sample only',
  not_full_web: 'not full-web',
  not_full_platform: 'not full-platform',
  not_full_thread: 'not full-thread',
  not_official_verification: 'not official verification',
  not_causal_proof: 'not causal proof',
  not_prediction: 'not prediction',
  not_production_score: 'not production score',
  human_review_required: 'human review required',
  no_auto_execute: 'no auto execution',
  no_generated_public_response: 'no generated public response',
}

const FORBIDDEN_RENDER_KEYS = new Set([
  'response_text',
  'generated_public_message',
  'target_user_list',
  'persuasion_score',
  'truth_score',
  'official_verified',
  'prediction_probability',
  'psychological_profile',
  'personality_diagnosis',
  'publish_now',
  'send_now',
  'post_now',
  'execute_now',
  'auto_execute',
])

function formatSafeValue(value) {
  if (value === null || value === undefined || value === '') return 'not provided'
  if (typeof value === 'boolean') return value ? 'true' : 'false'
  if (typeof value === 'number' || typeof value === 'string') return String(value)
  try {
    return JSON.stringify(
      value,
      (key, item) => (FORBIDDEN_RENDER_KEYS.has(String(key)) ? '[blocked safe key]' : item),
      2,
    )
  } catch {
    return 'unrenderable safe object'
  }
}

function isStructuredSafeValue(value) {
  return Boolean(value) && typeof value === 'object'
}

function compactRows(value, limit = 8) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) return []
  return Object.entries(value)
    .filter(([key]) => !FORBIDDEN_RENDER_KEYS.has(String(key)))
    .slice(0, limit)
    .map(([key, item]) => ({
      key: String(key),
      value: formatSafeValue(item),
      structured: isStructuredSafeValue(item),
    }))
}

function RenderSafeList({ title, items, color = 'default' }) {
  if (!items.length) return null
  return (
    <div className="ecosystem-generated-run-section">
      <Text type="secondary">{title}</Text>
      <List
        size="small"
        dataSource={items}
        renderItem={(item, index) => (
          <List.Item>
            <Tag color={color}>{index + 1}</Tag>
            <Text>{formatSafeValue(item)}</Text>
          </List.Item>
        )}
      />
    </div>
  )
}

function ModuleOutputCard({ moduleName, outputs }) {
  const rows = Array.isArray(outputs) ? outputs : []
  const isBlockedModule = rows.some((item) => item?.strategy_status === 'forbidden')

  return (
    <Card
      className={`panel-card ecosystem-generated-run-module-card ${moduleName === 'ResponseStrategyComparisonV01' ? 'response-strategy' : ''}`}
      title={
        <Space>
          <Sparkles size={16} />
          <span>{moduleName}</span>
        </Space>
      }
      extra={<Tag color={isBlockedModule ? 'red' : rows.length ? 'cyan' : 'default'}>{rows.length ? 'loaded' : 'empty'}</Tag>}
    >
      {rows.length === 0 ? (
        <Text type="secondary">No module output returned for this local fixture run.</Text>
      ) : (
        <List
          size="small"
          dataSource={rows.slice(0, 4)}
          renderItem={(item, index) => (
            <List.Item>
              <div className="ecosystem-generated-run-module-output">
                <Space wrap>
                  <Tag color="default">item {index + 1}</Tag>
                  {item?.schema && <Tag>{item.schema}</Tag>}
                  {item?.status && <Tag color={item.status === 'blocked' ? 'red' : 'green'}>{item.status}</Tag>}
                  {item?.strategy_status && (
                    <Tag color={item.strategy_status === 'forbidden' ? 'red' : 'gold'}>{item.strategy_status}</Tag>
                  )}
                </Space>
                <List
                  size="small"
                  dataSource={compactRows(item)}
                  renderItem={(row) => (
                    <List.Item>
                      <div className="ecosystem-generated-run-field-row">
                        <Text strong>{row.key}</Text>
                        {row.structured ? (
                          <pre className="ecosystem-generated-run-safe-json">{row.value}</pre>
                        ) : (
                          <Text type="secondary">{row.value}</Text>
                        )}
                      </div>
                    </List.Item>
                  )}
                />
              </div>
            </List.Item>
          )}
        />
      )}
    </Card>
  )
}

function boundaryEntries(boundaryFlags = {}) {
  return Object.entries(BOUNDARY_LABELS).map(([key, label]) => ({
    key,
    label,
    enabled: boundaryFlags[key] === true,
  }))
}

export function OpinionEcosystemGeneratedRunPanel({ sampleKey, sampleLabel }) {
  const [status, setStatus] = useState('idle')
  const [generatedRun, setGeneratedRun] = useState(null)
  const [safeError, setSafeError] = useState('')

  useEffect(() => {
    setStatus('idle')
    setGeneratedRun(null)
    setSafeError('')
  }, [sampleKey])

  const canRequest = sampleKey === 'helldivers_psn' || sampleKey === 'donglu_sunjihai_youth_football'
  const isBlockedState = generatedRun && ['blocked', 'manual_review_required', 'not_ready'].includes(generatedRun.run_status)
  const boundaries = useMemo(() => boundaryEntries(generatedRun?.boundary_flags || {}), [generatedRun])

  const handleRequestGeneratedRun = async () => {
    if (!canRequest) return
    setStatus('loading')
    setSafeError('')
    try {
      const run = await createOpinionEcosystemGeneratedRunLocalFixture({ sample_key: sampleKey })
      setGeneratedRun(run)
      setStatus(run.run_status === 'ready' ? 'success' : 'blocked')
    } catch {
      setGeneratedRun(null)
      setStatus('error')
      setSafeError('Local backend generated-run route is unavailable or rejected this safe fixture request.')
    }
  }

  return (
    <Card
      className="panel-card ecosystem-generated-run-card"
      title={
        <Space>
          <DatabaseZap size={18} />
          <span>Backend local generated run / 后端本地生成运行</span>
        </Space>
      }
      extra={<Tag color="purple">explicit click only</Tag>}
    >
      <Space direction="vertical" size={14}>
        <Alert
          type="info"
          showIcon
          message="Local fixture generated run only"
          description="This section calls the backend local fixture route only after an explicit click. It is selected-sample-only, not full-web, not full-platform, not full-thread, not official verification, not causal proof, not prediction, not production score, human-review-required, no generated public response, and no auto execution."
        />

        <Row gutter={[14, 14]} align="middle">
          <Col xs={24} lg={16}>
            <Space wrap>
              <Tag color="cyan">{sampleLabel}</Tag>
              <Tag color={canRequest ? 'green' : 'gold'}>{canRequest ? sampleKey : 'unsupported in 8S-6'}</Tag>
              <Tag>backend local fixture run</Tag>
              <Tag>static fallback remains visible</Tag>
            </Space>
            <Paragraph className="ecosystem-generated-run-copy">
              The existing static/local explanation remains the default view. This panel does not read package rows, exchange
              dirs, source URLs, private collector output, raw author identifiers, cookies, tokens, sessions, or secrets.
            </Paragraph>
          </Col>
          <Col xs={24} lg={8}>
            <Button
              type="primary"
              block
              loading={status === 'loading'}
              disabled={!canRequest}
              onClick={handleRequestGeneratedRun}
            >
              Load backend local generated run
            </Button>
          </Col>
        </Row>

        {!canRequest && (
          <Alert
            type="warning"
            showIcon
            message="Generated-run route not enabled for this local mode"
            description="8S-6 supports only Helldivers PSN and Dong/Sun youth football local fixture sample keys. There is no freeform sample_key input."
          />
        )}

        {status === 'error' && (
          <Alert type="warning" showIcon message="Generated-run unavailable" description={safeError} />
        )}

        {generatedRun && (
          <Space direction="vertical" size={14}>
            {isBlockedState && (
              <Alert
                type="warning"
                showIcon
                message="Generated run requires review before interpretation"
                description="Blockers and manual-review states are shown before module outputs. This is not a normal score and does not authorize any action."
              />
            )}

            <Descriptions
              className="ecosystem-generated-run-descriptions"
              size="small"
              bordered
              column={{ xs: 1, sm: 1, md: 1, lg: 2, xl: 2, xxl: 2 }}
              items={[
                { key: 'run_id', label: 'run_id', children: generatedRun.run_id },
                { key: 'run_schema', label: 'run_schema', children: generatedRun.run_schema },
                { key: 'run_status', label: 'run_status', children: generatedRun.run_status },
                { key: 'case_id', label: 'case_id', children: generatedRun.case_id },
                { key: 'sample_id', label: 'sample_id', children: generatedRun.sample_id },
                { key: 'input_package_id', label: 'input_package_id', children: generatedRun.input_package_id || 'not provided' },
                { key: 'input_source_kind', label: 'input_source_kind', children: generatedRun.input_source_kind },
                { key: 'input_scope_note', label: 'input_scope_note', children: generatedRun.input_scope_note },
                { key: 'generated_at', label: 'generated_at', children: generatedRun.generated_at || 'not provided' },
                { key: 'model_version', label: 'model_version', children: generatedRun.model_version },
                { key: 'coefficient_source', label: 'coefficient_source', children: generatedRun.coefficient_source },
                { key: 'calibration_status', label: 'calibration_status', children: generatedRun.calibration_status },
                { key: 'empirical_validation', label: 'empirical_validation', children: generatedRun.empirical_validation },
                {
                  key: 'human_review_required',
                  label: 'human_review_required',
                  children: generatedRun.human_review_required ? 'true' : 'false',
                },
              ]}
            />

            <Card className="ecosystem-generated-run-boundaries" size="small">
              <Space wrap>
                <ShieldCheck size={16} />
                {boundaries.map((item) => (
                  <Tag key={item.key} color={item.enabled ? 'gold' : 'default'}>
                    {item.label}: {item.enabled ? 'true' : 'false'}
                  </Tag>
                ))}
              </Space>
            </Card>

            <RenderSafeList title="Blockers before module outputs" items={generatedRun.blockers || []} color="red" />
            <RenderSafeList title="Warnings" items={generatedRun.warnings || []} color="gold" />

            <Row gutter={[14, 14]}>
              {MODULE_KEYS.map((moduleName) => (
                <Col xs={24} xl={moduleName === 'ResponseStrategyComparisonV01' ? 24 : 12} key={moduleName}>
                  <ModuleOutputCard moduleName={moduleName} outputs={generatedRun.module_outputs?.[moduleName]} />
                </Col>
              ))}
            </Row>
          </Space>
        )}
      </Space>
    </Card>
  )
}
