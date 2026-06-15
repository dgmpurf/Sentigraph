import { Alert, Button, Card, Col, Descriptions, Empty, List, Row, Space, Spin, Tag, Typography } from 'antd'
import { CheckCircle2, Database, FolderOpen, RefreshCw, ShieldCheck, Star, TriangleAlert } from 'lucide-react'
import { useEffect, useMemo, useState } from 'react'

import {
  getExternalCollectorPackage,
  getExternalCollectorStatus,
  listExternalCollectorPackages,
  validateExternalCollectorPackage,
} from '../api/sentigraphApi.js'

const { Paragraph, Text, Title } = Typography

const STATUS_COLOR = {
  pass: 'green',
  warn: 'gold',
  fail: 'red',
  unknown: 'default',
}

const NEXT_ACTION_LABEL = {
  ready_for_sample_review: 'ready for sample review',
  needs_manual_review: 'needs manual review',
  fail_validation: 'fail validation',
  sample_size_warning: 'sample / warning review',
}

const ROLE_LABEL = {
  recommended_demo_sample: '推荐演示样本',
  controlled_public_sample: '受控公开样本',
  local_snapshot_test: 'local snapshot 测试',
  seed_relevance_test: 'seed 相关性测试',
  historical_smoke_test: '历史 smoke 测试',
  unknown_historical_export: '内部测试 / unknown',
}

const ROLE_COLOR = {
  recommended_demo_sample: 'cyan',
  controlled_public_sample: 'blue',
  local_snapshot_test: 'geekblue',
  seed_relevance_test: 'purple',
  historical_smoke_test: 'default',
  unknown_historical_export: 'default',
}

const BOUNDARY_TAGS = [
  'local-only bridge',
  'reads exported evidence packages only',
  'does not run collector jobs',
  'does not call real APIs',
  'does not fetch URLs',
  'does not scrape websites',
  'does not use cookies/accounts',
  'not full-web coverage',
  'not official verification',
  'not causal proof',
]

function statusTag(status) {
  return <Tag color={STATUS_COLOR[status] || 'default'}>{status || 'unknown'}</Tag>
}

function nextActionLabel(value) {
  return NEXT_ACTION_LABEL[value] || value || 'needs manual review'
}

function roleLabel(role) {
  return ROLE_LABEL[role] || '内部测试 / unknown'
}

function roleTag(item) {
  return <Tag color={ROLE_COLOR[item.package_role] || 'default'}>{roleLabel(item.package_role)}</Tag>
}

function demoTag(item) {
  if (item.recommended_for_sentigraph_demo) return <Tag color="cyan">Sentigraph demo recommended</Tag>
  if (item.demo_recommendation) return <Tag color={item.demo_recommendation === 'recommended' ? 'cyan' : 'default'}>{item.demo_recommendation}</Tag>
  return <Tag color="default">not marked as demo sample</Tag>
}

export function ExternalCollectorBridge() {
  const [status, setStatus] = useState(null)
  const [packages, setPackages] = useState([])
  const [selectedPackage, setSelectedPackage] = useState(null)
  const [detail, setDetail] = useState(null)
  const [validation, setValidation] = useState(null)
  const [loading, setLoading] = useState(false)
  const [detailLoading, setDetailLoading] = useState(false)
  const [validating, setValidating] = useState(false)
  const [error, setError] = useState('')

  const loadBridge = async () => {
    setLoading(true)
    setError('')
    try {
      const nextStatus = await getExternalCollectorStatus()
      setStatus(nextStatus)
      if (nextStatus?.configured && nextStatus?.exists) {
        setPackages(await listExternalCollectorPackages())
      } else {
        setPackages([])
      }
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load external collector bridge status.')
      setPackages([])
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadBridge()
  }, [])

  const openPackage = async (packageName) => {
    setSelectedPackage(packageName)
    setDetail(null)
    setValidation(null)
    setDetailLoading(true)
    setError('')
    try {
      setDetail(await getExternalCollectorPackage(packageName))
    } catch (requestError) {
      setError(requestError?.message || 'Unable to load package detail.')
    } finally {
      setDetailLoading(false)
    }
  }

  const runValidation = async (packageName = selectedPackage) => {
    if (!packageName) return
    setSelectedPackage(packageName)
    setValidating(true)
    setError('')
    try {
      setValidation(await validateExternalCollectorPackage(packageName))
    } catch (requestError) {
      setError(requestError?.message || 'Unable to validate package locally.')
    } finally {
      setValidating(false)
    }
  }

  const selectedSummary = useMemo(
    () => packages.find((item) => item.package_name === selectedPackage) || null,
    [packages, selectedPackage],
  )
  const recommendedPackages = useMemo(
    () => packages.filter((item) => item.recommended_for_sentigraph_demo),
    [packages],
  )

  return (
    <div className="page-stack external-collector-page">
      <section className="external-collector-hero">
        <div>
          <Space wrap>
            <Tag color="cyan">local-only bridge</Tag>
            <Tag color="default">Evidence Export package</Tag>
            <Tag color="default">package_index.json optional</Tag>
          </Space>
          <Title level={1}>外部采集桥接 / External Collector Bridge</Title>
          <Paragraph>
            读取私有采集项目已经导出的 Sentigraph Evidence Export v1 包和可选 package_index.json。此页面只做本地导出包发现、摘要查看和安全校验。
          </Paragraph>
          <Space wrap>
            <Button type="primary" icon={<RefreshCw size={16} />} loading={loading} onClick={loadBridge}>
              刷新本地状态
            </Button>
            <Tag color={status?.configured ? 'green' : 'gold'}>{status?.configured ? 'configured' : 'not configured'}</Tag>
            <Tag color={status?.index_available ? 'green' : 'default'}>{status?.index_available ? 'package_index detected' : 'folder scan fallback'}</Tag>
          </Space>
        </div>
        <Card className="panel-card external-collector-status-card">
          <Space direction="vertical" size={12} className="full-width">
            <Text type="secondary">Package count</Text>
            <Title level={2}>{status?.package_count ?? 0}</Title>
            <Text>{status?.message || 'Waiting for local bridge status.'}</Text>
            <Text type="secondary">Env: SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR</Text>
          </Space>
        </Card>
      </section>

      <Alert
        className="external-collector-boundary-alert"
        type="info"
        showIcon
        message="Bridge boundary"
        description={
          <Space wrap>
            {BOUNDARY_TAGS.map((item) => (
              <Tag key={item}>{item}</Tag>
            ))}
          </Space>
        }
      />

      <Alert
        className="external-collector-boundary-alert"
        type="warning"
        showIcon
        message="验证状态说明"
        description="passed 只代表结果 / 安全检查通过，不等于推荐演示样本，也不代表全网全量、全平台覆盖或官方验证。请优先使用标记为推荐演示样本的 selected public sample。"
      />

      {status?.index_warning ? <Alert type="warning" showIcon message="package_index.json warning" description={status.index_warning} /> : null}
      {error ? <Alert type="error" showIcon message={error} /> : null}

      {recommendedPackages.length ? (
        <Card
          className="panel-card external-collector-recommended-card"
          title={
            <Space>
              <Star size={17} />
              <span>推荐演示样本</span>
            </Space>
          }
        >
          <Row gutter={[12, 12]}>
            {recommendedPackages.map((item) => (
              <Col span={12} key={item.package_name}>
                <div className="external-collector-recommended-tile">
                  <Space wrap>
                    <Text strong>{item.package_name}</Text>
                    {roleTag(item)}
                    {statusTag(item.validation_status)}
                  </Space>
                  <Paragraph>{item.case_title || item.case_id || 'Recommended package from package_index.json'}</Paragraph>
                  <Space wrap>
                    <Tag>{item.evidence_count} evidence</Tag>
                    <Tag>{item.source_count} sources</Tag>
                    <Tag>{item.comment_count} comments</Tag>
                    <Tag>{item.root_count} roots</Tag>
                    {item.sample_quality_label ? <Tag color="cyan">{item.sample_quality_label}</Tag> : null}
                  </Space>
                  <Space className="external-collector-tile-actions">
                    <Button type="primary" onClick={() => openPackage(item.package_name)}>查看推荐样本</Button>
                    <Button onClick={() => runValidation(item.package_name)} loading={validating && selectedPackage === item.package_name}>
                      本地验证
                    </Button>
                  </Space>
                </div>
              </Col>
            ))}
          </Row>
        </Card>
      ) : null}

      <Row gutter={[16, 16]}>
        <Col span={9}>
          <Card
            className="panel-card external-collector-setup-card"
            title={
              <Space>
                <FolderOpen size={17} />
                <span>Setup status</span>
              </Space>
            }
          >
            <Descriptions column={1} size="small">
              <Descriptions.Item label="configured">{String(Boolean(status?.configured))}</Descriptions.Item>
              <Descriptions.Item label="exists">{String(Boolean(status?.exists))}</Descriptions.Item>
              <Descriptions.Item label="index">{status?.index_available ? 'package_index.json' : 'folder scan fallback'}</Descriptions.Item>
              <Descriptions.Item label="exports_dir">{status?.exports_dir || 'not configured'}</Descriptions.Item>
              <Descriptions.Item label="suggested env">{status?.suggested_env_var || 'SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR'}</Descriptions.Item>
              <Descriptions.Item label="suggested local path">
                {status?.suggested_local_path || 'G:\\AICODING\\网页端任务二\\exports\\sentigraph-evidence-v1'}
              </Descriptions.Item>
            </Descriptions>
            {!status?.configured ? (
              <Alert
                className="external-collector-inline-alert"
                type="warning"
                showIcon
                message="Not configured"
                description="Set SENTIGRAPH_EXTERNAL_COLLECTOR_EXPORTS_DIR before starting the backend. The app will keep running when it is absent."
              />
            ) : null}
          </Card>
        </Col>
        <Col span={15}>
          <Card
            className="panel-card external-collector-package-card"
            title={
              <Space>
                <Database size={17} />
                <span>Available packages</span>
              </Space>
            }
          >
            <Spin spinning={loading}>
              {packages.length ? (
                <List
                  dataSource={packages}
                  renderItem={(item) => (
                    <List.Item>
                      <div className={`external-collector-package-row ${item.recommended_for_sentigraph_demo ? 'recommended' : 'subdued'}`}>
                        <div>
                          <Space wrap>
                            <Text strong>{item.package_name}</Text>
                            {roleTag(item)}
                            {demoTag(item)}
                            {statusTag(item.validation_status)}
                            <Tag color="default">{nextActionLabel(item.recommended_next_action)}</Tag>
                          </Space>
                          <Paragraph>{item.case_title || item.case_id || 'No case title in manifest or index'}</Paragraph>
                          <Space wrap>
                            <Tag>{item.evidence_count} evidence</Tag>
                            <Tag>{item.source_count} sources</Tag>
                            <Tag>{item.comment_count} comments</Tag>
                            <Tag>{item.root_count} roots</Tag>
                            <Tag color={item.warnings_count ? 'gold' : 'green'}>{item.warnings_count} warnings</Tag>
                            <Tag color={item.errors_count ? 'red' : 'green'}>{item.errors_count} errors</Tag>
                            {item.sample_quality_label ? <Tag>{item.sample_quality_label}</Tag> : null}
                            {item.exported_at ? <Tag>{item.exported_at}</Tag> : null}
                          </Space>
                        </div>
                        <Space>
                          <Button type={item.recommended_for_sentigraph_demo ? 'primary' : 'default'} onClick={() => openPackage(item.package_name)}>
                            查看详情
                          </Button>
                          <Button onClick={() => runValidation(item.package_name)} loading={validating && selectedPackage === item.package_name}>
                            本地验证
                          </Button>
                        </Space>
                      </div>
                    </List.Item>
                  )}
                />
              ) : (
                <Empty description={status?.configured ? 'No package folders found.' : 'Configure exports dir to list packages.'} />
              )}
            </Spin>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col span={12}>
          <Card className="panel-card external-collector-detail-card" title="Package detail / 包详情">
            <Spin spinning={detailLoading}>
              {detail ? (
                <Space direction="vertical" size={12} className="full-width">
                  <Space wrap>
                    <Tag color="cyan">{detail.package_name}</Tag>
                    {roleTag(detail)}
                    {demoTag(detail)}
                    <Tag>{nextActionLabel(detail.recommended_next_action)}</Tag>
                  </Space>
                  <Descriptions column={1} size="small">
                    <Descriptions.Item label="case_id">{detail.manifest_summary?.case_id || ''}</Descriptions.Item>
                    <Descriptions.Item label="case_title">{detail.manifest_summary?.case_title || ''}</Descriptions.Item>
                    <Descriptions.Item label="evidence">{detail.manifest_summary?.evidence_count || 0}</Descriptions.Item>
                    <Descriptions.Item label="sources">{detail.manifest_summary?.source_count || 0}</Descriptions.Item>
                    <Descriptions.Item label="validation">{detail.validation_report_summary?.status || 'unknown'}</Descriptions.Item>
                    <Descriptions.Item label="package_role">{detail.package_role || 'not indexed'}</Descriptions.Item>
                    <Descriptions.Item label="demo_recommendation">{detail.demo_recommendation || 'not indexed'}</Descriptions.Item>
                    <Descriptions.Item label="recommended_for_demo">{String(Boolean(detail.recommended_for_sentigraph_demo))}</Descriptions.Item>
                    <Descriptions.Item label="sample_quality">{detail.sample_quality_label || 'not indexed'}</Descriptions.Item>
                    <Descriptions.Item label="index source">{detail.index_source || 'folder scan fallback'}</Descriptions.Item>
                    <Descriptions.Item label="notes">{detail.index_notes || 'No index notes.'}</Descriptions.Item>
                  </Descriptions>
                  <div className="external-collector-file-grid">
                    {Object.entries(detail.expected_files || {}).map(([fileName, exists]) => (
                      <Tag key={fileName} color={exists ? 'green' : 'red'}>
                        {fileName}: {exists ? 'present' : 'missing'}
                      </Tag>
                    ))}
                  </div>
                  <Alert
                    type="info"
                    showIcon
                    message="Coverage limitations"
                    description={detail.coverage_note_excerpt || detail.manifest_summary?.coverage_note || 'No coverage note excerpt.'}
                  />
                  <Paragraph type="secondary">{detail.readme_excerpt}</Paragraph>
                </Space>
              ) : (
                <Empty description={selectedSummary ? 'Loading package detail...' : 'Select a package to inspect manifest, package_index metadata, and validation summaries.'} />
              )}
            </Spin>
          </Card>
        </Col>
        <Col span={12}>
          <Card className="panel-card external-collector-validation-card" title="Local validation / 本地验证">
            <Spin spinning={validating}>
              {validation ? (
                <Space direction="vertical" size={12} className="full-width">
                  <Space wrap>
                    {statusTag(validation.status)}
                    <Tag>{validation.privacy_status} privacy</Tag>
                    <Tag>{validation.coverage_status} coverage</Tag>
                    <Tag>{nextActionLabel(validation.recommended_next_action)}</Tag>
                  </Space>
                  <Row gutter={[10, 10]}>
                    {Object.entries(validation.counts || {}).map(([key, value]) => (
                      <Col span={8} key={key}>
                        <div className="external-collector-count-tile">
                          <Text type="secondary">{key}</Text>
                          <strong>{value}</strong>
                        </div>
                      </Col>
                    ))}
                  </Row>
                  <ValidationIssueList title="Errors" items={validation.errors || []} icon={<TriangleAlert size={16} />} />
                  <ValidationIssueList title="Warnings" items={validation.warnings || []} icon={<CheckCircle2 size={16} />} />
                  <Alert
                    type="info"
                    showIcon
                    message="Safety note"
                    description="Validation is local and read-only. It checks expected files, JSON parsing, coverage language, and raw identity / secret-like key names. It does not import evidence into backend cases."
                  />
                </Space>
              ) : (
                <Empty description="Click 本地验证 on a package to see local validation output." />
              )}
            </Spin>
          </Card>
        </Col>
      </Row>

      <Card
        className="panel-card external-collector-next-card"
        title={
          <Space>
            <ShieldCheck size={17} />
            <span>Next action / 下一步</span>
          </Space>
        }
      >
        <Space direction="vertical" size={8}>
          <Paragraph>如果 package 通过验证，可以复制到 <Text code>docs/samples/...</Text> 或生成 frontend fixture。</Paragraph>
          <Paragraph>当前页面暂不自动运行采集任务，也不把 package 导入后端数据存储。</Paragraph>
          <Paragraph>若要生成新 package，请到私有 collector 项目运行 export 命令，并在本页刷新桥接状态。</Paragraph>
        </Space>
      </Card>
    </div>
  )
}

function ValidationIssueList({ icon, items, title }) {
  return (
    <div>
      <Space>
        {icon}
        <Text strong>{title}</Text>
      </Space>
      {items.length ? (
        <List
          size="small"
          dataSource={items}
          renderItem={(item) => (
            <List.Item>
              <Space direction="vertical" size={2}>
                <Text strong>{item.code || 'ISSUE'}</Text>
                <Text type="secondary">{item.message || ''}</Text>
              </Space>
            </List.Item>
          )}
        />
      ) : (
        <Paragraph type="secondary">None.</Paragraph>
      )}
    </div>
  )
}
